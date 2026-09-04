# exp_R3_regime_crossover.py

r"""
Experiment R3: Regime Crossover & Non-Adaptive RF Solution.
Reproduces Figure 3 of the manuscript "The Blind Spot Paradox".
Strictly adheres to IEEE/ICDM FAIR reproducibility standards.
"""
import random
import numpy as np
import pandas as pd
from scipy.stats import norm
from joblib import Parallel, delayed
from tqdm import tqdm
import matplotlib
matplotlib.use('Agg')  # Headless backend to ensure exact visual reproducibility
import matplotlib.pyplot as plt
from river import tree, forest, ensemble, drift
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

# ------------------------------------------------------------------------------
# DYNAMIC PATH RESOLUTION (FAIR Compliance)
# Assumes script is located in experiments/R3_regime_crossover/
# ------------------------------------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
RESULTS_DIR = ROOT_DIR / "results" / "R3_regime_crossover"
DATA_DIR = RESULTS_DIR / "data"
FIG_DIR = RESULTS_DIR / "figures"

DATA_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)

N_STEPS = 8000
DRIFT_TIME = 4000
TOLERANCE = 1000
N_SEEDS = 100
DELTA_E_VALUES = np.linspace(0.02, 0.50, 15)

def compute_boundary_shift(delta_e):
    r"""
    Computes the theoretical decision boundary shift 'b' required to induce
    a specific effective error jump (\Delta e) under a Gaussian feature distribution.
    
    Mathematical formulation: \Delta e = \Phi(b/\sqrt{2}) - 0.5, 
    where \Phi is the standard Normal Cumulative Distribution Function (CDF).
    """
    safe_delta = min(delta_e, 0.4999)
    return np.sqrt(2) * norm.ppf(safe_delta + 0.5)

def run_single_seed(seed, delta_e, pipeline_type):
    r"""
    Executes a single stream evaluation strictly isolated by a deterministic seed.
    Simulates an abrupt concept drift mapping to the theoretical \Delta e.
    """
    # 100% Determinism (R5 Standard): Lock global RNGs per worker to ensure River's
    # internal stochasticity (Poisson bagging, tree splits) is bit-wise reproducible.
    int_seed = int(seed)
    random.seed(int_seed)
    np.random.seed(int_seed % (2**32 - 1))
    
    # AE Visual Match: Reverting to Legacy RandomState (MT19937) instead of PCG64
    # to exactly reconstruct the data streams X0, X1 used in the submitted manuscript.
    rng = np.random.RandomState(int_seed)
    b = compute_boundary_shift(delta_e)
    
    X0 = rng.randn(N_STEPS)
    X1 = rng.randn(N_STEPS)
    
    if pipeline_type == 'HT':
        model = tree.HoeffdingTreeClassifier()
    elif pipeline_type == 'ARF':
        model = forest.ARFClassifier(n_models=10, drift_detector=drift.ADWIN(clock=1), seed=seed)
    elif pipeline_type == 'RF_Static':
        # Static Bagging without internal ADWIN tree resets -> Non-Adaptive Ensemble
        model = ensemble.BaggingClassifier(model=tree.HoeffdingTreeClassifier(), n_models=10, seed=seed)
    else:
        raise ValueError("Unknown pipeline configuration.")
        
    pht = drift.PageHinkley(threshold=25.0, delta=0.005)
    
    alarms_pre = 0
    detected_in_window = 0
    correct_post = 0
    
    for t in range(N_STEPS):
        x = {'x0': X0[t], 'x1': X1[t]}
        
        # Inject abrupt concept drift at DRIFT_TIME by shifting the decision boundary
        y = 1 if (X0[t] + X1[t]) > (0 if t < DRIFT_TIME else b) else 0
            
        y_pred = model.predict_one(x) or 0
        error = 0 if y_pred == y else 1
        
        # The external cumulative-evidence monitor observes the binary error stream
        pht.update(error)
        if pht.drift_detected:
            if t < DRIFT_TIME:
                # Quantifies the "Noise Filter" capability (False Alarms)
                alarms_pre += 1
            elif DRIFT_TIME <= t <= DRIFT_TIME + TOLERANCE:
                # Validates detection survival against the Starvation Effect
                detected_in_window = 1
            
            # Reset detector state post-alarm to prevent cascade triggering
            pht = drift.PageHinkley(threshold=25.0, delta=0.005)
            
        if DRIFT_TIME <= t <= DRIFT_TIME + TOLERANCE:
            if y_pred == y: correct_post += 1
                
        model.learn_one(x, y)
        
    return (1.0 if detected_in_window == 0 else 0.0), alarms_pre, correct_post / (TOLERANCE + 1)

def main():
    print("[INFO] Launching Regime Crossover evaluation (HT vs ARF vs Static RF)...")
    pipes = ['HT', 'ARF', 'RF_Static']
    metrics = {p: {'miss':[], 'fp':[], 'acc':[], 'm_sem':[], 'f_sem':[], 'a_sem':[]} for p in pipes}
    
    # Pre-allocate records for exact tabular tracing
    data_records = []
    
    # AE Visual Match: Using the original naive 0-99 sequence to perfectly map 
    # the feature streams from the manuscript's submission run.
    worker_seeds = list(range(N_SEEDS))

    for de in tqdm(DELTA_E_VALUES, desc="Delta E Sweep"):
        for p in pipes:
            res = Parallel(n_jobs=-1)(delayed(run_single_seed)(worker_seeds[s], de, p) for s in range(N_SEEDS))
            miss_arr, fp_arr, acc_arr = zip(*res)
            
            # Record at seed-level (optional for full trace) and aggregate
            data_records.append({
                'delta_e': de, 'pipeline': p,
                'miss_mean': np.mean(miss_arr)*100, 'miss_sem': np.std(miss_arr, ddof=1)/np.sqrt(N_SEEDS)*100,
                'fp_mean': np.mean(fp_arr), 'fp_sem': np.std(fp_arr, ddof=1)/np.sqrt(N_SEEDS),
                'acc_mean': np.mean(acc_arr), 'acc_sem': np.std(acc_arr, ddof=1)/np.sqrt(N_SEEDS)
            })

            metrics[p]['miss'].append(np.mean(miss_arr)*100); metrics[p]['m_sem'].append(np.std(miss_arr, ddof=1)/np.sqrt(N_SEEDS)*100)
            metrics[p]['fp'].append(np.mean(fp_arr)); metrics[p]['f_sem'].append(np.std(fp_arr, ddof=1)/np.sqrt(N_SEEDS))
            metrics[p]['acc'].append(np.mean(acc_arr)); metrics[p]['a_sem'].append(np.std(acc_arr, ddof=1)/np.sqrt(N_SEEDS))
            
    for p in pipes:
        for k in metrics[p]: metrics[p][k] = np.array(metrics[p][k])
            
    # Save aggregated results to parquet artifact
    df_results = pd.DataFrame(data_records)
    parquet_path = DATA_DIR / 'R3_regime_crossover_metrics.parquet'
    df_results.to_parquet(parquet_path, index=False)
    print(f"[INFO] Metrics saved securely to {parquet_path}")

    print("[INFO] Generating analytical plot (Figure 3)...")
    fig, axes = plt.subplots(1, 3, figsize=(16, 4.5), dpi=300)
    labels =['PHT + HT (Base)', 'PHT + ARF (Adaptive)', 'PHT + RF (Non-Adaptive Solution)']
    colors =['#2A6A7C', '#C45C5C', '#E8A000']
    markers = ['o', 's', 'D']
    
    for idx, (m_key, title, ylbl, ylim) in enumerate([
        ('fp', "Pre-Drift False Alarms (Noise Filter)", "FP Count", None),
        ('miss', "Missed Detection Rate", "Missed Detections (%)", (-5, 105)),
        ('acc', "Post-Drift Recovery Accuracy", "Accuracy", None)
    ]):
        ax = axes[idx]
        if idx > 0:
            ax.axvspan(0.0, 0.09, color='#546E7A', alpha=0.08)
            ax.axvspan(0.09, 0.25, color='#2E7D32', alpha=0.08)
            ax.axvspan(0.25, 0.52, color='#C62828', alpha=0.08)
            
            # Dynamic annotations aligned with Y-axis relative size (0.0 = bottom, 1.0 = top)
            ax.text(0.045, 0.50, 'Weak\nSignal', color='#546E7A', ha='center', va='center', fontweight='bold', fontsize=9, alpha=0.7, transform=ax.get_xaxis_transform())
            ax.text(0.17, 0.98, 'SAFE ZONE\n(Literature)', color='#2E7D32', ha='center', va='top', fontweight='bold', fontsize=9, alpha=0.7, transform=ax.get_xaxis_transform())
            ax.text(0.385, 0.98, 'THE BLIND SPOT\n(Starvation)', color='#C62828', ha='center', va='top', fontweight='bold', fontsize=9, alpha=0.7, transform=ax.get_xaxis_transform())
            
        for i, p in enumerate(pipes):
            sem_key = 'f_sem' if m_key == 'fp' else ('m_sem' if m_key == 'miss' else 'a_sem')
            ax.plot(DELTA_E_VALUES, metrics[p][m_key], color=colors[i], label=labels[i], marker=markers[i])
            ax.fill_between(DELTA_E_VALUES, metrics[p][m_key] - metrics[p][sem_key], metrics[p][m_key] + metrics[p][sem_key], color=colors[i], alpha=0.2)
            
        ax.set_title(title, fontsize=11, fontweight='bold')
        ax.set_xlabel(r"Effective Error Jump ($\Delta e$)")
        ax.set_ylabel(ylbl)
        if ylim: ax.set_ylim(ylim)
        ax.grid(alpha=0.3)
        if idx == 0: ax.legend(loc='center right', fontsize=9)

    plt.tight_layout()
    fig_path = FIG_DIR / 'Fig_R3_Regime_Crossover.png'
    plt.savefig(fig_path, bbox_inches='tight', dpi=300)
    print(f"[SUCCESS] RF Solution plot saved to {fig_path}")

if __name__ == "__main__":
    main()