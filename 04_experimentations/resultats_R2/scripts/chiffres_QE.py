"""
chiffres_QE.py
===================================================================
Rejeu des chiffres de `redaction_QE_choix_du_seuil.tex` (section E).

LECTURE SEULE. Ne resimule rien, n'ecrit aucune table. Tout est recalcule
hors ligne a partir des trajectoires d'erreur deja enregistrees :
  - campagne avec drift : QCD_traces_error_full (2 000 runs x 2 000 pas) ;
  - bras SANS drift : QCD_traces_error_QE2000_nodrift_M10 (2 000 runs,
    memes graines que la campagne). Il remplace depuis le 15/09 le bras A1
    de 100 runs, dont les intervalles etaient trop larges pour le taux de
    fausses alarmes.

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

    meta0 = pd.read_parquet(DATA / "QCD_runs_meta_QE2000_nodrift_M10.parquet").set_index("run_id")
    det0 = _table_franchissements(
        pd.read_parquet(DATA / "QCD_traces_error_QE2000_nodrift_M10.parquet"), meta0["p_hat_0"], LAMBDAS)
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
              f" | {fa:3d}/{n0} = {fa/n0*100:5.2f} % [{lo*100:.2f};{hi*100:.2f}]")

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
    ev = pd.read_parquet(DATA / "QCD_events_swap_QE2000_nodrift_M10.parquet")
    meta = pd.read_parquet(DATA / "QCD_runs_meta_QE2000_nodrift_M10.parquet")
    ind = pd.read_parquet(DATA / "QCD_indicateurs_full.parquet")

    premier = ev.groupby("run_id")["t"].min()
    arbres = ev.groupby("run_id")["tree_id"].nunique()
    q1, q3 = premier.quantile([0.25, 0.75])
    faible = ind.loc[ind["delta_e"] < 0.03, "tau_arf"].median()

    n_runs = meta["run_id"].nunique()
    complet = int((arbres == 10).sum())
    print(f"\n[QE table 3] le temoin sans drift ({n_runs} runs, aucun changement)")
    print(f"  runs avec au moins un remplacement | mesure = {premier.size}/{n_runs}")
    print(f"  premier remplacement, mediane      | mesure = {premier.median():.0f} pas"
          f"  (quartiles {q1:.0f} et {q3:.0f})")
    print(f"  arbres distincts renouveles        | mesure = mediane {arbres.median():.0f}/10 ;"
          f" les 10 dans {complet} runs = {complet / n_runs * 100:.1f} %")
    print(f"  a comparer au drift le plus faible | mesure = tau_ARF median {faible:.0f} pas"
          f" a Delta_e = 0,028 ; {ind['tau_arf'].median():.0f} sur toute la grille")
    print("  table = QCD_events_swap_QE2000_nodrift_M10, QCD_indicateurs_full")


def _mediane_censuree(x, rng, n_boot=2000):
    """Mediane d'une duree censuree a H (NaN = aucun remplacement), rangee en dernier."""
    v = np.where(np.isnan(x), np.inf, x)
    boot = np.median(rng.choice(v, size=(n_boot, v.size), replace=True), axis=1)
    lo, hi = np.percentile(boot, [2.5, 97.5])
    return np.median(v), lo, hi


def temoins_bruit():
    """Deux temoins sans drift (exp_QCD_temoins_bruit.py) : bruit d'etiquette
    stationnaire, et foret dont les detecteurs sont desactives."""
    chemin = DATA / "QCD_temoins_bruit.parquet"
    if not chemin.exists():
        print("\n[temoins bruit] table absente : lancer exp_QCD_temoins_bruit.py")
        return
    d = pd.read_parquet(chemin)
    ev0 = pd.read_parquet(DATA / "QCD_events_swap_QE2000_nodrift_M10.parquet")
    rng = np.random.default_rng(0)
    fmt = lambda v: "> 2000" if np.isinf(v) else f"{v:.0f}"

    avec = d[d["remplacement"]]
    graines = sorted(avec["seed"].unique())
    ref = ev0.groupby("run_id")["t"].agg(["min", "size"]).reindex(np.array(graines) - 1)
    zero = avec[avec["eta"] == 0].set_index("seed").loc[graines]
    identique = (np.array_equal(zero["premier_remplacement"].fillna(-1).to_numpy(),
                                ref["min"].fillna(-1).to_numpy())
                 and np.array_equal(zero["n_remplacements"].to_numpy(), ref["size"].fillna(0).to_numpy()))
    print(f"\n[temoins bruit] {len(graines)} graines par bras ; eta = 0 reproduit le bras "
          f"QE2000 au run pres : {identique}")
    print("  eta | erreur de base p_hat_0 | runs avec remplacement | premier remplacement, mediane [IC 95 %]"
          " | remplacements par run")
    for eta, g in avec.groupby("eta"):
        med, lo, hi = _mediane_censuree(g["premier_remplacement"].to_numpy(), rng)
        n_avec = int(g["premier_remplacement"].notna().sum())
        print(f"  {eta:.2f} | {g['p_hat_0'].mean():.4f} | {n_avec}/{len(g)} = {n_avec / len(g) * 100:.1f} %"
              f" | {fmt(med)} [{fmt(lo)} ; {fmt(hi)}] | {g['n_remplacements'].mean():.2f}")

    # niveau d'erreur que voit la foret apres un drift faible, avant sa premiere reparation
    ind = pd.read_parquet(DATA / "QCD_indicateurs_full.parquet")
    tr = pd.read_parquet(DATA / "QCD_traces_error_full.parquet")
    for cible in (0.085, 0.141):
        sel = ind.loc[(ind["delta_e"] - cible).abs() < 0.002, ["run_id", "tau_arf", "p_hat_0"]]
        t = tr[tr["run_id"].isin(sel["run_id"])].merge(sel, on="run_id")
        avant = t[t["t"] < t["tau_arf"].fillna(H)].groupby("run_id")["e"].mean()
        print(f"  a Delta_e = {cible} : erreur moyenne avant le premier remplacement = {avant.mean():.4f}"
              f" (socle {sel['p_hat_0'].mean():.4f})")

    sans = d[~d["remplacement"]]
    tr0 = pd.read_parquet(DATA / "QCD_traces_error_QE2000_nodrift_M10.parquet")
    print(f"  foret sans remplacement : erreur moyenne post = {sans['erreur_post'].mean():.4f}"
          f" ; foret standard, memes graines = {zero['erreur_post'].mean():.4f}"
          f" ; foret standard, 2 000 runs = {tr0['e'].mean():.4f}")
    print("  table = QCD_temoins_bruit, QCD_events_swap_QE2000_nodrift_M10, QCD_traces_error_full")


def tolerance_en_ecarts_types():
    """delta_P rapporte a l'ecart-type binomial de l'estimation du socle p_hat_0."""
    p = pd.read_parquet(DATA / "QCD_indicateurs_full.parquet")["p_hat_0"].mean()
    print(f"\n[delta_P] socle moyen {p:.4f}")
    for n in (3000, 1000):
        sd = math.sqrt(p * (1 - p) / n)
        print(f"  socle sur {n} pas : ecart-type {sd:.4f} ; delta_P = {DELTA_P / sd:.1f} ecarts-types")
    print("  table = QCD_indicateurs_full.p_hat_0 (approximation binomiale)")


if __name__ == "__main__":
    balayage()
    temoin_sans_drift()
    temoins_bruit()
    tolerance_en_ecarts_types()
