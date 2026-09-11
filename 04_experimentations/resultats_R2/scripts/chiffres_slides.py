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


if __name__ == "__main__":
    comptes_r2()
    deux_campagnes_distinctes()
    chiffres_QC1()
