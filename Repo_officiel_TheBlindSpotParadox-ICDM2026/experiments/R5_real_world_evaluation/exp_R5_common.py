# exp_R5_common.py
"""Shared primitives for the R5 pipeline: deterministic seed pool, model/detector
factories, the single canonical prequential evaluation loop (shared by BAF and
INSECTS so detection logic is byte-identical), bipartite detection scoring,
PageHinkley calibration, phantom-aware ground-truth resolution, and the adaptive
Delta_e estimator."""
import random

import numpy as np
from scipy.optimize import linear_sum_assignment
from river import drift, tree, forest

import exp_R5_config as cfg


def make_seed_pool(n_seeds=cfg.N_SEEDS, master=cfg.SEED_MASTER):
    """Deterministic, independent seed pool via NumPy SeedSequence (joblib-safe)."""
    seq = np.random.SeedSequence(master)
    return [int(s.generate_state(1)[0]) % (2**31 - 1) for s in seq.spawn(n_seeds)]


def get_warmup_steps(stream_length):
    """Adaptive warm-up length, capped (BAF keeps its 100k backward-compatible cap)."""
    return min(cfg.INSECTS_WARMUP_CAP, int(cfg.INSECTS_WARMUP_FRACTION * stream_length))


def get_tau_tol(stream_length):
    """Adaptive detection tolerance window, capped."""
    return min(cfg.INSECTS_TAU_CAP, int(cfg.INSECTS_TAU_FRACTION * stream_length))


def valid_drifts(drifts, n_total, tau_tol):
    """Keep only drifts whose full +/- tau_tol window lies inside the stream,
    removing PHANTOM drifts (truncated or out-of-stream canonical positions)."""
    return [d for d in drifts if (d - tau_tol >= 0) and (d + tau_tol < n_total)]


def resolve_f1_drifts(raw_drifts, n_total, tau_tol):
    """F1 ground truth. Under G1-B (REOCCURRING_F1_K2) phantom drifts are filtered,
    so F1 is scored on the valid transitions only (reoccurring -> K=2)."""
    if cfg.REOCCURRING_F1_K2:
        return valid_drifts(raw_drifts, n_total, tau_tol)
    return list(raw_drifts)


def build_model(pipeline_name, seed):
    """Classifier factory. The internal ADWIN clock (c=1 vs c=32) is the artifact
    under study; the external monitor (PHT vs ADWIN) is selected in run_evaluation."""
    if pipeline_name.endswith("_ht"):
        return tree.HoeffdingTreeClassifier()
    clock = 32 if "c32" in pipeline_name else 1
    return forest.ARFClassifier(
        n_models=cfg.ARF_N_MODELS, seed=seed,
        drift_detector=drift.ADWIN(clock=clock),
        warning_detector=drift.ADWIN(clock=clock),
    )


def calibrate_lambda(error_stream, target_fa=cfg.PHT_TARGET_FA, max_iter=25):
    """Bisection calibration of the PageHinkley threshold to a false-alarm budget on
    the warm-up error stream (fallback to target_fa=3 if 1 is infeasible)."""
    low, high = 1.0, 500.0
    for _ in range(max_iter):
        mid = (low + high) / 2.0
        n_fa = 0
        pht = drift.PageHinkley(threshold=mid, delta=cfg.PHT_DELTA)
        for e in error_stream:
            pht.update(e)
            if pht.drift_detected:
                n_fa += 1
                pht = drift.PageHinkley(threshold=mid, delta=cfg.PHT_DELTA)
        if n_fa <= target_fa:
            high = mid
        else:
            low = mid
    final_fa = 0
    pht = drift.PageHinkley(threshold=high, delta=cfg.PHT_DELTA)
    for e in error_stream:
        pht.update(e)
        if pht.drift_detected:
            final_fa += 1
            pht = drift.PageHinkley(threshold=high, delta=cfg.PHT_DELTA)
    if final_fa > target_fa and target_fa == 1:
        return calibrate_lambda(error_stream, target_fa=3, max_iter=max_iter)
    return high


def run_evaluation(pipeline_name, seed, feature_stream, warmup_steps, none_fill):
    """Canonical prequential evaluation shared by BAF and INSECTS.

    feature_stream : iterable yielding (x_dict, y) for the WHOLE stream.
    Returns (detections, error_stream_full, lambda_val).

    Logic: warm-up -> calibrate the external monitor -> stream; on a detected drift,
    reset the external monitor and reset (tree) or clone (ARF) the classifier.
    # Determinism hardening: pin the global RNGs per cell so that any unseeded draw
    # on river's ARF clone / tree-spawn path is reproducible across process runs."""
    random.seed(seed)
    np.random.seed(seed % (2 ** 32 - 1))

    is_pht  = pipeline_name.startswith("pht_")
    is_tree = pipeline_name.endswith("_ht")
    clock   = 32 if "c32" in pipeline_name else 1

    model = build_model(pipeline_name, seed)
    it = iter(feature_stream)
    warmup_errors, error_stream_full, detections = [], [], []

    # 1. Warm-up
    for _ in range(warmup_steps):
        try:
            x, y = next(it)
        except StopIteration:
            break
        y_pred = model.predict_one(x)
        y_pred = y_pred if y_pred is not None else none_fill
        warmup_errors.append(float(y != y_pred))
        model.learn_one(x, y)

    # 2. Calibrate the external monitor
    if is_pht:
        lambda_val = calibrate_lambda(warmup_errors)
        detector = drift.PageHinkley(threshold=lambda_val, delta=cfg.PHT_DELTA)
    else:
        lambda_val = float("nan")
        detector = drift.ADWIN(clock=clock)
    error_stream_full.extend(warmup_errors)

    # 3. Stream
    t = warmup_steps
    for x, y in it:
        y_pred = model.predict_one(x)
        y_pred = y_pred if y_pred is not None else none_fill
        e_t = float(y != y_pred)
        error_stream_full.append(e_t)
        detector.update(e_t)
        if detector.drift_detected:
            detections.append(t)
            detector = (drift.PageHinkley(threshold=lambda_val, delta=cfg.PHT_DELTA)
                        if is_pht else drift.ADWIN(clock=clock))
            model = tree.HoeffdingTreeClassifier() if is_tree else model.clone()
        model.learn_one(x, y)
        t += 1

    return detections, error_stream_full, lambda_val


def evaluate_bipartite(detected, true_drifts, n, tau):
    """First-Match and optimal Bipartite (Hungarian / Hopcroft-Karp) detection
    scoring. Returns (ADD_fm, F1_fm, FP_fm, ADD_bp, F1_bp, FP_bp)."""
    tp_pairs_fm, used = [], set()
    for td in sorted(true_drifts):
        cands = [d for d in detected if td <= d <= td + tau and d not in used]
        if cands:
            first = min(cands)
            tp_pairs_fm.append((td, first))
            used.add(first)
    TP_fm = len(tp_pairs_fm)
    FP_fm = len([d for d in detected if d not in used])
    FN_fm = len(true_drifts) - TP_fm
    ADD_fm = float(np.mean([b - a for a, b in tp_pairs_fm])) if tp_pairs_fm else np.nan
    pr = TP_fm / (TP_fm + FP_fm) if (TP_fm + FP_fm) > 0 else 0.0
    rc = TP_fm / (TP_fm + FN_fm) if (TP_fm + FN_fm) > 0 else 0.0
    f1_fm = 2 * pr * rc / (pr + rc) if (pr + rc) > 0 else 0.0

    if not true_drifts or not detected:
        return ADD_fm, f1_fm, FP_fm, np.nan, 0.0, len(detected)

    PENALTY = 1e9
    cost = np.full((len(true_drifts), len(detected)), PENALTY)
    for i, td in enumerate(true_drifts):
        for j, d in enumerate(detected):
            if td <= d <= td + tau:
                cost[i, j] = d - td
    row_ind, col_ind = linear_sum_assignment(cost)
    tp_pairs_bp = [(true_drifts[i], detected[j])
                   for i, j in zip(row_ind, col_ind) if cost[i, j] < PENALTY]
    TP_bp = len(tp_pairs_bp)
    FP_bp = len(detected) - TP_bp
    FN_bp = len(true_drifts) - TP_bp
    ADD_bp = float(np.mean([b - a for a, b in tp_pairs_bp])) if tp_pairs_bp else np.nan
    pr_bp = TP_bp / (TP_bp + FP_bp) if (TP_bp + FP_bp) > 0 else 0.0
    rc_bp = TP_bp / (TP_bp + FN_bp) if (TP_bp + FN_bp) > 0 else 0.0
    f1_bp = 2 * pr_bp * rc_bp / (pr_bp + rc_bp) if (pr_bp + rc_bp) > 0 else 0.0
    return ADD_fm, f1_fm, FP_fm, ADD_bp, f1_bp, FP_bp


def adaptive_windows(drift_positions, n_total,
                     cap=cfg.DELTA_E_WINDOW_CAP, factor=cfg.DELTA_E_WINDOW_FACTOR):
    """Per-drift window w_k = min(cap, min(dt_left, dt_right)//factor), floored at
    DELTA_E_MIN_WINDOW. Boundaries: tau_0 = 0, tau_{K+1} = n_total."""
    if not drift_positions:
        return []
    extended = [0] + sorted(drift_positions) + [n_total]
    windows = []
    for i in range(1, len(extended) - 1):
        tau_k = extended[i]
        dt_left, dt_right = tau_k - extended[i - 1], extended[i + 1] - tau_k
        w_k = int(min(cap, min(dt_left, dt_right) // factor))
        windows.append((tau_k, max(cfg.DELTA_E_MIN_WINDOW, w_k)))
    return windows


def estimate_delta_e_adaptive(error_stream, drift_positions, n_total,
                              n_bootstrap=cfg.DELTA_E_N_BOOTSTRAP):
    """Adaptive-window effective error jump per drift, with a bootstrap 95% CI over
    the per-drift jumps."""
    empty = {"delta_e_per_drift": [], "windows": [],
             "delta_e_mean": 0.0, "delta_e_ci_lo": 0.0, "delta_e_ci_hi": 0.0}
    windows = adaptive_windows(drift_positions, n_total)
    if not windows:
        return empty
    deltas, used_w = [], []
    for tau_k, w_k in windows:
        if tau_k - w_k < 0 or tau_k + w_k > n_total:
            continue
        pre = error_stream[tau_k - w_k:tau_k]
        post = error_stream[tau_k + 1:tau_k + w_k + 1]
        if len(pre) == 0 or len(post) == 0:
            continue
        deltas.append(float(np.mean(post) - np.mean(pre)))
        used_w.append(w_k)
    if not deltas:
        return empty
    arr = np.asarray(deltas)
    rng = np.random.default_rng(cfg.DELTA_E_RNG)
    boot = np.array([arr[rng.integers(0, len(arr), len(arr))].mean()
                     for _ in range(n_bootstrap)])
    lo, hi = np.percentile(boot, [2.5, 97.5])
    return {"delta_e_per_drift": [float(x) for x in deltas],
            "windows": [int(x) for x in used_w],
            "delta_e_mean": float(arr.mean()),
            "delta_e_ci_lo": float(lo), "delta_e_ci_hi": float(hi)}