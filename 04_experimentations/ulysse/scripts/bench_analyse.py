"""Analyse des tests A1 (drift nul) et C1 (sensibilite a M)."""
import numpy as np, pandas as pd, glob, os
D = "/Users/ulyssepetit/Documents/Perso/ProjetsCode/FMR-39/repo/04_experimentations/ulysse/resultats/data/"

def tau_arf(tag):
    """Premier remplacement par execution, NaN si aucun."""
    meta = pd.read_parquet(f"{D}QCD_runs_meta_{tag}.parquet").sort_values('run_id')
    ev = pd.read_parquet(f"{D}QCD_events_swap_{tag}.parquet")
    first = ev.groupby('run_id')['t'].min()
    distincts = ev.groupby('run_id')['tree_id'].nunique()
    meta['tau_arf'] = meta['run_id'].map(first)
    meta['renouveles'] = meta['run_id'].map(distincts).fillna(0)
    return meta

print("=" * 76)
print("TEST A1 — LA METRIQUE SE TAIT-ELLE QUAND IL N'Y A RIEN A DETECTER ?")
print("=" * 76)
a1 = tau_arf("A1_nodrift")
full = pd.read_parquet(f"{D}QCD_indicateurs_full.parquet")
M = 10
print(f"Sans aucun drift, {len(a1)} executions :")
q = a1.tau_arf.quantile([.25, .5, .75])
print("  tau_ARF        : mediane %.0f  (quartiles %.0f - %.0f)  | censure %.0f%%"
      % (q[.5], q[.25], q[.75], 100 * a1.tau_arf.isna().mean()))
print("  arbres renouveles sur %d : mediane %.1f  (min %.0f, max %.0f)"
      % (M, a1.renouveles.median(), a1.renouveles.min(), a1.renouveles.max()))
print("  forets entierement renouvelees : %.0f%%" % (100 * (a1.renouveles == M).mean()))
print()
print("Avec drift, par amplitude (mediane de tau_ARF) :")
med = full.groupby('delta_e').tau_arf.median()
print("  amplitude la plus faible (%.3f) : %.0f" % (med.index[0], med.iloc[0]))
print("  amplitude la plus forte  (%.3f) : %.0f" % (med.index[-1], med.iloc[-1]))
print()
sd = a1.tau_arf.dropna().to_numpy()
print("Recouvrement des distributions :")
for de in (med.index[0], med.index[len(med)//2], med.index[-1]):
    ad = full.loc[full.delta_e == de, 'tau_arf'].dropna().to_numpy()
    # proportion de paires ou le sans-drift est PLUS RAPIDE que le avec-drift
    p = np.mean(sd[:, None] < ad[None, :])
    print("  vs delta_e=%.3f : dans %.0f%% des paires, la foret SANS drift reagit plus vite" % (de, 100 * p))

print()
print("=" * 76)
print("TEST C1 — LA METRIQUE DEPEND-ELLE DE LA TAILLE DE LA FORET ?")
print("=" * 76)
tags = sorted([os.path.basename(f).replace('QCD_runs_meta_C1_M', '').replace('.parquet', '')
               for f in glob.glob(f"{D}QCD_runs_meta_C1_M*.parquet")], key=int)
if not tags:
    print("  (pas encore de donnees C1)")
else:
    rows = []
    for m in tags:
        d = tau_arf(f"C1_M{m}")
        for de, g in d.groupby('delta_e'):
            rows.append({'M': int(m), 'delta_e': de, 'tau_arf': g.tau_arf.median(),
                         'renouveles': g.renouveles.median()})
    t = pd.DataFrame(rows)
    piv = t.pivot(index='delta_e', columns='M', values='tau_arf')
    print("Mediane de tau_ARF, par amplitude et par taille de foret :\n")
    print(piv.to_string(float_format=lambda v: "%7.1f" % v))
    print()
    ref = piv[int(tags[0])]
    print("Rapport a M=%s (si tau_ARF ne dependait pas de M, tout vaudrait 1) :\n" % tags[0])
    print(piv.div(ref, axis=0).to_string(float_format=lambda v: "%7.2f" % v))
    print()
    print("Moyenne des rapports sur les amplitudes :")
    for m in tags:
        print("  M=%-3s : %.2f" % (m, (piv[int(m)] / ref).mean()))
    print()
    print("Prediction : tau_ARF est le minimum de M delais. Si ces delais etaient")
    print("independants et de loi exponentielle, l'esperance du minimum decroitrait")
    print("en 1/M, soit un rapport de %.2f entre M=%s et M=%s."
          % (int(tags[0]) / int(tags[-1]), tags[0], tags[-1]))
