#!/usr/bin/env bash
# ==============================================================================
# Script: run_experiment_R5.sh
# Objective: Reproduce Table II (Real-World Evaluation on BAF & INSECTS).
# Outputs:   - Data:   results/R5_real_world_evaluation/data/*.parquet
#            - Table:  results/R5_real_world_evaluation/tables/table2_real_data_summary.tex
#            - Values: results/R5_real_world_evaluation/tables/table2_values.csv
# Execution: ./run_experiment_R5.sh
# Determinism: PYTHONHASHSEED is pinned for bit-wise reproducibility.
# ==============================================================================

set -e
set -o pipefail
export PYTHONHASHSEED=0

echo "[INFO] Initializing repository structure..."
EXP_NAME="R5_real_world_evaluation"
EXP_DIR="experiments/${EXP_NAME}"
mkdir -p results/${EXP_NAME}/data
mkdir -p results/${EXP_NAME}/tables
mkdir -p logs/${EXP_NAME}

LOG_FILE="logs/${EXP_NAME}/execution_$(date +%Y%m%d_%H%M%S).log"

{
    echo "======================================================================"
    echo " ICDM 2026 Artifact Evaluation: The Blind Spot Paradox"
    echo " Experiment R5: Real-World Evaluation (Table II)"
    echo "======================================================================"

    echo -e "\n[STEP 1/6] Pre-flight integrity checks..."
    python ${EXP_DIR}/exp_R5_preflight.py

    echo -e "\n[STEP 2/6] Smoke test (20k-row prefixes)..."
    python ${EXP_DIR}/exp_R5_smoke_test.py

    echo -e "\n[STEP 3/6] BAF evaluation (checkpointed; long-running, ~4.5h)..."
    python ${EXP_DIR}/exp_R5_compute_baf.py

    echo -e "\n[STEP 4/6] INSECTS evaluation (aggregate + per-episode)..."
    python ${EXP_DIR}/exp_R5_compute_insects.py

    echo -e "\n[STEP 5/6] Adaptive Delta_e estimation..."
    python ${EXP_DIR}/exp_R5_compute_delta_e.py

    echo -e "\n[STEP 6/6] Assembling Table II + flooding decomposition..."
    python ${EXP_DIR}/exp_R5_make_table2.py

    echo -e "\n[SUCCESS] Pipeline R5 completed. Outputs in results/${EXP_NAME}/tables/"
    echo "======================================================================"
} | tee "$LOG_FILE"