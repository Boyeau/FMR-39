"""
exp_QCD_etalon.py
===================================================================
Campagne instrumentee : la meme que `exp_QCD_campagne.py`, plus l'etalon
d'adaptation adosse a la VERITE ANALYTIQUE.

Meme contrat que la campagne d'origine, et il n'est pas negociable : ce script
n'ecrit que de la MATIERE PREMIERE. Aucun seuil, aucun `lambda`, aucun `tau`,
aucune aire. Les comptages ci-dessous se relisent hors ligne pour construire
acc_bande / acc_haut / acc_bas et V(t), et pour balayer les fenetres sans
repayer une campagne.

L'ETALON, ET POURQUOI IL N'A BESOIN D'AUCUNE FORET DE REFERENCE
    Le dispositif connait sa propre verite : apres la rupture, y*(x) = 1{x0+x1 > b},
    et l'erreur de Bayes est nulle (JOURNAL § 2a). Inutile donc de comparer la foret
    a une copie gelee d'elle-meme — c'etait la circularite qui a tue la v1 du plan.
    On sonde directement trois regions dont la verite est connue :

        R_bande   0 < x0+x1 <= b     avant 1, apres 0   ce qu'il faut REAPPRENDRE
        R_haut        x0+x1 >  b     avant 1, apres 1   competence a CONSERVER
        R_bas         x0+x1 <= 0     avant 0, apres 0   competence a CONSERVER

    R_haut et R_bas ne sont pas decoratives : une foret qui s'effondre sur
    « toujours 0 » saturerait acc_bande a 1 en ayant tout desappris. Sans elles,
    le controle certifierait la degenerescence au lieu de la detecter.

LOI DES SONDES — declaree ici, avant toute mesure
    x0 + x1 ~ N(0, 2), donc sigma_s = sqrt(2). On tire d'abord s = x0 + x1
    UNIFORMEMENT sur l'intervalle de la region, a distance fixee de ses bords :

        R_bande   s ~ U(0.05*b,  0.95*b)
        R_haut    s ~ U(b + 0.05*sigma_s,  b + 2*sigma_s)
        R_bas     s ~ U(-2*sigma_s,  -0.05*sigma_s)

    puis on complete par la composante orthogonale v ~ N(0,1) :

        x0 = s/2 + v/sqrt(2)        x1 = s/2 - v/sqrt(2)

    ce qui redonne exactement la loi de N(0, I2) conditionnee a x0+x1 = s.
    L'echantillonnage CONDITIONNEL a la region est ce qui donne la meme precision
    a toute amplitude, y compris quand la bande n'a qu'une masse de 2,8 % — un
    tirage dans le flux y placerait 6 sondes sur 200.

    Les sondes sont tirees par un `Generator` SEPARE, de graine fixe : elles sont
    donc IDENTIQUES pour tous les runs d'une meme amplitude, et leur erreur
    d'echantillonnage est un biais partage (mesure en tache 5, controle 5). Elles
    ne sont JAMAIS apprises, et `controle_api_structure.py` etablit que
    `predict_one` ne consomme pas d'alea : le flux n'est pas decale d'un bit.

CE QUI S'AJOUTE A LA CAMPAGNE D'ORIGINE, tous les PAS_SONDE pas post-rupture
    - table `sondes` : par (run, t, region), le nombre de sondes ou le VOTE de la
      foret donne la nouvelle etiquette, et celui ou il donne l'ancienne ;
    - table `votes`  : par (run, t, region), les comptages de dissensus entre
      arbres SUR CES MEMES SONDES, d'ou V(t) se calcule hors ligne.

    Le dissensus est mesure sur les sondes fixes et NON sur l'instance courante du
    flux : sur le flux il depend surtout de l'endroit ou tombe l'instance, ce qui
    le rend correle a e_t, donc au signal meme que lit le detecteur. La mesure
    serait circulaire, exactement comme le « retour de l'erreur ».

CONVENTION DE VOTE — arretee par `controle_api_structure.py`, appliquee partout
    Un arbre dont `predict_one` renvoie None (arbre de secours neuf) est EXCLU du
    vote ; le denominateur est le nombre d'arbres AYANT vote. Les compter comme un
    vote pour la classe 0 biaiserait acc_bande vers le haut juste apres un
    remplacement, c'est-a-dire au moment precis que la mesure doit decrire.

USAGE
    PYTHONHASHSEED=0 python exp_QCD_etalon.py                  # pilote 5 x 20
    PYTHONHASHSEED=0 python exp_QCD_etalon.py --full           # grille 20 x 100
    PYTHONHASHSEED=0 python exp_QCD_etalon.py --no-drift       # ligne de base b = 0
"""

import argparse
import random
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from scipy.stats import norm
from tqdm import tqdm

from river import drift
from river.forest import ARFClassifier

warnings.filterwarnings('ignore')

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "resultats" / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# --- Parametres du dispositif, identiques a exp_QCD_campagne.py ------------------
N_MODELS = 10
C_INT = 1
T_DRIFT = 4000
H = 2000
BOUNDARY_SHIFTS = np.linspace(0.1, 4.0, 20)
BASELINE_DEFAULT = 3000
BASELINE_MAX = 3000

PROTO_SHIFTS = BOUNDARY_SHIFTS[[0, 4, 9, 14, 19]]
PROTO_SEEDS = 20
FULL_SEEDS = 100

# --- Parametres de l'etalon, declares avant toute mesure -------------------------
N_SONDES = 200            # par region
PAS_SONDE = 25            # un releve tous les 25 pas post-rupture -> 80 releves
SEED_SONDES = 20260908    # graine du generateur SEPARE des sondes
MARGE = 0.05              # distance relative aux bords de la region
LARGEUR_QUEUE = 2.0       # en sigma_s, pour les regions non bornees
SIGMA_S = float(np.sqrt(2.0))
REGIONS = ('bande', 'haut', 'bas')


def delta_e(boundary_shift):
    """Amplitude du saut d'erreur induite par une translation `b` de la frontiere."""
    return float(norm.cdf(boundary_shift / np.sqrt(2)) - 0.5)


def tirer_sondes(boundary_shift, n=N_SONDES, seed=SEED_SONDES):
    """Les trois jeux de sondes d'une amplitude. Loi declaree dans l'en-tete.

    Renvoie {region: (X, y_avant, y_apres)}, X de forme (n, 2).
    Le generateur est propre a ce tirage : il ne touche jamais l'alea du flux.
    """
    g = np.random.default_rng(seed)
    b = float(boundary_shift)
    intervalles = {
        # La bande n'existe que si b > 0. A b = 0 elle est vide : la ligne de base
        # A1 reutilise les sondes de l'amplitude comparee, elle ne les retire pas.
        'bande': (MARGE * b, (1.0 - MARGE) * b),
        'haut': (b + MARGE * SIGMA_S, b + LARGEUR_QUEUE * SIGMA_S),
        'bas': (-LARGEUR_QUEUE * SIGMA_S, -MARGE * SIGMA_S),
    }
    jeux = {}
    for region in REGIONS:
        lo, hi = intervalles[region]
        s = g.uniform(lo, hi, size=n)
        v = g.normal(size=n)
        X = np.column_stack([s / 2.0 + v / np.sqrt(2.0), s / 2.0 - v / np.sqrt(2.0)])
        # Verite avant et apres la rupture, connue analytiquement region par region.
        y_avant = (s > 0.0).astype(np.int8)
        y_apres = (s > b).astype(np.int8)
        jeux[region] = (X, y_avant, y_apres)
    return jeux


def sonder(arf, jeux):
    """Un releve : vote de la foret et dissensus entre arbres, sur les trois regions.

    N'ecrit que des COMPTAGES. Aucun taux, aucun seuil : acc_*(t) et V(t) se
    construisent hors ligne a partir de ces colonnes.
    """
    lignes_sondes, lignes_votes = [], []
    arbres = arf.data
    for region in REGIONS:
        X, y_avant, y_apres = jeux[region]
        n_nouvelle = n_ancienne = 0
        somme_votants = somme_votes_1 = somme_desaccord = 0
        for i in range(X.shape[0]):
            x = {0: float(X[i, 0]), 1: float(X[i, 1])}
            # Convention arretee par controle_api_structure.py : un arbre muet est
            # exclu du vote, le denominateur est le nombre d'arbres ayant vote.
            votes = [a.predict_one(x) for a in arbres]
            exprimes = [int(v) for v in votes if v is not None]
            if not exprimes:
                continue
            n_votants = len(exprimes)
            n_un = sum(exprimes)
            majorite = int(n_un * 2 > n_votants)
            n_nouvelle += int(majorite == y_apres[i])
            n_ancienne += int(majorite == y_avant[i])
            somme_votants += n_votants
            somme_votes_1 += n_un
            somme_desaccord += n_votants - max(n_un, n_votants - n_un)
        lignes_sondes.append((region, X.shape[0], n_nouvelle, n_ancienne))
        lignes_votes.append((region, somme_votants, somme_votes_1, somme_desaccord))
    return lignes_sondes, lignes_votes


def run_one(boundary_shift, seed, baseline_window, n_models=N_MODELS, sans_drift=False,
            seed_sondes=SEED_SONDES):
    """Une execution instrumentee.

    Le rodage, la graine et l'ordre des tirages du flux sont INCHANGES par rapport
    a `exp_QCD_campagne.py` : c'est ce qui rend le controle de non-regression bit a
    bit possible (tache 4).
    """
    safe_seed = int(seed % (2 ** 31 - 1))
    random.seed(safe_seed)
    np.random.seed(safe_seed)
    rng = np.random.default_rng(safe_seed)

    arf = ARFClassifier(
        n_models=n_models, seed=safe_seed,
        drift_detector=drift.ADWIN(clock=C_INT),
        warning_detector=drift.ADWIN(clock=C_INT),
    )

    # Les sondes suivent le `b` de la cellule, y compris sans drift : la ligne de
    # base A1 compare la MEME question posee a une foret que rien n'a perturbee.
    jeux = tirer_sondes(boundary_shift, seed=seed_sondes)

    errors_pre = []
    pre_series = np.zeros(BASELINE_MAX, dtype=np.int8)
    p_hat_0 = None
    prev_counts = {}
    error_series = np.zeros(H, dtype=np.int8)
    events = []
    releves_sondes, releves_votes = [], []

    for t in range(T_DRIFT + H):
        x0, x1 = rng.normal(), rng.normal()
        x_dict = {0: x0, 1: x1}
        if t < T_DRIFT or sans_drift:
            y = int(x0 + x1 > 0.0)
        else:
            y = int(x0 + x1 > boundary_shift)

        y_pred = arf.predict_one(x_dict) or 0
        error = int(y_pred != y)

        if t < T_DRIFT:
            if t >= T_DRIFT - BASELINE_MAX:
                pre_series[t - (T_DRIFT - BASELINE_MAX)] = error
            if t >= T_DRIFT - baseline_window:
                errors_pre.append(error)
        elif t == T_DRIFT:
            p_hat_0 = float(np.mean(errors_pre)) if errors_pre else 0.05
            prev_counts = dict(arf._drift_tracker)

        arf.learn_one(x_dict, y)

        if t >= T_DRIFT:
            idx = t - T_DRIFT
            error_series[idx] = error
            for tid, v in arf._drift_tracker.items():
                if v > prev_counts.get(tid, 0):
                    events.append((idx, int(tid)))
                    prev_counts[tid] = v
            if idx % PAS_SONDE == 0:
                ls, lv = sonder(arf, jeux)
                releves_sondes.extend((idx,) + row for row in ls)
                releves_votes.extend((idx,) + row for row in lv)

    meta = {
        'boundary_shift': float(boundary_shift),
        'delta_e': 0.0 if sans_drift else delta_e(boundary_shift),
        'delta_e_sondes': delta_e(boundary_shift),   # amplitude des sondes, meme sans drift
        'seed': int(seed),
        'p_hat_0': p_hat_0,
        'baseline_window': int(baseline_window),
        'n_models': int(n_models),
        'sans_drift': bool(sans_drift),
        'n_sondes': int(N_SONDES),
        'pas_sonde': int(PAS_SONDE),
        'seed_sondes': int(seed_sondes),
    }
    return meta, error_series, events, pre_series, releves_sondes, releves_votes


def assembler(results, run_id0):
    """Met en tables les resultats d'une amplitude. Aucun calcul derive."""
    metas, traces, pres, evs, sondes, votes = [], [], [], [], [], []
    for k, (meta, err, events, pre, rs, rv) in enumerate(results):
        run_id = run_id0 + k
        meta = dict(meta, run_id=run_id)
        metas.append(meta)
        traces.append(pd.DataFrame({
            'run_id': np.full(H, run_id, dtype=np.int32),
            't': np.arange(H, dtype=np.int16),
            'e': err,
        }))
        pres.append(pd.DataFrame({
            'run_id': np.full(BASELINE_MAX, run_id, dtype=np.int32),
            't_pre': np.arange(-BASELINE_MAX, 0, dtype=np.int16),
            'e': pre,
        }))
        if events:
            ev = np.asarray(events, dtype=np.int32)
            evs.append(pd.DataFrame({
                'run_id': np.full(len(ev), run_id, dtype=np.int32),
                't': ev[:, 0].astype(np.int16),
                'tree_id': ev[:, 1].astype(np.int8),
            }))
        if rs:
            sondes.append(pd.DataFrame(
                [(run_id,) + row for row in rs],
                columns=['run_id', 't', 'region', 'n_sondes', 'n_vote_nouvelle',
                         'n_vote_ancienne']))
            votes.append(pd.DataFrame(
                [(run_id,) + row for row in rv],
                columns=['run_id', 't', 'region', 'somme_votants', 'somme_votes_1',
                         'somme_desaccord']))
    return metas, traces, pres, evs, sondes, votes


def ecrire(chemin, frames, colonnes_vides=None):
    """Ecriture incrementale : la campagne survit a une interruption."""
    if not frames:
        if colonnes_vides is not None and not chemin.exists():
            pd.DataFrame(colonnes_vides).to_parquet(chemin, index=False)
        return
    df = pd.concat(frames, ignore_index=True)
    if chemin.exists():
        df = pd.concat([pd.read_parquet(chemin), df], ignore_index=True)
    df.to_parquet(chemin, index=False)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--full', action='store_true', help="grille 20 amplitudes x 100 graines")
    ap.add_argument('--seeds', type=int, default=None)
    ap.add_argument('--baseline', type=int, default=BASELINE_DEFAULT)
    ap.add_argument('--tag', type=str, default=None)
    ap.add_argument('--jobs', type=int, default=-1)
    ap.add_argument('--models', type=int, default=N_MODELS)
    ap.add_argument('--seed-sondes', type=int, default=SEED_SONDES,
                    help="graine du tirage des sondes. Un SECOND tirage mesure le biais "
                         "partage par tous les runs d'une amplitude, que le bootstrap sur "
                         "les graines ne capture pas (tache 5, controle 5)")
    ap.add_argument('--no-drift', action='store_true',
                    help="ligne de base : la regle ne change jamais, mais les sondes "
                         "restent celles de l'amplitude comparee (acc_bande doit rester ~ 0)")
    args = ap.parse_args()

    if args.full:
        shifts, n_seeds, tag = BOUNDARY_SHIFTS, args.seeds or FULL_SEEDS, args.tag or 'full'
    else:
        shifts, n_seeds, tag = PROTO_SHIFTS, args.seeds or PROTO_SEEDS, args.tag or 'pilote'
    if args.baseline != BASELINE_DEFAULT:
        tag = f"{tag}_base{args.baseline}"
    if args.no_drift:
        tag = f"{tag}_nodrift"
    if args.seed_sondes != SEED_SONDES:
        tag = f"{tag}_sondes{args.seed_sondes}"
    tag = f"{tag}_M{args.models}"

    seeds = list(range(1, n_seeds + 1))
    n_total = len(shifts) * len(seeds)
    chemins = {
        'meta': DATA_DIR / f"QCD_etalon_meta_{tag}.parquet",
        'traces': DATA_DIR / f"QCD_etalon_traces_error_{tag}.parquet",
        'pre': DATA_DIR / f"QCD_etalon_traces_pre_{tag}.parquet",
        'events': DATA_DIR / f"QCD_etalon_events_swap_{tag}.parquet",
        'sondes': DATA_DIR / f"QCD_etalon_sondes_{tag}.parquet",
        'votes': DATA_DIR / f"QCD_etalon_votes_{tag}.parquet",
    }

    # Reprise : une amplitude deja complete n'est pas recalculee. Sans cela, une
    # campagne tuee en route est integralement perdue.
    faits = set()
    if chemins['meta'].exists():
        deja = pd.read_parquet(chemins['meta'])
        comptes = deja.groupby('boundary_shift').size()
        faits = set(comptes[comptes >= len(seeds)].index)
        if faits:
            print(f"[RESUME] {len(faits)}/{len(shifts)} amplitudes deja completes, on continue.")

    print(f"[INFO] {len(shifts)} amplitudes x {n_seeds} graines = {n_total} executions | "
          f"H = {H} | M = {args.models} | sondes {N_SONDES}/region tous les {PAS_SONDE} pas"
          + (" | SANS DRIFT (ligne de base)" if args.no_drift else ""))
    # ETA annoncee AVANT de lancer, jamais apres : ~3,25 s/run a M = 10, +19 % de
    # surcout de sondage mesure par controle_api_structure.py.
    n_jobs_eff = args.jobs if args.jobs > 0 else 8
    eta = n_total * 3.25 * 1.19 * (args.models / N_MODELS) / n_jobs_eff / 60
    print(f"[ETA ] ~{eta:.0f} min sur {n_jobs_eff} coeurs")

    t0 = time.time()
    run_id0 = 0 if not faits else int(pd.read_parquet(chemins['meta'])['run_id'].max()) + 1
    for i, b in enumerate(tqdm(shifts, desc=tag, unit="amplitude")):
        if b in faits:
            continue
        res = Parallel(n_jobs=args.jobs)(
            delayed(run_one)(b, s, args.baseline, args.models, args.no_drift,
                             args.seed_sondes) for s in seeds
        )
        metas, traces, pres, evs, sondes, votes = assembler(res, run_id0)
        run_id0 += len(res)
        ecrire(chemins['meta'], [pd.DataFrame(metas)])
        ecrire(chemins['traces'], traces)
        ecrire(chemins['pre'], pres)
        ecrire(chemins['events'], evs,
               colonnes_vides={'run_id': pd.Series(dtype=np.int32),
                               't': pd.Series(dtype=np.int16),
                               'tree_id': pd.Series(dtype=np.int8)})
        ecrire(chemins['sondes'], sondes)
        ecrire(chemins['votes'], votes)
        print(f"[CHECKPOINT] amplitude {i + 1}/{len(shifts)} (b = {b:.3f}) ecrite "
              f"| {(time.time() - t0) / 60:.1f} min ecoulees")

    elapsed = time.time() - t0
    print(f"[INFO] termine en {elapsed / 60:.1f} min ({elapsed / max(n_total, 1):.2f} s/run)")
    print(f"[SUCCESS] ecrit dans {DATA_DIR} (tag = {tag})")


if __name__ == "__main__":
    main()
