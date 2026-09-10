"""
chiffres_QD.py
===================================================================
Extraction, sous-question par sous-question, des valeurs citees dans les
quatre redactions de la question D.

LECTURE SEULE. N'ecrit aucune table, ne recalcule aucun indicateur, ne
resimule rien. Chaque chiffre du texte LaTeX doit se retrouver dans la
sortie de ce script, de `derives_QD.py` ou de `contre_exemple_kendall.py`
-- c'est la contrainte de tracabilite de `.claude/rules/redaction.md`.

TROIS VERIFICATIONS ACQUISES, REPRODUITES ICI
    1. Le "18 a 48 %" de R publie dans JOURNAL.md et README.md est faux :
       R_tau_arf est negatif sur 5 amplitudes et monte a +0,885.
    2. Le "49 a 75 %" de G est exact, mais seulement sur le domaine de
       decision ; sur la grille entiere il descend a 0,10.
    3. L'effondrement par agregation est reel, et le comparateur concerne
       est A_H : tau_b global 0,3965 contre une mediane stratifiee 0,0526.

USAGE
    python chiffres_QD.py            # tout
    python chiffres_QD.py --sous D3  # une seule sous-question
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

RACINE = Path(__file__).resolve().parents[1]
DATA = RACINE / "resultats" / "data"

# Domaine de decision : les 18 amplitudes retenues pour l'interpretation.
# La colonne `dans_domaine_decision` de la table stratifiee en fait foi ;
# on ne le redefinit pas ici.
LAMBDAS = (8, 25, 50)


def _t(nom: str) -> pd.DataFrame:
    return pd.read_parquet(DATA / f"{nom}.parquet")


def _titre(s: str) -> None:
    print()
    print("=" * 74)
    print(s)
    print("=" * 74)


def _sous_titre(s: str) -> None:
    print()
    print(f"--- {s}")


# ----------------------------------------------------------------------
# D.1 : instrumentation conjointe
# ----------------------------------------------------------------------
def d1() -> None:
    _titre("D.1 -- instrumentation conjointe")

    ind = _t("QCD_indicateurs_full")
    rg = _t("QCD_R_et_G_full")

    _sous_titre("campagne")
    print(f"runs                 : {len(ind)}")
    print(f"amplitudes           : {ind.delta_e.nunique()}")
    print(f"graines par amplitude: {ind.groupby('delta_e').size().unique().tolist()}")
    print(f"delta_e              : {ind.delta_e.min():.6f} a {ind.delta_e.max():.6f}")
    print(f"baseline_window      : {sorted(ind.baseline_window.unique().tolist())}")

    _sous_titre("socle p_hat_0 (fenetre 3 000 pas, la seule presente)")
    print(f"p_hat_0 median       : {ind.p_hat_0.median():.6f}")
    print(f"p_hat_0 min / max    : {ind.p_hat_0.min():.6f} / {ind.p_hat_0.max():.6f}")

    _sous_titre("R(tau_ARF) -- fraction d'adaptation acquise a tau_ARF")
    dom = rg.delta_e.isin(
        _t("QCD_correlations_stratifiees_full")
        .query("dans_domaine_decision")
        .delta_e.unique()
    )
    print(f"grille entiere (20)  : [{rg.R_tau_arf.min():+.4f} ; {rg.R_tau_arf.max():+.4f}]")
    print(f"domaine decision (18): [{rg.loc[dom, 'R_tau_arf'].min():+.4f} ; "
          f"{rg.loc[dom, 'R_tau_arf'].max():+.4f}]")
    neg = rg[rg.R_tau_arf < 0]
    print(f"amplitudes ou R < 0  : {len(neg)} -> "
          f"{[round(x, 3) for x in neg.delta_e.tolist()]}")
    print(f"  valeurs            : {[round(x, 4) for x in neg.R_tau_arf.tolist()]}")
    print("  >>> le '18 a 48 %' publie dans JOURNAL.md:35 et README.md:96 n'est")
    print("      reproductible sous AUCUNE restriction. A corriger (tache 8).")

    _sous_titre("R : les deux amplitudes qui contredisent le verdict du journal")
    for de in (0.085449, 0.140949):
        r = rg.loc[np.isclose(rg.delta_e, de, atol=1e-5)]
        if len(r):
            print(f"  delta_e = {r.delta_e.iloc[0]:.6f} : R = {r.R_tau_arf.iloc[0]:+.4f}")
    print("  >>> 'tot dans l'adaptation' n'est pas soutenu la : a delta_e = 0,085")
    print("      l'essentiel de l'adaptation est deja acquis a tau_ARF.")

    _sous_titre("G(tau_ARF) -- fraction de preuve accumulee a tau_ARF")
    print(f"grille entiere (20)  : [{rg.G_tau_arf_median.min():.4f} ; "
          f"{rg.G_tau_arf_median.max():.4f}]")
    print(f"domaine decision (18): [{rg.loc[dom, 'G_tau_arf_median'].min():.4f} ; "
          f"{rg.loc[dom, 'G_tau_arf_median'].max():.4f}]")
    print("  >>> le '49 a 75 %' est exact SUR LE DOMAINE DE DECISION seulement.")
    print("      La restriction se publie avec le chiffre.")

    _sous_titre("fenetre d'estimation du palier (bornee a tau_ARF/2)")
    print(rg[["delta_e", "tau_arf_median", "fenetre_palier", "e_palier",
              "e_theorique", "ecart_palier_theorie", "R_tau_arf"]]
          .head(8).to_string(index=False, float_format=lambda v: f"{v:9.4f}"))

    _sous_titre("ecart_palier_theorie : le controle du palier contre p_hat_0 + delta_e")
    n_neg = int((rg.ecart_palier_theorie < 0).sum())
    print(f"negatif sur          : {n_neg}/20 amplitudes")
    print(f"etendue              : [{rg.ecart_palier_theorie.min():+.4f} ; "
          f"{rg.ecart_palier_theorie.max():+.4f}]")
    print("  >>> le palier mesure est SYSTEMATIQUEMENT sous p_hat_0 + delta_e.")

    _sous_titre("evenements de remplacement")
    ev = _t("QCD_events_swap_full")
    print(f"evenements totaux    : {len(ev)}")
    print(f"colonnes             : {ev.columns.tolist()}")

    _sous_titre("tau_err : franchissements sans persistance (le piege du sec. 4)")
    te = _t("QCD_tau_err_full")
    au_premier_pas = te[te.tau_err_p1 == 1.0]
    print(f"amplitudes ou tau_err_p1 == 1 : {len(au_premier_pas)} -> "
          f"{[round(x, 3) for x in au_premier_pas.delta_e.tolist()]}")
    viol = te[te.avant_tau_arf_p1]
    print(f"violations sans persistance   : {len(viol)} -> "
          f"{[round(x, 3) for x in viol.delta_e.tolist()]}")
    print(f"  dont interpretables         : {int(viol.interpretable.sum())} -> "
          f"{[round(x, 3) for x in viol.loc[viol.interpretable, 'delta_e'].tolist()]}")
    print(f"  leurs tau_err_p1            : "
          f"{viol.loc[viol.interpretable, 'tau_err_p1'].tolist()}")
    print(f"violations avec persistance   : {int(te.avant_tau_arf_p20.sum())}")
    print("  >>> 2 amplitudes franchissent au 1er pas, 2 AUTRES au pas 101 :")
    print("      ce ne sont pas les memes. Ne pas confondre les deux comptes.")
    haut = te.iloc[-1]
    print(f"en haut de grille (Delta_e = {haut.delta_e:.3f}) : tau_err_p1 = "
          f"{haut.tau_err_p1:.0f}, tau_err_p20 = {haut.tau_err_p20:.0f}")
    print("  >>> le seuil est franchi la parce que la tache est PLUS FACILE,")
    print("      pas parce que la foret s'est adaptee (test de la tache facilitee).")

    _sous_titre("la course tau_det contre tau_ARF, par seuil")
    for lam in LAMBDAS:
        td, ta = ind[f"tau_det_{lam}"], ind["tau_arf"]
        ok = td.notna() & ta.notna()
        n = int(ok.sum())
        part = float((td[ok] < ta[ok]).mean()) if n else float("nan")
        print(f"  lambda = {lam:2d} : tau_det < tau_ARF dans {100 * part:6.2f} % "
              f"des {n} runs non censures")
    print("  >>> le point aveugle est une propriete du REGLAGE, pas du dispositif.")

    _sous_titre("fenetre du palier aux amplitudes ou R < 0")
    print(f"  {rg.loc[rg.R_tau_arf < 0, 'fenetre_palier'].tolist()}")
    print("  >>> le bornage a tau_ARF/2 EST actif et R reste negatif.")

    _sous_titre("le socle SANS drift (campagne A1_nodrift, 100 runs)")
    try:
        ev0 = _t("QCD_events_swap_A1_nodrift")
        m0 = _t("QCD_runs_meta_A1_nodrift")
        tr0 = _t("QCD_traces_error_A1_nodrift")
        premiers = ev0.groupby(["run_id", "tree_id"], sort=False).t.min().reset_index()
        print(f"  runs                          : {len(m0)}")
        print(f"  remplacements par run (mediane): "
              f"{ev0.groupby('run_id').size().median():.0f}")
        print(f"  arbres distincts (mediane)     : "
              f"{premiers.groupby('run_id').size().median():.0f}")
        print(f"  erreur moyenne post-rupture    : {tr0.e.mean():.4f}")
        print(f"  p_hat_0 median                 : {m0.p_hat_0.median():.4f}")
        print("  >>> sans le moindre drift, la foret renouvelle quand meme la")
        print("      quasi-totalite de ses arbres sur l'horizon. C'est le socle")
        print("      du JOURNAL section 2 b, mesure ici sur 100 runs et non 12.")
        print("  ATTENTION : l'erreur d'une foret qui ne remplace JAMAIS rien")
        print("      (0,0125 au JOURNAL section 2 b) n'est PAS recalculable ici :")
        print("      elle vient de verif_biais.py, 12 executions, sortie non")
        print("      persistee. Toute citation doit porter cette reserve.")
    except FileNotFoundError:
        print("  campagne A1_nodrift absente")


# ----------------------------------------------------------------------
# D.2 : coefficient d'association
# ----------------------------------------------------------------------
def d2() -> None:
    _titre("D.2 -- coefficient d'association")

    ind = _t("QCD_indicateurs_full")

    _sous_titre("censure globale, par comparateur")
    for c in ("arf", "swap_10", "swap_25", "swap_50", "swap_75",
              "det_8", "det_25", "det_50"):
        col = f"censored_{c}"
        if col in ind.columns:
            print(f"  {col:22s} : {ind[col].mean():.4f}")

    _sous_titre("A(H) et S_max(H) : definis partout, jamais censures")
    for c in ("A_H", "S_max_H"):
        print(f"  {c:10s} : {int(ind[c].notna().sum())}/{len(ind)} valeurs, "
              f"etendue [{ind[c].min():.4f} ; {ind[c].max():.4f}]")
    print("  >>> ex aequo d'un seul cote pour tau_ARF vs A(H) / S_max(H) ;")
    print("      des deux cotes pour tau_ARF vs tau_swap(q).")

    _sous_titre("ex aequo : nombre de valeurs distinctes (structure des blocs)")
    for c in ("tau_arf", "tau_swap_25", "tau_swap_50", "A_H", "S_max_H"):
        print(f"  {c:12s} : {ind[c].nunique():5d} distinctes sur {len(ind)}")

    _sous_titre("non-linearite : tau_ARF par amplitude (Pearson est invalide)")
    g = ind.groupby("delta_e").tau_arf.median()
    print(f"  tau_arf median : {g.iloc[0]:.0f} a delta_e={g.index[0]:.3f} -> "
          f"{g.iloc[-1]:.0f} a delta_e={g.index[-1]:.3f}")
    print(f"  rapport        : {g.iloc[0] / g.iloc[-1]:.1f}")


# ----------------------------------------------------------------------
# D.3 : stratification
# ----------------------------------------------------------------------
def d3() -> None:
    _titre("D.3 -- stratification par amplitude")

    st = _t("QCD_correlations_stratifiees_full")
    gl = _t("QCD_correlation_globale_full")

    _sous_titre("comparateurs et couverture")
    print(f"comparateurs : {sorted(st.comparateur.unique().tolist())}")
    print(f"cellules     : {len(st)} = {st.comparateur.nunique()} x "
          f"{st.delta_e.nunique()}")
    print(f"NaN sur tau_b: {int(st.tau_b.isna().sum())}")

    _sous_titre("seuil de detectabilite (valeur unique, a citer sans arrondi)")
    vals = st.seuil_detectabilite.unique()
    print(f"  {vals.tolist()}")

    _sous_titre("tautologie : tau_swap_10 EST tau_ARF a M = 10")
    t10 = st[st.comparateur == "tau_swap_10"]
    print(f"  cellules            : {len(t10)}")
    print(f"  tau_b               : min {t10.tau_b.min():.6f}, max {t10.tau_b.max():.6f}")
    print(f"  IC                  : [{t10.ci_lo.min():.3f} ; {t10.ci_hi.max():.3f}]")
    print(f"  discernable         : {int(t10.discernable.sum())}/{len(t10)}")
    print("  >>> 1,000000 par IDENTITE, pas par performance. A marquer")
    print("      tautologique, comme S_max(H) en B2 (JOURNAL.md section 8).")

    _sous_titre("le resultat central de D : A(H) contre S_max(H)")
    dom = st[st.dans_domaine_decision]
    for c in ("A_H", "S_max_H"):
        s = dom[dom.comparateur == c]
        print(f"  {c:10s} : discernable {int(s.discernable.sum())}/{len(s)}, "
              f"mediane tau_b {s.tau_b.median():+.4f}")
        pos = s[s.ci_lo > 0]
        if len(pos):
            print(f"              IC entierement > 0 a partir de "
                  f"delta_e = {pos.delta_e.min():.3f} ({len(pos)} cellules)")
    print("  >>> la grandeur qui DECIDE l'alarme est S_max(H), pas A(H).")
    print("      Le JOURNAL.md section 1 accroche sa parenthese au mauvais objet.")

    _sous_titre("effondrement par agregation")
    for _, r in gl.iterrows():
        med = st[(st.comparateur == r.comparateur) &
                 st.dans_domaine_decision].tau_b.median()
        print(f"  {r.comparateur:12s} : global {r.tau_b_global:+.6f} | "
              f"mediane stratifiee (18) {med:+.6f} | "
              f"rapport {r.tau_b_global / med if med else float('nan'):6.2f}")
    print("  >>> le coefficient global ne confirme pas un lien faible :")
    print("      il en FABRIQUE un. C'est l'artefact de Simpson sur delta_e.")

    _sous_titre("multiplicite (JOURNAL.md section 8)")
    n_tests = len(dom)
    n_signif = int((dom.p_value < 0.05).sum())
    print(f"  cellules du domaine    : {n_tests}")
    print(f"  significatives a 5 %   : {n_signif}")
    print("  >>> les cellules dont |tau_b| avoisine 0,15 ne se citent pas")
    print("      individuellement sans correction.")

    _sous_titre("table complete du domaine de decision")
    aff = dom[["delta_e", "comparateur", "n", "tau_b", "ci_lo", "ci_hi",
               "discernable", "censure_comparateur"]]
    print(aff.to_string(index=False, float_format=lambda v: f"{v:8.4f}"))


# ----------------------------------------------------------------------
# D.4 : protocole de decision et censure
# ----------------------------------------------------------------------
def d4() -> None:
    _titre("D.4 -- protocole de decision et sensibilite a la censure")

    ind = _t("QCD_indicateurs_full")
    st = _t("QCD_correlations_stratifiees_full")
    cc = _t("QCD_cas_complets_full")

    _sous_titre("le point aveugle chiffre")
    for lam in LAMBDAS:
        col = f"censored_det_{lam}"
        if col in ind.columns:
            n_alarme = int((~ind[col].astype(bool)).sum())
            print(f"  lambda = {lam:2d} : {n_alarme:4d}/{len(ind)} alarment "
                  f"({100 * ind[col].mean():5.2f} % de silence)")
    print("  >>> a lambda = 50, aucune correlation impliquant tau_det n'est")
    print("      calculable. C'est pourquoi la campagne ne fige aucun lambda.")

    _sous_titre("censure PAR AMPLITUDE : ce que le global masque")
    for c in ("tau_swap_75", "tau_swap_50", "tau_swap_25"):
        s = st[st.comparateur == c]
        if len(s):
            print(f"  {c:12s} : global {ind[f'censored_{c[4:]}'].mean():.4f} | "
                  f"max par amplitude {s.censure_comparateur.max():.4f} "
                  f"(a delta_e = {s.loc[s.censure_comparateur.idxmax(), 'delta_e']:.3f})")
    seuil_groupe = 0.05
    s75 = st[st.comparateur == "tau_swap_75"]
    if len(s75):
        pire = s75.censure_comparateur.max()
        print(f"  >>> critere D2 du groupe : censure <= {seuil_groupe:.0%}.")
        print(f"      tau_swap_75 le depasse d'un facteur {pire / seuil_groupe:.0f}.")

    _sous_titre("la censure pilote-t-elle le resultat ? (impute vs cas complets)")
    print(f"  ecart max absolu : {cc.ecart.abs().max():.6f}")
    for c in sorted(cc.comparateur.unique()):
        s = cc[cc.comparateur == c]
        print(f"  {c:12s} : ecart [{s.ecart.min():+.6f} ; {s.ecart.max():+.6f}]")
    nuls = [c for c in cc.comparateur.unique()
            if cc[cc.comparateur == c].ecart.abs().max() < 1e-9]
    print(f"  ecart exactement nul : {nuls}")
    print("  >>> NON. La censure ne pilote pas le resultat. Reponse tranchee.")
    print("      ROADMAP.md section 7 dit 'coincident a trois decimales' :")
    print("      trop fort pour swap_75, a corriger (tache 8).")

    _sous_titre("les deux regles de significativite qui divergent")
    dom = st[st.dans_domaine_decision].copy()
    dom["ic_exclut_zero"] = (dom.ci_lo > 0) | (dom.ci_hi < 0)
    div = dom[dom.discernable != dom.ic_exclut_zero]
    print(f"  cellules en desaccord : {len(div)}")
    if len(div):
        print(div[["delta_e", "comparateur", "tau_b", "ci_lo", "ci_hi",
                   "discernable", "ic_exclut_zero"]]
              .to_string(index=False, float_format=lambda v: f"{v:8.4f}"))
    print("  >>> D.4 doit FIXER la regle, la justifier, et l'appliquer partout.")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--sous", choices=["D1", "D2", "D3", "D4"], default=None,
                   help="n'imprimer qu'une sous-question")
    a = p.parse_args()

    fonctions = {"D1": d1, "D2": d2, "D3": d3, "D4": d4}
    for nom, f in fonctions.items():
        if a.sous is None or a.sous == nom:
            f()
    print()


if __name__ == "__main__":
    main()
