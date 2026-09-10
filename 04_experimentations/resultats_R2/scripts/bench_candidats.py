"""
bench_candidats.py
===================================================================
Banc de qualification des candidats au remplacement de `tau_ARF`.

Les criteres et leurs seuils sont figes AVANT toute mesure dans
`../../pistes_remplacement_tauARF.md` § 8, committe le 8 septembre 2026. Ce
script ne fait que les appliquer. Il ne resimule rien : tout se lit sur les
campagnes deja ecrites.

Remplace et generalise `bench_analyse.py`, qui n'implementait A1 et C1 que pour
`tau_ARF` et portait un chemin absolu en dur — donc inexecutable chez les trois
autres membres du groupe.

CE QUI EST MESURE ICI (sans etalon, donc sans nouvelle campagne)
    A1  la metrique se tait-elle quand il n'y a rien a detecter ?
    C1  depend-elle de la taille de la foret ?
    D1  fidelite     D2  censure     D3  granularite
    Validation de l'etalon analytique : `--valider-etalon` (cinq controles bloquants).
    A2, B1, B2 : `--banc-etalon`, une fois l'etalon valide.

DEFINITION DE L'AUC DU TEST A1 — a lire avant d'interpreter un chiffre
    AUC = P(le candidat indique une reaction PLUS FORTE sans drift qu'avec)
          + 0,5 x P(ex-aequo),  a amplitude fixee.

        0 %   la metrique est muette sans drift : c'est le comportement voulu
        50 %  elle ne distingue pas un drift de son absence
        > 50 % elle est ANTI-INFORMATIVE : elle reagit plus fort quand il ne se
              passe rien

    « Reaction plus forte » depend de l'orientation du candidat, declaree dans
    CANDIDATS : pour un temps, plus petit ; pour une aire ou un comptage, plus
    grand. Sans cette declaration, « AUC <= x » n'a pas le meme sens pour les deux.

    Le PLANCHER MECANIQUE vaut 0,5 x taux d'ex-aequo : une metrique a faible
    granularite ne peut pas descendre en dessous, quoi qu'elle vaille. Le critere
    est donc relatif au plancher (AUC <= plancher + 10 points) et non absolu — un
    seuil absolu punirait la discretion de l'echelle, que D3 mesure deja.

BOOTSTRAP APPARIE SUR LES GRAINES — et pourquoi ce n'est pas un detail
    Les campagnes partagent `seeds = range(1, n+1)` et le flux pre-rupture ne
    depend pas de `boundary_shift` (`exp_QCD_campagne.py:115`) : a graine egale,
    les runs b = 0 et b > 0 sont identiques bit a bit sur les 3 000 pas
    pre-rupture. On reechantillonne donc LA GRAINE une seule fois, et les deux
    groupes suivent. Reechantillonner les deux groupes independamment surestime
    l'intervalle de moitie.

USAGE
    PYTHONHASHSEED=0 python bench_candidats.py
"""

import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import rankdata

warnings.filterwarnings('ignore')

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA = ROOT_DIR / "resultats" / "data"
FIGURES = ROOT_DIR / "resultats" / "figures"
FIGURES.mkdir(parents=True, exist_ok=True)

H = 2000
N_MODELS = 10
N_BOOT = 2000                       # comme analyse_QCD.py:50
SEED_BOOT = 20260908
FENETRES = (50, 100, 200, 500, 2000)
QUOTAS = (10, 25, 50, 75, 100)      # 100 % = tau_erase

# --- Candidats, avec leur orientation et leur domaine declares A PRIORI ---------
# 'sens' = +1 si une valeur HAUTE signale une reaction plus forte, -1 sinon.
# 'extensif' = la grandeur croit mecaniquement avec M et doit etre normalisee par
# M avant C1, sans quoi elle echoue par les unites et non par la qualite.
CANDIDATS = {}
# tau_ARF est le PREMIER remplacement, un seul arbre, quelle que soit la taille de
# la foret. Ce n'est `tau_swap(10 %)` qu'a M = 10 : a M = 50, un quota de 10 %
# exigerait 5 arbres et mesurerait tout autre chose. Les confondre annulait le
# resultat C1 de la note (rapport 0,05 entre M=5 et M=50), qui devenait 0,48.
CANDIDATS['tau_arf'] = {
    'sens': -1, 'extensif': False,
    'libelle': "tau_ARF, premier remplacement (1 arbre, tout M)",
}
for _q in QUOTAS:
    CANDIDATS[f'tau_swap_{_q}'] = {
        'sens': -1, 'extensif': False,
        'libelle': (f"tau_erase = tau_swap(100 %)" if _q == 100 else
                    f"tau_swap({_q} %)"),
    }
for _w in FENETRES:
    CANDIDATS[f'N_{_w}'] = {
        'sens': +1, 'extensif': True,
        'libelle': f"N(W = {_w}), remplacements cumules",
    }
    CANDIDATS[f'exces_{_w}'] = {
        'sens': +1, 'extensif': True,
        'libelle': f"exces apparie N_drift - N_nodrift, W = {_w}",
    }
# ORIENTATION CORRIGEE APRES AUDIT. A(H) et S_max(H) avaient ete declares 'sens' = +1
# (« valeur haute = reaction plus forte »), ce qui est semantiquement FAUX : une aire
# d'erreur excedentaire GRANDE signale une adaptation LENTE, pas une reaction vive.
# La correction n'est pas un ajustement opportuniste — c'est une erreur de
# specification, et elle change les verdicts : A1 de A(H) passe de 9/20 a 2/20, et
# le tau-b negatif de B1 cesse d'etre lu comme une « refutation ». Les deux lectures
# sont consignees dans le JOURNAL.
CANDIDATS['A_H'] = {'sens': -1, 'extensif': False,
                    'libelle': "A(H), aire d'erreur excedentaire (grande = lent)"}
CANDIDATS['S_max_H'] = {'sens': -1, 'extensif': False,
                        'libelle': "S_max(H), budget de preuve (grand = lent)"}


# ------------------------------------------------------------------ lecture ----
DELTA_P = 0.01                      # StrictCUSUM(delta=0.01) dans R2


def charger(tag):
    """meta + evenements + trajectoires d'une campagne.

    Aucun indicateur n'est LU : A(H) et S_max(H) se recalculent ici depuis les
    traces, comme dans `analyse_QCD.py`. C'est ce qui les rend disponibles pour la
    ligne de base et pour les campagnes C1, ou aucune table d'indicateurs n'existe.
    """
    meta = pd.read_parquet(DATA / f"QCD_runs_meta_{tag}.parquet").sort_values('run_id')
    events = pd.read_parquet(DATA / f"QCD_events_swap_{tag}.parquet")
    traces = pd.read_parquet(DATA / f"QCD_traces_error_{tag}.parquet")
    mat = (traces.pivot(index='run_id', columns='t', values='e')
           .reindex(meta['run_id'].to_numpy()).to_numpy(dtype=float))
    return meta.reset_index(drop=True), events, mat


def aire_et_budget(meta, error_mat):
    """A(H) = somme des ecarts au socle ; S_max(H) = maximum du CUSUM (Lindley)."""
    p0 = meta['p_hat_0'].to_numpy(dtype=float)[:, None]
    ecart = error_mat - p0
    a_h = ecart.sum(axis=1)
    s = np.zeros(len(meta))
    s_max = np.zeros(len(meta))
    for t in range(error_mat.shape[1]):
        s = np.maximum(0.0, s + ecart[:, t] - DELTA_P)
        s_max = np.maximum(s_max, s)
    return a_h, s_max


def candidats_par_run(meta, events, n_models=None, error_mat=None):
    """Construit tous les candidats disponibles sans etalon, un run par ligne.

    tau_swap(q) compte les arbres DISTINCTS renouveles : un arbre remplace trois
    fois ne vaut qu'un arbre renouvele. N(W) compte au contraire TOUS les
    evenements de la fenetre, y compris les remplacements repetes du meme arbre —
    les deux grandeurs ne mesurent pas la meme chose, et c'est voulu.
    """
    M = int(n_models if n_models is not None else meta.get('n_models', pd.Series([N_MODELS])).iloc[0])
    out = meta.copy()
    n = len(meta)
    idx = {rid: i for i, rid in enumerate(meta['run_id'].to_numpy())}

    tau = {q: np.full(n, np.nan) for q in QUOTAS}
    tau_premier = np.full(n, np.nan)
    N_w = {w: np.zeros(n, dtype=float) for w in FENETRES}

    if len(events):
        ev = events.sort_values(['run_id', 't'], kind='stable')
        for run_id, grp in ev.groupby('run_id', sort=False):
            i = idx.get(int(run_id))
            if i is None:
                continue
            ts = grp['t'].to_numpy()
            tids = grp['tree_id'].to_numpy()
            for w in FENETRES:
                N_w[w][i] = float((ts < w).sum())
            tau_premier[i] = float(ts[0])          # tau_ARF : un arbre, tout M
            seen, distinct = set(), np.empty(len(ts), dtype=np.int32)
            for k, tid in enumerate(tids):
                seen.add(int(tid))
                distinct[k] = len(seen)
            for q in QUOTAS:
                # Quota en NOMBRE D'ARBRES, arrondi au superieur : « 25 % de 5 arbres »
                # vaut 2 arbres, soit 40 % de la foret. L'arrondi est donc publie
                # (colonne `arbres_requis_q`) au lieu d'etre confondu avec une
                # dependance a M, que C1 est precisement charge de tester.
                requis = int(np.ceil(q * M / 100.0))
                hit = np.flatnonzero(distinct >= requis)
                if hit.size:
                    tau[q][i] = float(ts[hit[0]])

    out['tau_arf'] = tau_premier
    out['censored_arf'] = np.isnan(tau_premier)
    for q in QUOTAS:
        out[f'tau_swap_{q}'] = tau[q]
        out[f'censored_swap_{q}'] = np.isnan(tau[q])
        out[f'arbres_requis_{q}'] = int(np.ceil(q * M / 100.0))
    for w in FENETRES:
        out[f'N_{w}'] = N_w[w]
    if error_mat is not None:
        out['A_H'], out['S_max_H'] = aire_et_budget(meta, error_mat)
    out['n_models_eff'] = M
    return out


def ajouter_exces(df_drift, df_nodrift):
    """Exces apparie N_drift(W) - N_nodrift(W), a GRAINE EGALE.

    Estimateur strictement meilleur que la soustraction d'un taux de fond global :
    le flux pre-rupture etant identique a graine egale, la difference elimine la
    variabilite de rodage au lieu de la moyenner.
    """
    base = df_nodrift.set_index('seed')
    for w in FENETRES:
        ref = df_drift['seed'].map(base[f'N_{w}'])
        df_drift[f'exces_{w}'] = df_drift[f'N_{w}'] - ref
    return df_drift


# -------------------------------------------------------------------- tests ----
def auc_a1(x_drift, x_nodrift, sens):
    """AUC du test A1 et son plancher d'ex-aequo. Voir l'en-tete pour la definition.

    Calculee par les rangs (Mann-Whitney), en O(n log n) : la forme naive en
    matrice de paires rendrait les 2 000 rejets du bootstrap intenables.
    """
    a = np.asarray(x_drift, dtype=float)
    b = np.asarray(x_nodrift, dtype=float)
    # Une valeur censuree (NaN) signale une absence de reaction : elle se place au
    # rang le plus defavorable a la reaction, jamais retiree en silence.
    pire = np.inf if sens == -1 else -np.inf
    a = np.where(np.isnan(a), pire, a)
    b = np.where(np.isnan(b), pire, b)
    if sens == -1:                      # « plus fort » = plus petit : on retourne l'axe
        a, b = -a, -b
    na, nb = len(a), len(b)
    both = np.concatenate([a, b])
    rangs = rankdata(both)              # rangs moyens : les ex-aequo comptent 1/2
    u = rangs[na:].sum() - nb * (nb + 1) / 2.0
    auc = float(u / (na * nb))
    # Taux d'ex-aequo, calcule sur les effectifs par valeur commune (pas de matrice).
    ca = pd.Series(a).value_counts()
    cb = pd.Series(b).value_counts()
    communes = ca.index.intersection(cb.index)
    ties = float((ca[communes] * cb[communes]).sum() / (na * nb)) if len(communes) else 0.0
    return auc, ties


def bootstrap_auc(x_drift, seeds_d, x_nodrift, seeds_n, sens, rng, n_boot=N_BOOT):
    """IC de l'AUC A1, en reechantillonnant LA GRAINE une seule fois."""
    communes = np.intersect1d(seeds_d, seeds_n)
    md = pd.Series(np.asarray(x_drift, dtype=float), index=np.asarray(seeds_d))
    mn = pd.Series(np.asarray(x_nodrift, dtype=float), index=np.asarray(seeds_n))
    md, mn = md[~md.index.duplicated()], mn[~mn.index.duplicated()]
    vals = []
    for _ in range(n_boot):
        tirage = rng.choice(communes, size=len(communes), replace=True)
        vals.append(auc_a1(md.loc[tirage].to_numpy(), mn.loc[tirage].to_numpy(), sens)[0])
    return float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))


def test_a1(df_drift, df_nodrift, rng):
    """A1, stratifie par amplitude, avec plancher d'ex-aequo et IC apparie."""
    lignes = []
    for nom, spec in CANDIDATS.items():
        if nom not in df_drift.columns or nom not in df_nodrift.columns:
            continue
        for de, g in df_drift.groupby('delta_e'):
            auc, ties = auc_a1(g[nom].to_numpy(), df_nodrift[nom].to_numpy(), spec['sens'])
            lo, hi = bootstrap_auc(g[nom].to_numpy(), g['seed'].to_numpy(),
                                   df_nodrift[nom].to_numpy(), df_nodrift['seed'].to_numpy(),
                                   spec['sens'], rng)
            plancher = 0.5 * ties
            lignes.append({
                'candidat': nom, 'test': 'A1', 'delta_e': de,
                'valeur': auc, 'ic_bas': lo, 'ic_haut': hi,
                'plancher': plancher, 'ex_aequo': ties,
                'passe': bool(auc <= plancher + 0.10),
            })
    return pd.DataFrame(lignes)


def test_c1(par_m, rng):
    """C1 : rapport des medianes M=5 -> M=50, IC bootstrap sur le rapport.

    Les grandeurs extensives sont normalisees par M AVANT le test : sans quoi
    N(W) echouerait parce qu'il compte des arbres, pas parce qu'il mesure mal.
    Un IC qui chevauche une borne de [0,7 ; 1,4] est declare INDECIS, pas rejete.
    """
    tailles = sorted(par_m)
    m_bas, m_haut = tailles[0], tailles[-1]
    lignes = []
    for nom, spec in CANDIDATS.items():
        if any(nom not in par_m[m].columns for m in (m_bas, m_haut)):
            continue
        amplitudes = np.intersect1d(par_m[m_bas]['delta_e'].unique(),
                                    par_m[m_haut]['delta_e'].unique())
        for de in amplitudes:
            def serie(m):
                g = par_m[m]
                v = g.loc[np.isclose(g['delta_e'], de), [nom, 'seed']].dropna()
                x = v[nom].to_numpy(dtype=float)
                return (x / m if spec['extensif'] else x), v['seed'].to_numpy()

            x_bas, s_bas = serie(m_bas)
            x_haut, s_haut = serie(m_haut)
            if len(x_bas) < 3 or len(x_haut) < 3:
                continue
            med_bas, med_haut = np.median(x_bas), np.median(x_haut)
            rapport = med_haut / med_bas if med_bas else np.nan
            communes = np.intersect1d(s_bas, s_haut)
            sb = pd.Series(x_bas, index=s_bas); sb = sb[~sb.index.duplicated()]
            sh = pd.Series(x_haut, index=s_haut); sh = sh[~sh.index.duplicated()]
            vals = []
            for _ in range(N_BOOT):
                tir = rng.choice(communes, size=len(communes), replace=True)
                a, b = np.median(sb.loc[tir]), np.median(sh.loc[tir])
                vals.append(b / a if a else np.nan)
            lo, hi = np.nanpercentile(vals, 2.5), np.nanpercentile(vals, 97.5)
            dedans = 0.7 <= rapport <= 1.4
            chevauche = not (lo >= 0.7 and hi <= 1.4) and not (hi < 0.7 or lo > 1.4)
            lignes.append({
                'candidat': nom, 'test': 'C1', 'delta_e': float(de),
                'valeur': float(rapport), 'ic_bas': float(lo), 'ic_haut': float(hi),
                'M_bas': m_bas, 'M_haut': m_haut,
                'passe': bool(dedans and not chevauche),
                'indecis': bool(chevauche),
            })
    return pd.DataFrame(lignes)


def tests_d(df_drift):
    """D1 fidelite, D2 censure, D3 granularite — tous stratifies par amplitude."""
    lignes = []
    for nom, spec in CANDIDATS.items():
        if nom not in df_drift.columns:
            continue
        for de, g in df_drift.groupby('delta_e'):
            x = g[nom].to_numpy(dtype=float)
            fini = x[~np.isnan(x)]
            censure = float(np.isnan(x).mean())
            med = float(np.median(fini)) if fini.size else np.nan
            iqr = float(np.subtract(*np.percentile(fini, [75, 25]))) if fini.size else np.nan
            n_distincts = int(pd.Series(fini).nunique())
            ref = g['tau_arf'].to_numpy(dtype=float)
            n_ref = int(pd.Series(ref[~np.isnan(ref)]).nunique())
            lignes += [
                {'candidat': nom, 'test': 'D1', 'delta_e': de,
                 'valeur': (iqr / abs(med) if med else np.nan), 'passe': None},
                {'candidat': nom, 'test': 'D2', 'delta_e': de,
                 'valeur': censure, 'passe': bool(censure <= 0.05)},
                {'candidat': nom, 'test': 'D3', 'delta_e': de,
                 'valeur': float(n_distincts), 'reference': float(n_ref),
                 'passe': bool(n_distincts >= n_ref)},
            ]
    return pd.DataFrame(lignes)


# --------------------------------------------------------------------- sortie --
def resume(bench):
    """Table candidat x test. « Non disqualifie » ne se lit jamais « valide »."""
    lignes = []
    for nom in CANDIDATS:
        sous = bench[bench.candidat == nom]
        if sous.empty:
            continue
        ligne = {'candidat': nom, 'libelle': CANDIDATS[nom]['libelle']}
        for test in ('A1', 'C1', 'D2', 'D3'):
            t = sous[sous.test == test]
            if t.empty:
                ligne[test] = None
                continue
            passe = t['passe'].dropna()
            ligne[test] = f"{int(passe.sum())}/{len(passe)}" if len(passe) else None
        a1 = sous[sous.test == 'A1']
        if not a1.empty:
            ligne['A1_max'] = float(a1['valeur'].max())
            ligne['A1_argmax_delta_e'] = float(a1.loc[a1['valeur'].idxmax(), 'delta_e'])
            ligne['A1_anti_informatif'] = int((a1['valeur'] > 0.5).sum())
        d1 = sous[sous.test == 'D1']
        if not d1.empty:
            ligne['D1_median'] = float(d1['valeur'].median())
        lignes.append(ligne)
    return pd.DataFrame(lignes)


def figure_auc_a1(bench, nom_fichier="Fig_QC_auc_A1.png"):
    """AUC A1 contre amplitude, par candidat, avec la bande a 50 % et les planchers."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    a1 = bench[bench.test == 'A1']
    montres = ['tau_arf', 'tau_swap_50', 'tau_swap_100',
               'N_200', 'exces_200', 'S_max_H']
    montres = [c for c in montres if c in set(a1.candidat)]
    fig, ax = plt.subplots(figsize=(9, 5.5))
    styles = ['-o', '-s', '-^', '--D', '--v', ':P']
    for c, st in zip(montres, styles):
        g = a1[a1.candidat == c].sort_values('delta_e')
        ax.plot(g.delta_e, 100 * g.valeur, st, ms=4, lw=1.3,
                label=CANDIDATS[c]['libelle'], color='black',
                alpha=0.35 + 0.65 * (montres.index(c) / max(len(montres) - 1, 1)))
        ax.plot(g.delta_e, 100 * g.plancher, ':', lw=0.7, color='0.6')
    ax.axhline(50, color='black', lw=1, ls='-.')
    ax.text(0.02, 51, "50 % : ne distingue pas un drift de son absence",
            fontsize=8, va='bottom')
    ax.fill_between([0, 0.52], 50, 100, color='0.9', zorder=0)
    ax.text(0.30, 92, "zone anti-informative", fontsize=9, color='0.35')
    ax.set_xlabel(r"amplitude du drift  $\Delta e$")
    ax.set_ylabel("AUC A1 (%) — la foret SANS drift reagit plus vite")
    ax.set_title("Test A1 : la metrique se tait-elle quand rien ne change ?\n"
                 "pointilles fins = plancher mecanique d'ex-aequo", fontsize=10)
    ax.set_xlim(0, 0.52); ax.set_ylim(0, 100)
    ax.legend(fontsize=8, loc='lower right')
    ax.grid(alpha=0.3)
    fig.savefig(FIGURES / nom_fichier, dpi=150, bbox_inches='tight')
    plt.close(fig)


def main():
    rng = np.random.default_rng(SEED_BOOT)
    print("=" * 78)
    print("BANC DES CANDIDATS — criteres figes le 8 septembre 2026 (pistes § 8)")
    print("=" * 78)

    meta_f, ev_f, mat_f = charger('full')
    meta_n, ev_n, mat_n = charger('A1_nodrift')
    drift_df = candidats_par_run(meta_f, ev_f, N_MODELS, mat_f)
    nodrift_df = candidats_par_run(meta_n, ev_n, N_MODELS, mat_n)
    drift_df = ajouter_exces(drift_df, nodrift_df)
    # Sans drift, l'exces est nul par construction : c'est la reference du test.
    for w in FENETRES:
        nodrift_df[f'exces_{w}'] = 0.0
    print(f"[INFO] campagne full : {len(drift_df)} runs, "
          f"{drift_df.delta_e.nunique()} amplitudes | ligne de base : {len(nodrift_df)} runs")

    par_m = {}
    for m in (5, 10, 20, 50):
        try:
            mm, ee, mat = charger(f'C1_M{m}')
        except FileNotFoundError:
            continue
        d = candidats_par_run(mm, ee, m, mat)
        for w in FENETRES:
            d[f'exces_{w}'] = np.nan       # pas de ligne de base par M : hors C1
        par_m[m] = d
    print(f"[INFO] campagnes C1 : M = {sorted(par_m)}")

    bench = pd.concat([
        test_a1(drift_df, nodrift_df, rng),
        test_c1(par_m, rng) if len(par_m) >= 2 else pd.DataFrame(),
        tests_d(drift_df),
    ], ignore_index=True)

    drift_df.to_parquet(DATA / "QCD_candidats_indicateurs.parquet", index=False)
    bench.to_parquet(DATA / "QCD_candidats_benchmark.parquet", index=False)
    syn = resume(bench)
    syn.to_parquet(DATA / "QCD_candidats_synthese.parquet", index=False)
    figure_auc_a1(bench)

    print("\nSYNTHESE candidat x test (cellules = amplitudes passees / testees)")
    print("« non disqualifie » ne se lit jamais « valide » : seul B1 departage.\n")
    cols = ['candidat', 'A1', 'C1', 'D2', 'D3', 'A1_max', 'A1_anti_informatif']
    print(syn[cols].to_string(index=False, float_format=lambda v: f"{v:.3f}"))

    a1 = bench[(bench.test == 'A1') & (bench.candidat == 'tau_arf')].sort_values('delta_e')
    print("\nTEST A1 POUR tau_ARF, par amplitude "
          "(AUC = part des paires ou la foret SANS drift reagit plus vite)")
    print(a1[['delta_e', 'valeur', 'ic_bas', 'ic_haut', 'plancher']]
          .to_string(index=False, float_format=lambda v: f"{v:.3f}"))
    pic = a1.loc[a1['valeur'].idxmax()]
    print(f"\n  maximum : {100 * pic['valeur']:.0f} % a delta_e = {pic['delta_e']:.3f} "
          f"[IC {100 * pic['ic_bas']:.0f} ; {100 * pic['ic_haut']:.0f}]")
    anti = a1[a1['ic_bas'] > 0.5]
    if len(anti):
        print(f"  ANTI-INFORMATIF (IC entierement au-dessus de 50 %) sur "
              f"{len(anti)} amplitudes : "
              f"delta_e de {anti.delta_e.min():.3f} a {anti.delta_e.max():.3f}")

    print(f"\n[SUCCESS] ecrit dans {DATA}")
    print(f"[SUCCESS] figure : {FIGURES / 'Fig_QC_auc_A1.png'}")




# ============================================================================ #
#  L'ETALON ANALYTIQUE — construction, puis les cinq controles qui le valident
# ============================================================================ #
#
# L'etalon n'est pas une metrique de plus : c'est la reference contre laquelle
# les autres sont jugees. Il doit donc etre valide AVANT d'etre utilise, et sur
# le pilote — c'est le point de sortie le moins cher si jamais il ne tient pas.
#
# Definition, figee dans `pistes_remplacement_tauARF.md` § 8 :
#     Etalon = aire sous acc_bande(t) sur [0, W_e],   W_e = 500 pas.
# Publies a cote, jamais agreges dedans : min_t acc_haut(t) et min_t acc_bas(t).

W_ETALON = 500                      # fenetre de l'etalon, declaree avant mesure
CHUTE_MAX = 0.10                    # au-dela, la competence conservee est signalee


def charger_etalon(tag):
    """Les relevés de sondes d'une campagne instrumentee, en taux par region."""
    meta = pd.read_parquet(DATA / f"QCD_etalon_meta_{tag}.parquet")
    sondes = pd.read_parquet(DATA / f"QCD_etalon_sondes_{tag}.parquet")
    votes = pd.read_parquet(DATA / f"QCD_etalon_votes_{tag}.parquet")
    sondes = sondes.merge(
        meta[['run_id', 'delta_e', 'delta_e_sondes', 'seed', 'boundary_shift']], on='run_id')
    votes = votes.merge(meta[['run_id', 'delta_e_sondes', 'seed']], on='run_id')
    # acc = fraction des sondes ou le VOTE de la foret donne la nouvelle etiquette.
    sondes['acc'] = sondes['n_vote_nouvelle'] / sondes['n_sondes']
    # V(t) = fraction d'arbres en desaccord avec la majorite, sur les memes sondes.
    votes['V'] = votes['somme_desaccord'] / votes['somme_votants']
    return meta, sondes, votes


def etalon_par_run(sondes, w=W_ETALON, pas=25):
    """Etalon scalaire par run, plus la competence conservee, publiee a cote."""
    fenetre = sondes[sondes.t < w]
    aire = (fenetre[fenetre.region == 'bande']
            .groupby('run_id')['acc'].sum() * pas).rename('etalon_aire')
    mins = (sondes[sondes.region.isin(['haut', 'bas'])]
            .groupby(['run_id', 'region'])['acc'].min().unstack()
            .rename(columns={'haut': 'min_acc_haut', 'bas': 'min_acc_bas'}))
    plateau = (sondes[(sondes.region == 'bande') & (sondes.t >= sondes.t.max() - 200)]
               .groupby('run_id')['acc'].mean().rename('plateau_bande'))
    # Le MINIMUM de acc_haut ne distingue pas un creux transitoire — normal pendant
    # la readaptation — d'un effondrement definitif sur « toujours 0 ». On publie
    # donc aussi sa valeur en FIN d'horizon : c'est elle qui separe les deux.
    fin = (sondes[(sondes.region == 'haut') & (sondes.t == sondes.t.max())]
           .set_index('run_id')['acc'].rename('acc_haut_fin'))
    depart = (sondes[(sondes.region == 'bande') & (sondes.t == 0)]
              .set_index('run_id')['acc'].rename('acc_bande_0'))
    return pd.concat([aire, mins, plateau, depart, fin], axis=1).reset_index()


def valider_etalon(tag_pilote='pilote_M10', tag_nodrift='pilote_nodrift_M10',
                   tag_sondes2='pilote_sondes777_M10'):
    """Les cinq controles du plan. Tous bloquants : l'etalon ne sert qu'apres."""
    echecs, lignes = [], []

    def note(num, nom, ok, detail):
        print(f"  [{'OK  ' if ok else 'ECHEC'}] {num}. {nom} : {detail}")
        lignes.append({'controle': num, 'nom': nom, 'passe': bool(ok), 'detail': detail})
        if not ok:
            echecs.append(f"{num}. {nom}")

    print("\n" + "=" * 78)
    print("VALIDATION DE L'ETALON — cinq controles, tous bloquants")
    print("=" * 78)
    meta, sondes, votes = charger_etalon(tag_pilote)
    par_run = etalon_par_run(sondes)
    par_run = par_run.merge(meta[['run_id', 'delta_e_sondes', 'seed']], on='run_id')

    # -- 1. Au premier releve, la foret est encore celle d'AVANT la rupture.
    #       Elle doit donc se tromper DANS la bande et avoir raison ailleurs.
    #       Seuils : 0,5 est le point de non-information, pas un seuil ajuste.
    t0 = sondes[sondes.t == 0].groupby(['delta_e_sondes', 'region'])['acc'].mean().unstack()
    ok1 = bool((t0['bande'] < 0.5).all() and (t0['haut'] > 0.9).all() and (t0['bas'] > 0.9).all())
    note(1, "acc_bande(0) < 0,5 et acc_haut(0), acc_bas(0) > 0,9", ok1,
         f"bande {t0['bande'].min():.3f}-{t0['bande'].max():.3f} | "
         f"haut {t0['haut'].min():.3f}+ | bas {t0['bas'].min():.3f}+")
    print("\n     acc au premier releve, par amplitude :")
    print(t0.round(3).to_string().replace('\n', '\n     '))

    # -- 2. acc_bande doit CROITRE et atteindre un plateau. Un plateau bas signale
    #       que l'erreur d'approximation domine — on le publie, on ne le tait pas.
    courbe = sondes[sondes.region == 'bande'].groupby(['delta_e_sondes', 't'])['acc'].mean()
    croissances = {}
    for de, g in courbe.groupby(level=0):
        v = g.droplevel(0).sort_index()
        croissances[de] = float(v.iloc[-8:].mean() - v.iloc[:4].mean())
    ok2 = all(c > 0 for c in croissances.values())
    plateaux = par_run.groupby('delta_e_sondes')['plateau_bande'].mean()
    note(2, "acc_bande croit et atteint un plateau", ok2,
         f"gain min {min(croissances.values()):+.3f} | "
         f"plateau de {plateaux.min():.3f} a {plateaux.max():.3f}")
    print("\n     plateau de acc_bande par amplitude (moyenne des 200 derniers pas) :")
    print(plateaux.round(3).to_string().replace('\n', '\n     '))

    # -- 3. LE CONTROLE QUI MANQUAIT A LA v1. Une foret qui bascule sur « toujours 0 »
    #       sature acc_bande a 1 en ayant tout desappris. On verifie donc que, en haut
    #       de grille, une montee rapide de acc_bande n'est PAS payee par un
    #       effondrement de acc_haut.
    haut_grille = par_run[par_run.delta_e_sondes >= 0.45]
    degeneres = haut_grille[haut_grille.min_acc_haut < 1 - CHUTE_MAX]
    definitifs = haut_grille[haut_grille.acc_haut_fin < 1 - CHUTE_MAX]
    if len(haut_grille) >= 3 and haut_grille['etalon_aire'].std() > 0:
        rho = float(np.corrcoef(haut_grille['etalon_aire'],
                                haut_grille['min_acc_haut'])[0, 1])
    else:
        rho = np.nan
    # Le critere de la v1 (« rho est un nombre ») etait une tautologie : il passait
    # quoi qu'il arrive. Le controle doit dire si l'etalon SEPARE les runs degeneres
    # des autres. Il echoue si les runs degeneres ont un etalon SUPERIEUR aux sains,
    # car alors l'etalon recompense l'effondrement au lieu de le penaliser.
    sains = haut_grille[haut_grille.acc_haut_fin >= 1 - CHUTE_MAX]
    if len(definitifs) and len(sains) >= 3:
        ecart = float(definitifs['etalon_aire'].median() - sains['etalon_aire'].median())
        ok3 = bool(ecart <= 0)
    else:
        ecart = np.nan
        ok3 = True
    note(3, "la degenerescence est DETECTEE, pas certifiee", ok3,
         f"{len(degeneres)}/{len(haut_grille)} runs signales, dont "
         f"{len(definitifs)} DEFINITIFS (acc_haut encore effondre en fin d'horizon) | "
         f"correlation aire vs acc_haut : {rho:+.3f} | "
         f"etalon des degeneres moins celui des sains : {ecart:+.1f} "
         f"(doit etre <= 0)")
    if len(degeneres):
        print(f"\n     ATTENTION — a delta_e >= 0,45, {len(degeneres)} runs atteignent "
              f"acc_bande = 1\n     en effondrant acc_haut (minimum mesure : "
              f"{haut_grille['min_acc_haut'].min():.3f}). La v1 les aurait comptes\n"
              f"     comme des adaptations exemplaires. Ils sont SIGNALES, pas agreges.\n"
              f"     Sur ces {len(degeneres)}, {len(definitifs)} ne se relevent jamais : "
              f"la foret repond\n     « toujours 0 » jusqu'a la fin. Les autres ne font que "
              f"traverser un creux.")

    # -- 4. Ligne de base : sans drift, la regle ne change pas, donc acc_bande — qui
    #       mesure l'adhesion a la NOUVELLE etiquette — doit rester bas.
    try:
        _, sondes0, _ = charger_etalon(tag_nodrift)
        base = sondes0[sondes0.region == 'bande'].groupby('delta_e_sondes')['acc'].mean()
        ok4 = bool((base < 0.5).all())
        note(4, "sans drift, acc_bande reste sous 0,5", ok4,
             f"de {base.min():.3f} a {base.max():.3f}")
    except FileNotFoundError:
        note(4, "ligne de base b = 0", False, "campagne absente")

    # -- 5. Les sondes sont COMMUNES a tous les runs d'une amplitude : leur erreur
    #       d'echantillonnage est un biais partage, que le bootstrap sur les graines
    #       ne capture pas. On le mesure en rejouant avec un second tirage.
    try:
        _, sondes2, _ = charger_etalon(tag_sondes2)
        e2 = etalon_par_run(sondes2).merge(
            pd.read_parquet(DATA / f"QCD_etalon_meta_{tag_sondes2}.parquet")
            [['run_id', 'delta_e_sondes', 'seed']], on='run_id')
        j = par_run.merge(e2, on=['delta_e_sondes', 'seed'], suffixes=('_1', '_2'))
        ecart = (j['etalon_aire_1'] - j['etalon_aire_2'])
        rel = float(np.abs(ecart).mean() / j['etalon_aire_1'].mean())
        # Le biais partage se lit sur la MOYENNE par amplitude, pas run par run.
        par_amp = j.groupby('delta_e_sondes')[['etalon_aire_1', 'etalon_aire_2']].mean()
        biais = (par_amp['etalon_aire_1'] - par_amp['etalon_aire_2']).abs()
        rel_amp = float((biais / par_amp['etalon_aire_1']).max())
        ok5 = bool(rel_amp < 0.10)
        note(5, "biais partage des sondes mesure et publie", ok5,
             f"ecart relatif par run {100 * rel:.1f} % | "
             f"biais partage par amplitude, au pire {100 * rel_amp:.1f} %")
    except FileNotFoundError:
        note(5, "second tirage de sondes", False, "campagne absente")

    val = pd.DataFrame(lignes)
    val.to_parquet(DATA / "QCD_etalon_validation.parquet", index=False)
    print("\n" + "-" * 78)
    if echecs:
        print(f"BLOQUANT — {len(echecs)} controle(s) en echec : {', '.join(echecs)}")
        print("L'etalon ne doit pas servir a juger les candidats en l'etat.")
    else:
        print("Les cinq controles passent. L'etalon peut servir de reference.")
    print("-" * 78)
    return len(echecs) == 0, par_run


# ============================================================================ #
#  Tache 6 — le banc complet, contre l'etalon : A2, B1, B2
# ============================================================================ #

from scipy.stats import kendalltau                                    # noqa: E402

LAMBDA_B2 = 25.0            # le seul seuil ou il y a quelque chose a separer


def charger_campagne_etalon(tag):
    """meta + evenements + traces d'une campagne INSTRUMENTEE."""
    meta = pd.read_parquet(DATA / f"QCD_etalon_meta_{tag}.parquet").sort_values('run_id')
    events = pd.read_parquet(DATA / f"QCD_etalon_events_swap_{tag}.parquet")
    traces = pd.read_parquet(DATA / f"QCD_etalon_traces_error_{tag}.parquet")
    mat = (traces.pivot(index='run_id', columns='t', values='e')
           .reindex(meta['run_id'].to_numpy()).to_numpy(dtype=float))
    return meta.reset_index(drop=True), events, mat


def dissensus_par_run(votes, w=W_ETALON, pas=25):
    """V(t) resume par son aire sur [0, W_e]. Construit HORS LIGNE, comme prevu.

    Reserve ecrite avant la mesure : si les arbres reagissent de facon tres
    synchrone — ce que C1 suggere a forte amplitude (rapport 0,83 contre 0,10
    attendu sous independance) — le dissensus reste plat et la metrique ne voit
    rien. Ce serait le regime ou N(W) fonctionne : candidats complementaires
    plutot que concurrents.
    """
    f = votes[(votes.t < w) & (votes.region == 'bande')]
    return (f.groupby('run_id')['V'].sum() * pas).rename('V_aire')


def tau_b_censure(x, y, horizon=H):
    """Kendall tau-b, valeurs censurees imputees au rang le moins reactif.

    ATTENTION AU SENS. `x` arrive DEJA ORIENTE : haut = plus reactif. Une valeur
    censuree est un quota jamais atteint, donc la reaction la plus LENTE : elle
    doit aller au rang MINIMAL de x oriente. Imputer en positif (`horizon * 10`)
    la placerait au rang le plus reactif, c'est-a-dire exactement a l'oppose de
    ce qu'elle signifie — bug corrige apres audit, il inversait le signe du tau-b
    de tau_erase sur quatre amplitudes.

    Kendall et non Spearman : le tau-b gere les ex-aequo, nombreux ici.
    """
    x = np.asarray(x, dtype=float).copy()
    y = np.asarray(y, dtype=float).copy()
    manquant = np.isnan(x)
    if manquant.all():
        return np.nan
    x[manquant] = np.nanmin(x) - 1.0
    ok = ~np.isnan(y)
    if ok.sum() < 5:
        return np.nan
    t, _ = kendalltau(x[ok], y[ok])
    return float(t)


def test_b1(cand_df, etalon_df, rng, n_boot=N_BOOT, exclure_degeneres=False):
    """B1 : le candidat suit-il l'etalon ? A amplitude fixee, IC excluant 0.

    Rapporte DEUX fois : imputation a l'horizon, et cas complets seuls, avec le
    taux de censure. Les candidats ne sont PAS classes par tau-b brut entre eux :
    la censure le tire vers 0 et les regimes de censure different.
    """
    j = cand_df.merge(etalon_df[['run_id', 'etalon_aire', 'min_acc_haut',
                                 'acc_haut_fin']], on='run_id')
    # Le § 8 fige : « un run dont la competence conservee chute de plus de 10 points
    # est SIGNALE, pas silencieusement compte ». Un run degenere a un etalon maximal
    # alors que la foret repond « toujours 0 » : le garder dans B1 revient a noter
    # l'effondrement comme une adaptation exemplaire. On rapporte donc les DEUX,
    # et la colonne `part_degeneres` dit ce que chaque cellule contient.
    degenere = j['acc_haut_fin'] < 1 - CHUTE_MAX
    if exclure_degeneres:
        j = j[~degenere]
    lignes = []
    for nom in CANDIDATS:
        if nom not in j.columns:
            continue
        for de, g in j.groupby('delta_e_sondes' if 'delta_e_sondes' in j else 'delta_e'):
            x, y = g[nom].to_numpy(dtype=float), g['etalon_aire'].to_numpy(dtype=float)
            if CANDIDATS[nom]['sens'] == -1:
                x = -x                      # oriente : haut = plus reactif, partout
            t_imp = tau_b_censure(x, y)
            complet = ~np.isnan(x)
            t_cc = (float(kendalltau(x[complet], y[complet])[0])
                    if complet.sum() >= 5 else np.nan)
            # Bootstrap APPARIE : on reechantillonne la GRAINE, pas la position de
            # ligne. Dans une strate d'amplitude une ligne vaut une graine, donc le
            # resultat coincide — mais l'appariement doit etre impose par le code,
            # pas herite d'une coincidence de mise en table.
            graines = g['seed'].to_numpy()
            pos = {gr: k for k, gr in enumerate(graines)}
            uniques = np.unique(graines)
            vals = []
            for _ in range(n_boot):
                tir = rng.choice(uniques, size=len(uniques), replace=True)
                idx = np.array([pos[gr] for gr in tir])
                v = tau_b_censure(x[idx], y[idx])
                if np.isfinite(v):
                    vals.append(v)
            lo, hi = ((float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5)))
                      if len(vals) > 20 else (np.nan, np.nan))
            lignes.append({
                'candidat': nom, 'test': 'B1' if not exclure_degeneres else 'B1_sains',
                'delta_e': float(de),
                'valeur': t_imp, 'ic_bas': lo, 'ic_haut': hi,
                'tau_b_cas_complets': t_cc,
                'censure': float(np.isnan(g[nom].to_numpy(dtype=float)).mean()),
                'part_degeneres': float((g['acc_haut_fin'] < 1 - CHUTE_MAX).mean()),
                'n_runs': int(len(g)), 'n_boot': int(n_boot),
                'passe': bool(np.isfinite(lo) and (lo > 0 or hi < 0)),
            })
    return pd.DataFrame(lignes)


def test_a2(cand_df, etalon_df, rng_a2):
    """A2 : le candidat indique-t-il une adaptation plus forte la ou la tache est
    seulement plus FACILE ?

    Operationnalise comme prevu : signe de la pente du candidat en Delta_e sur le
    haut de grille (>= 0,45), compare au signe de la pente de l'etalon. L'etalon
    y montre une competence conservee qui CHUTE ; un candidat dont la pente est
    positive la ou l'etalon se degrade confond facilitation et adaptation.
    """
    col = 'delta_e_sondes' if 'delta_e_sondes' in cand_df else 'delta_e'
    j = cand_df.merge(etalon_df[['run_id', 'etalon_aire', 'min_acc_haut',
                                 'acc_haut_fin']], on='run_id')
    haut = j[j[col] >= 0.45]
    milieu = j[(j[col] >= 0.25) & (j[col] <= 0.40)]
    if haut.empty or milieu.empty:
        return pd.DataFrame()
    pente_ref = np.polyfit(haut[col], haut['acc_haut_fin'], 1)[0]
    # L'ETALON LUI-MEME passe le test, en premier. S'il echoue, A2 ne separe pas les
    # metriques honnetes des contaminees : il separe seulement les grandeurs qui
    # montent en haut de grille de celles qui descendent, et sa portee doit etre
    # bornee en consequence. C'est une information necessaire a la lecture des
    # verdicts qui suivent, pas un detail d'implementation.
    pente_etalon = np.polyfit(haut[col], haut['etalon_aire'], 1)[0]
    lignes = [{'candidat': '(ETALON lui-meme)', 'test': 'A2', 'delta_e': np.nan,
               'valeur': float(pente_etalon), 'ic_bas': np.nan, 'ic_haut': np.nan,
               'pente_etalon': float(pente_ref), 'censure_haut': 0.0,
               'n_runs': int(len(haut)),
               'passe': not bool(pente_etalon > 0 and pente_ref < 0)}]
    for nom, spec in CANDIDATS.items():
        if nom not in j.columns:
            continue
        v_haut = haut[nom].to_numpy(dtype=float) * spec['sens']
        v_mil = milieu[nom].to_numpy(dtype=float) * spec['sens']
        if np.isnan(v_haut).all() or np.isnan(v_mil).all():
            continue
        fini = ~np.isnan(v_haut)
        pente = np.polyfit(haut[col][fini], v_haut[fini], 1)[0]
        plus_fort = np.nanmedian(v_haut) > np.nanmedian(v_mil)
        # IC de la pente, bootstrap APPARIE sur les graines : on reechantillonne la
        # graine une fois et toutes ses amplitudes suivent.
        graines = np.unique(haut['seed'].to_numpy())
        s_haut = haut['seed'].to_numpy()
        x_h = haut[col].to_numpy()
        pentes = []
        for _ in range(200):
            tir = rng_a2.choice(graines, size=len(graines), replace=True)
            m = np.concatenate([np.flatnonzero((s_haut == g) & fini) for g in tir])
            if len(m) > 3:
                pentes.append(np.polyfit(x_h[m], v_haut[m], 1)[0])
        lo, hi = ((float(np.percentile(pentes, 2.5)), float(np.percentile(pentes, 97.5)))
                  if len(pentes) > 20 else (np.nan, np.nan))
        # Echoue si le candidat monte alors que la competence conservee descend.
        echoue = bool(pente > 0 and pente_ref < 0 and plus_fort)
        lignes.append({'candidat': nom, 'test': 'A2', 'delta_e': np.nan,
                       'valeur': float(pente), 'ic_bas': lo, 'ic_haut': hi,
                       'pente_etalon': float(pente_ref),
                       'censure_haut': float(np.isnan(v_haut).mean()),
                       'n_runs': int(len(haut)),
                       'passe': not echoue})
    return pd.DataFrame(lignes)


def test_b2(cand_df, meta, error_mat, rng):
    """B2 : le candidat separe-t-il les runs ou l'alarme part de ceux ou elle ne
    part pas ? lambda = 25 seulement.

    SECONDAIRE ET NON DISQUALIFIANT : bien predire l'alarme recompense la
    contamination par la trajectoire d'erreur, motif exact pour lequel « retour de
    l'erreur » a ete ecarte comme circulaire.
    """
    p0 = meta['p_hat_0'].to_numpy(dtype=float)[:, None]
    ecart = error_mat - p0
    s = np.zeros(len(meta)); alarme = np.zeros(len(meta), dtype=bool)
    for t in range(error_mat.shape[1]):
        s = np.maximum(0.0, s + ecart[:, t] - DELTA_P)
        alarme |= (s >= LAMBDA_B2)
    col = 'delta_e_sondes' if 'delta_e_sondes' in cand_df else 'delta_e'
    d = cand_df.copy(); d['alarme'] = alarme
    lignes = []
    for nom, spec in CANDIDATS.items():
        if nom not in d.columns:
            continue
        for de, g in d.groupby(col):
            if g.alarme.nunique() < 2:
                continue
            auc, _ = auc_a1(g.loc[~g.alarme, nom].to_numpy(),
                            g.loc[g.alarme, nom].to_numpy(), spec['sens'])
            # L'alarme EST le franchissement de S_max par lambda : l'AUC de S_max_H
            # vaut 1,000 par identite, pas par performance. On l'ecrit dans la table
            # plutot que de publier dix-neuf 1,000 muets.
            tauto = (nom == 'S_max_H')
            lignes.append({'candidat': nom, 'test': 'B2', 'delta_e': float(de),
                           'valeur': auc, 'passe': None, 'tautologique': bool(tauto)})
    return pd.DataFrame(lignes)


def figure_series_internes(tag, etalon_df, nom_fichier="Fig_QD_series_internes.png"):
    """La figure de la question D : les series internes sur un axe temporel commun."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    meta, sondes, votes = charger_etalon(tag)
    _, events, mat = charger_campagne_etalon(tag)
    amplitudes = np.sort(meta.delta_e_sondes.unique())
    cible = amplitudes[len(amplitudes) // 3]
    runs = meta.loc[np.isclose(meta.delta_e_sondes, cible), 'run_id'].to_numpy()
    idx = {r: i for i, r in enumerate(meta.run_id.to_numpy())}

    fig, axes = plt.subplots(3, 1, figsize=(9, 8), sharex=True)
    e = mat[[idx[r] for r in runs]].mean(axis=0)
    L = 50
    axes[0].plot(np.arange(len(e) - L + 1), np.convolve(e, np.ones(L) / L, 'valid'),
                 color='black', lw=1.2)
    axes[0].set_ylabel(r"$\bar{e}_t$ (lisse, 50 pas)")
    axes[0].set_title(f"Series internes alignees, $\\Delta e$ = {cible:.3f} "
                      f"({len(runs)} executions)", fontsize=10)

    ev = events[events.run_id.isin(runs)]
    phi = np.zeros(H)
    for r, g in ev.groupby('run_id'):
        vus = np.zeros(H)
        prem = g.groupby('tree_id')['t'].min().to_numpy()
        for t in prem:
            vus[int(t):] += 1
        phi += vus
    axes[1].plot(np.arange(H), phi / (len(runs) * N_MODELS), color='black', lw=1.2)
    axes[1].set_ylabel(r"$\varphi(t)$, fraction remplacee")

    for region, style in (('bande', '-'), ('haut', '--'), ('bas', ':')):
        g = (sondes[(sondes.region == region) & (sondes.run_id.isin(runs))]
             .groupby('t')['acc'].mean())
        axes[2].plot(g.index, g.values, style, color='black', lw=1.2,
                     label=f"acc_{region}")
    axes[2].set_ylabel("etalon : acc par region")
    axes[2].set_xlabel("pas depuis la rupture")
    axes[2].legend(fontsize=8, loc='center right')
    for a in axes:
        a.grid(alpha=0.3)
    fig.savefig(FIGURES / nom_fichier, dpi=150, bbox_inches='tight')
    plt.close(fig)


def figure_taub(bench, nom_fichier="Fig_QC_tau_b_etalon.png"):
    """tau-b contre l'etalon, par amplitude, avec IC."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    b1 = bench[bench.test == 'B1']
    if b1.empty:
        return
    montres = [c for c in ('tau_arf', 'tau_swap_50', 'N_200', 'V_aire', 'S_max_H')
               if c in set(b1.candidat)]
    fig, ax = plt.subplots(figsize=(9, 5.5))
    for i, c in enumerate(montres):
        g = b1[b1.candidat == c].sort_values('delta_e')
        gris = str(0.05 + 0.6 * i / max(len(montres) - 1, 1))
        ax.plot(g.delta_e, g.valeur, '-o', ms=4, color=gris,
                label=CANDIDATS[c]['libelle'])
        ax.fill_between(g.delta_e, g.ic_bas, g.ic_haut, color=gris, alpha=0.15)
    ax.axhline(0, color='black', lw=1)
    ax.set_xlabel(r"amplitude du drift  $\Delta e$")
    ax.set_ylabel(r"Kendall $\tau_b$ avec l'etalon")
    ax.set_title("Test B1 : le candidat suit-il l'adaptation reelle ?\n"
                 "bandes = IC bootstrap 95 % apparie sur les graines", fontsize=10)
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    fig.savefig(FIGURES / nom_fichier, dpi=150, bbox_inches='tight')
    plt.close(fig)


def banc_etalon(tag='full_M10'):
    """Le banc complet, une fois l'etalon valide."""
    rng = np.random.default_rng(SEED_BOOT)
    print("=" * 78)
    print(f"BANC COMPLET CONTRE L'ETALON — campagne {tag}")
    print("=" * 78)
    meta, events, mat = charger_campagne_etalon(tag)
    _, sondes, votes = charger_etalon(tag)
    etalon = etalon_par_run(sondes)
    cand = candidats_par_run(meta, events, N_MODELS, mat)
    cand = cand.merge(dissensus_par_run(votes), on='run_id', how='left')
    CANDIDATS['V_aire'] = {'sens': +1, 'extensif': False,
                           'libelle': "V(t), dissensus entre arbres sur sondes"}
    print(f"[INFO] {len(cand)} runs | {cand.delta_e_sondes.nunique()} amplitudes")

    # A1 pour V(t) : la campagne b = 0 instrumentee n'existe qu'en PILOTE (5
    # amplitudes x 20 graines). Le test est donc fait sur ce perimetre reduit et la
    # restriction est ecrite dans la table, plutot que de laisser une case vide.
    a1_v = pd.DataFrame()
    try:
        m_p, e_p, mat_p = charger_campagne_etalon('pilote_M10')
        m_n, e_n, mat_n = charger_campagne_etalon('pilote_nodrift_M10')
        _, _, v_p = charger_etalon('pilote_M10')
        _, _, v_n = charger_etalon('pilote_nodrift_M10')
        d_p = (candidats_par_run(m_p, e_p, N_MODELS, mat_p)
               .merge(dissensus_par_run(v_p), on='run_id', how='left'))
        d_n = (candidats_par_run(m_n, e_n, N_MODELS, mat_n)
               .merge(dissensus_par_run(v_n), on='run_id', how='left'))
        d_p['delta_e'] = d_p['delta_e_sondes']
        garde = {k: v for k, v in CANDIDATS.items() if k == 'V_aire'}
        sauve = dict(CANDIDATS)
        CANDIDATS.clear(); CANDIDATS.update(garde)
        a1_v = test_a1(d_p, d_n, rng)
        a1_v['perimetre'] = 'pilote 5 amplitudes x 20 graines'
        CANDIDATS.clear(); CANDIDATS.update(sauve)
    except FileNotFoundError:
        pass
    # C1 pour V(t) est NON TESTABLE : il faudrait une campagne instrumentee par
    # taille de foret, et les tables `_C1_M*` existantes ne portent pas de sondes.
    # Le plan l'exclut explicitement du perimetre. On l'ecrit dans la table.
    c1_v = pd.DataFrame([{'candidat': 'V_aire', 'test': 'C1', 'delta_e': np.nan,
                          'valeur': np.nan, 'passe': None,
                          'non_testable': "aucune campagne instrumentee a M variable"}])

    bench = pd.concat([
        a1_v, c1_v,
        test_b1(cand, etalon, rng),
        test_b1(cand, etalon, rng, exclure_degeneres=True),
        test_a2(cand, etalon, rng),
        test_b2(cand, meta, mat, rng),
        tests_d(cand.rename(columns={'delta_e_sondes': 'delta_e_s'})
                .assign(delta_e=cand['delta_e_sondes'])),
    ], ignore_index=True)
    bench.to_parquet(DATA / "QCD_candidats_benchmark_etalon.parquet", index=False)
    cand.to_parquet(DATA / "QCD_candidats_indicateurs_etalon.parquet", index=False)
    etalon.to_parquet(DATA / "QCD_etalon_par_run.parquet", index=False)

    b1 = bench[bench.test == 'B1']
    print("\nTEST B1 — tau-b avec l'etalon (le SEUL test qui departage)")
    piv = b1.pivot_table(index='delta_e', columns='candidat', values='valeur')
    montres = [c for c in ('tau_arf', 'tau_swap_50', 'N_200', 'V_aire', 'S_max_H')
               if c in piv.columns]
    print(piv[montres].round(3).to_string())
    print("\n  nombre d'amplitudes ou l'IC exclut 0 :")
    for c in montres:
        g = b1[b1.candidat == c]
        print(f"    {CANDIDATS[c]['libelle']:<45} {int(g['passe'].sum())}/{len(g)}")

    a2 = bench[bench.test == 'A2']
    if not a2.empty:
        echecs = a2[~a2['passe'].astype(bool)]
        print(f"\nTEST A2 — {len(echecs)}/{len(a2)} candidats confondent facilitation "
              f"et adaptation")
        if len(echecs):
            print("    " + ", ".join(echecs.candidat.tolist()))
        ref = a2[a2.candidat == '(ETALON lui-meme)']
        if not ref.empty and not bool(ref['passe'].iloc[0]):
            print("\n  RESERVE — l'ETALON LUI-MEME echoue A2 : son aire croit en haut de")
            print("  grille alors que la competence conservee s'y effondre. A2 ne separe")
            print("  donc pas les metriques honnetes des contaminees ; il separe les")
            print("  grandeurs croissantes des decroissantes. Ses verdicts se lisent avec")
            print("  cette borne, et le haut de grille est un regime degenere pour TOUTES")
            print("  les mesures, etalon compris.")
    figure_series_internes(tag, etalon)
    figure_taub(bench)
    print(f"\n[SUCCESS] figures : Fig_QD_series_internes.png, Fig_QC_tau_b_etalon.png")
    return bench


def synthese_globale():
    """La table candidat x test exigee comme livrable minimal, meme si tout tombe.

    Fusionne le banc sans etalon (A1, C1, D*) et le banc contre l'etalon (A2, B1,
    B2). Une cellule « n/N » compte les amplitudes ou le critere est satisfait.

    RAPPEL, ecrit dans la table : « non disqualifie » ne se lit jamais « valide ».
    Seul B1 stratifie departage ; les sept autres tests ne font qu'eliminer.
    """
    parts = []
    for f in ("QCD_candidats_benchmark.parquet", "QCD_candidats_benchmark_etalon.parquet"):
        if (DATA / f).exists():
            parts.append(pd.read_parquet(DATA / f))
    if not parts:
        raise SystemExit("aucun banc a synthetiser : lancer d'abord bench_candidats.py")
    bench = pd.concat(parts, ignore_index=True)
    # Les deux bancs portent sur des campagnes identiques BIT A BIT (controle de
    # non-regression, tache 4) : leurs tests D1/D2/D3 font donc doublon et
    # doubleraient les denominateurs. On ne garde qu'une occurrence par cellule.
    bench = bench.drop_duplicates(subset=['candidat', 'test', 'delta_e'], keep='first')

    lignes = []
    for nom in bench.candidat.unique():
        sous = bench[bench.candidat == nom]
        spec = CANDIDATS.get(nom, {'libelle': nom, 'sens': +1})
        ligne = {'candidat': nom, 'libelle': spec['libelle']}
        for test in ('A1', 'A2', 'B1', 'C1', 'D2', 'D3'):
            t = sous[sous.test == test]
            passe = t['passe'].dropna() if 'passe' in t else pd.Series(dtype=float)
            if not len(passe):
                ligne[test] = "-"
                continue
            cellule = f"{int(passe.sum())}/{len(passe)}"
            # Le § 8 fige : « un IC qui chevauche la borne est declare INDECIS, pas
            # disqualifie ». Les compter comme des echecs fausserait le denominateur.
            if 'indecis' in t and t['indecis'].fillna(False).any():
                cellule += f" ({int(t['indecis'].fillna(False).sum())} ind.)"
            ligne[test] = cellule
        b1 = sous[sous.test == 'B1']
        if not b1.empty:
            med = float(b1['valeur'].median())
            ligne['B1_tau_b_median'] = med
            # Un tau-b significatif mais de signe OPPOSE a l'orientation declaree
            # n'est pas une reussite : c'est la refutation de cette orientation.
            ligne['B1_signe_inverse'] = bool(med < 0)
            ligne['B1_censure_median'] = float(b1['censure'].median())
        a1 = sous[sous.test == 'A1']
        if not a1.empty:
            ligne['A1_max'] = float(a1['valeur'].max())
            ligne['A1_anti_informatif'] = int((a1['valeur'] > 0.5).sum())
        lignes.append(ligne)
    syn = pd.DataFrame(lignes).sort_values('candidat')
    syn.to_parquet(DATA / "QCD_candidats_synthese.parquet", index=False)

    print("=" * 100)
    print("SYNTHESE candidat x test — livrable minimal du plan")
    print("cellule = amplitudes ou le critere est satisfait / amplitudes testees")
    print("« non disqualifie » ne se lit JAMAIS « valide » : seul B1 departage.")
    print("=" * 100)
    cols = ['candidat', 'A1', 'A2', 'B1', 'C1', 'D2', 'D3',
            'B1_tau_b_median', 'B1_signe_inverse', 'A1_anti_informatif']
    cols = [c for c in cols if c in syn.columns]
    print(syn[cols].to_string(index=False, float_format=lambda v: f"{v:+.3f}"))
    print("\nLecture :")
    print("  A1 se tait sans drift | A2 insensible a la facilitation | B1 suit l'etalon")
    print("  C1 independant de M   | D2 censure <= 5 %              | D3 granularite")
    print("  B1_signe_inverse : le lien est significatif mais de signe OPPOSE a")
    print("  l'orientation declaree a priori — c'est une refutation, pas une reussite.")
    return syn


def cli():
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--valider-etalon', action='store_true',
                    help="les cinq controles bloquants de l'etalon, sur le pilote")
    ap.add_argument('--banc-etalon', type=str, nargs='?', const='full_M10', default=None,
                    help="le banc complet A2/B1/B2 contre l'etalon (defaut : full_M10)")
    ap.add_argument('--synthese', action='store_true',
                    help="la table candidat x test, fusion des deux bancs")
    args = ap.parse_args()
    if args.valider_etalon:
        valider_etalon()
    elif args.banc_etalon:
        banc_etalon(args.banc_etalon)
    elif args.synthese:
        synthese_globale()
    else:
        main()


if __name__ == "__main__":
    cli()
