"""
contre_exemple_kendall.py
===================================================================
Contre-exemple a dix executions fictives montrant que le rho de Spearman
surestime l'association quand une part des durees est censuree a l'horizon,
la ou le tau-b de Kendall la neutralise.

CONTROLE SUR CAS CONNU. Les deux coefficients sont calcules DEUX FOIS :
a la main depuis leur definition, puis par scipy. Les deux doivent
coincider -- c'est l'un qui controle l'autre. Aucune donnee de campagne
n'intervient : la reponse est connue d'avance, ce qui en fait un temoin
au sens de `/valider-mesure`.

L'ENONCE DU BUSINESS CASE EST EN DEFAUT
    Il prescrit quatre observees "parfaitement ordonnees". On obtient alors
    rho = tau_b = 1,000 : aucun ecart, donc aucune demonstration. L'artefact
    n'apparait QUE si les observees sont anti-ordonnees entre elles. Les
    deux configurations sont calculees ici et la table les porte toutes les
    deux : c'est l'ecart entre elles qui est le resultat.

POURQUOI L'IMPUTATION AU RANG MAXIMAL EST LICITE
    L'horizon H est le meme pour toutes les executions. Une valeur censuree
    a H depasse donc effectivement toute valeur observee, ce qui autorise a
    les placer au dernier rang, ex aequo entre elles. L'argument TOMBERAIT
    si l'horizon variait d'une execution a l'autre. Voir
    `analyse_QCD.kendall_censored`, meme convention.

SORTIE
    QCD_contre_exemple_kendall.parquet

USAGE
    python contre_exemple_kendall.py
"""

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

RACINE = Path(__file__).resolve().parents[1]
DATA = RACINE / "resultats" / "data"

H = 2000        # horizon commun, identique pour les dix executions
N_OBS = 4       # executions observees
N_CENS = 6      # executions censurees des deux cotes


# ----------------------------------------------------------------------
# Coefficients calcules a la main, depuis leur definition
# ----------------------------------------------------------------------
def tau_b_main(x, y):
    """tau-b de Kendall : (C - D) / sqrt((n0 - t_x)(n0 - t_y)).

    C paires concordantes, D discordantes, n0 = n(n-1)/2, et t_x, t_y les
    corrections de blocs d'ex aequo de chaque cote.
    """
    n = len(x)
    c = d = tx = ty = 0
    for i in range(n):
        for j in range(i + 1, n):
            dx = np.sign(x[i] - x[j])
            dy = np.sign(y[i] - y[j])
            if dx == 0 and dy == 0:
                tx += 1
                ty += 1
            elif dx == 0:
                tx += 1
            elif dy == 0:
                ty += 1
            elif dx * dy > 0:
                c += 1
            else:
                d += 1
    n0 = n * (n - 1) / 2
    denom = np.sqrt((n0 - tx) * (n0 - ty))
    return (c - d) / denom if denom > 0 else np.nan


def rangs_moyens(v):
    """Rangs avec moyenne sur les ex aequo, comme scipy.stats.rankdata."""
    v = np.asarray(v, dtype=float)
    ordre = np.argsort(v, kind="stable")
    rangs = np.empty(len(v), dtype=float)
    i = 0
    while i < len(v):
        j = i
        while j + 1 < len(v) and v[ordre[j + 1]] == v[ordre[i]]:
            j += 1
        moyen = (i + j) / 2 + 1
        for k in range(i, j + 1):
            rangs[ordre[k]] = moyen
        i = j + 1
    return rangs


def rho_main(x, y):
    """rho de Spearman : Pearson sur les rangs moyens."""
    rx, ry = rangs_moyens(x), rangs_moyens(y)
    rx = rx - rx.mean()
    ry = ry - ry.mean()
    denom = np.sqrt((rx ** 2).sum() * (ry ** 2).sum())
    return float((rx * ry).sum() / denom) if denom > 0 else np.nan


# ----------------------------------------------------------------------
# Les deux configurations
# ----------------------------------------------------------------------
def configurations():
    """Deux jeux de dix executions, censurees a H pour les six dernieres.

    Les valeurs des observees sont choisies a la main, sans tirage : le
    contre-exemple doit etre reproductible a la lecture, pas par une graine.
    """
    # x = tau_ARF (jamais censure : censored_arf = 0,0000 sur la campagne),
    # y = comparateur censure a H pour les six dernieres executions.
    x_obs = np.array([10.0, 20.0, 30.0, 40.0])
    x_cens = np.array([50.0, 60.0, 70.0, 80.0, 90.0, 100.0])
    x = np.concatenate([x_obs, x_cens])

    y_ordonne = np.concatenate([[100.0, 200.0, 300.0, 400.0],
                                np.full(N_CENS, float(H))])
    y_anti = np.concatenate([[400.0, 300.0, 200.0, 100.0],
                             np.full(N_CENS, float(H))])

    # (a) la lecture LITTERALE de la prescription : les censurees sont ex aequo
    #     des DEUX cotes, ce qui suppose tau_ARF lui-meme censure. Les deux
    #     coefficients valent alors 1 exactement et le contre-exemple ne montre
    #     rien. Mais l'hypothese est fausse sur la campagne : tau_ARF n'est
    #     jamais censure. C'est la condition d'echec de la prescription, et
    #     elle est plus precise que "quatre observees ordonnees".
    x_bloque = np.concatenate([x_obs, np.full(N_CENS, float(H))])

    return {
        "prescription_litterale": (x_bloque, y_ordonne),
        "ordonnee": (x, y_ordonne),
        "anti_ordonnee": (x, y_anti),
    }


def main():
    configs = configurations()
    lignes = []

    print("Contre-exemple a dix executions, horizon commun H = 2 000")
    print(f"  {N_OBS} observees, {N_CENS} censurees (imputees a H, ex aequo)")

    for nom, (x, y) in configs.items():
        rho_m, rho_s = rho_main(x, y), float(stats.spearmanr(x, y).statistic)
        tb_m, tb_s = tau_b_main(x, y), float(stats.kendalltau(x, y).statistic)

        # Controle sur cas connu : la main et scipy doivent coincider.
        ecart_rho = abs(rho_m - rho_s)
        ecart_tb = abs(tb_m - tb_s)
        if ecart_rho > 1e-12 or ecart_tb > 1e-12:
            raise ValueError(
                f"[{nom}] le calcul a la main et scipy divergent : "
                f"rho {ecart_rho:.2e}, tau_b {ecart_tb:.2e}"
            )

        print(f"\n  configuration '{nom}'")
        print(f"    y observes : {y[:N_OBS].tolist()}")
        print(f"    rho Spearman : main {rho_m:.6f} | scipy {rho_s:.6f} "
              f"| ecart {ecart_rho:.2e}")
        print(f"    tau_b Kendall: main {tb_m:.6f} | scipy {tb_s:.6f} "
              f"| ecart {ecart_tb:.2e}")
        print(f"    ecart rho - tau_b : {rho_m - tb_m:+.6f}")

        for i in range(len(x)):
            lignes.append({
                "configuration": nom,
                "run_fictif": i,
                "x_tau_arf": float(x[i]),
                "y_comparateur": float(y[i]),
                "censure": bool(i >= N_OBS),
                "horizon": H,
                "rho_spearman_main": rho_m,
                "rho_spearman_scipy": rho_s,
                "tau_b_main": tb_m,
                "tau_b_scipy": tb_s,
                "ecart_rho_moins_tau_b": float(rho_m - tb_m),
                "controle_main_vs_scipy_ok": True,
            })

    df = pd.DataFrame(lignes)
    df.to_parquet(DATA / "QCD_contre_exemple_kendall.parquet", index=False)
    print(f"\n-> QCD_contre_exemple_kendall.parquet, "
          f"{df.shape[0]} lignes x {df.shape[1]}")

    print("\nCe que le contre-exemple etablit :")
    etiquettes = {
        "prescription_litterale":
            "la prescription lue au pied de la lettre ne montre RIEN",
        "ordonnee":
            "observees ordonnees, tau_ARF non censure : ecart faible",
        "anti_ordonnee":
            "observees anti-ordonnees : l'artefact apparait",
    }
    for nom, texte in etiquettes.items():
        r = df[df.configuration == nom].iloc[0]
        print(f"  {nom:24s} : rho {r.rho_spearman_main:.4f}, "
              f"tau_b {r.tau_b_main:.4f}, ecart "
              f"{r.ecart_rho_moins_tau_b:+.4f}")
        print(f"  {'':24s}   {texte}")
    print()
    print("  Condition d'echec de la prescription, precisee : rho = tau_b = 1")
    print("  exige des ex aequo des DEUX cotes, donc un tau_ARF lui-meme")
    print("  censure. Sur la campagne, censored_arf = 0,0000 : l'hypothese")
    print("  ne tient pas, et l'exercice prescrit est mal pose.")
    print()


if __name__ == "__main__":
    main()
