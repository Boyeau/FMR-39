# exp_R5_compute_baf.py
"""BAF real-world evaluation: 3 temporal-split variants x 30 seeds x 3 pipelines.
Produces baf_results.parquet (per-run bipartite F1 -> BAF rows of Table II).
The long run is checkpointed (G3) and resumes after interruption."""
import sys
import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from tqdm import tqdm

import exp_R5_config as cfg
import exp_R5_common as common


def simulate(variant, seed, pipeline_name):
    """Evaluate one (variant, seed, pipeline) cell on BAF."""
    df = pd.read_csv(cfg.BAF_DIR / f"{variant}.csv")
    num_cols = df.select_dtypes(include=["number"]).columns.drop(
        ["fraud_bool", "month"], errors="ignore")
    # Static z-score fitted on the warm-up window only (no temporal leakage).
    means = df.iloc[:cfg.BAF_WARMUP][num_cols].mean()
    stds = df.iloc[:cfg.BAF_WARMUP][num_cols].std().replace(0, 1)
    X_vals = ((df[num_cols] - means) / stds).values
    y_vals = df["fraud_bool"].values.astype(int)
    n_total = len(df)
    cols = list(num_cols)

    def feature_stream():
        for t in range(n_total):
            yield {cols[i]: X_vals[t, i] for i in range(len(cols))}, int(y_vals[t])

    detections, _, lambda_val = common.run_evaluation(
        pipeline_name, seed, feature_stream(), cfg.BAF_WARMUP, cfg.BAF_NONE_FILL)

    add_fm, f1_fm, fp_fm, add_bp, f1_bp, fp_bp = common.evaluate_bipartite(
        detections, cfg.BAF_DRIFTS, n_total, cfg.BAF_TAU_TOL)
    return {"variant": variant, "seed": seed, "pipeline": pipeline_name,
            "F1_fm": f1_fm, "F1_bp": f1_bp, "ADD_bp": add_bp,
            "lambda_calibrated": lambda_val, "n_detections": len(detections)}


def main():
    print(f"[R5/BAF] River pinned to {cfg.RIVER_VERSION_PIN}", flush=True)
    seed_pool = common.make_seed_pool()
    grid = [(v, s, p) for v in cfg.BAF_VARIANTS for s in seed_pool for p in cfg.PIPELINES]
    np.random.default_rng(cfg.SEED_MASTER).shuffle(grid)
    chunks = [grid[i:i + cfg.BAF_CHUNK_SIZE]
              for i in range(0, len(grid), cfg.BAF_CHUNK_SIZE)]

    existing = sorted(cfg.CHECKPOINTS_DIR.glob("baf_partial_*.parquet"))
    if existing:
        all_results = [r for f in existing for r in pd.read_parquet(f).to_dict("records")]
        last_idx = max(int(f.stem.split("_")[-1]) for f in existing)
        todo = list(enumerate(chunks))[last_idx + 1:]
        print(f"[RESUME] {len(all_results)} runs recovered; resuming at chunk "
              f"{last_idx + 1}/{len(chunks)}.", flush=True)
    else:
        all_results, todo = [], list(enumerate(chunks))

    for idx, chunk in todo:
        print(f"[R5/BAF] chunk {idx + 1}/{len(chunks)}", flush=True)
        res = Parallel(n_jobs=cfg.N_JOBS, batch_size=2)(
            delayed(simulate)(*args) for args in tqdm(chunk, desc=f"BAF Chunk {idx + 1}/{len(chunks)}"))
        all_results.extend(res)
        pd.DataFrame(res).to_parquet(
            cfg.CHECKPOINTS_DIR / f"baf_partial_{idx}.parquet", index=False)

    pd.DataFrame(all_results).to_parquet(cfg.OUT_BAF, index=False)
    print(f"[R5/BAF] DONE -> {cfg.OUT_BAF} ({len(all_results)} runs)")


if __name__ == "__main__":
    main()