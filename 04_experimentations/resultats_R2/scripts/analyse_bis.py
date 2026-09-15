"""
analyse_bis.py
===================================================================
Reponses aux questions `.bis` du mail de l'encadrant du 15 septembre 2026
(`repo/01_consignes/Questions_bis_15sept.md`).

Analyse HORS LIGNE seulement : aucune campagne n'est relancee ici. Tout se
recalcule depuis les Parquet de `resultats/data/` produits par
`exp_QCD_campagne.py` et `exp_QCD_etalon.py`.

SOUS-COMMANDES
    --c3bis      profil d'erreur post-rupture, temps de fraction, pont avec
                 l'ajustement 18,5 * Delta_e^-0,98 de l'article   (priorite 1)
    --c2bis      cadre d'optimisation de la fenetre w de A(0,w)   (priorite 2)
    --d3bis      matrice de correlation complete, empilee et stratifiee,
                 amplification de Simpson                          (priorite 3)
    --d1bis      dispersion entre arbres : constat, argument, proxy V(t) (pr. 4)
    --c1bis      Z-score de la baisse d'erreur, resultat negatif    (priorite 5)
    --self-check controles sur cas connus (reponse analytique ou simulee)
    --all        tout, dans l'ordre des dependances

CE QUI N'EST PAS FAIT ICI
    La variance transversale entre arbres n'est pas calculable hors ligne :
    aucune table ne porte l'erreur par arbre par pas (cf. --d1bis). Le pilote
    instrumente est un script separe, `exp_bis_pilote_arbres.py`.
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Fonctions reutilisees telles quelles : le module est garde par __main__ et
# n'execute au niveau module que des imports et des constantes.
from analyse_QCD import (
    kendall_censored,
    H,
    DELTA_E_MIN_DECISION,
    TAU_ARF_FIT,
    PERSIST,
)

RACINE = Path(__file__).resolve().parents[1]
DATA = RACINE / "resultats" / "data"
FIGURES = RACINE / "resultats" / "figures"
FIGURES.mkdir(parents=True, exist_ok=True)

# --- Parametres declares AVANT mesure -----------------------------------------
SEED_BOOTSTRAP = 20260915           # graine unique de tous les bootstrap, ecrite en table
N_BOOT_TQ = 2000                    # bootstrap des temps de fraction et de w_opt
N_BOOT_CORR = 1000                  # bootstrap de chaque cellule de correlation
FEN_EINF = (1500, 2000)             # fenetre du niveau asymptotique, declaree avant mesure
FEN_EINF_A = (1500, 1750)           # deux moities, pour le test de platitude
FEN_EINF_B = (1750, 2000)
FEN_ESTART = (0, 5)                 # niveau de depart mesure, 5 pas = 500 observations
FRACTIONS = (0.25, 0.50, 0.90)      # q de t_q
N_SEEDS = 100                       # graines par amplitude dans la campagne `full`
AMPLITUDES_FIG = (0.028186, 0.140949, 0.287108, 0.436013, 0.497661)  # 5 du plan
GRILLE_W = np.concatenate([np.arange(1, 51), np.arange(55, 2001, 5)])  # fine sous 50
W_FIN_OPT = 1.2564                  # racine de 2x e^-x = 1 - e^-x, cas ferme
LN2 = float(np.log(2.0))


# ============================================================== SOCLE ==========
def _pivot_traces(tag):
    """Matrice E (n_runs x H) int8, indexee par run_id croissant."""
    tr = pd.read_parquet(DATA / f"QCD_traces_error_{tag}.parquet")
    n_runs = int(tr.run_id.max()) + 1
    E = np.full((n_runs, H), -1, dtype=np.int8)
    E[tr.run_id.to_numpy(), tr.t.to_numpy()] = tr.e.to_numpy().astype(np.int8)
    if (E < 0).any():
        raise ValueError(f"trace incomplete dans QCD_traces_error_{tag}: "
                         f"{int((E < 0).sum())} cases non remplies")
    return E


def charger_campagne():
    """Campagne principale : E (2000 x 2000) et sa meta, triee par run_id."""
    meta = pd.read_parquet(DATA / "QCD_runs_meta_full.parquet").sort_values("run_id")
    meta = meta.reset_index(drop=True)
    E = _pivot_traces("full")
    if len(meta) != E.shape[0]:
        raise ValueError(f"meta {len(meta)} lignes contre {E.shape[0]} runs")
    return E, meta


def charger_temoin():
    """Temoin sans drift QE2000 : 2000 graines distinctes, delta_e = 0."""
    meta = pd.read_parquet(DATA / "QCD_runs_meta_QE2000_nodrift_M10.parquet")
    meta = meta.sort_values("run_id").reset_index(drop=True)
    E = _pivot_traces("QE2000_nodrift_M10")
    if len(meta) != E.shape[0]:
        raise ValueError(f"meta temoin {len(meta)} lignes contre {E.shape[0]} runs")
    return E, meta


def poids_bootstrap(rng, n_boot, n):
    """Matrice de comptages multinomiaux (n_boot x n).

    Rigoureusement equivalent a un reechantillonnage avec remise pour toute
    statistique fonction de moyennes ; permet de tout passer en produit
    matriciel au lieu d'une boucle.
    """
    return rng.multinomial(n, np.full(n, 1.0 / n), size=n_boot).astype(np.float64)


def premier_franchissement(cond, persistance=PERSIST):
    """Premier t ou `cond` (bool, ... x T) est vraie `persistance` pas de suite.

    Renvoie NaN quand aucune fenetre de `persistance` pas consecutifs n'est
    entierement vraie. JOURNAL section 4 : un premier franchissement sur une
    courbe bruitee sans condition de persistance n'est pas un instant.

    ATTENTION : exiger la condition a CHAQUE pas de la fenetre biaise fortement
    l'instant vers le haut des que le bruit est comparable a la pente. Mesure sur
    le cas connu (--self-check) : t_half = 150 pour une verite de 69. Les temps de
    fraction utilisent donc `franchissement_en_moyenne`, pas cette fonction.
    """
    c = np.asarray(cond, dtype=np.int32)
    T = c.shape[-1]
    if T < persistance:
        return np.full(c.shape[:-1], np.nan)
    cs = np.cumsum(c, axis=-1)
    tot = cs[..., persistance - 1:].copy()
    tot[..., 1:] -= cs[..., :-persistance]
    plein = tot == persistance
    trouve = plein.any(axis=-1)
    idx = plein.argmax(axis=-1).astype(np.float64)
    return np.where(trouve, idx, np.nan)


def franchissement_en_moyenne(x, niveau, persistance=PERSIST):
    """Premier t ou la MOYENNE de `x` sur [t, t+persistance) passe sous `niveau`.

    C'est toujours une condition de persistance -- un pas isole sous le seuil ne
    declenche rien -- mais le bruit y est divise par sqrt(persistance) au lieu
    d'etre subi pas a pas. Le prix est un decalage borne : sur une courbe
    decroissante la moyenne de la fenetre vaut a peu pres x au milieu, donc
    l'instant rendu precede d'environ persistance/2 le franchissement de la
    courbe moyenne. Ce decalage est MESURE sur le cas connu et publie
    (`QCD_bis_self_check.parquet`), au lieu du facteur 2 de la regle pas a pas.

    `x` : (lot x T). `niveau` : (lot,).
    """
    x = np.asarray(x, dtype=np.float64)
    T = x.shape[-1]
    if T < persistance:
        return np.full(x.shape[:-1], np.nan)
    cs = np.cumsum(x, axis=-1)
    som = cs[..., persistance - 1:].copy()
    som[..., 1:] -= cs[..., :-persistance]
    moy = som / persistance
    sous = moy <= np.asarray(niveau, dtype=np.float64)[..., None]
    trouve = sous.any(axis=-1)
    idx = sous.argmax(axis=-1).astype(np.float64)
    return np.where(trouve, idx, np.nan)


def ic_percentile(vals, lo=2.5, hi=97.5):
    v = np.asarray(vals, dtype=np.float64)
    v = v[np.isfinite(v)]
    if v.size == 0:
        return np.nan, np.nan
    return float(np.percentile(v, lo)), float(np.percentile(v, hi))


def se_binomiale(p, n):
    return np.sqrt(np.clip(p, 0.0, 1.0) * (1.0 - np.clip(p, 0.0, 1.0)) / n)


def style_axes(ax, xlabel, ylabel):
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.3, linewidth=0.5)


def amplitudes_proches(valeurs, cibles=AMPLITUDES_FIG):
    """Les amplitudes de la grille les plus proches des 5 representatives."""
    valeurs = np.asarray(sorted(valeurs))
    return [float(valeurs[np.abs(valeurs - c).argmin()]) for c in cibles]


# ====================================================== C.3.bis (priorite 1) ===
def _profil_un_groupe(Emat, p0, delta_e, n_runs):
    """Profil moyen brut d'un bloc de runs. Aucun lissage temporel.

    JOURNAL section 4 : un filtre de longueur L decale tout marqueur de L/2 ;
    la table ne porte donc que la moyenne sur les graines, pas par pas.
    """
    e_mean = Emat.mean(axis=0)
    return pd.DataFrame({
        "delta_e": delta_e,
        "t": np.arange(H, dtype=np.int32),
        "e_mean": e_mean,
        "se": se_binomiale(e_mean, n_runs),
        "n_runs": n_runs,
        "p_hat_0_moyen": float(p0),
    })


def _test_platitude_fin(Emat):
    """Platitude de la fin d'horizon : les deux moities de [1500, 2000).

    L'ecart-type se prend SUR LES GRAINES (l'erreur binomiale ignorerait
    l'autocorrelation de l'erreur d'une foret qui apprend).
    """
    n = Emat.shape[0]
    m1 = Emat[:, FEN_EINF_A[0]:FEN_EINF_A[1]].mean(axis=1)
    m2 = Emat[:, FEN_EINF_B[0]:FEN_EINF_B[1]].mean(axis=1)
    se1 = m1.std(ddof=1) / np.sqrt(n)
    se2 = m2.std(ddof=1) / np.sqrt(n)
    ecart = float(m1.mean() - m2.mean())
    seuil = float(2.0 * np.sqrt(se1 ** 2 + se2 ** 2))
    return ecart, seuil, bool(abs(ecart) <= seuil)


def _test_platitude_debut(e_bar, n_runs):
    """Pente OLS sur les `FEN_ESTART` premiers pas, contre 2 fois son ecart-type."""
    t0, t1 = FEN_ESTART
    t = np.arange(t0, t1, dtype=np.float64)
    y = e_bar[t0:t1]
    tc = t - t.mean()
    sxx = float((tc ** 2).sum())
    pente = float((tc * y).sum() / sxx)
    var = float(((tc / sxx) ** 2 * se_binomiale(y, n_runs) ** 2).sum())
    se_pente = float(np.sqrt(var))
    return pente, se_pente, bool(abs(pente) <= 2.0 * se_pente)


def _temps_fractions(e_bar_lot, e_start_lot, e_inf_lot, n_runs):
    """t_q pour chaque q et chaque ligne de `e_bar_lot` (lot x H).

    Renvoie {q: (t_q, niveau_franchi, marge)}. NaN quand la baisse est nulle ou
    negative, ou quand aucune fenetre de PERSIST pas consecutifs ne tient.
    """
    baisse = e_start_lot - e_inf_lot
    out = {}
    for q in FRACTIONS:
        marge = (1.0 - q) * baisse
        niveau = e_inf_lot + marge
        tq = franchissement_en_moyenne(e_bar_lot, niveau, PERSIST)
        tq = np.where(baisse > 0, tq, np.nan)
        out[q] = (tq, niveau, marge)
    return out


def _bloc_amplitude(Emat, p0_moyen, delta_e, rng, n_runs):
    """Toutes les grandeurs de C.3.bis pour un bloc de runs de meme amplitude."""
    e_bar = Emat.mean(axis=0)
    e_start = float(e_bar[FEN_ESTART[0]:FEN_ESTART[1]].mean())
    e_inf = float(e_bar[FEN_EINF[0]:FEN_EINF[1]].mean())
    ecart_fin, seuil_fin, e_inf_fiable = _test_platitude_fin(Emat)
    pente, se_pente, e_start_plat = _test_platitude_debut(e_bar, n_runs)

    point = _temps_fractions(e_bar[None, :],
                             np.array([e_start]), np.array([e_inf]), n_runs)

    # --- bootstrap sur les graines, par comptages multinomiaux ------------------
    W = poids_bootstrap(rng, N_BOOT_TQ, n_runs)
    Ebar_b = (W @ Emat.astype(np.float64)) / n_runs
    e_start_b = Ebar_b[:, FEN_ESTART[0]:FEN_ESTART[1]].mean(axis=1)
    e_inf_b = Ebar_b[:, FEN_EINF[0]:FEN_EINF[1]].mean(axis=1)
    boot = _temps_fractions(Ebar_b, e_start_b, e_inf_b, n_runs)

    ligne = {
        "delta_e": float(delta_e),
        "n_runs": int(n_runs),
        "seed_bootstrap": SEED_BOOTSTRAP,
        "n_boot": N_BOOT_TQ,
        "fenetre_e_start": f"[{FEN_ESTART[0]}, {FEN_ESTART[1]})",
        "fenetre_e_inf": f"[{FEN_EINF[0]}, {FEN_EINF[1]})",
        "persistance": PERSIST,
        "p_hat_0_moyen": float(p0_moyen),
        "e_start_mesure": e_start,
        "e_start_pente": pente,
        "e_start_pente_se": se_pente,
        "e_start_plat": e_start_plat,
        # colonne de CONTROLE seulement : deja refutee (JOURNAL section 10.3),
        # jamais au denominateur d'un temps de fraction.
        "e_start_theorique": float(p0_moyen + delta_e),
        "e_inf": e_inf,
        "e_inf_ecart_moities": ecart_fin,
        "e_inf_seuil_platitude": seuil_fin,
        "e_inf_fiable": e_inf_fiable,
        "baisse_mesuree": e_start - e_inf,
        # Ecart du palier au socle, en erreurs types : e_inf < p_hat_0 partout, mais
        # l'ecart n'est net qu'en haut de grille, et cela se cite avec son z.
        "se_e_inf": float(se_binomiale(e_inf, n_runs)),
        "z_palier_sous_socle": float((p0_moyen - e_inf) / se_binomiale(e_inf, n_runs))
                               if se_binomiale(e_inf, n_runs) > 0 else np.nan,
    }

    for q in FRACTIONS:
        nom = {0.25: "t_25", 0.50: "t_half", 0.90: "t_90"}[q]
        tq, niveau, marge = point[q]
        tq = float(tq[0])
        niveau = float(niveau[0])
        marge = float(marge[0])
        se_niveau = float(se_binomiale(niveau, n_runs))
        tq_b, _, _ = boot[q]
        lo, hi = ic_percentile(tq_b)
        ligne[nom] = tq
        ligne[f"{nom}_lo"] = lo
        ligne[f"{nom}_hi"] = hi
        ligne[f"niveau_{nom}"] = niveau
        ligne[f"marge_{nom}"] = marge
        ligne[f"deux_se_{nom}"] = 2.0 * se_niveau
        ligne[f"interpretable_{nom}"] = bool(marge > 2.0 * se_niveau)
        ligne[f"taux_non_defini_{nom}"] = float(np.mean(~np.isfinite(tq_b)))

    # --- rapports de forme : le test est t_90/t_half, pas le collapse ----------
    for nom, num, den in (("ratio_t90_t50", 0.90, 0.50), ("ratio_t25_t50", 0.25, 0.50)):
        a = point[num][0][0]
        b = point[den][0][0]
        ligne[nom] = float(a / b) if (np.isfinite(a) and np.isfinite(b) and b > 0) else np.nan
        ab = boot[num][0]
        bb = boot[den][0]
        with np.errstate(divide="ignore", invalid="ignore"):
            r = np.where((bb > 0) & np.isfinite(ab) & np.isfinite(bb), ab / bb, np.nan)
        lo, hi = ic_percentile(r)
        ligne[f"{nom}_lo"] = lo
        ligne[f"{nom}_hi"] = hi
        ligne[f"{nom}_taux_non_defini"] = float(np.mean(~np.isfinite(r)))
    # Valeurs de reference d'une exponentielle pure, connues sans estimation.
    ligne["ratio_t90_t50_exponentielle"] = float(np.log(10.0) / LN2)
    ligne["ratio_t25_t50_exponentielle"] = float(np.log(4.0 / 3.0) / LN2)
    return ligne, e_bar


def _resume_forme(dv):
    """Le verdict de forme et son critere de selection vont dans le meme sens.

    Cette table le chiffre : correlation du rapport t_90/t_half a l'amplitude, et
    moyenne du rapport de part et d'autre du seuil de lisibilite. Un verdict qui
    ne vaut que sur le sous-ensemble ou l'estimateur est le plus bas doit porter
    ce chiffre avec lui.
    """
    from scipy.stats import spearmanr
    d = dv[~dv.temoin_sans_drift]
    m = d.ratio_t90_t50.notna()
    rho, pval = spearmanr(d.delta_e[m], d.ratio_t90_t50[m])
    lis, non = d[d.interpretable_t_90], d[~d.interpretable_t_90]
    t = pd.DataFrame([{
        "grandeur": "ratio_t90_t50",
        "spearman_rho_contre_delta_e": float(rho),
        "spearman_p": float(pval),
        "n_amplitudes_definies": int(m.sum()),
        "moyenne_amplitudes_lisibles": float(lis.ratio_t90_t50.mean()),
        "moyenne_amplitudes_non_lisibles": float(non.ratio_t90_t50.mean()),
        "n_lisibles": int(len(lis)), "n_non_lisibles": int(len(non)),
        "reference_exponentielle": float(np.log(10.0) / LN2),
        "marge_sur_2se_min_lisibles": float((lis.marge_t_90 / lis.deux_se_t_90).min()),
        "marge_sur_2se_max_non_lisibles": float((non.marge_t_90 / non.deux_se_t_90).max()),
    }])
    t.to_parquet(DATA / "QCD_bis_forme_resume.parquet", index=False)
    print(f"  forme : rho de Spearman du rapport contre l'amplitude {rho:.4f} "
          f"(p = {pval:.4f}) ; moyenne {lis.ratio_t90_t50.mean():.4f} sur les lisibles "
          f"contre {non.ratio_t90_t50.mean():.4f} ailleurs")
    return t


def run_c3bis(args):
    print("[C.3.bis] profil d'erreur post-rupture, temps de fraction, pont avec l'article")
    rng = np.random.default_rng(SEED_BOOTSTRAP)
    E, meta = charger_campagne()
    ind = pd.read_parquet(DATA / "QCD_indicateurs_full.parquet")
    tau_med = ind.groupby("delta_e")["tau_arf"].median()

    profils, lignes, courbes = [], [], {}
    for de, grp in meta.groupby("delta_e", sort=True):
        idx = grp.run_id.to_numpy()
        Emat = E[idx]
        p0 = float(grp.p_hat_0.mean())
        profils.append(_profil_un_groupe(Emat, p0, float(de), len(idx)))
        ligne, e_bar = _bloc_amplitude(Emat, p0, float(de), rng, len(idx))
        ligne["tau_arf_median"] = float(tau_med.loc[de])
        ligne["tau_arf_article"] = float(TAU_ARF_FIT[0] * de ** TAU_ARF_FIT[1])
        ligne["temoin_sans_drift"] = False
        lignes.append(ligne)
        courbes[float(de)] = e_bar

    # --- le temoin sans drift entre dans les deux tables, delta_e = 0 ----------
    Et, metat = charger_temoin()
    p0t = float(metat.p_hat_0.mean())
    profils.append(_profil_un_groupe(Et, p0t, 0.0, Et.shape[0]))
    ligne_t, e_bar_t = _bloc_amplitude(Et, p0t, 0.0, rng, Et.shape[0])
    ligne_t["tau_arf_median"] = np.nan
    ligne_t["tau_arf_article"] = np.nan
    ligne_t["temoin_sans_drift"] = True
    lignes.append(ligne_t)

    prof = pd.concat(profils, ignore_index=True)
    prof.to_parquet(DATA / "QCD_bis_profil_erreur.parquet", index=False)
    dv = pd.DataFrame(lignes)
    dv.to_parquet(DATA / "QCD_bis_demi_vie.parquet", index=False)

    # --- controle de non-regression sur e_inf ---------------------------------
    fh = pd.read_parquet(DATA / "QCD_fin_horizon_full.parquet")
    fh500 = fh[fh.fenetre_derniers_pas == 500].set_index("delta_e")["erreur_fin_horizon"]
    ref = dv[~dv.temoin_sans_drift].set_index("delta_e")["e_inf"]
    ecart = float((ref - fh500.reindex(ref.index)).abs().max())
    print(f"  non-regression e_inf contre QCD_fin_horizon_full (fenetre 500) : "
          f"ecart max {ecart:.3e}")
    if ecart > 1e-9:
        raise ValueError(f"e_inf ne reproduit pas erreur_fin_horizon : ecart {ecart:.3e}")

    _resume_forme(dv)
    _figures_c3bis(prof, dv, courbes, e_bar_t)
    aff = dv[~dv.temoin_sans_drift]
    print(aff[["delta_e", "e_start_mesure", "e_inf", "e_inf_fiable", "t_25", "t_half",
               "t_90", "interpretable_t_90", "ratio_t90_t50", "tau_arf_median",
               "tau_arf_article"]].to_string(index=False,
                                             float_format=lambda v: f"{v:9.4f}"))
    print(f"[OK] QCD_bis_profil_erreur.parquet ({len(prof)} lignes), "
          f"QCD_bis_demi_vie.parquet ({len(dv)} lignes)")
    return dv


STYLES = ["-", "--", "-.", ":", (0, (5, 1, 1, 1))]
GRIS = [0.0, 0.25, 0.45, 0.62, 0.78]


def _figures_c3bis(prof, dv, courbes, e_bar_temoin):
    reps = amplitudes_proches(courbes.keys())
    dvi = dv.set_index("delta_e")

    # --- 1. profils bruts, deux panneaux ---------------------------------------
    # Aucun lissage : JOURNAL section 10.4. Le bruit binomial a 100 graines vaut
    # +/- 0,05 en haut de grille, d'ou le decoupage transitoire / fin d'horizon
    # plutot qu'une seule vue de 2 000 pas ou rien ne se lit.
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.4))
    for k, de in enumerate(reps):
        e_bar = courbes[de]
        n = int(dvi.loc[de, "n_runs"])
        se = se_binomiale(e_bar, n)
        t = np.arange(H)
        axes[0].plot(t, e_bar, linestyle=STYLES[k], color=str(GRIS[k]), linewidth=1.1,
                     label=f"$\\Delta e$ = {de:.3f}")
        axes[0].fill_between(t, e_bar - 2 * se, e_bar + 2 * se, color=str(GRIS[k]),
                             alpha=0.10, linewidth=0)
        for col, mark in (("tau_arf_median", "o"), ("t_half", "s"), ("t_90", "^")):
            v = dvi.loc[de, col]
            if not np.isfinite(v) or v > 250:
                continue
            if col == "t_90" and not bool(dvi.loc[de, "interpretable_t_90"]):
                continue
            axes[0].plot([v], [e_bar[int(v)]], mark, color=str(GRIS[k]), markersize=6,
                         markerfacecolor="white", markeredgewidth=1.1)
        # Moyennes par blocs DISJOINTS de 100 pas : une agregation declaree, pas
        # un lissage glissant. Aucun marqueur temporel n'est pose sur ce panneau,
        # donc aucun decalage de L/2 n'est en jeu (JOURNAL section 10.4).
        blocs = e_bar[:H].reshape(-1, 100).mean(axis=1)
        axes[1].step(np.arange(0, H, 100) + 100, blocs, where="pre",
                     linestyle=STYLES[k], color=str(GRIS[k]), linewidth=1.2,
                     label=f"$\\Delta e$ = {de:.3f}")
        axes[1].hlines(float(dvi.loc[de, "e_inf"]), FEN_EINF[0], FEN_EINF[1],
                       color=str(GRIS[k]), linestyle="-", linewidth=2.4, alpha=0.55)
    axes[0].plot(np.arange(H), e_bar_temoin, linestyle=(0, (1, 3)), color="0.55",
                 linewidth=0.9, label="no-drift control ($\\Delta e$ = 0)")
    p0 = float(prof[prof.delta_e > 0].p_hat_0_moyen.mean())
    for ax in axes:
        ax.axhline(p0, color="0.2", linewidth=0.9, linestyle=(0, (4, 4)))
    axes[0].set_xlim(0, 250)
    axes[0].annotate("$\\hat{p}_0$", xy=(252, p0), xytext=(215, p0 + 0.035), fontsize=9)
    style_axes(axes[0], "steps since the change", "error rate (mean over seeds)")
    axes[0].set_title("Transient: first 250 steps\n"
                      "circle = median $\\tau_{ARF}$, square = $t_{1/2}$, "
                      "triangle = $t_{90}$ where interpretable", fontsize=9)
    axes[0].legend(fontsize=8, loc="upper right")
    axes[1].set_xlim(0, H)
    axes[1].set_ylim(0, 0.075)
    style_axes(axes[1], "steps since the change", "error rate (mean over seeds)")
    axes[1].set_title("Full horizon, zoomed on the floor\n"
                      "means over disjoint 100-step blocks; thick segment = "
                      "$e_\\infty$ on [1500, 2000)", fontsize=9)
    axes[1].legend(fontsize=7.5, loc="upper right")
    fig.savefig(FIGURES / "Fig_bis_profil_erreur.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # --- 2. collapse : ILLUSTRATION, pas un test de forme -----------------------
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2))
    for k, de in enumerate(reps):
        e_bar = courbes[de]
        e_start = float(dvi.loc[de, "e_start_mesure"])
        e_inf = float(dvi.loc[de, "e_inf"])
        th = float(dvi.loc[de, "t_half"])
        if not np.isfinite(th) or th <= 0 or e_start <= e_inf:
            continue
        y = (e_bar - e_inf) / (e_start - e_inf)
        t = np.arange(H)
        axes[0].plot(t, y, linestyle=STYLES[k], color=str(GRIS[k]), linewidth=1.1,
                     label=f"$\\Delta e$ = {de:.3f}")
        axes[1].plot(t / th, y, linestyle=STYLES[k], color=str(GRIS[k]), linewidth=1.1,
                     label=f"$\\Delta e$ = {de:.3f}")
    for ax, xl, xmax in ((axes[0], "steps since the change", 600),
                         (axes[1], "steps / $t_{1/2}$ (dimensionless)", 8)):
        ax.axhline(0.5, color="0.4", linewidth=0.7, linestyle=(0, (3, 3)))
        ax.set_xlim(0, xmax)
        ax.set_ylim(-0.4, 1.15)
        style_axes(ax, xl, "$(\\bar{e}_t - e_\\infty)/(e_{start} - e_\\infty)$")
    axes[0].legend(fontsize=8)
    fig.suptitle("Illustration only: rescaling by $t_{1/2}$ forces every curve through 0.5 "
                 "at $x = 1$.\nThe shape test is the ratio $t_{90}/t_{1/2}$, not this collapse.",
                 fontsize=9)
    fig.savefig(FIGURES / "Fig_bis_profil_collapse.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # --- 3. le pont avec l'ajustement de l'article ------------------------------
    d = dv[~dv.temoin_sans_drift].sort_values("delta_e")
    fig, ax = plt.subplots(figsize=(7.6, 5.0))
    ax.plot(d.delta_e, d.tau_arf_article, "-", color="0.0", linewidth=1.4,
            label="article: $18.5\\,\\Delta e^{-0.98}$")
    ax.plot(d.delta_e, d.tau_arf_median, "o--", color="0.25", markersize=4.5,
            markerfacecolor="white", linewidth=1.0, label="median $\\tau_{ARF}$ (measured)")
    ax.plot(d.delta_e, d.t_half, "s-.", color="0.45", markersize=4.5,
            markerfacecolor="white", linewidth=1.0, label="$t_{1/2}$ of the error profile")
    lis = d[d.interpretable_t_90]
    gri = d[~d.interpretable_t_90]
    ax.plot(lis.delta_e, lis.t_90, "^", color="0.15", markersize=6,
            label="$t_{90}$ (interpretable)")
    ax.plot(gri.delta_e, gri.t_90, "^", color="0.75", markersize=5,
            markerfacecolor="none", label="$t_{90}$ (below $2\\,se$, not read)")
    ax.errorbar(d.delta_e, d.t_half, yerr=[d.t_half - d.t_half_lo, d.t_half_hi - d.t_half],
                fmt="none", ecolor="0.45", elinewidth=0.8, capsize=2)
    ax.set_xscale("log")
    ax.set_yscale("log")
    style_axes(ax, "change size $\\Delta e$ (log)", "steps since the change (log)")
    ax.set_title("Characteristic time of the error against the article's fit", fontsize=10)
    ax.legend(fontsize=8)
    fig.savefig(FIGURES / "Fig_bis_demi_vie_vs_article.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


# ====================================================== C.2.bis (priorite 2) ===
def _aires_cumulees(E, meta):
    """A(0,w) par run pour tout w : somme cumulee de (e_t - p_hat_0) du run.

    A(0,H) redonne exactement `A_H` de QCD_indicateurs_full (meme definition,
    analyse_QCD.py l. 154) : c'est le controle de non-regression de la tache.
    """
    p0 = meta.p_hat_0.to_numpy(dtype=np.float64)[:, None]
    return np.cumsum(E.astype(np.float64) - p0, axis=1)


def _snr_un_bloc(Aw):
    """mu, sigma, SNR sur la grille de w, a partir de A(0,w) par run (n x W)."""
    mu = Aw.mean(axis=0)
    sigma = Aw.std(axis=0, ddof=1)
    with np.errstate(divide="ignore", invalid="ignore"):
        snr = np.where(sigma > 0, mu / sigma, np.nan)
    return mu, sigma, snr


def _w_opt_et_plage(mu, sigma, grille):
    """argmax du SNR restreint a la plage mu > 0, et plage W_95.

    Le signe compte : en haut de grille mu(w) change de signe (l'erreur finit
    SOUS le socle), et maximiser |SNR| sur la partie negative n'aurait pas de
    sens. On publie aussi le point de retournement w_0 = min{w : mu(w) <= 0}.
    """
    positif = mu > 0
    if not positif.any():
        return np.nan, np.nan, np.nan, np.nan, np.nan, np.nan
    snr = np.where(positif & (sigma > 0), mu / np.where(sigma > 0, sigma, 1.0), -np.inf)
    k = int(np.argmax(snr))
    smax = float(snr[k])
    if not np.isfinite(smax):
        return np.nan, np.nan, np.nan, np.nan, np.nan, np.nan
    dedans = snr >= 0.95 * smax
    idx = np.flatnonzero(dedans)
    apres = np.flatnonzero(~positif)
    w0 = float(grille[apres[0]]) if apres.size else np.nan
    # Le retournement qui a un sens est celui qui suit le maximum : en bas de
    # grille mu(w) traverse zero tot par pur bruit et repasse au-dessus.
    apres_max = apres[apres > k]
    w0_max = float(grille[apres_max[0]]) if apres_max.size else np.nan
    return float(grille[k]), smax, float(grille[idx[0]]), float(grille[idx[-1]]), w0, w0_max


def _bootstrap_w_opt(Aw, rng, grille, n_boot=N_BOOT_TQ):
    """IC de w_opt et de W_95 par bootstrap de graines, en produits matriciels.

    mean et var par reechantillon se lisent dans W @ A et W @ A^2 : exact pour
    un bootstrap avec remise, et sans materialiser n_boot x n x W valeurs.
    """
    n = Aw.shape[0]
    W = poids_bootstrap(rng, n_boot, n)
    m = (W @ Aw) / n
    m2 = (W @ (Aw ** 2)) / n
    var = np.clip(m2 - m ** 2, 0.0, None) * (n / max(n - 1, 1))
    sd = np.sqrt(var)
    wopt = np.full(n_boot, np.nan)
    wlo = np.full(n_boot, np.nan)
    whi = np.full(n_boot, np.nan)
    for b in range(n_boot):
        wopt[b], _, wlo[b], whi[b], _, _ = _w_opt_et_plage(m[b], sd[b], grille)
    return wopt, wlo, whi


def run_c2bis(args):
    print("[C.2.bis] fenetre d'accumulation : SNR(w), W_95, regle declaree")
    rng = np.random.default_rng(SEED_BOOTSTRAP + 1)
    E, meta = charger_campagne()
    ind = pd.read_parquet(DATA / "QCD_indicateurs_full.parquet").sort_values("run_id")
    dv = pd.read_parquet(DATA / "QCD_bis_demi_vie.parquet")
    dv = dv[~dv.temoin_sans_drift].set_index("delta_e")

    C = _aires_cumulees(E, meta)
    ecart_AH = float(np.abs(C[:, H - 1] - ind.A_H.to_numpy()).max())
    print(f"  non-regression A(0,2000) contre A_H de QCD_indicateurs_full : "
          f"ecart max {ecart_AH:.3e}")
    if ecart_AH > 1e-9:
        raise ValueError(f"A(0,H) ne reproduit pas A_H : ecart {ecart_AH:.3e}")

    idx_w = GRILLE_W - 1
    lignes_snr, lignes_opt, lignes_run = [], [], []
    for de, grp in meta.groupby("delta_e", sort=True):
        runs = grp.run_id.to_numpy()
        Aw = C[runs][:, idx_w]
        n = len(runs)
        mu, sigma, snr = _snr_un_bloc(Aw)

        # Ecart a la variance binomiale : la formule Sum e(1-e) est fausse ici
        # (Jensen, autocorrelation, effet graine). Publiee pour l'illustration.
        e_bar = E[runs].mean(axis=0)
        var_formule = np.cumsum(e_bar * (1.0 - e_bar))[idx_w]
        with np.errstate(divide="ignore", invalid="ignore"):
            ratio_sigma = np.where(var_formule > 0, sigma / np.sqrt(var_formule), np.nan)

        lignes_snr.append(pd.DataFrame({
            "delta_e": float(de), "w": GRILLE_W, "mu": mu, "sigma": sigma, "snr": snr,
            "sigma_formule_binomiale": np.sqrt(var_formule),
            "ratio_sigma_emp_formule": ratio_sigma,
            "n_runs": n, "seed_bootstrap": SEED_BOOTSTRAP + 1,
        }))

        w_opt, snr_max, w95_lo, w95_hi, w0, w0_max = _w_opt_et_plage(mu, sigma, GRILLE_W)
        wb, wlb, whb = _bootstrap_w_opt(Aw, rng, GRILLE_W)
        lo, hi = ic_percentile(wb)

        interp = bool(dv.loc[de, "interpretable_t_half"]) if de in dv.index else False
        t_half = float(dv.loc[de, "t_half"]) if de in dv.index else np.nan
        w_regle = float(round(W_FIN_OPT * t_half / LN2)) if (interp and np.isfinite(t_half)) \
            else np.nan
        w_cert = float(round(3 * TAU_ARF_FIT[0] / de))
        t90 = float(dv.loc[de, "t_90"]) if de in dv.index else np.nan
        t90_lisible = bool(dv.loc[de, "interpretable_t_90"]) if de in dv.index else False

        lignes_opt.append({
            "delta_e": float(de), "n_runs": n, "seed_bootstrap": SEED_BOOTSTRAP + 1,
            "n_boot": N_BOOT_TQ, "grille_w_min": int(GRILLE_W[0]),
            "grille_w_max": int(GRILLE_W[-1]), "grille_w_pas_fin": 50,
            "w_opt": w_opt, "w_opt_lo": lo, "w_opt_hi": hi,
            "snr_max": snr_max, "w_95_lo": w95_lo, "w_95_hi": w95_hi,
            "w_95_lo_boot_median": float(np.nanmedian(wlb)),
            "w_95_hi_boot_median": float(np.nanmedian(whb)),
            "w_0_retournement": w0,
            "w_0_apres_max": w0_max,
            "w_opt_sur_borne": bool(w_opt in (GRILLE_W[0], GRILLE_W[-1])),
            # Sous l'absence de signal, SNR(w) est un bruit d'ecart-type ~1/sqrt(n) :
            # un maximum en deca de 3/sqrt(n) ne designe pas une fenetre.
            "snr_max_significatif": bool(np.isfinite(snr_max)
                                         and snr_max > 3.0 / np.sqrt(n)),
            "seuil_snr_nul": float(3.0 / np.sqrt(n)),
            "w_opt_sur_maillage": bool(w_opt in (50, 55)),
            "w_regle": w_regle,
            "rapport_wregle_wopt": float(w_regle / w_opt)
                                   if (np.isfinite(w_regle) and w_opt) else np.nan,
            "rapport_wcert_wopt": float(w_cert / w_opt) if w_opt else np.nan,
            "w_regle_dans_W95": bool(np.isfinite(w_regle) and w95_lo <= w_regle <= w95_hi),
            "w_certificat": w_cert,
            "w_certificat_dans_W95": bool(w95_lo <= w_cert <= w95_hi),
            "t_half": t_half, "t_90": t90, "t_90_lisible": t90_lisible,
            "interpretable_t_half": interp,
            "ratio_sigma_emp_formule_w50": float(ratio_sigma[GRILLE_W == 50][0]),
            "ratio_sigma_emp_formule_w2000": float(ratio_sigma[GRILLE_W == 2000][0]),
            "snr_w50": float(snr[GRILLE_W == 50][0]),
            "snr_w2000": float(snr[GRILLE_W == 2000][0]),
        })

        wr = int(w_regle) if np.isfinite(w_regle) else None
        lignes_run.append(pd.DataFrame({
            "run_id": runs, "delta_e": float(de),
            "seed": grp.seed.to_numpy(),
            "A_0_wregle": C[runs, wr - 1] if wr else np.nan,
            "w_regle": w_regle,
            "A_0_wcert": C[runs, int(w_cert) - 1],
            "w_certificat": w_cert,
            "A_H": C[runs, H - 1],
        }))

    snrt = pd.concat(lignes_snr, ignore_index=True)
    snrt.to_parquet(DATA / "QCD_bis_snr_fenetre.parquet", index=False)
    opt = pd.DataFrame(lignes_opt)
    opt["rapport_wregle_wopt_median"] = float(opt.rapport_wregle_wopt.median())
    opt["rapport_wcert_wopt_min"] = float(opt.rapport_wcert_wopt.min())
    haut = opt[opt.delta_e >= 0.40]
    opt["rapport_wcert_wopt_min_haut_grille"] = float(haut.rapport_wcert_wopt.min())
    opt["rapport_wcert_wopt_max_haut_grille"] = float(haut.rapport_wcert_wopt.max())
    opt.to_parquet(DATA / "QCD_bis_w_opt.parquet", index=False)
    par_run = pd.concat(lignes_run, ignore_index=True)
    par_run.to_parquet(DATA / "QCD_bis_A0w_par_run.parquet", index=False)

    _figure_c2bis(snrt, opt)
    aff = opt[["delta_e", "w_opt", "w_95_lo", "w_95_hi", "w_0_apres_max", "w_regle",
               "w_regle_dans_W95", "w_certificat", "ratio_sigma_emp_formule_w50",
               "ratio_sigma_emp_formule_w2000"]].copy()
    print(aff.to_string(index=False, formatters={"delta_e": lambda v: f"{v:7.4f}"},
                        float_format=lambda v: f"{v:9.2f}"))
    print(f"[OK] QCD_bis_snr_fenetre.parquet ({len(snrt)}), "
          f"QCD_bis_w_opt.parquet ({len(opt)}), "
          f"QCD_bis_A0w_par_run.parquet ({len(par_run)})")
    return opt


def _figure_c2bis(snrt, opt):
    reps = amplitudes_proches(opt.delta_e.unique())
    o = opt.set_index("delta_e")
    fig, ax = plt.subplots(figsize=(8.4, 5.2))
    for k, de in enumerate(reps):
        s = snrt[snrt.delta_e == de]
        ax.plot(s.w, s.snr, linestyle=STYLES[k], color=str(GRIS[k]), linewidth=1.2,
                label=f"$\\Delta e$ = {de:.3f}")
        for col, mark, lab in (("w_opt", "o", None), ("w_certificat", "x", None)):
            v = float(o.loc[de, col])
            if np.isfinite(v):
                y = float(np.interp(v, s.w, s.snr))
                ax.plot([v], [y], mark, color=str(GRIS[k]), markersize=7,
                        markerfacecolor="white", markeredgewidth=1.2)
        v = float(o.loc[de, "t_90"])
        if np.isfinite(v) and bool(o.loc[de, "t_90_lisible"]):
            ax.plot([v], [float(np.interp(v, s.w, s.snr))], "^", color=str(GRIS[k]),
                    markersize=7, markerfacecolor="white", markeredgewidth=1.2)
        lo, hi = float(o.loc[de, "w_95_lo"]), float(o.loc[de, "w_95_hi"])
        if np.isfinite(lo):
            ax.axvspan(lo, hi, color=str(GRIS[k]), alpha=0.06, linewidth=0)
    ax.axhline(0.0, color="0.2", linewidth=0.9, linestyle=(0, (4, 4)))
    ax.set_xscale("log")
    style_axes(ax, "accumulation window $w$ (steps, log)", "$SNR(w) = \\mu(w)/\\sigma(w)$")
    ax.set_title("Signal-to-noise of the pure area $A(0,w)$\n"
                 "circle = $w_{opt}$, cross = prescribed certificate window "
                 "$3\\cdot18.5/\\Delta e$, triangle = $t_{90}$ where readable;\n"
                 "shaded band = $W_{95}$. Below the dashed line $\\mu(w) \\leq 0$: "
                 "the error has fallen under $\\hat{p}_0$.", fontsize=9)
    ax.legend(fontsize=8, loc="lower left")
    fig.savefig(FIGURES / "Fig_bis_snr_fenetre.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


# ====================================================== D.3.bis (priorite 3) ===
# Douze metriques. Exclusions motivees dans le .tex :
#   tau_swap_10 : identite avec tau_ARF a M = 10 (JOURNAL section 10.2) ;
#   tau_det_25  : 61,1 % de censure globale, profil en U ;
#   tau_det_50  : 99,95 % de censure.
DUREES = ("tau_arf", "tau_swap_25", "tau_swap_50", "tau_swap_75", "tau_det_8")
AIRES = ("A_H", "A_0_wregle", "A_0_wcert", "S_max_H", "etalon_aire", "V_aire", "N_2000")
METRIQUES = DUREES + AIRES

# Cellules a marquer, pas a lire. JOURNAL section 8.
# S_max(H) = max_{k<=j} [A(k,j) - (j-k) delta_P] est un sup sur une famille qui
# CONTIENT A(0,w) - w delta_P pour tout w. Le lien vaut donc pour A(H) comme pour
# chaque A(0,w), et plus serre encore pour les fenetres courtes : l'argmax de
# Lindley tombe dans leur voisinage en haut de grille. Marquer A_H seul, comme le
# faisait la premiere version, revenait a hachurer le terme de comparaison et a
# laisser lire les deux autres.
LIENS_ALGEBRIQUES = {
    frozenset(("S_max_H", "A_H")): "Lindley : S_max est un sup de sommes partielles de A",
    frozenset(("S_max_H", "A_0_wregle")): "Lindley : A(0,w) - w delta_P est dans la famille dont S_max est le sup",
    frozenset(("S_max_H", "A_0_wcert")): "Lindley : A(0,w) - w delta_P est dans la famille dont S_max est le sup",
    frozenset(("A_0_wregle", "etalon_aire")): "meme identite approchee que (A_H, etalon)",
    frozenset(("A_0_wcert", "etalon_aire")): "meme identite approchee que (A_H, etalon)",
    frozenset(("A_H", "etalon_aire")): "identite approchee e_t - p0 ~ delta_e (1 - acc_bande)",
    frozenset(("S_max_H", "etalon_aire")): "meme identite approchee, via A",
    frozenset(("V_aire", "etalon_aire")): "memes votes, memes sondes, meme fenetre",
    frozenset(("A_0_wregle", "A_H")): "emboitement de sommes : A(0,w) est un prefixe de A(H)",
    frozenset(("A_0_wcert", "A_H")): "emboitement de sommes",
    frozenset(("A_0_wregle", "A_0_wcert")): "emboitement de sommes",
}
# tau_swap(10 %) est EXCLU de METRIQUES parce qu'il est identique a tau_ARF a
# M = 10 : la seule tautologie connue n'a donc pas de cellule dans cette matrice,
# et la colonne `tautologique` y est vide par construction. Elle est conservee
# pour que l'exclusion reste lisible dans la table, pas parce qu'elle marque
# quelque chose.
TAUTOLOGIES = {
    frozenset(("tau_arf", "tau_swap_10")): "tau_ARF = tau_swap(1/M), identiques a M = 10",
}


def _table_metriques():
    """Une ligne par run, les 12 metriques plus la censure de chaque duree."""
    ind = pd.read_parquet(DATA / "QCD_indicateurs_full.parquet")
    cand = pd.read_parquet(DATA / "QCD_candidats_indicateurs_etalon.parquet")
    eta = pd.read_parquet(DATA / "QCD_etalon_par_run.parquet")
    a0w = pd.read_parquet(DATA / "QCD_bis_A0w_par_run.parquet")
    df = (ind
          .merge(cand[["run_id", "V_aire", "N_2000"]], on="run_id", validate="1:1")
          .merge(eta[["run_id", "etalon_aire"]], on="run_id", validate="1:1")
          .merge(a0w[["run_id", "A_0_wregle", "A_0_wcert", "w_regle"]], on="run_id",
                 validate="1:1"))
    if len(df) != 2000:
        raise ValueError(f"jointure incomplete : {len(df)} lignes")
    return df


def _paire(df, a, b, rng, n_boot, grappes=None):
    """tau-b d'une paire, IC bootstrap, effectif et censure effectivement utilises.

    Une duree censuree (NaN) est imputee a l'horizon : legitime, l'horizon est le
    meme pour tous les runs. Une AIRE a NaN n'est pas censuree, elle n'existe pas
    (w_regle indefini) : la ligne sort, et l'effectif le dit.
    """
    x = df[a].to_numpy(dtype=float)
    y = df[b].to_numpy(dtype=float)
    garde = np.ones(len(df), dtype=bool)
    if a in AIRES:
        garde &= np.isfinite(x)
    if b in AIRES:
        garde &= np.isfinite(y)
    x, y = x[garde], y[garde]
    n = int(garde.sum())
    cens_a = float(np.mean(~np.isfinite(x))) if (a in DUREES and n) else 0.0
    cens_b = float(np.mean(~np.isfinite(y))) if (b in DUREES and n) else 0.0
    if n < 3:
        return dict(tau_b=np.nan, ci_lo=np.nan, ci_hi=np.nan, n=n,
                    censure_a=cens_a, censure_b=cens_b)
    tb, _ = kendall_censored(x, y, H)
    if grappes is None:
        vals = np.empty(n_boot)
        for i in range(n_boot):
            idx = rng.integers(0, n, n)
            vals[i], _ = kendall_censored(x[idx], y[idx], H)
    else:
        # Bootstrap PAR GRAPPES DE GRAINES : les 100 graines sont communes aux 20
        # amplitudes ; reechantillonner les runs un a un donnerait des IC trop
        # etroits sur la matrice empilee.
        gr = grappes[garde]
        listes = [np.flatnonzero(gr == g) for g in np.unique(gr)]
        ng = len(listes)
        vals = np.empty(n_boot)
        for i in range(n_boot):
            pris = rng.integers(0, ng, ng)
            idx = np.concatenate([listes[j] for j in pris])
            vals[i], _ = kendall_censored(x[idx], y[idx], H)
    lo, hi = ic_percentile(vals)
    return dict(tau_b=float(tb), ci_lo=lo, ci_hi=hi, n=n,
                censure_a=cens_a, censure_b=cens_b)


def run_d3bis(args):
    print("[D.3.bis] matrice de correlation, empilee puis stratifiee")
    rng = np.random.default_rng(SEED_BOOTSTRAP + 2)
    df = _table_metriques()
    paires = [(a, b) for i, a in enumerate(METRIQUES) for b in METRIQUES[i + 1:]]
    print(f"  {len(METRIQUES)} metriques, {len(paires)} paires, "
          f"{N_BOOT_CORR} reechantillons par cellule")

    lignes = []
    graines = df.seed.to_numpy()
    for a, b in paires:
        cle = frozenset((a, b))
        r = _paire(df, a, b, rng, N_BOOT_CORR, grappes=graines)
        r.update(metrique_a=a, metrique_b=b, delta_e=np.nan, empile=True,
                 tautologique=cle in TAUTOLOGIES,
                 lien_algebrique=LIENS_ALGEBRIQUES.get(cle, ""),
                 non_lisible=max(r["censure_a"], r["censure_b"]) > 0.50,
                 bootstrap="grappes de graines")
        lignes.append(r)

    for de, grp in df.groupby("delta_e", sort=True):
        for a, b in paires:
            cle = frozenset((a, b))
            r = _paire(grp, a, b, rng, N_BOOT_CORR)
            r.update(metrique_a=a, metrique_b=b, delta_e=float(de), empile=False,
                     tautologique=cle in TAUTOLOGIES,
                     lien_algebrique=LIENS_ALGEBRIQUES.get(cle, ""),
                     non_lisible=max(r["censure_a"], r["censure_b"]) > 0.50,
                     bootstrap="graines de la strate")
            lignes.append(r)

    mat = pd.DataFrame(lignes)
    mat["seed_bootstrap"] = SEED_BOOTSTRAP + 2
    mat["n_boot"] = N_BOOT_CORR
    mat.to_parquet(DATA / "QCD_bis_matrice_correlation.parquet", index=False)

    _controle_non_regression(mat)
    ratios = _amplification_simpson(mat)
    _controles_complementaires(mat, df, rng)
    _figures_d3bis(mat, ratios, df)
    print(f"[OK] QCD_bis_matrice_correlation.parquet ({len(mat)} lignes)")
    return mat


def _mediane_stratifiee(mat, domaine=True):
    """Mediane des tau-b par paire sur les strates du domaine de decision.

    Definition d'origine de D conservee : les 18 amplitudes de delta_e >= 0,10,
    sans la regle de lisibilite par cellule, qui ne s'applique qu'aux cellules
    neuves. L'ecart des deux conventions est publie dans le .tex.
    """
    s = mat[~mat.empile]
    if domaine:
        s = s[s.delta_e >= DELTA_E_MIN_DECISION]
    return s.groupby(["metrique_a", "metrique_b"])["tau_b"].median()


def _controle_non_regression(mat):
    emp = mat[mat.empile].set_index(["metrique_a", "metrique_b"])["tau_b"]
    med = _mediane_stratifiee(mat)
    cle = ("tau_arf", "A_H")
    got_e, got_m = float(emp.loc[cle]), float(med.loc[cle])
    att_e, att_m = 0.396512, 0.052559
    print(f"  non-regression tab:agregation : empile {got_e:.6f} (attendu {att_e:.6f}), "
          f"mediane stratifiee {got_m:.6f} (attendu {att_m:.6f}), "
          f"ratio {abs(got_e / got_m):.2f} (attendu 7,54)")
    if abs(got_e - att_e) > 5e-7 or abs(got_m - att_m) > 5e-7:
        raise ValueError("la matrice ne reproduit pas tab:agregation de redaction_QD3")


def _amplification_simpson(mat):
    """Resume par paire : empile, mediane stratifiee, comptage de strates lisibles.

    Ce resume est ECRIT en table : toute valeur citee dans le .tex doit se relire
    dans un Parquet, et une mediane calculee a la volee ne serait pas tracable.
    """
    emp = mat[mat.empile].set_index(["metrique_a", "metrique_b"])
    med = _mediane_stratifiee(mat)
    # Comptage a la regle de l'IC, sur les strates LISIBLES du domaine de decision,
    # meme convention que la redaction D.
    lis = mat[(~mat.empile) & (mat.delta_e >= DELTA_E_MIN_DECISION) & (~mat.non_lisible)]
    g = lis.groupby(["metrique_a", "metrique_b"])
    r = pd.DataFrame({
        "tau_b_empile": emp["tau_b"],
        "ci_lo_empile": emp["ci_lo"],
        "ci_hi_empile": emp["ci_hi"],
        "n_empile": emp["n"],
        "mediane_stratifiee": med,
        "mediane_stratifiee_lisibles": g["tau_b"].median(),
        "n_strates_lisibles": g.size(),
        "n_strates_discernables": g.apply(
            lambda d: int(((d.ci_lo > 0) | (d.ci_hi < 0)).sum()), include_groups=False),
        "tautologique": emp["tautologique"],
        "lien_algebrique": emp["lien_algebrique"],
        "non_lisible": emp["non_lisible"],
    })
    with np.errstate(divide="ignore", invalid="ignore"):
        r["ratio_simpson"] = np.where(np.abs(r.mediane_stratifiee) > 1e-12,
                                      np.abs(r.tau_b_empile) / np.abs(r.mediane_stratifiee),
                                      np.nan)
    with np.errstate(divide="ignore", invalid="ignore"):
        r["ratio_simpson_lisibles"] = np.where(
            np.abs(r.mediane_stratifiee_lisibles) > 1e-12,
            np.abs(r.tau_b_empile) / np.abs(r.mediane_stratifiee_lisibles), np.nan)
    r["signe_inverse"] = np.sign(r.tau_b_empile) != np.sign(r.mediane_stratifiee)
    r["lien_connu"] = r.tautologique | (r.lien_algebrique != "")
    r = r.reset_index()
    libres = r[~r.lien_connu]
    r["ratio_simpson_median_paires_libres"] = float(libres.ratio_simpson.median())
    r["ratio_simpson_lisibles_median_paires_libres"] = float(
        libres.ratio_simpson_lisibles.median())
    r["n_paires_libres_moitie_strates_discernables"] = int(
        (libres.n_strates_discernables >= libres.n_strates_lisibles / 2).sum())
    r["n_paires_libres"] = int(len(libres))
    r["n_paires_libres_signe_inverse"] = int(libres.signe_inverse.sum())
    r["seed_bootstrap"] = SEED_BOOTSTRAP + 2
    r["n_boot"] = N_BOOT_CORR
    r.to_parquet(DATA / "QCD_bis_matrice_resume.parquet", index=False)
    print(f"  resume : {len(libres)} paires sans lien connu, ratio de Simpson median "
          f"{libres.ratio_simpson.median():.4f}, "
          f"{int(libres.signe_inverse.sum())} paires a signe inverse")
    return r


def _controles_complementaires(mat, df, rng):
    """Deux controles que la matrice seule ne porte pas.

    1. Impute contre cas complets sur (tau_ARF, tau_swap(75 %)), la paire la plus
       censuree parmi celles retenues : si les deux coincident, l'imputation a
       l'horizon ne pilote pas le resultat.
    2. Les deux conventions de mediane stratifiee. La definition d'origine de D
       garde les 18 strates du domaine ; la regle de lisibilite par cellule, qui
       ne s'applique qu'aux cellules neuves, en retirerait celles dont une marge
       depasse 50 % de censure. Les deux chiffres se publient cote a cote.
    """
    a, b = "tau_arf", "tau_swap_75"
    lignes = []
    for de, grp in df.groupby("delta_e", sort=True):
        x = grp[a].to_numpy(float)
        y = grp[b].to_numpy(float)
        t_imp, _ = kendall_censored(x, y, H)
        plein = np.isfinite(x) & np.isfinite(y)
        t_cc = kendall_censored(x[plein], y[plein], H)[0] if plein.sum() >= 3 else np.nan
        lignes.append({
            "delta_e": float(de), "paire": f"{a} / {b}",
            "tau_b_impute": float(t_imp), "tau_b_cas_complets": float(t_cc),
            "ecart_impute_cas_complets": float(abs(t_imp - t_cc))
                                          if np.isfinite(t_cc) else np.nan,
            "censure_b": float(np.mean(~np.isfinite(y))),
            "n_cas_complets": int(plein.sum()),
            "dans_domaine_decision": bool(de >= DELTA_E_MIN_DECISION),
            "lisible_regle_50pct": bool(np.mean(~np.isfinite(y)) <= 0.50),
        })
    c = pd.DataFrame(lignes)
    dom = c[c.dans_domaine_decision]
    med_origine = float(dom.tau_b_impute.median())
    med_regle = float(dom[dom.lisible_regle_50pct].tau_b_impute.median())
    emp = float(mat[mat.empile & (mat.metrique_a == a) & (mat.metrique_b == b)].tau_b.iloc[0])
    c.attrs = {}
    resume = pd.DataFrame([{
        "paire": f"{a} / {b}",
        "tau_b_empile": emp,
        "mediane_convention_origine": med_origine,
        "mediane_convention_regle_50pct": med_regle,
        "ratio_simpson_origine": abs(emp / med_origine) if med_origine else np.nan,
        "ratio_simpson_regle": abs(emp / med_regle) if med_regle else np.nan,
        "n_strates_origine": int(len(dom)),
        "n_strates_regle": int(dom.lisible_regle_50pct.sum()),
        "ecart_max_impute_cas_complets": float(dom.ecart_impute_cas_complets.max()),
        "censure_max_domaine": float(dom.censure_b.max()),
    }])
    c["seed_bootstrap"] = SEED_BOOTSTRAP + 2
    c.to_parquet(DATA / "QCD_bis_controle_censure.parquet", index=False)
    resume["seed_bootstrap"] = SEED_BOOTSTRAP + 2
    resume.to_parquet(DATA / "QCD_bis_controle_conventions.parquet", index=False)
    r = resume.iloc[0]
    print(f"  impute contre cas complets, {a}/{b} : ecart max sur le domaine "
          f"{r.ecart_max_impute_cas_complets:.6f} (censure max {r.censure_max_domaine:.3f})")
    print(f"  mediane stratifiee, convention d'origine {r.mediane_convention_origine:.6f} "
          f"({r.n_strates_origine} strates) contre regle 50 % "
          f"{r.mediane_convention_regle_50pct:.6f} ({r.n_strates_regle} strates) ; "
          f"ratio {r.ratio_simpson_origine:.2f} contre {r.ratio_simpson_regle:.2f}")


ETIQUETTES = {
    "tau_arf": "$\\tau_{ARF}$", "tau_swap_25": "$\\tau_{swap}(25\\%)$",
    "tau_swap_50": "$\\tau_{swap}(50\\%)$", "tau_swap_75": "$\\tau_{swap}(75\\%)$",
    "tau_det_8": "$\\tau_{det}(\\lambda=8)$", "A_H": "$A(H)$",
    "A_0_wregle": "$A(0,w_{rule})$", "A_0_wcert": "$A(0,w_{cert})$",
    "S_max_H": "$S_{max}(H)$", "etalon_aire": "reference area",
    "V_aire": "$\\int V(t)$", "N_2000": "$N_{2000}$",
}


def _heatmap(valeurs, marques, titre, fichier, vmin, vmax, fmt="{:+.2f}", cbar_label=""):
    n = len(METRIQUES)
    M = np.full((n, n), np.nan)
    for (a, b), v in valeurs.items():
        i, j = METRIQUES.index(a), METRIQUES.index(b)
        M[max(i, j), min(i, j)] = v            # triangle inferieur seulement
    fig, ax = plt.subplots(figsize=(9.4, 8.0))
    im = ax.imshow(M, cmap="Greys", vmin=vmin, vmax=vmax)
    for (a, b), v in valeurs.items():
        i, j = max(METRIQUES.index(a), METRIQUES.index(b)), \
               min(METRIQUES.index(a), METRIQUES.index(b))
        if not np.isfinite(v):
            continue
        rel = (v - vmin) / (vmax - vmin) if vmax > vmin else 0.5
        ax.text(j, i, fmt.format(v), ha="center", va="center", fontsize=7,
                color="white" if rel > 0.55 else "black")
        if marques.get((a, b)):
            ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False,
                                       hatch="////", edgecolor="0.15", linewidth=0.7))
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels([ETIQUETTES[m] for m in METRIQUES], rotation=45, ha="right",
                       fontsize=8)
    ax.set_yticklabels([ETIQUETTES[m] for m in METRIQUES], fontsize=8)
    ax.set_title(titre, fontsize=10)
    fig.colorbar(im, ax=ax, shrink=0.72, label=cbar_label)
    fig.savefig(FIGURES / fichier, dpi=150, bbox_inches="tight")
    plt.close(fig)


def _figures_d3bis(mat, ratios, df):
    # `non_lisible` de la ligne empilee est toujours faux : les censures globales
    # restent sous 50 %. Le hachurage doit porter sur les strates, ou la censure
    # mord reellement (bas de grille).
    nl = (mat[(~mat.empile) & (mat.delta_e >= DELTA_E_MIN_DECISION)]
          .groupby(["metrique_a", "metrique_b"]).non_lisible.any())
    marques = {(r.metrique_a, r.metrique_b):
               bool(r.tautologique) or bool(r.lien_algebrique)
               or bool(nl.get((r.metrique_a, r.metrique_b), False))
               for r in ratios.itertuples()}

    emp = {(r.metrique_a, r.metrique_b): r.tau_b_empile for r in ratios.itertuples()}
    _heatmap(emp, marques,
             "Kendall $\\tau_b$, all 20 amplitudes stacked ($n$ = 2000)\n"
             "hatched: algebraically linked, or above 50% censoring in at least "
             "one stratum: marked, not read",
             "Fig_bis_matrice_empilee.png", -1.0, 1.0, cbar_label="$\\tau_b$ (stacked)")

    med = {(r.metrique_a, r.metrique_b): r.mediane_stratifiee for r in ratios.itertuples()}
    _heatmap(med, marques,
             "Kendall $\\tau_b$, median over the 18 decision-domain strata "
             "($\\Delta e \\geq 0.10$, $n$ = 100 each)\n"
             "hatched: algebraically linked, or above 50% censoring in at least one "
             "stratum. Compare cell by cell with the stacked matrix.",
             "Fig_bis_matrice_stratifiee_mediane.png", -1.0, 1.0,
             cbar_label="median $\\tau_b$ (stratified)")

    rat = {(r.metrique_a, r.metrique_b): r.ratio_simpson for r in ratios.itertuples()}
    fini = np.array([v for v in rat.values() if np.isfinite(v)])
    haut = float(np.percentile(fini, 95)) if fini.size else 10.0
    _heatmap(rat, marques,
             "Simpson amplification $|\\tau_b^{stacked}| / |\\mathrm{median}\\,"
             "\\tau_b^{strata}|$\n"
             "1 = stacking changes nothing; large = the stacked coefficient is "
             "manufactured by the amplitude grid.",
             "Fig_bis_matrice_ratio_simpson.png", 0.0, haut, fmt="{:.1f}",
             cbar_label="ratio (clipped at the 95th percentile)")

    # --- le paradoxe, montre sur une paire --------------------------------------
    fig, ax = plt.subplots(figsize=(7.8, 5.4))
    des = sorted(df.delta_e.unique())
    bornes = np.array_split(np.array(des), 5)
    # Les tendances sont ajustees en log10(tau_ARF), l'echelle sur laquelle elles
    # sont tracees, et chacune est bornee a l'etendue de son propre groupe : une
    # droite prolongee hors de son nuage donnerait a voir une relation qui n'a pas
    # ete mesuree la.
    for k, bloc in enumerate(bornes):
        sub = df[df.delta_e.isin(bloc)]
        lx = np.log10(np.clip(sub.tau_arf.to_numpy(dtype=float), 0.5, None))
        ax.scatter(sub.tau_arf, sub.A_H, s=9, color=str(GRIS[k]), alpha=0.55,
                   edgecolors="none",
                   label=f"$\\Delta e \\in$ [{bloc[0]:.3f}, {bloc[-1]:.3f}]")
        z = np.polyfit(lx, sub.A_H.to_numpy(dtype=float), 1)
        xs = np.linspace(lx.min(), lx.max(), 20)
        ax.plot(10 ** xs, np.polyval(z, xs), linestyle=STYLES[k], color=str(GRIS[k]),
                linewidth=1.6)
    lx = np.log10(np.clip(df.tau_arf.to_numpy(dtype=float), 0.5, None))
    z = np.polyfit(lx, df.A_H.to_numpy(dtype=float), 1)
    xs = np.linspace(lx.min(), lx.max(), 40)
    ax.plot(10 ** xs, np.polyval(z, xs), "-", color="0.0", linewidth=2.4,
            label="stacked trend (all amplitudes)")
    ax.set_xscale("log")
    style_axes(ax, "$\\tau_{ARF}$ (steps, log)", "$A(H)$ (excess error area)")
    emp_v = float(ratios.set_index(["metrique_a", "metrique_b"])
                  .loc[("tau_arf", "A_H"), "tau_b_empile"])
    med_v = float(ratios.set_index(["metrique_a", "metrique_b"])
                  .loc[("tau_arf", "A_H"), "mediane_stratifiee"])
    ax.set_title(f"Simpson on one pair: stacked $\\tau_b$ = {emp_v:+.4f}, "
                 f"median within strata = {med_v:+.4f}\n"
                 "the stacked slope follows the amplitude grid, not the within-strata "
                 "relation", fontsize=9.5)
    ax.legend(fontsize=7.5, loc="upper left")
    fig.savefig(FIGURES / "Fig_bis_simpson_paire.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


# ===================================================== D.1.bis (priorite 4) ====
# CONSTAT, a ecrire avant toute mesure : aucune table ne porte l'erreur par arbre
# par pas. `exp_QCD_campagne.py::run_one` n'enregistre que l'erreur de la foret et
# les remplacements ; `exp_QCD_etalon.py::sonder` interroge chaque arbre puis somme
# immediatement sur les 10 arbres et les 200 sondes. La variance transversale
# demandee n'est donc PAS calculable hors ligne. Ce qui suit est un proxy, et il
# partage ses votes, ses sondes et sa fenetre avec `acc_bande` (JOURNAL section 8) :
# ce n'est pas une mesure externe.
PAS_SONDE = 25
M_ARBRES = 10


def _fraction_arbres_remplaces(events, run_ids, instants, m=M_ARBRES):
    """|{tree_id remplaces au moins une fois avant t}| / M, par run et par instant."""
    pos = {r: i for i, r in enumerate(run_ids)}
    vus = np.zeros((len(run_ids), m), dtype=bool)
    frac = np.zeros((len(run_ids), len(instants)))
    ev = events[events.run_id.isin(pos)].sort_values("t")
    r_arr = ev.run_id.to_numpy()
    t_arr = ev.t.to_numpy()
    k_arr = ev.tree_id.to_numpy()
    j = 0
    for c, t in enumerate(instants):
        while j < len(ev) and t_arr[j] <= t:
            vus[pos[r_arr[j]], k_arr[j]] = True
            j += 1
        frac[:, c] = vus.sum(axis=1) / m
    return frac


def _proxy_dispersion(votes, meta, events, rng, etiquette):
    """V(t) par amplitude, region et instant, avec IC bootstrap sur les graines."""
    instants = np.sort(votes.t.unique())
    lignes = []
    for de, grp in meta.groupby("delta_e", sort=True):
        runs = np.sort(grp.run_id.to_numpy())
        frac = _fraction_arbres_remplaces(events, runs, instants)
        v = votes[votes.run_id.isin(runs)]
        for region, vr in v.groupby("region", sort=True):
            piv = vr.pivot(index="run_id", columns="t", values="somme_desaccord")
            den = vr.pivot(index="run_id", columns="t", values="somme_votants")
            piv = piv.reindex(index=runs, columns=instants)
            den = den.reindex(index=runs, columns=instants)
            V = (piv.to_numpy() / den.to_numpy())
            n = V.shape[0]
            W = poids_bootstrap(rng, N_BOOT_CORR, n)
            Vb = (W @ np.nan_to_num(V)) / n
            lo = np.percentile(Vb, 2.5, axis=0)
            hi = np.percentile(Vb, 97.5, axis=0)
            lignes.append(pd.DataFrame({
                "delta_e": float(de), "t": instants, "region": region,
                "V_mean": V.mean(axis=0), "V_lo": lo, "V_hi": hi,
                "frac_swap_mean": frac.mean(axis=0),
                "n_runs": n, "campagne": etiquette,
                "pas_sonde": PAS_SONDE, "n_models": M_ARBRES,
                "seed_bootstrap": SEED_BOOTSTRAP + 3, "n_boot": N_BOOT_CORR,
            }))
    return pd.concat(lignes, ignore_index=True)


def run_d1bis(args):
    print("[D.1.bis] dispersion entre arbres : constat, argument, proxy V(t)")
    rng = np.random.default_rng(SEED_BOOTSTRAP + 3)
    votes = pd.read_parquet(DATA / "QCD_etalon_votes_full_M10.parquet")
    meta = pd.read_parquet(DATA / "QCD_etalon_meta_full_M10.parquet")
    events = pd.read_parquet(DATA / "QCD_events_swap_full.parquet")
    d = _proxy_dispersion(votes, meta, events, rng, "full")

    votes_t = pd.read_parquet(DATA / "QCD_etalon_votes_pilote_nodrift_M10.parquet")
    meta_t = pd.read_parquet(DATA / "QCD_etalon_meta_pilote_nodrift_M10.parquet")
    events_t = pd.read_parquet(DATA / "QCD_etalon_events_swap_pilote_nodrift_M10.parquet")
    dt = _proxy_dispersion(votes_t, meta_t, events_t, rng, "pilote_nodrift")
    dt["delta_e"] = 0.0

    out = pd.concat([d, dt], ignore_index=True)
    out.to_parquet(DATA / "QCD_bis_dispersion_arbres.parquet", index=False)
    _figure_d1bis(out)

    # Ce que la table dit du reaccord : V(t) en bande retombe-t-il AVANT que la
    # foret soit entierement renouvelee ? A lire, pas a anticiper.
    b = out[(out.campagne == "full") & (out.region == "bande")]
    res = []
    for de, g in b.groupby("delta_e"):
        g = g.sort_values("t")
        k = int(g.V_mean.to_numpy().argmax())
        t_pic = int(g.t.to_numpy()[k])
        vmax = float(g.V_mean.to_numpy()[k])
        v0 = float(g.V_mean.to_numpy()[0])
        apres = g.iloc[k:]
        seuil = v0 + 0.5 * (vmax - v0)
        sous = apres[apres.V_mean <= seuil]
        t_mi = int(sous.t.iloc[0]) if len(sous) else -1
        frac_alors = float(sous.frac_swap_mean.iloc[0]) if len(sous) else np.nan
        res.append((de, t_pic, vmax, t_mi, frac_alors))
    r = pd.DataFrame(res, columns=["delta_e", "t_pic_V", "V_pic", "t_mi_retombee",
                                   "frac_arbres_remplaces_alors"])
    print(r.to_string(index=False, float_format=lambda v: f"{v:8.3f}"))
    print(f"[OK] QCD_bis_dispersion_arbres.parquet ({len(out)} lignes)")
    return out


def _figure_d1bis(out):
    full = out[out.campagne == "full"]
    reps = amplitudes_proches(full.delta_e.unique())
    fig, axes = plt.subplots(1, 2, figsize=(11.6, 4.4), sharey=True)
    for ax, region, titre in ((axes[0], "bande", "in the drifting band"),
                              (axes[1], "haut", "outside the band (upper region)")):
        for k, de in enumerate(reps):
            g = full[(full.delta_e == de) & (full.region == region)].sort_values("t")
            ax.plot(g.t, g.V_mean, linestyle=STYLES[k], color=str(GRIS[k]), linewidth=1.2,
                    label=f"$\\Delta e$ = {de:.3f}")
            ax.fill_between(g.t, g.V_lo, g.V_hi, color=str(GRIS[k]), alpha=0.10,
                            linewidth=0)
        t0 = out[(out.campagne == "pilote_nodrift") & (out.region == region)].sort_values("t")
        ax.plot(t0.t, t0.V_mean, linestyle=(0, (1, 2)), color="0.55", linewidth=1.0,
                label="no-drift control, $n$ = 100")
        ax.set_xlim(0, 500)
        style_axes(ax, "steps since the change", "$V(t)$ = disagreement / votes cast")
        ax.set_title(titre, fontsize=9.5)
    g = full[(full.delta_e == reps[-1]) & (full.region == "bande")].sort_values("t")
    ax2 = axes[0].twinx()
    ax2.plot(g.t, g.frac_swap_mean, linestyle=(0, (3, 1, 1, 1)), color="0.0", linewidth=1.0)
    ax2.set_ylabel(f"replaced / $M$, $\\Delta e$ = {reps[-1]:.3f}", fontsize=7.5,
                   labelpad=2)
    ax2.tick_params(axis="y", labelsize=7)
    ax2.set_ylim(0, 1.05)
    axes[0].legend(fontsize=7.5, loc="lower right")
    fig.suptitle("Proxy for tree dispersion: instantaneous disagreement $V(t)$, probed "
                 f"every {PAS_SONDE} steps.\nNot an external measure: same votes, "
                 "same probes, same window as the reference area.", fontsize=9, y=1.10)
    fig.subplots_adjust(wspace=0.38)
    fig.savefig(FIGURES / "Fig_bis_dispersion_arbres.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


# ===================================================== C.1.bis (priorite 5) ====
# Resultat NEGATIF, etabli en une table. Le denominateur du Z-score decroit en
# 1/sqrt(n) : l'instant ou il franchit un seuil mesure le nombre de graines, pas
# la dynamique. La version invariante en n du meme objet est t_25 / t_half / t_90
# de C.3.bis, deja publies.
SEUILS_Z = (2.0, 3.0, 4.0)
TAILLES_N = (25, 50, 100)


def _t_zscore(Emat, seuil):
    """Premier t ou Z_t franchit `seuil`, avec la persistance habituelle."""
    n = Emat.shape[0]
    e_bar = Emat.mean(axis=0)
    t0, t1 = FEN_ESTART
    e_start = float(e_bar[t0:t1].mean())
    se_start = float(np.sqrt(max(e_start * (1 - e_start), 0.0) / (n * (t1 - t0))))
    se_t = se_binomiale(e_bar, n)
    den = np.sqrt(se_start ** 2 + se_t ** 2)
    with np.errstate(divide="ignore", invalid="ignore"):
        Z = np.where(den > 0, (e_start - e_bar) / den, np.nan)
    # Meme regle que les temps de fraction : franchissement EN MOYENNE sur la
    # fenetre de persistance. Z croit, donc on lit -Z contre -seuil.
    tz = franchissement_en_moyenne((-Z)[None, :], np.array([-seuil]), PERSIST)
    return float(tz[0]), e_start


def run_c1bis(args):
    print("[C.1.bis] Z-score de la baisse d'erreur : ce qu'il mesure vraiment")
    rng = np.random.default_rng(SEED_BOOTSTRAP + 4)
    E, meta = charger_campagne()
    lignes = []
    for de, grp in meta.groupby("delta_e", sort=True):
        runs = grp.sort_values("seed").run_id.to_numpy()
        for n in TAILLES_N:
            sous = runs[:n]                       # n premieres graines, ordre declare
            Emat = E[sous]
            for seuil in SEUILS_Z:
                tz, e_start = _t_zscore(Emat, seuil)
                vals = np.empty(N_BOOT_TQ)
                for b in range(N_BOOT_TQ):
                    idx = rng.integers(0, n, n)
                    vals[b], _ = _t_zscore(Emat[idx], seuil)
                lo, hi = ic_percentile(vals)
                lignes.append({
                    "delta_e": float(de), "seuil": float(seuil), "n_graines": int(n),
                    "t_Z": tz, "lo": lo, "hi": hi,
                    "taux_non_defini": float(np.mean(~np.isfinite(vals))),
                    "e_start": e_start, "persistance": PERSIST,
                    "seed_bootstrap": SEED_BOOTSTRAP + 4, "n_boot": N_BOOT_TQ,
                })
    z = pd.DataFrame(lignes)
    z.to_parquet(DATA / "QCD_bis_t_zscore.parquet", index=False)
    _figure_c1bis(z)
    piv = z[z.seuil == 3.0].pivot(index="delta_e", columns="n_graines", values="t_Z")
    print("  t_Z au seuil 3, par nombre de graines :")
    print(piv.to_string(float_format=lambda v: f"{v:8.1f}"))
    print(f"[OK] QCD_bis_t_zscore.parquet ({len(z)} lignes)")
    return z


def _figure_c1bis(z):
    """Deux vues. La seconde porte TOUTES les amplitudes : la premiere en montre
    trois, et choisir trois amplitudes ne doit pas faire la demonstration."""
    reps = [float(v) for v in amplitudes_proches(z.delta_e.unique())[1:4]]
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.4))

    for k, de in enumerate(reps):
        for j, seuil in enumerate(SEUILS_Z):
            g = z[(z.delta_e == de) & (z.seuil == seuil)].sort_values("n_graines")
            if g.t_Z.isna().all():
                continue
            axes[0].plot(g.n_graines, g.t_Z, marker="osd"[j], linestyle=STYLES[k],
                         color=str(GRIS[k]), markersize=5.5, markerfacecolor="white",
                         linewidth=1.1,
                         label=f"$\\Delta e$ = {de:.3f}, seuil {seuil:.0f}")
    axes[0].set_xticks(list(TAILLES_N))
    axes[0].set_yscale("log")
    style_axes(axes[0], "number of seeds averaged", "$t_Z$ (steps since the change, log)")
    axes[0].set_title("Three amplitudes, three thresholds", fontsize=9.5)
    axes[0].legend(fontsize=6.5, ncol=1, loc="upper right")

    # --- toutes les amplitudes, rapporte a n = 100 -----------------------------
    piv = z.pivot_table(index=["delta_e", "seuil"], columns="n_graines", values="t_Z")
    piv = piv.dropna()
    rel = piv.div(piv[100], axis=0)
    for j, seuil in enumerate(SEUILS_Z):
        sub = rel[rel.index.get_level_values("seuil") == seuil]
        if sub.empty:
            continue
        med = sub.median(axis=0)
        axes[1].plot(list(TAILLES_N), [med[n] for n in TAILLES_N], marker="osd"[j],
                     linestyle=STYLES[j], color=str(GRIS[j]), markersize=6,
                     markerfacecolor="white", linewidth=1.3,
                     label=f"seuil {seuil:.0f} ({len(sub)} amplitudes)")
        for _, r in sub.iterrows():
            axes[1].plot(list(TAILLES_N), [r[n] for n in TAILLES_N], "-",
                         color=str(GRIS[j]), linewidth=0.4, alpha=0.30)
    axes[1].axhline(1.0, color="0.2", linewidth=0.9, linestyle=(0, (4, 4)))
    axes[1].set_xticks(list(TAILLES_N))
    style_axes(axes[1], "number of seeds averaged", "$t_Z(n) \\, / \\, t_Z(100)$")
    axes[1].set_title("Every amplitude where $t_Z$ exists at all three sizes\n"
                      "(thin lines), and the median per threshold", fontsize=9.5)
    axes[1].legend(fontsize=8, loc="upper right")

    fig.suptitle("The Z-score crossing time is a function of the sample size: more seeds "
                 "shrink the denominator,\nso the same dynamics crosses earlier. "
                 "$t_Z$ measures $n$, not adaptation.", fontsize=9, y=1.06)
    fig.savefig(FIGURES / "Fig_bis_zscore.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # Le rapport median par seuil est CITE dans le .tex : il doit etre en table.
    lignes = []
    for seuil in SEUILS_Z:
        sub = rel[rel.index.get_level_values("seuil") == seuil]
        for n in TAILLES_N:
            lignes.append({"seuil": float(seuil), "n_graines": int(n),
                           "rapport_median_a_n100": float(sub[n].median()),
                           "n_amplitudes": int(len(sub)),
                           "n_amplitudes_croissantes": int((sub[n] >= 1.0).sum())})
    pd.DataFrame(lignes).assign(seed_bootstrap=SEED_BOOTSTRAP + 4,
                                n_boot=N_BOOT_TQ, persistance=PERSIST).to_parquet(
        DATA / "QCD_bis_zscore_rapports.parquet", index=False)


# ==================================================== CONTROLES SUR CAS CONNUS ==
# Parametres du temoin a bruit correle, ECRITS AVANT le verdict : un effet graine
# de niveau et un AR(1) positif donnent toujours Var[A] >= Sum e(1-e), alors que les
# donnees donnent 0,60 a w = 50. Il faut donc une anticorrelation a court terme,
# plus une heterogeneite de calendrier qui gonfle la variance a grand w.
SC_THETA = 100.0
SC_DELTA_E = 0.30
SC_P0 = 0.023
SC_PHI_AR1 = -0.30          # signe libre, choisi negatif : anticorrelation courte
SC_SIGMA_LOG_THETA = 0.45   # dispersion log-normale du calendrier entre runs
SC_N_VERITE_CORRELE = 5000      # graines de la verite du temoin a bruit correle
SC_N_VERITE_BERNOULLI = 20000   # graines de la verite du temoin Bernoulli
SC_N_ESTIMATION = 100           # graines de l'estimateur teste, comme la campagne
SC_N_REPLICATIONS = 100


def _trajectoires_synthetiques(rng, n, theta=SC_THETA, delta_e=SC_DELTA_E, p0=SC_P0,
                               phi=0.0, sigma_log_theta=0.0):
    """Trajectoires binaires de moyenne p_t = p0 + delta_e exp(-t/theta).

    `phi` : AR(1) sur la variable latente gaussienne (copule) ; `sigma_log_theta` :
    heterogeneite du calendrier d'un run a l'autre. Les deux a zero redonnent le
    cas ferme a bruit independant, dont la reponse `w_opt = 1,2564 theta` est connue.
    """
    from scipy.stats import norm
    t = np.arange(H)
    if sigma_log_theta > 0:
        th = theta * np.exp(rng.normal(0.0, sigma_log_theta, size=n))
        P = p0 + delta_e * np.exp(-t[None, :] / th[:, None])
    else:
        P = np.broadcast_to(p0 + delta_e * np.exp(-t / theta), (n, H))
    if phi == 0.0:
        U = rng.random((n, H))
    else:
        Z = np.empty((n, H))
        Z[:, 0] = rng.normal(0.0, 1.0, n)
        s = np.sqrt(1.0 - phi ** 2)
        bruit = rng.normal(0.0, 1.0, (n, H)) * s
        for k in range(1, H):
            Z[:, k] = phi * Z[:, k - 1] + bruit[:, k]
        U = norm.cdf(Z)
    return (U < P).astype(np.int8), P


def _snr_synthetique(E, p0=SC_P0):
    A = np.cumsum(E.astype(np.float64) - p0, axis=1)[:, GRILLE_W - 1]
    mu, sigma, _ = _snr_un_bloc(A)
    return A, mu, sigma


def _self_check_fenetre(rng, lignes):
    # --- (a1) bruit ADDITIF HOMOSCEDASTIQUE : le cas ferme s'applique ----------
    # La formule w_opt = 1,2564 theta suppose un bruit d'ecart-type CONSTANT. Un
    # tirage de Bernoulli ne l'est pas : Var(e_t) = p_t (1 - p_t) decroit avec le
    # transitoire. On separe donc les deux controles au lieu de les confondre.
    t_ax = np.arange(H)
    signal = SC_DELTA_E * np.exp(-t_ax / SC_THETA)
    X = signal[None, :] + rng.normal(0.0, 0.30, (SC_N_ESTIMATION, H))
    Ah = np.cumsum(X, axis=1)[:, GRILLE_W - 1]
    mu_h, sig_h, _ = _snr_un_bloc(Ah)
    w_h, _, w95h_lo, w95h_hi, _, _ = _w_opt_et_plage(mu_h, sig_h, GRILLE_W)
    verite = W_FIN_OPT * SC_THETA
    # La cible est W_95, pas l'argmax : a 100 graines la courbe SNR est plate
    # autour de son maximum et un argmax ponctuel n'a pas de contenu
    # (meme motif que JOURNAL section 9.5 sur les bornes de maillage).
    lignes.append({
        "controle": "C2bis_a1_bruit_additif_homoscedastique",
        "grandeur": "verite_dans_W95", "attendu": verite, "attendu_lo": w95h_lo,
        "attendu_hi": w95h_hi, "obtenu": w_h, "obtenu_lo": w95h_lo,
        "obtenu_hi": w95h_hi,
        "verdict": bool(w95h_lo <= verite <= w95h_hi),
        "n_verite": np.nan, "n_estimation": SC_N_ESTIMATION,
        "detail": f"bruit gaussien d'ecart-type constant (verite analytique) : les hypotheses du cas ferme "
                  f"sont reunies. Verite 1,2564 theta = {verite:.0f} ; argmax ponctuel "
                  f"a 100 graines = {w_h:.0f}, publie mais non lu ; la lecture porte "
                  f"sur W_95 = [{w95h_lo:.0f}, {w95h_hi:.0f}]",
    })

    # --- (a2) Bernoulli : verite NUMERIQUE, pas la formule fermee --------------
    Eg, _ = _trajectoires_synthetiques(rng, SC_N_VERITE_BERNOULLI)
    _, mug, sigg = _snr_synthetique(Eg)
    w_vrai_bern, _, _, _, _, _ = _w_opt_et_plage(mug, sigg, GRILLE_W)
    E, _ = _trajectoires_synthetiques(rng, SC_N_ESTIMATION)
    A, mu, sigma = _snr_synthetique(E)
    w_opt, _, w95_lo, w95_hi, _, _ = _w_opt_et_plage(mu, sigma, GRILLE_W)
    lignes.append({
        "controle": "C2bis_a2_bernoulli", "grandeur": "verite_dans_W95",
        "attendu": w_vrai_bern, "attendu_lo": w95_lo, "attendu_hi": w95_hi,
        "obtenu": w_opt, "obtenu_lo": w95_lo, "obtenu_hi": w95_hi,
        "verdict": bool(w95_lo <= w_vrai_bern <= w95_hi),
        "n_verite": SC_N_VERITE_BERNOULLI, "n_estimation": SC_N_ESTIMATION,
        "detail": f"verite sur {SC_N_VERITE_BERNOULLI} graines : w_opt = {w_vrai_bern:.0f}, soit "
                  f"{w_vrai_bern / SC_THETA:.2f} theta et non 1,2564 theta -- le bruit "
                  f"binomial est heteroscedastique, la formule fermee ne s'y applique "
                  f"pas. Argmax a 100 graines = {w_opt:.0f}, W_95 = "
                  f"[{w95_lo:.0f}, {w95_hi:.0f}]",
    })
    e_bar = E.mean(axis=0)
    e_start = float(e_bar[FEN_ESTART[0]:FEN_ESTART[1]].mean())
    e_inf = float(e_bar[FEN_EINF[0]:FEN_EINF[1]].mean())
    th = _temps_fractions(e_bar[None, :], np.array([e_start]), np.array([e_inf]), 100)
    t_half = float(th[0.50][0][0])
    # La regle PAS A PAS, celle que le projet appliquait jusqu'ici, est mesuree sur
    # le meme cas connu : c'est elle qui justifie le changement de regle, et une
    # phrase publiee doit se relire dans une table, pas dans un commentaire.
    baisse = e_start - e_inf
    niveau_pas = e_inf + 0.5 * baisse
    t_half_pas = float(premier_franchissement((e_bar <= niveau_pas)[None, :], PERSIST)[0])
    lignes.append({
        "controle": "C2bis_a2_bernoulli", "grandeur": "t_half_regle_pas_a_pas",
        "attendu": SC_THETA * LN2, "attendu_lo": 0.75 * SC_THETA * LN2,
        "attendu_hi": 1.25 * SC_THETA * LN2, "obtenu": t_half_pas,
        "obtenu_lo": np.nan, "obtenu_hi": np.nan,
        "verdict": bool(0.75 * SC_THETA * LN2 <= t_half_pas <= 1.25 * SC_THETA * LN2),
        "detail": "regle du projet jusqu'au 15/09 : seuil tenu a CHAQUE pas de la "
                  "fenetre de persistance. C'est ce controle qui l'a fait abandonner ; "
                  "la ligne suivante donne la regle retenue sur le meme tirage.",
    })
    lignes.append({
        "controle": "C2bis_a2_bernoulli",
        "grandeur": "t_half", "attendu": SC_THETA * LN2, "attendu_lo": 0.75 * SC_THETA * LN2,
        "attendu_hi": 1.25 * SC_THETA * LN2, "obtenu": t_half,
        "obtenu_lo": np.nan, "obtenu_hi": np.nan,
        "verdict": bool(0.75 * SC_THETA * LN2 <= t_half <= 1.25 * SC_THETA * LN2),
        "detail": "exponentielle pure : t_half = theta ln 2. Le biais residuel mesure "
                  "ici est celui de la regle de franchissement en moyenne sur "
                  f"{PERSIST} pas, a reporter sur toutes les valeurs de t_q publiees.",
    })

    # --- (b) bruit correle : verite par simulation, validation par couverture ---
    Ev, _ = _trajectoires_synthetiques(rng, SC_N_VERITE_CORRELE, phi=SC_PHI_AR1,
                                       sigma_log_theta=SC_SIGMA_LOG_THETA)
    Av, muv, sigv = _snr_synthetique(Ev)
    w_vrai, _, w95v_lo, w95v_hi, _, _ = _w_opt_et_plage(muv, sigv, GRILLE_W)
    plateau = (w95v_hi - w95v_lo) / max(w_vrai, 1.0)
    e_barv = Ev.mean(axis=0)
    var_formule = np.cumsum(e_barv * (1 - e_barv))[GRILLE_W - 1]
    ratio50 = float(sigv[GRILLE_W == 50][0] / np.sqrt(var_formule[GRILLE_W == 50][0]))
    ratio2000 = float(sigv[GRILLE_W == 2000][0] / np.sqrt(var_formule[GRILLE_W == 2000][0]))
    lignes.append({
        "controle": "C2bis_b_bruit_correle", "grandeur": "ratio_sigma_emp_formule_w50",
        "attendu": np.nan, "attendu_lo": np.nan, "attendu_hi": np.nan,
        "obtenu": ratio50, "obtenu_lo": np.nan, "obtenu_hi": np.nan,
        "verdict": bool(ratio50 < 1.0),
        "detail": f"cible qualitative : < 1 comme les donnees (0,60) ; "
                  f"phi = {SC_PHI_AR1}, sigma_log_theta = {SC_SIGMA_LOG_THETA}",
    })
    lignes.append({
        "controle": "C2bis_b_bruit_correle", "grandeur": "ratio_sigma_emp_formule_w2000",
        "attendu": np.nan, "attendu_lo": np.nan, "attendu_hi": np.nan,
        "obtenu": ratio2000, "obtenu_lo": np.nan, "obtenu_hi": np.nan,
        "verdict": bool(ratio2000 > 1.0),
        "detail": "cible qualitative : > 1 comme les donnees (1,59)",
    })
    lignes.append({
        "controle": "C2bis_b_bruit_correle", "grandeur": "plateau_relatif_W95",
        "attendu": np.nan, "attendu_lo": np.nan, "attendu_hi": np.nan,
        "obtenu": float(plateau), "obtenu_lo": w95v_lo, "obtenu_hi": w95v_hi,
        "verdict": bool(np.isfinite(plateau)),
        "detail": "largeur de W_95 rapportee a w_opt sur 5 000 graines : au-dela de "
                  "0,20 la cible de couverture est W_95, pas le point",
    })

    couv_point, couv_plage = 0, 0
    for _ in range(SC_N_REPLICATIONS):
        Er, _ = _trajectoires_synthetiques(rng, SC_N_ESTIMATION, phi=SC_PHI_AR1,
                                           sigma_log_theta=SC_SIGMA_LOG_THETA)
        Ar, _, _ = _snr_synthetique(Er)
        wb, wlb, whb = _bootstrap_w_opt(Ar, rng, GRILLE_W, n_boot=500)
        lo, hi = ic_percentile(wb)
        if np.isfinite(lo) and lo <= w_vrai <= hi:
            couv_point += 1
        if np.isfinite(lo) and not (hi < w95v_lo or lo > w95v_hi):
            couv_plage += 1
    for nom, val, det in (
            ("couverture_IC_w_opt", couv_point / SC_N_REPLICATIONS,
             f"IC de w_opt contenant la verite {w_vrai:.0f}"),
            ("couverture_IC_W95", couv_plage / SC_N_REPLICATIONS,
             f"IC de w_opt intersectant W_95 vrai [{w95v_lo:.0f}, {w95v_hi:.0f}]")):
        lignes.append({
            "controle": "C2bis_b_bruit_correle", "grandeur": nom, "attendu": 0.95,
            "attendu_lo": 0.90, "attendu_hi": 1.00, "obtenu": float(val),
            "obtenu_lo": np.nan, "obtenu_hi": np.nan,
            "verdict": bool(val >= 0.90),
            "detail": f"{SC_N_REPLICATIONS} replications de 100 graines ; {det}",
        })

    # --- (c) temoin nul : aucun signal ----------------------------------------
    E0, _ = _trajectoires_synthetiques(rng, SC_N_ESTIMATION, delta_e=0.0)
    A0, mu0, sig0 = _snr_synthetique(E0)
    w0_opt, _, w095_lo, w095_hi, _, _ = _w_opt_et_plage(mu0, sig0, GRILLE_W)
    sur_borne = bool(w0_opt in (GRILLE_W[0], GRILLE_W[-1]))
    large = bool(np.isfinite(w095_lo) and (w095_hi - w095_lo) >= 0.5 * GRILLE_W[-1])
    _, snr0_max, _, _, _, _ = _w_opt_et_plage(mu0, sig0, GRILLE_W)
    non_signif = bool(not (np.isfinite(snr0_max) and snr0_max > 3.0 / np.sqrt(100)))
    e_bar0 = E0.mean(axis=0)
    es0 = float(e_bar0[FEN_ESTART[0]:FEN_ESTART[1]].mean())
    ei0 = float(e_bar0[FEN_EINF[0]:FEN_EINF[1]].mean())
    marge = 0.5 * (es0 - ei0)
    niveau = ei0 + marge
    interp = bool(marge > 2 * se_binomiale(niveau, 100))
    for nom, val, det in (
            ("critere_w_opt_sur_borne", sur_borne,
             "critere prevu au plan : w_opt sur une borne de la grille"),
            ("critere_W95_large", large,
             "critere prevu au plan : W_95 couvrant la moitie de la grille"),
            ("critere_snr_max_non_significatif", non_signif,
             f"critere AJOUTE apres l'echec des deux precedents : SNR max = "
             f"{snr0_max:.4f} contre un seuil de 3/sqrt(n) = {3 / np.sqrt(100):.4f}")):
        lignes.append({
            "controle": "C2bis_c_temoin_nul", "grandeur": nom, "attendu": 1.0,
            "attendu_lo": np.nan, "attendu_hi": np.nan, "obtenu": float(val),
            "obtenu_lo": np.nan, "obtenu_hi": np.nan, "verdict": bool(val),
            "detail": det,
        })
    lignes.append({
        "controle": "C2bis_c_temoin_nul", "grandeur": "flag_leve",
        "attendu": 1.0, "attendu_lo": np.nan, "attendu_hi": np.nan,
        "obtenu": float(sur_borne or large or non_signif),
        "obtenu_lo": w095_lo, "obtenu_hi": w095_hi,
        "verdict": bool(sur_borne or large or non_signif),
        "detail": f"delta_e = 0 : w_opt sur une borne ({sur_borne}), W_95 couvrant la "
                  f"moitie de la grille ({large}), ou SNR max sous 3/sqrt(n) "
                  f"({non_signif}, max = {snr0_max:.3f})",
    })
    lignes.append({
        "controle": "C2bis_c_temoin_nul", "grandeur": "interpretable_t_half",
        "attendu": 0.0, "attendu_lo": np.nan, "attendu_hi": np.nan,
        "obtenu": float(interp), "obtenu_lo": np.nan, "obtenu_hi": np.nan,
        "verdict": not interp,
        "detail": "sans signal, aucun temps de fraction ne doit etre declare lisible",
    })


def _self_check_simpson(rng, lignes):
    """Deux jeux synthetiques : Simpson pur, puis temoin sans Simpson."""
    n_strates, n_par_strate = 20, 100
    for nom, avec_simpson in (("D3bis_a_simpson_pur", True),
                              ("D3bis_b_temoin_sans_simpson", False)):
        xs, ys, strates = [], [], []
        for s in range(n_strates):
            if avec_simpson:
                # moyennes de X ET de Y croissantes avec la strate, X et Y
                # INDEPENDANTS a l'interieur : tout coefficient empile est un
                # artefact de la grille.
                x = rng.normal(10.0 * s, 1.0, n_par_strate)
                y = rng.normal(10.0 * s, 1.0, n_par_strate)
            else:
                # relation reelle dans chaque strate, moyennes constantes.
                x = rng.normal(0.0, 1.0, n_par_strate)
                y = x + rng.normal(0.0, 1.0, n_par_strate)
            xs.append(x)
            ys.append(y)
            strates.append(np.full(n_par_strate, s))
        X = np.concatenate(xs)
        Y = np.concatenate(ys)
        S = np.concatenate(strates)
        emp, _ = kendall_censored(X, Y, H)
        par_strate = np.array([kendall_censored(X[S == s], Y[S == s], H)[0]
                               for s in range(n_strates)])
        med = float(np.median(par_strate))
        vals = np.empty(500)
        for b in range(500):
            tir = rng.integers(0, n_strates, n_strates)
            vals[b] = float(np.median(par_strate[tir]))
        lo, hi = ic_percentile(vals)
        ratio = abs(emp) / abs(med) if abs(med) > 1e-12 else np.inf
        if avec_simpson:
            ok = bool(emp > 0.30 and lo <= 0.0 <= hi and ratio > 3.0)
            det = ("X et Y independants dans chaque strate, moyennes des deux "
                   "croissantes : empile > 0, mediane stratifiee couvrant 0, ratio >> 1")
        else:
            ok = bool(abs(ratio - 1.0) < 0.25 and lo > 0.0)
            det = ("Y = X + bruit dans chaque strate, moyennes constantes : "
                   "empile et stratifie doivent coincider, ratio ~ 1")
        for g, v in (("tau_b_empile", emp), ("mediane_stratifiee", med),
                     ("ratio_simpson", ratio)):
            lignes.append({
                "controle": nom, "grandeur": g,
                "attendu": np.nan, "attendu_lo": np.nan, "attendu_hi": np.nan,
                "obtenu": float(v),
                "obtenu_lo": lo if g == "mediane_stratifiee" else np.nan,
                "obtenu_hi": hi if g == "mediane_stratifiee" else np.nan,
                "verdict": ok, "detail": det,
            })


def run_self_check(args):
    print("[self-check] controles sur cas connus")
    rng = np.random.default_rng(SEED_BOOTSTRAP + 7)
    lignes = []
    _self_check_fenetre(rng, lignes)
    _self_check_simpson(rng, lignes)
    sc = pd.DataFrame(lignes)
    sc["seed"] = SEED_BOOTSTRAP + 7
    sc["n_replications"] = SC_N_REPLICATIONS
    sc.to_parquet(DATA / "QCD_bis_self_check.parquet", index=False)
    print(sc[["controle", "grandeur", "attendu", "obtenu", "verdict"]].to_string(
        index=False, float_format=lambda v: f"{v:10.4f}"))
    echecs = sc[~sc.verdict]
    if len(echecs):
        print(f"[ATTENTION] {len(echecs)} controle(s) en echec :")
        print(echecs[["controle", "grandeur", "obtenu", "detail"]].to_string(index=False))
    print(f"[OK] QCD_bis_self_check.parquet ({len(sc)} lignes)")
    return sc



# ============================== D.1.bis, volet pilote par arbre (tache 5b) =====
# Lit `QCD_bis_traces_arbres_pilote.parquet`, produit par `exp_bis_pilote_arbres.py`
# apres reproduction bit a bit de la campagne (trajectoire ET remplacements).
N_BLOCS_TAU = 6
FEN_BLOC_COURT = 10         # <= 10 pas : une fenetre de 50 decalerait de 25, contre
                            # un transitoire de 28 a 38 pas en haut de grille.


def _taux_par_arbre(e, vote):
    """Taux d'erreur de chaque arbre sur une fenetre, NaN si l'arbre n'a pas vote."""
    n = vote.sum(axis=0)
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.where(n > 0, (e * vote).sum(axis=0) / np.where(n > 0, n, 1), np.nan), n


def run_arbres(args):
    f = DATA / "QCD_bis_traces_arbres_pilote.parquet"
    if not f.exists():
        print("[D.1.bis/5b] pilote par arbre absent : lancer exp_bis_pilote_arbres.py")
        return None
    print("[D.1.bis/5b] variance transversale des taux d'erreur par arbre")
    tr = pd.read_parquet(f)
    meta = pd.read_parquet(DATA / "QCD_bis_meta_arbres_pilote.parquet")
    ind = pd.read_parquet(DATA / "QCD_indicateurs_full.parquet").set_index("run_id")
    ev = pd.read_parquet(DATA / "QCD_bis_events_swap_arbres_pilote.parquet")
    m = int(meta.n_models.iloc[0])

    n_runs = len(meta)
    E = np.zeros((n_runs, H, m), dtype=np.int8)
    V = np.zeros((n_runs, H, m), dtype=np.int8)
    E[tr.run_id.to_numpy(), tr.t.to_numpy(), tr.tree_id.to_numpy()] = tr.e.to_numpy()
    V[tr.run_id.to_numpy(), tr.t.to_numpy(), tr.tree_id.to_numpy()] = tr.a_vote.to_numpy()

    lignes, series = [], []
    for r in meta.itertuples():
        tau = float(ind.loc[int(r.run_id_campagne), "tau_arf"])
        if not np.isfinite(tau) or tau < 1:
            continue
        deja = np.zeros(m, dtype=bool)
        evr = ev[ev.run_id == r.run_id].sort_values("t")
        for k in range(N_BLOCS_TAU):
            a, b = int(round(k * tau)), int(round((k + 1) * tau))
            if a >= H:
                break
            b = min(b, H)
            neufs = deja.copy()            # etat AU DEBUT du bloc
            taux, n_obs = _taux_par_arbre(E[r.run_id, a:b], V[r.run_id, a:b])
            bon = np.isfinite(taux)
            if bon.sum() < 2:
                continue
            var_obs = float(np.var(taux[bon], ddof=1))
            p_bar = float(np.mean(taux[bon]))
            # Variance d'echantillonnage attendue si TOUS les arbres avaient le meme
            # taux p_bar : au-dela, l'heterogeneite est reelle et persistante.
            n_eff = float(np.mean(n_obs[bon]))
            var_att = p_bar * (1 - p_bar) / n_eff if n_eff > 0 else np.nan
            lignes.append({
                "delta_e": float(r.delta_e), "seed": int(r.seed),
                "run_id_pilote": int(r.run_id), "bloc": k,
                "t_debut": a, "t_fin": b, "tau_arf": tau,
                "var_transversale": var_obs,
                "var_echantillonnage_attendue": var_att,
                "exces_variance": var_obs / var_att if var_att and var_att > 0 else np.nan,
                "taux_moyen": p_bar,
                "n_arbres_lus": int(bon.sum()),
                "n_arbres_deja_remplaces": int(neufs.sum()),
                "taux_moyen_neufs": float(np.nanmean(taux[bon & neufs]))
                                    if (bon & neufs).any() else np.nan,
                "taux_moyen_survivants": float(np.nanmean(taux[bon & ~neufs]))
                                         if (bon & ~neufs).any() else np.nan,
                "n_models": m, "fenetre": "bloc aligne sur tau_ARF",
                "seed_pilote": int(r.seed),
            })
            for e in evr[(evr.t >= a) & (evr.t < b)].itertuples():
                deja[int(e.tree_id)] = True

        # Serie en blocs DISJOINTS courts (pas glissants), pour la figure seulement.
        w = FEN_BLOC_COURT
        nb = H // w
        e3 = E[r.run_id, :nb * w].reshape(nb, w, m)
        v3 = V[r.run_id, :nb * w].reshape(nb, w, m)
        nv = v3.sum(axis=1)
        with np.errstate(invalid="ignore"):
            tx = np.where(nv > 0, (e3 * v3).sum(axis=1) / np.where(nv > 0, nv, 1), np.nan)
        series.append(pd.DataFrame({
            "delta_e": float(r.delta_e), "seed": int(r.seed),
            "t": np.arange(nb) * w, "var_transversale": np.nanvar(tx, axis=1, ddof=1),
            "taux_moyen": np.nanmean(tx, axis=1), "fenetre": w,
        }))

    blocs = pd.DataFrame(lignes)
    ser = pd.concat(series, ignore_index=True)
    agg = (blocs.groupby(["delta_e", "bloc"])
           .agg(var_transversale=("var_transversale", "mean"),
                var_echantillonnage_attendue=("var_echantillonnage_attendue", "mean"),
                exces_variance=("exces_variance", "median"),
                taux_moyen=("taux_moyen", "mean"),
                taux_moyen_neufs=("taux_moyen_neufs", "mean"),
                taux_moyen_survivants=("taux_moyen_survivants", "mean"),
                n_arbres_deja_remplaces=("n_arbres_deja_remplaces", "mean"),
                tau_arf_median=("tau_arf", "median"),
                n_runs=("seed", "nunique"))
           .reset_index())
    agg["ecart_neufs_survivants"] = agg.taux_moyen_neufs - agg.taux_moyen_survivants
    agg["n_models"] = m
    agg["fenetre"] = "bloc aligne sur tau_ARF"
    blocs.to_parquet(DATA / "QCD_bis_variance_arbres.parquet", index=False)
    agg.to_parquet(DATA / "QCD_bis_variance_arbres_agregee.parquet", index=False)
    _figure_arbres(agg, ser)
    print(agg[["delta_e", "bloc", "tau_arf_median", "var_transversale",
               "exces_variance", "taux_moyen_neufs", "taux_moyen_survivants",
               "ecart_neufs_survivants", "n_arbres_deja_remplaces"]].to_string(
        index=False, float_format=lambda v: f"{v:8.4f}"))
    print(f"[OK] QCD_bis_variance_arbres.parquet ({len(blocs)} lignes), "
          f"QCD_bis_variance_arbres_agregee.parquet ({len(agg)} lignes)")
    return agg


def _figure_arbres(agg, ser):
    des = sorted(agg.delta_e.unique())
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.4))
    for k, de in enumerate(des):
        g = agg[agg.delta_e == de].sort_values("bloc")
        axes[0].plot(g.bloc, g.var_transversale, marker="o", linestyle=STYLES[k % 5],
                     color=str(GRIS[k % 5]), markersize=5, markerfacecolor="white",
                     linewidth=1.2, label=f"$\\Delta e$ = {de:.3f}")
        s = ser[ser.delta_e == de].groupby("t").var_transversale.mean()
        axes[1].plot(s.index, s.to_numpy(), linestyle=STYLES[k % 5],
                     color=str(GRIS[k % 5]), linewidth=1.0)
    axes[0].set_xticks(range(N_BLOCS_TAU))
    style_axes(axes[0], "block index $k$ (block = $[k\\tau_{ARF}, (k+1)\\tau_{ARF})$)",
               "cross-tree variance of error rates")
    axes[0].set_title("Aligned on each run's own $\\tau_{ARF}$", fontsize=9.5)
    axes[0].legend(fontsize=8)
    axes[1].set_xlim(0, 400)
    style_axes(axes[1], "steps since the change",
               "cross-tree variance of error rates")
    axes[1].set_title(f"Disjoint blocks of {FEN_BLOC_COURT} steps "
                      "(short enough not to smear the transient)", fontsize=9.5)
    fig.suptitle("Tree dispersion measured directly: per-tree error rates from the "
                 "instrumented pilot\n(5 amplitudes, 20 seeds, bit-for-bit identical "
                 "to the campaign)", fontsize=9, y=1.10)
    fig.savefig(FIGURES / "Fig_bis_variance_arbres.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


# ============ CONSEQUENCE POUR C.1.c : tau_err sous les deux regles ============
# `analyse_QCD.py::tau_err_table` calcule tau_err(rho) par la regle PAS A PAS, la
# meme que le controle sur cas connu a montree biaisee (112 pour une verite de
# 69,3147). La question n'est pas de refaire C.1.c, qui n'est pas notre piste,
# mais de mesurer si le verdict en depend. Lecture seule, hors ligne, rejouable.
def run_tauerr(args):
    print("[C.1.c] tau_err sous les deux regles de franchissement")
    from analyse_QCD import RHO_ERR
    E, meta = charger_campagne()
    ind = pd.read_parquet(DATA / "QCD_indicateurs_full.parquet")
    tau_med = ind.groupby("delta_e")["tau_arf"].median()
    ref = pd.read_parquet(DATA / "QCD_tau_err_full.parquet")

    lignes = []
    for de, grp in meta.groupby("delta_e", sort=True):
        e_mean = E[grp.run_id.to_numpy()].mean(axis=0)
        p0 = float(grp.p_hat_0.mean())
        seuil = RHO_ERR * de
        sigma = float(e_mean[-500:].std())
        ecart = e_mean - p0
        ok = ecart <= seuil
        conv = np.convolve(ok.astype(int), np.ones(PERSIST, int), "valid")
        hit = np.flatnonzero(conv == PERSIST)
        t_pas = float(hit[0]) if hit.size else np.nan
        t_moy = float(franchissement_en_moyenne(ecart[None, :], np.array([seuil]),
                                                PERSIST)[0])
        tm = float(tau_med.loc[de])
        lignes.append({
            "delta_e": float(de), "rho": RHO_ERR, "seuil": seuil,
            "sigma_courbe": sigma, "interpretable": bool(seuil > 2 * sigma),
            "tau_arf_median": tm,
            "tau_err_pas_a_pas": t_pas, "tau_err_en_moyenne": t_moy,
            "ecart_deux_regles": t_pas - t_moy,
            "avant_tau_arf_pas_a_pas": bool(np.isfinite(t_pas) and t_pas < tm),
            "avant_tau_arf_en_moyenne": bool(np.isfinite(t_moy) and t_moy < tm),
            "persistance": PERSIST, "n_runs": len(grp),
        })
    d = pd.DataFrame(lignes)
    d["verdict_bascule"] = d.avant_tau_arf_pas_a_pas != d.avant_tau_arf_en_moyenne

    # Controle : la colonne pas a pas doit reproduire la table publiee de C.1.c.
    m = d.merge(ref[["delta_e", "tau_err_p20"]], on="delta_e")
    ecart_ref = float(np.nanmax(np.abs(m.tau_err_pas_a_pas - m.tau_err_p20)))
    print(f"  non-regression contre QCD_tau_err_full : ecart max {ecart_ref:.0f} pas")
    if ecart_ref > 0:
        raise ValueError("la reimplementation ne reproduit pas tau_err_p20")

    d.to_parquet(DATA / "QCD_bis_tau_err_deux_regles.parquet", index=False)
    i = d[d.interpretable]
    print(f"  sur les {len(i)} amplitudes interpretables : "
          f"{int(i.avant_tau_arf_pas_a_pas.sum())}/{len(i)} avec la regle pas a pas, "
          f"{int(i.avant_tau_arf_en_moyenne.sum())}/{len(i)} avec la regle en moyenne")
    print(f"  verdicts qui basculent : {int(i.verdict_bascule.sum())}")
    print(f"  ecart entre regles : median {i.ecart_deux_regles.median():.0f} pas, "
          f"max {i.ecart_deux_regles.max():.0f}, min {i.ecart_deux_regles.min():.0f}")
    print(d[["delta_e", "interpretable", "tau_arf_median", "tau_err_pas_a_pas",
             "tau_err_en_moyenne", "verdict_bascule"]].to_string(
        index=False, float_format=lambda v: f"{v:9.1f}"))
    print(f"[OK] QCD_bis_tau_err_deux_regles.parquet ({len(d)} lignes)")
    return d


# ================================================================== CLI ========
def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--c3bis", action="store_true", help="profil d'erreur (priorite 1)")
    p.add_argument("--c2bis", action="store_true", help="fenetre d'accumulation (pr. 2)")
    p.add_argument("--d3bis", action="store_true", help="matrice de correlation (pr. 3)")
    p.add_argument("--d1bis", action="store_true", help="dispersion entre arbres (pr. 4)")
    p.add_argument("--c1bis", action="store_true", help="Z-score (priorite 5)")
    p.add_argument("--tauerr", action="store_true",
                   help="consequence de la regle de franchissement sur tau_err (C.1.c)")
    p.add_argument("--arbres", action="store_true",
                   help="volet 5b : variance par arbre depuis le pilote instrumente")
    p.add_argument("--self-check", action="store_true", help="controles sur cas connus")
    p.add_argument("--all", action="store_true", help="tout, dans l'ordre des dependances")
    a = p.parse_args()
    if not any([a.c3bis, a.c2bis, a.d3bis, a.d1bis, a.c1bis, a.arbres, a.tauerr,
                a.self_check, a.all]):
        p.error("choisir au moins une sous-commande")
    if a.all or a.self_check:
        run_self_check(a)
    if a.all or a.c3bis:
        run_c3bis(a)
    if a.all or a.c2bis:
        run_c2bis(a)
    if a.all or a.d3bis:
        run_d3bis(a)
    if a.all or a.d1bis:
        run_d1bis(a)
    if a.all or a.arbres:
        run_arbres(a)
    if a.all or a.c1bis:
        run_c1bis(a)
    if a.all or a.tauerr:
        run_tauerr(a)


if __name__ == "__main__":
    main()
