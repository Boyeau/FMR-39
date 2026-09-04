#!/usr/bin/env bash
# ==============================================================================
# Script: run_experiment_R2.sh
# Objective: Reproduce Figures 2A, 2B, 2C (Instrumented Asymptotic Complexity).
# Outputs:   - Data: results/R2_instrumented_blind_spot/data/*.parquet
#            - Figures: results/R2_instrumented_blind_spot/figures/*.png
# Execution: ./run_experiment_R2.sh
# Determinism: PYTHONHASHSEED is pinned for bit-wise reproducibility.
# ==============================================================================

set -e
set -o pipefail
export PYTHONHASHSEED=0

echo "[INFO] Initializing repository structure..."
EXP_NAME="R2_instrumented_blind_spot"
mkdir -p results/${EXP_NAME}/data
mkdir -p results/${EXP_NAME}/figures
mkdir -p logs/${EXP_NAME}

LOG_FILE="logs/${EXP_NAME}/execution_$(date +%Y%m%d_%H%M%S).log"

{
    echo "======================================================================"
    echo " ICDM 2026 Artifact Evaluation: The Blind Spot Paradox"
    echo " Experiment R2: Instrumented Asymptotic Complexity (Figures 2A, 2B, 2C)"
    echo "======================================================================"
    
    echo -e "\n[STEP 1/1] Running Instrumentation & Generating Plots..."
    python experiments/${EXP_NAME}/exp_R2_instrumented_blind_spot.py
    
    echo -e "\n[SUCCESS] Pipeline R2 completed. Outputs in results/${EXP_NAME}/"
    echo "======================================================================"
} | tee "$LOG_FILE"