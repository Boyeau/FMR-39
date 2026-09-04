#!/usr/bin/env bash
# ==============================================================================
# Script: run_all.sh
# Objective: One-click reproduction of all experiments (R1 to R9) and tests.
# ==============================================================================
set -e
set -o pipefail

# [IEEE/ICDM FAIR Compliance] Enforcing global determinism for child processes
export PYTHONHASHSEED=0

echo "======================================================================"
echo " ICDM 2026 Artifact Evaluation: FULL REPRODUCTION PIPELINE"
echo "======================================================================"

# S1: Execute all experiments sequentially
for i in {1..9}; do
    script="./run_experiment_R${i}.sh"
    echo -e "\n>>> Executing ${script}..."
    $script
done

echo -e "\n======================================================================"
echo " [INFO] All experiments generated successfully. Launching validation..."
echo "======================================================================"

# S2 & S4: Trigger the test suite
./run_tests.sh

echo -e "\n======================================================================"
echo " [SUCCESS] 100% of the repository pipelines executed and validated."
echo "======================================================================"