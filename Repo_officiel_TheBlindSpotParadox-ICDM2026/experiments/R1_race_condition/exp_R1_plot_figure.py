"""
exp_R1_plot_figure.py
Renders Figure 1 (race condition) from R1_race_condition.parquet: one panel per
lambda showing the joint stopping times (tau_ARF, tau_det) on a broken linear
x-axis, with a deterministic 2D jitter (one seeded generator per lambda panel)
applied to the censored/starved runs to keep the scatter cloud readable.
"""
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# [IEEE/ICDM FAIR Compliance] Dynamic path resolution aligned with data generator
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
RESULTS_DIR = ROOT_DIR / "results" / "R1_race_condition" / "data"
FIG_DIR = ROOT_DIR / "results" / "R1_race_condition" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

def plot_tau_scatter(df_diag):
    import matplotlib.gridspec as gridspec
    import matplotlib.lines as mlines
    
    lambdas = [5.0, 10.0, 25.0, 100.0]
    # Extreme aspect ratio (1x4) tailored for IEEE page width (\textwidth)
    fig = plt.figure(figsize=(14, 3.2), dpi=300)
    outer_gs = gridspec.GridSpec(1, 4, wspace=0.18)

    for i, l in enumerate(lambdas):
        # Subgrid per lambda: width 3 for the active zone [0-800], 1 for the censored zone [49k-56k]
        inner_gs = gridspec.GridSpecFromSubplotSpec(1, 2, subplot_spec=outer_gs[i], wspace=0.08, width_ratios=[3, 1])
        ax_left = fig.add_subplot(inner_gs[0])
        ax_right = fig.add_subplot(inner_gs[1], sharey=ax_left)

        sub = df_diag[df_diag['lambda_val'] == l]
        mask_both = sub['tau_arf_finite'] & sub['tau_det_emp_finite']
        bs_mask = mask_both & (sub['tau_arf'] < sub['tau_det_emp'])
        win_mask = mask_both & (sub['tau_arf'] >= sub['tau_det_emp'])
        starved_mask = sub['tau_arf_finite'] & (~sub['tau_det_emp_finite'])

        # [IEEE/ICDM FAIR Compliance] Deterministic RNG for visual jitter to guarantee bit-wise identical PNGs
        rng_jitter = np.random.default_rng(int(l) * 42)
        y_starved = sub[starved_mask]['tau_arf'].values
        n_starved = len(y_starved)
        
        if n_starved > 0:
            jitter_y = rng_jitter.uniform(-15, 15, size=n_starved)
            jitter_x = rng_jitter.uniform(53000, 55000, size=n_starved)
        else:
            jitter_y, jitter_x = None, None

        # Data repetition on both axes (xlim acts as a visual filter)
        for ax in (ax_left, ax_right):
            ax.scatter(sub[bs_mask]['tau_det_emp'], sub[bs_mask]['tau_arf'], color='red', alpha=0.6, s=18)
            ax.scatter(sub[win_mask]['tau_det_emp'], sub[win_mask]['tau_arf'], color='green', alpha=0.6, s=18)
            
            # Add 2D jitter (X and Y) to render censored density readable as a scatter cloud
            if n_starved > 0:
                ax.scatter(jitter_x, y_starved + jitter_y, marker='x', color='gray', alpha=0.4, s=18)
            
            ax.set_ylim(-10, 600)
            ax.grid(True, alpha=0.3, linestyle='--')

        # Scale constraints redefined to create typographic whitespace around the broken axis
        ax_left.set_xlim(-20, 700)
        ax_right.set_xlim(48000, 57000)

        # Formatting and topological cleanup: the last left tick is pushed to 600
        ax_left.set_xticks([0, 300, 600])
        ax_right.set_xticks([50000, 55000])
        ax_right.set_xticklabels(["50k", "55k"])
        ax_left.set_title(rf"$\lambda = {l}$", fontsize=10, fontweight='bold', pad=10)

        # The y=x bisector mathematically and logically exists ONLY on the left panel
        x_line = np.array([0, 600])
        ax_left.plot(x_line, x_line, 'k--', alpha=0.5, lw=1)

        # Remove central spines (merging the two subplots)
        ax_left.spines['right'].set_visible(False)
        ax_right.spines['left'].set_visible(False)
        ax_right.yaxis.set_ticks_position('none')
        plt.setp(ax_right.get_yticklabels(), visible=False)
        
        # Share Y-axis for columns 2, 3, and 4
        if i > 0:
            ax_left.yaxis.set_ticks_position('none')
            plt.setp(ax_left.get_yticklabels(), visible=False)

        # Inject more pronounced oblique markers (broken axis)
        d = 0.03
        kwargs = dict(transform=ax_left.transAxes, color='black', clip_on=False, lw=1.2)
        ax_left.plot((1-d, 1+d), (-d, +d), **kwargs)
        ax_left.plot((1-d, 1+d), (1-d, 1+d), **kwargs)
        kwargs.update(transform=ax_right.transAxes)
        ax_right.plot((-d, +d), (-d, +d), **kwargs)
        ax_right.plot((-d, +d), (1-d, 1+d), **kwargs)

    # Create a single global legend extracted above the figure
    r_marker = mlines.Line2D([], [], color='red', marker='o', linestyle='None', alpha=0.6, label=r'Blind Spot ($\tau_{ARF} < \tau_{det}$)')
    g_marker = mlines.Line2D([], [], color='green', marker='o', linestyle='None', alpha=0.6, label=r'Detector Wins ($\tau_{det} \leq \tau_{ARF}$)')
    x_marker = mlines.Line2D([], [], color='gray', marker='x', linestyle='None', alpha=0.5, label=r'Starved (Censored $\tau_{det}$)')
    fig.legend(handles=[r_marker, g_marker, x_marker], loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=3, frameon=False, fontsize=10)

    # Share labels (minimal ink) - Y-axis pushed out to free ticks
    fig.text(0.5, -0.05, r"$\tau_{det}$ (External CUSUM)", ha='center', fontsize=11)
    fig.text(0.04, 0.5, r"$\tau_{ARF}$ (Internal Swap)", va='center', rotation='vertical', fontsize=11)

    plt.subplots_adjust(bottom=0.15, top=0.85, left=0.08, right=0.98)
    # Bbox_inches='tight' secures the inclusion of the extracted legend
    plt.savefig(FIG_DIR / "Fig_R1_race_condition.png", bbox_inches='tight')
    plt.close()

def main():
    data_path = RESULTS_DIR / "R1_race_condition.parquet"
    try:
        df_diag = pd.read_parquet(data_path)
        print(f"[INFO] Successfully loaded data from {data_path}. Generating plot...")
        plot_tau_scatter(df_diag)
        print(f"[SUCCESS] Figure R1 saved to {FIG_DIR / 'Fig_R1_race_condition.png'}")
    except FileNotFoundError:
        print(f"[ERROR] Data file not found at {data_path}. Please run the diagnostic script first.")
        raise

if __name__ == "__main__":
    main()