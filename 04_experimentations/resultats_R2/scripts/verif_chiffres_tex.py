"""
verif_chiffres_tex.py
===================================================================
Le controle de tracabilite exige par `.claude/rules/redaction.md` :
« toute valeur numerique du texte doit se retrouver dans une table de
`resultats/data/`, un log de campagne, ou une demonstration ecrite ».

Ce script le rend REPRODUCTIBLE. Il lit les redactions LaTeX passees en
argument, extrait chaque litteral numerique, et cherche chacun :
    1. dans la sortie des scripts de tracabilite (`chiffres_QC.py`,
       `chiffres_QD.py`), rejoues ici meme ;
    2. dans les colonnes numeriques des Parquet de `resultats/data/`,
       sous sept formats d'arrondi et en pourcentage.
Un nombre introuvable est imprime avec sa ligne : c'est une faute a
corriger, pas une approximation.

CE QUE LE SCRIPT NE FAIT PAS
    Il ne verifie pas qu'un nombre est cite AU BON ENDROIT : un chiffre
    exact rattache a la mauvaise amplitude ou a la mauvaise fenetre passe
    ce controle. C'est precisement le piege du 10 septembre (JOURNAL.md
    section 11.5), et il se rattrape a la relecture, pas ici.

LITTERAUX EXCLUS
    Les parametres du dispositif et les reperes de redaction, listes en
    clair dans EXCLUS ci-dessous : ils ne sont pas des mesures. Toute autre
    exclusion serait un moyen de faire passer un chiffre faux, donc la
    liste est fixe et commentee.

LECTURE SEULE. N'ecrit aucune table.

USAGE
    PYTHONHASHSEED=0 python verif_chiffres_tex.py                # les 5 revises
    PYTHONHASHSEED=0 python verif_chiffres_tex.py ../../redaction_QA_*.tex
"""

import re
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RACINE = Path(__file__).resolve().parents[1]
DATA = RACINE / "resultats" / "data"
TEX_DIR = RACINE.parent

# Les cinq redactions revisees le 10 septembre. QC1 et QC2 ne sont pas
# controlees ici : elles ne sont pas de nous (voir AUDIT_QC1_QC2_10SEPT.md).
DEFAUT = [
    "redaction_QC3_invariance.tex",
    "redaction_QD1_instrumentation_conjointe.tex",
    "redaction_QD2_coefficient_association.tex",
    "redaction_QD3_stratification_amplitude.tex",
    "redaction_QD4_protocole_decision.tex",
]

# Parametres du dispositif et reperes de redaction : ce ne sont pas des
# mesures, ils n'ont pas de table d'origine. Liste fixe et commentee.
EXCLUS = {
    # horizon, graines, taille de grille, taille de foret, fenetres de socle
    "2000", "1000", "3000", "100", "20", "18", "10", "120", "108",
    # seuils lambda et leurs sommes avec H*delta_P
    "8", "25", "50", "28", "45", "70",
    # parametres du detecteur et de tau_rec
    "0.01", "0.25", "0.10",
    # ajustement de l'article
    "18.5", "0.98", "0.02",
    # quantiles, niveaux de confiance, seuil de detectabilite
    "95", "2.5", "97.5", "0.05", "10000", "2000", "500", "0.13295637",
    # petits entiers de prose (nombre de raisons, de colonnes, de regles)
    "0", "1", "2", "3", "4", "5", "6", "7", "9", "12", "15", "14", "16",
    # bornes de graphe et repere de la mi-grille, cites comme reperes
    "0.19", "0.29",
    # precision machine du controle de scipy
    "2.2",
}

MOTIFS_A_RETIRER = (
    r"\\(?:usepackage|documentclass|geometry|hypersetup|includegraphics|"
    r"label|ref|eqref|cmidrule|multicolumn|parbox|hspace|vspace|textwidth)"
    r"(?:\[[^\]]*\])?(?:\{[^}]*\})*"
)


def sortie_des_scripts() -> str:
    """Rejoue les deux scripts de tracabilite et concatene leur sortie."""
    ici = Path(__file__).resolve().parent
    out = []
    for script in ("chiffres_QC.py", "chiffres_QD.py"):
        r = subprocess.run([sys.executable, str(ici / script)],
                           capture_output=True, text=True, cwd=ici)
        if r.returncode != 0:
            raise SystemExit(f"{script} a echoue :\n{r.stderr[-2000:]}")
        out.append(r.stdout)
    return "\n".join(out)


def valeurs_des_tables() -> set:
    """Toutes les valeurs numeriques des Parquet, sous sept arrondis."""
    vals = set()
    for f in sorted(DATA.glob("*.parquet")):
        # les traces brutes ne portent que des 0/1 et des indices
        if any(k in f.name for k in ("traces", "events", "votes", "sondes")):
            continue
        df = pd.read_parquet(f)
        for c in df.columns:
            col = df[c]
            if not np.issubdtype(col.dtype, np.number):
                continue
            for v in col.dropna().unique():
                v = abs(float(v))
                for fmt in ("{:.0f}", "{:.1f}", "{:.2f}", "{:.3f}",
                            "{:.4f}", "{:.5f}", "{:.6f}"):
                    vals.add(fmt.format(v))
                    vals.add(fmt.format(100 * v))
    return vals


def nombres_du_tex(chemin: Path):
    """Litteraux numeriques du texte, avec leur ligne, hors macros LaTeX."""
    trouves = {}
    for i, ligne in enumerate(chemin.read_text(encoding="utf-8").splitlines(), 1):
        nettoyee = re.sub(MOTIFS_A_RETIRER, " ", ligne).replace("\\,", "")
        for n in re.findall(r"(?<![A-Za-z_\\])\d+\.\d+|(?<![A-Za-z_\\.\d])\d{2,}(?![\d.])",
                            nettoyee):
            trouves.setdefault(n, i)
    return trouves


def main() -> None:
    cibles = sys.argv[1:] or DEFAUT
    print("Rejeu de chiffres_QC.py et chiffres_QD.py...")
    corpus = sortie_des_scripts()
    print(f"  {len(corpus.splitlines())} lignes de sortie")
    vals = valeurs_des_tables()
    print(f"  {len(vals)} valeurs distinctes dans les Parquet de resultats/data/\n")

    total, total_manquants = 0, 0
    for nom in cibles:
        chemin = Path(nom) if Path(nom).exists() else TEX_DIR / nom
        nums = nombres_du_tex(chemin)
        manquants = []
        for n, ligne in sorted(nums.items(), key=lambda kv: float(kv[0])):
            if n in EXCLUS:
                continue
            court = n.rstrip("0").rstrip(".") if "." in n else n
            if n in corpus or n in vals or court in corpus or court in vals:
                continue
            manquants.append((n, ligne))
        controles = len(nums) - sum(1 for n in nums if n in EXCLUS)
        total += controles
        total_manquants += len(manquants)
        etat = "OK" if not manquants else f"{len(manquants)} INTROUVABLE(S)"
        print(f"{chemin.name}: {len(nums)} litteraux distincts, "
              f"{controles} controles (le reste est dans EXCLUS) -> {etat}")
        for n, ligne in manquants:
            print(f"    l.{ligne} : {n}")

    print(f"\nTotal : {total} litteraux controles, {total_manquants} introuvable(s).")
    if total_manquants:
        raise SystemExit("un chiffre du texte ne sort d'aucune table ni d'aucun script")


if __name__ == "__main__":
    main()
