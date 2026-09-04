#!/usr/bin/env bash
# ==============================================================================
# Script: run_experiment_R7.sh
# Objective: Reproduce the Clock-Mismatch Artefact (Regime 1).
# Outputs:   - Data: results/R7_clock_mismatch/data/*.parquet
#            - Table: results/R7_clock_mismatch/tables/*.tex and *.csv
# Execution: ./run_experiment_R7.sh
# Determinism: PYTHONHASHSEED is pinned for bit-wise reproducibility.
# ==============================================================================

set -e
set -o pipefail
export PYTHONHASHSEED=0

echo "[INFO] Initializing repository structure..."
EXP_NAME="R7_clock_mismatch"
mkdir -p results/${EXP_NAME}/data
mkdir -p results/${EXP_NAME}/tables
mkdir -p logs/${EXP_NAME}

LOG_FILE="logs/${EXP_NAME}/execution_$(date +%Y%m%d_%H%M%S).log"

{
    echo "======================================================================"
    echo " ICDM 2026 Artifact Evaluation: The Blind Spot Paradox"
    echo " Experiment R7: The Clock-Mismatch Artefact (Regime 1)"
    echo "======================================================================"
    
    echo -e "\n[STEP 1/2] Generating Data (Running clock mismatch instrumentation)..."
    python experiments/${EXP_NAME}/exp_R7_generate_data.py
    
    echo -e "\n[STEP 2/2] Computing Regime-1 miss-rate summary..."
    python experiments/${EXP_NAME}/exp_R7_compute_regime1.py
    
    echo -e "\n[SUCCESS] Pipeline R7 completed. Outputs in results/${EXP_NAME}/"
    echo "          To verify academic claims, run: python -m pytest tests/test_R7_regime1.py -v -s"
    echo "======================================================================"
} | tee "$LOG_FILE"