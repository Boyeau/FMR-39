# %%
"""
exp_R8_lambda_op_sweep.py
=========================
Consolidation of the worst-case lambda_op bound for the Decoupling Principle (Definition 11).
Strictly measures the internal adaptation time tau_ARF of the ARF (c_int=1, M=10) over a
fine grid of magnitudes to locate the global minimum of the limit capacity:
    lambda_limit(Delta_e) = q_05(tau_ARF(Delta_e)) * (Delta_e - delta_P).
The external CUSUM is NOT simulated here (unnecessary for measuring tau_ARF).

Methodological alignments:
  1. Timing aligns with Experiment R1 (warmup=1000, gap=1000 -> drift at t=2000;
     tolerance=50000) ensuring the common magnitude steps perfectly match R1's q05.
  2. predict_one() is removed: the internal swap is driven exclusively by learn_one()
     (per-tree ADWINs are fed internally). As predict_one() is deterministic and does
     not consume RNG state, its removal yields identical tau_ARF while doubling speed.
  3. Early-break upon the first captured post-drift swap (identical logic to R1).
  4. Seed pooling matches the established R1 pipeline (SeedSequence(42).spawn(N_SEEDS)).
"""
import numpy as np
import pandas as pd
from pathlib import Path
from joblib import Parallel, delayed
from tqdm import tqdm
from scipy.stats import norm
from river import drift, forest

# --- Configuration -----------------------------------------------------------
ROOT_DIR    = Path(__file__).resolve().parent.parent.parent
RESULTS_DIR = ROOT_DIR / "results" / "R8_lambda_op_sweep" / "data"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
OUT_CSV     = RESULTS_DIR / "exp_R8_lambda_op_sweep.csv"

WARMUP        = 1000            # Warmup steps (matches R1)
DRIFT_GAP     = 1000            # t_drift_eff = WARMUP + DRIFT_GAP = 2000 (matches R1)
TOLERANCE     = 50000           # Post-drift tracking tolerance (matches R1)
T_DRIFT       = WARMUP + DRIFT_GAP
N_STEPS       = T_DRIFT + TOLERANCE

N_MODELS      = 10              # M = 10
C_INT         = 1               # Blind spot configuration
N_SEEDS       = 200
DELTA_E_GRID  = np.linspace(0.10, 0.50, 21)
DELTA_P       = 0.005           # PH/CUSUM tolerance
Q_LEVEL       = 0.05
OVERLAP_REF   = {0.10: 12.95, 0.25: 48.90, 0.40: 26.95}  # Reference q05 to reproduce from R1


def run_tau_arf(seed: int, delta_e: float):
    """Returns the timestamp of the first internal post-drift swap (NaN if none < TOLERANCE)."""
    rng = np.random.default_rng(seed)
    b_shift = np.sqrt(2.0) * norm.ppf(0.5 + delta_e)   # Shifted boundary matching target Delta_e

    model = forest.ARFClassifier(
        n_models=N_MODELS, seed=seed,
        drift_detector=drift.ADWIN(clock=C_INT),
        warning_detector=drift.ADWIN(clock=C_INT),
    )

    if not hasattr(model, "_drift_tracker"):
        raise RuntimeError(
            "ARFClassifier missing '_drift_tracker' attribute: incompatible River version. "
            "Ensure River 0.23.0 is installed for proper internal tree swap tracking."
        )

    tau_arf = np.nan
    for t in range(1, N_STEPS + 1):
        x0, x1 = rng.normal(), rng.normal()
        x_dict = {0: x0, 1: x1}
        y = int(x0 + x1 > 0.0) if t <= T_DRIFT else int(x0 + x1 > b_shift)

        before = sum(model._drift_tracker.values())
        model.learn_one(x_dict, y)          # predict_one omitted: unnecessary for tau_ARF tracking
        after = sum(model._drift_tracker.values())

        if t > T_DRIFT and after > before:
            tau_arf = t - T_DRIFT
            break                            # First post-drift swap captured -> stop
    return {"seed": seed, "delta_e": float(delta_e), "tau_arf": tau_arf}


def main():
    seq = np.random.SeedSequence(42)
    seed_pool = [int(s.generate_state(1)[0]) for s in seq.spawn(N_SEEDS)]
    grid = [(s, de) for de in DELTA_E_GRID for s in seed_pool]

    print(f"[INFO] {len(grid)} ARF runs (c_int={C_INT}, M={N_MODELS}) "
          f"| drift@t={T_DRIFT} tol={TOLERANCE}")
    res = Parallel(n_jobs=-1)(
        delayed(run_tau_arf)(s, de) for s, de in tqdm(grid, desc="R8 Lambda Sweep")
    )
    df = pd.DataFrame(res)
    df.to_csv(RESULTS_DIR / "exp_R8_fine_grid_raw.csv", index=False)

    # --- Per-magnitude aggregation ----------------------------------------------
    records = []
    for de in DELTA_E_GRID:
        sub = df[np.isclose(df["delta_e"], de)]
        finite = sub["tau_arf"].dropna().to_numpy()
        n_fin = finite.size
        q05 = float(np.quantile(finite, Q_LEVEL)) if n_fin else np.nan
        lam_limit = q05 * (de - DELTA_P) if n_fin else np.nan
        records.append({
            "delta_e": round(float(de), 4),
            "n_finite": n_fin,
            "miss_rate": round(float(sub["tau_arf"].isna().mean()), 3),
            "q05_tau_arf": round(q05, 3),
            "lambda_limit": round(lam_limit, 3),
        })
    table = pd.DataFrame.from_records(records)
    table.to_csv(OUT_CSV, index=False)

    # --- Global minimum search --------------------------------------------------
    valid = table.dropna(subset=["lambda_limit"])
    idx_min = valid["lambda_limit"].idxmin()
    de_crit = valid.loc[idx_min, "delta_e"]
    lam_min = valid.loc[idx_min, "lambda_limit"]

    print("\n=== FINE GRID CALIBRATION TABLE ===")
    print(table.to_string(index=False))
    print("-" * 60)
    print(f"Global minimum lambda_limit = {lam_min:.3f} reached at Delta_e = {de_crit}")
    print(f"  -> Worst-case bound for the Decoupling Principle on [0.10, 0.50].")
    print(f"  -> If envelope is floored at Delta_e_min = 0.20, calculating minimum over "
          f"[0.20, 0.50]:")
    sub20 = valid[valid["delta_e"] >= 0.20]
    if not sub20.empty:
        i20 = sub20["lambda_limit"].idxmin()
        print(f"     min lambda_limit[0.20,0.50] = {sub20.loc[i20,'lambda_limit']:.3f} "
              f"at Delta_e = {sub20.loc[i20,'delta_e']}")


if __name__ == "__main__":
    main()