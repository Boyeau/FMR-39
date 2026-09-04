#!/usr/bin/env bash
# ==============================================================================
# Script: run_experiment_R4.sh
# Objective: Reproduce Table I and KSWIN Sweep (Heteroscedastic ARMA-GARCH Streams).
# Outputs:   - Data: results/R4_proteus_evaluation/data/*.csv
#            - Table: results/R4_proteus_evaluation/tables/*.tex
# Execution: ./run_experiment_R4.sh
# Determinism: PYTHONHASHSEED is pinned for bit-wise reproducibility.
# ==============================================================================

set -e
set -o pipefail
export PYTHONHASHSEED=0

echo "[INFO] Initializing repository structure..."
EXP_NAME="R4_proteus_evaluation"
mkdir -p results/${EXP_NAME}/data
mkdir -p results/${EXP_NAME}/tables
mkdir -p logs/${EXP_NAME}

LOG_FILE="logs/${EXP_NAME}/execution_$(date +%Y%m%d_%H%M%S).log"

{
    echo "======================================================================"
    echo " ICDM 2026 Artifact Evaluation: The Blind Spot Paradox"
    echo " Experiment R4: ProteuS Heteroscedastic Evaluation (Table I & KSWIN)"
    echo "======================================================================"
    
    # Ensure dependencies are available
    if ! command -v python &> /dev/null; then
        echo "Error: Python is not available in the current path. Please activate your environment."
        exit 1
    fi
    
    echo -e "\n[STEP 1/2] Running Main Table Generation (PHT, EDDM, ADWIN, SRP, KSWIN)..."
    python experiments/${EXP_NAME}/exp_R4_main_table.py
    
    echo -e "\n[STEP 2/2] Running KSWIN Alpha Sweep..."
    python experiments/${EXP_NAME}/exp_R4_kswin_sweep.py
    
    echo -e "\n[SUCCESS] Pipeline R4 completed. Outputs in results/${EXP_NAME}/tables/"
    echo "======================================================================"
} | tee "$LOG_FILE"