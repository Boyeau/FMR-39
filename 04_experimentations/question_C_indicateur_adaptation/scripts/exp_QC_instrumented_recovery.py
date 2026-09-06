"""
exp_QC_instrumented_recovery.py
=================================================
Instrumentation de l'ARF pour les Questions C et D du Sujet 39
(le paradoxe du point aveugle).

Part de exp_R2_instrumented_blind_spot.py (dépôt officiel) mais :
- ne s'arrête plus dès que tau_ARF et tau_det sont trouvés (pas de `break`
  anticipé) ;
- observe une fenêtre post-drift tronquée (POST_HORIZON pas, au lieu des
  ~4000 du script original) ;
- calcule les 4 indicateurs définis dans le document du prof
  (Business_case_Filiere_Recherche_Blind_Spot_FIN.md) :
    tau_ARF, tau_swap(q), A(H), S_max(H)
  au lieu de seulement tau_ARF/tau_det.

Voir le README du dossier pour le détail des définitions, le piège API
sur `_drift_tracker` (stock vs flux), et pourquoi Kendall tau-b (pas
Spearman/Pearson) pour la corrélation.
"""

import time
import warnings
import random
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
from joblib import Parallel, delayed
from tqdm import tqdm
from scipy.stats import norm, kendalltau
from river import drift
from river.forest import ARFClassifier

warnings.filterwarnings('ignore')

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "resultats" / "data"
FIGURES_DIR = ROOT_DIR / "resultats" / "figures"
DATA_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

N_MODELS = 10
T_DRIFT = 4000
POST_HORIZON = 1000          # fenêtre post-drift tronquée (largement suffisant pour H=500, cf. README)
BASELINE_WINDOW = 1000        # pas pré-drift utilisés pour estimer p_pre_empirical (identique à R2)
SWAP_QUANTILES = [0.10, 0.25, 0.50, 0.75]
WINDOWS_H = [50, 100, 200, 500]

CFG = {"id": "A_PHT_ARF", "c_int": 1, "lambda": 50.0}   # scénario du "vrai" point aveugle (Fig. 2A de l'article)


class StrictCUSUM:
    def __init__(self, p_pre, delta, threshold):
        self.S = 0.0
        self.p_pre = p_pre
        self.delta = delta
        self.threshold = threshold
        self.drift_detected = False

    def update(self, x):
        self.S = max(0.0, self.S + (x - self.p_pre) - self.delta)
        if self.S >= self.threshold:
            self.drift_detected = True


def run_one(boundary_shift, seed, cfg=CFG, keep_traces=False):
    """Rejoue une simulation ARF vs PHT et calcule les indicateurs Q C/D pour ce run."""
    safe_seed = int(seed % (2**31 - 1))
    random.seed(safe_seed)
    np.random.seed(safe_seed)
    rng = np.random.default_rng(safe_seed)

    arf = ARFClassifier(
        n_models=N_MODELS, seed=safe_seed,
        drift_detector=drift.ADWIN(clock=cfg['c_int']),
        warning_detector=drift.ADWIN(clock=cfg['c_int']),
    )

    errors_pre = []
    ext_pht = None
    p_pre_empirical = None
    tau_det = np.nan
    baseline_counts = {}

    error_series = np.full(POST_HORIZON, np.nan)
    phi_series = np.full(POST_HORIZON, np.nan)   # fraction d'arbres DISTINCTS remplacés DEPUIS le drift
    s_series = np.full(POST_HORIZON, np.nan)      # état interne du détecteur (S du CUSUM)

    total_steps = T_DRIFT + POST_HORIZON
    for t in range(total_steps):
        x0, x1 = rng.normal(), rng.normal()
        x_dict = {0: x0, 1: x1}
        y = int(x0 + x1 > 0.0) if t < T_DRIFT else int(x0 + x1 > boundary_shift)

        y_pred = arf.predict_one(x_dict) or 0
        error = float(y_pred != y)

        if t < T_DRIFT:
            if t >= T_DRIFT - BASELINE_WINDOW:
                errors_pre.append(error)
        elif t == T_DRIFT:
            p_pre_empirical = np.mean(errors_pre) if errors_pre else 0.05
            ext_pht = StrictCUSUM(p_pre=p_pre_empirical, delta=0.01, threshold=cfg['lambda'])
            # Piège API (cf. README) : _drift_tracker est un stock cumulé DEPUIS t=0.
            # Avec ADWIN(clock=1) hyper-réactif, tous les arbres ont déjà été
            # remplacés plusieurs fois pendant le warmup pré-drift, par simple
            # bruit — sans baseline, phi(t) serait déjà saturé à 100% avant
            # même le drift. On fige donc l'état juste avant le drift, et on ne
            # comptera ensuite que les arbres dont le compteur AUGMENTE par
            # rapport à cette référence (nouveaux remplacements post-drift).
            baseline_counts = dict(arf._drift_tracker)

        arf.learn_one(x_dict, y)

        if t >= T_DRIFT:
            idx = t - T_DRIFT
            distinct_swapped = sum(
                1 for tid, v in arf._drift_tracker.items() if v > baseline_counts.get(tid, 0)
            )
            phi = distinct_swapped / N_MODELS

            ext_pht.update(error)
            if np.isnan(tau_det) and ext_pht.drift_detected:
                tau_det = idx

            error_series[idx] = error
            phi_series[idx] = phi
            s_series[idx] = ext_pht.S

    swapped_mask = phi_series > 0
    tau_arf = float(np.argmax(swapped_mask)) if swapped_mask.any() else np.nan

    tau_swap = {}
    for q in SWAP_QUANTILES:
        reached = phi_series >= q
        tau_swap[q] = float(np.argmax(reached)) if reached.any() else np.nan

    A, Smax = {}, {}
    for H in WINDOWS_H:
        A[H] = float(np.sum(error_series[:H] - p_pre_empirical))
        Smax[H] = float(np.max(s_series[:H]))

    row = {
        'boundary_shift': boundary_shift,
        'seed': seed,
        'delta_e_theoretical': norm.cdf(boundary_shift / np.sqrt(2)) - 0.5,
        'tau_arf': tau_arf,
        'tau_arf_censored': bool(np.isnan(tau_arf)),
        'tau_det': tau_det,
        'p_pre_empirical': p_pre_empirical,
    }
    for q in SWAP_QUANTILES:
        row[f'tau_swap_{int(q * 100)}'] = tau_swap[q]
        row[f'tau_swap_{int(q * 100)}_censored'] = bool(np.isnan(tau_swap[q]))
    for H in WINDOWS_H:
        row[f'A_{H}'] = A[H]
        row[f'Smax_{H}'] = Smax[H]

    if keep_traces:
        row['_error_series'] = error_series
        row['_phi_series'] = phi_series
        row['_s_series'] = s_series

    return row


def kendall_censored(x, y, horizon=POST_HORIZON):
    """Kendall tau-b en attribuant aux valeurs censurées (NaN) le rang maximal (= horizon)."""
    x_filled = np.where(np.isnan(x), horizon, x)
    y_filled = np.where(np.isnan(y), horizon, y)
    tau, p = kendalltau(x_filled, y_filled)
    return tau, p


if __name__ == "__main__":
    import sys

    FULL = "--full" in sys.argv

    if FULL:
        # Grille complete : 21 valeurs de boundary_shift (meme convention que R2/prototype,
        # on ne force pas la grille Delta_e=[0.10,0.50] de R8, calibree pour un autre scenario)
        # x 200 graines = 4200 runs, comme demande dans le document du prof.
        print("[INFO] Grille complete : 21 amplitudes x 200 graines = 4200 runs")
        shifts = np.linspace(0.1, 4.0, 21)
        seeds = list(range(1, 201))
        out_name = "QC_full_summary.parquet"
    else:
        print("[INFO] Sous-grille de prototypage : 5 amplitudes x 20 graines = 100 runs")
        shifts = np.linspace(0.1, 4.0, 5)
        seeds = list(range(1, 21))
        out_name = "QC_prototype_summary.parquet"

    t0 = time.time()
    grid = [(bs, s) for bs in shifts for s in seeds]
    results = Parallel(n_jobs=-1)(
        delayed(run_one)(bs, s) for bs, s in tqdm(grid, desc="Grille" if FULL else "Prototype")
    )
    elapsed = time.time() - t0
    df = pd.DataFrame(results)
    df.to_parquet(DATA_DIR / out_name, index=False)
    per_run = elapsed / len(grid)
    if FULL:
        print(f"[INFO] Grille complete terminee en {elapsed / 60:.1f} min ({per_run:.2f}s/run, {len(grid)} runs)")
    else:
        print(f"[INFO] Prototype termine en {elapsed:.1f}s ({per_run:.2f}s/run) "
              f"-> extrapolation grille complete (21x200=4200 runs): ~{per_run * 4200 / 60:.1f} min")

    print("\n[INFO] Correlations Kendall tau-b (sous-grille de prototypage, indicatif seulement) :")
    pairs = [
        ('tau_arf', 'tau_swap_50'),
        ('tau_arf', 'A_200'),
        ('tau_arf', 'Smax_200'),
    ]
    for col_x, col_y in pairs:
        x = df[col_x].to_numpy(dtype=float)
        y = df[col_y].to_numpy(dtype=float)
        tau, p = kendall_censored(x, y)
        censor_rate = np.mean(np.isnan(x))
        print(f"  tau-b({col_x}, {col_y}) = {tau:.3f} (p={p:.3g}), taux de censure {col_x} = {censor_rate:.1%}")

    print("\n[INFO] Run d'illustration (moyenne inter-graines) pour le graphique conjoint Q D...")
    illus_shift = 0.8
    illus_seeds = list(range(1, 31))
    traces = Parallel(n_jobs=-1)(
        delayed(run_one)(illus_shift, s, keep_traces=True) for s in tqdm(illus_seeds, desc="Illustration")
    )
    error_mat = np.array([r['_error_series'] for r in traces])
    phi_mat = np.array([r['_phi_series'] for r in traces])
    s_mat = np.array([r['_s_series'] for r in traces])

    illus_df = pd.DataFrame({
        't_post_drift': np.arange(POST_HORIZON),
        'error_mean_inter_graines': np.nanmean(error_mat, axis=0),
        'phi_mean': np.nanmean(phi_mat, axis=0),
        's_mean': np.nanmean(s_mat, axis=0),
    })
    illus_df.to_parquet(DATA_DIR / "QC_illustration_traces.parquet", index=False)

    fig, ax1 = plt.subplots(figsize=(9, 5))
    ax1.plot(illus_df['t_post_drift'], illus_df['phi_mean'], color='#04617b', label="Fraction d'arbres remplacés φ(t)")
    ax1.plot(illus_df['t_post_drift'], illus_df['error_mean_inter_graines'], color='#C62828', label="Erreur moyenne inter-graines")
    ax1.set_xlabel("Pas de temps post-drift")
    ax1.set_ylabel("Fraction / Erreur")
    ax2 = ax1.twinx()
    ax2.plot(illus_df['t_post_drift'], illus_df['s_mean'] / CFG['lambda'], color='#E8A000', linestyle='--', label="État détecteur S/λ")
    ax2.set_ylabel("État du détecteur (normalisé)")
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right', fontsize=9)
    ax1.set_title(f"Question D — 3 métriques conjointes (boundary_shift={illus_shift}, moyenne sur {len(illus_seeds)} graines)")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "Fig_QD_joint_metrics.png")
    plt.close()

    print("[SUCCESS] Prototype + illustration termines. Voir resultats/data/ et resultats/figures/.")
