"""
exp_QCD_temoins_bruit.py
===================================================================
Deux temoins sans drift, ajoutes le 15/09 apres une relecture externe.

1. POURQUOI LE PREMIER REMPLACEMENT RECULE-T-IL AVEC UN DRIFT FAIBLE ?
   Sans drift, le premier remplacement median arrive a 95 pas ; a
   Delta_e = 0,085 il arrive a 346. Hypothese : la coupure d'ADWIN,
   epsilon = sqrt(2 m var delta') + (2/3) m delta', croit avec la variance
   de la fenetre. Autour de 2 % d'erreur la variance est minuscule et des
   rafales de bruit suffisent a couper ; apres un drift faible l'erreur
   monte vers 10 %, la variance est multipliee par 4 a 5 et ces coupures
   par bruit se rarefient.
   Temoin : AUCUN drift, mais un bruit d'etiquette STATIONNAIRE de taux eta,
   present des t = 0. L'erreur de base monte sans qu'aucune rupture n'ait
   lieu. Si le premier remplacement recule quand eta croit, l'hypothese tient.

2. CE QUE COUTE LE MECANISME DE REMPLACEMENT SANS DRIFT
   Une foret identique dont les detecteurs sont desactives (NoDrift) : elle ne
   remplace jamais rien. Son erreur moyenne se compare aux 0,0228 de la foret
   standard, et remplace le 0,0125 non persiste du journal.

Le bruit est tire dans un generateur a part : a eta = 0 un run reproduit au
bit pres le run de meme graine du bras QE2000_nodrift_M10 (controle imprime).

USAGE
    PYTHONHASHSEED=0 python exp_QCD_temoins_bruit.py              # 200 graines par bras
    PYTHONHASHSEED=0 python exp_QCD_temoins_bruit.py --seeds 20   # prototype
"""

import argparse
import random
import time

import numpy as np
import pandas as pd
from joblib import Parallel, delayed

from river import drift
from river.forest import ARFClassifier

from exp_QCD_campagne import BASELINE_MAX, C_INT, DATA_DIR, H, N_MODELS, T_DRIFT

ETAS = (0.0, 0.04, 0.08, 0.12)
DECALAGE_BRUIT = 1_000_003      # graine du generateur de bruit = graine + decalage


def run_one(seed, eta, remplacement=True):
    safe_seed = int(seed % (2 ** 31 - 1))
    random.seed(safe_seed)
    np.random.seed(safe_seed)
    rng = np.random.default_rng(safe_seed)
    rng_bruit = np.random.default_rng(safe_seed + DECALAGE_BRUIT)

    detecteur = (lambda: drift.ADWIN(clock=C_INT)) if remplacement else drift.NoDrift
    arf = ARFClassifier(n_models=N_MODELS, seed=safe_seed,
                        drift_detector=detecteur(), warning_detector=detecteur())

    err_pre, err_post = [], np.zeros(H, dtype=np.int8)
    prev_counts, events = {}, []
    for t in range(T_DRIFT + H):
        x0, x1 = rng.normal(), rng.normal()
        x = {0: x0, 1: x1}
        y = int(x0 + x1 > 0.0)
        if rng_bruit.random() < eta:
            y = 1 - y
        error = int((arf.predict_one(x) or 0) != y)
        if t < T_DRIFT:
            if t >= T_DRIFT - BASELINE_MAX:
                err_pre.append(error)
        elif t == T_DRIFT and remplacement:
            prev_counts = dict(arf._drift_tracker)
        arf.learn_one(x, y)
        if t >= T_DRIFT:
            err_post[t - T_DRIFT] = error
            if remplacement:
                for tid, v in arf._drift_tracker.items():
                    if v > prev_counts.get(tid, 0):
                        events.append(t - T_DRIFT)
                        prev_counts[tid] = v

    return {
        "seed": int(seed), "eta": float(eta), "remplacement": bool(remplacement),
        "p_hat_0": float(np.mean(err_pre)), "erreur_post": float(err_post.mean()),
        "premier_remplacement": (min(events) if events else np.nan),
        "n_remplacements": len(events),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--seeds", type=int, default=200)
    ap.add_argument("--jobs", type=int, default=-1)
    args = ap.parse_args()
    graines = range(1, args.seeds + 1)
    grille = [(s, eta, True) for eta in ETAS for s in graines] + [(s, 0.0, False) for s in graines]
    print(f"[INFO] {len(grille)} executions : eta dans {ETAS} avec remplacement, "
          f"et eta = 0 sans remplacement ; {args.seeds} graines par bras")
    t0 = time.time()
    lignes = Parallel(n_jobs=args.jobs)(delayed(run_one)(*g) for g in grille)
    df = pd.DataFrame(lignes)
    tag = "" if args.seeds == 200 else f"_s{args.seeds}"
    sortie = DATA_DIR / f"QCD_temoins_bruit{tag}.parquet"
    df.to_parquet(sortie, index=False)
    print(f"[INFO] termine en {(time.time() - t0) / 60:.1f} min -> {sortie.name}")


if __name__ == "__main__":
    main()
