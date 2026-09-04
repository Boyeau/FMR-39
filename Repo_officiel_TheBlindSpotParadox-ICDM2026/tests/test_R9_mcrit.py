# tests/test_R9_mcrit.py
"""
Non-regression test for Experiment R9 (worked M_crit example, distribution-free).
Asserts that the regenerated artifact reproduces the numerical example of the manuscript Corollary.
Run after run_experiment_R9.sh.   Usage:  python -m pytest tests/test_R9_mcrit.py
"""
import numpy as np
import pandas as pd
from pathlib import Path
from pytest import approx

ROOT_DIR = Path(__file__).resolve().parent.parent
CSV = ROOT_DIR / "results" / "R9_mcrit" / "data" / "exp_R9_mcrit_comparison.csv"

def test_mcrit_numerical_example():
    df = pd.read_csv(CSV)
    # The worked example and the "M_crit <= 3" claim are stated at beta = 0.50. The CSV also
    # tabulates a conservative beta = 0.05 (necessarily larger M_crit), which is NOT the claim.
    b50 = np.isclose(df["beta"], 0.50)
    row = df[b50 & np.isclose(df["delta_e"], 0.33) & (df["lambda"] == 50)].iloc[0]
    assert row["E_tau_HAT"]      == approx(463, rel=0.05), row["E_tau_HAT"]
    assert row["tau_det_star"]   == approx(155, rel=0.05), row["tau_det_star"]
    assert row["F_emp"]          == approx(0.49, abs=0.03), row["F_emp"]
    assert int(row["Mcrit_emp"]) == 1, row["Mcrit_emp"]
    assert row["Pmiss_M10"]      == approx(0.999, abs=0.003), row["Pmiss_M10"]
    # Operative blind-spot magnitudes (Delta_e in {0.24,0.33,0.39,0.50}), lambda in {25,50}, beta=0.50:
    # the empirical critical size never exceeds 3 (<< River's default M=10).
    grid = df[b50 & (df["delta_e"] >= 0.24) & (df["lambda"].isin([25, 50]))]
    assert grid["Mcrit_emp"].max() <= 3, grid["Mcrit_emp"].max()