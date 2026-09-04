# tests/test_R8_lambda_op.py
"""
Non-regression test for Experiment R8 (lambda_op fine-grid sweep, Decoupling Principle).
Asserts that the regenerated artifact reproduces the three numerical claims of Definition 11.
Run after run_experiment_R8.sh.   Usage:  python -m pytest tests/test_R8_lambda_op.py
"""
import numpy as np
import pandas as pd
from pathlib import Path
from pytest import approx

ROOT_DIR = Path(__file__).resolve().parent.parent
CSV = ROOT_DIR / "results" / "R8_lambda_op_sweep" / "data" / "exp_R8_lambda_op_sweep.csv"

def test_lambda_op_claims():
    df = pd.read_csv(CSV)
    q = lambda de: float(df[np.isclose(df["delta_e"], de)]["q05_tau_arf"].iloc[0])
    lam = lambda de: float(df[np.isclose(df["delta_e"], de)]["lambda_limit"].iloc[0])

    # 1. Noise-driven swaps: q05(tau_arf) is magnitude-independent (~13) below the weak band.
    for de in (0.10, 0.12, 0.14, 0.16):
        assert q(de) == approx(12.95, abs=0.5), f"q05 at {de} = {q(de)}"
    # 2. Contaminated lower edge of the envelope: lambda_op ~ 4.2 at Delta_e = 0.20.
    assert lam(0.20) == approx(4.2, abs=0.1), f"lambda_limit at 0.20 = {lam(0.20)}"
    # 3. Global ceiling over the envelope [0.20, 0.50]: lambda_op never exceeds ~12.4.
    env = df[df["delta_e"] >= 0.20]["lambda_limit"]
    assert env.max() == approx(12.4, abs=0.1) and env.max() <= 12.5, f"max = {env.max()}"