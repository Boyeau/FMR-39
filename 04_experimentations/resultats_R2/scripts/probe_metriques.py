"""
probe_metriques.py — exploration, avant de figer quoi que ce soit.

Fait tourner TROIS forets sur exactement le meme flux :

  1. l'ARF normale       : elle apprend et remplace ses arbres (le dispositif de R2) ;
  2. une ARF NoDrift     : meme graine, memes donnees, mais elle ne remplace JAMAIS
                           un arbre. Elle continue d'apprendre. C'est l'etalon : ce qui
                           se passerait sans le mecanisme de reparation ;
  3. une copie gelee     : photographie de l'ARF normale a tau*, qui n'apprend plus rien.
                           Sert de reference pour mesurer de combien la foret a change
                           d'avis.

On teste trois affirmations qui n'ont jamais ete verifiees :

  H1  e_t - p_hat_0  ~=  Delta_e - D(t)
      ou D(t) est la fraction du flux sur laquelle la foret normale et la copie gelee
      ne disent plus la meme chose. Si H1 tient, le budget de preuve du detecteur est
      l'integrale du deficit d'adaptation, ce qui relierait C.1 et C.3.

  H2  la masse de vote renouvelee (fraction de la performance totale detenue par des
      arbres nes apres tau*) est un meilleur indicateur que le simple comptage d'arbres.

  H3  l'erreur de la foret NoDrift reste a p_0 + Delta_e, ce qui valide l'etalon --
      et l'ecart entre les deux courbes isole ce que le REMPLACEMENT apporte, par
      rapport au simple apprentissage incremental (conjecture de C.1c).
"""

import copy
import random
import sys
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from scipy.stats import norm

from river import drift
from river.forest import ARFClassifier

warnings.filterwarnings('ignore')

T_DRIFT, H, N_MODELS, C_INT = 4000, 2000, 10, 1
# Les sorties partaient dans un scratchpad de session, donc perime et non rejouable :
# elles vont desormais dans le depot, comme toute matiere premiere de campagne.
OUT = str(Path(__file__).resolve().parents[1] / "resultats" / "data")


def delta_e(b):
    return float(norm.cdf(b / np.sqrt(2)) - 0.5)


def masse_vote(arf, ids_pre):
    """Fraction de la performance totale detenue par des arbres nes apres tau*.

    `_metrics` donne la performance courante de chaque arbre. On pondere par elle
    plutot que de compter les arbres : un arbre neuf mais encore mauvais ne devrait
    pas peser autant qu'un arbre neuf performant.
    """
    try:
        perf = np.array([m.get() for m in arf._metrics], dtype=float)
    except Exception:
        return np.nan
    perf = np.clip(perf, 0, None)
    tot = perf.sum()
    if tot <= 0:
        return np.nan
    tracker = arf._drift_tracker
    keys = list(range(len(perf)))
    neufs = np.array([tracker.get(k, 0) > ids_pre.get(k, 0) for k in keys], dtype=float)
    return float((perf * neufs).sum() / tot)


def run_one(b, seed):
    ss = int(seed % (2 ** 31 - 1))
    random.seed(ss); np.random.seed(ss)
    rng = np.random.default_rng(ss)

    def make(det):
        return ARFClassifier(n_models=N_MODELS, seed=ss,
                             drift_detector=det, warning_detector=copy.deepcopy(det))

    arf = make(drift.ADWIN(clock=C_INT))
    temoin = make(drift.NoDrift())          # meme graine, ne remplace jamais

    errors_pre = []
    p0 = None
    gel = None
    ids_pre = {}

    e = np.zeros(H, np.int8)        # erreur de l'ARF normale
    e_tem = np.zeros(H, np.int8)    # erreur de l'etalon (sans remplacement)
    dis = np.zeros(H, np.int8)      # desaccord avec la copie gelee
    mv = np.zeros(H, np.float32)    # masse de vote renouvelee

    for t in range(T_DRIFT + H):
        x0, x1 = rng.normal(), rng.normal()
        x = {0: x0, 1: x1}
        y = int(x0 + x1 > 0.0) if t < T_DRIFT else int(x0 + x1 > b)

        p = arf.predict_one(x) or 0
        err = int(p != y)

        if t < T_DRIFT:
            if t >= T_DRIFT - 3000:
                errors_pre.append(err)
        elif t == T_DRIFT:
            p0 = float(np.mean(errors_pre))
            gel = copy.deepcopy(arf)                 # photographie d'avant
            ids_pre = dict(arf._drift_tracker)

        arf.learn_one(x, y)
        temoin.learn_one(x, y)

        if t >= T_DRIFT:
            i = t - T_DRIFT
            e[i] = err
            e_tem[i] = int((temoin.predict_one(x) or 0) != y)
            dis[i] = int((gel.predict_one(x) or 0) != p)
            mv[i] = masse_vote(arf, ids_pre)

    de = delta_e(b)
    tracker = arf._drift_tracker
    tau_arf = np.nan
    distincts = sum(1 for k, v in tracker.items() if v > ids_pre.get(k, 0))
    return {
        'b': b, 'delta_e': de, 'seed': seed, 'p_hat_0': p0,
        'e': e, 'e_temoin': e_tem, 'D': dis, 'masse_vote': mv,
        'arbres_renouveles': distincts,
    }


if __name__ == "__main__":
    shifts = np.linspace(0.1, 4.0, 20)[[0, 4, 9, 14, 19]]
    seeds = list(range(1, int(sys.argv[1]) + 1)) if len(sys.argv) > 1 else list(range(1, 21))
    grid = [(b, s) for b in shifts for s in seeds]
    print(f"[INFO] {len(shifts)} amplitudes x {len(seeds)} graines = {len(grid)} executions, 3 forets")
    t0 = time.time()
    res = Parallel(n_jobs=-1)(delayed(run_one)(b, s) for b, s in grid)
    print(f"[INFO] termine en {(time.time()-t0)/60:.1f} min")

    meta = pd.DataFrame([{k: r[k] for k in ('b', 'delta_e', 'seed', 'p_hat_0', 'arbres_renouveles')}
                         for r in res])
    np.savez_compressed(f"{OUT}/probe_traces.npz",
                        e=np.array([r['e'] for r in res]),
                        e_temoin=np.array([r['e_temoin'] for r in res]),
                        D=np.array([r['D'] for r in res]),
                        masse_vote=np.array([r['masse_vote'] for r in res]))
    meta.to_parquet(f"{OUT}/probe_meta.parquet", index=False)
    print(f"[SUCCESS] {len(res)} executions ecrites dans {OUT}")
