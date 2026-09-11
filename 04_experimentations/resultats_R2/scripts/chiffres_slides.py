"""
chiffres_slides.py
===================================================================
Rejeu des chiffres de `presentation_pitch_3min.tex` que
`verif_chiffres_tex.py` ne peut pas atteindre.

POURQUOI CE SCRIPT EXISTE
    `verif_chiffres_tex.py` cherche chaque litteral dans les Parquet de
    `resultats/data/`. L'accroche de la slide 3 ne vient PAS de notre
    campagne : elle vient de la reproduction locale de l'experience R2 des
    auteurs, dont les sorties vivent dans
    `03_repo_officiel_.../results/R2_instrumented_blind_spot/data/`.
    Ces trois comptes seront donc signales « introuvables » par le controle
    general, et c'est normal. Ils se justifient ici.

    Ils NE SONT PAS ajoutes a la liste `EXCLUS` de `verif_chiffres_tex.py` :
    ce script dit lui-meme qu'une exclusion est un moyen de faire passer un
    chiffre faux. On les sort de la porte principale, on les prouve par
    celle-ci.

LECTURE SEULE. N'ecrit aucune table, ne touche a rien dans le depot
officiel, qui est une copie fidele.

CE QUE LE SCRIPT ETABLIT AUSSI
    Que la campagne des auteurs et la notre ne sont PAS la meme, alors
    qu'elles partagent la grille et les graines. La presentation doit dire
    « we re-ran the authors' experiment » en slide 3 et « our own
    instrumented campaign » en slide 5 : le taux de coincidence imprime
    ci-dessous est ce qui rend cette distinction obligatoire.

USAGE
    PYTHONHASHSEED=0 python chiffres_slides.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

RACINE = Path(__file__).resolve().parents[1]
DATA = RACINE / "resultats" / "data"

OFFICIEL = RACINE.parents[1] / "03_repo_officiel_TheBlindSpotParadox-ICDM2026"
DATA_R2 = OFFICIEL / "results" / "R2_instrumented_blind_spot" / "data"

# exp_R2_instrumented_blind_spot.py l. 55-57 : les trois regimes de R2 ne
# sont pas trois scenarios opaques, ce sont trois seuils lambda.
REGIMES = [("A", 50.0), ("B", 25.0), ("C", 8.0)]


def comptes_r2():
    """Slide 3 : combien de fois le detecteur externe a tire, par regime."""
    print("[slide 3] alarmes du detecteur externe, campagne R2 des auteurs")
    print("          rejouee localement (20 amplitudes x 100 graines)\n")
    for nom, lam in REGIMES:
        d = pd.read_parquet(DATA_R2 / f"R2_instrumented_{nom}_PHT_ARF.parquet")
        n, tire = len(d), int(d["tau_det"].notna().sum())
        muet = n - tire
        print(f"  regime {nom} (lambda = {lam:>4.0f}) | ecrit = {tire} / {n}"
              f"  | mesure = {tire} / {n} alarmes"
              f"  | muet = {muet} ({100 * muet / n:.2f} %)"
              f"  | table = R2_instrumented_{nom}_PHT_ARF.parquet")
    print()


def deux_campagnes_distinctes():
    """Le controle qui interdit de dire « la meme campagne » a l'oral."""
    a = pd.read_parquet(DATA_R2 / "R2_instrumented_A_PHT_ARF.parquet")
    q = pd.read_parquet(DATA / "QCD_indicateurs_full.parquet")

    meme_grille = np.allclose(np.sort(a.boundary_shift.unique()),
                              np.sort(q.boundary_shift.unique()))
    memes_graines = sorted(a.seed.unique()) == sorted(q.seed.unique())
    m = a.merge(q[["boundary_shift", "seed", "tau_arf"]],
                on=["boundary_shift", "seed"], suffixes=("_off", "_nous"))
    coincidence = float((m.tau_arf_off == m.tau_arf_nous).mean())

    print("[controle] la campagne des auteurs et la notre")
    print(f"  meme grille de boundary_shift : {meme_grille}")
    print(f"  memes graines                 : {memes_graines}")
    print(f"  tau_arf identiques            : {100 * coincidence:.2f} % des runs")
    if coincidence == 1.0:
        print("  => campagnes confondues : l'oral peut les unifier.")
    else:
        print("  => campagnes DISTINCTES : la slide 3 dit « we re-ran the")
        print("     authors' experiment », la slide 5 « our own instrumented")
        print("     campaign ». Les confondre serait une faute.")
    print()


def chiffres_QC1():
    """Slide 5 : les trois chiffres de C.1, relus dans notre campagne.

    Ils sont deja rejoues par `chiffres_QC.py --sous QC1`, qui reste la
    reference. Repris ici pour que la slide ait une sortie unique a citer.
    """
    q = pd.read_parquet(DATA / "QCD_indicateurs_full.parquet")

    egalite = float((q.tau_arf == q.tau_swap_10).mean())
    violations, comparaisons = 0, 0
    for quota in (25, 50, 75):
        libre = ~q[f"censored_swap_{quota}"].astype(bool)
        comparaisons += int(libre.sum())
        violations += int((q.loc[libre, f"tau_swap_{quota}"]
                           < q.loc[libre, "tau_arf"]).sum())

    g = q.groupby("delta_e")
    ecart = g.apply(lambda x: np.nanmedian(x.tau_swap_75 - x.tau_arf),
                    include_groups=False)
    ratio = g.apply(lambda x: np.nanmedian(x.tau_swap_75 - x.tau_arf)
                    / np.nanmedian(x.tau_arf), include_groups=False)
    # Les 18 amplitudes interpretables de QC1 : censure de tau_swap(75 %)
    # au plus 50 %, ce qui ecarte Delta_e = 0,085 et 0,141.
    interp = (g["censored_swap_75"].mean() <= 0.5).values

    print("[slide 5] les chiffres de C.1, dans notre campagne instrumentee\n")
    print(f"  tau_ARF = tau_swap(10 %)      | ecrit = 100 %"
          f"      | mesure = {100 * egalite:.2f} %")
    print(f"  comparaisons non censurees    | ecrit = 5795"
          f"      | mesure = {comparaisons}")
    print(f"  violations de l'inegalite     | ecrit = 0"
          f"         | mesure = {violations}")
    print(f"  amplitudes interpretables     | ecrit = 18"
          f"        | mesure = {int(interp.sum())}")
    print(f"  ecart a q = 75 %, en pas      | ecrit = 167 a 1368"
          f" | mesure = {ecart.values[interp].min():.0f}"
          f" a {ecart.values[interp].max():.0f}")
    print(f"  le meme, en multiples de tau_ARF | ecrit = 6,0 a 14,3"
          f" | mesure = {ratio.values[interp].min():.1f}"
          f" a {ratio.values[interp].max():.1f}")
    print("  table = QCD_indicateurs_full.parquet\n")


def mesures_en_erreur():
    """Slide 8 (« Measuring the repair in mistakes ») : nos indicateurs.

    Ajoutee le 11/09 a la demande d'Alexandre. Chaque valeur est prise AU
    MEME point de grille que la slide 7 (Delta_e le plus proche de 0,24,
    choisi comme dans `figures_slides.figure_deux_horloges`), pour que le
    public lise les horloges sur une seule echelle.

    tau_rec est `tau_err_p20` de `QCD_tau_err_full` : l'instant ou la courbe
    d'erreur MOYENNEE sur les graines revient sous p0 + rho * Delta_e
    (rho = 0,25) et y reste 20 pas. Il n'existe pas run par run.

    Le 15/18 de S_max(H) est la regle de l'IC retenue en D (JOURNAL.md
    section 10.8) ; la colonne `discernable` applique la regle du seuil et
    donne 14/18 (seule Delta_e = 0,287 bascule). Les deux sont imprimes.
    """
    q = pd.read_parquet(DATA / "QCD_indicateurs_full.parquet")
    te = pd.read_parquet(DATA / "QCD_tau_err_full.parquet")
    co = pd.read_parquet(DATA / "QCD_correlations_stratifiees_full.parquet")

    grille = np.sort(q.delta_e.unique())
    cible = grille[np.argmin(np.abs(grille - 0.24))]
    s = q[q.delta_e == cible]
    ligne_te = te.iloc[np.argmin(np.abs(te.delta_e.to_numpy() - cible))]

    t_arf = float(s.tau_arf.median())
    t_75 = float(s.tau_swap_75.median())
    t_rec = float(ligne_te.tau_err_p20)
    a_h = float(s.A_H.median())
    s_max = float(s.S_max_H.median())

    print(f"[slide 8] nos indicateurs, a Delta_e = {cible:.4f} "
          f"(le point de la slide 7), mediane sur {len(s)} graines\n")
    print(f"  first tree replaced (tau_ARF)   | ecrit = 86     | mesure = {t_arf:.0f}")
    print(f"  error back to normal (tau_rec)  | ecrit = 261    | mesure = {t_rec:.0f}"
          f"  (rho = {ligne_te.rho}, persistance 20 pas, courbe moyenne)")
    print(f"  forest 3/4 renewed (tau_swap75) | ecrit = 1225   | mesure = {t_75:.0f}")
    print(f"  excess mistakes A(H)            | ecrit = 38     | mesure = {a_h:.1f}")
    print(f"  watchdog's peak S_max(H)        | ecrit = 33     | mesure = {s_max:.1f}")
    print(f"  « fourteen times longer » (7)   | ecrit = 14     | mesure = {t_75 / t_arf:.1f}")

    d = co[co.dans_domaine_decision]
    for comp, ecrit in (("A_H", "0/18"), ("S_max_H", "15/18")):
        x = d[d.comparateur == comp]
        ic = int(((x.ci_lo > 0) | (x.ci_hi < 0)).sum())
        seuil = int(x.discernable.sum())
        print(f"  tau_ARF vs {comp:8s}          | ecrit = {ecrit:6s} | mesure = "
              f"{ic}/{len(x)} (regle de l'IC) ; {seuil}/{len(x)} (regle du seuil)")
    print("  tables = QCD_indicateurs_full, QCD_tau_err_full,"
          " QCD_correlations_stratifiees_full\n")


if __name__ == "__main__":
    comptes_r2()
    deux_campagnes_distinctes()
    chiffres_QC1()
    mesures_en_erreur()
