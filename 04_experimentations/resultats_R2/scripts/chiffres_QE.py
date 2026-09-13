"""
chiffres_QE.py
===================================================================
Rejeu des chiffres de `redaction_QE_choix_du_seuil.tex` (section E).

LECTURE SEULE. Ne resimule rien, n'ecrit aucune table. Tout est recalcule
hors ligne a partir des trajectoires d'erreur deja enregistrees :
  - campagne avec drift : QCD_traces_error_full (2 000 runs x 2 000 pas) ;
  - bras SANS drift de A1 : QCD_traces_error_A1_nodrift (100 runs), le
    seul endroit du projet ou l'on observe le detecteur quand il ne se
    passe rien.

CE QUE LA SECTION E ETABLIT, ET QUI N'EST NULLE PART AILLEURS
  1. Detecter n'est pas gagner. La detection dans l'horizon et la victoire
     dans la course (tau_det < tau_ARF) se separent des que lambda monte :
     a lambda = 15 le detecteur alarme dans 93 % des runs mais n'arrive le
     premier que dans 36 % d'entre eux. La signature paradoxale de
     l'article survit donc a ce seuil sur la course.
  2. Le cout en fausses alarmes de lambda = 8, que l'article affirme
     (« sacrifices false-alarm robustness ») sans le mesurer sur ce banc.

CONTROLE OBLIGATOIRE
  Le balayage doit redonner exactement les comptes de la campagne aux trois
  seuils du sujet : 1906 / 778 / 1. S'il ne les redonne pas, la recurrence
  hors ligne differe de celle de la campagne et RIEN d'autre n'est lisible.

USAGE
    PYTHONHASHSEED=0 python chiffres_QE.py
"""

import math
from pathlib import Path

import numpy as np
import pandas as pd

RACINE = Path(__file__).resolve().parents[1]
DATA = RACINE / "resultats" / "data"

H = 2000
DELTA_P = 0.01
LAMBDAS = (8, 12, 15, 20, 25, 50)
ATTENDU = {8: 1906, 25: 778, 50: 1}          # QCD_indicateurs_full


def wilson(k: int, n: int, z: float = 1.959963984540054):
    """Intervalle de Wilson a 95 %. Controle : 50/100 -> [0.4038 ; 0.5962]."""
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    den = 1.0 + z * z / n
    centre = (p + z * z / (2 * n)) / den
    demi = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return centre - demi, centre + demi


def _premiers_franchissements(x, lambdas):
    """Premier pas ou S_t = max(0, S_{t-1} + x_t) atteint chaque lambda.

    Un seul passage sur la trajectoire pour tous les seuils : S_t ne depend
    pas de lambda, seul le franchissement en depend.
    """
    s, atteint, restants = 0.0, {l: None for l in lambdas}, set(lambdas)
    for t, v in enumerate(x):
        s += v
        if s < 0.0:
            s = 0.0
        if restants:
            for l in tuple(restants):
                if s >= l:
                    atteint[l] = t
                    restants.discard(l)
    return atteint


def _table_franchissements(traces, socles, lambdas, n_pas=H):
    lignes = []
    for rid, g in traces.sort_values(["run_id", "t"]).groupby("run_id"):
        x = g["e"].to_numpy()[:n_pas] - float(socles.loc[rid]) - DELTA_P
        lignes.append({"run_id": rid, **_premiers_franchissements(x, lambdas)})
    return pd.DataFrame(lignes).set_index("run_id")


def balayage():
    ind = pd.read_parquet(DATA / "QCD_indicateurs_full.parquet").set_index("run_id")
    det = _table_franchissements(
        pd.read_parquet(DATA / "QCD_traces_error_full.parquet"), ind["p_hat_0"], LAMBDAS)

    print("[QE controle] le balayage hors ligne contre la campagne")
    for lam, attendu in ATTENDU.items():
        mesure = int(det[lam].notna().sum())
        etat = "OK" if mesure == attendu else "ECART -- NE RIEN LIRE PLUS BAS"
        print(f"  lambda = {lam:2d} | alarmes attendues {attendu:4d} | mesurees {mesure:4d}  {etat}")

    meta0 = pd.read_parquet(DATA / "QCD_runs_meta_A1_nodrift.parquet").set_index("run_id")
    det0 = _table_franchissements(
        pd.read_parquet(DATA / "QCD_traces_error_A1_nodrift.parquet"), meta0["p_hat_0"], LAMBDAS)
    n0 = len(det0)

    print("\n[QE table 1] detecter n'est pas gagner, et ce que coute le silence")
    print(f"  {'lam':>4} | {'detecte':>14} | {'gagne la course':>16} | {'sur non censures':>16}"
          f" | {'fausses alarmes sans drift':>28}")
    lignes = {}
    for lam in LAMBDAS:
        alarme = det[lam].notna()
        gagne = alarme & (det[lam] < ind["tau_arf"])
        k, n = int(gagne.sum()), len(det)
        fa = int(det0[lam].notna().sum())
        lo, hi = wilson(fa, n0)
        lignes[lam] = (int(alarme.sum()), k, int(alarme.sum()), fa)
        print(f"  {lam:>4} | {int(alarme.sum()):5d}/{n} {alarme.mean()*100:5.1f} %"
              f" | {k:5d}/{n} {k/n*100:5.1f} %"
              f" | {gagne.sum()/max(alarme.sum(),1)*100:14.1f} %"
              f" | {fa:3d}/{n0} = {fa/n0*100:4.1f} % [{lo*100:.1f};{hi*100:.1f}]")

    print("\n[QE table 2] victoire de la course par amplitude (part des 100 runs)")
    pivot = pd.DataFrame({"delta_e": ind["delta_e"]})
    for lam in (8, 15, 20):
        pivot[lam] = (det[lam].notna() & (det[lam] < ind["tau_arf"])).astype(float)
    par = pivot.groupby("delta_e").mean().mul(100).round(0).astype(int)
    print(par.to_string())
    return det, det0


def temoin_sans_drift():
    """Le controle qui ne depend d'aucun seuil : la foret se « repare »
    aussi quand rien ne change."""
    ev = pd.read_parquet(DATA / "QCD_events_swap_A1_nodrift.parquet")
    meta = pd.read_parquet(DATA / "QCD_runs_meta_A1_nodrift.parquet")
    ind = pd.read_parquet(DATA / "QCD_indicateurs_full.parquet")

    premier = ev.groupby("run_id")["t"].min()
    arbres = ev.groupby("run_id")["tree_id"].nunique()
    q1, q3 = premier.quantile([0.25, 0.75])
    faible = ind.loc[ind["delta_e"] < 0.03, "tau_arf"].median()

    print("\n[QE table 3] le temoin sans drift (100 runs, aucun changement)")
    print(f"  runs avec au moins un remplacement | mesure = {premier.size}/{meta['run_id'].nunique()}")
    print(f"  premier remplacement, mediane      | mesure = {premier.median():.0f} pas"
          f"  (quartiles {q1:.0f} et {q3:.0f})")
    print(f"  arbres distincts renouveles        | mesure = mediane {arbres.median():.0f}/10 ;"
          f" les 10 dans {int((arbres == 10).sum())} runs")
    print(f"  a comparer au drift le plus faible | mesure = tau_ARF median {faible:.0f} pas"
          f" a Delta_e = 0,028 ; {ind['tau_arf'].median():.0f} sur toute la grille")
    print("  table = QCD_events_swap_A1_nodrift, QCD_indicateurs_full")


if __name__ == "__main__":
    balayage()
    temoin_sans_drift()
