# exp_R4_kswin_sweep.py
# =============================================================================
# TARGETED SCRIPT: KSWIN ROBUSTNESS EVALUATION (ALPHA SWEEP)
# Addresses the ICDM reviewer's requirement regarding KSWIN stability
# under heteroscedastic GARCH regimes to rule out false-alarm flooding.
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

from river import drift, tree, forest

warnings.filterwarnings("ignore")

# ─── Configuration & Paths (FAIR Compliance) ─────────────────────────────────
ROOT_DIR    = Path(__file__).resolve().parent.parent.parent
RESULTS_DIR = ROOT_DIR / "results" / "R4_proteus_evaluation" / "data"
TABLES_DIR  = ROOT_DIR / "results" / "R4_proteus_evaluation" / "tables"
LOGS_DIR    = ROOT_DIR / "logs" / "R4_proteus_evaluation"

for d in [RESULTS_DIR, TABLES_DIR, LOGS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

RAW_CSV   = RESULTS_DIR / "exp_R4_results_KSWIN_alpha_sweep.csv"
OUT_TEX   = TABLES_DIR / "exp_R4_table_KSWIN_alpha_sweep.tex"
SIGN_CSV  = RESULTS_DIR / "exp_R4_seed_level_tests_KSWIN_alpha_sweep.csv"

N_SEEDS        = 30
SEEDS          = list(range(1, N_SEEDS + 1))
BOOTSTRAP_SEED = 12345
KSWIN_LAG      = 15
KSWIN_RESET_MODEL = True

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

def run_concept_drift_kswin(df, model, detector_factory):
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

def kswin(seed, alpha): return drift.KSWIN(alpha=alpha, window_size=100, stat_size=30, seed=seed)
def adwin(c): return drift.ADWIN(delta=0.002, clock=c)
def make_arf(seed, c): return forest.ARFClassifier(n_models=10, seed=seed, drift_detector=adwin(c))

# ─── Targeted Execution Loop (Alpha Sweep) ────────────────────────────────────
def process_transition_seed(trans, seed):
    # Strict RNG isolation per worker for bit-wise reproducibility
    # C-Level Overflow Prevention: apply modulo for Cython-compiled extensions
    safe_seed = seed % (2**31 - 1)
    np.random.seed(safe_seed)
    random.seed(safe_seed)
    
    from_t, to_t, w, name = trans
    out = []
    for regime, params in [('IID', ETF_PARAMS_A), ('Cal. A', ETF_PARAMS_A), ('Cal. B', ETF_PARAMS_B)]:
        df, dpts = simulate_stream(params[from_t], params[to_t], regime, w, seed=seed)
        tau = max(1000, w)

        def rec(detector_label, dets):
            add, f1 = evaluate(dets, dpts, len(df), tau)
            out.append([regime, detector_label, 1, name, w, f1, add, seed])

        for alpha in [0.001, 0.005, 0.01, 0.05]:
            det_label = f'KSWIN_a_{alpha}'
            rec(det_label, run_concept_drift_kswin(df, make_arf(seed, 1), lambda s=seed, a=alpha: kswin(s, a)))
            
    return out

# ─── Bootstrap CI & Formatting ────────────────────────────────────────────────
def bootstrap_ci_half_width(series, n_resamples=1000):
    arr = series.dropna().values
    if len(arr) < 2: return 0.0
    resamples = np.random.choice(arr, size=(n_resamples, len(arr)), replace=True)
    means = np.mean(resamples, axis=1)
    return (np.percentile(means, 97.5) - np.percentile(means, 2.5)) / 2.0

def format_cell(mean_val, ci_val, is_f1=False):
    if pd.isna(mean_val) or (not is_f1 and np.isinf(mean_val)): return "N/A" if is_f1 else r"$\infty$"
    if is_f1:
        s = f"{float(mean_val):.2f}"
        return (s + r" {\small $\pm$" + f"{float(ci_val):.2f}" + r"}") if (not pd.isna(ci_val) and float(ci_val) > 0.005) else s
    mi = int(round(float(mean_val)))
    return (f"{mi}" + r" {\small $\pm$" + f"{int(round(float(ci_val)))}" + r"}") if (not pd.isna(ci_val) and float(ci_val) > 0.5) else str(mi)

# ─── Statistical Tests ────────────────────────────────────────────────────────
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
    return {'pipeline_A': labelA, 'pipeline_B': labelB,
            'n_det_A': int(gA['n_det'].sum()), 'n_total_A': int(gA['n_streams'].sum()), 
            'n_det_B': int(gB['n_det'].sum()), 'n_total_B': int(gB['n_streams'].sum()),
            'sign_test_p': sign_p}

# ─── LaTeX Assembly ───────────────────────────────────────────────────────────
ROW_SPECS = [
    (r"\textbf{KSWIN ($\alpha = 0.001$) + ARF}", 'KSWIN_a_0.001', 1, True),
    (r"\textbf{KSWIN ($\alpha = 0.005$) + ARF}", 'KSWIN_a_0.005', 1, True),
    (r"\textbf{KSWIN ($\alpha = 0.01$) + ARF}",  'KSWIN_a_0.01',  1, True),
    (r"\textbf{KSWIN ($\alpha = 0.05$) + ARF}",  'KSWIN_a_0.05',  1, True),
]
REG_DISPLAY = [('IID', 'IID Baseline'), ('Cal. A', 'Cal. A'), ('Cal. B', 'Cal. B')]

def cell_pair(agg, detector, clock, regime_raw, is_kswin):
    r = agg[(agg.Detector == detector) & (agg.Clock == clock) & (agg.Calibration == regime_raw)]
    if r.empty: return ["N/A", "N/A"]
    f1 = format_cell(r.F1_mean.values[0], r.F1_ci.values[0], is_f1=True)
    if is_kswin and not pd.isna(r.ADD_mean.values[0]):
        raw = int(round(r.ADD_mean.values[0]))
        add = f"{raw} [{max(0, raw - KSWIN_LAG)}]"
    else:
        add = format_cell(r.ADD_mean.values[0], r.ADD_ci.values[0], is_f1=False)
    return [f1, add]

def build_table(agg):
    caption = (r"KSWIN sensitivity sweep ($\alpha \in \{0.001, 0.005, 0.01, 0.05\}$) on heteroscedastic ProteuS streams "
               r"(12 transitions $\times$ 30 seeds $=$ 360 runs per cell). Evaluates the robustness of the distribution-based "
               r"test against false-alarm flooding under high GARCH variance (Cal. B). Mean $\pm$ 95\% CI (1000 bootstrap resamples).")
    L = [r"\begin{table*}[t]", r"  \centering", rf"  \caption{{{caption}}}",
         r"  \label{tab:kswin_alpha_sweep}", r"  \begin{tabular}{@{}lrrrrrr@{}}", r"    \toprule",
         r"                                                   & \multicolumn{2}{c}{\textbf{IID Baseline}} & \multicolumn{2}{c}{\textbf{Cal. A (Low GARCH)}} & \multicolumn{2}{c}{\textbf{Cal. B (High GARCH)}} \\",
         r"    \cmidrule(lr){2-3} \cmidrule(lr){4-5} \cmidrule(lr){6-7}",
         r"    \textbf{Pipeline Configuration}                & \textbf{F1} & \textbf{ADD} & \textbf{F1} & \textbf{ADD} & \textbf{F1} & \textbf{ADD} \\",
         r"    \midrule"]
    for spec in ROW_SPECS:
        label, det, clk, ks = spec
        cells = []
        for reg_raw, _ in REG_DISPLAY:
            cells += cell_pair(agg, det, clk, reg_raw, ks)
        L.append(f"    {label:46s} & " + " & ".join(cells) + r" \\")
    L += [r"    \bottomrule", r"  \end{tabular}", r"\end{table*}", ""]
    return "\n".join(L)

# ─── Main ────────────────────────────────────────────────────────────────────
def main():
    grid = list(itertools.product(TRANSITIONS, SEEDS))
    print(f"[run] {len(TRANSITIONS)} transitions x {N_SEEDS} seeds x 4 alphas x 3 regimes")
    print("[run] Parallel execution (Joblib) - Please wait...")
    nested = Parallel(n_jobs=-1)(delayed(process_transition_seed)(t, s) for t, s in tqdm(grid, desc="R4 KSWIN Sweep"))
    df = pd.DataFrame([row for sub in nested for row in sub],
                      columns=['Calibration', 'Detector', 'Clock', 'Dataset', 'w', 'F1', 'ADD', 'Seed'])
    df.to_csv(RAW_CSV, index=False)

    sign = pd.DataFrame([
        analyze_pair(df, (df.Detector == 'KSWIN_a_0.005'), (df.Detector == 'KSWIN_a_0.05'),
                     "KSWIN a=0.005", "KSWIN a=0.05")
    ])
    sign.to_csv(SIGN_CSV, index=False)

    # C-Level Overflow Prevention applied to the bootstrap global seed
    safe_bootstrap_seed = BOOTSTRAP_SEED % (2**31 - 1)
    np.random.seed(safe_bootstrap_seed)
    agg = df.groupby(['Detector', 'Clock', 'Calibration']).agg(
        F1_mean=('F1', 'mean'), F1_ci=('F1', bootstrap_ci_half_width),
        ADD_mean=('ADD', lambda x: np.nan if x.dropna().empty else x.dropna().mean()),
        ADD_ci=('ADD', bootstrap_ci_half_width)).reset_index()

    tex = build_table(agg)
    OUT_TEX.write_text(tex, encoding='utf-8')
    print(f"[ok] KSWIN table -> {OUT_TEX}\n")

if __name__ == "__main__":
    main()