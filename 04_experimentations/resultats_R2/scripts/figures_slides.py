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

# Les trois seuils de R2 sont definis une seule fois, dans le script de
# tracabilite : deux listes qui divergent, c'est deux chiffres qui divergent.
from chiffres_slides import REGIMES

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


def figure_mecanisme():
    """Slide 2 : le mecanisme, en schema.

    SCHEMA STYLISE, aucune donnee. Pour un auditoire qui decouvre le sujet,
    une vraie trajectoire est trop bruitee pour montrer le mecanisme : ce
    qu'il faut voir, c'est que la preuve monte puis REDESCEND sans avoir
    atteint le seuil. La legende de la slide dit « schematic ».
    """
    t = np.linspace(0, 100, 800)
    t0, base, saut, tau = 20.0, 0.10, 0.32, 11.0
    err = np.where(t < t0, base, base + saut * np.exp(-(t - t0) / tau))

    # Preuve accumulee : l'excedent d'erreur au-dessus du niveau de base,
    # moins la tolerance du detecteur. C'est la recurrence de CUSUM.
    exces = np.clip(err - base - 0.055, 0, None)
    preuve = np.cumsum(exces) * (t[1] - t[0])
    seuil = preuve.max() * 1.55

    with plt.rc_context(PLT):
        fig, (h, b) = plt.subplots(2, 1, figsize=(10.5, 6.0), sharex=True,
                                   gridspec_kw={"height_ratios": [1, 1]})

        h.plot(t, err, color="#1b1b1b", lw=2.6)
        h.axvline(t0, color="#b03a2e", lw=1.8, ls="--")
        h.annotate("the world changes", xy=(t0, base + saut), xytext=(6, -6),
                   textcoords="offset points", color="#b03a2e", weight="bold",
                   fontsize=14, va="top")
        h.annotate("the forest repairs itself", xy=(t0 + 2.2 * tau, base + 0.05),
                   xytext=(24, 34), textcoords="offset points", fontsize=14,
                   arrowprops=dict(arrowstyle="->", color="#1b1b1b", lw=1.6))
        h.set_ylabel("model error")
        h.set_yticks([])
        h.grid(alpha=0.15, lw=0.6)

        b.plot(t, preuve, color="#1b1b1b", lw=2.6)
        b.axhline(seuil, color="#b03a2e", lw=2.2, ls=":")
        b.axvline(t0, color="#b03a2e", lw=1.8, ls="--")
        b.annotate("alarm threshold", xy=(2, seuil), xytext=(0, -22),
                   textcoords="offset points", color="#b03a2e", weight="bold",
                   fontsize=14)
        # La distance qui n'est jamais franchie : c'est tout le sujet.
        b.annotate("", xy=(t[-1] * 0.86, seuil),
                   xytext=(t[-1] * 0.86, preuve.max()),
                   arrowprops=dict(arrowstyle="<->", color="#b03a2e", lw=2.0))
        b.text(t[-1] * 0.84, (seuil + preuve.max()) / 2, "the gap", ha="right",
               va="center", color="#b03a2e", weight="bold", fontsize=14)
        b.annotate("evidence stops here.\nthe alarm never fires",
                   xy=(t[-1] * 0.62, preuve.max()), xytext=(-6, -18),
                   textcoords="offset points", fontsize=14, ha="right", va="top")
        b.set_ylabel("evidence for the\nexternal detector")
        b.set_xlabel("time")
        b.set_yticks([])
        b.set_xticks([])
        b.grid(alpha=0.15, lw=0.6)

        fig.tight_layout()
        out = FIGURES / "Fig_slide_mecanisme.png"
        fig.savefig(out, dpi=150, bbox_inches="tight")
        plt.close(fig)
    return out


def figure_deux_horloges():
    """Slide 5 : les deux dates, a une amplitude du milieu de grille.

    Medianes reelles, pas un schema. L'amplitude est choisie pour sa censure
    faible (2 % sur tau_swap(75 %)), et elle est ecrite sur la figure : une
    duree qui ne porte pas son point de grille n'est pas reproductible.
    """
    df = pd.read_parquet(DATA / "QCD_indicateurs_full.parquet")
    g = df.groupby("delta_e")
    med = g.agg(tau_arf=("tau_arf", "median"), tau75=("tau_swap_75", "median"),
                cens=("censored_swap_75", "mean"))
    cible = med.index[np.argmin(np.abs(med.index - 0.24))]
    ligne = med.loc[cible]
    court, long = float(ligne.tau_arf), float(ligne.tau75)

    with plt.rc_context(PLT):
        fig, ax = plt.subplots(figsize=(10.5, 3.2))
        ax.barh([1], [court], height=0.55, color="#b03a2e")
        ax.barh([0], [long], height=0.55, color="#1b1b1b")
        ax.set_ylim(-0.55, 1.55)
        ax.text(court + long * 0.012, 1, f"{court:.0f}", va="center",
                fontsize=17, weight="bold", color="#b03a2e")
        ax.text(long + long * 0.012, 0, f"{long:.0f}", va="center",
                fontsize=17, weight="bold", color="#1b1b1b")
        ax.set_yticks([1, 0])
        ax.set_yticklabels(['called "repaired"\nby the literature',
                            "three quarters of\nthe forest renewed"],
                           fontsize=15)
        ax.set_xlim(0, long * 1.22)
        ax.set_xlabel("observations seen since the change")
        ax.spines[["top", "right", "left"]].set_visible(False)
        ax.tick_params(axis="y", length=0)
        ax.text(1.0, -0.42, f"median of 100 runs, forest of {N_MODELS} trees,"
                f" change size {cible:.2f}", transform=ax.transAxes,
                ha="right", va="top", fontsize=12, color="#6a6a6a")

        out = FIGURES / "Fig_slide_deux_horloges.png"
        fig.savefig(out, dpi=150, bbox_inches="tight")
        plt.close(fig)
    return out, court, long


def figure_drift():
    """Slide 2 : ce qu'est un changement de concept, et ce que le banc simule.

    Fidele au generateur du depot officiel
    (`exp_R2_instrumented_blind_spot.py` l. 74-76) : x0 et x1 sont deux
    normales centrees reduites, l'etiquette vaut 1 si x0 + x1 depasse un
    seuil, et le drift DEPLACE ce seuil de 0 a `boundary_shift`. La bande
    entre les deux frontieres est exactement l'ensemble des points dont
    l'etiquette change, et c'est la tout le changement : les points, eux,
    ne bougent pas.

    Graine fixee ici meme : la figure est un dessin d'illustration, pas une
    mesure, mais elle doit se regenerer a l'identique.
    """
    rng = np.random.default_rng(7)
    n = 420
    x0, x1 = rng.normal(size=n), rng.normal(size=n)
    b = 1.15
    avant, apres = (x0 + x1 > 0.0), (x0 + x1 > b)
    lim = 3.0
    d = np.linspace(-lim, lim, 10)

    with plt.rc_context(PLT):
        fig, axes = plt.subplots(1, 2, figsize=(11, 4.6), sharey=True)
        for ax, lab, titre in ((axes[0], avant, "before"),
                               (axes[1], apres, "after the change")):
            ax.scatter(x0[lab], x1[lab], s=26, marker="o", color="#1b1b1b")
            ax.scatter(x0[~lab], x1[~lab], s=30, marker="x", color="#8a8a8a",
                       linewidths=1.5)
            ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
            ax.set_title(titre)
            ax.set_xticks([]); ax.set_yticks([])
            ax.set_xlabel("input 1"); ax.set_aspect("equal")
        axes[0].set_ylabel("input 2")

        axes[0].plot(d, -d, color="#b03a2e", lw=2.6)
        axes[1].plot(d, b - d, color="#b03a2e", lw=2.6)
        axes[1].plot(d, -d, color="#b03a2e", lw=1.6, ls=":")
        axes[1].fill_between(d, -d, b - d, color="#b03a2e", alpha=0.20)
        axes[1].annotate("these points\nswapped sides", xy=(-0.50, 1.10),
                         xytext=(-2.85, -2.60), fontsize=14, color="#b03a2e",
                         weight="bold",
                         arrowprops=dict(arrowstyle="->", color="#b03a2e", lw=1.8))

        fig.text(0.5, -0.045, "one dot = one observation;  its shape is the "
                 "answer the model has to predict", ha="center", fontsize=13,
                 color="#6a6a6a")
        fig.tight_layout()
        out = FIGURES / "Fig_slide_drift.png"
        fig.savefig(out, dpi=150, bbox_inches="tight")
        plt.close(fig)
    return out


def figure_seuils():
    """Slide 5 : le taux d'alarme depend entierement du reglage du seuil.

    Les trois regimes de R2 ne sont pas trois scenarios, ce sont trois
    valeurs de lambda (`exp_R2_instrumented_blind_spot.py` l. 55-57). Citer
    le seul lambda = 50, ou l'alarme ne part que 3 fois sur 2 000, revient a
    choisir le reglage le plus favorable a la these et a le donner pour le
    cas general : a lambda = 8 l'alarme part dans 96 % des cas. La figure
    montre les trois, c'est la dependance au reglage qui est le resultat.
    """
    lignes = []
    for nom, lam in REGIMES:
        d = pd.read_parquet(DATA_R2 / f"R2_instrumented_{nom}_PHT_ARF.parquet")
        lignes.append((lam, int(d["tau_det"].notna().sum()), len(d)))

    with plt.rc_context(PLT):
        fig, ax = plt.subplots(figsize=(10.5, 4.4))
        # Pas de « lambda » : la notation n'est definie nulle part dans un
        # pitch de trois minutes, et elle ne sert a rien ici.
        lams = [f"{l:.0f}" for l, _, _ in lignes]
        parts = [100 * t / n for _, t, n in lignes]
        couleurs = ["#1b1b1b", "#6a6a6a", "#b03a2e"]
        ax.bar(lams, parts, color=couleurs, width=0.55)
        for i, ((lam, tire, n), part) in enumerate(zip(lignes, parts)):
            ax.text(i, part + 2.5, f"{tire} / {n}", ha="center",
                    fontsize=17, weight="bold", color=couleurs[i])
        ax.set_ylim(0, 112)
        ax.set_ylabel("runs where the alarm fired  (%)")
        ax.set_xlabel("threshold the watchdog must cross")
        ax.set_yticks([0, 25, 50, 75, 100])
        ax.grid(axis="y", alpha=0.18, lw=0.6)
        ax.spines[["top", "right"]].set_visible(False)
        ax.text(0.99, -0.30, "2 000 runs per threshold, same drifts, same seeds",
                transform=ax.transAxes, ha="right", va="top",
                fontsize=12, color="#6a6a6a")

        out = FIGURES / "Fig_slide_seuils.png"
        fig.savefig(out, dpi=150, bbox_inches="tight")
        plt.close(fig)
    return out, lignes


def _petit_arbre(ax, cx, cy, h, couleur, barre=False):
    """Un pictogramme d'arbre binaire : une racine, deux branches, quatre feuilles."""
    seg = [((cx, cy + h / 2), (cx - h / 3, cy)), ((cx, cy + h / 2), (cx + h / 3, cy)),
           ((cx - h / 3, cy), (cx - h / 2, cy - h / 2)),
           ((cx - h / 3, cy), (cx - h / 6, cy - h / 2)),
           ((cx + h / 3, cy), (cx + h / 6, cy - h / 2)),
           ((cx + h / 3, cy), (cx + h / 2, cy - h / 2))]
    for (x0, y0), (x1, y1) in seg:
        ax.plot([x0, x1], [y0, y1], color=couleur, lw=2.0, solid_capstyle="round")
    if barre:
        ax.plot([cx - h / 2, cx + h / 2], [cy + h / 2, cy - h / 2],
                color="#b03a2e", lw=3.0)


def figure_foret():
    """Slide 3 : ce qu'est un arbre de decision, et pourquoi une foret.

    A gauche, le MEME espace et la MEME frontiere que la figure du drift :
    l'arbre ne sait couper que parallelement aux axes, donc il approche la
    diagonale par un escalier. C'est aussi la raison du socle d'erreur
    mesure a 0,0231 pour une erreur de Bayes nulle (JOURNAL.md section 2 a),
    mais ici il ne sert qu'a montrer ce qu'est un arbre.

    A droite, les dix arbres, dont un barre : la foret se repare en
    remplacant ses arbres un par un.
    """
    rng = np.random.default_rng(7)
    n = 300
    x0, x1 = rng.normal(size=n), rng.normal(size=n)
    lab = (x0 + x1 > 0.0)
    lim = 3.0

    with plt.rc_context(PLT):
        fig, (g, d) = plt.subplots(1, 2, figsize=(11.5, 4.5),
                                   gridspec_kw={"width_ratios": [1, 1.35]})

        g.scatter(x0[lab], x1[lab], s=18, marker="o", color="#1b1b1b")
        g.scatter(x0[~lab], x1[~lab], s=22, marker="x", color="#8a8a8a",
                  linewidths=1.3)
        dd = np.linspace(-lim, lim, 10)
        g.plot(dd, -dd, color="#b03a2e", lw=1.6, ls=":")
        # L'escalier : des coupes parallelement aux axes, jamais obliques.
        marches = np.linspace(-lim, lim, 9)
        xs, ys = [], []
        for i in range(len(marches) - 1):
            xs += [marches[i], marches[i + 1]]
            ys += [-marches[i], -marches[i]]
        g.plot(xs, ys, color="#1b1b1b", lw=2.4, drawstyle="default")
        g.set_xlim(-lim, lim); g.set_ylim(-lim, lim)
        g.set_xticks([]); g.set_yticks([]); g.set_aspect("equal")
        g.set_title("one tree", fontsize=16)
        g.set_xlabel("it can only cut straight across", fontsize=13)

        for i in range(10):
            cx, cy = 0.9 + (i % 5) * 1.5, 1.25 if i < 5 else -0.6
            _petit_arbre(d, cx, cy, 0.95, "#1b1b1b", barre=(i == 7))
        d.annotate("failing: thrown away,\na fresh one grows back",
                   xy=(4.45, -0.95), xytext=(7.0, -1.5), fontsize=13,
                   color="#b03a2e", weight="bold", ha="center",
                   arrowprops=dict(arrowstyle="->", color="#b03a2e", lw=1.8))
        d.set_xlim(0, 9.2); d.set_ylim(-2.3, 2.2)
        d.axis("off")
        d.set_title("ten trees, and they vote", fontsize=16)

        fig.tight_layout()
        out = FIGURES / "Fig_slide_foret.png"
        fig.savefig(out, dpi=150, bbox_inches="tight")
        plt.close(fig)
    return out


def figure_watchdog():
    """Slide 4 : comment le detecteur decide.

    Il lit les reponses une par une, empile ce qui depasse du taux normal,
    et alerte au franchissement. Schema stylise, aucune donnee.
    """
    rng = np.random.default_rng(3)
    n = 26
    # Deux regimes, pour que la pile fasse voir les deux choses qui comptent :
    # elle retombe a zero tant que le modele va bien, elle ne monte que
    # pendant la rafale d'erreurs.
    taux = np.where(np.arange(n) < 13, 0.12, 0.62)
    faux = rng.random(n) < taux
    # La vraie recurrence du detecteur, S_t = max(0, S_{t-1} + x_t), et non
    # un cumsum tronque apres coup : c'est la forme que C.2 demontre, et la
    # seule qui reparte de zero quand les erreurs cessent.
    pile, s_t = [], 0.0
    for est_faux in faux:
        s_t = max(0.0, s_t + (1.0 if est_faux else -0.45))
        pile.append(s_t)
    pile = np.array(pile)
    seuil = 3.2

    with plt.rc_context(PLT):
        fig, (h, b) = plt.subplots(2, 1, figsize=(10.5, 4.8), sharex=True,
                                   gridspec_kw={"height_ratios": [1, 2.1]})

        for i in range(n):
            h.text(i, 0, "x" if faux[i] else "o", ha="center", va="center",
                   fontsize=15, weight="bold",
                   color="#b03a2e" if faux[i] else "#8a8a8a")
        h.set_xlim(-1, n); h.set_ylim(-0.6, 0.6)
        h.axis("off")
        h.text(-0.9, 0.45, "the model answers, one observation at a time"
               "   (x = wrong)", fontsize=13, color="#6a6a6a", ha="left")

        b.fill_between(range(n), 0, pile, step="mid", color="#cfcfcf")
        b.plot(range(n), pile, drawstyle="steps-mid", color="#1b1b1b", lw=2.4)
        b.axhline(seuil, color="#b03a2e", lw=2.2, ls=":")
        b.text(0, seuil + 0.25, "threshold", color="#b03a2e", weight="bold",
               fontsize=14)
        franchi = int(np.argmax(pile >= seuil)) if (pile >= seuil).any() else None
        if franchi:
            b.plot([franchi], [pile[franchi]], "v", color="#b03a2e", ms=14)
            b.annotate("alarm", xy=(franchi, pile[franchi]), xytext=(12, 16),
                       textcoords="offset points", color="#b03a2e",
                       weight="bold", fontsize=15)
        b.set_ylabel("pile of excess\nmistakes")
        b.set_xlim(-1, n); b.set_ylim(0, seuil * 1.45)
        b.set_xticks([]); b.set_yticks([])
        b.set_xlabel("time")
        b.grid(alpha=0.15, lw=0.6)

        fig.tight_layout()
        out = FIGURES / "Fig_slide_watchdog.png"
        fig.savefig(out, dpi=150, bbox_inches="tight")
        plt.close(fig)
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--only", choices=["blindspot", "ecarts", "mecanisme",
                                      "horloges", "drift", "seuils",
                                      "foret", "watchdog"])
    a = p.parse_args()

    if a.only in (None, "blindspot"):
        out, n_al, n_ru = figure_blindspot()
        print(f"[slide 3] {out.name}  | alarmes = {n_al} / {n_ru}")
    if a.only in (None, "ecarts"):
        print(f"[annexe ] {figure_ecarts().name}")
    if a.only in (None, "drift"):
        print(f"[slide 2] {figure_drift().name}")
    if a.only in (None, "foret"):
        print(f"[slide 3] {figure_foret().name}")
    if a.only in (None, "watchdog"):
        print(f"[slide 4] {figure_watchdog().name}")
    if a.only in (None, "mecanisme"):
        print(f"[slide 2] {figure_mecanisme().name}")
    if a.only in (None, "seuils"):
        out, lignes = figure_seuils()
        print(f"[slide 5] {out.name}  | " +
              ", ".join(f"lambda {l:.0f} : {t}/{n}" for l, t, n in lignes))
    if a.only in (None, "horloges"):
        out, c, l = figure_deux_horloges()
        print(f"[slide 5] {out.name}  | {c:.0f} pas contre {l:.0f}")


if __name__ == "__main__":
    main()
