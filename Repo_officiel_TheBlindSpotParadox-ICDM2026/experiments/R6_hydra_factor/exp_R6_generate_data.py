# exp_R6_generate_data.py
"""
exp_R6_generate_data.py
Experiment R6: single-tree HAT (M=1) instrumentation for the Hydra acceleration factor.
Records the internal adaptation delay tau_HAT (first post-drift tree swap) across a
Delta_e sweep, 100 seeds/magnitude. Determinized with the EXACT R2 worker-level RNG
locking so the run is bit-wise reproducible. The Hydra factor tau_HAT / tau_ARF and the
power-law fits (K_HAT, alpha_HAT) are assembled downstream by exp_R6_compute_hydra.py.
"""
import random
import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from tqdm import tqdm
from pathlib import Path
from scipy.stats import norm
from river import drift
from river.forest import ARFClassifier
import warnings
warnings.filterwarnings('ignore')

# [IEEE/ICDM FAIR Compliance] Dynamic path resolution; script lives in experiments/R6_hydra_factor/
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT_DIR / "results" / "R6_hydra_factor" / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# M=1 => single Hoeffding Adaptive Tree; internal clock c_int=1 (hyper-reactive)
N_STEPS, T_DRIFT, N_MODELS, C_INT = 8000, 4000, 1, 1
BOUNDARY_SHIFTS = np.linspace(0.1, 4.0, 20)
SEEDS = list(range(1, 101))

def run_instrumented_hat(boundary_shift, seed):
    # Worker-Level Global Locking (CRITICAL): identical to the validated R2 scheme,
    # prevents silent entropy leaks on river's Cython tree-spawn / clone path.
    safe_seed = int(seed % (2**31 - 1))
    random.seed(safe_seed)
    np.random.seed(safe_seed)
    rng = np.random.default_rng(safe_seed)

    hat = ARFClassifier(n_models=N_MODELS, seed=safe_seed,
                        drift_detector=drift.ADWIN(clock=C_INT),
                        warning_detector=drift.ADWIN(clock=C_INT))

    tau_hat = np.nan
    for t in range(N_STEPS):
        x0, x1 = rng.normal(), rng.normal()
        x_dict = {0: x0, 1: x1}
        y = int(x0 + x1 > 0.0) if t < T_DRIFT else int(x0 + x1 > boundary_shift)

        hat.predict_one(x_dict)  # prequential order preserved (predict-then-learn)

        swaps_before = sum(hat._drift_tracker.values())
        hat.learn_one(x_dict, y)
        swaps_after = sum(hat._drift_tracker.values())

        if t >= T_DRIFT and np.isnan(tau_hat) and swaps_after > swaps_before:
            tau_hat = t - T_DRIFT
            break

    return {'boundary_shift': boundary_shift, 'seed': seed, 'tau_hat': tau_hat}

if __name__ == "__main__":
    grid = [(bs, s) for bs in BOUNDARY_SHIFTS for s in SEEDS]
    results = Parallel(n_jobs=-1)(delayed(run_instrumented_hat)(bs, s) for bs, s in tqdm(grid, desc="Experiment R6"))
    df = pd.DataFrame(results)
    # Theoretical Delta_e mapping (same transform as R2)
    df['delta_e'] = norm.cdf(df['boundary_shift'] / np.sqrt(2)) - 0.5

    out = DATA_DIR / "R6_hat_instrumented.parquet"
    df.to_parquet(out, index=False)
    print(f"[INFO] tau_HAT artifact saved to: {out}")

    # Diagnostic print: empirical power-law fit for (K_HAT, alpha_HAT) computation
    agg = df.dropna(subset=['tau_hat']).groupby('delta_e')['tau_hat'].mean()
    valid = agg[(agg.index > 0) & (agg.values > 0)]
    if len(valid) >= 4:
        c = np.polyfit(np.log(valid.index.values), np.log(valid.values), 1)
        print(f"[INFO] HAT empirical power-law fit: tau_HAT ~ {np.exp(c[1]):.1f} (delta_e)^{c[0]:.2f}")
        print("[INFO] Compare to the values reported in the paper (K_HAT ~ 102, alpha_HAT ~ -1.02).")