"""
derives_QC.py
===================================================================
Un derive manquant pour la question C.3 : l'erreur de FIN D'HORIZON par
amplitude et par fenetre. Tout se calcule HORS LIGNE depuis les traces de
la campagne `full` : aucune resimulation.

CE QUI MANQUAIT
    `redaction_QC3_invariance.tex` ecrivait que l'erreur « tombe de 0,024 a
    0,007 en fin d'horizon » et que ce deficit « retranche environ trente
    unites » a l'aire brute. Ni le 0,007 ni le « trente » ne sortaient d'une
    table, et le texte ne disait ni l'amplitude ni la fenetre. Le chiffre
    etait herite de JOURNAL.md section 2 c, ou il n'a pas davantage de
    source. Le premier audit l'a « corrige » par 0,0024, un autre chiffre
    sans fenetre, et seule la reproduction a arrete la chaine.

    Ce script ecrit la table qui manquait : pour chaque amplitude et pour
    trois fenetres (les 50, 100 et 500 derniers pas de l'horizon), l'erreur
    moyenne sur les graines et sur la fenetre, a cote du socle, de A(H) et
    de A(w) lus dans `QCD_budget_preuve_full`. Le deficit A(H) - A(w) est la
    grandeur qui remplace le « environ trente ».

    Deux colonnes disent COMBIEN DE TEMPS l'erreur passe sous le socle, sans
    quoi le deficit n'est pas interpretable : `n_pas_sous_socle` compte les
    pas ou la courbe moyenne est strictement sous p_hat_0, et
    `t_reste_sous_socle` donne le premier instant a partir duquel elle n'en
    ressort plus. Les deux sont des proprietes de l'horizon entier, donc
    constantes sur les trois lignes d'une meme amplitude.

    La grille entiere est ecrite (20 amplitudes) et la colonne `bande_haute`
    marque les 9 amplitudes Delta_e >= 0,452 que QC3 discute. Restreindre la
    table aux 9 aurait cache le reste de la courbe.

SORTIE
    QCD_fin_horizon_full.parquet    60 lignes = 20 amplitudes x 3 fenetres

USAGE
    PYTHONHASHSEED=0 python derives_QC.py --tag full
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

import analyse_QCD as aq

RACINE = Path(__file__).resolve().parents[1]
DATA = RACINE / "resultats" / "data"

# Fenetres de fin d'horizon : nombre de derniers pas sur lesquels l'erreur
# est moyennee. Choisies avant lecture des resultats, sur des reperes ronds.
FENETRES_FIN = (50, 100, 500)

# Bande haute discutee par QC3 (« A(H) croise zero a partir de 0,482 », et
# le paragraphe sur la tache facilitee). Seuil pose sur la grille : les 9
# dernieres amplitudes de linspace(0.1, 4.0, 20) / 8 sont >= 0,452.
SEUIL_BANDE_HAUTE = 0.452


def fin_horizon(meta, error_mat, budget, n_models):
    """Erreur moyenne de fin d'horizon par amplitude et fenetre.

    L'erreur est moyennee sur les 100 graines ET sur les w derniers pas : c'est
    la meme convention que la courbe moyenne de `tau_err_table`, ou e_t vaut 0
    ou 1 par run et n'a de dynamique lisible qu'en moyenne inter-graines.
    """
    lignes = []
    bud = budget.set_index("delta_e")
    for de, grp in meta.groupby("delta_e", sort=True):
        runs = grp["run_id"].to_numpy()
        bloc = error_mat[runs]
        p0 = grp["p_hat_0"].to_numpy()
        # la ligne du budget est cherchee par egalite numerique, pas par
        # arrondi : les deux tables viennent de la meme campagne
        idx = np.flatnonzero(np.isclose(bud.index.to_numpy(), de, atol=1e-12))
        if idx.size != 1:
            raise ValueError(f"amplitude {de} introuvable dans QCD_budget_preuve_full")
        b = bud.iloc[idx[0]]
        for w in FENETRES_FIN:
            fin = bloc[:, -w:]
            # combien de temps la courbe moyenne passe-t-elle sous le socle ?
            courbe = bloc.mean(axis=0)
            sous = courbe < p0.mean()
            jamais_apres = np.flatnonzero(np.cumsum(~sous[::-1])[::-1] == 0)
            t_reste = int(jamais_apres[0]) if jamais_apres.size else -1
            lignes.append({
                "delta_e": float(de),
                "fenetre_derniers_pas": int(w),
                "n_seeds": int(len(runs)),
                "n_models": int(n_models),
                "delta_P": float(aq.DELTA_P),
                "bande_haute": bool(de >= SEUIL_BANDE_HAUTE),
                "p_hat_0_median": float(np.median(p0)),
                "p_hat_0_mean": float(p0.mean()),
                "erreur_fin_horizon": float(fin.mean()),
                "erreur_fin_horizon_std_graines": float(fin.mean(axis=1).std(ddof=1)),
                "erreur_fin_moins_socle": float(fin.mean() - p0.mean()),
                "w_fenetre_courte": int(b["w_fenetre_courte"]),
                "A_H_mesure_median": float(b["A_H_mesure_median"]),
                "A_w_mesure_median": float(b["A_w_mesure_median"]),
                "deficit_A_H_moins_A_w": float(b["A_H_mesure_median"] - b["A_w_mesure_median"]),
                "n_pas_sous_socle": int(sous.sum()),
                "frac_pas_sous_socle": float(sous.mean()),
                # -1 = la courbe ressort du socle jusqu'au dernier pas
                "t_reste_sous_socle": t_reste,
            })
    return pd.DataFrame(lignes)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--tag", default="full")
    p.add_argument("--n-models", type=int, default=aq.N_MODELS)
    a = p.parse_args()

    print(f"Lecture de la campagne '{a.tag}' (M = {a.n_models})")
    meta, error_mat, _events = aq.load_campaign(a.tag)
    budget = pd.read_parquet(DATA / f"QCD_budget_preuve_{a.tag}.parquet")

    df = fin_horizon(meta, error_mat, budget, a.n_models)
    out = DATA / f"QCD_fin_horizon_{a.tag}.parquet"
    df.to_parquet(out, index=False)
    print(f"   -> {out.name}, {df.shape[0]} lignes x {df.shape[1]}")

    # Controle : la premiere amplitude et la derniere doivent avoir la meme
    # taille de bloc, et aucune cellule ne doit etre vide.
    if df.isna().any().any():
        raise ValueError("cellule vide dans QCD_fin_horizon : trou dans la campagne")
    if df.groupby("delta_e").size().nunique() != 1:
        raise ValueError("nombre de fenetres heterogene par amplitude")
    n_haute = int(df[df.bande_haute].delta_e.nunique())
    print(f"   bande haute (Delta_e >= {SEUIL_BANDE_HAUTE}) : {n_haute} amplitudes")

    haut = df[df.bande_haute].pivot(index="delta_e", columns="fenetre_derniers_pas",
                                    values="erreur_fin_horizon")
    print("\n   erreur de fin d'horizon, bande haute (lignes : Delta_e, colonnes : w) :")
    print(haut.to_string(float_format=lambda v: f"{v:.4f}"))
    print()


if __name__ == "__main__":
    main()
