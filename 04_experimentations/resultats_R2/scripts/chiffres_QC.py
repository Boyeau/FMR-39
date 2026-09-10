"""
chiffres_QC.py
===================================================================
Rejeu, constat par constat, des valeurs citees dans les trois redactions
de la question C (`redaction_QC1_hierarchie.tex`,
`redaction_QC2_certificat_deterministe.tex`, `redaction_QC3_invariance.tex`)
et des deux chiffres de D que l'audit du 10 septembre a contestes.

LECTURE SEULE. N'ecrit aucune table, ne recalcule aucun indicateur de
campagne, ne resimule rien. La seule table nouvelle dont il a besoin,
`QCD_fin_horizon_full.parquet`, est ecrite par `derives_QC.py`.

Chaque bloc imprime une ligne de la forme
    [QCx l.N] ecrit = ...  mesure = ...  table = ...
ou N est la ligne du `.tex` au 10 septembre. Un constat dont le rejeu ne
redonne pas la valeur annoncee par l'audit preparatoire est RETIRE de la
note d'audit, pas « ajuste » : ce script est la porte.

Les blocs QC1 et QC2 portent sur des fichiers qui NE SE MODIFIENT PAS ici
(ecrits par Alexandre et Salome) : leurs constats vont dans
`AUDIT_QC1_QC2_10SEPT.md`. Les blocs QC3 et QD portent sur des fichiers
revises directement.

USAGE
    PYTHONHASHSEED=0 python chiffres_QC.py            # tout
    PYTHONHASHSEED=0 python chiffres_QC.py --sous QC3 # un seul fichier
"""

import argparse
import math
import re
from pathlib import Path

import numpy as np
import pandas as pd

import analyse_QCD as aq
from chiffres_QD import wilson

RACINE = Path(__file__).resolve().parents[1]
DATA = RACINE / "resultats" / "data"
TEX = RACINE.parent  # repo/04_experimentations/

LAMBDAS = (8, 25, 50)


def _t(nom: str) -> pd.DataFrame:
    """Lit une table et la TRIE par delta_e quand la colonne existe.

    Plusieurs blocs ci-dessous lisent par position (`.iloc[0]`, `.iloc[-1]`,
    `.shift(1)`) : sans tri explicite, ils dependraient de l'ordre d'ecriture
    du Parquet, qui n'est garanti par rien.
    """
    df = pd.read_parquet(DATA / f"{nom}.parquet")
    if "delta_e" in df.columns:
        df = df.sort_values("delta_e", kind="stable").reset_index(drop=True)
    return df


def _titre(s: str) -> None:
    print()
    print("=" * 74)
    print(s)
    print("=" * 74)


def _sous_titre(s: str) -> None:
    print()
    print(f"--- {s}")


def _ligne(tag: str, ecrit, mesure, table: str) -> None:
    print(f"  [{tag}] ecrit = {ecrit}  |  mesure = {mesure}  |  table = {table}")


def _pres(df: pd.DataFrame, de: float, tol: float = 3e-3) -> pd.Series:
    """La ligne de `df` dont `delta_e` est le plus proche de `de` (a `tol` pres).

    Les amplitudes citees dans les .tex sont arrondies a trois decimales ; la
    grille est linspace(0.1, 4.0, 20) / 8. On cherche le plus proche voisin
    plutot qu'une egalite a 5e-4, qui echoue sur 0,1945 contre 0,19445.
    """
    i = int((df.delta_e - de).abs().idxmin())
    if abs(float(df.delta_e[i]) - de) > tol:
        raise ValueError(f"aucune amplitude a {tol} de {de}")
    return df.loc[i]


def domaine_decision() -> np.ndarray:
    """Les amplitudes du domaine de decision, lues dans la table stratifiee.

    On ne redefinit pas le domaine ici : la colonne en fait foi.
    """
    st = _t("QCD_correlations_stratifiees_full")
    return np.sort(st.loc[st.dans_domaine_decision, "delta_e"].unique())


# ----------------------------------------------------------------------
# QC1 : hierarchie deterministe (Alexandre, Salome) -- AUDIT SEULEMENT
# ----------------------------------------------------------------------
def qc1() -> None:
    _titre("QC1 -- redaction_QC1_hierarchie.tex (audit, fichier non modifie)")

    ind = _t("QCD_indicateurs_full")
    te = _t("QCD_tau_err_full")
    n_seeds = int(ind.groupby("delta_e").size().iloc[0])

    _sous_titre("l. 56 : comparaisons non censurees pour q in {25, 50, 75} %")
    par_q = {q: int((~ind[f"censored_swap_{q}"].astype(bool)).sum()) for q in (25, 50, 75)}
    total = sum(par_q.values())
    _ligne("QC1 l.56", "5 795", f"{total} = {par_q[25]} + {par_q[50]} + {par_q[75]}",
           "QCD_indicateurs_full.censored_swap_*")
    print(f"      -> JOURNAL.md section 1 (C.1 a) dit « 6 000 comparaisons » : "
          f"c'est 3 x 2 000 AVANT censure ; le texte de QC1 a raison ({total}).")
    viol = 0
    for q in (25, 50, 75):
        ok = ~ind[f"censored_swap_{q}"].astype(bool)
        viol += int((ind.loc[ok, f"tau_swap_{q}"] < ind.loc[ok, "tau_arf"]).sum())
    _ligne("QC1 l.57", "0 violations", f"{viol} violations", "QCD_indicateurs_full")
    egal = int((ind.tau_swap_10 == ind.tau_arf).sum())
    _ligne("QC1 l.55", "tau_ARF = tau_swap(10 %) dans 100 % des cas",
           f"{egal}/{len(ind)} egalites exactes", "QCD_indicateurs_full")

    _sous_titre("l. 132 : « 6,0 a 14,3 fois tau_ARF », ecart median tau_swap(75 %) - tau_ARF")
    # censure par amplitude du quota 75 % : les amplitudes a plus de 50 % de
    # censure sont exclues (QC1 l. 133), ce qui laisse 18 amplitudes
    cens75 = ind.groupby("delta_e")["censored_swap_75"].mean()
    ampl_cens_ok = cens75[cens75 <= 0.5].index.to_numpy()
    # deux lectures possibles de l'ecart median : mediane des ecarts par run
    # (sur les runs non censures), ou difference des medianes. Les deux sont
    # imprimees ; celle qui redonne 167-1368 est celle de QC1.
    rows = []
    for de, grp in ind.groupby("delta_e", sort=True):
        ok = ~grp.censored_swap_75.astype(bool)
        med_arf = float(grp.tau_arf.median())
        ecart_par_run = float((grp.loc[ok, "tau_swap_75"] - grp.loc[ok, "tau_arf"]).median())
        diff_medianes = float(grp.loc[ok, "tau_swap_75"].median() - med_arf)
        rows.append({"delta_e": de, "cens_75": float(cens75[de]),
                     "tau_arf_median": med_arf,
                     "ecart_median_par_run": ecart_par_run,
                     "diff_des_medianes": diff_medianes,
                     "ratio_par_run": ecart_par_run / med_arf,
                     "ratio_diff_med": diff_medianes / med_arf})
    r = pd.DataFrame(rows)
    r18 = r[r.delta_e.isin(ampl_cens_ok)]
    print(f"      amplitudes retenues (censure 75 % <= 50 %) : {len(r18)}")
    _ligne("QC1 l.132", "ecart de 167 a 1 368 pas",
           f"mediane des ecarts par run : {r18.ecart_median_par_run.min():.0f} a "
           f"{r18.ecart_median_par_run.max():.0f} ; difference des medianes : "
           f"{r18.diff_des_medianes.min():.0f} a {r18.diff_des_medianes.max():.0f}",
           "QCD_indicateurs_full")
    _ligne("QC1 l.132", "6,0 a 14,3 fois tau_ARF",
           f"par run : {r18.ratio_par_run.min():.1f} a {r18.ratio_par_run.max():.1f} ; "
           f"diff. des medianes : {r18.ratio_diff_med.min():.1f} a {r18.ratio_diff_med.max():.1f}",
           "QCD_indicateurs_full")
    exclu = r[~r.delta_e.isin(ampl_cens_ok)]
    _ligne("QC1 l.134", "maximum apparent 1 393 a Delta_e = 0,141 (censure 54 %)",
           "; ".join(f"{x.ecart_median_par_run:.1f} a {x.delta_e:.3f} (censure {x.cens_75:.0%})"
                     for x in exclu.itertuples()),
           "QCD_indicateurs_full")
    print("      -> README.md de resultats_R2 dit « 7 a 15 fois » : a corriger en « 6,0 a 14,3 ».")

    _sous_titre("l. 132 et l. 213 : deux ensembles de « 18 amplitudes » sous le meme mot")
    ampl_interp = te.loc[te.interpretable, "delta_e"].to_numpy()
    seul_cens = sorted(set(np.round(ampl_cens_ok, 3)) - set(np.round(ampl_interp, 3)))
    seul_interp = sorted(set(np.round(ampl_interp, 3)) - set(np.round(ampl_cens_ok, 3)))
    _ligne("QC1 l.132", "18 amplitudes « where its median is interpretable » (censure)",
           f"{len(ampl_cens_ok)} amplitudes, exclues : "
           f"{sorted(np.round(r.loc[~r.delta_e.isin(ampl_cens_ok), 'delta_e'], 3))}",
           "QCD_indicateurs_full.censored_swap_75")
    _ligne("QC1 l.213", "18 amplitudes « where the test is interpretable » (puissance)",
           f"{len(ampl_interp)} amplitudes, exclues : "
           f"{sorted(np.round(te.loc[~te.interpretable, 'delta_e'], 3))}",
           "QCD_tau_err_full.interpretable")
    print(f"      difference symetrique : dans le 1er seulement {seul_cens}, "
          f"dans le 2nd seulement {seul_interp}")
    print("      -> deux ensembles differents de 18 sous le meme adjectif « interpretable ».")

    _sous_titre("l. 210 : « nearly 1 800 seeds » a 0,028, « 200 » a 0,085 -- n (2 sigma / rho Delta_e)^2")
    for de_cible, ecrit in ((0.0282, "nearly 1 800"), (0.0854, "on the order of 200")):
        row = te.loc[np.isclose(te.delta_e, de_cible, atol=5e-4)].iloc[0]
        n_req = n_seeds * (2 * row.sigma_courbe / row.seuil) ** 2
        _ligne("QC1 l.210", f"{ecrit} a Delta_e = {row.delta_e:.4f}",
               f"{n_req:.0f} = {n_seeds} x (2 x {row.sigma_courbe:.6f} / {row.seuil:.6f})^2",
               "QCD_tau_err_full.sigma_courbe, .seuil")
    print("      -> herite de JOURNAL.md section 7 (« de l'ordre de 1 800 »). Ordre de "
          "grandeur juste ; la valeur de la formule est 1 874.")

    _sous_titre("l. 188-192 : bande +-2 sigma de Fig_QC_tauerr_power_full contre sigma_courbe")
    meta, error_mat, _ = aq.load_campaign("full")
    for de_cible in (0.0282, 0.0854):
        grp = meta[np.isclose(meta.delta_e, de_cible, atol=5e-4)]
        runs = grp.run_id.to_numpy()
        courbe = error_mat[runs].mean(axis=0)
        n = len(runs)
        se_400 = float(np.sqrt(courbe[:400] * (1 - courbe[:400]) / n).mean())
        se_H = float(np.sqrt(courbe * (1 - courbe) / n).mean())
        sig = float(te.loc[np.isclose(te.delta_e, de_cible, atol=5e-4), "sigma_courbe"].iloc[0])
        _ligne("QC1 l.188", f"bande +-2 sigma (Delta_e = {grp.delta_e.iloc[0]:.4f})",
               f"sigma binomial sqrt(e(1-e)/n) : {se_400:.4f} (0-400 pas trace), "
               f"{se_H:.4f} (horizon) ; sigma_courbe (queue 500 pas) : {sig:.4f}",
               "QCD_traces_error_full, QCD_tau_err_full.sigma_courbe")
    print("      -> deux estimateurs de bruit differents : la figure trace le binomial "
          "par pas, le critere `interpretable` lit l'ecart-type empirique de queue. "
          "Sans effet sur le verdict (AVERTISSEMENT point 5).")

    _sous_titre("l. 50 : « quotas (also used in Q C.2/D) »")
    qc2 = (TEX / "redaction_QC2_certificat_deterministe.tex").read_text(encoding="utf-8")
    qd = "".join((TEX / f).read_text(encoding="utf-8") for f in (
        "redaction_QD1_instrumentation_conjointe.tex",
        "redaction_QD3_stratification_amplitude.tex",
        "redaction_QD4_protocole_decision.tex"))
    n_qc2 = len(re.findall(r"tau_\{\\mathrm\{swap\}\}", qc2))
    n_qd = len(re.findall(r"tau_\{\\mathrm\{swap\}\}", qd))
    _ligne("QC1 l.50", "quotas also used in Q C.2/D",
           f"occurrences de tau_swap : QC2 = {n_qc2}, QD1+QD3+QD4 = {n_qd}",
           "grep sur les .tex")
    print("      -> la moitie « D » est juste, la moitie « C.2 » est fausse.")

    _sous_titre("notation : tau_err(rho) et tau^* dans QC1, tau_rec dans QD1")
    qc1 = (TEX / "redaction_QC1_hierarchie.tex").read_text(encoding="utf-8")
    print(f"      tau_err dans QC1 : {len(re.findall(r'tau_\{\\mathrm\{err\}\}', qc1))} ; "
          f"tau^* dans QC1 : {len(re.findall(r'tau\^\*', qc1))} ; "
          f"tau_rec dans QC1 : {len(re.findall(r'tau_\{\\mathrm\{rec\}\}', qc1))}")
    print("      -> QC1 ne definit ni tau^* ni le lien tau_rec = tau_err(rho) ; QD1 l. 66 le fait.")

    _sous_titre("l. 149-152 : les 4 violations sans persistance, 0 avec (controle croise)")
    viol1 = te[te.avant_tau_arf_p1]
    _ligne("QC1 l.151", "4 violations a 0,028 / 0,085 / 0,141 / 0,194",
           f"{len(viol1)} a {sorted(np.round(viol1.delta_e, 3))}", "QCD_tau_err_full")
    _ligne("QC1 l.193", "0 violations avec persistance",
           f"{int(te.avant_tau_arf_p20.sum())}", "QCD_tau_err_full")
    _ligne("QC1 l.190", "franchissement au pas 101 a 0,141 et 0,194, tau_ARF median 263 et 143",
           "; ".join(f"{x.tau_err_p1:.0f} / {x.tau_arf_median:.0f} a {x.delta_e:.3f}"
                     for x in viol1[viol1.interpretable].itertuples()),
           "QCD_tau_err_full")
    _ligne("QC1 l.192", "avec persistance, pas 626 et 322",
           "; ".join(f"{x.tau_err_p20:.0f} a {x.delta_e:.3f}"
                     for x in viol1[viol1.interpretable].itertuples()),
           "QCD_tau_err_full")
    _ligne("QC1 l.156", "sigma de 0,0154 a 0,0047",
           f"{te.sigma_courbe.max():.4f} a {te.sigma_courbe.min():.4f}", "QCD_tau_err_full")


# ----------------------------------------------------------------------
# QC2 : certificat deterministe (Salome, Alexandre) -- AUDIT SEULEMENT
# ----------------------------------------------------------------------
def qc2() -> None:
    _titre("QC2 -- redaction_QC2_certificat_deterministe.tex (audit, fichier non modifie)")

    bud = _t("QCD_budget_preuve_full")
    ind = _t("QCD_indicateurs_full")
    tex = (TEX / "redaction_QC2_certificat_deterministe.tex").read_text(encoding="utf-8")

    _sous_titre("l. 241 : \\eqref{eq:certificate} -- le label existe-t-il ?")
    labels = re.findall(r"\\label\{(eq:[^}]+)\}", tex)
    refs = re.findall(r"\\eqref\{(eq:[^}]+)\}", tex)
    manquants = sorted(set(refs) - set(labels))
    _ligne("QC2 l.241", "\\eqref{eq:certificate}",
           f"labels definis : {labels} ; references sans label : {manquants}",
           "grep sur le .tex")
    print("      -> BLOQUANT : rend « (??) » au PDF.")

    _sous_titre("l. 215 : « checked over every trajectory of the campaign » : 1,07e-10")
    rng = np.random.default_rng(12345)  # meme graine que analyse_QCD.main
    synth = aq.self_check(rng)
    meta, error_mat, _ = aq.load_campaign("full")
    p0 = meta.p_hat_0.to_numpy()
    ferme = aq.cusum_path(error_mat, p0[:, None])
    pire = 0.0
    for i in range(len(meta)):
        pire = max(pire, float(np.abs(ferme[i] - aq.cusum_path_recurrent(error_mat[i], p0[i])).max()))
    _ligne("QC2 l.215", "1,07e-10 sur « every trajectory of the campaign »",
           f"200 trajectoires Bernoulli synthetiques (--self-check, graine 12345) : {synth:.2e} ; "
           f"2 000 trajectoires de la campagne : {pire:.2e}",
           "analyse_QCD.self_check ; QCD_traces_error_full")
    print("      -> le 1,07e-10 est le controle SYNTHETIQUE ; sur la campagne c'est "
          f"{pire:.2e}. JOURNAL.md section 5 le dit correctement (« 200 trajectoires »).")

    _sous_titre("l. 231 : A(0,H) >= 28 dans 473 runs, >= 45 dans 66, >= 70 dans 0")
    seuils = {8: 28, 25: 45, 50: 70}
    for lam, s in seuils.items():
        k = int((ind.A_H >= s).sum())
        _ligne("QC2 l.231", f"A(0,H) >= {s} ({lam})", f"{k}/{len(ind)} = {100 * k / len(ind):.1f} %",
               "QCD_indicateurs_full.A_H")
    bas = ind[np.isclose(ind.delta_e, ind.delta_e.min())]
    _ligne("QC2 l.232", "a Delta_e = 0,028, aucun run >= 28",
           f"{int((bas.A_H >= 28).sum())}/{len(bas)}", "QCD_indicateurs_full.A_H")

    _sous_titre("l. 238 : w = ceil(3 x 18,5 / Delta_e) contre le script (round)")
    a_fit = aq.TAU_ARF_FIT[0]
    w_round = np.array([int(min(aq.H, max(1, round(3 * a_fit / de)))) for de in bud.delta_e])
    w_ceil = np.array([int(min(aq.H, max(1, math.ceil(3 * a_fit / de)))) for de in bud.delta_e])
    n_diff = int((w_ceil != bud.w_fenetre_courte.to_numpy()).sum())
    n_diff_round = int((w_round != bud.w_fenetre_courte.to_numpy()).sum())
    _ligne("QC2 l.238", "w = ceil(3 x 18,5 / Delta_e)",
           f"round reproduit la table sur {20 - n_diff_round}/20 amplitudes ; "
           f"ceil s'en ecarte sur {n_diff}/20 (ex. Delta_e = {bud.delta_e.iloc[0]:.4f} : "
           f"table {int(bud.w_fenetre_courte.iloc[0])}, ceil {w_ceil[0]}, "
           f"3 x 18,5 / Delta_e = {3 * a_fit / bud.delta_e.iloc[0]:.3f})",
           "QCD_budget_preuve_full.w_fenetre_courte ; analyse_QCD.evidence_budget")

    _sous_titre("l. 272 : « mean gap 0,037 over all cells, median 0 » pour lambda = 8")
    gaps = {}
    for lam in LAMBDAS:
        g = bud[f"detection_observee_H_l{lam}"] - bud[f"certificat_court_l{lam}"]
        gaps[lam] = g
        print(f"      lambda = {lam:2d} : ecart moyen {g.mean():.4f}, median {g.median():.4f}, "
              f"min {g.min():.2e}, max {g.max():.4f}, cellules < -1e-9 : {int((g < -1e-9).sum())}")
    tous = pd.concat(gaps.values())
    _ligne("QC2 l.272", "mean gap 0,037 over all cells, median 0 (phrase sur lambda = 8)",
           f"60 cellules : moyenne {tous.mean():.4f}, mediane {tous.median():.4f} ; "
           f"les 20 cellules de lambda = 8 seules : moyenne {gaps[8].mean():.4f}",
           "QCD_budget_preuve_full")
    _ligne("QC2 l.263", "le certificat ne depasse JAMAIS la detection observee (60 cellules)",
           f"{int((tous < -1e-9).sum())} cellules avec certificat > detection (a 1e-9 pres ; "
           f"ecart le plus negatif {tous.min():.2e}, bruit flottant)", "QCD_budget_preuve_full")
    print("      -> le 0,0375 est la moyenne des 60 cellules ; la parenthese est dans une "
          "phrase sur lambda = 8, ou la moyenne vaut 0,0005.")

    _sous_titre("l. 247-253 : la table sur 100 graines, avec IC de Wilson a 95 %")
    lo, hi = wilson(50, 100)
    print(f"      controle Wilson 50/100 : [{lo:.4f} ; {hi:.4f}] (attendu [0,4038 ; 0,5962])")
    assert abs(lo - 0.4038) < 5e-4 and abs(hi - 0.5962) < 5e-4, "Wilson faux"
    cibles = (0.028, 0.085, 0.141, 0.194, 0.243, 0.361, 0.498)
    n = 100
    print("      lignes LaTeX pretes a coller (fraction [IC Wilson]) :")
    for c in cibles:
        b = _pres(bud, c)
        cells = []
        for col in ("certificat_court_l8", "detection_observee_H_l8",
                    "certificat_court_l25", "detection_observee_H_l25", "certificat_court_l50"):
            k = int(round(b[col] * n))
            lo, hi = wilson(k, n)
            cells.append(f"{b[col]:.2f} [{lo:.2f};{hi:.2f}]")
        print(f"      {b.delta_e:.3f} & {int(b.w_fenetre_courte)} & " + " & ".join(cells) + r" \\")
    print("      table = QCD_budget_preuve_full ; n = 100 graines par amplitude")

    _sous_titre("l. 240-241 : guillemets francais « » dans un texte anglais")
    n_guil = len(re.findall("[«»]", tex))
    _ligne("QC2 l.240", "« ... »", f"{n_guil} guillemets francais", "grep sur le .tex")

    _sous_titre("l. 223 : « two-directional short-window » -- ce que le corollaire dit")
    print("      l'equivalence porte sur S_max(w) >= lambda <=> une sous-fenetre de ]0,w] "
          "satisfait A(k,j) >= lambda + (j-k) delta_P ; elle ne dit pas que l'alarme "
          "tombe AVANT w. Constat de lecture, pas de calcul : voir la note d'audit.")


# ----------------------------------------------------------------------
# QC3 : invariance du budget (Ulysse) -- REVISE DIRECTEMENT
# ----------------------------------------------------------------------
def qc3() -> None:
    _titre("QC3 -- redaction_QC3_invariance.tex (revise)")

    bud = _t("QCD_budget_preuve_full")
    diag = _t("QCD_diagnostic_ajustement_full")
    fin = _t("QCD_fin_horizon_full")
    ind = _t("QCD_indicateurs_full")
    a_fit, b_fit = aq.TAU_ARF_FIT
    de_min, de_max = float(bud.delta_e.min()), float(bud.delta_e.max())

    _sous_titre("l. 34 : « 3 x 18,5 / 0,028 ~ 1 982 » contre w de la table")
    _ligne("QC3 l.34", "~ 1 982",
           f"w = {int(bud.w_fenetre_courte.iloc[0])} a Delta_e = {de_min:.4f} "
           f"(3 x 18,5 / {de_min:.4f} = {3 * a_fit / de_min:.2f} ; avec 0,028 arrondi : "
           f"{3 * a_fit / 0.028:.1f})",
           "QCD_budget_preuve_full.w_fenetre_courte")
    print("      -> le 1 982 vient de l'arrondi 0,028 ; la grille est a 0,0282.")

    _sous_titre("l. 43-45 : exposant residuel, rapport des extremes, 17,2 a 18,2, facteur 17,7")
    _ligne("QC3 l.44", "(0,498/0,028)^0,02 = 1,059",
           f"({de_max:.4f}/{de_min:.4f})^{1 + b_fit:.2f} = {(de_max / de_min) ** (1 + b_fit):.4f}",
           "grille de QCD_budget_preuve_full")
    _ligne("QC3 l.45", "17,2 a 18,2 ; facteur 17,7",
           f"A_predit_brut {bud.A_predit_brut.min():.2f} a {bud.A_predit_brut.max():.2f} ; "
           f"Delta_e max/min = {de_max / de_min:.2f}",
           "QCD_budget_preuve_full.A_predit_brut")

    _sous_titre("l. 66-67 : table du budget utilisable")
    for i in (0, len(bud) - 1):
        b = bud.iloc[i]
        print(f"      Delta_e = {b.delta_e:.4f} : brut {b.A_predit_brut:.2f}, part prelevee "
              f"{100 * b.part_prelevee_par_delta_P:.1f} %, utilisable {b.A_predit_utilisable:.2f}")
    print("      table = QCD_budget_preuve_full")

    _sous_titre("l. 83-86 : 28, 45, 70 = lambda + H delta_P")
    print(f"      {[float(bud[f'seuil_fenetre_entiere_l{l}'].iloc[0]) for l in LAMBDAS]} "
          f"(table = QCD_budget_preuve_full.seuil_fenetre_entiere_l*)")

    _sous_titre("l. 110-126 : facteur 1,78 sur [0,085 ; 0,498], 11,4 sur la grille, 30,8 vs 18,0")
    haut = bud[bud.delta_e >= 0.085]
    _ligne("QC3 l.113", "facteur 1,78 (A(w) sur Delta_e >= 0,085)",
           f"{haut.A_w_mesure_median.max() / haut.A_w_mesure_median.min():.2f} "
           f"= {haut.A_w_mesure_median.max():.2f} / {haut.A_w_mesure_median.min():.2f}",
           "QCD_budget_preuve_full.A_w_mesure_median")
    _ligne("QC3 l.111", "amplitude x 5,8", f"{de_max / haut.delta_e.min():.2f}", "grille")
    _ligne("QC3 l.114", "facteur 1,04 predit",
           f"{haut.A_predit_brut.max() / haut.A_predit_brut.min():.3f}", "A_predit_brut")
    _ligne("QC3 l.121", "facteur 11,4 (grille entiere)",
           f"{bud.A_w_mesure_median.max() / bud.A_w_mesure_median.min():.1f} "
           f"= {bud.A_w_mesure_median.max():.2f} / {bud.A_w_mesure_median.min():.2f}",
           "QCD_budget_preuve_full.A_w_mesure_median")
    r243 = _pres(bud, 0.243)
    _ligne("QC3 l.115", "30,8 mesure contre 18,0 predit a 0,243",
           f"A(w) = {r243.A_w_mesure_median:.1f}, predit {r243.A_predit_brut:.1f} "
           f"a Delta_e = {r243.delta_e:.4f}", "QCD_budget_preuve_full")
    _ligne("QC3 l.120", "A(w) = 2,71 a 0,028", f"{bud.A_w_mesure_median.iloc[0]:.2f}",
           "QCD_budget_preuve_full")
    _ligne("QC3 l.123", "w = 1 969", f"{int(bud.w_fenetre_courte.iloc[0])}", "QCD_budget_preuve_full")

    _sous_titre("l. 128-129 : A(H) culmine a 38,3, croise zero a partir de 0,482, tombe a -20,8")
    imax = bud.A_H_mesure_median.idxmax()
    neg = bud[bud.A_H_mesure_median < 0]
    _ligne("QC3 l.128", "pic 38,3", f"{bud.A_H_mesure_median.max():.1f} a Delta_e = {bud.delta_e[imax]:.3f}",
           "QCD_budget_preuve_full.A_H_mesure_median")
    _ligne("QC3 l.129", "croise zero a partir de 0,482",
           f"A(H) < 0 a {sorted(np.round(neg.delta_e, 3))} ; A(H) a 0,475 = "
           f"{_pres(bud, 0.475).A_H_mesure_median:.2f}",
           "QCD_budget_preuve_full")
    _ligne("QC3 l.129", "-20,8", f"{bud.A_H_mesure_median.min():.1f}", "QCD_budget_preuve_full")

    _sous_titre("l. 133-136 : « 0,024 -> 0,007 en fin d'horizon », « environ trente unites »")
    print("      erreur de fin d'horizon, bande haute, par fenetre (table = QCD_fin_horizon_full) :")
    piv = fin[fin.bande_haute].pivot(index="delta_e", columns="fenetre_derniers_pas",
                                     values="erreur_fin_horizon")
    piv.insert(0, "p_hat_0", fin[fin.bande_haute].groupby("delta_e").p_hat_0_mean.first())
    print(piv.to_string(float_format=lambda v: f"{v:.4f}"))
    f50 = fin[(fin.fenetre_derniers_pas == 50)]
    _ligne("QC3 l.134", "0,024 avant la rupture",
           f"p_hat_0 moyen {f50.p_hat_0_mean.mean():.4f} (grille), median campagne "
           f"{ind.p_hat_0.median():.4f}", "QCD_fin_horizon_full.p_hat_0_mean")
    tol = 5e-4
    ou = fin[np.isclose(fin.erreur_fin_horizon, 0.007, atol=tol)]
    _ligne("QC3 l.134", "0,007 en fin d'horizon (ni amplitude ni fenetre)",
           "tombe a " + "; ".join(f"Delta_e = {x.delta_e:.3f}, w = {x.fenetre_derniers_pas} "
                                  f"({x.erreur_fin_horizon:.4f})" for x in ou.itertuples())
           if len(ou) else "nulle part a +-0,0005 pres",
           "QCD_fin_horizon_full")
    ou24 = fin[np.isclose(fin.erreur_fin_horizon, 0.0024, atol=tol)]
    _ligne("QC3 (1er audit)", "0,0024",
           "tombe a " + "; ".join(f"Delta_e = {x.delta_e:.3f}, w = {x.fenetre_derniers_pas}"
                                  for x in ou24.itertuples()) if len(ou24) else "nulle part",
           "QCD_fin_horizon_full")
    b482 = f50[f50.delta_e >= 0.482]
    b452 = f50[f50.bande_haute]
    print(f"      50 derniers pas : moyenne des {len(b482)} amplitudes >= 0,482 = "
          f"{b482.erreur_fin_horizon.mean():.4f} ; des {len(b452)} amplitudes >= 0,452 = "
          f"{b452.erreur_fin_horizon.mean():.4f}")
    top = fin[np.isclose(fin.delta_e, de_max)].iloc[0]
    _ligne("QC3 l.135", "environ trente unites retranchees",
           f"A(H) - A(w) = {top.A_H_mesure_median:.2f} - {top.A_w_mesure_median:.2f} = "
           f"{top.deficit_A_H_moins_A_w:.2f} a Delta_e = {top.delta_e:.4f}",
           "QCD_budget_preuve_full (via QCD_fin_horizon_full.deficit_A_H_moins_A_w)")
    print("      -> le 0,007 est exact a Delta_e = 0,488 (50 pas) et faux a 0,498 ; "
          "le « trente » est 38,15 ; le 0,0024 du 1er audit n'existe qu'a 0,498 sur >= 100 pas.")
    print("      deficit A(H) - A(w) sur la bande haute :")
    for x in f50[f50.bande_haute].itertuples():
        print(f"        Delta_e = {x.delta_e:.4f} : A(H) {x.A_H_mesure_median:7.2f}  "
              f"A(w) {x.A_w_mesure_median:6.2f}  deficit {x.deficit_A_H_moins_A_w:7.2f}")

    _sous_titre("l. 143-145 : sigma(p_hat_0) = 0,00298, +-6,0 sur A(H), ecart 14,5 a 0,028")
    sd = float(ind.p_hat_0.std(ddof=1))
    _ligne("QC3 l.144", "0,00298 ; +-6,0", f"{sd:.5f} ; H x sigma = {aq.H * sd:.2f}",
           "QCD_indicateurs_full.p_hat_0")
    b0 = bud.iloc[0]
    _ligne("QC3 l.145", "ecart de 14,5 a 0,028",
           f"A_predit_brut - A(w) = {b0.A_predit_brut:.2f} - {b0.A_w_mesure_median:.2f} = "
           f"{b0.A_predit_brut - b0.A_w_mesure_median:.2f}", "QCD_budget_preuve_full")

    _sous_titre("l. 158-162 : table tau_ARF mesure / predit / ratio / Delta_e x tau / A(w)")
    for c in (0.028, 0.141, 0.287, 0.436, 0.498):
        d = _pres(diag, c)
        print(f"      {d.delta_e:.3f} & {d.tau_arf_median:.0f} & {d.tau_arf_predit:.0f} & "
              f"{d.ratio_mesure_predit:.2f} & {d.budget_recalcule:.2f} & {d.A_w_mesure:.2f}")
    print("      table = QCD_diagnostic_ajustement_full")

    _sous_titre("l. 178-182 : le rectangle Delta_e x tau_ARF contre A(w) mesure, par amplitude")
    diag = diag.copy()
    diag["ecart_relatif"] = diag.budget_recalcule / diag.A_w_mesure - 1
    for d in diag.itertuples():
        print(f"      Delta_e = {d.delta_e:.4f} : rectangle {d.budget_recalcule:6.2f}  "
              f"A(w) {d.A_w_mesure:6.2f}  rapport {d.budget_recalcule / d.A_w_mesure:.3f}  "
              f"ecart {100 * d.ecart_relatif:+6.1f} %")
    sous = diag[diag.delta_e < 0.19]
    dessus = diag[diag.delta_e >= 0.19]
    _ligne("QC3 l.178", "surestime de 23 % a 43 % sous 0,19",
           f"{100 * sous.ecart_relatif.min():+.1f} % a {100 * sous.ecart_relatif.max():+.1f} % "
           f"sur {len(sous)} amplitudes", "QCD_diagnostic_ajustement_full")
    _ligne("QC3 l.179", "sous-estime de 20 % a 41 % au-dessus",
           f"{100 * dessus.ecart_relatif.min():+.1f} % a {100 * dessus.ecart_relatif.max():+.1f} % "
           f"sur {len(dessus)} amplitudes ; a Delta_e = {dessus.delta_e.iloc[0]:.4f} : "
           f"{100 * dessus.ecart_relatif.iloc[0]:+.1f} %", "QCD_diagnostic_ajustement_full")
    au_dela = dessus.iloc[1:]
    print(f"      au-dela de 0,194 : {100 * au_dela.ecart_relatif.min():+.1f} % a "
          f"{100 * au_dela.ecart_relatif.max():+.1f} %")
    print("      -> le +43 % est a 0,085 (cote « sous 0,19 ») ; -6,9 % a 0,194 est hors de "
          "l'intervalle « 20 a 41 % » annonce.")
    change = diag[(diag.ecart_relatif.shift(1) > 0) & (diag.ecart_relatif < 0)]
    _ligne("QC3 l.180", "changement de signe vers 0,19",
           f"premier ecart negatif a Delta_e = {change.delta_e.iloc[0]:.4f}" if len(change) else "aucun",
           "QCD_diagnostic_ajustement_full")
    _ligne("QC3 l.196", "-41 % a +43 %",
           f"{100 * diag.ecart_relatif.min():+.1f} % a {100 * diag.ecart_relatif.max():+.1f} %",
           "QCD_diagnostic_ajustement_full")

    _sous_titre("l. 167-171 : ratio mesure / predit 0,19 ; > 2 vers 0,141 ; ~1 vers 0,287 ; 0,76")
    print(f"      min {diag.ratio_mesure_predit.min():.2f} a {diag.delta_e[diag.ratio_mesure_predit.idxmin()]:.3f}, "
          f"max {diag.ratio_mesure_predit.max():.2f} a {diag.delta_e[diag.ratio_mesure_predit.idxmax()]:.3f}, "
          f"dernier {diag.ratio_mesure_predit.iloc[-1]:.2f}")
    print("      table = QCD_diagnostic_ajustement_full.ratio_mesure_predit")

    _sous_titre("l. 186 : « 6 to 14 times later » (QC1 : 6,0 a 14,3)")
    print("      voir le bloc QC1 l.132 : meme chiffre, meme table.")

    _sous_titre("l. 209 : socle mesure 0,0231")
    _ligne("QC3 l.209", "0,0231", f"{ind.p_hat_0.mean():.4f} (moyenne), {ind.p_hat_0.median():.4f} (mediane)",
           "QCD_indicateurs_full.p_hat_0")

    _sous_titre("forme : ---, ~: et em-dashes dans le .tex")
    tex = (TEX / "redaction_QC3_invariance.tex").read_text(encoding="utf-8")
    lignes = tex.splitlines()
    tirets = [i + 1 for i, l in enumerate(lignes) if "---" in l and "\\title" not in l]
    print(f"      « --- » hors titre : {len(tirets)} aux lignes {tirets}")
    print(f"      « ~: » : {tex.count('~:')} ; em-dash litteral : {tex.count(chr(0x2014))}")
    print(f"      « M = 10 » dans le preambule : {'M=10' in tex.replace(' ', '') or 'M = 10' in tex}")


# ----------------------------------------------------------------------
# QD : les deux chiffres de D contestes par l'audit
# ----------------------------------------------------------------------
def qd() -> None:
    _titre("QD -- deux chiffres de QD1 et QD4 contestes")

    ind = _t("QCD_indicateurs_full")
    dom = domaine_decision()

    _sous_titre("QD1 l. 183 et QD4 l. 209 : « 62 % a Delta_e = 0,085 »")
    g = ind[np.isclose(ind.delta_e, 0.0854, atol=5e-4)]
    ok = g.tau_det_8.notna()
    k = int((g.loc[ok, "tau_det_8"] < g.loc[ok, "tau_arf"]).sum())
    n = int(ok.sum())
    lo, hi = wilson(k, n)
    _ligne("QD1 l.183 / QD4 l.209", "62 %",
           f"{k}/{n} = {100 * k / n:.1f} % [Wilson {100 * lo:.1f} ; {100 * hi:.1f}]",
           "QCD_indicateurs_full.tau_det_8, .tau_arf")
    print("      -> 62 est le NUMERATEUR (62 victoires sur 96 non censures), pas le pourcentage.")

    _sous_titre("QD4 l. 118 : pire censure de tau_det a lambda = 25, dans et hors domaine")
    for lam in (25, 50):
        c = ind.groupby("delta_e")[f"censored_det_{lam}"].mean()
        c_dom = c[c.index.isin(dom)]
        c_hors = c[~c.index.isin(dom)]
        _ligne("QD4 l.118", f"lambda = {lam} : pire 1,0000 (domaine)",
               f"grille : {c.max():.4f} a Delta_e = {c.idxmax():.3f} ; domaine : {c_dom.max():.4f} "
               f"a Delta_e = {c_dom.idxmax():.3f} ; hors domaine : {c_hors.max():.4f} a {c_hors.idxmax():.3f}",
               "QCD_indicateurs_full.censored_det_*")
        pires = c_dom[c_dom == c_dom.max()]
        print(f"      amplitudes du domaine au pire : {sorted(np.round(pires.index, 3))}")
    c8 = ind.groupby("delta_e").censored_det_8.mean()
    _ligne("QD4 l.117", "lambda = 8 : 0,9000 (0,028) ; 0,0000 dans le domaine",
           f"grille {c8.max():.4f} a {c8.idxmax():.3f} ; domaine {c8[c8.index.isin(dom)].max():.4f}",
           "QCD_indicateurs_full.censored_det_8")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--sous", choices=["QC1", "QC2", "QC3", "QD"], default=None)
    a = p.parse_args()
    for nom, f in {"QC1": qc1, "QC2": qc2, "QC3": qc3, "QD": qd}.items():
        if a.sous is None or a.sous == nom:
            f()
    print()


if __name__ == "__main__":
    main()
