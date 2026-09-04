#!/usr/bin/env bash
# ==============================================================================
# Script: run_experiment_R9.sh
# Objective: Reproduce the Critical Ensemble Size (M_crit) empirical comparison.
# Outputs:   - Data: results/R9_mcrit/data/*.csv
#            - Figure: results/R9_mcrit/figures/*.png
# Execution: ./run_experiment_R9.sh
# Determinism: PYTHONHASHSEED is pinned for bit-wise reproducibility.
# ==============================================================================

set -e
set -o pipefail
export PYTHONHASHSEED=0

echo "[INFO] Initializing repository structure..."
EXP_NAME="R9_mcrit"
mkdir -p results/${EXP_NAME}/data
mkdir -p results/${EXP_NAME}/figures
mkdir -p logs/${EXP_NAME}

LOG_FILE="logs/${EXP_NAME}/execution_$(date +%Y%m%d_%H%M%S).log"

{
    echo "======================================================================"
    echo " ICDM 2026 Artifact Evaluation: The Blind Spot Paradox"
    echo " Experiment R9: The Critical Ensemble Size (M_crit)"
    echo "======================================================================"
    
    echo -e "\n[STEP 1/2] Generating Data (Running single-tree HAT instrumentation)..."
    python experiments/${EXP_NAME}/exp_R9_generate_data.py
    
    echo -e "\n[STEP 2/2] Computing M_crit empirical distribution and plotting..."
    python experiments/${EXP_NAME}/exp_R9_compute_mcrit.py
    
    echo -e "\n[SUCCESS] Pipeline R9 completed. Outputs in results/${EXP_NAME}/"
    echo "          To verify academic claims, run: python -m pytest tests/test_R9_mcrit.py -v -s"
    echo "======================================================================"
} | tee "$LOG_FILE"