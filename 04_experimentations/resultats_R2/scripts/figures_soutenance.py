"""
figures_soutenance.py
===================================================================
Figure nouvelle de la soutenance du 16/09/2026 : la preuve accumulee avant
le premier remplacement, S_pre = max_{t < tau_ARF} S_t, contre les seuils.

Par l'identite de course (rapport, Proposition 4), le detecteur arrive le
premier si et seulement si S_pre >= lambda. La figure montre donc directement
ou se situe la transition en lambda, et pourquoi elle se deplace avec Delta_e.

LECTURE SEULE sur les donnees. Ecrit figures/slides_latex/Fig_slide_spre.png,
texte en Latin Modern Sans (meme police que Beamer, via figures_slides).

USAGE
    PYTHONHASHSEED=0 python figures_soutenance.py
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from figures_slides import _police_latex

RACINE = Path(__file__).resolve().parents[1]
DATA = RACINE / "resultats" / "data"
SORTIE = RACINE / "resultats" / "figures" / "slides_latex" / "Fig_slide_spre.png"
H, DELTA_P = 2000, 0.01


def s_pre_par_run():
    ind = pd.read_parquet(DATA / "QCD_indicateurs_full.parquet").sort_values("run_id").reset_index(drop=True)
    tr = pd.read_parquet(DATA / "QCD_traces_error_full.parquet").sort_values(["run_id", "t"])
    E = tr["e"].to_numpy(dtype=float).reshape(len(ind), H)
    inc = E - (ind["p_hat_0"].to_numpy() + DELTA_P)[:, None]
    s = np.zeros(len(ind))
    cum = np.zeros(len(ind))
    tau = ind["tau_arf"].to_numpy().astype(int)
    s_pre = np.zeros(len(ind))
    for t in range(H):
        s = np.maximum(0.0, s + inc[:, t])
        cum = np.maximum(cum, s)
        # S_pre est le max jusqu'a t = tau_ARF - 1 inclus
        fige = tau == t + 1
        s_pre[fige] = cum[fige]
    return ind, s_pre


def main():
    ind, s_pre = s_pre_par_run()
    for lam in (8, 25):
        gagne = (~ind[f"censored_det_{lam}"]) & (ind[f"tau_det_{lam}"] < ind["tau_arf"])
        print(f"controle identite lambda = {lam} : {int((gagne.to_numpy() == (s_pre >= lam)).sum())}/{len(ind)}")
    q = pd.DataFrame({"de": ind["delta_e"], "s": s_pre}).groupby("de")["s"].quantile([0.25, 0.5, 0.75]).unstack()
    print("S_pre par amplitude, quartiles :")
    print(q.round(1).to_string())

    plt.rcParams.update(_police_latex())
    plt.rcParams.update({"font.size": 13})
    fig, ax = plt.subplots(figsize=(8.2, 4.1))
    x = q.index.to_numpy()
    ax.axvspan(0, 0.10, color="0.92", lw=0)
    ax.fill_between(x, q[0.25], q[0.75], color="#9fb4d6", alpha=0.6, lw=0, label="middle half of the runs")
    ax.plot(x, q[0.5], color="#1f3a68", lw=2.2, marker="o", ms=4, label="median")
    for lam, ls in [(8, ":"), (15, "--"), (25, "-.")]:
        ax.axhline(lam, color="#8a1c1c", ls=ls, lw=1.3)
        ax.text(0.505, lam, f"  threshold {lam}", va="center", ha="left", color="#8a1c1c", fontsize=12)
    ax.set_xlim(0, 0.50)
    ax.set_ylim(0, 30)
    ax.set_xlabel("size of the change")
    ax.set_ylabel("evidence before the first repair")
    ax.text(0.05, 28.5, "weak signal", ha="center", va="top", color="0.35", fontsize=11)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="upper right", frameon=False, fontsize=11, bbox_to_anchor=(0.86, 1.0))
    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(SORTIE, dpi=200, bbox_inches="tight")
    print(f"figure : {SORTIE.name}")


if __name__ == "__main__":
    main()
