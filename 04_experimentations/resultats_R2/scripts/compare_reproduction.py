"""
compare_reproduction.py
===================================================================
Verifie qu'une campagne relancee redonne les tables versionnees A L'IDENTIQUE.

Appele par `reproduire.sh --complet`, apres que les campagnes ont ete relancees
sous des tags a part (`repro`, `repro2000`), pour ne rien ecraser. Compare,
table par table, le contenu (colonnes communes, lignes triees par cle). Toute
difference, meme d'un pas ou d'un evenement, fait echouer le script.

LECTURE SEULE sur les tables versionnees. Avec --nettoyer, supprime ensuite
les fichiers produits sous les tags de reproduction (tables et figures), et
seulement si tout concorde.

USAGE
    PYTHONHASHSEED=0 python compare_reproduction.py            # comparer
    PYTHONHASHSEED=0 python compare_reproduction.py --nettoyer # comparer puis nettoyer
"""

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RACINE = Path(__file__).resolve().parents[1]
DATA = RACINE / "resultats" / "data"
FIGURES = RACINE / "resultats" / "figures"

# (table versionnee, table reproduite, cles de tri)
PAIRES = [
    # campagne avec drift, 20 x 100
    ("QCD_runs_meta_full", "QCD_runs_meta_repro_M10", ["run_id"]),
    ("QCD_traces_error_full", "QCD_traces_error_repro_M10", ["run_id", "t"]),
    ("QCD_events_swap_full", "QCD_events_swap_repro_M10", ["run_id", "t", "tree_id"]),
    # bras sans drift, 2 000 runs
    ("QCD_runs_meta_QE2000_nodrift_M10", "QCD_runs_meta_repro2000_nodrift_M10", ["run_id"]),
    ("QCD_traces_error_QE2000_nodrift_M10", "QCD_traces_error_repro2000_nodrift_M10", ["run_id", "t"]),
    ("QCD_events_swap_QE2000_nodrift_M10", "QCD_events_swap_repro2000_nodrift_M10", ["run_id", "t", "tree_id"]),
    # sondes analytiques
    ("QCD_etalon_sondes_full_M10", "QCD_etalon_sondes_repro_M10", ["run_id", "t", "region"]),
    ("QCD_etalon_traces_error_full_M10", "QCD_etalon_traces_error_repro_M10", ["run_id", "t"]),
    # tables d'analyse derivees
    ("QCD_indicateurs_full", "QCD_indicateurs_repro_M10", ["run_id"]),
    ("QCD_correlations_stratifiees_full", "QCD_correlations_stratifiees_repro_M10", ["delta_e", "comparateur"]),
]

# colonnes qui decrivent l'execution et non le resultat
IGNOREES = ("duree", "elapsed", "time_s", "date", "tag")


def comparer(ref, new, cles):
    a = pd.read_parquet(DATA / f"{ref}.parquet")
    b = pd.read_parquet(DATA / f"{new}.parquet")
    communes = [c for c in a.columns if c in b.columns and not any(i in c.lower() for i in IGNOREES)]
    manquantes = sorted(set(a.columns) - set(b.columns))
    a = a[communes].sort_values(cles).reset_index(drop=True)
    b = b[communes].sort_values(cles).reset_index(drop=True)
    if len(a) != len(b):
        return False, f"{len(a)} lignes contre {len(b)}"
    for c in communes:
        x, y = a[c].to_numpy(), b[c].to_numpy()
        if np.issubdtype(x.dtype, np.number) and np.issubdtype(y.dtype, np.number):
            egal = np.allclose(x.astype(float), y.astype(float), rtol=0, atol=1e-9, equal_nan=True)
        else:
            egal = bool((pd.Series(x).astype(str).values == pd.Series(y).astype(str).values).all())
        if not egal:
            return False, f"colonne {c} differente"
    note = f" (colonnes absentes de la reproduction : {manquantes})" if manquantes else ""
    return True, f"{len(a)} lignes, {len(communes)} colonnes identiques{note}"


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--nettoyer", action="store_true")
    args = p.parse_args()

    tout_ok = True
    for ref, new, cles in PAIRES:
        if not (DATA / f"{new}.parquet").exists():
            print(f"  ABSENT  {new} (campagne non relancee)")
            tout_ok = False
            continue
        ok, detail = comparer(ref, new, cles)
        tout_ok &= ok
        print(f"  {'OK    ' if ok else 'ECART '}  {ref}  <->  {new} : {detail}")

    if not tout_ok:
        print("\nLA REPRODUCTION NE REDONNE PAS LES TABLES VERSIONNEES. Fichiers conserves pour examen.")
        sys.exit(1)
    print("\nReproduction identique aux tables versionnees.")
    if args.nettoyer:
        produits = list(DATA.glob("*repro*")) + list(FIGURES.glob("*repro*"))
        for f in produits:
            f.unlink()
        print(f"{len(produits)} fichiers de reproduction supprimes.")


if __name__ == "__main__":
    main()
