"""
figures_slides.py
===================================================================
Les deux figures de `presentation_pitch_3min.tex`, en version PROJETEE.

POURQUOI REGENERER PLUTOT QUE RECADRER
    `Fig_R2_A_PHT_ARF` et `Fig_QC_ecarts_full` ont ete produites pour une
    largeur d'article A4. Posees a 0,75 de la largeur d'une slide, leurs
    labels tombent sous 10 pt a la projection. Le texte d'une figure doit
    etre au moins aussi gros que le corps de la slide, ce qui se regle par
    la `figsize`, jamais par le facteur d'echelle.

    Deux autres motifs, propres a chaque figure :

    - le panneau du bas de `Fig_R2_*` (« % runs where ARF absorbed drift »)
      ne montre PAS le taux de silence du detecteur : il vaut
      P(tau_det absent OU tau_arf <= tau_det), soit 97,35 % sur le regime B
      quand le taux de silence y est de 59,95 %. Projeter la figure entiere
      ferait dire a l'image le contraire de la voix ;
    - `Fig_QC_ecarts_full` porte deux em-dashes DANS SES PIXELS (titre
      « C.1b --- how far ahead » et axe « Delta e — error jump amplitude »).
      `.claude/rules/redaction.md` les proscrit sur les livrables.

AUCUNE FIGURE EXISTANTE N'EST REECRITE : les sorties portent le prefixe
`Fig_slide_`. Les PNG du depot officiel ne sont pas touches non plus, seuls
ses Parquet sont lus.

ANALYSE PURE. Aucune simulation, aucune campagne relancee.

CONVENTIONS (celles de `figures_revision_QCD.py`)
    anglais ; dpi = 150 ; bbox_inches = "tight" ; marqueur ET style de trait
    distincts par serie, la couleur n'est jamais seule a porter
    l'information ; axes legendes avec unite ; « M = 10 » dans un coin.

USAGE
    PYTHONHASHSEED=0 python figures_slides.py
    PYTHONHASHSEED=0 python figures_slides.py --only blindspot
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RACINE = Path(__file__).resolve().parents[1]
DATA = RACINE / "resultats" / "data"
FIGURES = RACINE / "resultats" / "figures"
FIGURES.mkdir(parents=True, exist_ok=True)

# Le depot officiel : lecture seule, c'est une copie fidele.
OFFICIEL = RACINE.parents[1] / "03_repo_officiel_TheBlindSpotParadox-ICDM2026"
DATA_R2 = OFFICIEL / "results" / "R2_instrumented_blind_spot" / "data"

N_MODELS = 10
LAMBDA_A = 50.0          # exp_R2_instrumented_blind_spot.py l. 55 : regime A

# Taille de police calee sur un corps de slide a 11 pt projete.
PLT = {
    "font.size": 15, "axes.titlesize": 17, "axes.labelsize": 16,
    "xtick.labelsize": 14, "ytick.labelsize": 14, "legend.fontsize": 14,
}


def delta_e_theorique(boundary_shift):
    """La conversion des auteurs, `exp_R2_instrumented_blind_spot.py` l. 114."""
    return norm.cdf(np.asarray(boundary_shift) / np.sqrt(2)) - 0.5


def figure_blindspot():
    """Slide 3 : la courbe du detecteur n'est pas la.

    Un seul panneau. Le panneau du bas de la figure d'origine mesure autre
    chose que ce que dit la voix (voir l'en-tete), il n'est pas repris.
    """
    df = pd.read_parquet(DATA_R2 / "R2_instrumented_A_PHT_ARF.parquet")
    n_runs, n_alarmes = len(df), int(df["tau_det"].notna().sum())

    g = df.groupby("boundary_shift")
    agg = pd.DataFrame({
        "tau_arf": g["tau_arf"].mean(),
        "tau_arf_sem": g["tau_arf"].sem(),
        "tau_det": g["tau_det"].mean(),
    })
    de = delta_e_theorique(agg.index.values)

    with plt.rc_context(PLT):
        fig, ax = plt.subplots(figsize=(10, 5.4))
        ax.errorbar(de, agg["tau_arf"], yerr=agg["tau_arf_sem"],
                    fmt="o-", color="#1b1b1b", lw=2.4, ms=6, capsize=3,
                    label=r"$\tau_{\mathrm{ARF}}$  (forest repairs itself)")
        fini = agg["tau_det"].notna().values
        ax.plot(de[fini], agg["tau_det"].values[fini], "s", color="#b03a2e",
                ms=13, markerfacecolor="none", markeredgewidth=2.6,
                label=rf"$\tau_{{\mathrm{{det}}}}$  (external detector, $\lambda={LAMBDA_A:.0f}$)")

        ax.set_xlabel(r"$\Delta e$  (error jump amplitude)")
        ax.set_ylabel("delay after the drift  (steps)")
        # Pas de titre interne : le titre de la slide 3 le porte deja.
        ax.grid(alpha=0.18, lw=0.6)
        ax.legend(loc="upper right", framealpha=0.95)

        # Pas de `\,` hors mathtext : matplotlib l'afficherait litteralement.
        ax.annotate(
            f"the external detector fired\nin {n_alarmes} of {n_runs} runs",
            xy=(0.045, 0.52), xycoords="axes fraction", fontsize=17,
            color="#b03a2e", weight="bold", va="top")
        # A l'ecart des deux marqueurs tau_det, qui sont vers (0,62 ; 0,30)
        # et (0,37 ; 0,97) en coordonnees d'axe.
        ax.text(0.97, 0.42, f"$M = {N_MODELS}$", transform=ax.transAxes,
                ha="right", va="bottom", fontsize=12, color="#6a6a6a")

        out = FIGURES / "Fig_slide_blindspot_R2.png"
        fig.savefig(out, dpi=150, bbox_inches="tight")
        plt.close(fig)
    return out, n_alarmes, n_runs


def figure_ecarts():
    """Slide 5 : de combien `tau_ARF` devance les quotas plus stricts.

    `q = 0,10` est retire : il vaut `tau_ARF` par construction (C.1 a), donc
    la courbe est plate a zero et ne fait que manger une nuance de gris.
    """
    df = pd.read_parquet(DATA / "QCD_indicateurs_full.parquet")
    # (quota, marqueur, trait, couleur, decalage du label) -- marqueur et trait
    # portent seuls l'information en noir et blanc. Le label de q = 75 % passe
    # SOUS son maximum : au-dessus il chevaucherait le titre.
    series = [(25, "^", ":", "#7f7f7f", (10, 12, "bottom")),
              (50, "s", "--", "#4d4d4d", (10, 12, "bottom")),
              (75, "o", "-", "#1b1b1b", (18, -14, "top"))]

    with plt.rc_context(PLT):
        fig, ax = plt.subplots(figsize=(10, 5.4))
        g = df.groupby("delta_e")
        for q, marq, trait, coul, (dx, dy, va) in series:
            col = f"tau_swap_{q}"
            med = g.apply(lambda x: np.nanmedian(x[col] - x["tau_arf"]),
                          include_groups=False)
            cens = g[f"censored_swap_{q}"].mean()
            ax.plot(med.index, med.values, marker=marq, linestyle=trait,
                    color=coul, lw=2.2, ms=7)
            lourd = (cens > 0.5).values
            if lourd.any():
                ax.plot(med.index[lourd], med.values[lourd], marker=marq,
                        linestyle="none", color=coul, ms=15,
                        markerfacecolor="none", markeredgewidth=2.4)
            # Label pose sur la courbe : pas de legende encadree a decoder.
            # Au maximum, et non au dernier point : les trois courbes
            # convergent vers zero a droite, ou les labels se chevaucheraient.
            i = int(np.nanargmax(med.values))
            ax.annotate(f"$q = {q}\\%$", xy=(med.index[i], med.values[i]),
                        xytext=(dx, dy), textcoords="offset points",
                        color=coul, fontsize=15, weight="bold", va=va)

        ax.set_xlabel(r"$\Delta e$  (error jump amplitude)")
        ax.set_ylabel(r"$\tau_{\mathrm{swap}}(q) - \tau_{\mathrm{ARF}}$  (steps)")
        ax.set_title(r"How far ahead of a real forest renewal $\tau_{\mathrm{ARF}}$ fires")
        ax.grid(alpha=0.18, lw=0.6)
        ax.text(0.98, 0.94,
                "hollow marker: more than 50% of runs censored here",
                transform=ax.transAxes, ha="right", va="top",
                fontsize=12, color="#6a6a6a")
        ax.text(0.98, 0.80, f"$M = {N_MODELS}$", transform=ax.transAxes,
                ha="right", va="top", fontsize=12, color="#6a6a6a")

        out = FIGURES / "Fig_slide_ecarts_swap.png"
        fig.savefig(out, dpi=150, bbox_inches="tight")
        plt.close(fig)
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--only", choices=["blindspot", "ecarts"])
    a = p.parse_args()

    if a.only in (None, "blindspot"):
        out, n_al, n_ru = figure_blindspot()
        print(f"[slide 3] {out.name}  | alarmes = {n_al} / {n_ru}")
    if a.only in (None, "ecarts"):
        print(f"[slide 5] {figure_ecarts().name}")


if __name__ == "__main__":
    main()
