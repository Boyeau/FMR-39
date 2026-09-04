# exp_R5_smoke_test.py
"""Fast end-to-end smoke test on 20k-row prefixes of BAF Base and INSECTS abrupt.
Confirms the River API, model/detector factories, calibration and the canonical
evaluation loop execute correctly before launching the full (long) pipeline."""
import sys

import pandas as pd
from river import stream

import exp_R5_config as cfg
import exp_R5_common as common

SMOKE_ROWS = 20_000
SMOKE_WARMUP = 2_000


def smoke_baf():
    df = pd.read_csv(cfg.BAF_DIR / "Base.csv", nrows=SMOKE_ROWS)
    num_cols = df.select_dtypes(include=["number"]).columns.drop(
        ["fraud_bool", "month"], errors="ignore")
    means = df[num_cols].mean()
    stds = df[num_cols].std().replace(0, 1)
    X = ((df[num_cols] - means) / stds).values
    y = df["fraud_bool"].values.astype(int)
    cols = list(num_cols)

    def feature_stream():
        for t in range(len(df)):
            yield {cols[i]: X[t, i] for i in range(len(cols))}, int(y[t])

    det, _, lam = common.run_evaluation("pht_arf_c1", cfg.SEED_MASTER,
                                        feature_stream(), SMOKE_WARMUP, cfg.BAF_NONE_FILL)
    print(f"  BAF Base       (pht_arf_c1): lambda={lam:.2f}, detections={len(det)}")


def smoke_insects():
    df = pd.read_csv(cfg.INSECTS_DIR / "abrupt_balanced.csv", nrows=SMOKE_ROWS)
    target = df.columns[-1]

    def feature_stream():
        for x, y in stream.iter_pandas(df.drop(columns=[target]), df[target]):
            yield x, y

    det, _, lam = common.run_evaluation("pht_ht", cfg.SEED_MASTER,
                                        feature_stream(), SMOKE_WARMUP, cfg.INSECTS_NONE_FILL)
    print(f"  INSECTS abrupt (pht_ht)    : lambda={lam:.2f}, detections={len(det)}")


def main():
    print("[R5/smoke] Running end-to-end smoke test (20k-row prefixes)...", flush=True)
    try:
        smoke_baf()
        smoke_insects()
    except Exception as exc:  # noqa: BLE001
        print(f"[R5/smoke] FAILED: {exc}")
        sys.exit(1)
    print("[R5/smoke] PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()