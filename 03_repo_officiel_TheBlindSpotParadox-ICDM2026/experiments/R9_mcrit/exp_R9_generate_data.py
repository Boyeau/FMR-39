# exp_R9_generate_data.py
"""
exp_R9_generate_data.py
Experiment R9 (stage 1): single-tree HAT (M=1) instrumentation feeding the worked M_crit example.
Records, per (drift magnitude, seed), the internal adaptation delay tau_HAT, the empirically measured
Delta_e, and post-drift swap/warning counts, for the reference configuration (c_int=1, c_ext=32).
The empirical CDF of tau_HAT is consumed by exp_R9_compute_mcrit.py to derive the distribution-free
critical ensemble size M_crit. Determinized with the exact R2/R6/R7 worker-level RNG locking.
"""
import random
import warnings
import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from tqdm import tqdm
from pathlib import Path
from river import drift
from river.forest import ARFClassifier
warnings.filterwarnings('ignore')

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT_DIR / "results" / "R9_mcrit" / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

N_STEPS, T_DRIFT, N_MODELS = 8000, 4000, 1   # M=1 single Hoeffding Adaptive Tree
DELTA_E_WINDOW = 500
C_INT, C_EXT = 1, 32
BOUNDARY_SHIFTS = np.linspace(0.1, 4.0, 20)
SEEDS = list(range(1, 101))                  # 100 seeds per magnitude

def run_instrumented_hat(boundary_shift, seed):
    safe_seed = int(seed % (2**31 - 1))
    random.seed(safe_seed)
    np.random.seed(safe_seed)
    rng = np.random.default_rng(safe_seed)

    hat = ARFClassifier(n_models=N_MODELS, seed=safe_seed,
                        drift_detector=drift.ADWIN(clock=C_INT),
                        warning_detector=drift.ADWIN(clock=C_INT))
    ext = drift.ADWIN(delta=0.002, clock=C_EXT)

    tau_hat, tau_det = np.nan, np.nan
    errors_pre, errors_post = [], []
    swaps_at_drift = warnings_at_drift = 0

    for t in range(N_STEPS):
        x0, x1 = rng.normal(), rng.normal()
        x_dict = {0: x0, 1: x1}
        y = int(x0 + x1 > 0.0) if t < T_DRIFT else int(x0 + x1 > boundary_shift)

        y_pred = hat.predict_one(x_dict) or 0
        error = float(y_pred != y)

        if T_DRIFT - DELTA_E_WINDOW <= t < T_DRIFT:
            errors_pre.append(error)
        elif T_DRIFT <= t < T_DRIFT + DELTA_E_WINDOW:
            errors_post.append(error)

        if t == T_DRIFT:
            swaps_at_drift = sum(hat._drift_tracker.values())
            warnings_at_drift = sum(hat._warning_tracker.values())

        swaps_before = sum(hat._drift_tracker.values())
        hat.learn_one(x_dict, y)
        swaps_after = sum(hat._drift_tracker.values())
        if t >= T_DRIFT and np.isnan(tau_hat) and swaps_after > swaps_before:
            tau_hat = t - T_DRIFT

        ext.update(error)
        if t >= T_DRIFT and np.isnan(tau_det) and ext.drift_detected:
            tau_det = t - T_DRIFT

        if not np.isnan(tau_hat) and not np.isnan(tau_det) and t >= T_DRIFT + DELTA_E_WINDOW:
            break

    e_pre = np.mean(errors_pre) if errors_pre else np.nan
    e_post = np.mean(errors_post) if errors_post else np.nan
    delta_e = (e_post - e_pre) if not (np.isnan(e_pre) or np.isnan(e_post)) else np.nan

    return {'boundary_shift': boundary_shift, 'seed': seed, 'delta_e': delta_e,
            'tau_hat': tau_hat, 'tau_det': tau_det,
            'n_swaps_post': sum(hat._drift_tracker.values()) - swaps_at_drift,
            'n_warnings_post': sum(hat._warning_tracker.values()) - warnings_at_drift}

if __name__ == "__main__":
    grid = [(bs, s) for bs in BOUNDARY_SHIFTS for s in SEEDS]
    rows = Parallel(n_jobs=-1)(delayed(run_instrumented_hat)(bs, s) for bs, s in tqdm(grid, desc="Experiment R9"))
    out = DATA_DIR / "results_instrumented_A_ADWIN_HAT.csv"
    pd.DataFrame(rows).to_csv(out, index=False)
    print(f"[INFO] single-tree HAT instrumentation saved to: {out}")
    print(f"[INFO] {len(rows)} runs; next: exp_R9_compute_mcrit.py")