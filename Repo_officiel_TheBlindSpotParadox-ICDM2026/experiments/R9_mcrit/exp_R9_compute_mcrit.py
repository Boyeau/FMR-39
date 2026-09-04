import warnings
import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

warnings.filterwarnings("ignore", category=RuntimeWarning)

# --------------------------------------------------------------------
# Parameters
# --------------------------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
RESULTS_DIR = ROOT_DIR / "results" / "R9_mcrit" / "data"
FIG_DIR = ROOT_DIR / "results" / "R9_mcrit" / "figures"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)

LAMBDAS = [8, 25, 50]                 # Three calibrations from the paper
DELTA_P = 0.005                       # CUSUM tolerance
BETAS = [0.50, 0.05]                  # Main beta + complement
DKW_ALPHA = 0.05                      # 95% DKW confidence band
TARGET_DELTAS = [0.10, 0.15, 0.20, 0.25, 0.33, 0.40, 0.50]
PALETTE = {8: "#00748C", 25: "#E08000", 50: "#3B6FA0"}  # teal / orange / navy


# --------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------
def mcrit_from_F(F, beta):
    """
    M_crit = floor( ln(beta) / ln(1-F) ), STRICTLY DECREASING with respect to F.
    F <= 0: no adaptation observed before tau_det* -> no finite M
            starves the detector -> +inf.
    F >= 1: a single tree is already sufficient to starve the detector -> 0.
    """
    if not np.isfinite(F):
        return np.nan
    if F <= 0.0:
        return np.inf
    if F >= 1.0:
        return 0.0
    return float(np.floor(np.log(beta) / np.log(1.0 - F)))


def empirical_cdf_at(data, x):
    """F_emp(x) = proportion of observations <= x."""
    data = np.asarray(data, dtype=float)
    return float(np.mean(data <= x))


def best_alt_cdf_at(data, x):
    """
    Best heavy-tailed alternative (lognorm / weibull_min, floc=0),
    selected via the lowest KS statistic. Returns (F_alt, name).
    Strictly informational: the paper's narrative does not rely on this.
    """
    best_name, best_stat, best_cdf = "N/A", np.inf, np.nan
    for name in ("lognorm", "weibull_min"):
        dist = getattr(stats, name)
        try:
            params = dist.fit(data, floc=0.0)
            ks_stat, _ = stats.kstest(data, name, args=params)
            if ks_stat < best_stat:
                best_stat, best_name = ks_stat, name
                best_cdf = float(dist.cdf(x, *params))
        except Exception:
            continue
    return best_cdf, best_name


def ks_bootstrap_expon(data, n_boot=2000, seed=42):
    """
    Performs a Kolmogorov-Smirnov test with parametric bootstrap (N=2000)
    to test the null hypothesis that data follows an exponential distribution.
    Returns the empirical p-value.
    """
    rng = np.random.default_rng(seed)
    n = len(data)
    mean_emp = np.mean(data)
    
    # Empirical KS statistic against Expon(scale=mean_emp)
    D_emp, _ = stats.kstest(data, 'expon', args=(0, mean_emp))
    
    # Parametric bootstrap
    boot_stats = np.empty(n_boot)
    for i in range(n_boot):
        boot_sample = rng.exponential(scale=mean_emp, size=n)
        boot_mean = np.mean(boot_sample)
        D_boot, _ = stats.kstest(boot_sample, 'expon', args=(0, boot_mean))
        boot_stats[i] = D_boot
        
    return float(np.mean(boot_stats >= D_emp))


# --------------------------------------------------------------------
# Main
# --------------------------------------------------------------------
def main():
    print("=== START: Empirical vs Exponential M_crit (real stream data) ===")

    file_path = RESULTS_DIR / "results_instrumented_A_ADWIN_HAT.csv"
    if not file_path.exists():
        raise FileNotFoundError(
            f"CRITICAL ERROR: {file_path} not found. Halting. "
            "Ensure Stage 1 (exp_R9_generate_data.py) has been executed."
        )

    print(f"[INFO] Real instrumentation data: {file_path.name}")
    df = pd.read_csv(file_path)
    for col in ("boundary_shift", "tau_hat"):
        if col not in df.columns:
            raise ValueError(f"Required column missing: {col}")
    print(f"[INFO] Read {len(df)} rows.")

    df["delta_e_eff"] = stats.norm.cdf(df["boundary_shift"] / np.sqrt(2)) - 0.5
    unique_eff = np.sort(df["delta_e_eff"].unique())

    rows = []
    print("\n--- CELL-BY-CELL EVALUATION ---")
    print("Conservatism Rule: F_exp <= F_emp <=> Exponential distribution is "
          "conservative (yields an UPPER BOUND on M_crit).")

    for target in TARGET_DELTAS:
        if unique_eff.size == 0:
            continue
        de_eff = unique_eff[np.argmin(np.abs(unique_eff - target))]
        bs_src = df.loc[df["delta_e_eff"] == de_eff, "boundary_shift"].iloc[0]
        data = df.loc[df["boundary_shift"] == bs_src, "tau_hat"].dropna().values
        n = data.size
        if n < 10:
            print(f"  -> Step {target:.2f} ignored (insufficient N={n}).")
            continue

        mean_tau = float(np.mean(data))
        eps_dkw = float(np.sqrt(np.log(2.0 / DKW_ALPHA) / (2.0 * n)))  # DKW band

        # Fair/AE requirement: KS Test with parametric bootstrap (N=2000)
        p_boot = ks_bootstrap_expon(data, n_boot=2000, seed=int(target * 1000))
        rejected = "REJECTED (p < 0.05)" if p_boot < 0.05 else "ACCEPTED (p >= 0.05)"
        print(f"\n  [FAIR] KS Bootstrap N=2000 (Expon approx) at De~{de_eff:.3f}: p_boot={p_boot:.4f} -> {rejected}")

        for lam in LAMBDAS:
            tau_det_star = lam / (de_eff - DELTA_P)
            F_emp = empirical_cdf_at(data, tau_det_star)
            F_exp = 1.0 - np.exp(-tau_det_star / mean_tau)
            F_alt, alt_name = best_alt_cdf_at(data, tau_det_star)

            verdict = "CONSERVATIVE" if F_exp <= F_emp else "ANTI-CONSERVATIVE"
            F_emp_low = max(0.0, F_emp - eps_dkw)  # borne basse -> M_crit max (defensif)
            pmiss_m10 = 1.0 - (1.0 - F_emp) ** 10

            for beta in BETAS:
                m_emp = mcrit_from_F(F_emp, beta)
                m_exp = mcrit_from_F(F_exp, beta)
                m_alt = mcrit_from_F(F_alt, beta) if np.isfinite(F_alt) else np.nan
                m_emp_dkw_up = mcrit_from_F(F_emp_low, beta)  # Lower bound -> M_crit max (defensive)
                coherent = (m_exp >= m_emp) == (F_exp <= F_emp)

                rows.append({
                    "delta_e": round(target, 3),
                    "delta_e_eff": round(de_eff, 4),
                    "lambda": lam,
                    "beta": beta,
                    "n_samples": n,
                    "E_tau_HAT": round(mean_tau, 2),
                    "tau_det_star": round(tau_det_star, 2),
                    "F_emp": round(F_emp, 4),
                    "F_exp": round(F_exp, 4),
                    "F_alt": round(F_alt, 4) if np.isfinite(F_alt) else np.nan,
                    "alt_dist": alt_name,
                    "Mcrit_emp": m_emp,
                    "Mcrit_exp": m_exp,
                    "Mcrit_alt": m_alt,
                    "Mcrit_emp_dkw_up": m_emp_dkw_up,
                    "Pmiss_M10": round(pmiss_m10, 4),
                    "verdict_conservatism": verdict,
                    "coherence_check": bool(coherent),
                })

            print(f"  De~{de_eff:.3f} | lam={lam:>2} | tau*={tau_det_star:8.1f} | "
                  f"F_emp={F_emp:.3f} F_exp={F_exp:.3f} | "
                  f"Mcrit(.50) emp={mcrit_from_F(F_emp,0.5)} exp={mcrit_from_F(F_exp,0.5)} | "
                  f"{verdict}")

    res = pd.DataFrame(rows)
    out_csv = RESULTS_DIR / "exp_R9_mcrit_comparison.csv"
    res.to_csv(out_csv, index=False)
    print(f"\n[INFO] Comparison table exported to: {out_csv}")

    # ----------------------------------------------------------------
    # Figure: M_crit emp (solid) vs exp (dashed) vs Delta_e, by lambda
    # ----------------------------------------------------------------
    # Figure restricted to the BLIND-SPOT REGIME (Delta_e > 0.20) and lambda in {25, 50}.
    # Justification: For Delta_e < 0.20 (Safe Zone), the detector wins, M_crit is
    # large/volatile (up to +inf when F_emp=0 at N=100). These points are NOT relevant
    # to the structural claim. Restricting the DOMAIN cleanly removes out-of-scale
    # peaks, inf values, and prevents matplotlib from connecting points over gaps.
    sub = res[(res["beta"] == 0.50) & (res["delta_e_eff"] > 0.20)].copy()
    FIG_LAMBDAS = [25, 50]
    CAP = 10
    fig, ax = plt.subplots(figsize=(7.0, 4.3), dpi=300)
    for lam in FIG_LAMBDAS:
        s = sub[sub["lambda"] == lam].sort_values("delta_e_eff")
        x = s["delta_e_eff"].values
        m_emp = s["Mcrit_emp"].astype(float).values
        m_exp = s["Mcrit_exp"].astype(float).values
        finite = np.isfinite(m_emp)  # Safety check: no inf expected in this regime
        if (~finite).any():
            print(f"  [WARNING] Unexpected inf (lambda={lam}) in the plotted regime.")
        c = PALETTE[lam]
        ax.plot(x[finite], m_emp[finite], "-o", color=c, lw=2.0, ms=5,
                label=rf"$M_{{\rm crit}}^{{\rm emp}}\ (\lambda={lam})$")
        ax.plot(x, np.clip(m_exp, 0, CAP), "--", color=c, lw=1.6, alpha=0.85,
                label=rf"$M_{{\rm crit}}^{{\rm exp}}\ (\lambda={lam})$")
    ax.axhline(10, color="0.35", ls=":", lw=1.4)
    ax.text(0.015, 0.9, "River default $M=10$", transform=ax.transAxes,
            ha="left", va="top", fontsize=8, color="0.35")
    ax.set_xlabel(r"Effective error jump $\Delta e$")
    ax.set_ylabel(r"Critical ensemble size $M_{\rm crit}$  ($\beta=0.50$)")
    ax.set_ylim(-0.5, CAP + 0.8)
    ax.set_title(r"Empirical vs exponential $M_{\rm crit}$ (blind-spot regime, real $\tau_{\rm HAT}$)",
                 fontweight="bold", pad=10)
    ax.grid(alpha=0.3, ls="--")
    ax.legend(fontsize=8, ncol=2, loc="upper right", framealpha=0.9)
    plt.tight_layout()
    fig_path = FIG_DIR / "Fig_R9_Mcrit_empirical_vs_exp.png"
    plt.savefig(fig_path)
    plt.close()
    print(f"[INFO] Figure exported (blind-spot Delta_e>0.20, lambda in {FIG_LAMBDAS}): {fig_path}")

    # ----------------------------------------------------------------
    # Diagnostic Routing (Conservatism Check)
    # ----------------------------------------------------------------
    cells = res.drop_duplicates(subset=["delta_e_eff", "lambda"])
    n_anti = int((cells["verdict_conservatism"] == "ANTI-CONSERVATIVE").sum())
    n_cons = int((cells["verdict_conservatism"] == "CONSERVATIVE").sum())
    n_bad = int((~res["coherence_check"]).sum())

    print("\n=== ROUTING DECISION (Monotonicity Check) ===")
    print(f"Conservative cells (F_exp <= F_emp)    : {n_cons}")
    print(f"Anti-conservative cells (F_exp > F_emp): {n_anti}")
    if n_bad:
        print(f"[WARNING] {n_bad} monotonicity/verdict incoherences found.")
    if n_anti == 0:
        print("-> Conservative upper bound VALID EVERYWHERE.")
    elif n_cons == 0:
        print("-> Conservative bound INVALID EVERYWHERE.")
    else:
        print("-> MIXED conservatism depending on (Delta_e, lambda).")
    print("RECOMMENDATION: Distribution-free evaluation (M_crit on empirical CDF F_emp) "
          "— robust regardless of sign, drops any parametric assumption.")


if __name__ == "__main__":
    main()