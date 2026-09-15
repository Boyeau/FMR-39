"""
matrice_correlations.py
===================================================================
Matrice de correlation de toutes les mesures, globale puis par amplitude
(question D.3.bis de l'encadrant, 15/09/2026), et verification de
l'identite de course.

LECTURE SEULE sur les donnees : ne resimule rien, n'ecrit aucune table.
Ecrit une seule figure, nouvelle : Fig_QD_matrice_correlations_full.png.

CE QUE LE SCRIPT ETABLIT
  1. Identite de course. Le detecteur gagne (tau_det < tau_ARF) si et seulement
     si la pile a atteint lambda AVANT le premier remplacement :
         max_{t < tau_ARF} S_t >= lambda.
     C'est une identite sur la trajectoire, pas une approximation ; le script la
     verifie run par run contre QCD_indicateurs_full aux trois seuils.
  2. Matrice globale contre matrice stratifiee. Kendall tau_b, censure imputee
     a H (meme convention que analyse_QCD.kendall_censored). Globale : 2 000 runs
     empiles. Stratifiee : mediane sur les 18 amplitudes du domaine de decision
     (Delta_e >= 0,10), avec le nombre d'amplitudes ou |tau_b| depasse le seuil
     de detectabilite 0,13295637.
  3. Groupes de mesures : classification hierarchique sur 1 - |tau_b stratifie|.

Mesures (une valeur par run) :
  tau_ARF, tau_swap(25/50/75 %)      dates de remplacement (plus petit = plus tot)
  S_pre                              max de S_t avant tau_ARF (preuve disponible pour la course)
  S_max(H), A(H), A(w)               preuve et degats, horizon complet et fenetre courte
  G                                  part de la preuve acquise a tau_ARF
  tau_det(8), tau_det(25)            dates d'alarme
  etalon (aire), t_50                etalon analytique d'Ulysse : aire de acc_bande sur
                                     [0, 500], et premier instant ou acc_bande >= 0,5
  p0_hat                             socle estime (temoin de bruit)

EXPLORATOIRE : la liste des mesures et la figure sont posees le 15/09, apres D.3.

USAGE
    PYTHONHASHSEED=0 python matrice_correlations.py
"""

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import leaves_list, linkage
from scipy.spatial.distance import squareform
from scipy.stats import kendalltau

RACINE = Path(__file__).resolve().parents[1]
DATA = RACINE / "resultats" / "data"
FIGURES = RACINE / "resultats" / "figures"
H, DELTA_P, SEUIL = 2000, 0.01, 0.13295637


def tau_b(x, y):
    xf = np.where(np.isnan(x), H, x)
    yf = np.where(np.isnan(y), H, y)
    if np.all(xf == xf[0]) or np.all(yf == yf[0]):
        return np.nan
    return float(kendalltau(xf, yf).statistic)


def charger():
    ind = pd.read_parquet(DATA / "QCD_indicateurs_full.parquet").sort_values("run_id").reset_index(drop=True)
    tr = pd.read_parquet(DATA / "QCD_traces_error_full.parquet").sort_values(["run_id", "t"])
    E = tr["e"].to_numpy(dtype=float).reshape(len(ind), H)
    p0 = ind["p_hat_0"].to_numpy()

    inc = E - (p0 + DELTA_P)[:, None]
    S = np.empty_like(E)
    s = np.zeros(len(ind))
    for t in range(H):
        s = np.maximum(0.0, s + inc[:, t])
        S[:, t] = s
    ecart = np.abs(S.max(axis=1) - ind["S_max_H"].to_numpy()).max()
    print(f"[controle] S_max(H) recalcule contre la table : ecart maximal {ecart:.2e}")

    tau = ind["tau_arf"].to_numpy(dtype=float)          # jamais censure
    Mcum = np.maximum.accumulate(S, axis=1)
    idx = np.clip(tau.astype(int) - 1, 0, H - 1)
    s_pre = np.where(tau >= 1, Mcum[np.arange(len(ind)), idx], 0.0)

    w = np.array([int(min(H, max(1, round(3 * 18.5 / de)))) for de in ind["delta_e"]])
    a_w = np.array([(E[i, :w[i]] - p0[i]).sum() for i in range(len(ind))])

    et = pd.read_parquet(DATA / "QCD_etalon_par_run.parquet").set_index("run_id").loc[ind["run_id"]]
    so = pd.read_parquet(DATA / "QCD_etalon_sondes_full_M10.parquet")
    so = so[so["region"] == "bande"].assign(acc=lambda d: d.n_vote_nouvelle / d.n_sondes)
    bande = so.pivot(index="run_id", columns="t", values="acc").loc[ind["run_id"]]
    atteint = bande.to_numpy() >= 0.5
    t50 = bande.columns.to_numpy()[atteint.argmax(axis=1)].astype(float)
    t50[~atteint.any(axis=1)] = np.nan

    def date(col, cens):
        return np.where(ind[cens], np.nan, ind[col]).astype(float)

    mesures = pd.DataFrame({
        "tau_ARF": tau,
        "tau_swap(25%)": date("tau_swap_25", "censored_swap_25"),
        "tau_swap(50%)": date("tau_swap_50", "censored_swap_50"),
        "tau_swap(75%)": date("tau_swap_75", "censored_swap_75"),
        "S_pre": s_pre,
        "S_max(H)": ind["S_max_H"].to_numpy(),
        "A(H)": ind["A_H"].to_numpy(),
        "A(w)": a_w,
        "G": ind["G_tau_arf"].to_numpy(dtype=float),
        "tau_det(8)": date("tau_det_8", "censored_det_8"),
        "tau_det(25)": date("tau_det_25", "censored_det_25"),
        "etalon": et["etalon_aire"].to_numpy(),
        "t_50": t50,
        "p0_hat": p0,
    })
    return ind, mesures, S


def identite_course(ind, mesures):
    print("\n[1] identite de course : tau_det < tau_ARF  <=>  max_{t < tau_ARF} S_t >= lambda")
    for lam in (8, 25, 50):
        gagne_table = (~ind[f"censored_det_{lam}"]) & (ind[f"tau_det_{lam}"] < ind["tau_arf"])
        gagne_pile = mesures["S_pre"] >= lam
        accord = int((gagne_table.to_numpy() == gagne_pile.to_numpy()).sum())
        print(f"  lambda = {lam:2d} : detecteur gagnant {int(gagne_table.sum()):4d} (table) / "
              f"{int(gagne_pile.sum()):4d} (pile) ; accord run par run {accord}/{len(ind)}")
    print("  S_pre, mediane par amplitude (preuve disponible avant la reparation) :")
    med = mesures.assign(de=ind["delta_e"].round(3)).groupby("de")["S_pre"].median()
    print("  " + " ".join(f"{d}:{v:.1f}" for d, v in med.items()))


def matrices(ind, mesures):
    noms = list(mesures.columns)
    k = len(noms)
    glob = np.eye(k)
    for i in range(k):
        for j in range(i + 1, k):
            glob[i, j] = glob[j, i] = tau_b(mesures.iloc[:, i].to_numpy(), mesures.iloc[:, j].to_numpy())

    de = ind["delta_e"].to_numpy()
    strates = sorted(d for d in np.unique(de) if d >= 0.10)
    cube = np.full((len(strates), k, k), np.nan)
    for s_i, d in enumerate(strates):
        m = np.isclose(de, d)
        sub = mesures[m]
        for i in range(k):
            cube[s_i, i, i] = 1.0
            for j in range(i + 1, k):
                cube[s_i, i, j] = cube[s_i, j, i] = tau_b(sub.iloc[:, i].to_numpy(), sub.iloc[:, j].to_numpy())
    strat = np.nanmedian(cube, axis=0)
    compte = (np.abs(cube) > SEUIL).sum(axis=0)
    return noms, glob, strat, compte, len(strates)


def main():
    ind, mesures, _ = charger()
    identite_course(ind, mesures)
    noms, glob, strat, compte, n_strates = matrices(ind, mesures)

    dist = 1 - np.abs(np.nan_to_num(strat))
    np.fill_diagonal(dist, 0)
    ordre = leaves_list(linkage(squareform(dist, checks=False), method="average"))
    o = [noms[i] for i in ordre]
    G = pd.DataFrame(glob, index=noms, columns=noms).loc[o, o]
    St = pd.DataFrame(strat, index=noms, columns=noms).loc[o, o]
    C = pd.DataFrame(compte, index=noms, columns=noms).loc[o, o]

    pd.set_option("display.width", 250)
    print("\n[2a] tau_b GLOBAL (2 000 runs empiles), ordre de la classification")
    print(G.round(2).to_string())
    print(f"\n[2b] tau_b STRATIFIE, mediane sur {n_strates} amplitudes")
    print(St.round(2).to_string())
    print(f"\n[2c] nombre d'amplitudes (sur {n_strates}) ou |tau_b| > {SEUIL}")
    print(C.to_string())

    print("\n[3] ce que l'empilement fabrique : paires dont |global| - |stratifie| > 0,25")
    lignes = []
    for i in range(len(o)):
        for j in range(i + 1, len(o)):
            g, s = G.iloc[i, j], St.iloc[i, j]
            lignes.append((o[i], o[j], g, s, C.iloc[i, j]))
    df = pd.DataFrame(lignes, columns=["a", "b", "global", "stratifie", "strates"])
    df["gonflement"] = df["global"].abs() - df["stratifie"].abs()
    print(df[df.gonflement > 0.25].sort_values("gonflement", ascending=False).round(3).to_string(index=False))
    print("\n    paires liees dans les strates (|stratifie| >= 0,30)")
    print(df[df.stratifie.abs() >= 0.30].sort_values("stratifie", key=abs, ascending=False)
          .round(3).to_string(index=False))

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "serif", "font.serif": ["cmr10"], "mathtext.fontset": "cm",
                         "axes.formatter.use_mathtext": True, "axes.unicode_minus": False, "font.size": 9})
    etiquettes = {
        "tau_ARF": r"$\tau_{\mathrm{ARF}}$", "tau_swap(25%)": r"$\tau_{\mathrm{swap}}(25\%)$",
        "tau_swap(50%)": r"$\tau_{\mathrm{swap}}(50\%)$", "tau_swap(75%)": r"$\tau_{\mathrm{swap}}(75\%)$",
        "S_pre": r"$S_{\mathrm{pre}}$", "S_max(H)": r"$S_{\max}(H)$", "A(H)": r"$A(H)$", "A(w)": r"$A(w)$",
        "G": r"$G(\tau_{\mathrm{ARF}})$", "tau_det(8)": r"$\tau_{\mathrm{det}}(8)$",
        "tau_det(25)": r"$\tau_{\mathrm{det}}(25)$", "etalon": "reference area", "t_50": r"$t_{50}$",
        "p0_hat": r"$\hat p_0$",
    }
    lab = [etiquettes[n] for n in o]
    fig, axes = plt.subplots(1, 2, figsize=(14.5, 6.2), gridspec_kw={"wspace": 0.42})
    for ax, M, titre in [(axes[0], G, "pooled over the 2,000 runs"),
                         (axes[1], St, f"median within the {n_strates} amplitudes")]:
        im = ax.imshow(M.to_numpy(), cmap="RdBu_r", vmin=-1, vmax=1)
        ax.set_xticks(range(len(o)), lab, rotation=90)
        ax.set_yticks(range(len(o)), lab)
        for i in range(len(o)):
            for j in range(len(o)):
                if i != j:
                    v = M.iloc[i, j]
                    ax.text(j, i, f"{v:.2f}".replace("-0.", "-.").replace("0.", "."), ha="center",
                            va="center", fontsize=6.2, color="white" if abs(v) > 0.6 else "black")
        ax.set_title(r"Kendall $\tau_b$, " + titre)
    fig.colorbar(im, ax=axes, shrink=0.8, label=r"$\tau_b$")
    FIGURES.mkdir(parents=True, exist_ok=True)
    sortie = FIGURES / "Fig_QD_matrice_correlations_full.png"
    fig.savefig(sortie, dpi=200, bbox_inches="tight")
    print(f"\nfigure : {sortie.name}")


if __name__ == "__main__":
    main()
