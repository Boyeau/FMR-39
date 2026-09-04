#!/usr/bin/env bash
# ==============================================================================
# Script: run_experiment_R1.sh
# Objective: Reproduce Figure 1 (Race Condition & Starvation) for ICDM 2026.
# Outputs:   - Data: results/R1_race_condition/data/R1_race_condition.parquet
#            - Figure: results/R1_race_condition/figures/Fig_R1_race_condition.png
# Execution: ./run_experiment_R1.sh
# Determinism: PYTHONHASHSEED is pinned for bit-wise reproducibility.
# ==============================================================================

set -e # Exit immediately if a command exits with a non-zero status
set -o pipefail

# [IEEE/ICDM FAIR Compliance] Pinned dictionary hashing for bit-wise reproducibility
export PYTHONHASHSEED=0

# 1. Structure Initialization
echo "[INFO] Initializing repository structure..."
EXP_NAME="R1_race_condition"
mkdir -p results/${EXP_NAME}/data
mkdir -p results/${EXP_NAME}/figures
mkdir -p logs/${EXP_NAME}

LOG_FILE="logs/${EXP_NAME}/execution_$(date +%Y%m%d_%H%M%S).log"

# 2. Execution Wrapper with Logging
{
    echo "======================================================================"
    echo " ICDM 2026 Artifact Evaluation: The Blind Spot Paradox"
    echo " Experiment R1: Race Condition (tau_ARF vs tau_det)"
    echo "======================================================================"
    
    echo -e "\n[STEP 1/2] Generating Data (Computing Adaptation vs Detection Times)..."
    echo "Warning: This step runs parallelized (n_jobs=-1) over 200 seeds."
    python experiments/${EXP_NAME}/exp_R1_generate_data.py
    
    echo -e "\n[STEP 2/2] Generating Figure 1..."
    python experiments/${EXP_NAME}/exp_R1_plot_figure.py
    
    echo -e "\n[SUCCESS] Pipeline R1 completed. Check results/${EXP_NAME}/figures/ for outputs."
    echo "======================================================================"
} | tee "$LOG_FILE"