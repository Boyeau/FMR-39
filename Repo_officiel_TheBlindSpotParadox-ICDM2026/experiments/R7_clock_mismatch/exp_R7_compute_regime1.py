# exp_R7_compute_regime1.py
"""
exp_R7_compute_regime1.py
Builds the Regime-1 (clock-mismatch) miss-rate summary from the R7 instrumentation parquet.
For each clock configuration it aggregates the blind-spot miss rate miss = P(tau_arf < tau_det)
as a function of the drift magnitude Delta_e, and emits the compact summary table that backs the
"Regime 1: The Clock-Mismatch Artefact" subsection of the manuscript.
Inputs : results/R7_clock_mismatch/data/R7_clock_mismatch.parquet
Outputs: results/R7_clock_mismatch/tables/exp_R7_regime1_miss_curve.csv    (full curve per config)
         results/R7_clock_mismatch/tables/exp_R7_regime1_miss_summary.tex  (per-config / per-band)
"""
import numpy as np
import pandas as pd
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DATA   = ROOT_DIR / "results" / "R7_clock_mismatch" / "data" / "R7_clock_mismatch.parquet"
TABLES = ROOT_DIR / "results" / "R7_clock_mismatch" / "tables"
TABLES.mkdir(parents=True, exist_ok=True)

CONFIG_LABEL = {
    "A_mismatched": r"Mismatched ($c_{\mathrm{int}}{=}1,\ c_{\mathrm{ext}}{=}32$)",
    "B_matched":    r"Matched ($c_{\mathrm{int}}{=}1,\ c_{\mathrm{ext}}{=}1$)",
    "C_decoupled":  r"Decoupled ($c_{\mathrm{int}}{=}32,\ c_{\mathrm{ext}}{=}1$)",
}
BANDS = [(r"$\Delta e \le 0.15$",          -np.inf, 0.15),
         (r"$0.15 < \Delta e \le 0.35$",    0.15,   0.35),
         (r"$\Delta e > 0.35$",             0.35,   np.inf)]

df = pd.read_parquet(DATA)
df["miss"] = df["tau_arf"].fillna(np.inf) < df["tau_det"].fillna(np.inf)

# Full curve: miss rate per (config, delta_e)
(df.groupby(["config", "delta_e"])["miss"].mean()
   .reset_index().rename(columns={"miss": "miss_rate"})
   .to_csv(TABLES / "exp_R7_regime1_miss_curve.csv", index=False))

# Compact summary: mean miss rate per config per magnitude band
rows = []
for cid in ["A_mismatched", "B_matched", "C_decoupled"]:
    g = df[df.config == cid]
    cells = []
    for _, lo, hi in BANDS:
        sub = g[(g.delta_e > lo) & (g.delta_e <= hi)]
        cells.append(rf"${100 * sub['miss'].mean():.0f}\%$" if len(sub) else "---")
    rows.append((CONFIG_LABEL[cid], cells))

tex = [r"\begin{tabular}{@{}lccc@{}}", r"  \toprule",
       r"  Clock configuration & " + " & ".join(b[0] for b in BANDS) + r" \\", r"  \midrule"]
tex += [f"  {label} & " + " & ".join(cells) + r" \\" for label, cells in rows]
tex += [r"  \bottomrule", r"\end{tabular}"]
(TABLES / "exp_R7_regime1_miss_summary.tex").write_text("\n".join(tex) + "\n", encoding="utf-8")

print("[R7] Blind-spot miss rate by clock configuration and drift-magnitude band:")
for label, cells in rows:
    plain = "  ".join(c.replace("$", "").replace(r"\%", "%") for c in cells)
    print(f"      {label:48s} {plain}")
print(f"[R7] curve   -> {TABLES / 'exp_R7_regime1_miss_curve.csv'}")
print(f"[R7] summary -> {TABLES / 'exp_R7_regime1_miss_summary.tex'}")