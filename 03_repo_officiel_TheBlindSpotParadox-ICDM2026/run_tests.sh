#!/usr/bin/env bash
# ==============================================================================
# Script: run_tests.sh
# Objective: Execute the pytest suite against generated artifacts and log output.
# ==============================================================================
set -e
set -o pipefail

# S3: Isolate test logs from experiment logs
mkdir -p logs/pytest
LOG_FILE="logs/pytest/pytest_$(date +%Y%m%d_%H%M%S).log"

echo "[INFO] Running full pytest validation suite. Logging to ${LOG_FILE}..."

export PYTHONHASHSEED=0
python -m pytest tests/ -v -s | tee "$LOG_FILE"

echo "[SUCCESS] Validation complete."