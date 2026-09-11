"""
chiffres_QA.py
===================================================================
Rejeu des chiffres empiriques cites dans `redaction_QA_course_concurrente.tex`
(section « The Race, Measured »).

LECTURE SEULE. Ne resimule rien, n'ecrit aucune table. Lit la seule table
`QCD_indicateurs_full.parquet`, produite par `exp_QCD_campagne.py`.

Meme convention d'affichage que `chiffres_QC.py` :
    [QA l.N] ecrit = ...  |  mesure = ...  |  table = ...

Les trois quantites de la question A que l'enonce demande de MESURER et non
de seulement poser :
  A.1  la proportion d'ex-aequo tau_ARF == tau_det, qui mesure l'enjeu reel
       du choix inegalite stricte / large ;
  A.2  la proportion de doubles censures C_H, qui est exactement la largeur
       de l'encadrement de Manski ;
  et le cas limite de double famine {tau_ARF = +inf, tau_det = +inf}.

USAGE
    PYTHONHASHSEED=0 python chiffres_QA.py
"""

import math
from pathlib import Path

import pandas as pd

RACINE = Path(__file__).resolve().parents[1]
DATA = RACINE / "resultats" / "data"

LAMBDAS = (8, 25, 50)
H = 2000


def wilson(k: int, n: int, z: float = 1.959963984540054):
    """Intervalle de Wilson a 95 %. Controle : 50/100 -> [0.4038 ; 0.5962]."""
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    den = 1.0 + z * z / n
    centre = (p + z * z / (2 * n)) / den
    demi = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return centre - demi, centre + demi


def _titre(s: str) -> None:
    print("=" * 74)
    print(s)
    print("=" * 74)


def _sous_titre(s: str) -> None:
    print()
    print(f"--- {s}")


def _ligne(tag: str, ecrit, mesure, table: str) -> None:
    print(f"  [{tag}] ecrit = {ecrit}  |  mesure = {mesure}  |  table = {table}")


def qa() -> None:
    d = pd.read_parquet(DATA / "QCD_indicateurs_full.parquet")
    n = len(d)
    ca = d["censored_arf"].astype(bool)

    _titre("QA -- redaction_QA_course_concurrente.tex")

    _sous_titre("cadre : la censure de tau_ARF, dont tout le reste depend")
    _ligne(
        "QA l.86",
        "tau_ARF jamais censure sur la campagne",
        f"{int(ca.sum())}/{n} censures ; max observe {d.tau_arf.max():.0f} < H = {H} "
        f"(min {d.tau_arf.min():.0f})",
        "QCD_indicateurs_full.tau_arf, .censored_arf",
    )

    _sous_titre("A.1 : ex-aequo tau_ARF == tau_det (enjeu de la convention stricte)")
    for lam in LAMBDAS:
        cd = d[f"censored_det_{lam}"].astype(bool)
        obs = (~ca) & (~cd)
        ties = int((d.loc[obs, "tau_arf"] == d.loc[obs, f"tau_det_{lam}"]).sum())
        part = ties / n
        _ligne(
            f"QA l.94 lam={lam}",
            "proportion d'ex-aequo negligeable",
            f"{ties} ex-aequo sur {int(obs.sum())} runs doublement observes "
            f"({ties / max(int(obs.sum()), 1) * 100:.2f} % de ceux-ci, {part * 100:.2f} % des {n})",
            "QCD_indicateurs_full",
        )

    _sous_titre("cas limite : double famine {tau_ARF = +inf, tau_det = +inf}")
    for lam in LAMBDAS:
        cd = d[f"censored_det_{lam}"].astype(bool)
        _ligne(
            f"QA l.40 lam={lam}",
            "exclue de Miss par convention",
            f"{int((ca & cd).sum())} runs concernes",
            "QCD_indicateurs_full",
        )

    _sous_titre("A.2 : partition en 4 regions et encadrement de Manski (H = 2000)")
    print(
        f"      {'lam':>4} {'R1':>6} {'R2':>6} {'R3':>6} {'R4=C_H':>7} "
        f"{'borne inf':>10} {'borne sup':>10} {'largeur':>8}"
    )
    for lam in LAMBDAS:
        cd = d[f"censored_det_{lam}"].astype(bool)
        r1, r2 = (~ca) & (~cd), (~ca) & cd
        r3, r4 = ca & (~cd), ca & cd
        miss_r1 = int((d.loc[r1, "tau_arf"] < d.loc[r1, f"tau_det_{lam}"]).sum())
        k = miss_r1 + int(r2.sum())
        lo, hi = k / n, (k + int(r4.sum())) / n
        print(
            f"      {lam:>4} {int(r1.sum()):>6} {int(r2.sum()):>6} {int(r3.sum()):>6} "
            f"{int(r4.sum()):>7} {lo:>10.4f} {hi:>10.4f} {hi - lo:>8.4f}"
        )
        wlo, whi = wilson(k, n)
        _ligne(
            f"QA l.99 lam={lam}",
            "largeur = P(C_H)",
            f"P_miss identifie a {lo:.4f} (Wilson [{wlo:.4f} ; {whi:.4f}]), "
            f"largeur de l'encadrement {hi - lo:.4f}",
            "QCD_indicateurs_full",
        )

    _sous_titre("dispersion par amplitude a lambda = 8 (l'agregat masque la grille)")
    # PIEGE : tau_det vaut NaN quand il est censure, et (tau_arf < NaN) est False.
    # Compter seulement (tau_arf < tau_det) jetterait donc la region 2, qui est
    # pourtant un Miss CERTAIN (tau_ARF <= H < tau_det). Le « ou censure » la remet.
    g = d.groupby("delta_e").apply(
        lambda x: ((x.tau_arf < x.tau_det_8) | x.censored_det_8.astype(bool)).mean(),
        include_groups=False,
    )
    _ligne(
        "QA l.104",
        "de 0,01 a 1,00 selon l'amplitude",
        f"min {g.min():.2f} (Delta_e = {g.idxmin():.3f}) ; "
        f"max {g.max():.2f} (Delta_e = {g.idxmax():.3f}) ; agregat {g.mean():.4f}",
        "QCD_indicateurs_full ; table 2 de QD1 donne le complement par cellule",
    )

    _sous_titre("controle croise avec QD1 (qui compte l'evenement complementaire)")
    wins = int((d.tau_det_8 < d.tau_arf).sum())
    _ligne(
        "QA <-> QD1",
        "P_miss(lam=8) = 1 - 0,9095",
        f"tau_det < tau_ARF dans {wins}/{n} = {wins / n:.4f} ; "
        f"Miss {n - wins}/{n} = {(n - wins) / n:.4f} ; somme = {(wins + (n - wins)) / n:.4f}",
        "QCD_indicateurs_full",
    )


def _cdfs(sub: pd.DataFrame, lam: int, h: int = H):
    """CDF empiriques de tau_ARF (propre) et tau_det (SOUS-stochastique : tau_det
    vaut NaN quand il est censure, et ces runs ne sont jamais comptes dans F_D)."""
    import numpy as np

    grille = np.arange(0, h + 2)
    n = len(sub)
    ta = sub["tau_arf"].to_numpy()
    td = sub[f"tau_det_{lam}"].to_numpy()
    fa = np.array([(ta <= x).sum() for x in grille]) / n
    fd = np.array([(td <= x).sum() for x in grille]) / n
    return fa, fd, ta, td


def frechet(sub: pd.DataFrame, lam: int):
    """Encadrement universel de la section 3, evalue sur les marginales estimees.

    inf : max(0, sup_s [F_A(s) - F_D(s)])
    sup : min(1, inf_s [F_A(s) + 1 - F_D(s+1)])
    et P_miss observe = region 1 gagnante + region 2 (Miss certain).
    """
    import numpy as np

    fa, fd, ta, td = _cdfs(sub, lam)
    lo = max(0.0, float((fa - fd).max()))
    up = min(1.0, float((fa[:-1] + 1 - fd[1:]).min()))
    miss = float(((ta < td) | np.isnan(td)).mean())
    return lo, miss, up


def qa_frechet() -> None:
    import numpy as np

    d = pd.read_parquet(DATA / "QCD_indicateurs_full.parquet")
    grille = sorted(d["delta_e"].unique())

    _sous_titre("section 3 : la borne de Frechet sur les marginales estimees")
    print(f"      {'lam':>4} {'Delta_e':>9} {'inf':>7} {'P_miss':>7} {'sup':>7} {'largeur':>8}")
    for lam in LAMBDAS:
        larg, dedans = [], 0
        for de in grille:
            lo, m, up = frechet(d[d["delta_e"] == de], lam)
            larg.append(up - lo)
            dedans += int(lo - 1e-12 <= m <= up + 1e-12)
            if de in (grille[0], grille[1], grille[2], grille[19]):
                print(
                    f"      {lam:>4} {de:>9.3f} {lo:>7.2f} {m:>7.2f} {up:>7.2f} {up - lo:>8.2f}"
                )
        lo_p, m_p, up_p = frechet(d, lam)
        _ligne(
            f"QA sec.3 lam={lam}",
            "borne valable quelle que soit la dependance",
            f"P_miss encadre sur {dedans}/20 amplitudes ; largeur par amplitude "
            f"min {min(larg):.3f} max {max(larg):.3f} moyenne {np.mean(larg):.3f} ; "
            f"en agregeant les 20 amplitudes [{lo_p:.3f} ; {up_p:.3f}], largeur {up_p - lo_p:.3f}",
            "QCD_indicateurs_full",
        )


if __name__ == "__main__":
    qa()
    qa_frechet()
