# tests/test_R7_regime1.py
"""
Non-regression test for Experiment R7 (clock-mismatch / Regime 1).
Asserts that the regenerated artifact reproduces the three qualitative claims of the manuscript
subsection 'Regime 1: The Clock-Mismatch Artefact'. Run after run_experiment_R7.sh.
Usage:  python -m pytest tests/test_R7_regime1.py   (or:  python tests/test_R7_regime1.py)
"""
import numpy as np
import pandas as pd
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
PARQUET  = ROOT_DIR / "results" / "R7_clock_mismatch" / "data" / "R7_clock_mismatch.parquet"

def _curve(df, cid):
    g = df[df.config == cid].copy()
    g["miss"] = g["tau_arf"].fillna(np.inf) < g["tau_det"].fillna(np.inf)
    return g.groupby("delta_e")["miss"].mean()

def test_regime1_claims():
    df = pd.read_parquet(PARQUET)
    A, B, C = _curve(df, "A_mismatched"), _curve(df, "B_matched"), _curve(df, "C_decoupled")
    # Mismatched: the external ADWIN is starved at every magnitude beyond 0.35 (pointwise, not averaged).
    assert (A[A.index > 0.35] > 0.50).all(), f"mismatched min miss (de>0.35) = {A[A.index>0.35].min():.1%}"
    # Matched / decoupled: above the weak-signal band the external ADWIN wins pointwise.
    assert (B[B.index > 0.30] < 0.05).all(), f"matched max miss (de>0.30) = {B[B.index>0.30].max():.1%}"
    assert (C[C.index > 0.30] < 0.05).all(), f"decoupled max miss (de>0.30) = {C[C.index>0.30].max():.1%}"

if __name__ == "__main__":
    test_regime1_claims()
    print("[OK] R7 reproduces the three Regime-1 claims of the submitted manuscript.")