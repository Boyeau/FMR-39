"""
balayage_lambda.py
===================================================================
Balayage fin du seuil `lambda` : un seuil bien choisi suffit-il ?

LECTURE SEULE sur la simulation. Ne resimule rien. Tout est recalcule
hors ligne depuis les trajectoires d'erreur deja enregistrees :
  - campagne avec drift : QCD_traces_error_full (2 000 runs x 2 000 pas) ;
  - bras SANS drift de A1 : QCD_traces_error_A1_nodrift (100 runs), seul
    endroit du projet ou l'on observe le detecteur quand il ne se passe rien.

CE QUE CE SCRIPT AJOUTE A `chiffres_QE.py`
  `chiffres_QE.py` evalue six seuils (8, 12, 15, 20, 25, 50) et ne descend
  jamais sous 8. Or la question « existe-t-il un lambda qui arrange tout »
  se joue en dessous : il faut voir ou le cout en fausses alarmes explose.
  Ici la grille est continue de 0,5 a 50, ce qui donne la courbe complete
  non-detection contre fausses alarmes quand lambda varie -- exactement la
  piste d'originalite annoncee au ROADMAP paragraphe 5.

  Methode : `S_t` ne depend pas de lambda. On le reconstruit une fois par
  forme close de Lindley, on prend son maximum courant `M_t` (croissant),
  et `tau_det(lambda) = searchsorted(M, lambda)` donne le premier
  franchissement pour TOUTE la grille en une passe.

CE QUE CE SCRIPT N'ETABLIT PAS
  Le taux de fausse alarme n'est resolu que jusqu'a la borne haute de
  Wilson pour zero evenement : 3,7 % a n = 100, 0,18 % a n = 2 000. La
  colonne `fa_resolue` dit pour chaque lambda si le chiffre porte une
  information ou seulement une borne. Toute la falaise de la course se
  joue sous 4 % de fausses alarmes, donc dans l'angle mort du temoin a
  n = 100 : c'est ce qui justifie de l'etendre, et cette extension est
  une relance de campagne, donc une decision, pas une verification.

CONTROLES OBLIGATOIRES (le script s'arrete si l'un echoue)
  1. le balayage redonne les comptes de la campagne aux trois seuils du
     sujet : 1906 / 778 / 1 alarmes a lambda = 8, 25, 50 ;
  2. la forme close de Lindley + searchsorted redonne exactement la
     recurrence naive `S_t = max(0, S_{t-1} + x_t)` de `chiffres_QE.py`,
     sur un sous-echantillon, aux six seuils de la section E ;
  3. Wilson sur un cas connu : 50/100 -> [0,4038 ; 0,5962] ;
  4. temoin etendu seulement : les graines communes avec `A1_nodrift`
     doivent redonner la meme trajectoire d'erreur BIT A BIT. Sinon les
     deux bras ne sont pas le meme dispositif et ne se comparent pas.

USAGE
    PYTHONHASHSEED=0 python balayage_lambda.py
    PYTHONHASHSEED=0 python balayage_lambda.py --temoin QE2000_nodrift_M10
"""

import argparse
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

RACINE = Path(__file__).resolve().parents[1]
DATA, FIGURES = RACINE / "resultats" / "data", RACINE / "resultats" / "figures"
FIGURES.mkdir(parents=True, exist_ok=True)

H = 2000
DELTA_P = 0.01
SEUILS_SUJET = {8: 1906, 25: 778, 50: 1}      # QCD_indicateurs_full
SEUILS_SECTION_E = (8, 12, 15, 20, 25, 50)

# Grille continue. Pas fin la ou tout se joue (la bascule est entre 8 et 15),
# plus large ensuite, ou le detecteur a deja perdu la course.
GRILLE = np.concatenate([
    np.arange(0.5, 20.0, 0.25),
    np.arange(20.0, 50.5, 0.5),
])

TEMOIN_DEFAUT = "A1_nodrift"


def wilson(k, n, z=1.959963984540054):
    """Intervalle de Wilson a 95 %. Controle : 50/100 -> [0,4038 ; 0,5962]."""
    if n == 0:
        return float("nan"), float("nan")
    p = k / n
    den = 1.0 + z * z / n
    centre = (p + z * z / (2 * n)) / den
    demi = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return centre - demi, centre + demi


def charge_increments(nom_traces, socles, n_pas=H):
    """Matrice (runs x pas) des increments `e_t - p_hat_0 - delta_P`.

    L'ordre des lignes est celui de `run_id` trie, et il est renvoye pour
    que l'appelant aligne ses propres colonnes dessus.
    """
    tr = pd.read_parquet(DATA / f"{nom_traces}.parquet")
    piv = tr.pivot(index="run_id", columns="t", values="e").sort_index()
    piv = piv.loc[:, piv.columns[:n_pas]]
    return piv.index.to_numpy(), piv.to_numpy() - socles.loc[piv.index].to_numpy()[:, None] - DELTA_P


def max_courant(X):
    """`M_t = max_{u <= t} S_u`, ou `S` est la statistique de Page-Hinkley.

    Forme close de Lindley : `S_t = C_t - min(0, min_{k < t} C_k)` avec
    `C` la somme cumulee. `M` est croissant par construction, ce qui rend
    le premier franchissement lisible par recherche dichotomique.
    """
    C = np.cumsum(X, axis=1)
    prefixes = np.concatenate([np.zeros((C.shape[0], 1)), C], axis=1)
    S = C - np.minimum.accumulate(prefixes, axis=1)[:, :-1]
    return np.maximum.accumulate(S, axis=1)


def franchissements(M, grille):
    """`tau_det(lambda)` pour toute la grille. `H` code la censure."""
    return np.stack([np.searchsorted(ligne, grille, side="left") for ligne in M])


def recurrence_naive(X, seuils):
    """La recurrence de `chiffres_QE.py`, gardee comme temoin du controle 2."""
    out = np.full((X.shape[0], len(seuils)), H, dtype=int)
    for i, ligne in enumerate(X):
        s, restants = 0.0, {j: l for j, l in enumerate(seuils)}
        for t, v in enumerate(ligne):
            s = max(0.0, s + v)
            for j in [j for j, l in restants.items() if s >= l]:
                out[i, j] = t
                del restants[j]
            if not restants:
                break
    return out


def controles(X_drift, M_drift):
    print("[controle 1] comptes de la campagne aux trois seuils du sujet")
    tau = franchissements(M_drift, np.array(sorted(SEUILS_SUJET)))
    for j, lam in enumerate(sorted(SEUILS_SUJET)):
        mesure, attendu = int((tau[:, j] < H).sum()), SEUILS_SUJET[lam]
        etat = "OK" if mesure == attendu else "ECART -- NE RIEN LIRE PLUS BAS"
        print(f"  lambda = {lam:2d} | attendu {attendu:4d} | mesure {mesure:4d}  {etat}")
        assert mesure == attendu, f"balayage incoherent avec la campagne a lambda = {lam}"

    print("[controle 2] forme close de Lindley contre la recurrence naive")
    sous = slice(0, 60)
    seuils = np.array(SEUILS_SECTION_E, dtype=float)
    rapide = franchissements(M_drift[sous], seuils)
    lente = recurrence_naive(X_drift[sous], SEUILS_SECTION_E)
    ecarts = int((rapide != lente).sum())
    print(f"  60 runs x {len(seuils)} seuils | ecarts = {ecarts}  "
          f"{'OK' if ecarts == 0 else 'ECART -- NE RIEN LIRE PLUS BAS'}")
    assert ecarts == 0, "la forme close ne reproduit pas la recurrence"

    lo, hi = wilson(50, 100)
    print(f"[controle 3] Wilson 50/100 = [{lo:.4f} ; {hi:.4f}] "
          f"{'OK' if abs(lo - 0.4038) < 5e-4 and abs(hi - 0.5962) < 5e-4 else 'ECART'}")
    assert abs(lo - 0.4038) < 5e-4 and abs(hi - 0.5962) < 5e-4


def controle_non_regression(temoin):
    """Le temoin etendu doit contenir le temoin d'origine, bit a bit.

    Les graines sont `range(1, n+1)` : un bras a 2 000 graines rejoue donc
    les 100 premieres du bras A1. Si une seule trajectoire differe, les
    deux bras ne sont pas le meme dispositif et le taux de fausse alarme
    etendu ne se substitue pas a celui de la section E.
    """
    ref = pd.read_parquet(DATA / f"QCD_traces_error_{TEMOIN_DEFAUT}.parquet")
    ref_meta = pd.read_parquet(DATA / f"QCD_runs_meta_{TEMOIN_DEFAUT}.parquet")
    new = pd.read_parquet(DATA / f"QCD_traces_error_{temoin}.parquet")
    new_meta = pd.read_parquet(DATA / f"QCD_runs_meta_{temoin}.parquet")

    graines = sorted(set(ref_meta["seed"]) & set(new_meta["seed"]))
    a = ref.merge(ref_meta[["run_id", "seed"]], on="run_id")
    b = new.merge(new_meta[["run_id", "seed"]], on="run_id")
    a = a[a["seed"].isin(graines)].sort_values(["seed", "t"])["e"].to_numpy()
    b = b[b["seed"].isin(graines)].sort_values(["seed", "t"])["e"].to_numpy()

    ecarts = int((a != b).sum()) if a.shape == b.shape else -1
    print(f"[controle 4] non-regression du temoin, {len(graines)} graines communes")
    print(f"  {a.size} valeurs comparees | ecarts bit a bit = {ecarts}  "
          f"{'OK' if ecarts == 0 else 'ECART -- NE RIEN LIRE PLUS BAS'}")
    assert ecarts == 0, "le temoin etendu ne rejoue pas le temoin d'origine"


def balaye(temoin=TEMOIN_DEFAUT):
    ind = pd.read_parquet(DATA / "QCD_indicateurs_full.parquet").set_index("run_id").sort_index()
    meta0 = pd.read_parquet(DATA / f"QCD_runs_meta_{temoin}.parquet").set_index("run_id").sort_index()

    runs, X = charge_increments("QCD_traces_error_full", ind["p_hat_0"])
    ind = ind.loc[runs]
    M = max_courant(X)

    runs0, X0 = charge_increments(f"QCD_traces_error_{temoin}", meta0["p_hat_0"])
    M0 = max_courant(X0)

    controles(X, M)
    if temoin != TEMOIN_DEFAUT:
        controle_non_regression(temoin)

    tau = franchissements(M, GRILLE)               # (2000, len(GRILLE))
    tau0 = franchissements(M0, GRILLE)             # (100,  len(GRILLE))
    tau_arf = ind["tau_arf"].to_numpy()[:, None]

    alarme, alarme0 = tau < H, tau0 < H
    gagne = alarme & (tau < tau_arf)               # censure comptee comme defaite
    n, n0 = len(runs), len(runs0)

    # Sous ce taux, le temoin ne separe plus de zero : c'est la borne haute
    # de Wilson pour 0 evenement sur n0 runs, et elle depend donc du temoin.
    resolution = wilson(0, n0)[1]

    lignes = []
    for j, lam in enumerate(GRILLE):
        k_fa = int(alarme0[:, j].sum())
        lo, hi = wilson(k_fa, n0)
        lo_w, hi_w = wilson(int(gagne[:, j].sum()), n)
        delais = tau[alarme[:, j], j]
        lignes.append({
            "lambda": lam,
            "taux_detection": alarme[:, j].mean(),
            "taux_victoire": gagne[:, j].mean(),
            "victoire_lo": lo_w, "victoire_hi": hi_w,
            "victoire_sur_non_censures": gagne[:, j].sum() / max(alarme[:, j].sum(), 1),
            "taux_censure_det": 1.0 - alarme[:, j].mean(),
            "taux_fausse_alarme": k_fa / n0,
            "fa_lo": lo, "fa_hi": hi, "fa_k": k_fa, "resolution_fa": resolution,
            "fa_resolue": k_fa / n0 >= resolution,
            "delai_detection_median": float(np.median(delais)) if delais.size else float("nan"),
            # parametres de grille et de campagne, pour rejouer la ligne
            "H": H, "delta_P": DELTA_P, "n_runs": n, "n_runs_sans_drift": n0,
            "n_graines": int(ind["seed"].nunique()), "n_models": 10,
        })
    table = pd.DataFrame(lignes)

    par_ampl = []
    for j, lam in enumerate(GRILLE):
        d = pd.DataFrame({"delta_e": ind["delta_e"].to_numpy(), "gagne": gagne[:, j]})
        for amp, g in d.groupby("delta_e"):
            lo, hi = wilson(int(g["gagne"].sum()), len(g))
            par_ampl.append({"lambda": lam, "delta_e": amp, "taux_victoire": g["gagne"].mean(),
                             "lo": lo, "hi": hi, "n": len(g), "H": H, "delta_P": DELTA_P})
    return table, pd.DataFrame(par_ampl)


def figures(table, suffixe=""):
    lisible = table[table["fa_resolue"]]
    resolution = float(table["resolution_fa"].iloc[0])
    n0 = int(table["n_runs_sans_drift"].iloc[0])

    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    ax.plot(table["lambda"], table["taux_detection"] * 100, "k-", lw=1.6,
            label="alarme dans l'horizon")
    ax.plot(table["lambda"], table["taux_victoire"] * 100, "k--", lw=1.6,
            label=r"gagne la course ($\tau_{det} < \tau_{ARF}$)")
    ax.plot(table["lambda"], table["taux_fausse_alarme"] * 100, "k:", lw=1.8,
            label="fausse alarme, sans drift")
    ax.fill_between(table["lambda"], table["fa_lo"] * 100, table["fa_hi"] * 100,
                    color="0.75", alpha=0.5, lw=0, label=f"IC Wilson 95 %, n = {n0}")
    ax.axhline(resolution * 100, color="0.5", lw=0.8)
    ax.text(33, resolution * 100 + 1.8, f"resolution du temoin (n = {n0})",
            fontsize=7.5, color="0.35")
    ax.set_xlabel(r"seuil $\lambda$")
    ax.set_ylabel("part des executions (%)")
    ax.set_xlim(0, 50)
    ax.set_ylim(-2, 102)
    ax.legend(fontsize=8, loc="center right")
    ax.grid(alpha=0.25, lw=0.5)
    fig.savefig(FIGURES / f"Fig_QE_balayage_lambda{suffixe}.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.0, 4.4))
    ax.plot(table["taux_fausse_alarme"] * 100, table["taux_victoire"] * 100,
            color="0.55", lw=1.2, zorder=1)
    ax.scatter(lisible["taux_fausse_alarme"] * 100, lisible["taux_victoire"] * 100,
               s=14, facecolor="k", zorder=2, label=r"$\lambda$ ou le temoin resout le taux")
    masque = table[~table["fa_resolue"]]
    ax.scatter(masque["taux_fausse_alarme"] * 100, masque["taux_victoire"] * 100,
               s=14, facecolor="none", edgecolor="0.45", zorder=2,
               label=rf"$\lambda$ ou il ne le resout pas ($\leq {resolution*100:.2f}\,\%$)")
    for lam in (3, 5, 8, 12, 15, 20, 25):
        ligne = table.iloc[(table["lambda"] - lam).abs().argmin()]
        ax.annotate(rf"$\lambda={lam}$",
                    (ligne["taux_fausse_alarme"] * 100, ligne["taux_victoire"] * 100),
                    textcoords="offset points", xytext=(6, -3), fontsize=8)
    ax.set_xlabel("fausses alarmes sans drift, sur 2 000 pas (%)")
    ax.set_ylabel(r"gagne la course, avec drift (%)")
    ax.legend(fontsize=8, loc="lower right")
    ax.grid(alpha=0.25, lw=0.5)
    fig.savefig(FIGURES / f"Fig_QE_compromis_lambda{suffixe}.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def rapporte(table):
    n0 = int(table["n_runs_sans_drift"].iloc[0])
    print("\n[balayage] la courbe complete, un point sur quatre affiche")
    print(f"  {'lam':>5} | {'detecte':>8} | {'gagne':>8} | {'fausses alarmes':>22} | {'delai med.':>10}")
    for _, r in table[table["lambda"].isin(
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 20, 25, 30, 40, 50])].iterrows():
        marque = "" if r["fa_resolue"] else "  (borne seule)"
        print(f"  {r['lambda']:5.1f} | {r['taux_detection']*100:6.1f} % | {r['taux_victoire']*100:6.1f} %"
              f" | {r['fa_k']:4.0f}/{n0} = {r['taux_fausse_alarme']*100:5.1f} %"
              f" [{r['fa_lo']*100:4.1f};{r['fa_hi']*100:4.1f}]{marque}"
              f" | {r['delai_detection_median']:8.0f}")

    print("\n[frontiere] le meilleur lambda sous contrainte de fausses alarmes")
    for plafond in (0.01, 0.02, 0.05, 0.10, 0.20):
        adm = table[table["fa_hi"] <= plafond]          # borne HAUTE de Wilson sous le plafond
        if adm.empty:
            print(f"  fausses alarmes garanties <= {plafond*100:4.1f} % | aucun lambda admissible"
                  f" (le temoin a n = 100 ne le certifie pour aucun seuil)")
            continue
        best = adm.loc[adm["taux_victoire"].idxmax()]
        print(f"  fausses alarmes garanties <= {plafond*100:4.1f} % | lambda = {best['lambda']:5.2f}"
              f" | gagne {best['taux_victoire']*100:5.1f} %"
              f" [{best['victoire_lo']*100:.1f};{best['victoire_hi']*100:.1f}]"
              f" | detecte {best['taux_detection']*100:5.1f} %")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--temoin", default=TEMOIN_DEFAUT,
                    help="tag du bras sans drift (defaut : A1_nodrift, 100 runs)")
    args = ap.parse_args()

    suffixe = "" if args.temoin == TEMOIN_DEFAUT else "_n2000"
    table, par_ampl = balaye(args.temoin)
    table.to_parquet(DATA / f"QE_balayage_lambda{suffixe}.parquet", index=False)
    par_ampl.to_parquet(DATA / f"QE_balayage_lambda_par_amplitude{suffixe}.parquet", index=False)
    figures(table, suffixe)
    rapporte(table)
    print(f"\n  ecrit : QE_balayage_lambda{suffixe}.parquet ({len(table)} seuils),"
          f" QE_balayage_lambda_par_amplitude{suffixe}.parquet ({len(par_ampl)} lignes)")
    print(f"  ecrit : Fig_QE_balayage_lambda{suffixe}.png, Fig_QE_compromis_lambda{suffixe}.png")
