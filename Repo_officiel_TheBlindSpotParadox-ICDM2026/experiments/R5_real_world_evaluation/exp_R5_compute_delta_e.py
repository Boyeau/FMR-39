# exp_R5_compute_delta_e.py
"""Adaptive effective-error-jump (Delta_e) estimation for the BAF and INSECTS
streams of Table II. One Hoeffding Tree produces the reference error stream per
variant; Delta_e is then estimated per drift with an adaptive window and a
bootstrap 95% CI. Reoccurring uses K=2 (phantom-free) positions. Fast (minutes)."""
import sys
import numpy as np
import pandas as pd
from river import tree, stream

import exp_R5_config as cfg
import exp_R5_common as common


def error_stream_baf(variant):
    """Reference HT error stream on a BAF variant (warm-up-fitted z-score)."""
    df = pd.read_csv(cfg.BAF_DIR / f"{variant}.csv")
    num_cols = df.select_dtypes(include=["number"]).columns.drop(
        ["fraud_bool", "month"], errors="ignore")
    means = df.iloc[:cfg.BAF_WARMUP][num_cols].mean()
    stds = df.iloc[:cfg.BAF_WARMUP][num_cols].std().replace(0, 1)
    X_vals = ((df[num_cols] - means) / stds).values
    y_vals = df["fraud_bool"].values.astype(int)
    cols = list(num_cols)
    model = tree.HoeffdingTreeClassifier()
    errs = []
    for t in range(len(df)):
        x = {cols[i]: X_vals[t, i] for i in range(len(cols))}
        y_pred = model.predict_one(x)
        y_pred = y_pred if y_pred is not None else cfg.BAF_NONE_FILL
        errs.append(float(y_vals[t] != y_pred))
        model.learn_one(x, int(y_vals[t]))
    return errs, len(df)


def error_stream_insects(variant):
    """Reference HT error stream on an INSECTS variant."""
    df = pd.read_csv(cfg.INSECTS_DIR / f"{variant}.csv")
    target = df.columns[-1]
    it = stream.iter_pandas(df.drop(columns=[target]), df[target])
    model = tree.HoeffdingTreeClassifier()
    errs = []
    for x, y in it:
        y_pred = model.predict_one(x)
        y_pred = y_pred if y_pred is not None else cfg.INSECTS_NONE_FILL
        errs.append(float(y != y_pred))
        model.learn_one(x, y)
    return errs, len(df)


def main():
    rows = []
    print("[R5/Delta_e] BAF ...", flush=True)
    for v in cfg.BAF_VARIANTS:
        errs, n = error_stream_baf(v)
        out = common.estimate_delta_e_adaptive(errs, cfg.BAF_DRIFTS, n)
        rows.append({"dataset": "baf", "variant": v, **out})
        print(f"  BAF {v}: Delta_e = {out['delta_e_mean']:+.4f} "
              f"[{out['delta_e_ci_lo']:+.4f}, {out['delta_e_ci_hi']:+.4f}]")

    print("[R5/Delta_e] INSECTS ...", flush=True)
    for v in cfg.INSECTS_VARIANTS:
        errs, n = error_stream_insects(v)
        out = common.estimate_delta_e_adaptive(errs, cfg.INSECTS_DRIFTS_DELTA_E[v], n)
        rows.append({"dataset": "insects", "variant": v, **out})
        print(f"  INSECTS {v}: Delta_e = {out['delta_e_mean']:+.4f} "
              f"[{out['delta_e_ci_lo']:+.4f}, {out['delta_e_ci_hi']:+.4f}]")

    pd.DataFrame(rows).to_parquet(cfg.OUT_DELTA_E, index=False)
    print(f"[R5/Delta_e] DONE -> {cfg.OUT_DELTA_E}")


if __name__ == "__main__":
    main()