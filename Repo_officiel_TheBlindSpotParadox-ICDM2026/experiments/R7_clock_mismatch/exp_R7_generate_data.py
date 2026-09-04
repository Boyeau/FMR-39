# exp_R7_generate_data.py
"""
exp_R7_generate_data.py
Experiment R7: the Clock-Mismatch Artefact (Regime 1).
Instruments the real ARF (M=10) internal drift ADWIN (clock c_int) against an EXTERNAL
ADWIN (delta=0.002, clock c_ext) on the ensemble error stream, over three clock
configurations, 100 seeds x 20 drift magnitudes. Records the internal swap delay tau_arf
and the external detection delay tau_det; miss = (tau_arf < tau_det). Determinized with the
exact R2/R6 worker-level RNG locking. The Regime-1 miss-rate summary is assembled
downstream by exp_R7_compute_regime1.py; reproduction checks live in tests/test_R7_regime1.py.
"""
import random
import warnings
import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from tqdm import tqdm
from pathlib import Path
from scipy.stats import norm
from river import drift
from river.forest import ARFClassifier
warnings.filterwarnings('ignore')

# Script lives in experiments/R7_clock_mismatch/ ; target the centralized results root.
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT_DIR / "results" / "R7_clock_mismatch" / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

N_STEPS, T_DRIFT, N_MODELS = 8000, 4000, 10
BOUNDARY_SHIFTS = np.linspace(0.1, 4.0, 20)
SEEDS = list(range(1, 101))
EXT_DELTA = 0.002  # external ADWIN sensitivity (matches the submitted Fig. 2ter setup)

SCENARIOS = [
    {"id": "A_mismatched", "c_int": 1,  "c_ext": 32},  # River's default external clock
    {"id": "B_matched",    "c_int": 1,  "c_ext": 1},
    {"id": "C_decoupled",  "c_int": 32, "c_ext": 1},
]

def run_clock_mismatch(boundary_shift, seed, cfg):
    # Worker-Level Global Locking (CRITICAL): identical to the validated R2/R6 scheme,
    # prevents silent entropy leaks on river's Cython tree-spawn / clone path.
    safe_seed = int(seed % (2**31 - 1))
    random.seed(safe_seed)
    np.random.seed(safe_seed)
    rng = np.random.default_rng(safe_seed)

    arf = ARFClassifier(n_models=N_MODELS, seed=safe_seed,
                        drift_detector=drift.ADWIN(clock=cfg['c_int']),
                        warning_detector=drift.ADWIN(clock=cfg['c_int']))
    ext = drift.ADWIN(delta=EXT_DELTA, clock=cfg['c_ext'])

    tau_arf, tau_det = np.nan, np.nan
    for t in range(N_STEPS):
        x0, x1 = rng.normal(), rng.normal()
        x_dict = {0: x0, 1: x1}
        y = int(x0 + x1 > 0.0) if t < T_DRIFT else int(x0 + x1 > boundary_shift)

        y_pred = arf.predict_one(x_dict) or 0
        error = float(y_pred != y)

        swaps_before = sum(arf._drift_tracker.values())
        arf.learn_one(x_dict, y)
        swaps_after = sum(arf._drift_tracker.values())
        if t >= T_DRIFT and np.isnan(tau_arf) and swaps_after > swaps_before:
            tau_arf = t - T_DRIFT

        ext.update(error)  # external monitor reads the ensemble error every step
        if t >= T_DRIFT and np.isnan(tau_det) and ext.drift_detected:
            tau_det = t - T_DRIFT

        if not np.isnan(tau_arf) and not np.isnan(tau_det):
            break

    return {'config': cfg['id'], 'boundary_shift': boundary_shift, 'seed': seed,
            'tau_arf': tau_arf, 'tau_det': tau_det}

if __name__ == "__main__":
    all_rows = []
    for cfg in SCENARIOS:
        grid = [(bs, s) for bs in BOUNDARY_SHIFTS for s in SEEDS]
        all_rows.extend(Parallel(n_jobs=-1)(delayed(run_clock_mismatch)(bs, s, cfg) for bs, s in tqdm(grid, desc=cfg['id'])))
    df = pd.DataFrame(all_rows)
    # Theoretical Delta_e for the axis (avoids the empirical measurement artefact, as in the legacy script).
    df['delta_e'] = norm.cdf(df['boundary_shift'] / np.sqrt(2)) - 0.5

    out = DATA_DIR / "R7_clock_mismatch.parquet"
    df.to_parquet(out, index=False)
    print(f"[INFO] clock-mismatch artifact saved to: {out}")
    print(f"[INFO] {len(df)} runs across {df['config'].nunique()} clock configurations; "
          f"next: exp_R7_compute_regime1.py")