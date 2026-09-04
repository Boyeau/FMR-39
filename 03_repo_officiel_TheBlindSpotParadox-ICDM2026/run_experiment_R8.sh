#!/usr/bin/env bash
# ==============================================================================
# Script: run_experiment_R8.sh
# Objective: Reproduce the lambda_op fine-grid sweep (Decoupling Principle).
# Outputs:   - Data: results/R8_lambda_op_sweep/data/*.csv
# Execution: ./run_experiment_R8.sh
# Determinism: PYTHONHASHSEED is pinned for bit-wise reproducibility.
# ==============================================================================

set -e
set -o pipefail
export PYTHONHASHSEED=0

echo "[INFO] Initializing repository structure..."
EXP_NAME="R8_lambda_op_sweep"
mkdir -p results/${EXP_NAME}/data
mkdir -p logs/${EXP_NAME}

LOG_FILE="logs/${EXP_NAME}/execution_$(date +%Y%m%d_%H%M%S).log"

{
    echo "======================================================================"
    echo " ICDM 2026 Artifact Evaluation: The Blind Spot Paradox"
    echo " Experiment R8: The Decoupling Principle (lambda_op sweep)"
    echo "======================================================================"
    
    echo -e "\n[STEP 1/1] Generating Data (Running tau_ARF on fine magnitude grid)..."
    python experiments/${EXP_NAME}/exp_R8_lambda_op_sweep.py
    
    echo -e "\n[SUCCESS] Pipeline R8 completed. Outputs in results/${EXP_NAME}/"
    echo "          To verify academic claims, run: python -m pytest tests/test_R8_lambda_op.py -v -s"
    echo "======================================================================"
} | tee "$LOG_FILE"