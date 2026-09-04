# exp_R4_main_table.py
# =============================================================================
# MAIN EXPERIMENT SCRIPT (TABLE I): CONCEPT DRIFT ON HETEROSCEDASTIC STREAMS
#
# Common backbone for ALL pipelines:
#   - simulate_stream / evaluate / run_concept_drift protocols.
#   - 30 seeds, 12 transitions, 3 GARCH regimes (IID / Cal. A / Cal. B).
# Pipelines evaluated:
#   PHT+HT, ADWIN+HT, PHT+ARF{1,32}, ADWIN+ARF{1,32}, EDDM+HT, EDDM+ARF{1},
#   SRP+PHT{1,32}, KSWIN+ARF{1,32}, PHT+RF(Static), ADWIN+RF(Static).
# Significance: Seed-level SIGN test (Wilcoxon strictly deprecated).
# Outputs: Raw CSV + Merged LaTeX table + CSV for seed-level sign tests.
# =============================================================================

import collections
import itertools
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.special import expit, gammaln
import random
from scipy.stats import binomtest
from joblib import Parallel, delayed
from tqdm import tqdm

from river import drift, tree, ensemble, forest
from river.ensemble import SRPClassifier

warnings.filterwarnings("ignore")

# ─── Configuration & Paths (FAIR Compliance) ─────────────────────────────────
ROOT_DIR    = Path(__file__).resolve().parent.parent.parent
RESULTS_DIR = ROOT_DIR / "results" / "R4_proteus_evaluation" / "data"
TABLES_DIR  = ROOT_DIR / "results" / "R4_proteus_evaluation" / "tables"
LOGS_DIR    = ROOT_DIR / "logs" / "R4_proteus_evaluation"

for d in [RESULTS_DIR, TABLES_DIR, LOGS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

RAW_CSV   = RESULTS_DIR / "exp_R4_results_aligned_fusion.csv"
OUT_TEX   = TABLES_DIR / "table1_proteus_summary.tex"
SIGN_CSV  = RESULTS_DIR / "exp_R4_seed_level_tests.csv"

N_SEEDS        = 30
SEEDS          = list(range(1, N_SEEDS + 1))    # Strict alignment: seeds 1..30
BOOTSTRAP_SEED = 12345                          # Determinism for bootstrap CI
KSWIN_LAG      = 15                             # W/2 (Structural smoothing lag)
KSWIN_RESET_MODEL = True   # True = legacy protocol alignment (reset model on detection).
                           # False = continuous behavior (no reset upon KSWIN warning).

ETF_PARAMS_A = {
    'SPY': {'mu': 0.10/252,  'omega': 5e-7,  'alpha': 0.08,  'beta': 0.88},
    'PFF': {'mu': 0.03/252,  'omega': 8e-8,  'alpha': 0.05,  'beta': 0.90},
    'VNQ': {'mu': 0.08/252,  'omega': 2e-6,  'alpha': 0.12,  'beta': 0.82},
    'BWX': {'mu': 0.02/252,  'omega': 4e-8,  'alpha': 0.04,  'beta': 0.92},
}
ETF_PARAMS_B = {
    'SPY': {'mu': 0.112/252, 'omega': 1.2e-7, 'alpha': 0.09,  'beta': 0.893},
    'PFF': {'mu': 0.025/252, 'omega': 2.5e-8, 'alpha': 0.062, 'beta': 0.928},
    'VNQ': {'mu': 0.075/252, 'omega': 6.0e-7, 'alpha': 0.115, 'beta': 0.875},
    'BWX': {'mu': 0.008/252, 'omega': 8.0e-9, 'alpha': 0.055, 'beta': 0.940},
}
TICKERS     = ['SPY', 'PFF', 'VNQ', 'BWX']
TRANSITIONS = []
for from_t, to_t in itertools.permutations(TICKERS, 2):
    w = 100 if to_t == 'VNQ' else (1000 if from_t == 'VNQ' else 500)
    TRANSITIONS.append((from_t, to_t, w, f"{from_t}->{to_t}"))

# ─── Stream Simulation & Evaluation ───────────────────────────────────────────
def simulate_stream(p_from, p_to, regime_name, w, n_steps=8000, tp=4000, seed=42):
    np.random.seed(seed)
    t_arr = np.arange(n_steps, dtype=float)
    f_t   = expit(4.0 * (t_arr - tp) / w)
    mu_t  = p_from['mu'] * (1 - f_t) + p_to['mu'] * f_t
    r, h, eps = np.zeros(n_steps), np.zeros(n_steps), np.zeros(n_steps)

    if regime_name == 'IID':
        var_from = p_from['omega'] / (1 - p_from['alpha'] - p_from['beta'])
        var_to   = p_to['omega']   / (1 - p_to['alpha']   - p_to['beta'])
        var_t    = var_from * (1 - f_t) + var_to * f_t
        r        = mu_t + np.sqrt(var_t) * np.random.standard_normal(n_steps)
    else:
        omega_t = p_from['omega'] * (1 - f_t) + p_to['omega'] * f_t
        alpha_t = p_from['alpha'] * (1 - f_t) + p_to['alpha'] * f_t
        beta_t  = p_from['beta']  * (1 - f_t) + p_to['beta']  * f_t
        nu      = 7.0
        z_arr   = np.random.standard_t(nu, size=n_steps) * np.sqrt((nu - 2) / nu)
        h[0]    = omega_t[0] / (1 - alpha_t[0] - beta_t[0])
        eps[0]  = np.sqrt(h[0]) * z_arr[0]
        r[0]    = mu_t[0] + eps[0]
        for t in range(1, n_steps):
            h[t]   = max(omega_t[t] + alpha_t[t]*eps[t-1]**2 + beta_t[t]*h[t-1], 1e-12)
            eps[t] = np.sqrt(h[t]) * z_arr[t]
            r[t]   = mu_t[t] + eps[t]

    rs = pd.Series(r)
    df = pd.DataFrame({
        'log_return' : r,
        'rolling_vol': rs.rolling(20, min_periods=1).std(ddof=1).fillna(0).values,
        'regime'     : (f_t > 0.5).astype(int),
    })
    return df, [tp]

def evaluate(detected, true_drifts, n, tau):
    tp_pairs, used = [], set()
    for td in sorted(true_drifts):
        cands = [d for d in detected if td <= d <= td + tau and d not in used]
        if cands:
            first = min(cands)
            tp_pairs.append((td, first))
            used.add(first)
    TP = len(tp_pairs)
    FP = len([d for d in detected if d not in used])
    FN = len(true_drifts) - TP
    ADD = float(np.mean([b - a for a, b in tp_pairs])) if tp_pairs else np.nan
    pr  = TP / (TP + FP) if (TP + FP) > 0 else 0.0
    rc  = TP / (TP + FN) if (TP + FN) > 0 else 0.0
    f1  = 2 * pr * rc / (pr + rc) if (pr + rc) > 0 else 0.0
    return ADD, f1

# ─── Pipeline Execution Loops ─────────────────────────────────────────────────
def run_concept_drift(df, model, detector_factory):
    """Legacy protocol: reset the model upon external detection."""
    y, X = df['regime'].values, df[['log_return', 'rolling_vol']].values
    det, dets = detector_factory(), []
    for t in range(len(df)):
        x  = {0: X[t, 0], 1: X[t, 1]}
        yt = int(y[t])
        yp = model.predict_one(x) or 0
        det.update(float(yp != yt))
        model.learn_one(x, yt)
        if det.drift_detected:
            dets.append(t)
            det   = detector_factory()
            model = model.clone()
    return dets

def run_concept_drift_kswin(df, model, detector_factory):
    """KSWIN on smoothed error (buffer 30); model reset governed by KSWIN_RESET_MODEL."""
    y, X = df['regime'].values, df[['log_return', 'rolling_vol']].values
    det, dets = detector_factory(), []
    buf = collections.deque(maxlen=30)
    for t in range(len(df)):
        x  = {0: X[t, 0], 1: X[t, 1]}
        yt = int(y[t])
        yp = model.predict_one(x) or 0
        buf.append(float(yp != yt))
        if len(buf) == 30:
            det.update(float(np.mean(buf)))
        model.learn_one(x, yt)
        if det.drift_detected:
            dets.append(t)
            det = detector_factory()
            buf.clear()
            if KSWIN_RESET_MODEL:
                model = model.clone()
    return dets

# ─── Detector & Model Factories (Unified Configs) ─────────────────────────────
def pht():        return drift.PageHinkley(threshold=15.0)            # Equivalent to delta=0.005 (default)
def adwin(c):     return drift.ADWIN(delta=0.002, clock=c)
def kswin(seed):  return drift.KSWIN(alpha=0.005, window_size=100, stat_size=30, seed=seed)
try:
    from river.drift.binary import EDDM
except ImportError:
    from river.drift import EDDM

def eddm():       return EDDM()
def make_ht():    return tree.HoeffdingTreeClassifier()
def make_arf(seed, c):
    # Exact ARF from legacy Table I: only drift_detector is fixed (warning kept at default).
    return forest.ARFClassifier(n_models=10, seed=seed, drift_detector=adwin(c))
def make_srp(seed, c):
    return SRPClassifier(model=tree.HoeffdingTreeClassifier(), n_models=10,
                         subspace_size=0.6, training_method='patches', lam=6.0,
                         drift_detector=adwin(c), warning_detector=adwin(c), seed=seed)
def make_rf(seed):
    return ensemble.BaggingClassifier(model=tree.HoeffdingTreeClassifier(),
                                      n_models=10, seed=seed)

# ─── 14 Pipelines per (transition, seed) ──────────────────────────────────────
def process_transition_seed(trans, seed):
    # Strict RNG isolation per worker (Bit-wise reproducibility).
    # C-Level Overflow Prevention: apply modulo for Cython-compiled extensions
    safe_seed = seed % (2**31 - 1)
    np.random.seed(safe_seed)
    random.seed(safe_seed)
    
    from_t, to_t, w, name = trans
    out = []
    for regime, params in [('IID', ETF_PARAMS_A), ('Cal. A', ETF_PARAMS_A), ('Cal. B', ETF_PARAMS_B)]:
        df, dpts = simulate_stream(params[from_t], params[to_t], regime, w, seed=seed)
        tau = max(1000, w)

        def rec(detector, clock, dets):
            add, f1 = evaluate(dets, dpts, len(df), tau)
            out.append([regime, detector, clock, name, w, f1, add, seed])

        # --- HT Baselines (external clock = 1) ---
        rec('PHT + HT',   1, run_concept_drift(df, make_ht(), pht))
        rec('EDDM + HT',  1, run_concept_drift(df, make_ht(), eddm))
        rec('ADWIN + HT', 1, run_concept_drift(df, make_ht(), lambda: adwin(1)))

        # --- Adaptive Random Forest (c_int in {1,32}) ---
        for c in (1, 32):
            rec('PHT + ARF',   c, run_concept_drift(df, make_arf(seed, c), pht))
            rec('EDDM + ARF',  c, run_concept_drift(df, make_arf(seed, c), eddm))
            rec('ADWIN + ARF', c, run_concept_drift(df, make_arf(seed, c), lambda cc=c: adwin(cc)))

        # --- Streaming Random Patches (SRP) + PHT (c_int in {1,32}) ---
        for c in (1, 32):
            rec('SRP + PHT', c, run_concept_drift(df, make_srp(seed, c), pht))

        # --- KSWIN + ARF (c_int in {1,32}): ARF paired with KSWIN smoothing ---
        for c in (1, 32):
            rec('KSWIN + ARF', c, run_concept_drift_kswin(df, make_arf(seed, c),
                                                          lambda s=seed: kswin(s)))

        # --- Static RF (no internal adaptation/clock) ---
        rec('PHT + RF (Static)',   1, run_concept_drift(df, make_rf(seed), pht))
        rec('ADWIN + RF (Static)', 1, run_concept_drift(df, make_rf(seed), lambda: adwin(1)))
    return out

# ─── Bootstrap CI & Formatting ────────────────────────────────────────────────
def bootstrap_ci_half_width(series, n_resamples=1000):
    arr = series.dropna().values
    if len(arr) < 2: return 0.0
    resamples = np.random.choice(arr, size=(n_resamples, len(arr)), replace=True)
    means = np.mean(resamples, axis=1)
    return (np.percentile(means, 97.5) - np.percentile(means, 2.5)) / 2.0

def format_cell(mean_val, ci_val, is_f1=False, force_bold=False):
    if pd.isna(mean_val) or (not is_f1 and np.isinf(mean_val)):
        base = "N/A" if is_f1 else r"$\infty$"
        return rf"\textbf{{{base}}}" if force_bold else base
    if is_f1:
        s = f"{float(mean_val):.2f}"
        if force_bold:
            s = rf"\textbf{{{s}}}"
        return (s + r" {\small $\pm$" + f"{float(ci_val):.2f}" + r"}") if (not pd.isna(ci_val) and float(ci_val) > 0.005) else s
    mi = int(round(float(mean_val)))
    s = str(mi)
    if force_bold:
        s = rf"\textbf{{{s}}}"
    return (s + r" {\small $\pm$" + f"{int(round(float(ci_val)))}" + r"}") if (not pd.isna(ci_val) and float(ci_val) > 0.5) else s

# ─── Seed-Level Sign Test ─────────────────────────────────────────────────────
def log10_fisher_point(a, b, c, d):
    n = a + b + c + d
    lp = (gammaln(a+b+1) + gammaln(c+d+1) + gammaln(a+c+1) + gammaln(b+d+1)
          - gammaln(n+1) - gammaln(a+1) - gammaln(b+1) - gammaln(c+1) - gammaln(d+1))
    return lp / np.log(10)

def per_seed_detections(df, mask):
    sub = df[mask].copy()
    sub['detected'] = (sub['F1'] > 0).astype(int)
    g = sub.groupby('Seed')['detected'].agg(['sum', 'size']).reset_index()
    g.columns = ['Seed', 'n_det', 'n_streams']
    return g

def analyze_pair(df, mA, mB, labelA, labelB):
    gA, gB = per_seed_detections(df, mA), per_seed_detections(df, mB)
    m = gA.merge(gB, on='Seed', suffixes=('_A', '_B'))
    detA, detB = m['n_det_A'].values, m['n_det_B'].values
    wins_A, wins_B = int((detA > detB).sum()), int((detB > detA).sum())
    n_eff = wins_A + wins_B
    sign_p = binomtest(max(wins_A, wins_B), n_eff, 0.5, alternative='two-sided').pvalue if n_eff > 0 else 1.0
    rawA, totA = int(gA['n_det'].sum()), int(gA['n_streams'].sum())
    rawB, totB = int(gB['n_det'].sum()), int(gB['n_streams'].sum())
    log10_f = log10_fisher_point(rawA, totA - rawA, rawB, totB - rawB)
    # Wilcoxon deprecated. Primary metric: raw count;
    # Safeguard: sign test; Fisher log10 kept strictly for documentation purposes.
    return {'pipeline_A': labelA, 'pipeline_B': labelB,
            'n_det_A': rawA, 'n_total_A': totA, 'n_det_B': rawB, 'n_total_B': totB,
            'n_seeds': len(m), 'seeds_favor_A': wins_A, 'seeds_favor_B': wins_B,
            'seeds_tied': len(m) - n_eff, 'sign_test_p': sign_p,
            'log10_fisher_runlevel': round(float(log10_f), 1)}

# ─── LaTeX Assembly (Layout identical to Table I in the manuscript) ───────────
ROW_SPECS = [  # (label, Detector, Clock, is_kswin)
    (r"\textbf{PHT + HT}",                              'PHT + HT',            1, False),
    (r"\textbf{PHT + ARF} ($c_{\mathrm{int}} = 32$)",   'PHT + ARF',           32, False),
    (r"\textbf{PHT + ARF} ($c_{\mathrm{int}} = 1$)",    'PHT + ARF',           1, False),
    "MIDRULE",
    (r"\textbf{EDDM + HT}",                             'EDDM + HT',           1, False),
    (r"\textbf{EDDM + ARF} ($c_{\mathrm{int}} = 1$)",   'EDDM + ARF',          1, False),
    "MIDRULE",
    (r"\textbf{ADWIN + HT}",                            'ADWIN + HT',          1, False),
    (r"\textbf{ADWIN + ARF} ($c_{\mathrm{int}} = 32$)", 'ADWIN + ARF',         32, False),
    (r"\textbf{ADWIN + ARF} ($c_{\mathrm{int}} = 1$)",  'ADWIN + ARF',         1, False),
    "MIDRULE",
    (r"\textbf{SRP + PHT} ($c_{\mathrm{int}} = 1$)",    'SRP + PHT',           1, False),
    (r"\textbf{SRP + PHT} ($c_{\mathrm{int}} = 32$)",   'SRP + PHT',           32, False),
    (r"\textbf{KSWIN + ARF} ($c_{\mathrm{int}} = 1$)",  'KSWIN + ARF',         1, True),
    (r"\textbf{KSWIN + ARF} ($c_{\mathrm{int}} = 32$)", 'KSWIN + ARF',         32, True),
    "MIDRULE",
    (r"\textbf{PHT + RF} (Static)",                     'PHT + RF (Static)',   1, False),
    (r"\textbf{ADWIN + RF} (Static)",                   'ADWIN + RF (Static)', 1, False),
]
REG_DISPLAY = [('IID', 'IID Baseline'), ('Cal. A', 'Cal. A'), ('Cal. B', 'Cal. B')]

def cell_pair(agg, detector, clock, regime_raw, is_kswin, force_bold_f1=False):
    r = agg[(agg.Detector == detector) & (agg.Clock == clock) & (agg.Calibration == regime_raw)]
    if r.empty:
        return ["N/A", "N/A"]
    f1 = format_cell(r.F1_mean.values[0], r.F1_ci.values[0], is_f1=True, force_bold=force_bold_f1)
    if is_kswin and not pd.isna(r.ADD_mean.values[0]):
        raw = int(round(r.ADD_mean.values[0]))
        add = f"{raw} [{max(0, raw - KSWIN_LAG)}]"   # ADD_corr = max(0, ADD_raw - W/2)
    else:
        add = format_cell(r.ADD_mean.values[0], r.ADD_ci.values[0], is_f1=False)
    return [f1, add]

def fmt_p(p):
    if p <= 0: return "0"
    e = int(np.floor(np.log10(p))); return rf"{p/10**e:.0f}\times10^{{{e}}}"

def build_caption(sign_df):
    # Explicit and safe pair extraction to guarantee exact ICDM caption ordering
    pht_pair = sign_df[sign_df['pipeline_A'] == 'PHT+ARF c=1'].iloc[0]
    eddm_pair = sign_df[sign_df['pipeline_A'] == 'EDDM+ARF c=1'].iloc[0]
    srp_pair = sign_df[sign_df['pipeline_A'] == 'SRP+PHT c=1'].iloc[0]
    kswin_pair = sign_df[sign_df['pipeline_A'] == 'KSWIN+ARF c=1'].iloc[0]

    pairs = [
        rf"PHT+ARF c=1 detects {pht_pair.n_det_A}/{pht_pair.n_total_A} runs vs {pht_pair.n_det_B}/{pht_pair.n_total_B} for PHT+HT",
        rf"EDDM+ARF c=1 detects {eddm_pair.n_det_A}/{eddm_pair.n_total_A} runs vs {eddm_pair.n_det_B}/{eddm_pair.n_total_B} for EDDM+HT",
        rf"SRP+PHT c=1 detects {srp_pair.n_det_A}/{srp_pair.n_total_A} runs vs {srp_pair.n_det_B}/{srp_pair.n_total_B} for PHT+HT",
        rf"KSWIN+ARF c=1 detects {kswin_pair.n_det_A}/{kswin_pair.n_total_A} runs vs {kswin_pair.n_det_B}/{kswin_pair.n_total_B} for PHT+ARF c=1"
    ]
    
    p0 = float(pht_pair.sign_test_p)
    ns = int(pht_pair.n_seeds)
    
    return (r"Concept Drift detection on heteroscedastic ProteuS streams with the static RF resolution, "
            r"all pipelines generated by a SINGLE aligned method (12 transitions $\times$ 30 seeds $=$ 360 runs "
            r"per cell; identical streams, seeds, and ARF configuration). Mean $\pm$ 95\% CI (1000 bootstrap "
            r"resamples); $\infty$ denotes detection failure. Significance is assessed at the seed level (the unit "
            rf"of statistical independence of the synthetic generator): {'; '.join(pairs)}. All {ns} seeds separate "
            rf"completely (paired sign test $p \approx {fmt_p(p0)}$); Wilcoxon is deprecated. "
            r"KSWIN ADD includes a structural lag $W/2 = 15$; bracketed $[X]$ is lag-corrected. "
            r"Boldface marks the blind-spot collapse (F1=0.00) and its KSWIN resolution (F1=1.00).")

def build_table(agg, sign_df):
    L = [r"\begin{table*}[t]", r"  \centering", rf"  \caption{{{build_caption(sign_df)}}}",
         r"  \label{tab:results_concept}", r"  \begin{tabular}{@{}lrrrrrr@{}}", r"    \toprule",
         r"                                                   & \multicolumn{2}{c}{\textbf{IID Baseline}} & \multicolumn{2}{c}{\textbf{Cal. A (Low GARCH)}} & \multicolumn{2}{c}{\textbf{Cal. B (High GARCH)}} \\",
         r"    \cmidrule(lr){2-3} \cmidrule(lr){4-5} \cmidrule(lr){6-7}",
         r"    \textbf{Pipeline Configuration}                & \textbf{F1} & \textbf{ADD} & \textbf{F1} & \textbf{ADD} & \textbf{F1} & \textbf{ADD} \\",
         r"    \midrule"]
    for spec in ROW_SPECS:
        if spec == "MIDRULE":
            L.append(r"    \midrule"); continue
        label, det, clk, ks = spec
        
        # IEEE/ICDM standard: bolding aligned with the submitted Table I caption
        # (blind-spot collapse F1=0.00 AND its KSWIN resolution F1=1.00; ADD never bolded)
        force_bold = label in [
            r"\textbf{PHT + ARF} ($c_{\mathrm{int}} = 1$)",
            r"\textbf{EDDM + ARF} ($c_{\mathrm{int}} = 1$)",
            r"\textbf{SRP + PHT} ($c_{\mathrm{int}} = 1$)",
            r"\textbf{KSWIN + ARF} ($c_{\mathrm{int}} = 1$)",
            r"\textbf{KSWIN + ARF} ($c_{\mathrm{int}} = 32$)"
        ]
        
        cells = []
        for reg_raw, _ in REG_DISPLAY:
            cells += cell_pair(agg, det, clk, reg_raw, ks, force_bold_f1=force_bold)
        L.append(f"    {label:46s} & " + " & ".join(cells) + r" \\")
    L += [r"    \bottomrule", r"  \end{tabular}", r"\end{table*}", ""]
    return "\n".join(L)

# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    grid = list(itertools.product(TRANSITIONS, SEEDS))
    print(f"[run] {len(TRANSITIONS)} transitions x {N_SEEDS} seeds x 14 pipelines x 3 regimes")
    print("[run] Parallel execution (Joblib) - Please wait...")
    nested = Parallel(n_jobs=-1)(delayed(process_transition_seed)(t, s) for t, s in tqdm(grid, desc="R4 Main Table"))
    df = pd.DataFrame([row for sub in nested for row in sub],
                      columns=['Calibration', 'Detector', 'Clock', 'Dataset', 'w', 'F1', 'ADD', 'Seed'])
    df.to_csv(RAW_CSV, index=False)
    print(f"[ok] {len(df)} rows -> {RAW_CSV}")

    # Seed-level sign tests for statistical significance
    sign = pd.DataFrame([
        analyze_pair(df, (df.Detector == 'PHT + ARF')   & (df.Clock == 1),
                         (df.Detector == 'PHT + HT')    & (df.Clock == 1),  "PHT+ARF c=1", "PHT+HT"),
        analyze_pair(df, (df.Detector == 'SRP + PHT')   & (df.Clock == 1),
                         (df.Detector == 'PHT + HT')    & (df.Clock == 1),  "SRP+PHT c=1", "PHT+HT"),
        analyze_pair(df, (df.Detector == 'KSWIN + ARF') & (df.Clock == 1),
                         (df.Detector == 'PHT + ARF')   & (df.Clock == 1),  "KSWIN+ARF c=1", "PHT+ARF c=1"),
        analyze_pair(df, (df.Detector == 'PHT + RF (Static)')   & (df.Clock == 1),
                         (df.Detector == 'PHT + ARF')           & (df.Clock == 1),  "PHT+RF", "PHT+ARF c=1"),
        analyze_pair(df, (df.Detector == 'ADWIN + RF (Static)') & (df.Clock == 1),
                         (df.Detector == 'ADWIN + ARF')         & (df.Clock == 1),  "ADWIN+RF", "ADWIN+ARF c=1"),
        analyze_pair(df, (df.Detector == 'EDDM + ARF')  & (df.Clock == 1),
                         (df.Detector == 'EDDM + HT')   & (df.Clock == 1),  "EDDM+ARF c=1", "EDDM+HT"),
    ])
    sign.to_csv(SIGN_CSV, index=False)
    print(f"[ok] sign tests -> {SIGN_CSV}")
    print(sign[['pipeline_A', 'pipeline_B', 'n_det_A', 'n_det_B', 'sign_test_p']].to_string(index=False))

    # Aggregation + Bootstrap (seeded) + Table generation
    # C-Level Overflow Prevention applied to the bootstrap global seed
    safe_bootstrap_seed = BOOTSTRAP_SEED % (2**31 - 1)
    np.random.seed(safe_bootstrap_seed)
    agg = df.groupby(['Detector', 'Clock', 'Calibration']).agg(
        F1_mean=('F1', 'mean'), F1_ci=('F1', bootstrap_ci_half_width),
        ADD_mean=('ADD', lambda x: np.nan if x.dropna().empty else x.dropna().mean()),
        ADD_ci=('ADD', bootstrap_ci_half_width)).reset_index()

    tex = build_table(agg, sign)
    OUT_TEX.write_text(tex, encoding='utf-8')
    print(f"[ok] merged table -> {OUT_TEX}\n")
    print(tex)

if __name__ == "__main__":
    main()