# exp_R5_compute_insects.py
"""INSECTS real-world evaluation, fused module: one simulation per cell yields
BOTH the aggregate detection metrics and, for the two blind-spot pipelines, the
per-episode decomposition used by the flooding analysis. Grid: 3 variants x 30
seeds x 3 pipelines = 270 runs (one-shot, no checkpointing; completes in
minutes). Reoccurring F1 is scored on the phantom-free K=2 in-stream ground
truth."""
import sys
import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from tqdm import tqdm
from river import stream

import exp_R5_config as cfg
import exp_R5_common as common


def per_episode_match(detections, true_drifts, tau_tol):
    """Greedy one-to-one episode matching: each drift claims the earliest unclaimed
    detection in (d, d+tau_tol]. Returns (detected_flags, add_per_drift)."""
    claimed, detected, add = set(), [False] * len(true_drifts), [np.nan] * len(true_drifts)
    for k, d in enumerate(true_drifts):
        cand = [det for det in detections if d < det <= d + tau_tol and det not in claimed]
        if cand:
            first = min(cand)
            detected[k], add[k] = True, first - d
            claimed.add(first)
    return detected, add


def simulate(variant, seed, pipeline_name):
    """One (variant, seed, pipeline) cell. Returns (aggregate_dict, episode_rows)."""
    df = pd.read_csv(cfg.INSECTS_DIR / f"{variant}.csv")
    n_total = len(df)
    target = df.columns[-1]
    warmup = common.get_warmup_steps(n_total)
    tau = common.get_tau_tol(n_total)
    raw_drifts = cfg.INSECTS_DRIFTS[variant]
    f1_drifts = common.resolve_f1_drifts(raw_drifts, n_total, tau)   # K-corrected (G1-B)

    def feature_stream():
        for x, y in stream.iter_pandas(df.drop(columns=[target]), df[target]):
            yield x, y

    detections, errors, lambda_val = common.run_evaluation(
        pipeline_name, seed, feature_stream(), warmup, cfg.INSECTS_NONE_FILL)

    add_fm, f1_fm, fp_fm, add_bp, f1_bp, fp_bp = common.evaluate_bipartite(
        detections, f1_drifts, n_total, tau)
    agg = {"variant": variant, "seed": seed, "pipeline": pipeline_name,
           "F1_fm": f1_fm, "F1_bp": f1_bp, "ADD_bp": add_bp,
           "lambda_calibrated": lambda_val, "n_detections": len(detections),
           "n_valid_drifts": len(f1_drifts)}

    episodes = []
    if pipeline_name in cfg.PIPELINES_FLOODING:
        valid = common.valid_drifts(raw_drifts, n_total, tau)
        detected, add = per_episode_match(detections, valid, tau)
        tp = int(sum(detected))
        run_recall = tp / len(valid) if valid else np.nan
        run_precision = tp / len(detections) if detections else np.nan
        run_n_fp = len(detections) - tp
        for k, d in enumerate(valid):
            e_post = float(np.mean(errors[d + 1:d + tau + 1]))
            e_pre = float(np.mean(errors[d - tau:d]))
            episodes.append({
                "variant": variant, "seed": seed, "pipeline": pipeline_name,
                "drift_idx": k, "drift_pos": d, "detected": int(detected[k]),
                "local_add": add[k], "local_delta_e": e_post - e_pre,
                "e_pre": e_pre, "e_post": e_post, "tau_tol": tau, "n_total": n_total,
                "lambda_calibrated": lambda_val, "n_detections_total": len(detections),
                "run_recall": run_recall, "run_precision": run_precision,
                "run_n_fp": run_n_fp, "n_valid_drifts": len(valid)})
    return agg, episodes


def main():
    print(f"[R5/INSECTS] River pinned to {cfg.RIVER_VERSION_PIN} | "
          f"REOCCURRING_F1_K2 = {cfg.REOCCURRING_F1_K2}", flush=True)
    seed_pool = common.make_seed_pool()
    grid = [(v, s, p) for v in cfg.INSECTS_VARIANTS
            for s in seed_pool for p in cfg.PIPELINES]
    np.random.default_rng(cfg.SEED_MASTER).shuffle(grid)

    chunks = [grid[i:i + cfg.INSECTS_CHUNK_SIZE]
              for i in range(0, len(grid), cfg.INSECTS_CHUNK_SIZE)]
    aggs, episodes = [], []
    for idx, chunk in enumerate(chunks):
        print(f"[R5/INSECTS] chunk {idx + 1}/{len(chunks)}", flush=True)
        res = Parallel(n_jobs=cfg.N_JOBS, batch_size=2)(
            delayed(simulate)(*args) for args in tqdm(chunk, desc=f"INSECTS Chunk {idx + 1}/{len(chunks)}"))
        for a, eps in res:
            aggs.append(a)
            episodes.extend(eps)

    df_agg, df_ep = pd.DataFrame(aggs), pd.DataFrame(episodes)
    df_agg.to_parquet(cfg.OUT_INSECTS, index=False)
    df_ep.to_parquet(cfg.OUT_EPISODE, index=False)

    print("\n=== Mean F1_bp by (variant, pipeline) [non-regression check] ===")
    print(df_agg.groupby(["variant", "pipeline"])["F1_bp"].mean().round(4).to_string())
    print("\n=== Per-episode detection rate (flooding pipelines) ===")
    print(df_ep.groupby(["variant", "pipeline"])["detected"].mean().round(4).to_string())
    print(f"\n[R5/INSECTS] DONE -> {cfg.OUT_INSECTS} ({len(df_agg)} runs), "
          f"{cfg.OUT_EPISODE} ({len(df_ep)} episode rows)")


if __name__ == "__main__":
    main()