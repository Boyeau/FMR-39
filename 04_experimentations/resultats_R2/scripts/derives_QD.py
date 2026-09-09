"""
derives_QD.py
===================================================================
Les trois derives exiges par l'enonce de la question D qui ne sont dans
aucune table. Tout se calcule HORS LIGNE depuis les Parquet de la campagne
`full` : aucune resimulation, aucune foret instanciee.

CE QUI MANQUAIT
    1. phi(t) = N_t / M avec MEDIANE et ECART INTERQUARTILE inter-graines,
       par amplitude. D.1 l'exige explicitement ; `analyse_QCD.py` ne
       produit que la matrice brute, jamais ses quantiles tabules.

    2. LE SOCLE SUR DEUX FENETRES. Le business case impose de reproduire
       R2 a l'identique (socle sur 1 000 pas), puis de basculer a 3 000
       pas, et de RAPPORTER LES DEUX. `QCD_indicateurs_full.baseline_window`
       ne contient qu'une valeur : 3000. Or p_hat_0 commande tau_det, A(H)
       et S_max(H), donc TOUS les taux de censure cites en D.4. La trace
       pre-rupture de 3 000 pas permet de recalculer le socle a 1 000 pas
       sans resimuler -- la campagne a ete concue pour cela
       (`exp_QCD_campagne.py`, docstring l. 23-26).
       Comparaison au socle theorique : la cible pre-rupture
       y = 1{x0 + x1 > 0} est DETERMINISTE, donc l'erreur de Bayes vaut
       exactement 0 (JOURNAL.md section 2 a). Tout le socle mesure est de
       l'erreur d'approximation, dont une part est fabriquee par le
       mecanisme de remplacement lui-meme (section 2 b).

    3. LA COLONNE n_models. `experimentation.md` exige une colonne par
       parametre de grille. M = 10 ne vient aujourd'hui que du defaut
       `exp_QCD_campagne.py:67` : une ligne qui ne porte pas son M n'est
       pas rejouable, et phi(t) = N_t / M en depend directement.

SORTIES
    QCD_derives_QD.parquet          phi(t) median + IQR par amplitude
    QCD_socle_deux_fenetres.parquet socle, tau_det et censure, 1 000 vs 3 000

USAGE
    python derives_QD.py --tag full
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

import analyse_QCD as aq

RACINE = Path(__file__).resolve().parents[1]
DATA = RACINE / "resultats" / "data"

# Instants ou phi(t) est tabule. Choisis avant lecture des resultats, sur des
# reperes du dispositif (H = 2000) et non sur la forme des courbes.
INSTANTS_PHI = (25, 50, 100, 200, 400, 800, 1200, 1600, 1999)

# Les deux fenetres imposees par le business case.
FENETRES_SOCLE = (1000, 3000)

# Socle theorique : cible pre-rupture deterministe, erreur de Bayes nulle.
SOCLE_THEORIQUE = 0.0


# ----------------------------------------------------------------------
# 1. phi(t) = N_t / M : mediane et ecart interquartile inter-graines
# ----------------------------------------------------------------------
def phi_quantiles(meta, events, n_models):
    """Mediane et IQR de phi(t) par amplitude, aux instants tabules.

    phi est reconstruit par `analyse_QCD.phi_matrix`, qui ne compte que les
    arbres DISTINCTS : un arbre remplace trois fois ne vaut qu'un.
    """
    phi = aq.phi_matrix(events, len(meta))
    lignes = []
    for de, grp in meta.groupby("delta_e", sort=True):
        runs = grp["run_id"].to_numpy()
        bloc = phi[runs]
        for t in INSTANTS_PHI:
            col = bloc[:, t]
            q1, med, q3 = np.percentile(col, [25, 50, 75])
            lignes.append({
                "delta_e": float(de),
                "t": int(t),
                "n_models": int(n_models),
                "n_seeds": int(len(runs)),
                "phi_median": float(med),
                "phi_q1": float(q1),
                "phi_q3": float(q3),
                "phi_iqr": float(q3 - q1),
                "phi_mean": float(col.mean()),
                "n_trees_median": float(med * n_models),
                "frac_forest_fully_renewed": float((col >= 1.0).mean()),
            })
    return pd.DataFrame(lignes)


# ----------------------------------------------------------------------
# 2. Le socle sur deux fenetres
# ----------------------------------------------------------------------
def socle_deux_fenetres(meta, error_mat, events, traces_pre, n_models):
    """Recalcule p_hat_0 sur 1 000 et 3 000 pas, puis tout ce qui en depend.

    La trace pre-rupture porte t_pre de -3000 a -1. Le socle sur W pas est la
    moyenne de e sur t_pre >= -W. Aucune resimulation : c'est exactement le
    calcul de `exp_QCD_campagne.run_one`, rejoue hors ligne.
    """
    pre = traces_pre.sort_values(["run_id", "t_pre"], kind="stable")
    n_runs = len(meta)
    largeur = pre.groupby("run_id", sort=True).size().unique()
    if len(largeur) != 1:
        raise ValueError(f"traces pre-rupture de longueurs heterogenes : {largeur}")
    largeur = int(largeur[0])
    e_pre = pre["e"].to_numpy().reshape(n_runs, largeur)
    t_pre = pre["t_pre"].to_numpy()[:largeur]

    lignes = []
    socles = {}
    for w in FENETRES_SOCLE:
        if w > largeur:
            raise ValueError(f"fenetre {w} > {largeur} pas enregistres")
        masque = t_pre >= -w
        if int(masque.sum()) != w:
            raise ValueError(f"fenetre {w} : {int(masque.sum())} pas selectionnes")
        p0 = e_pre[:, masque].mean(axis=1)
        socles[w] = p0

        # Tout le derive se recalcule avec CE socle.
        s_mat = aq.cusum_path(error_mat, p0[:, None])
        a_h = (error_mat - p0[:, None]).sum(axis=1)
        s_max = s_mat.max(axis=1)

        for de, grp in meta.groupby("delta_e", sort=True):
            runs = grp["run_id"].to_numpy()
            ligne = {
                "delta_e": float(de),
                "baseline_window": int(w),
                "n_models": int(n_models),
                "n_seeds": int(len(runs)),
                "p_hat_0_median": float(np.median(p0[runs])),
                "p_hat_0_mean": float(p0[runs].mean()),
                "p_hat_0_std": float(p0[runs].std(ddof=1)),
                "socle_theorique": SOCLE_THEORIQUE,
                "ecart_au_socle_theorique": float(np.median(p0[runs]) - SOCLE_THEORIQUE),
                "A_H_median": float(np.median(a_h[runs])),
                "S_max_H_median": float(np.median(s_max[runs])),
            }
            for lam in aq.LAMBDAS:
                atteint = (s_mat[runs] >= lam).any(axis=1)
                td = np.where(
                    atteint,
                    (s_mat[runs] >= lam).argmax(axis=1).astype(float),
                    np.nan,
                )
                li = int(lam)
                ligne[f"censure_det_{li}"] = float(1.0 - atteint.mean())
                # JOURNAL.md section 9.5 : pas de mediane de delai au-dela de
                # 50 % de censure. La colonne existe, mais elle est mise a NaN.
                ligne[f"tau_det_{li}_median"] = (
                    float(np.nanmedian(td)) if atteint.mean() > 0.5 else np.nan
                )
            lignes.append(ligne)

    df = pd.DataFrame(lignes)

    # Controle : les deux fenetres doivent donner des socles differents, sans
    # quoi le recalcul n'a rien fait.
    ecart = float(np.abs(socles[1000] - socles[3000]).max())
    if ecart == 0.0:
        raise ValueError("les deux fenetres donnent le meme socle : recalcul muet")
    print(f"  controle : ecart max entre les deux socles = {ecart:.6f} (non nul, OK)")

    # Controle : le socle a 3 000 pas doit reproduire celui de la campagne.
    ref = meta["p_hat_0"].to_numpy()
    ecart_ref = float(np.abs(socles[3000] - ref).max())
    print(f"  controle : socle recalcule a 3 000 pas contre la campagne, "
          f"ecart max = {ecart_ref:.2e}")
    if ecart_ref > 1e-12:
        raise ValueError(
            f"le socle recalcule a 3 000 pas ne reproduit pas la campagne "
            f"(ecart {ecart_ref:.2e}) : le recalcul hors ligne est invalide"
        )

    # Les deux controles vont dans une TABLE, pas seulement sur la sortie
    # standard : un controle qui n'existe que dans un `print` n'est pas
    # relisable, et c'est un chiffre que la redaction cite.
    controles = pd.DataFrame([
        {"controle": "ecart_max_entre_les_deux_socles",
         "valeur": ecart, "seuil": 0.0, "sens": "doit etre > 0",
         "passe": ecart > 0.0},
        {"controle": "socle_3000_contre_campagne",
         "valeur": ecart_ref, "seuil": 1e-12, "sens": "doit etre <= seuil",
         "passe": ecart_ref <= 1e-12},
    ])
    controles.to_parquet(DATA / "QCD_socle_controles.parquet", index=False)
    return df, socles


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--tag", default="full")
    p.add_argument("--n-models", type=int, default=aq.N_MODELS,
                   help="M de la campagne ; defaut = celui de analyse_QCD")
    a = p.parse_args()

    print(f"Lecture de la campagne '{a.tag}' (M = {a.n_models})")
    meta, error_mat, events = aq.load_campaign(a.tag)
    traces_pre = pd.read_parquet(DATA / f"QCD_traces_pre_{a.tag}.parquet")

    print("\n1. phi(t) = N_t / M, mediane et ecart interquartile")
    phi = phi_quantiles(meta, events, a.n_models)
    phi.to_parquet(DATA / "QCD_derives_QD.parquet", index=False)
    print(f"   -> QCD_derives_QD.parquet, {phi.shape[0]} lignes x {phi.shape[1]}")
    apercu = phi[phi.t.isin((100, 400, 1999))]
    print(apercu.groupby("t")[["phi_median", "phi_iqr"]]
          .describe()[[("phi_median", "min"), ("phi_median", "max"),
                       ("phi_iqr", "min"), ("phi_iqr", "max")]]
          .to_string())

    print("\n2. Le socle sur deux fenetres")
    socle, _ = socle_deux_fenetres(meta, error_mat, events, traces_pre, a.n_models)
    socle.to_parquet(DATA / "QCD_socle_deux_fenetres.parquet", index=False)
    print(f"   -> QCD_socle_deux_fenetres.parquet, "
          f"{socle.shape[0]} lignes x {socle.shape[1]}")
    for w in FENETRES_SOCLE:
        s = socle[socle.baseline_window == w]
        print(f"   fenetre {w:5d} pas : p_hat_0 median "
              f"{s.p_hat_0_median.min():.6f} a {s.p_hat_0_median.max():.6f}")
        for lam in (8, 25, 50):
            col = f"censure_det_{lam}"
            print(f"      lambda = {lam:2d} : censure "
                  f"{s[col].min():.4f} a {s[col].max():.4f} "
                  f"(moyenne {s[col].mean():.4f})")

    print("\n3. Colonne n_models : ecrite dans les deux tables ci-dessus.")
    print(f"   n_models = {a.n_models} sur "
          f"{phi.n_models.nunique()} valeur(s) distincte(s)")
    print()


if __name__ == "__main__":
    main()
