# exp_R5_config.py
"""Central configuration for the R5 real-world evaluation (Table II: BAF + INSECTS)
of "The Blind Spot Paradox" (ICDM 2026).

All paths are resolved dynamically from this file's location, so the repository is
fully portable (no hard-coded absolute path). River is pinned to 0.23.0 because the
internal ADWIN clock artifact studied in the paper is version-sensitive."""
from pathlib import Path

# --- Dynamic, portable paths (mandated FAIR layout) ---
ROOT_DIR    = Path(__file__).resolve().parent.parent.parent
DATA_DIR    = ROOT_DIR / "data"
RESULTS_DIR = ROOT_DIR / "results" / "R5_real_world_evaluation" / "data"
TABLES_DIR  = ROOT_DIR / "results" / "R5_real_world_evaluation" / "tables"
LOGS_DIR    = ROOT_DIR / "logs" / "R5_real_world_evaluation"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
TABLES_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

BAF_DIR         = DATA_DIR / "baf"
INSECTS_DIR     = DATA_DIR / "insects"
CHECKPOINTS_DIR = RESULTS_DIR / "checkpoints"
CHECKPOINTS_DIR.mkdir(parents=True, exist_ok=True)

# --- Reproducibility ---
SEED_MASTER       = 42
N_SEEDS           = 30
RIVER_VERSION_PIN = "0.23.0"

# --- Pipelines (G4: only the three columns shown in Table II) ---
PIPELINES          = ["pht_ht", "pht_arf_c1", "adwin_arf_c1"]
PIPELINES_FLOODING = ["pht_ht", "pht_arf_c1"]   # per-episode decomposition (Section IV-C)

# --- BAF (Jesus et al., 2022) ---
BAF_VARIANTS  = ["Base", "VariantI", "VariantII"]
BAF_DRIFTS    = [125000, 250000, 375000, 500000, 625000, 750000, 875000]
BAF_WARMUP    = 100_000
BAF_TAU_TOL   = 5_000
BAF_NONE_FILL = 0     # default label used when the classifier abstains

# --- INSECTS (Souza et al., 2020, Table 2) ---
INSECTS_VARIANTS = ["abrupt_balanced", "gradual_balanced",
                    "incremental_reoccurring_balanced"]
INSECTS_WARMUP_FRACTION = 0.10
INSECTS_WARMUP_CAP      = 100_000
INSECTS_TAU_FRACTION    = 0.05
INSECTS_TAU_CAP         = 5_000
INSECTS_NONE_FILL       = -1

# Canonical drift positions (Souza 2020, Table 2). The reoccurring stream stops at
# ~79,986 instances: positions 79932 (truncated post-window) and 106497
# (out-of-stream) are PHANTOM drifts that cap the recall of every pipeline at 2/4.
INSECTS_DRIFTS = {
    "abrupt_balanced":                  [14352, 19500, 33240, 38682, 39510],   # K=5
    "gradual_balanced":                 [14028],                                # K=1
    "incremental_reoccurring_balanced": [26568, 53364, 79932, 106497],          # K=4 raw
}
# G1-B (validated): apply the valid-window anti-phantom filter to the F1 ground
# truth, so reoccurring F1 is evaluated on K=2, consistent with Delta_e, the
# per-episode flooding analysis, and the manuscript caption.
REOCCURRING_F1_K2 = True

# Delta_e ground truth (already phantom-free: reoccurring = K=2 by construction).
INSECTS_DRIFTS_DELTA_E = {
    "abrupt_balanced":                  [14352, 19500, 33240, 38682, 39510],
    "gradual_balanced":                 [14028],
    "incremental_reoccurring_balanced": [26568, 53364],
}

# --- Adaptive Delta_e estimation ---
DELTA_E_WINDOW_CAP    = 5_000
DELTA_E_WINDOW_FACTOR = 3
DELTA_E_MIN_WINDOW    = 50
DELTA_E_N_BOOTSTRAP   = 1_000
DELTA_E_RNG           = 42

# --- Paired difference / seed-level sign test (INSECTS, make_table2) ---
PAIR_NUM, PAIR_DEN = "pht_ht", "pht_arf_c1"
F1_COL             = "F1_bp"     # bipartite Hopcroft-Karp F1 (matches Section IV-C)

# --- Flooding decomposition (genuine detection vs false-alarm flooding) ---
FLOODING_GENUINE_MARGIN = 0.10

# --- PageHinkley / ARF hyper-parameters ---
PHT_DELTA     = 0.005
PHT_TARGET_FA = 1
ARF_N_MODELS  = 10

# --- Parallelism ---
N_JOBS             = -1
BAF_CHUNK_SIZE     = 30     # checkpoint granularity for the long BAF run (G3)
INSECTS_CHUNK_SIZE = 50

# --- Output artifacts (parquet everywhere; Table II body as .tex) ---
OUT_BAF        = RESULTS_DIR / "baf_results.parquet"
OUT_INSECTS    = RESULTS_DIR / "insects_results.parquet"
OUT_EPISODE    = RESULTS_DIR / "insects_per_episode.parquet"
OUT_DELTA_E    = RESULTS_DIR / "delta_e.parquet"
OUT_FLOODING   = RESULTS_DIR / "flooding_decomposition.parquet"
OUT_TABLE2_TEX = TABLES_DIR / "table2_real_data_summary.tex"
OUT_TABLE2_CSV = TABLES_DIR / "table2_values.csv"