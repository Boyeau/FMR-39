#!/usr/bin/env bash
# ==============================================================================
# Script: run_experiment_R6.sh
# Objective: Reproduce the Hydra Effect acceleration factors (tau_HAT vs tau_ARF).
# Outputs:   - Data: results/R6_hydra_factor/data/*.parquet
#            - Table: results/R6_hydra_factor/tables/exp_R6_hydra_empirical_validation.tex
# Execution: ./run_experiment_R6.sh
# Determinism: PYTHONHASHSEED is pinned for bit-wise reproducibility.
# Dependency: run_experiment_R2.sh MUST be executed first to generate ARF data.
# ==============================================================================

set -e
set -o pipefail
export PYTHONHASHSEED=0

echo "[INFO] Initializing repository structure..."
EXP_NAME="R6_hydra_factor"
mkdir -p results/${EXP_NAME}/data
mkdir -p results/${EXP_NAME}/tables
mkdir -p logs/${EXP_NAME}

LOG_FILE="logs/${EXP_NAME}/execution_$(date +%Y%m%d_%H%M%S).log"

{
    echo "======================================================================"
    echo " ICDM 2026 Artifact Evaluation: The Blind Spot Paradox"
    echo " Experiment R6: Single-Tree HAT Instrumentation & Hydra Effect"
    echo "======================================================================"
    
    echo -e "\n[STEP 1/2] Generating Data (Running HAT M=1 instrumentation)..."
    python experiments/${EXP_NAME}/exp_R6_generate_data.py
    
    echo -e "\n[STEP 2/2] Computing Hydra Factor and extracting empirical parameters..."
    python experiments/${EXP_NAME}/exp_R6_compute_hydra.py
    
    echo -e "\n[SUCCESS] Pipeline R6 completed. Outputs in results/${EXP_NAME}/"
    echo "          To verify academic claims, run: python -m pytest tests/test_R6_hydra.py -v -s"
    echo "======================================================================"
} | tee "$LOG_FILE"