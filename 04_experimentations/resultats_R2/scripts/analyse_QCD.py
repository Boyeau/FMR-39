"""
analyse_QCD.py
===================================================================
Analyse hors ligne de la campagne produite par `exp_QCD_campagne.py`.

Aucune simulation n'est relancee ici. Tout se deduit des deux seules choses
enregistrees par la campagne : la trajectoire d'erreur e_t, et la table des
evenements de remplacement.

CE QUI SE RECALCULE HORS LIGNE
    S_t, tau_det et S_max pour n'importe quel lambda et n'importe quel delta_P ;
    A(H) pour n'importe quel H <= 2000 ; tau_ARF ; tau_swap(q) pour tout q.
    C'est ce qui permet a UNE campagne de remplacer les trois de R2.

RECONSTRUCTION DE S_t
    La recurrence S_t = max(0, S_{t-1} + x_t), avec x_t = e_t - p_hat_0 - delta_P
    et S_0 = 0, admet la forme close de Lindley : S_t = C_t - min_{0<=k<=t} C_k,
    ou C est la somme cumulee de x. C'est exactement l'identite demandee en C.2,
    S_max(H) = max_{k<=j} [A(k,j) - (j-k) delta_P] : le minimum courant selectionne
    la sous-fenetre optimale. `--self-check` verifie la forme close contre la
    recurrence naive, pas a pas.

USAGE
    python analyse_QCD.py --tag proto
    python analyse_QCD.py --tag full --boot 2000
    python analyse_QCD.py --self-check      # controle de la reconstruction seule
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import kendalltau

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "resultats" / "data"
FIGURES_DIR = ROOT_DIR / "resultats" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# --- Constantes du sujet -------------------------------------------------------
H = 2000
N_MODELS = 10
DELTA_P = 0.01                          # StrictCUSUM(delta=0.01) dans R2
LAMBDAS = (8.0, 25.0, 50.0)
SWAP_QUANTILES = (0.10, 0.25, 0.50, 0.75)
N_BOOT = 2000
DELTA_E_MIN_DECISION = 0.10             # domaine de validite du critere (D.4)
TAU_ARF_FIT = (18.5, -0.98)             # ajustement de l'article : 18,5 * Delta_e^-0,98
RHO_ERR = 0.25                          # fraction de resorption residuelle pour tau_err(rho)
PERSIST = 20                            # pas consecutifs exiges avant de declarer la resorption


# ------------------------------------------------------------------ CUSUM ------
def cusum_path(e, p0, delta_p=DELTA_P):
    """S_t par la forme close de Lindley. `e` de forme (..., H)."""
    x = e.astype(np.float64) - p0 - delta_p
    c = np.cumsum(x, axis=-1)
    zero = np.zeros(c.shape[:-1] + (1,))
    c_full = np.concatenate([zero, c], axis=-1)          # C_0 = 0
    running_min = np.minimum.accumulate(c_full, axis=-1)
    return c_full[..., 1:] - running_min[..., 1:]


def cusum_path_recurrent(e, p0, delta_p=DELTA_P):
    """Reference naive, uniquement pour le controle. Une seule trajectoire."""
    s, out = 0.0, np.empty(len(e), dtype=np.float64)
    for i, ei in enumerate(e):
        s = max(0.0, s + (float(ei) - p0) - delta_p)
        out[i] = s
    return out


def self_check(rng, n=200, horizon=H):
    """Verifie la forme close contre la recurrence, exigence de l'annexe."""
    worst = 0.0
    for _ in range(n):
        p0 = float(rng.uniform(0.005, 0.08))
        e = (rng.random(horizon) < rng.uniform(0.01, 0.6)).astype(np.int8)
        worst = max(worst, np.abs(cusum_path(e, p0) - cusum_path_recurrent(e, p0)).max())
    return worst


# ------------------------------------------------- indicateurs par execution ---
def load_campaign(tag):
    meta = pd.read_parquet(DATA_DIR / f"QCD_runs_meta_{tag}.parquet")
    traces = pd.read_parquet(DATA_DIR / f"QCD_traces_error_{tag}.parquet")
    events = pd.read_parquet(DATA_DIR / f"QCD_events_swap_{tag}.parquet")

    meta = meta.sort_values('run_id').reset_index(drop=True)
    if not np.array_equal(meta['run_id'].to_numpy(), np.arange(len(meta))):
        raise ValueError("run_id non contigus : l'indexation positionnelle de error_mat casserait")
    traces = traces.sort_values(['run_id', 't'], kind='stable')
    counts = traces.groupby('run_id', sort=True).size().to_numpy()
    if not np.all(counts == H):
        raise ValueError(f"trajectoires incompletes : longueurs {set(counts.tolist())}, attendu {H}")
    error_mat = traces['e'].to_numpy().reshape(len(meta), H)
    return meta, error_mat, events


def phi_matrix(events, n_runs):
    """phi(t) = N_t / M par execution, ou N_t compte les arbres DISTINCTS renouvelees.

    Reconstruit depuis la seule table d'evenements : on prend le premier
    remplacement de chaque arbre, puis on cumule. Un arbre remplace trois fois ne
    compte que pour un.
    """
    phi = np.zeros((n_runs, H))
    if len(events) == 0:
        return phi
    first = events.groupby(['run_id', 'tree_id'], sort=False)['t'].min().reset_index()
    for run_id, grp in first.groupby('run_id', sort=False):
        counts = np.bincount(grp['t'].to_numpy().astype(int), minlength=H)[:H]
        phi[run_id] = np.cumsum(counts) / N_MODELS
    return phi


def swap_times(events, meta):
    """tau_ARF et tau_swap(q), reconstruits depuis la table d'evenements.

    tau_swap(q) compte les arbres DISTINCTS renouvelees : un arbre remplace trois
    fois ne vaut qu'un seul arbre renouvele dans la foret.
    """
    n_runs = len(meta)
    tau_arf = np.full(n_runs, np.nan)
    tau_swap = {q: np.full(n_runs, np.nan) for q in SWAP_QUANTILES}
    if len(events) == 0:
        return tau_arf, tau_swap

    ev = events.sort_values(['run_id', 't'], kind='stable')
    for run_id, grp in ev.groupby('run_id', sort=False):
        ts = grp['t'].to_numpy()
        tids = grp['tree_id'].to_numpy()
        tau_arf[run_id] = float(ts[0])
        seen, distinct = set(), np.empty(len(ts), dtype=np.int32)
        for i, tid in enumerate(tids):
            seen.add(int(tid))
            distinct[i] = len(seen)
        for q in SWAP_QUANTILES:
            hit = np.flatnonzero(distinct >= q * N_MODELS)
            if hit.size:
                tau_swap[q][run_id] = float(ts[hit[0]])
    return tau_arf, tau_swap


def build_indicators(meta, error_mat, events):
    p0 = meta['p_hat_0'].to_numpy()[:, None]
    s_mat = cusum_path(error_mat, p0)

    df = meta.copy()
    df['A_H'] = (error_mat - p0).sum(axis=1)
    df['S_max_H'] = s_mat.max(axis=1)

    for lam in LAMBDAS:
        reached = s_mat >= lam
        any_hit = reached.any(axis=1)
        td = np.where(any_hit, reached.argmax(axis=1).astype(float), np.nan)
        df[f'tau_det_{int(lam)}'] = td
        df[f'censored_det_{int(lam)}'] = ~any_hit

    tau_arf, tau_swap = swap_times(events, meta)
    df['tau_arf'] = tau_arf
    df['censored_arf'] = np.isnan(tau_arf)
    for q in SWAP_QUANTILES:
        df[f'tau_swap_{int(q * 100)}'] = tau_swap[q]
        df[f'censored_swap_{int(q * 100)}'] = np.isnan(tau_swap[q])
    return df, s_mat


# ------------------------------------------------------------- correlations ----
def kendall_censored(x, y, horizon=H):
    """tau-b en imputant les valeurs censurees au rang maximal.

    Legitime ici parce que l'horizon est IDENTIQUE pour toutes les executions :
    une valeur censuree depasse effectivement toute valeur observee. L'argument
    tomberait si l'horizon variait d'une execution a l'autre.
    """
    xf = np.where(np.isnan(x), horizon, x)
    yf = np.where(np.isnan(y), horizon, y)
    if np.all(xf == xf[0]) or np.all(yf == yf[0]):
        return np.nan, np.nan
    return kendalltau(xf, yf)


def bootstrap_ci(x, y, rng, n_boot=N_BOOT, horizon=H):
    """IC bootstrap sur les GRAINES de la strate, quantiles 2,5 % / 97,5 %."""
    n = len(x)
    if n < 3:
        return np.nan, np.nan
    vals = np.empty(n_boot)
    for b in range(n_boot):
        idx = rng.integers(0, n, n)
        t, _ = kendall_censored(x[idx], y[idx], horizon)
        vals[b] = t
    vals = vals[~np.isnan(vals)]
    if vals.size == 0:
        return np.nan, np.nan
    return float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))


def tau_b_threshold(n):
    """Ecart-type de tau-b sous H0 ; en deca de 1,96 sigma, rien n'est discernable."""
    sigma = np.sqrt(2 * (2 * n + 5) / (9 * n * (n - 1)))
    return sigma, 1.96 * sigma


def stratified_correlations(df, rng, n_boot=N_BOOT):
    comparators = [f'tau_swap_{int(q * 100)}' for q in SWAP_QUANTILES] + ['A_H', 'S_max_H']
    rows = []
    for de, grp in df.groupby('delta_e', sort=True):
        x = grp['tau_arf'].to_numpy(dtype=float)
        n = len(grp)
        sigma, thr = tau_b_threshold(n)
        for comp in comparators:
            y = grp[comp].to_numpy(dtype=float)
            tau, p = kendall_censored(x, y)
            lo, hi = bootstrap_ci(x, y, rng, n_boot)
            rows.append({
                'delta_e': de, 'comparateur': comp, 'n': n,
                'tau_b': tau, 'p_value': p, 'ci_lo': lo, 'ci_hi': hi,
                'seuil_detectabilite': thr,
                'discernable': (not np.isnan(tau)) and abs(tau) > thr,
                'censure_tau_arf': float(np.mean(np.isnan(x))),
                'censure_comparateur': float(np.mean(np.isnan(y))),
                'dans_domaine_decision': de >= DELTA_E_MIN_DECISION,
            })
    return pd.DataFrame(rows), comparators


def global_correlations(df, comparators):
    """tau-b global, calcule UNIQUEMENT pour documenter l'effondrement par agregation."""
    x = df['tau_arf'].to_numpy(dtype=float)
    rows = []
    for comp in comparators:
        tau, p = kendall_censored(x, df[comp].to_numpy(dtype=float))
        rows.append({'comparateur': comp, 'tau_b_global': tau, 'p_value': p})
    return pd.DataFrame(rows)


def complete_cases_comparison(df, comparators):
    """Echantillon impute vs cas complets (D.4) : un ecart marque signale que la
    censure pilote le resultat."""
    rows = []
    for de, grp in df.groupby('delta_e', sort=True):
        x = grp['tau_arf'].to_numpy(dtype=float)
        for comp in comparators:
            y = grp[comp].to_numpy(dtype=float)
            tau_imp, _ = kendall_censored(x, y)
            keep = ~np.isnan(x) & ~np.isnan(y)
            if keep.sum() >= 3:
                tau_cc, _ = kendalltau(x[keep], y[keep])
            else:
                tau_cc = np.nan
            rows.append({'delta_e': de, 'comparateur': comp,
                         'tau_b_impute': tau_imp, 'tau_b_cas_complets': tau_cc,
                         'n_cas_complets': int(keep.sum()),
                         'ecart': (tau_imp - tau_cc) if not np.isnan(tau_cc) else np.nan})
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ R et G -----
def adaptation_and_evidence(df, error_mat, s_mat, palier_max=50):
    """D.1 : R par amplitude (courbe moyennee, mediane de tau_ARF) ; G par execution.

    Les deux ne se calculent pas au meme niveau : S_t est une grandeur continue definie
    sur un run isole, alors que e_t vaut 0 ou 1 et n'a de dynamique lisible qu'en
    moyenne inter-graines.

    Piege du palier : il s'estime sur une courte fenetre suivant la rupture, mais cette
    fenetre ne doit PAS empieter sur tau_ARF. A forte amplitude tau_ARF tombe sous 50,
    la foret a deja commence a se reparer, et un palier mesure sur 50 pas sous-estime
    le vrai saut — ce qui pousse R vers zero, voire dans le negatif. On borne donc la
    fenetre a la moitie de tau_ARF.
    """
    g = np.full(len(df), np.nan)
    smax = df['S_max_H'].to_numpy()
    tau = df['tau_arf'].to_numpy()
    ok = ~np.isnan(tau) & (smax > 0)
    idx = np.flatnonzero(ok)
    g[idx] = s_mat[idx, tau[idx].astype(int)] / smax[idx]
    df = df.copy()
    df['G_tau_arf'] = g

    rows = []
    for de, grp in df.groupby('delta_e', sort=True):
        runs = grp.index.to_numpy()
        e_mean = error_mat[runs].mean(axis=0)
        p0 = grp['p_hat_0'].mean()
        tau_med = np.nanmedian(grp['tau_arf'].to_numpy())
        if np.isnan(tau_med):
            continue
        wpal = int(max(5, min(palier_max, tau_med // 2)))
        e_post = e_mean[:wpal].mean()
        denom = e_post - p0
        r = (e_post - e_mean[int(tau_med)]) / denom if denom > 0 else np.nan
        rows.append({'delta_e': de, 'tau_arf_median': tau_med,
                     'fenetre_palier': wpal,
                     'e_palier': e_post, 'p_hat_0': p0,
                     'e_theorique': p0 + de,
                     'ecart_palier_theorie': e_post - (p0 + de),
                     'R_tau_arf': r,
                     'G_tau_arf_median': float(np.nanmedian(grp['G_tau_arf']))})
    return df, pd.DataFrame(rows)


def evidence_budget(df, error_mat, s_mat):
    """C.3 : A(H) mesuree contre la constante predite, et certificat en fenetre courte.

    L'aire sur la fenetre entiere est trompeuse : la foret continue d'apprendre bien
    apres s'etre reparee, et l'erreur peut finir SOUS le socle pre-rupture — l'aire
    brute devient alors negative sans que le budget de preuve reellement offert au
    detecteur ait diminue. D'ou la fenetre courte w = 3 x 18,5 / Delta_e, taillee sur
    le transitoire de l'amplitude consideree.

    Certificat (C.2) : par l'identite S_max = max_{k<=j} [A(k,j) - (j-k) delta_P],
    l'existence d'une sous-fenetre telle que A(k,j) >= lambda + (j-k) delta_P equivaut
    a S_max >= lambda. Evalue sur ]0, w], c'est une borne inferieure DEMONTREE du taux
    de detection sur l'horizon complet, puisque w <= H.
    """
    a, b = TAU_ARF_FIT
    p0 = df['p_hat_0'].to_numpy()
    rows = []
    for de, grp in df.groupby('delta_e', sort=True):
        runs = grp.index.to_numpy()
        w = int(min(H, max(1, round(3 * a / de))))
        a_w = (error_mat[runs, :w] - p0[runs, None]).sum(axis=1)
        smax_w = s_mat[runs, :w].max(axis=1)
        pred = a * de ** (1 + b)
        row = {'delta_e': de, 'w_fenetre_courte': w,
               'A_H_mesure_median': float(np.nanmedian(grp['A_H'])),
               'A_w_mesure_median': float(np.median(a_w)),
               'A_predit_brut': pred,
               'A_predit_utilisable': pred * (de - DELTA_P) / de,
               'part_prelevee_par_delta_P': 1 - (de - DELTA_P) / de}
        for lam in LAMBDAS:
            li = int(lam)
            row[f'certificat_court_l{li}'] = float(np.mean(smax_w >= lam))
            row[f'detection_observee_H_l{li}'] = float(1 - grp[f'censored_det_{li}'].mean())
            row[f'seuil_fenetre_entiere_l{li}'] = lam + H * DELTA_P
        rows.append(row)
    return pd.DataFrame(rows)


def tau_err_table(df, error_mat, rho=RHO_ERR, persist=PERSIST):
    """C.1c : tau_err(rho) confronte a la mediane inter-graines de tau_ARF.

    tau_err ne se calcule QUE sur la courbe moyennee inter-graines : sur une execution
    isolee, e_t vaut 0 ou 1 et la question n'a pas de sens. Meme moyennee, la courbe
    garde un bruit d'ecart-type sigma ~ sqrt(p(1-p)/n) ; le seuil rho*Delta_e n'est
    donc lisible que s'il domine ce bruit, et un PREMIER franchissement reste biaise
    vers le bas par simple fluctuation. D'ou l'exigence de persistance : la condition
    doit tenir `persist` pas consecutifs.
    """
    rows = []
    for de, grp in df.groupby('delta_e', sort=True):
        runs = grp.index.to_numpy()
        e_mean = error_mat[runs].mean(axis=0)
        p0 = grp['p_hat_0'].mean()
        sigma = float(e_mean[-500:].std())
        tau_med = np.nanmedian(grp['tau_arf'].to_numpy())
        row = {'delta_e': de, 'tau_arf_median': tau_med, 'rho': rho,
               'seuil': rho * de, 'sigma_courbe': sigma,
               'interpretable': rho * de > 2 * sigma}
        ok = (e_mean - p0) <= rho * de
        for pz in (1, persist):
            if pz <= 1:
                hit = np.flatnonzero(ok)
            else:
                conv = np.convolve(ok.astype(int), np.ones(pz, int), 'valid')
                hit = np.flatnonzero(conv == pz)
            val = float(hit[0]) if hit.size else np.nan
            row[f'tau_err_p{pz}'] = val
            row[f'avant_tau_arf_p{pz}'] = (not np.isnan(val)) and val < tau_med
        rows.append(row)
    return pd.DataFrame(rows)


def figure_pouvoir_tauerr(df, error_mat, terr, tag):
    """Complement visuel a tau_err_table (C.1c) : trace la bande de bruit +-2 sigma
    de la courbe moyenne contre le seuil rho*Delta_e, sur les amplitudes marquees
    non interpretables (seuil <= 2 sigma). Objectif : montrer que le choc y est
    noye dans le bruit plutot que de se contenter de l'affirmer en mots.
    """
    bad = terr.loc[~terr['interpretable'], 'delta_e'].to_numpy()
    if bad.size == 0:
        return None
    fig, axes = plt.subplots(1, len(bad), figsize=(5.5 * len(bad), 4.3), sharey=True)
    axes = np.atleast_1d(axes)
    for ax, de in zip(axes, bad):
        grp = df[df['delta_e'] == de]
        runs = grp.index.to_numpy()
        mat = error_mat[runs]
        mean_curve = mat.mean(axis=0)
        n = mat.shape[0]
        se = np.sqrt(mean_curve * (1 - mean_curve) / n)
        p0 = grp['p_hat_0'].mean()
        thresh = p0 + RHO_ERR * de
        t = np.arange(len(mean_curve))
        ax.plot(t, mean_curve, color='#04617B', lw=1.3, label=r"$\bar e_t$ (mean over seeds)")
        ax.fill_between(t, mean_curve - 2 * se, mean_curve + 2 * se, color='#04617B',
                        alpha=0.2, label=r"$\pm 2\sigma$ band")
        ax.axhline(p0, color='#555', ls=':', lw=1.1, label=r"baseline $\hat p_0$")
        ax.axhline(thresh, color='#C62828', ls='--', lw=1.3,
                   label=r"threshold $\hat p_0 + \rho\Delta e$")
        ax.set_title(rf"$\Delta e = {de:.3f}$")
        ax.set_xlabel("post-drift step")
        ax.set_xlim(0, 400)
    axes[0].set_ylabel("error rate")
    axes[0].legend(fontsize=8, loc='upper right')
    fig.suptitle("Why the recovery test lacks power at these amplitudes", fontsize=11)
    fig.tight_layout()
    out = FIGURES_DIR / f"Fig_QC_tauerr_power_{tag}.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


def figure_signal_bruit_tauerr(terr, tag):
    """Vue d'ensemble complementaire a figure_pouvoir_tauerr : plutot que de zoomer
    sur 2 amplitudes, trace le seuil rho*Delta_e (signal) contre 2*sigma (bruit) sur
    toute la grille -- montre en un coup d'oeil ou et pourquoi le critere
    d'interpretabilite (seuil > 2 sigma) bascule. Aucune resimulation necessaire,
    tout vient de tau_err_table.
    """
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    ax.plot(terr['delta_e'], terr['seuil'], 'o-', color='#C62828', lw=1.8, ms=4,
            label=r"threshold $\rho\Delta e$ (signal)")
    ax.plot(terr['delta_e'], 2 * terr['sigma_courbe'], 'o-', color='#04617B', lw=1.8,
            ms=4, label=r"$2\sigma$ (noise floor)")
    bad = terr[~terr['interpretable']]
    ax.scatter(bad['delta_e'], bad['seuil'], s=140, facecolors='none',
               edgecolors='#C62828', linewidths=1.8, zorder=5,
               label="non-interpretable (signal < noise)")
    ax.set_xlabel(r"$\Delta e$ — error jump amplitude")
    ax.set_ylabel("magnitude")
    ax.set_title("Signal vs. noise floor for the recovery test, across the full grid")
    ax.legend(fontsize=9)
    ax.grid(alpha=0.18, lw=0.6)
    fig.tight_layout()
    out = FIGURES_DIR / f"Fig_QC_tauerr_signal_bruit_{tag}.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


def fit_diagnosis(df, budget):
    """C.3f : l'ecart entre budget mesure et budget predit vient-il du socle, de la
    censure, ou de l'ajustement 18,5 * Delta_e^-0,98 lui-meme ?

    Le test discriminant : comparer tau_ARF mesure a sa prediction. Si le modele
    E[A] = Delta_e * E[tau_ARF] tient mais que la prediction de tau_ARF est fausse,
    l'ecart est imputable a l'ajustement, pas au dispositif de mesure.
    """
    a, b = TAU_ARF_FIT
    rows = []
    for de, grp in df.groupby('delta_e', sort=True):
        tau_med = np.nanmedian(grp['tau_arf'].to_numpy())
        pred_tau = a * de ** b
        aw = float(budget.loc[budget.delta_e == de, 'A_w_mesure_median'].iloc[0])
        rows.append({'delta_e': de,
                     'tau_arf_median': tau_med,
                     'tau_arf_predit': pred_tau,
                     'ratio_mesure_predit': tau_med / pred_tau,
                     'A_w_mesure': aw,
                     'budget_recalcule': de * tau_med,
                     'A_predit_brut': a * de ** (1 + b)})
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ figures ----
def figure_joint(df, error_mat, s_mat, phi_mat, target_de, tag, terr=None,
                 amplitudes=None):
    """Figure D.1 : les trois grandeurs sur un axe temporel commun, avec les
    quatre marqueurs temporels, sur PLUSIEURS amplitudes.

    Trois panneaux plutot qu'un seul axe partage : N_t/M vit sur [0,1], l'erreur
    autour du socle, et S_t sur l'echelle des lambda. Les superposer ecraserait
    l'erreur, qui est justement la grandeur que le detecteur consomme.

    Quatre marqueurs, comme l'exige ROADMAP.md section 3 :
        tau_det   premiere alarme du detecteur externe. Trace a lambda = 8, le
                  seul seuil ou la censure reste minoritaire (4,7 % contre
                  61,1 % a lambda = 25 et 99,95 % a lambda = 50) : a lambda = 25
                  ou 50 la mediane serait calculee sur une minorite de runs et
                  ne se publie pas (JOURNAL.md section 9.5).
        tau_ARF   premier remplacement d'arbre.
        tau_50%   instant ou la moitie des arbres a ete renouvelee.
        tau_rec   retour de l'erreur moyenne sous p_hat_0 + rho*Delta_e, avec la
                  condition de persistance de 20 pas (colonne tau_err_p20). Sans
                  cette persistance, le franchissement est un artefact de bruit
                  (JOURNAL.md section 4).

    Plusieurs amplitudes plutot qu'une seule : JOURNAL.md section 4 pose la
    regle qu'une relation verifiee a une amplitude se verifie sur toute la
    grille. Une figure a une amplitude a deja produit une conclusion fausse en
    C.3.

    Aucun lissage temporel : e_t est binaire, seule la moyenne inter-graines
    est prise, a chaque pas. Un filtre glissant decalerait la courbe d'un
    demi-support et detruirait la synchronisation avec tau*.
    """
    de_vals = np.sort(df['delta_e'].unique())
    if amplitudes is None:
        # Bas, milieu et haut de grille, repartis sur l'ETENDUE de Delta_e et
        # non sur l'index : la grille est lineaire en boundary_shift, donc
        # resserree en Delta_e vers le haut. Cibles fixees avant lecture des
        # courbes.
        cibles = [de_vals[1],
                  0.5 * (de_vals[1] + de_vals[-1]),
                  de_vals[-1]]
        amplitudes = [de_vals[np.argmin(np.abs(de_vals - c))] for c in cibles]
    else:
        amplitudes = [de_vals[np.argmin(np.abs(de_vals - a))] for a in amplitudes]

    t_axis = np.arange(H)
    n_col = len(amplitudes)
    fig, axes = plt.subplots(3, n_col, figsize=(5.2 * n_col, 9.4),
                             sharex=True, squeeze=False)

    lam_marqueur = min(LAMBDAS)          # lambda = 8, censure minoritaire
    couleurs = {'det': '#2E7D32', 'arf': '#04617B',
                'swap50': '#6A3D9A', 'rec': '#C62828'}

    for j, de in enumerate(amplitudes):
        runs = df.index[df['delta_e'] == de].to_numpy()

        phi = phi_mat[runs]
        phi_med = np.median(phi, axis=0)
        phi_q1, phi_q3 = np.percentile(phi, [25, 75], axis=0)
        e_mean = error_mat[runs].mean(axis=0)
        p0 = df.loc[runs, 'p_hat_0'].mean()
        s_med = np.median(s_mat[runs], axis=0)
        s_q1, s_q3 = np.percentile(s_mat[runs], [25, 75], axis=0)

        # --- les quatre marqueurs -----------------------------------------
        # Chaque entree est (valeur, etiquette, fiable). `fiable = False` trace
        # le marqueur en pointille et le dit dans l'etiquette, plutot que de le
        # taire ou de le publier comme les autres.
        marqueurs = {}
        col_det = f'censored_det_{int(lam_marqueur)}'
        part_censuree = float(df.loc[runs, col_det].mean())
        if part_censuree <= 0.5:
            marqueurs['det'] = (
                np.nanmedian(df.loc[runs, f'tau_det_{int(lam_marqueur)}'].to_numpy()),
                rf"$\tau_{{\mathrm{{det}}}}$ ($\lambda={int(lam_marqueur)}$)", True)
        marqueurs['arf'] = (np.nanmedian(df.loc[runs, 'tau_arf'].to_numpy()),
                            r"$\tau_{\mathrm{ARF}}$", True)
        part_c50 = float(df.loc[runs, 'censored_swap_50'].mean())
        if part_c50 <= 0.5:
            marqueurs['swap50'] = (
                np.nanmedian(df.loc[runs, 'tau_swap_50'].to_numpy()),
                r"$\tau_{50\%}$", True)
        if terr is not None:
            ligne = terr.loc[np.isclose(terr['delta_e'], de, atol=1e-9)]
            if len(ligne) and np.isfinite(ligne['tau_err_p20'].iloc[0]):
                # tau_rec n'a de sens que la ou le test a la puissance de
                # trancher (rho*Delta_e > 2*sigma). Aux amplitudes declarees
                # non interpretables, le marqueur est trace en pointille et
                # son etiquette le dit : le publier sans mention reviendrait a
                # dater une resorption sur une courbe ou le seuil est sous le
                # bruit. Meme convention que figure_signal_bruit_tauerr.
                interpretable = bool(ligne['interpretable'].iloc[0])
                etiquette = (r"$\tau_{\mathrm{rec}}$" if interpretable
                             else r"$\tau_{\mathrm{rec}}$ (not interpretable)")
                marqueurs['rec'] = (float(ligne['tau_err_p20'].iloc[0]),
                                    etiquette, interpretable)

        # --- panneau 1 : fraction d'arbres remplaces -----------------------
        ax = axes[0][j]
        ax.plot(t_axis, phi_med, color='#04617b', lw=1.6,
                label="inter-seed median")
        ax.fill_between(t_axis, phi_q1, phi_q3, color='#04617b', alpha=0.18,
                        label="interquartile range")
        ax.set_ylim(0, 1.02)
        ax.set_title(rf"$\Delta e = {de:.3f}$, {len(runs)} seeds, $H = {H}$",
                     fontsize=10)
        if j == 0:
            ax.set_ylabel(r"$N_t / M$")
            ax.legend(fontsize=7, loc='lower right')

        # --- panneau 2 : erreur globale ------------------------------------
        ax = axes[1][j]
        ax.plot(t_axis, e_mean, color='#C62828', lw=0.8,
                label=r"$\bar{e}_t$ (inter-seed mean, no smoothing)")
        ax.axhline(p0, color='#555', ls=':', lw=1.2,
                   label=r"baseline $\hat{p}_0$")
        ax.axhline(p0 + de, color='#555', ls='--', lw=1.0,
                   label=r"theoretical plateau $\hat{p}_0 + \Delta e$")
        if j == 0:
            ax.set_ylabel(r"$\bar{e}_t$")
            ax.legend(fontsize=7, loc='upper right')

        # --- panneau 3 : etat interne du detecteur -------------------------
        ax = axes[2][j]
        ax.plot(t_axis, s_med, color='#E8A000', lw=1.6,
                label=r"$S_t$ (inter-seed median)")
        ax.fill_between(t_axis, s_q1, s_q3, color='#E8A000', alpha=0.18,
                        label="interquartile range")
        for lam, ls in zip(LAMBDAS, ('-', '--', ':')):
            ax.axhline(lam, color='#2E7D32', ls=ls, lw=1.0,
                       label=rf"$\lambda = {int(lam)}$")
        ax.set_ylim(0, max(max(LAMBDAS), float(s_q3.max())) * 1.1)
        ax.set_xlabel(r"steps after the drift ($t - \tau^*$), log scale")
        if j == 0:
            ax.set_ylabel(r"$S_t$")
            ax.legend(fontsize=7, loc='upper right', ncol=2)

        # --- les marqueurs sur les trois panneaux --------------------------
        # Axe temporel en echelle logarithmique : les quatre instants
        # s'etalent sur deux ordres de grandeur d'une amplitude a l'autre
        # (tau_ARF vaut 346 pas a Delta_e = 0,085 et 28 en haut de grille).
        # En echelle lineaire, les quatre marqueurs du haut de grille se
        # superposent dans les cinquante premiers pixels et la figure ne se
        # lit plus. L'axe reste commun aux trois colonnes, ce qu'exige
        # l'enonce.
        ordonnees = np.linspace(0.94, 0.60, len(marqueurs))
        for (cle, (val, etiquette, fiable)), y_lab in zip(marqueurs.items(),
                                                          ordonnees):
            if val is None or not np.isfinite(val):
                continue
            style = '-' if fiable else (0, (2, 2))
            for ax in (axes[0][j], axes[1][j], axes[2][j]):
                ax.axvline(max(val, 1.0), color=couleurs[cle], lw=1.1,
                           alpha=0.8 if fiable else 0.55, ls=style)
            axes[0][j].annotate(
                etiquette, xy=(max(val, 1.0), y_lab),
                xycoords=('data', 'axes fraction'),
                fontsize=7.5, color=couleurs[cle], ha='left', va='center',
                alpha=1.0 if fiable else 0.7,
                xytext=(3, 0), textcoords='offset points')

        for ax in (axes[0][j], axes[1][j], axes[2][j]):
            ax.set_xscale('log')
            ax.set_xlim(1, H)

    fig.suptitle("Question D.1 — replacement, error and detector on a common "
                 "time axis", fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    out = FIGURES_DIR / f"Fig_QD_trajectoires_{tag}.png"
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return out


def figure_dispersion_swap(df, tag, quantiles=(25, 50, 75)):
    """C.1a : nuage tau_ARF vs tau_swap(q) sur tous les runs, une couleur par
    censure. Montre la dispersion individuelle (invisible dans figure_ecarts, qui ne
    trace que la mediane) et confirme visuellement l'inegalite deterministe -- tous
    les points au-dessus de la diagonale, sur les 2000 runs, pas seulement en moyenne.
    """
    fig, axes = plt.subplots(1, len(quantiles), figsize=(4.3 * len(quantiles), 4.3),
                             sharex=True, sharey=True)
    axes = np.atleast_1d(axes)
    lim = H
    for ax, q in zip(axes, quantiles):
        col = f'tau_swap_{q}'
        cens = df[f'censored_swap_{q}']
        ax.scatter(df.loc[~cens, 'tau_arf'], df.loc[~cens, col], s=8, alpha=0.35,
                  color='#04617B', label='uncensored')
        if cens.any():
            ax.scatter(df.loc[cens, 'tau_arf'], np.full(cens.sum(), lim), s=10,
                      alpha=0.3, color='#C62828', marker='^',
                      label='censored (quota never reached)')
        ax.plot([0, lim], [0, lim], 'k--', lw=1, alpha=0.6)
        ax.set_title(f"q = {q}%")
        ax.set_xlabel(r"$\tau_{ARF}$")
    axes[0].set_ylabel(r"$\tau_{swap}(q)$")
    axes[0].legend(fontsize=8, loc='lower right')
    fig.suptitle(r"$\tau_{ARF}$ vs. $\tau_{swap}(q)$ on every run --- dashed line: equality",
                fontsize=11)
    fig.tight_layout()
    out = FIGURES_DIR / f"Fig_QC_dispersion_swap_{tag}.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


def figure_ecarts(df, tag):
    """C.1b : l'ecart tau_swap(q) - tau_ARF en fonction de Delta_e."""
    fig, ax = plt.subplots(figsize=(9, 5.2))
    colors = ['#04617B', '#2E7D32', '#B97C00', '#C62828']
    for q, c in zip(SWAP_QUANTILES, colors):
        col = f'tau_swap_{int(q * 100)}'
        g = df.groupby('delta_e')
        med = g.apply(lambda x: np.nanmedian(x[col] - x['tau_arf']), include_groups=False)
        cens = g[f'censored_swap_{int(q * 100)}'].mean()
        # une seule ligne continue -- eviter de tracer les points tres censures
        # comme un second segment separe, qui se retrouve alors deconnecte du
        # reste de la courbe (defaut visuel corrige le 08/09).
        ax.plot(med.index, med.values, 'o-', color=c, lw=1.8, ms=4,
                label=rf"$q = {q:.2f}$")
        heavy = cens > 0.5
        if heavy.any():
            ax.plot(med.index[heavy], med[heavy], 'o', color=c, ms=9,
                    markerfacecolor='none', markeredgewidth=1.8, alpha=0.9)
    ax.set_xlabel(r"$\Delta e$ — error jump amplitude")
    ax.set_ylabel(r"$\tau_{swap}(q) - \tau_{ARF}$  (steps)")
    ax.set_title(r"C.1b --- how far ahead of stricter quotas $\tau_{ARF}$ runs")
    ax.legend(fontsize=9, title="fraction of trees renewed", title_fontsize=8)
    ax.grid(alpha=0.18, lw=0.6)
    ax.text(0.98, 0.95, "hollow circle: >50% of runs censored at this amplitude",
            transform=ax.transAxes, ha='right', va='top', fontsize=7.5, color='#6A848D')
    fig.tight_layout()
    out = FIGURES_DIR / f"Fig_QC_ecarts_{tag}.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


def figure_budget(budget, tag):
    """C.3f : A(H) et A(w) mesurees contre la constante predite."""
    fig, ax = plt.subplots(figsize=(9, 5.2))
    de = budget['delta_e'].to_numpy()
    ax.axhline(0, color='#6A848D', lw=0.8)
    ax.plot(de, budget['A_predit_brut'], '--', color='#0F252D', lw=1.6,
            label=r"predicted: $18.5 \cdot \Delta e^{0.02}$")
    ax.plot(de, budget['A_w_mesure_median'], 'o-', color='#04617B', lw=1.8, ms=4,
            label=r"measured, short window $A(w)$")
    ax.plot(de, budget['A_H_mesure_median'], 's-', color='#C62828', lw=1.8, ms=4,
            label=r"measured, full horizon $A(H)$")
    ax.fill_between(de, budget['A_H_mesure_median'], 0,
                    where=budget['A_H_mesure_median'] < 0,
                    color='#C62828', alpha=0.12)
    ax.set_xlabel(r"$\Delta e$ — error jump amplitude")
    ax.set_ylabel("excess error area")
    ax.set_title(r"C.3f --- evidence budget: measured vs.\ predicted")
    ax.legend(fontsize=9)
    ax.grid(alpha=0.18, lw=0.6)
    fig.tight_layout()
    out = FIGURES_DIR / f"Fig_QC_budget_{tag}.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


def figure_rg(rg, tag):
    """D.1 : R et G en fonction de Delta_e."""
    fig, ax = plt.subplots(figsize=(9, 5.2))
    ax.plot(rg['delta_e'], rg['R_tau_arf'], 'o-', color='#C62828', lw=1.8, ms=4,
            label=r"$R(\tau_{\mathrm{ARF}})$ — fraction of adaptation already acquired")
    ax.plot(rg['delta_e'], rg['G_tau_arf_median'], 's-', color='#E8A000', lw=1.8, ms=4,
            label=r"$G(\tau_{\mathrm{ARF}})$ — fraction of evidence accumulated")
    ax.axhline(0, color='#6A848D', lw=0.8)
    ax.axhline(1, color='#6A848D', lw=0.8, ls=':')
    ax.set_xlabel(r"$\Delta e$ — error jump amplitude")
    ax.set_ylabel("fraction")
    ax.set_ylim(-0.3, 1.05)
    ax.set_title(r"D.1 — what is acquired at time $\tau_{\mathrm{ARF}}$")
    ax.legend(fontsize=9)
    ax.grid(alpha=0.18, lw=0.6)
    fig.tight_layout()
    out = FIGURES_DIR / f"Fig_QD_R_et_G_{tag}.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


def figure_heatmap(corr, comparators, tag):
    """Tous les coefficients publies, sans selection a posteriori (D.3).

    Les cellules tautologiques sont hachurees : a M = 10, tau_swap(10 %) EST
    tau_ARF (C.1 a), donc son tau_b vaut 1 par identite et non par performance.
    Le precedent est celui de S_max(H) en B2 (JOURNAL.md section 8).
    """
    piv = corr.pivot(index='comparateur', columns='delta_e', values='tau_b')
    piv = piv.reindex(comparators)
    fig, ax = plt.subplots(figsize=(max(8, 0.5 * piv.shape[1] + 4), 3.6))
    im = ax.imshow(piv.to_numpy(), aspect='auto', cmap='RdBu_r', vmin=-1, vmax=1)

    tautologiques = {f'tau_swap_{int(100 / N_MODELS)}'}
    for i, nom in enumerate(piv.index):
        if nom in tautologiques:
            for j in range(piv.shape[1]):
                ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1,
                                           fill=False, hatch='///',
                                           edgecolor='k', lw=0.0, alpha=0.55))
    ax.set_xticks(range(piv.shape[1]))
    ax.set_xticklabels([f"{v:.3f}" for v in piv.columns], rotation=90, fontsize=7)
    ax.set_yticks(range(piv.shape[0]))
    ax.set_yticklabels(piv.index, fontsize=8)
    ax.set_xlabel(r"$\Delta e$")
    ax.set_title(r"$\tau_b(\tau_{\mathrm{ARF}}, \cdot)$ by amplitude — every "
                 r"coefficient published"
                 "\n" r"hatched: tautological ($\tau_{\mathrm{swap}}(10\%) "
                 r"\equiv \tau_{\mathrm{ARF}}$ at $M=10$)", fontsize=10)
    fig.colorbar(im, ax=ax, label=r"$\tau_b$")
    fig.tight_layout()
    out = FIGURES_DIR / f"Fig_QD_heatmap_taub_{tag}.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


# --------------------------------------------------------------------- main ----
def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--tag', default='proto')
    ap.add_argument('--boot', type=int, default=N_BOOT)
    ap.add_argument('--self-check', action='store_true',
                    help="verifie la reconstruction de S_t, sans lire de campagne")
    ap.add_argument('--figure-de', type=float, default=0.21,
                    help="amplitude visee pour la figure D")
    args = ap.parse_args()

    graine_bootstrap = 12345
    rng = np.random.default_rng(graine_bootstrap)

    worst = self_check(rng)
    status = "OK" if worst < 1e-9 else "ECHEC"
    print(f"[CONTROLE] forme close vs recurrence : ecart max = {worst:.2e} -> {status}")
    if worst >= 1e-9:
        raise SystemExit("reconstruction de S_t invalide, rien de ce qui suit n'aurait de sens")
    if args.self_check:
        return

    meta, error_mat, events = load_campaign(args.tag)
    print(f"[INFO] {len(meta)} executions, {len(events):,} evenements de remplacement")

    df, s_mat = build_indicators(meta, error_mat, events)
    phi_mat = phi_matrix(events, len(meta))
    df, rg = adaptation_and_evidence(df, error_mat, s_mat)
    budget = evidence_budget(df, error_mat, s_mat)
    terr = tau_err_table(df, error_mat)
    fitdiag = fit_diagnosis(df, budget)
    corr, comparators = stratified_correlations(df, rng, args.boot)
    glob = global_correlations(df, comparators)
    cc = complete_cases_comparison(df, comparators)

    # `experimentation.md` : une colonne par parametre de grille, et la graine
    # DANS la table. M ne venait jusqu'ici que du defaut d'exp_QCD_campagne, et
    # la graine du bootstrap n'etait ecrite nulle part : une ligne qui ne les
    # porte pas n'est pas rejouable.
    for name, frame in (('indicateurs', df), ('correlations_stratifiees', corr),
                        ('correlation_globale', glob), ('cas_complets', cc),
                        ('budget_preuve', budget), ('R_et_G', rg),
                        ('tau_err', terr), ('diagnostic_ajustement', fitdiag)):
        frame = frame.copy()
        frame['n_models'] = N_MODELS
        frame['delta_P'] = DELTA_P
        if name in ('correlations_stratifiees', 'correlation_globale',
                    'cas_complets'):
            frame['graine_bootstrap'] = graine_bootstrap
            frame['n_boot'] = args.boot
        frame.to_parquet(DATA_DIR / f"QCD_{name}_{args.tag}.parquet", index=False)

    f1 = figure_joint(df, error_mat, s_mat, phi_mat, args.figure_de, args.tag,
                      terr=terr)
    f2 = figure_heatmap(corr, comparators, args.tag)
    f3 = figure_ecarts(df, args.tag)
    f3b = figure_dispersion_swap(df, args.tag)
    f4 = figure_budget(budget, args.tag)
    f5 = figure_rg(rg, args.tag)
    f6 = figure_pouvoir_tauerr(df, error_mat, terr, args.tag)
    f7 = figure_signal_bruit_tauerr(terr, args.tag)

    print("\n[CENSURE] par seuil, toutes amplitudes confondues :")
    for lam in LAMBDAS:
        print(f"  lambda = {int(lam):2d} : tau_det censure a "
              f"{100 * df[f'censored_det_{int(lam)}'].mean():5.1f} %")
    print(f"  tau_ARF censure a {100 * df['censored_arf'].mean():5.1f} %")

    print("\n[BUDGET] A(H) mesuree vs predite (invariance attendue, C.3) :")
    cols = ['delta_e', 'w_fenetre_courte', 'A_H_mesure_median', 'A_w_mesure_median',
            'A_predit_brut', 'part_prelevee_par_delta_P']
    print(budget[cols].to_string(index=False, float_format=lambda v: f"{v:8.3f}"))
    print("\n[CERTIFICAT] fenetre courte ]0,w] : borne inferieure DEMONTREE du taux de "
          "detection, vs detection observee sur H :")
    cert_cols = ['delta_e', 'w_fenetre_courte'] + [
        c for lam in LAMBDAS for c in (f'certificat_court_l{int(lam)}',
                                       f'detection_observee_H_l{int(lam)}')]
    print(budget[cert_cols].to_string(index=False, float_format=lambda v: f"{v:7.3f}"))

    n = int(corr['n'].iloc[0])
    sigma, thr = tau_b_threshold(n)
    print(f"\n[SEUIL] n = {n} graines -> sigma(tau_b) = {sigma:.3f} ; "
          f"|tau_b| <= {thr:.3f} n'est pas discernable de zero")
    dom = corr[corr['dans_domaine_decision']]
    print(f"[CORR] {int(dom['discernable'].sum())} / {len(dom)} coefficients discernables "
          f"dans le domaine Delta_e >= {DELTA_E_MIN_DECISION}")
    print("\n[GLOBAL] effondrement par agregation (a expliquer via C.3, pas a publier seul) :")
    print(glob.to_string(index=False, float_format=lambda v: f"{v:7.3f}"))

    ok = terr[terr['interpretable']]
    print(f"\n[C.1c] tau_err(rho={RHO_ERR}) : {len(ok)}/{len(terr)} amplitudes interpretables "
          f"(seuil > 2 sigma)")
    print(f"  resorption AVANT le 1er remplacement — sans persistance : "
          f"{int(ok['avant_tau_arf_p1'].sum())}/{len(ok)} amplitudes ; "
          f"avec {PERSIST} pas de persistance : {int(ok[f'avant_tau_arf_p{PERSIST}'].sum())}/{len(ok)}")

    print("\n[C.3f] l'ajustement 18,5*de^-0,98 tient-il ? (ratio mesure/predit)")
    fd = fitdiag[['delta_e', 'tau_arf_median', 'tau_arf_predit', 'ratio_mesure_predit',
                  'A_w_mesure', 'budget_recalcule']]
    print(fd.to_string(index=False, float_format=lambda v: f"{v:8.2f}"))

    print("\n[D.1] R et G a l'instant tau_ARF (mediane par amplitude) :")
    print(rg[['delta_e', 'tau_arf_median', 'fenetre_palier', 'e_palier', 'e_theorique',
              'ecart_palier_theorie', 'R_tau_arf', 'G_tau_arf_median']].iloc[::3].to_string(
        index=False, float_format=lambda v: f"{v:8.3f}"))

    print(f"\n[SUCCESS] figures : {f1.name}, {f2.name}, {f3.name}, {f4.name}, {f5.name}")
    print(f"[SUCCESS] tables ecrites dans {DATA_DIR} (tag = {args.tag})")


if __name__ == "__main__":
    main()
