"""
exp_bis_pilote_arbres.py
===================================================================
Pilote instrumente PAR ARBRE, pour la question D.1.bis du mail du 15 septembre
(`repo/01_consignes/Questions_bis_15sept.md`).

POURQUOI UNE CAMPAGNE, ET PAS UNE ANALYSE HORS LIGNE
    Aucune table existante ne porte l'erreur par arbre par pas. `exp_QCD_campagne.py`
    n'enregistre que l'erreur de la FORET ; `exp_QCD_etalon.py` interroge bien chaque
    arbre mais somme immediatement sur les 10 arbres et les 200 sondes. La variance
    transversale demandee par D.1.bis n'est donc pas calculable depuis les Parquet :
    ce script est une decision, prise avec son cout annonce, pas une verification.

CE QUI EST ENREGISTRE
    Une ligne par (run, pas post-rupture, arbre) : l'erreur de cet arbre sur le point
    du flux, et s'il a vote. Rien d'autre. Aucun indicateur, aucune fenetre, aucune
    variance : tout le derive se recalcule hors ligne, comme pour la campagne.

CONTROLE OBLIGATOIRE : NON-REGRESSION BIT A BIT
    L'erreur de FORET produite ici doit reproduire `QCD_traces_error_full` a
    l'identique sur les memes (amplitude, graine). Si elle ne le fait pas, le sondage
    par arbre a consomme de l'alea ou decale l'ordre des tirages, et le pilote ne se
    lit pas. `--controle` s'arrete alors en erreur.

    L'ordre des operations de `exp_QCD_campagne.py::run_one` est repris tel quel :
    tirage du point, predict_one de la foret, sondage des arbres (qui ne consomme
    aucun alea, cf. controle_api_structure.py), puis learn_one.

USAGE
    PYTHONHASHSEED=0 python exp_bis_pilote_arbres.py --chrono     # cout d'un run
    PYTHONHASHSEED=0 python exp_bis_pilote_arbres.py --controle   # 1 run, bit a bit
    PYTHONHASHSEED=0 python exp_bis_pilote_arbres.py --pilote     # 5 x 20, defaut
    PYTHONHASHSEED=0 python exp_bis_pilote_arbres.py --pilote --amplitudes 3
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

# --- Parametres repris SANS MODIFICATION de exp_QCD_campagne.py ----------------
N_MODELS = 10
C_INT = 1
T_DRIFT = 4000
H = 2000
BOUNDARY_SHIFTS = np.linspace(0.1, 4.0, 20)
BASELINE_DEFAULT = 3000
BASELINE_MAX = 3000

# --- Grille reduite du pilote ---------------------------------------------------
PILOTE_IDX_5 = [0, 4, 9, 14, 19]      # memes 5 amplitudes que PROTO_SHIFTS
PILOTE_IDX_3 = [0, 9, 19]             # repli si le cout depasse 15 min
PILOTE_SEEDS = 20
BUDGET_LANCEMENT_S = 15 * 60          # seuil declare AVANT le chronometrage
BUDGET_REPLI_S = 45 * 60


def delta_e(boundary_shift):
    return float(norm.cdf(boundary_shift / np.sqrt(2)) - 0.5)


def run_one(boundary_shift, seed, baseline_window=BASELINE_DEFAULT, n_models=N_MODELS):
    """Une execution. Identique a exp_QCD_campagne.py::run_one, plus le sondage
    par arbre a chaque pas post-rupture."""
    safe_seed = int(seed % (2 ** 31 - 1))
    random.seed(safe_seed)
    np.random.seed(safe_seed)
    rng = np.random.default_rng(safe_seed)

    arf = ARFClassifier(
        n_models=n_models, seed=safe_seed,
        drift_detector=drift.ADWIN(clock=C_INT),
        warning_detector=drift.ADWIN(clock=C_INT),
    )

    errors_pre = []
    p_hat_0 = None
    prev_counts = {}
    error_series = np.zeros(H, dtype=np.int8)
    err_arbres = np.zeros((H, n_models), dtype=np.int8)
    vote_arbres = np.zeros((H, n_models), dtype=np.int8)
    events = []

    for t in range(T_DRIFT + H):
        x0, x1 = rng.normal(), rng.normal()
        x_dict = {0: x0, 1: x1}
        y = int(x0 + x1 > 0.0) if t < T_DRIFT else int(x0 + x1 > boundary_shift)

        y_pred = arf.predict_one(x_dict) or 0
        error = int(y_pred != y)

        if t < T_DRIFT:
            if t >= T_DRIFT - baseline_window:
                errors_pre.append(error)
        elif t == T_DRIFT:
            p_hat_0 = float(np.mean(errors_pre)) if errors_pre else 0.05
            prev_counts = dict(arf._drift_tracker)

        if t >= T_DRIFT:
            # Sondage par arbre AVANT learn_one, sur le point du flux. Convention
            # de controle_api_structure.py : un arbre muet ne vote pas, et son
            # erreur ne compte pas. predict_one ne consomme aucun alea.
            idx = t - T_DRIFT
            for m, arbre in enumerate(arf.data):
                v = arbre.predict_one(x_dict)
                if v is None:
                    continue
                vote_arbres[idx, m] = 1
                err_arbres[idx, m] = int(int(v) != y)

        arf.learn_one(x_dict, y)

        if t >= T_DRIFT:
            idx = t - T_DRIFT
            error_series[idx] = error
            for tid, v in arf._drift_tracker.items():
                if v > prev_counts.get(tid, 0):
                    events.append((idx, int(tid)))
                    prev_counts[tid] = v

    meta = {
        'boundary_shift': float(boundary_shift),
        'delta_e': delta_e(boundary_shift),
        'seed': int(seed),
        'p_hat_0': p_hat_0,
        'baseline_window': int(baseline_window),
        'n_models': int(n_models),
    }
    return meta, error_series, err_arbres, vote_arbres, events


def trace_reference(delta_e_cible, seed):
    """Trajectoire d'erreur de foret deja publiee, pour le controle bit a bit."""
    meta = pd.read_parquet(DATA_DIR / "QCD_runs_meta_full.parquet")
    lignes = meta[(np.abs(meta.delta_e - delta_e_cible) < 1e-12) & (meta.seed == seed)]
    if lignes.empty:
        raise ValueError(f"aucun run de reference pour delta_e={delta_e_cible}, seed={seed}")
    run_id = int(lignes.run_id.iloc[0])
    tr = pd.read_parquet(DATA_DIR / "QCD_traces_error_full.parquet")
    tr = tr[tr.run_id == run_id].sort_values("t")
    return tr.e.to_numpy().astype(np.int8), run_id


def controle_bit_a_bit(boundary_shift, seed):
    """Le pilote doit reproduire la campagne a l'identique. Sinon il ne se lit pas."""
    t0 = time.time()
    meta, serie, _, _, _ = run_one(boundary_shift, seed)
    duree = time.time() - t0
    ref, run_id = trace_reference(meta['delta_e'], seed)
    ecarts = int(np.sum(serie != ref))
    print(f"[CONTROLE] run_id de reference {run_id} | delta_e = {meta['delta_e']:.6f} | "
          f"graine {seed}")
    print(f"[CONTROLE] pas differents : {ecarts} / {H} | duree d'un run : {duree:.1f} s")
    if ecarts:
        raise SystemExit("[ECHEC] le sondage par arbre a modifie la trajectoire : "
                         "l'alea a ete consomme ou l'ordre des tirages decale. "
                         "Le pilote ne se lit pas.")
    print("[OK] reproduction bit a bit de QCD_traces_error_full")
    return duree


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--chrono', action='store_true',
                    help="chronometre un run et annonce l'ETA, sans rien ecrire")
    ap.add_argument('--controle', action='store_true',
                    help="un run, compare bit a bit a QCD_traces_error_full")
    ap.add_argument('--pilote', action='store_true', help="lance le pilote complet")
    ap.add_argument('--amplitudes', type=int, default=5, choices=(3, 5))
    ap.add_argument('--seeds', type=int, default=PILOTE_SEEDS)
    ap.add_argument('--jobs', type=int, default=-1)
    ap.add_argument('--tag', type=str, default='pilote')
    args = ap.parse_args()

    idx = PILOTE_IDX_5 if args.amplitudes == 5 else PILOTE_IDX_3
    shifts = BOUNDARY_SHIFTS[idx]

    if args.chrono or args.controle:
        duree = controle_bit_a_bit(float(BOUNDARY_SHIFTS[9]), 1)
        n = len(shifts) * args.seeds
        import os
        coeur = os.cpu_count() or 1
        eta = duree * n / max(coeur - 1, 1)
        print(f"[ETA] {n} executions | {coeur} coeurs | environ {eta / 60:.1f} min")
        print(f"[SEUILS] lancement automatique si <= {BUDGET_LANCEMENT_S / 60:.0f} min ; "
              f"repli a 3 amplitudes si <= {BUDGET_REPLI_S / 60:.0f} min ; sinon abandon "
              f"declare")
        if not args.pilote:
            return

    if not args.pilote:
        ap.error("choisir --chrono, --controle ou --pilote")

    seeds = list(range(1, args.seeds + 1))
    grille = [(float(b), s) for b in shifts for s in seeds]
    print(f"[INFO] pilote par arbre : {len(shifts)} amplitudes x {args.seeds} graines "
          f"= {len(grille)} executions de {T_DRIFT + H} pas, M = {N_MODELS}")

    t0 = time.time()
    res = Parallel(n_jobs=args.jobs)(
        delayed(run_one)(b, s) for b, s in tqdm(grille, desc=f"pilote_arbres_{args.tag}")
    )
    duree = time.time() - t0

    metas, traces, arbres, evs = [], [], [], []
    for run_id, (meta, serie, err_m, vote_m, events) in enumerate(res):
        meta = dict(meta, run_id=run_id)
        metas.append(meta)
        traces.append(pd.DataFrame({"run_id": run_id, "t": np.arange(H, dtype=np.int32),
                                    "e": serie}))
        evs.append(pd.DataFrame(events, columns=["t", "tree_id"]).assign(run_id=run_id))
        tt, mm = np.meshgrid(np.arange(H, dtype=np.int32),
                             np.arange(N_MODELS, dtype=np.int8), indexing="ij")
        arbres.append(pd.DataFrame({"run_id": np.int32(run_id), "t": tt.ravel(),
                                    "tree_id": mm.ravel(), "e": err_m.ravel(),
                                    "a_vote": vote_m.ravel()}))

    meta_df = pd.DataFrame(metas)
    traces_df = pd.concat(traces, ignore_index=True)
    arbres_df = pd.concat(arbres, ignore_index=True)
    events_df = pd.concat(evs, ignore_index=True)[["run_id", "t", "tree_id"]]

    # Controle bit a bit sur TOUTES les executions qui existent dans la campagne.
    ref_meta = pd.read_parquet(DATA_DIR / "QCD_runs_meta_full.parquet")
    ref_tr = pd.read_parquet(DATA_DIR / "QCD_traces_error_full.parquet")
    ref_ev = pd.read_parquet(DATA_DIR / "QCD_events_swap_full.parquet")
    verifies, ecarts_total, ecarts_events = 0, 0, 0
    correspondance = {}
    for r in meta_df.itertuples():
        m = ref_meta[(np.abs(ref_meta.delta_e - r.delta_e) < 1e-12) &
                     (ref_meta.seed == r.seed)]
        if m.empty:
            continue
        rid = int(m.run_id.iloc[0])
        correspondance[r.run_id] = rid
        ref = ref_tr[ref_tr.run_id == rid].sort_values("t").e.to_numpy()
        mine = traces_df[traces_df.run_id == r.run_id].sort_values("t").e.to_numpy()
        ecarts_total += int(np.sum(ref != mine))
        # Second controle, plus exigeant que la trajectoire : les remplacements
        # d'arbres doivent coincider evenement par evenement.
        a = ref_ev[ref_ev.run_id == rid].sort_values(["t", "tree_id"])[["t", "tree_id"]]
        b = events_df[events_df.run_id == r.run_id].sort_values(["t", "tree_id"])[
            ["t", "tree_id"]]
        if a.shape != b.shape or not np.array_equal(a.to_numpy(), b.to_numpy()):
            ecarts_events += 1
        verifies += 1
    print(f"[CONTROLE] {verifies} executions comparees a la campagne, "
          f"{ecarts_total} pas differents au total, "
          f"{ecarts_events} executions aux remplacements differents")
    if ecarts_total or ecarts_events:
        raise SystemExit("[ECHEC] non-regression bit a bit rompue : rien n'est ecrit.")
    meta_df["run_id_campagne"] = meta_df.run_id.map(correspondance)

    meta_df["n_pas_verifies"] = H
    events_df.to_parquet(DATA_DIR / f"QCD_bis_events_swap_arbres_{args.tag}.parquet",
                         index=False)
    meta_df.to_parquet(DATA_DIR / f"QCD_bis_meta_arbres_{args.tag}.parquet", index=False)
    arbres_df.to_parquet(DATA_DIR / f"QCD_bis_traces_arbres_{args.tag}.parquet", index=False)
    # Log de campagne : `experimentation.md` prescrit « *.parquet + logs de
    # campagne ». Une duree citee dans une redaction doit se relire quelque part.
    log = DATA_DIR / f"QCD_bis_pilote_arbres_{args.tag}.log"
    with open(log, "w", encoding="utf-8") as f:
        f.write(f"campagne      : pilote instrumente par arbre (D.1.bis, tache 5b)\n")
        f.write(f"date          : {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"amplitudes    : {len(shifts)} ({', '.join(f'{delta_e(b):.6f}' for b in shifts)})\n")
        f.write(f"graines       : {args.seeds} (1..{args.seeds})\n")
        f.write(f"executions    : {len(grille)}\n")
        f.write(f"M             : {N_MODELS}\n")
        f.write(f"horizon H     : {H}\n")
        f.write(f"rodage        : {T_DRIFT}\n")
        f.write(f"socle         : {BASELINE_DEFAULT} pas pre-rupture\n")
        f.write(f"jobs          : {args.jobs}\n")
        f.write(f"duree_secondes: {duree:.1f}\n")
        f.write(f"duree_minutes : {duree / 60:.1f}\n")
        f.write(f"controle      : {verifies} executions comparees a la campagne, "
                f"{ecarts_total} pas differents, {ecarts_events} executions aux "
                f"remplacements differents\n")
        f.write(f"lignes_arbres : {len(arbres_df)}\n")
    print(f"[SUCCESS] {len(arbres_df)} lignes par arbre ecrites en {duree / 60:.1f} min")
    print(f"[SUCCESS] log de campagne : {log.name}")
    print(f"[SUCCESS] QCD_bis_traces_arbres_{args.tag}.parquet, "
          f"QCD_bis_meta_arbres_{args.tag}.parquet")


if __name__ == "__main__":
    main()
