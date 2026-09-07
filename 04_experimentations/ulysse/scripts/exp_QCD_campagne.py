"""
exp_QCD_campagne.py
===================================================================
Campagne UNIQUE pour les questions C et D du sujet 39.

Cadrage : Business_case_Filiere_Recherche_Blind_Spot_FIN.md (version du 07/09).

Ce script ne fait qu'une chose : produire les trajectoires. Il ne calcule aucun
indicateur, ne connait aucun seuil `lambda`, et ne decide jamais si une alarme a
retenti. Tout cela est du ressort de `analyse_QCD.py`, qui relit ce qui est ecrit
ici sans relancer une seule simulation.

POURQUOI UNE SEULE CAMPAGNE
    `lambda` n'intervient nulle part dans la dynamique : le detecteur externe lit
    la trajectoire d'erreur, il n'agit jamais sur la foret. Les trois scenarios de
    R2 (lambda = 8, 25, 50) partagent `c_int = 1` et la meme graine : une fois le
    `break` retire, ils produisent des executions identiques au bit pres. On simule
    donc une fois, et on balaye lambda hors ligne.

CE QUI EST ENREGISTRE — deux choses seulement (cf. D.1)
    1. la trajectoire d'erreur e_t sur les H pas post-rupture (int8) ;
    2. les evenements de remplacement, une ligne par (pas, identifiant d'arbre) ;
    3. la trajectoire d'erreur sur les BASELINE_MAX pas PRE-rupture, qui permet de
       recalculer le socle p_hat_0 pour n'importe quelle fenetre <= BASELINE_MAX sans
       resimuler. Le sujet demande de rapporter le socle a 1000 pas (reproduction de
       R2) ET a 3000 pas (analyse) : sans cette trace, il faudrait deux campagnes.
    Le dictionnaire `_drift_tracker` n'est PAS ecrit pas a pas : il contient vingt
    fois plus de lignes pour exactement la meme information.

ECARTS ASSUMES PAR RAPPORT A exp_R2_instrumented_blind_spot.py (depot officiel)
    - le `break` de fin de boucle est retire (sans lui, aucune trajectoire n'existe) ;
    - l'horizon post-rupture est borne a H = 2000 (R2 en simule 4000 : les 2000
      derniers n'apportent rien et doublent le cout) ;
    - le socle p_hat_0 est estime sur 3000 pas pre-rupture au lieu de 1000
      (--baseline 1000 pour reproduire R2 a l'identique).
    Le rodage de 4000 pas est intact : il fixe la maturite de la foret et la valeur
    du socle. Le reduire changerait tau_ARF et romprait la comparaison avec l'article.

USAGE
    PYTHONHASHSEED=0 python exp_QCD_campagne.py                 # prototype 5 x 20
    PYTHONHASHSEED=0 python exp_QCD_campagne.py --full          # campagne 20 x 100
    PYTHONHASHSEED=0 python exp_QCD_campagne.py --baseline 1000 # repro de controle
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

# --- Parametres imposes par le sujet -------------------------------------------
N_MODELS = 10                              # M, taille de la foret (R2)
C_INT = 1                                  # horloge ADWIN : reactivite maximale
T_DRIFT = 4000                             # instant de rupture, SANCTUARISE
H = 2000                                   # horizon post-rupture, fixe pour tout le projet
BOUNDARY_SHIFTS = np.linspace(0.1, 4.0, 20)   # grille de R2 : b, PAS Delta_e
BASELINE_DEFAULT = 3000                    # pas pre-rupture pour estimer p_hat_0
BASELINE_MAX = 3000                        # pas pre-rupture enregistres (socle recalculable)

# Sous-grille de prototypage : 5 amplitudes x 20 graines.
PROTO_SHIFTS = BOUNDARY_SHIFTS[[0, 4, 9, 14, 19]]   # 5 amplitudes bien reparties
PROTO_SEEDS = 20
FULL_SEEDS = 100


def delta_e(boundary_shift):
    """Amplitude du saut d'erreur induite par une translation `b` de la frontiere.

    Un modele cale sur l'ancienne frontiere se trompe sur les points tombes entre
    les deux ; comme x0 + x1 ~ N(0, 2), cela vaut P(0 < x0 + x1 <= b).
    C'est Delta_e, et non `b`, qui alimente le detecteur : toutes les questions
    raisonnent en Delta_e.
    """
    return float(norm.cdf(boundary_shift / np.sqrt(2)) - 0.5)


def run_one(boundary_shift, seed, baseline_window):
    """Une execution. Renvoie (meta, trajectoire d'erreur, evenements de remplacement)."""
    safe_seed = int(seed % (2 ** 31 - 1))
    random.seed(safe_seed)
    np.random.seed(safe_seed)
    rng = np.random.default_rng(safe_seed)

    arf = ARFClassifier(
        n_models=N_MODELS, seed=safe_seed,
        drift_detector=drift.ADWIN(clock=C_INT),
        warning_detector=drift.ADWIN(clock=C_INT),
    )

    errors_pre = []
    pre_series = np.zeros(BASELINE_MAX, dtype=np.int8)
    p_hat_0 = None
    prev_counts = {}
    error_series = np.zeros(H, dtype=np.int8)
    events = []          # (pas post-rupture, identifiant d'arbre)

    for t in range(T_DRIFT + H):
        x0, x1 = rng.normal(), rng.normal()
        x_dict = {0: x0, 1: x1}
        y = int(x0 + x1 > 0.0) if t < T_DRIFT else int(x0 + x1 > boundary_shift)

        y_pred = arf.predict_one(x_dict) or 0
        error = int(y_pred != y)

        if t < T_DRIFT:
            if t >= T_DRIFT - BASELINE_MAX:
                pre_series[t - (T_DRIFT - BASELINE_MAX)] = error
            if t >= T_DRIFT - baseline_window:
                errors_pre.append(error)
        elif t == T_DRIFT:
            p_hat_0 = float(np.mean(errors_pre)) if errors_pre else 0.05
            # `_drift_tracker` est un STOCK cumule depuis t = 0, pas un flux. Avec
            # ADWIN(clock=1), des arbres ont deja ete remplaces plusieurs fois
            # pendant le rodage, par simple bruit. On fige donc l'etat juste avant
            # la rupture : seuls les compteurs qui AUGMENTENT ensuite comptent.
            prev_counts = dict(arf._drift_tracker)

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
    }
    return meta, error_series, events, pre_series


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--full', action='store_true',
                    help="campagne complete : 20 amplitudes x 100 graines")
    ap.add_argument('--seeds', type=int, default=None,
                    help="nombre de graines (defaut : 20 en prototype, 100 en complet)")
    ap.add_argument('--baseline', type=int, default=BASELINE_DEFAULT,
                    help="pas pre-rupture pour estimer p_hat_0 (1000 = R2 a l'identique)")
    ap.add_argument('--tag', type=str, default=None,
                    help="suffixe des fichiers de sortie")
    ap.add_argument('--jobs', type=int, default=-1)
    args = ap.parse_args()

    if args.full:
        shifts = BOUNDARY_SHIFTS
        n_seeds = args.seeds or FULL_SEEDS
        tag = args.tag or 'full'
    else:
        shifts = PROTO_SHIFTS
        n_seeds = args.seeds or PROTO_SEEDS
        tag = args.tag or 'proto'
    if args.baseline != BASELINE_DEFAULT:
        tag = f"{tag}_base{args.baseline}"

    seeds = list(range(1, n_seeds + 1))
    grid = [(b, s) for b in shifts for s in seeds]
    print(f"[INFO] {len(shifts)} amplitudes x {n_seeds} graines = {len(grid)} executions "
          f"de {T_DRIFT + H} pas | socle sur {args.baseline} pas | H = {H}")

    t0 = time.time()
    results = Parallel(n_jobs=args.jobs)(
        delayed(run_one)(b, s, args.baseline) for b, s in tqdm(grid, desc=tag)
    )
    elapsed = time.time() - t0

    metas, trace_frames, event_frames, pre_frames = [], [], [], []
    for run_id, (meta, err, events, pre) in enumerate(results):
        meta['run_id'] = run_id
        metas.append(meta)
        trace_frames.append(pd.DataFrame({
            'run_id': np.full(H, run_id, dtype=np.int32),
            't': np.arange(H, dtype=np.int16),
            'e': err,
        }))
        pre_frames.append(pd.DataFrame({
            'run_id': np.full(BASELINE_MAX, run_id, dtype=np.int32),
            't_pre': np.arange(-BASELINE_MAX, 0, dtype=np.int16),
            'e': pre,
        }))
        if events:
            ev = np.asarray(events, dtype=np.int32)
            event_frames.append(pd.DataFrame({
                'run_id': np.full(len(ev), run_id, dtype=np.int32),
                't': ev[:, 0].astype(np.int16),
                'tree_id': ev[:, 1].astype(np.int8),
            }))

    meta_df = pd.DataFrame(metas)
    traces_df = pd.concat(trace_frames, ignore_index=True)
    events_df = (pd.concat(event_frames, ignore_index=True) if event_frames
                 else pd.DataFrame({'run_id': pd.Series(dtype=np.int32),
                                    't': pd.Series(dtype=np.int16),
                                    'tree_id': pd.Series(dtype=np.int8)}))

    pd.concat(pre_frames, ignore_index=True).to_parquet(
        DATA_DIR / f"QCD_traces_pre_{tag}.parquet", index=False)
    meta_df.to_parquet(DATA_DIR / f"QCD_runs_meta_{tag}.parquet", index=False)
    traces_df.to_parquet(DATA_DIR / f"QCD_traces_error_{tag}.parquet", index=False)
    events_df.to_parquet(DATA_DIR / f"QCD_events_swap_{tag}.parquet", index=False)

    per_run = elapsed / len(grid)
    print(f"[INFO] termine en {elapsed / 60:.1f} min ({per_run:.2f} s/run)")
    if not args.full:
        n_full = len(BOUNDARY_SHIFTS) * FULL_SEEDS
        print(f"[INFO] extrapolation campagne complete ({n_full} runs) : "
              f"~{per_run * n_full / 60:.1f} min")
    print(f"[INFO] traces {len(traces_df):,} lignes | evenements {len(events_df):,} lignes")
    print(f"[SUCCESS] ecrit dans {DATA_DIR} (tag = {tag})")


if __name__ == "__main__":
    main()
