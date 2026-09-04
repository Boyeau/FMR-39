"""
exp_R1_generate_data.py
Extended Diagnostic 3: Isolate the evolution of P(tau_arf < tau_det) over a lambda grid,
with truncation bias correction for the Share Blind Spot computation.
"""
import random
import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from pathlib import Path
from tqdm import tqdm
from scipy.stats import norm
from river import forest, drift

# [IEEE/ICDM FAIR Compliance] Dynamic path resolution based on script location
# The script is in experiments/R1_race_condition/. We target the root centralized results folder.
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
RESULTS_DIR = ROOT_DIR / "results" / "R1_race_condition" / "data"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

N_STEPS = 54000  # Warmup 4000 + Tolerance 50000 (harmonized)
T_DRIFT = 4000
N_SEEDS = 200
DELTA_E = 0.25
LAMBDAS_TO_TEST = [2.5, 5.0, 10.0, 25.0, 50.0, 100.0]
DELTA_P = 0.005

class StrictCUSUM:
    def __init__(self, p_pre, delta, threshold):
        self.S = 0.0; self.p_pre = p_pre; self.delta = delta; self.threshold = threshold
        self.drift_detected = False
    def update(self, x):
        self.S = max(0.0, self.S + (x - self.p_pre) - self.delta)
        if self.S >= self.threshold: self.drift_detected = True

def run_diff_test(seed, lambda_val):
    # [IEEE/ICDM FAIR Compliance] Worker-Level Global Locking (Controlled Rollback)
    # We use the exact original uint32 seed to guarantee bit-wise match with the submitted paper.
    # Python 3.12 and Numpy 1.26 natively handle uint32, avoiding C-level overflow.
    
    # 1. Lock global singletons inside the parallel worker to prevent stochastic drift
    random.seed(seed)
    np.random.seed(seed)
    
    # 2. Restore the EXACT original generators
    rng = np.random.default_rng(seed)
    
    b_shift = np.sqrt(2) * norm.ppf(0.5 + DELTA_E)
    
    arf = forest.ARFClassifier(n_models=10, seed=seed, drift_detector=drift.ADWIN(clock=1), warning_detector=drift.ADWIN(clock=1))
    cusum_external_fixed = StrictCUSUM(0.05, DELTA_P, lambda_val)
    
    errors_warmup = []
    cusum_external_emp = None
    
    tau_arf_internal = np.nan
    tau_det_ext_fixed = np.nan
    tau_det_ext_emp = np.nan
    
    swaps_at_drift = 0
    
    for t in range(1, N_STEPS + 1):
        x0, x1 = rng.normal(), rng.normal()
        x_dict = {0: x0, 1: x1}
        y = int(x0 + x1 > 0.0) if t <= T_DRIFT else int(x0 + x1 > b_shift)
        
        y_pred = arf.predict_one(x_dict) or 0
        error = float(y_pred != y)
        
        if T_DRIFT - 1000 <= t <= T_DRIFT:
            if t < T_DRIFT: errors_warmup.append(error)
            if t == T_DRIFT:
                swaps_at_drift = sum(arf._drift_tracker.values())
                p_pre_emp = np.mean(errors_warmup)
                if p_pre_emp == 0: p_pre_emp = 0.01
                cusum_external_emp = StrictCUSUM(p_pre_emp, DELTA_P, lambda_val)
            
        before = sum(arf._drift_tracker.values())
        arf.learn_one(x_dict, y)
        after = sum(arf._drift_tracker.values())
        
        if t > T_DRIFT:
            if np.isnan(tau_arf_internal) and after > before:
                tau_arf_internal = t - T_DRIFT
                
            if np.isnan(tau_det_ext_fixed):
                cusum_external_fixed.update(error)
                if cusum_external_fixed.drift_detected:
                    tau_det_ext_fixed = t - T_DRIFT
                
            if np.isnan(tau_det_ext_emp):
                cusum_external_emp.update(error)
                if cusum_external_emp.drift_detected:
                    tau_det_ext_emp = t - T_DRIFT
                    
            if not np.isnan(tau_arf_internal) and not np.isnan(tau_det_ext_fixed) and not np.isnan(tau_det_ext_emp):
                break
                
    # Empirical Blind Spot definition 
    # True if CUSUM completely misses (NaN) and ARF succeeds, OR if ARF succeeds strictly before CUSUM.
    if np.isnan(tau_det_ext_emp) and not np.isnan(tau_arf_internal):
        blind_spot_observed = True
    elif not np.isnan(tau_det_ext_emp) and not np.isnan(tau_arf_internal):
        blind_spot_observed = bool(tau_arf_internal < tau_det_ext_emp)
    else:
        blind_spot_observed = False
                
    return {
        'seed': seed,
        'lambda_val': lambda_val,
        'tau_arf': tau_arf_internal,
        'tau_det_fixed': tau_det_ext_fixed,
        'tau_det_emp': tau_det_ext_emp,
        'tau_arf_finite': not np.isnan(tau_arf_internal),
        'tau_det_emp_finite': not np.isnan(tau_det_ext_emp),
        'blind_spot_observed': blind_spot_observed
    }

if __name__ == "__main__":
    print("[INFO] Launching Extended Diagnostic 3 (Share Blind Spot Cartography)...")
    seq = np.random.SeedSequence(42)
    seeds = [int(s.generate_state(1)[0]) for s in seq.spawn(N_SEEDS)]
    
    grid = [(s, l) for s in seeds for l in LAMBDAS_TO_TEST]
    results = Parallel(n_jobs=-1)(delayed(run_diff_test)(s, l) for s, l in tqdm(grid, desc="Experiment R1"))
    df = pd.DataFrame(results)
    output_parquet = RESULTS_DIR / "R1_race_condition.parquet"
    df.to_parquet(output_parquet, index=False)
    print(f"[INFO] Parquet artifact saved to: {output_parquet}")
    
    agg = df.groupby('lambda_val').agg(
        Share_Blind_Spot=('blind_spot_observed', 'mean'),
        Detection_Rate=('tau_det_emp_finite', 'mean')
    ).round(3)
    
    output_md = RESULTS_DIR / "R1_race_condition_diagnostic.md"
    with open(output_md, "w") as f:
        f.write("# Experiment R1: Share Blind Spot Evolution\n\n")
        f.write(agg.to_markdown())
        
    print(f"[SUCCESS] Diagnostic saved to: {output_md}")