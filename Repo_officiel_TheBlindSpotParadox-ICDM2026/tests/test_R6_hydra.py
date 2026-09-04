"""
Non-regression test for Experiment R6 (The Hydra Effect).
Asserts that the regenerated artifact reproduces the empirical power-law constants
reported in 'Section III-C: The Hydra Effect: Ensemble Acceleration'.
Run after run_experiment_R6.sh.
Usage:  python -m pytest tests/test_R6_hydra.py
"""
import numpy as np
import pandas as pd
import pytest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
R6_PATH = ROOT_DIR / "results" / "R6_hydra_factor" / "data" / "R6_hat_instrumented.parquet"
R2_PATH = ROOT_DIR / "results" / "R2_instrumented_blind_spot" / "data" / "R2_instrumented_A_PHT_ARF.parquet"

def powerlaw(series_mean):
    v = series_mean[(series_mean.index > 0) & (series_mean.values > 0)]
    c = np.polyfit(np.log(v.index.values), np.log(v.values), 1)
    return np.exp(c[1]), c[0]

def test_hydra_factor_and_powerlaw():
    assert R6_PATH.exists(), "R6 data missing. Run run_experiment_R6.sh first."
    assert R2_PATH.exists(), "R2 data missing. Run run_experiment_R2.sh first."

    hat = pd.read_parquet(R6_PATH).dropna(subset=['tau_hat'])
    arf = pd.read_parquet(R2_PATH).dropna(subset=['tau_arf'])

    if 'delta_e' not in arf.columns:
        from scipy.stats import norm
        arf['delta_e'] = norm.cdf(arf['boundary_shift'] / np.sqrt(2)) - 0.5

    hat_m = hat.groupby('delta_e')['tau_hat'].mean()
    arf_m = arf.groupby('delta_e')['tau_arf'].mean()

    K_hat, a_hat = powerlaw(hat_m)
    K_arf, a_arf = powerlaw(arf_m)

    # Asserts empirical fits match the published manuscript within 5% relative tolerance
    assert K_hat == pytest.approx(102.0, rel=0.05), f"K_HAT = {K_hat:.1f}, expected ~102"
    assert a_hat == pytest.approx(-1.02, rel=0.05), f"alpha_HAT = {a_hat:.2f}, expected ~-1.02"
    assert K_arf == pytest.approx(18.5, rel=0.05), f"K_ARF = {K_arf:.1f}, expected ~18.5"
    assert a_arf == pytest.approx(-0.98, rel=0.05), f"alpha_ARF = {a_arf:.2f}, expected ~-0.98"

if __name__ == "__main__":
    test_hydra_factor_and_powerlaw()
    print("[OK] R6 reproduces the Hydra Effect constants of the submitted manuscript.")