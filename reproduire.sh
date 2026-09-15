#!/usr/bin/env bash
# =====================================================================
# reproduire.sh — le sujet 39 en une seule commande.
#
#   ./reproduire.sh             Rejoue toute l'analyse depuis les tables
#                               versionnees : controle chaque chiffre du rapport,
#                               des redactions et de la soutenance, regenere les
#                               figures nouvelles, recompile rapport et soutenance.
#                               Quelques minutes.
#
#   ./reproduire.sh --complet   Relance d'abord les simulations (campagne 20 x 100,
#                               bras sans drift de 2 000 runs, sondes analytiques)
#                               sous des tags a part, verifie qu'elles redonnent
#                               les tables versionnees a l'identique, puis fait
#                               tout ce qui precede. Environ 1 h sur 10 coeurs.
#
# Environnement : Python 3.12 avec river 0.23.0 (voir README.md). Par defaut le
# venv du depot officiel ; sinon PYTHON=/chemin/vers/python ./reproduire.sh
# LaTeX : pdflatex et lualatex.
# =====================================================================
set -euo pipefail

ICI="$(cd "$(dirname "$0")" && pwd)"
SCRIPTS="$ICI/04_experimentations/resultats_R2/scripts"
PY="${PYTHON:-$ICI/03_repo_officiel_TheBlindSpotParadox-ICDM2026/blindspot_env/bin/python}"
[ -x "$PY" ] || PY="$(command -v python3)"
export PYTHONHASHSEED=0

COMPLET=0
[ "${1:-}" = "--complet" ] && COMPLET=1

etape() { printf '\n=== %s ===\n' "$1"; }

etape "Environnement"
"$PY" - <<'EOF'
import importlib.util, sys
requis = ["numpy", "pandas", "scipy", "matplotlib", "pyarrow"]
manque = [m for m in requis if importlib.util.find_spec(m) is None]
if manque:
    sys.exit(f"paquets manquants : {manque}")
print("python", sys.version.split()[0], "| paquets d'analyse presents")
EOF
command -v pdflatex >/dev/null && command -v lualatex >/dev/null || { echo "pdflatex et lualatex requis"; exit 1; }

cd "$SCRIPTS"

if [ "$COMPLET" = 1 ]; then
  etape "Simulations (tags de reproduction, rien n'est ecrase)"
  "$PY" -c "import river, sys; sys.exit(0 if river.__version__ == '0.23.0' else 'river 0.23.0 requis')"
  "$PY" exp_QCD_campagne.py --full --tag repro
  "$PY" exp_QCD_campagne.py --full --no-drift --seeds 2000 --tag repro2000
  "$PY" exp_QCD_etalon.py --full --tag repro
  "$PY" analyse_QCD.py --tag repro_M10 --boot 2000

  etape "Comparaison aux tables versionnees"
  "$PY" compare_reproduction.py --nettoyer
fi

etape "Controle de la reconstruction du detecteur"
"$PY" analyse_QCD.py --self-check

etape "Figures ajoutees le 15/09 (matrice des indicateurs, preuve avant reparation)"
"$PY" matrice_correlations.py
"$PY" figures_soutenance.py

etape "Chaque chiffre des textes contre les scripts et les tables"
"$PY" verif_chiffres_tex.py \
  ../../rapport_final.tex \
  ../../redaction_QB_biais_independance.tex \
  ../../redaction_QD1_instrumentation_conjointe.tex \
  ../../redaction_QD2_coefficient_association.tex \
  ../../redaction_QD3_stratification_amplitude.tex \
  ../../redaction_QE_choix_du_seuil.tex \
  ../../../05_presentation/soutenance_20min.tex

etape "Compilation du rapport"
cd "$ICI/04_experimentations"
for i in 1 2 3; do pdflatex -interaction=nonstopmode -halt-on-error rapport_final.tex >/dev/null; done
echo "rapport_final.pdf : $(pdfinfo rapport_final.pdf 2>/dev/null | awk '/Pages/ {print $2}') pages"

etape "Compilation de la soutenance"
cd "$ICI/05_presentation"
for i in 1 2; do lualatex -interaction=nonstopmode -halt-on-error soutenance_20min.tex >/dev/null; done
echo "soutenance_20min.pdf : $(pdfinfo soutenance_20min.pdf 2>/dev/null | awk '/Pages/ {print $2}') pages"

if [ "$COMPLET" = 1 ]; then
  etape "Termine : simulations identiques aux tables, analyse rejouee sans ecart"
else
  etape "Termine : analyse rejouee sans ecart (simulations : ./reproduire.sh --complet)"
fi
