# exp_R5_preflight.py
"""Pre-flight integrity checks for the R5 pipeline (fused preflight + API
introspection). Verifies that the six required raw CSVs exist and are readable,
reports stream lengths, and audits the canonical drift positions against each
stream length, flagging phantom drifts removed by the K=2 valid-window filter.
Exits non-zero on any blocking issue so the orchestrator halts early."""
import sys

import exp_R5_config as cfg
import exp_R5_common as common


def count_rows(path):
    if not path.exists():
        return None, "MISSING"
    try:
        with open(path) as f:
            n = sum(1 for _ in f) - 1  # minus header
        return n, "OK"
    except Exception as exc:  # noqa: BLE001
        return None, f"UNREADABLE ({exc})"


def main():
    print(f"[R5/preflight] River pin = {cfg.RIVER_VERSION_PIN}", flush=True)
    ok = True

    print("\n--- BAF streams ---")
    for v in cfg.BAF_VARIANTS:
        n, status = count_rows(cfg.BAF_DIR / f"{v}.csv")
        print(f"  {v:10s}: {status}" + (f" | n={n:,}" if n is not None else ""))
        ok = ok and (n is not None)

    print("\n--- INSECTS streams ---")
    insects_n = {}
    for v in cfg.INSECTS_VARIANTS:
        n, status = count_rows(cfg.INSECTS_DIR / f"{v}.csv")
        insects_n[v] = n
        print(f"  {v:35s}: {status}" + (f" | n={n:,}" if n is not None else ""))
        ok = ok and (n is not None)

    print("\n--- Drift-position audit (K-correction rationale) ---")
    for v in cfg.INSECTS_VARIANTS:
        n = insects_n.get(v)
        if n is None:
            continue
        tau = common.get_tau_tol(n)
        raw = cfg.INSECTS_DRIFTS[v]
        valid = common.valid_drifts(raw, n, tau)
        phantom = [d for d in raw if d not in valid]
        line = f"  {v:35s}: tau={tau} | K_raw={len(raw)} -> K_valid={len(valid)}"
        if phantom:
            line += f" | PHANTOM removed: {phantom}"
        print(line)

    print("\n[R5/preflight] " + ("ALL CHECKS PASSED" if ok else "FAILURES DETECTED"))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()