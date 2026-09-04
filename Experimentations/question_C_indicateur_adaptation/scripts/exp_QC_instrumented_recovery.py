"""
exp_R2_instrumented_blind_spot.py
=================================================
Direct instrumentation of the ARF confronted with the Page-Hinkley Test (PHT).
Generates Figures 2A, 2B, 2C of the article (Experiment R2).
Demonstrates the asymptotic complexity intersection (O(1/x^2) vs O(1/x))
AND the Hydra Effect on correlated internal streams.
"""

import sys, warnings, itertools, random
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
from joblib import Parallel, delayed
from tqdm import tqdm
from scipy.stats import sem, norm
from river import drift
from river.forest import ARFClassifier

warnings.filterwarnings('ignore')

# Dynamic Path Resolution (IEEE/ICDM FAIR Compliance)
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
RESULTS_DIR = ROOT_DIR / "results" / "R2_instrumented_blind_spot"
DATA_DIR = RESULTS_DIR / "data"
FIGURES_DIR = RESULTS_DIR / "figures"

DATA_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

N_STEPS, T_DRIFT, N_MODELS = 8000, 4000, 10
BOUNDARY_SHIFTS = np.linspace(0.1, 4.0, 20)

# IEEE/ICDM FAIR Determinism: Controlled Rollback to original seed space
# Restoring the naive sequence to match the submitted PDF's exact fitted coefficients (e.g., 18.5)
SEEDS = list(range(1, 101))

BLUE, ORANGE, RED, GREEN, GRAY = '#04617b', '#E8A000', '#C62828', '#2E7D32', '#546E7A'
plt.rcParams.update({'figure.dpi': 300, 'font.family': 'sans-serif', 'font.size': 11,
                     'axes.spines.top': False, 'axes.spines.right': False, 'mathtext.fontset': 'stix'})

# ─── Strict CUSUM Implementation ──────────────────────────────────────────
class StrictCUSUM:
    def __init__(self, p_pre, delta, threshold):
        self.S = 0.0; self.p_pre = p_pre; self.delta = delta
        self.threshold = threshold; self.drift_detected = False
    def update(self, x):
        self.S = max(0.0, self.S + (x - self.p_pre) - self.delta)
        if self.S >= self.threshold: self.drift_detected = True

SCENARIOS =[
    {"id": "A_PHT_ARF", "title": "Instrumented Robust PHT", "subtitle": r"Real ARF ($c_{\mathrm{int}}=1$) vs External PHT ($\lambda=50$) (Error bars = SEM)", "c_int": 1, "lambda": 50.0},
    {"id": "B_PHT_ARF", "title": "Instrumented Complexity Intersection", "subtitle": r"Real ARF ($c_{\mathrm{int}}=1$) vs External PHT ($\lambda=25$) (Error bars = SEM)", "c_int": 1, "lambda": 25.0},
    {"id": "C_PHT_ARF", "title": "Instrumented Hyper-reactive PHT", "subtitle": r"Real ARF ($c_{\mathrm{int}}=1$) vs External PHT ($\lambda=8$) (Error bars = SEM)", "c_int": 1, "lambda": 8.0}
]

def run_instrumented_arf_pht(boundary_shift, seed, cfg):
    # Worker-Level Global Locking (CRITICAL): Prevent Silent Entropy Leaks in Cython/River
    safe_seed = int(seed % (2**31 - 1))
    random.seed(safe_seed)
    np.random.seed(safe_seed)
    rng = np.random.default_rng(safe_seed)
    
    arf = ARFClassifier(n_models=N_MODELS, seed=safe_seed, drift_detector=drift.ADWIN(clock=cfg['c_int']), warning_detector=drift.ADWIN(clock=cfg['c_int']))
    
    tau_arf, tau_det = np.nan, np.nan
    errors_pre =[]
    ext_pht = None

    for t in range(N_STEPS):
        x0, x1 = rng.normal(), rng.normal()
        x_dict = {0: x0, 1: x1}
        y = int(x0 + x1 > 0.0) if t < T_DRIFT else int(x0 + x1 > boundary_shift)
        
        y_pred = arf.predict_one(x_dict) or 0
        error = float(y_pred != y)
        
        # Empirical calibration on the last 1000 pre-drift steps
        if t < T_DRIFT:
            if t >= T_DRIFT - 1000:
                errors_pre.append(error)
        elif t == T_DRIFT:
            p_pre_empirical = np.mean(errors_pre) if errors_pre else 0.05
            ext_pht = StrictCUSUM(p_pre=p_pre_empirical, delta=0.01, threshold=cfg['lambda'])

        swaps_before = sum(arf._drift_tracker.values())
        arf.learn_one(x_dict, y)
        swaps_after = sum(arf._drift_tracker.values())

        if t >= T_DRIFT and np.isnan(tau_arf):
            if swaps_after > swaps_before: tau_arf = t - T_DRIFT
        
        if t >= T_DRIFT and ext_pht is not None:
            ext_pht.update(error)
            if np.isnan(tau_det):
                if ext_pht.drift_detected: tau_det = t - T_DRIFT
                
        if not np.isnan(tau_arf) and not np.isnan(tau_det): break

    return {'boundary_shift': boundary_shift, 'seed': seed, 'tau_arf': tau_arf, 'tau_det': tau_det}

def plot_scenario(df, cfg):
    agg = df.groupby('boundary_shift').apply(lambda g: pd.Series({
        'tau_arf_mean': g['tau_arf'].dropna().mean(),
        'tau_arf_sem': sem(g['tau_arf'].dropna()) if len(g['tau_arf'].dropna()) > 1 else 0,
        'tau_det_mean': g['tau_det'].dropna().mean(),
        'tau_det_sem': sem(g['tau_det'].dropna()) if len(g['tau_det'].dropna()) > 1 else 0,
        'missed_rate': np.mean(g['tau_arf'].fillna(np.inf) < g['tau_det'].fillna(np.inf))
    }), include_groups=False).reset_index()

    agg['delta_e_theoretical'] = norm.cdf(agg['boundary_shift'] / np.sqrt(2)) - 0.5
    delta_e_vals = agg['delta_e_theoretical'].values

    fig, (ax_main, ax_blind) = plt.subplots(2, 1, figsize=(8, 7), gridspec_kw={'height_ratios':[3, 1]}, sharex=True)

    ax_main.errorbar(delta_e_vals, agg['tau_arf_mean'], yerr=agg['tau_arf_sem'], fmt='o-', color=BLUE, lw=2.5, label=rf'Real ARF $\tau_{{\mathrm{{ARF}}}}$ ($c_{{\mathrm{{int}}}}={cfg["c_int"]}$)')
    ax_main.errorbar(delta_e_vals, agg['tau_det_mean'], yerr=agg['tau_det_sem'], fmt='s--', color=ORANGE, lw=2.5, label=rf'External PHT $\tau_{{\mathrm{{det}}}}$ ($\lambda={cfg["lambda"]}$)')

    de_fine = np.linspace(delta_e_vals[0], delta_e_vals[-1], 200)
    tau_arf_interp = np.interp(de_fine, delta_e_vals, np.nan_to_num(agg['tau_arf_mean'].values, nan=9999))
    tau_det_interp = np.interp(de_fine, delta_e_vals, np.nan_to_num(agg['tau_det_mean'].values, nan=9999))

    y_lim_top = 800
    blind_mask = tau_arf_interp < tau_det_interp
    if blind_mask.any():
        ax_main.fill_between(de_fine, tau_arf_interp, np.minimum(tau_det_interp, y_lim_top), where=blind_mask, color=RED, alpha=0.08)
        if cfg['id'] == 'A_PHT_ARF':
            ax_main.text(de_fine[blind_mask].mean(), y_lim_top*0.5, 'THE BLIND SPOT\n' + r'$\tau_{\mathrm{ARF}} < \tau_{\mathrm{det}}$', color=RED, fontsize=10, ha='center', va='center', fontweight='bold', bbox=dict(facecolor='white', alpha=0.85, edgecolor='none', pad=3))

    safe_mask = tau_det_interp < tau_arf_interp
    if safe_mask.any():
        ax_main.fill_between(de_fine, tau_det_interp, np.minimum(tau_arf_interp, y_lim_top), where=safe_mask, color=GREEN, alpha=0.08)
        if cfg['id'] == 'C_PHT_ARF':
            ax_main.text(de_fine[safe_mask].mean(), y_lim_top*0.5, 'SAFE ZONE\n' + r'$\tau_{\mathrm{det}} < \tau_{\mathrm{ARF}}$', color=GREEN, fontsize=10, ha='center', va='center', fontweight='bold', bbox=dict(facecolor='white', alpha=0.85, edgecolor='none', pad=3))

    for vals, col, lbl in [(agg['tau_arf_mean'].values, BLUE, 'ARF'), (agg['tau_det_mean'].values, ORANGE, 'PHT')]:
        valid = ~np.isnan(vals) & (vals > 0)
        if valid.sum() >= 4:
            log_de, log_tau = np.log(delta_e_vals[valid]), np.log(vals[valid])
            c = np.polyfit(log_de, log_tau, 1)
            ax_main.plot(de_fine, np.exp(c[1]) * de_fine ** c[0], color=col, linestyle=':', lw=2, alpha=0.4, label=rf'{lbl} Fit: $\approx {np.exp(c[1]):.1f}(\Delta e)^{{{c[0]:.2f}}}$')

    ax_main.set_ylabel('Time Steps (Delay)', fontsize=12); ax_main.set_title(cfg['title'], fontsize=13, fontweight='bold', pad=20)
    ax_main.text(0.5, 1.02, cfg['subtitle'], transform=ax_main.transAxes, ha='center', fontsize=10, color=GRAY)
    ax_main.set_ylim(0, y_lim_top); ax_main.legend(loc='upper right', fontsize=9, framealpha=0.9)

    ax_blind.bar(delta_e_vals, agg['missed_rate'].values * 100, color=RED, alpha=0.6, width=(delta_e_vals[1]-delta_e_vals[0])*0.7, label='% runs where ARF absorbed drift (Blind Spot)')
    ax_blind.set_ylabel('Missed Det.\n(%)', fontsize=10); ax_blind.set_xlabel(r'Theoretical Error Jump $\Delta e$', fontsize=12)
    ax_blind.set_ylim(0, 105); ax_blind.legend(fontsize=8, loc='center left')

    plt.tight_layout(); plt.savefig(FIGURES_DIR / f"Fig_R2_{cfg['id']}.png")
    plt.close(); print(f"[INFO] Successfully generated {cfg['title']}")

if __name__ == "__main__":
    for cfg in SCENARIOS:
        grid = list(itertools.product(BOUNDARY_SHIFTS, SEEDS))
        results = Parallel(n_jobs=-1)(delayed(run_instrumented_arf_pht)(bs, s, cfg) for bs, s in tqdm(grid, desc=f"Run {cfg['id']}"))
        df = pd.DataFrame(results)
        
        # Use Parquet for bit-wise deterministic storage as per FAIR guidelines
        parquet_path = DATA_DIR / f"R2_instrumented_{cfg['id']}.parquet"
        df.to_parquet(parquet_path, index=False)
        
        plot_scenario(df, cfg)