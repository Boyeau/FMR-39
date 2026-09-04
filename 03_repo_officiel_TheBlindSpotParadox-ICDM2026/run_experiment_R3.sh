#!/usr/bin/env bash
# ==============================================================================
# Script: run_experiment_R3.sh
# Objective: Reproduce Figure 3 (Regime Crossover & Non-Adaptive RF Solution).
# Outputs:   - Data: results/R3_regime_crossover/data/R3_regime_crossover_metrics.parquet
#            - Figure: results/R3_regime_crossover/figures/Fig_R3_Regime_Crossover.png
# Execution: ./run_experiment_R3.sh
# Determinism: PYTHONHASHSEED is pinned for bit-wise reproducibility.
# ==============================================================================

set -e
set -o pipefail
export PYTHONHASHSEED=0

echo "[INFO] Initializing repository structure for Experiment R3..."
EXP_NAME="R3_regime_crossover"
mkdir -p results/${EXP_NAME}/data
mkdir -p results/${EXP_NAME}/figures
mkdir -p logs/${EXP_NAME}

LOG_FILE="logs/${EXP_NAME}/execution_$(date +%Y%m%d_%H%M%S).log"

{
    echo "======================================================================"
    echo " ICDM 2026 Artifact Evaluation: The Blind Spot Paradox"
    echo " Experiment R3: Regime Crossover & Non-Adaptive RF (Figure 3)"
    echo "======================================================================"
    
    # Execution Step
    echo -e "\n[STEP 1/1] Running the Bernoulli crossover simulation and rendering Figure 3..."
    python experiments/${EXP_NAME}/exp_R3_regime_crossover.py
    
    echo -e "\n[SUCCESS] Pipeline R3 completed."
    echo "          -> Metrics saved in results/${EXP_NAME}/data/"
    echo "          -> Figure saved in results/${EXP_NAME}/figures/"
    echo "======================================================================"
} | tee "$LOG_FILE"