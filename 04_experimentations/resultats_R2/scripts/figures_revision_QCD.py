"""
figures_revision_QCD.py
===================================================================
Les neuf figures ajoutees le 10 septembre aux redactions revisees de C.3 et
de D.1 a D.4. Analyse pure : aucune simulation, aucun indicateur recalcule
en dehors de ce que la figure trace. Tout est lu dans `resultats/data/`.

AUCUNE FIGURE EXISTANTE N'EST REECRITE. Les figures de QC1 (`Fig_QC_ecarts_full`,
`Fig_QC_dispersion_swap_full`, `Fig_QC_tauerr_*`) sortent d'`analyse_QCD.py`
et restent telles quelles : leur regeneration changerait le rendu d'un texte
qui n'est pas le notre.

CONVENTIONS COMMUNES
    anglais ; dpi = 150 ; bbox_inches = "tight" ; marqueurs ET styles de trait
    distincts par serie (lisible en noir et blanc, la couleur n'est jamais
    seule a porter l'information) ; axes legendes avec unite ; grille legere ;
    les deux amplitudes hors du domaine de decision (Delta_e < 0,10) grisees
    quand la figure balaie Delta_e ; « M = 10 » dans un coin.

CONTROLE CROISE
    `Fig_QD_course_lambda_full` recalcule les fractions de la course depuis
    `QCD_indicateurs_full` avec son propre code, puis verifie l'egalite avec
    `chiffres_QD.course_par_amplitude`, qui est la reference des tables de
    QD1. Une divergence arrete le script.

USAGE
    PYTHONHASHSEED=0 python figures_revision_QCD.py                  # les 9
    PYTHONHASHSEED=0 python figures_revision_QCD.py --only course     # une seule
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from chiffres_QD import course_par_amplitude, wilson

RACINE = Path(__file__).resolve().parents[1]
DATA = RACINE / "resultats" / "data"
FIGURES = RACINE / "resultats" / "figures"
FIGURES.mkdir(parents=True, exist_ok=True)

N_MODELS = 10
DOMAINE_MIN = 0.10          # domaine de decision de D.4 : Delta_e >= 0,10
LAMBDAS = (8, 25, 50)

# Styles : (marqueur, trait, couleur) -- chaque serie se distingue par le
# marqueur et le trait, la couleur n'est qu'un renfort.
STYLES = [("o", "-", "#1b1b1b"), ("s", "--", "#4d4d4d"), ("^", ":", "#7f7f7f"),
          ("d", "-.", "#2c5f8a"), ("v", "-", "#b03a2e"), ("x", "--", "#8a6d1b")]


def _t(nom):
    return pd.read_parquet(DATA / f"{nom}.parquet")


def _grise_hors_domaine(ax, de_min_grille):
    """Grise la bande Delta_e < 0,10 (les deux amplitudes hors domaine)."""
    ax.axvspan(de_min_grille * 0.9, DOMAINE_MIN, color="#000000", alpha=0.07, lw=0)


def _coin_M(ax, pos="br"):
    """« M = 10 » dans un coin : br (defaut), bl, tr, tl."""
    x, ha = (0.99, "right") if pos[1] == "r" else (0.01, "left")
    y, va = (0.02, "bottom") if pos[0] == "b" else (0.98, "top")
    ax.text(x, y, f"M = {N_MODELS}", transform=ax.transAxes, ha=ha, va=va,
            fontsize=8, color="#555555")


def _save(fig, nom):
    out = FIGURES / nom
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  -> {out}")
    return out


# ----------------------------------------------------------------------
# QC3
# ----------------------------------------------------------------------
def fig_ajustement():
    """Fig_QC_ajustement_full : le fit de l'article et le rectangle, par amplitude."""
    d = _t("QCD_diagnostic_ajustement_full").sort_values("delta_e")
    fig, (a, b) = plt.subplots(1, 2, figsize=(11, 4.2))

    m, ls, c = STYLES[0]
    a.plot(d.delta_e, d.tau_arf_median, marker=m, ls=ls, color=c, label=r"measured median $\tau_{\mathrm{ARF}}$")
    m, ls, c = STYLES[1]
    a.plot(d.delta_e, d.tau_arf_predit, marker=m, ls=ls, color=c, label=r"article fit $18.5\,\Delta e^{-0.98}$")
    a.set_xscale("log"); a.set_yscale("log")
    a.set_xticks([0.03, 0.05, 0.1, 0.2, 0.3, 0.5]); a.set_xticklabels(["0.03", "0.05", "0.1", "0.2", "0.3", "0.5"])
    a.set_yticks([30, 50, 100, 200, 300, 600]); a.set_yticklabels(["30", "50", "100", "200", "300", "600"])
    a.minorticks_off()
    a.set_xlabel(r"$\Delta e$"); a.set_ylabel(r"$\tau_{\mathrm{ARF}}$ (steps, log scale)")
    a.set_title("(a) first replacement: measured vs. fitted")
    a.grid(True, which="major", alpha=0.25); a.legend(fontsize=8, loc="lower left")
    _grise_hors_domaine(a, d.delta_e.min()); _coin_M(a, "tr")

    m, ls, c = STYLES[0]
    b.plot(d.delta_e, d.ratio_mesure_predit, marker=m, ls=ls, color=c,
           label=r"measured / fitted $\tau_{\mathrm{ARF}}$")
    m, ls, c = STYLES[3]
    b.plot(d.delta_e, d.budget_recalcule / d.A_w_mesure, marker=m, ls=ls, color=c,
           label=r"rectangle $\Delta e\cdot\tau_{\mathrm{ARF}}$ / measured $A(w)$")
    b.axhline(1.0, color="#000000", lw=0.9, ls="-", alpha=0.6)
    b.set_xlabel(r"$\Delta e$"); b.set_ylabel("ratio (dimensionless)")
    b.set_title("(b) two ratios against 1")
    b.grid(True, alpha=0.25); b.legend(fontsize=8)
    _grise_hors_domaine(b, d.delta_e.min()); _coin_M(b)
    fig.tight_layout()
    return _save(fig, "Fig_QC_ajustement_full.png")


def fig_budget_utilisable():
    """Fig_QC_budget_utilisable_full : les quatre aires, et la part prise par delta_P.

    Remplace `Fig_QC_budget_full` dans QC3. Cette derniere, produite par
    `analyse_QCD.py`, se lit par la COULEUR (« in blue A(w), in red A(H) »
    dans sa legende) et porte des `---` et un `vs.\ ` litteraux dans son
    titre : elle reste au depot pour le banc, elle ne part pas au rapport.
    """
    d = _t("QCD_budget_preuve_full").sort_values("delta_e")
    fig, (a, b) = plt.subplots(2, 1, figsize=(8, 7), sharex=True,
                               gridspec_kw={"height_ratios": [2.3, 1]})
    m, ls, c = STYLES[0]
    a.plot(d.delta_e, d.A_w_mesure_median, marker=m, ls=ls, color=c,
           label=r"measured $A(w)$, short window, median over seeds")
    m, ls, c = STYLES[4]
    a.plot(d.delta_e, d.A_H_mesure_median, marker=m, ls=ls, color=c,
           label=r"measured $A(H)$, full horizon, median over seeds")
    m, ls, c = STYLES[1]
    a.plot(d.delta_e, d.A_predit_brut, marker=m, ls=ls, color=c,
           label=r"predicted raw budget $18.5\,\Delta e^{0.02}$")
    m, ls, c = STYLES[2]
    a.plot(d.delta_e, d.A_predit_utilisable, marker=m, ls=ls, color=c,
           label=r"predicted usable budget $(1-\delta_P/\Delta e)\times$ raw")
    a.axhline(0, color="#000000", lw=0.9, alpha=0.6)
    a.set_ylabel("excess-error area\n(error units $\\times$ steps)")
    a.set_title("(a) evidence budget: predicted flat, measured not")
    a.grid(True, alpha=0.25); a.legend(fontsize=8, loc="lower left")
    m, ls, c = STYLES[3]
    b.plot(d.delta_e, 100 * d.part_prelevee_par_delta_P, marker=m, ls=ls, color=c, ms=5,
           label=r"share of the raw budget taken by $\delta_P$")
    b.set_ylabel(r"share taken by $\delta_P$ (%)")
    b.set_xlabel(r"$\Delta e$")
    b.set_ylim(0, 40); b.grid(True, alpha=0.25); b.legend(fontsize=8, loc="upper right")
    b.set_title("(b) what the tolerance confiscates", fontsize=10)
    for ax in (a, b):
        _grise_hors_domaine(ax, d.delta_e.min())
    _coin_M(a, "tr")
    fig.tight_layout()
    return _save(fig, "Fig_QC_budget_utilisable_full.png")


# ----------------------------------------------------------------------
# QD1
# ----------------------------------------------------------------------
def _course_independante(ind):
    """Recalcul independant des fractions de la course, pour le controle croise.

    Ecrit sans reprendre `course_par_amplitude` : boucle explicite sur les
    lignes, comptage a la main.
    """
    out = {}
    for lam in LAMBDAS:
        for de in sorted(ind.delta_e.unique()):
            k = n_ok = n = 0
            for _, r in ind[ind.delta_e == de].iterrows():
                n += 1
                if not np.isnan(r[f"tau_det_{lam}"]) and not np.isnan(r["tau_arf"]):
                    n_ok += 1
                    if r[f"tau_det_{lam}"] < r["tau_arf"]:
                        k += 1
            out[(lam, round(float(de), 6))] = (k, n_ok, n)
    return out


def fig_course_lambda():
    """Fig_QD_course_lambda_full : la course par amplitude, avec la censure."""
    ind = _t("QCD_indicateurs_full")
    ref = course_par_amplitude(ind, LAMBDAS)
    indep = _course_independante(ind)
    for r in ref.rename(columns={"lambda": "lam"}).itertuples():
        k, n_ok, n = indep[(r.lam, round(r.delta_e, 6))]
        assert (k, n_ok, n) == (r.victoires_det, r.n_non_censures, r.n_runs), \
            f"controle croise : ({k}, {n_ok}, {n}) != table de reference a lambda = {r.lam}, {r.delta_e}"
        if n_ok:
            lo, hi = wilson(k, n_ok)
            assert abs(lo - r.wilson_lo) < 1e-12 and abs(hi - r.wilson_hi) < 1e-12
    print("  controle croise course : figure = chiffres_QD.course_par_amplitude sur 60 cellules")

    fig, (a, b) = plt.subplots(2, 1, figsize=(8, 7), sharex=True,
                               gridspec_kw={"height_ratios": [2.2, 1]})
    for i, lam in enumerate(LAMBDAS):
        c = ref[ref["lambda"] == lam].sort_values("delta_e")
        m, ls, col = STYLES[i]
        lis = c[c.lisible]
        if len(lis):
            a.errorbar(lis.delta_e, 100 * lis.frac_survivants,
                       yerr=[np.maximum(0, 100 * (lis.frac_survivants - lis.wilson_lo)),
                             np.maximum(0, 100 * (lis.wilson_hi - lis.frac_survivants))],
                       marker=m, ls=ls, color=col, capsize=2, ms=5, lw=1.3,
                       label=rf"$\lambda={lam}$: uncensored runs only (Wilson 95%)")
        a.plot(c.delta_e, 100 * c.frac_imputee, marker=m, ls="none", color=col, ms=5,
               mfc="none", mew=1.2, label=rf"$\lambda={lam}$: all 100 runs, censored = detector loses")
        b.plot(c.delta_e, 100 * c.censure_det, marker=m, ls=ls, color=col, ms=4,
               label=rf"$\lambda={lam}$")
    a.set_ylabel(r"share of runs with $\tau_{\mathrm{det}} < \tau_{\mathrm{ARF}}$ (%)")
    a.set_title("The race by amplitude: the detector's win rate and its censoring")
    a.set_ylim(-3, 103); a.grid(True, alpha=0.25); a.legend(fontsize=7, ncol=2, loc="center right")
    b.axhline(50, color="#000000", lw=0.9, ls="--", alpha=0.6)
    b.text(0.12, 52, "50 % censoring: survivor statistic not plotted above this line",
           ha="left", va="bottom", fontsize=7)
    b.set_ylabel(r"censoring of $\tau_{\mathrm{det}}$ (%)"); b.set_xlabel(r"$\Delta e$")
    b.set_ylim(-3, 103); b.grid(True, alpha=0.25)
    b.legend(fontsize=7, loc="center", bbox_to_anchor=(0.55, 0.72))
    for ax in (a, b):
        _grise_hors_domaine(ax, ref.delta_e.min())
    _coin_M(a, "tl")
    fig.tight_layout()
    return _save(fig, "Fig_QD_course_lambda_full.png")


def fig_palier():
    """Fig_QD_palier_full : le palier mesure contre p0 + Delta_e, et R(tau_ARF)."""
    d = _t("QCD_R_et_G_full").sort_values("delta_e")
    fig, (a, b) = plt.subplots(2, 1, figsize=(7.5, 7), sharex=True)
    m, ls, c = STYLES[0]
    a.plot(d.delta_e, d.e_palier, marker=m, ls=ls, color=c, label=r"measured plateau $\bar e$ just after the drift")
    m, ls, c = STYLES[1]
    a.plot(d.delta_e, d.e_theorique, marker=m, ls=ls, color=c, label=r"stylised plateau $\hat p_0 + \Delta e$")
    m, ls, c = STYLES[4]
    a.plot(d.delta_e, d.ecart_palier_theorie, marker=m, ls=ls, color=c, label="difference (measured $-$ stylised)")
    a.axhline(0, color="#000000", lw=0.9, alpha=0.6)
    a.set_ylabel("error rate"); a.set_title("Post-drift plateau: measured vs. stylised, all 20 amplitudes")
    a.grid(True, alpha=0.25); a.legend(fontsize=8)
    m, ls, c = STYLES[3]
    b.plot(d.delta_e, d.R_tau_arf, marker=m, ls=ls, color=c, label=r"$R(\tau_{\mathrm{ARF}})$, fraction of adaptation acquired")
    b.axhline(0, color="#000000", lw=0.9, alpha=0.6)
    b.set_ylabel(r"$R(\tau_{\mathrm{ARF}})$ (dimensionless)"); b.set_xlabel(r"$\Delta e$")
    b.grid(True, alpha=0.25); b.legend(fontsize=8)
    for ax in (a, b):
        _grise_hors_domaine(ax, d.delta_e.min())
    _coin_M(a, "tl")
    fig.tight_layout()
    return _save(fig, "Fig_QD_palier_full.png")


# ----------------------------------------------------------------------
# QD2
# ----------------------------------------------------------------------
def fig_boxplot():
    """Fig_QD_tau_arf_boxplot_full : tau_ARF par amplitude, medianes annotees.

    ECHELLE : symlog, lineaire sous 1 et logarithmique au-dela. Un axe log pur
    ELIMINE SILENCIEUSEMENT les 34 executions ou tau_ARF = 0 (un arbre est
    remplace au pas de la rupture elle-meme) : matplotlib retire les valeurs
    <= 0 sans un mot, le titre annoncerait 100 graines et la boite en montrerait
    97 a 99. C'est le piege du JOURNAL.md section 10.4, « une echelle qui rend la
    figure muette », dans sa variante silencieuse. Le compte de zeros est en plus
    annote sur la figure.
    """
    ind = _t("QCD_indicateurs_full")
    ic = _t("QCD_ic_medianes_tau_arf")
    ampl = sorted(ind.delta_e.unique())
    data = [ind.loc[ind.delta_e == de, "tau_arf"].to_numpy() for de in ampl]
    n_zeros = [int((d == 0).sum()) for d in data]
    fig, a = plt.subplots(figsize=(10, 4.5))
    a.boxplot(data, positions=range(len(ampl)), widths=0.6, showfliers=True,
              flierprops={"marker": ".", "ms": 3, "alpha": 0.5},
              medianprops={"color": "#1b1b1b", "lw": 1.6},
              boxprops={"color": "#4d4d4d"}, whiskerprops={"color": "#4d4d4d"},
              capprops={"color": "#4d4d4d"})
    a.set_yscale("symlog", linthresh=1.0, linscale=0.35)
    a.set_ylim(-0.35, 2000)
    # marge a gauche : l'annotation de la premiere amplitude s'y loge sans
    # recouvrir ni la boite voisine ni le label de l'axe
    a.set_xlim(-2.6, len(ampl) - 0.3)
    a.axhline(0, color="#999999", lw=0.7, ls=":")
    a.set_xticks(range(len(ampl)))
    a.set_xticklabels([f"{de:.3f}" for de in ampl], rotation=60, fontsize=8)
    a.set_xlabel(r"$\Delta e$")
    a.set_ylabel(r"$\tau_{\mathrm{ARF}}$ (steps, symlog: linear below 1)")
    a.set_title(r"$\tau_{\mathrm{ARF}}$ by amplitude, 100 seeds each: not monotone in $\Delta e$")
    for i, k in enumerate(n_zeros):
        if k:
            a.annotate(str(k), xy=(i, 0), xytext=(i, -0.28), ha="center", va="center",
                       fontsize=6.5, color="#b03a2e")
    a.text(len(ampl) - 0.5, -0.28, r"  runs with $\tau_{\mathrm{ARF}} = 0$",
           ha="left", va="center", fontsize=6.5, color="#b03a2e")
    a.grid(True, axis="y", which="both", alpha=0.25)
    # les quatre annotations sont decalees en x et en y pour ne pas se recouvrir
    decalages = {0: (-0.35, 1.0, "right"), 1: (0.0, 4.2, "center"),
                 2: (1.9, 2.6, "left"), 3: (-0.6, 6.0, "right")}
    for j, r in enumerate(ic.itertuples()):
        i = int(np.argmin(np.abs(np.array(ampl) - r.delta_e)))
        dx, dy, ha = decalages.get(j, (0.0, 2.6, "center"))
        a.annotate(f"median {r.mediane:.0f}\n[{r.ci_lo:g}; {r.ci_hi:g}]",
                   xy=(i, r.mediane), xytext=(i + dx, r.mediane * dy), ha=ha, fontsize=7.5,
                   arrowprops={"arrowstyle": "-", "color": "#555555", "lw": 0.8})
    a.axvspan(-0.5, 1.5, color="#000000", alpha=0.07, lw=0)
    a.text(0.5, 3.0, "outside\ndecision\ndomain", ha="center", va="center",
           fontsize=7, color="#555555")
    a.text(0.99, 0.93, f"M = {N_MODELS}", transform=a.transAxes, ha="right",
           va="top", fontsize=8, color="#555555")
    fig.tight_layout()
    return _save(fig, "Fig_QD_tau_arf_boxplot_full.png")


def fig_contre_exemple():
    """Fig_QD_contre_exemple_kendall : les trois configurations du contre-exemple."""
    d = _t("QCD_contre_exemple_kendall")
    confs = list(dict.fromkeys(d.configuration.tolist()))
    titres = {"prescription_litterale": "(a) prescribed, read literally\n(ties on both sides)",
              "ordonnee": "(b) observed runs ordered,\n" + r"$\tau_{\mathrm{ARF}}$ uncensored",
              "anti_ordonnee": "(c) observed runs anti-ordered,\n" + r"$\tau_{\mathrm{ARF}}$ uncensored"}
    fig, axes = plt.subplots(1, len(confs), figsize=(4.2 * len(confs), 4.2), sharey=True)
    for ax, conf in zip(np.atleast_1d(axes), confs):
        s = d[d.configuration == conf]
        rx = s.x_tau_arf.rank(method="average"); ry = s.y_comparateur.rank(method="average")
        obs = ~s.censure.astype(bool); cen = s.censure.astype(bool)
        ax.plot(rx[obs], ry[obs], "o", color="#1b1b1b", ms=7, label="observed run")
        ax.plot(rx[cen], ry[cen], "o", mfc="none", mec="#1b1b1b", ms=7, mew=1.3, label="censored at $H$")
        rho = float(s.rho_spearman_scipy.iloc[0]); tb = float(s.tau_b_scipy.iloc[0])
        titre = titres.get(conf, conf.replace("_", " "))
        ax.set_title(f"{titre}\n" + rf"$\rho = {rho:.3f}$, $\tau_b = {tb:.3f}$, gap ${rho - tb:.3f}$", fontsize=9)
        # les censures peuvent se superposer exactement : le dire, sinon le
        # lecteur compte les marqueurs et n'en trouve pas dix
        n_cen = int(cen.sum())
        positions = {(round(float(a), 3), round(float(b), 3))
                     for a, b in zip(rx[cen], ry[cen])}
        if n_cen and len(positions) < n_cen:
            x0, y0 = float(rx[cen].iloc[0]), float(ry[cen].iloc[0])
            ax.annotate(f"{n_cen} censored runs\nat one point", xy=(x0, y0),
                        xytext=(x0 - 1.2, y0 - 1.6), ha="center", fontsize=7,
                        arrowprops={"arrowstyle": "->", "color": "#555555", "lw": 0.8})
        ax.set_xlabel(r"rank of $\tau_{\mathrm{ARF}}$ (mid-ranks)")
        ax.grid(True, alpha=0.25)
    np.atleast_1d(axes)[0].set_ylabel("rank of comparator (mid-ranks)")
    np.atleast_1d(axes)[0].legend(fontsize=8, loc="upper left")
    fig.suptitle("Ten fictitious runs, six censored: what separates Spearman from Kendall", fontsize=10)
    fig.tight_layout()
    return _save(fig, "Fig_QD_contre_exemple_kendall.png")


# ----------------------------------------------------------------------
# QD3
# ----------------------------------------------------------------------
def fig_forest():
    """Fig_QD_forest_taub_full : forest plot de tau_b pour A(H) et S_max(H)."""
    st = _t("QCD_correlations_stratifiees_full")
    fig, axes = plt.subplots(1, 2, figsize=(10, 6), sharey=True)
    for ax, comp, titre in zip(axes, ("A_H", "S_max_H"), (r"$A(H)$", r"$S_{\max}(H)$")):
        s = st[st.comparateur == comp].sort_values("delta_e").reset_index(drop=True)
        y = np.arange(len(s))
        for i, r in s.iterrows():
            dans = bool(r.dans_domaine_decision)
            exclut = (r.ci_lo > 0) or (r.ci_hi < 0)
            col = "#1b1b1b" if dans else "#9a9a9a"
            ax.plot([r.ci_lo, r.ci_hi], [i, i], "-", color=col, lw=1.4)
            ax.plot(r.tau_b, i, marker="s" if exclut else "o", color=col, ms=6,
                    mfc=col if exclut else "white", mew=1.3)
        ax.axvline(0, color="#000000", lw=0.9, alpha=0.7)
        ax.set_yticks(y); ax.set_yticklabels([f"{v:.3f}" for v in s.delta_e], fontsize=8)
        ax.set_xlabel(r"Kendall $\tau_b(\tau_{\mathrm{ARF}}, \cdot)$ with bootstrap 95% CI")
        n_ex = int(((s.ci_lo > 0) | (s.ci_hi < 0))[s.dans_domaine_decision].sum())
        n_dom = int(s.dans_domaine_decision.sum())
        ax.set_title(f"{titre}: {n_ex} of {n_dom} intervals exclude zero", fontsize=10)
        ax.grid(True, axis="x", alpha=0.25)
        ax.axhspan(-0.5, 1.5, color="#000000", alpha=0.07, lw=0)
    axes[0].set_ylabel(r"$\Delta e$")
    handles = [plt.Line2D([], [], marker="s", color="#1b1b1b", ls="none", label="CI excludes zero"),
               plt.Line2D([], [], marker="o", color="#1b1b1b", mfc="white", ls="none", label="CI straddles zero"),
               Patch(facecolor="#000000", alpha=0.07, label="outside decision domain")]
    axes[1].legend(handles=handles, fontsize=8, loc="upper left")
    _coin_M(axes[1], "br")
    fig.tight_layout()
    return _save(fig, "Fig_QD_forest_taub_full.png")


# ----------------------------------------------------------------------
# QD4
# ----------------------------------------------------------------------
def fig_censure():
    """Fig_QD_censure_full : taux de censure de chaque duree censurable, par amplitude."""
    st = _t("QCD_correlations_stratifiees_full")
    so = _t("QCD_socle_deux_fenetres")
    so = so[so.baseline_window == 3000].sort_values("delta_e")
    fig, a = plt.subplots(figsize=(8, 4.8))
    i = 0
    for q in (25, 50, 75):
        s = st[st.comparateur == f"tau_swap_{q}"].sort_values("delta_e")
        m, ls, c = STYLES[i]; i += 1
        a.plot(s.delta_e, 100 * s.censure_comparateur, marker=m, ls=ls, color=c, ms=5,
               label=rf"$\tau_{{\mathrm{{swap}}}}({q}\%)$")
    for lam in LAMBDAS:
        m, ls, c = STYLES[i]; i += 1
        a.plot(so.delta_e, 100 * so[f"censure_det_{lam}"], marker=m, ls=ls, color=c, ms=5,
               label=rf"$\tau_{{\mathrm{{det}}}}$, $\lambda={lam}$")
    a.axhline(50, color="#000000", lw=0.9, ls="--", alpha=0.6)
    a.text(so.delta_e.max(), 52, "50 %: no median reported beyond this", ha="right", va="bottom", fontsize=7)
    a.axhline(5, color="#000000", lw=0.7, ls=":", alpha=0.6)
    a.text(so.delta_e.max(), 6, "5 %: benchmark criterion", ha="right", va="bottom", fontsize=7)
    a.set_xlabel(r"$\Delta e$"); a.set_ylabel("runs censored at $H = 2\\,000$ (%)")
    a.set_title("Administrative censoring by amplitude, baseline over 3 000 pre-drift steps")
    a.set_ylim(-3, 103); a.grid(True, alpha=0.25)
    a.legend(fontsize=8, ncol=2, loc="center", bbox_to_anchor=(0.52, 0.72))
    _grise_hors_domaine(a, so.delta_e.min())
    a.text(0.5, 0.12, f"M = {N_MODELS}", transform=a.transAxes, ha="center", va="bottom", fontsize=8, color="#555555")
    fig.tight_layout()
    return _save(fig, "Fig_QD_censure_full.png")


def fig_imputation():
    """Fig_QD_imputation_full : tau_b cas complets contre tau_b impute, par comparateur."""
    cc = _t("QCD_cas_complets_full")
    fig, a = plt.subplots(figsize=(6, 6))
    comps = ["tau_swap_10", "tau_swap_25", "tau_swap_50", "tau_swap_75", "A_H", "S_max_H"]
    noms = {"tau_swap_10": r"$\tau_{\mathrm{swap}}(10\%)$ (tautological)", "tau_swap_25": r"$\tau_{\mathrm{swap}}(25\%)$",
            "tau_swap_50": r"$\tau_{\mathrm{swap}}(50\%)$", "tau_swap_75": r"$\tau_{\mathrm{swap}}(75\%)$",
            "A_H": r"$A(H)$", "S_max_H": r"$S_{\max}(H)$"}
    for i, comp in enumerate(comps):
        s = cc[cc.comparateur == comp]
        m, _, c = STYLES[i]
        if comp == "tau_swap_10":
            a.plot(s.tau_b_impute, s.tau_b_cas_complets, marker=m, ls="none", color=c, ms=9,
                   mfc="none", mew=1.5, label=noms[comp])
        else:
            a.plot(s.tau_b_impute, s.tau_b_cas_complets, marker=m, ls="none", color=c, ms=6, label=noms[comp])
    lim = (-0.3, 1.05)
    a.plot(lim, lim, "-", color="#000000", lw=0.9, alpha=0.6, label="identity")
    a.set_xlim(lim); a.set_ylim(lim)
    a.set_xlabel(r"$\tau_b$, censored runs imputed to the last rank")
    a.set_ylabel(r"$\tau_b$, complete cases only")
    a.set_title("Does censoring drive the coefficient? 120 cells, one per amplitude and comparator", fontsize=9.5)
    ecart = cc.ecart.abs().max()
    a.text(0.03, 0.97, f"largest |difference| = {ecart:.4f}\n(on " + r"$\tau_{\mathrm{swap}}(75\%)$)",
           transform=a.transAxes, va="top", fontsize=8)
    a.annotate("identity, not a measurement:\n" + r"$\tau_{\mathrm{swap}}(10\%) = \tau_{\mathrm{ARF}}$ at $M=10$",
               xy=(1.0, 1.0), xytext=(0.45, 0.8), fontsize=7.5,
               arrowprops={"arrowstyle": "->", "color": "#555555"})
    a.grid(True, alpha=0.25); a.legend(fontsize=7.5, loc="lower right")
    a.text(0.03, 0.86, f"M = {N_MODELS}", transform=a.transAxes, fontsize=8, color="#555555")
    fig.tight_layout()
    return _save(fig, "Fig_QD_imputation_full.png")


FIGURES_DISPO = {
    "ajustement": fig_ajustement, "budget": fig_budget_utilisable,
    "course": fig_course_lambda, "palier": fig_palier,
    "boxplot": fig_boxplot, "kendall": fig_contre_exemple,
    "forest": fig_forest, "censure": fig_censure, "imputation": fig_imputation,
}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--only", choices=sorted(FIGURES_DISPO), default=None)
    a = p.parse_args()
    for nom, f in FIGURES_DISPO.items():
        if a.only is None or a.only == nom:
            print(f"[{nom}]")
            f()


if __name__ == "__main__":
    main()
