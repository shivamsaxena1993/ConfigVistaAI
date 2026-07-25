"""
config/ml_config.py

ConfigVista AI
Machine Learning Configuration

Author: Shivam Saxena
Version: Phase 3
"""

from pathlib import Path

# ==============================================================================
# PROJECT PATHS
# ==============================================================================

# ConfigVistaAI/
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# ml/
ML_ROOT = PROJECT_ROOT / "ml"

# ==============================================================================
# DATA DIRECTORIES
# ==============================================================================

RAW_DATA_DIR = ML_ROOT / "data" / "raw"

SYNTHETIC_DATA_DIR = ML_ROOT / "data" / "synthetic"

PROCESSED_DATA_DIR = ML_ROOT / "data" / "processed"

# ==============================================================================
# DATASET FILES
# ==============================================================================

RAW_DATASET = RAW_DATA_DIR / "comparison_results.csv"

SYNTHETIC_DATASET = SYNTHETIC_DATA_DIR / "synthetic_changes.csv"

TRAIN_DATASET = PROCESSED_DATA_DIR / "training_dataset.csv"

VALIDATION_DATASET = PROCESSED_DATA_DIR / "validation_dataset.csv"

TEST_DATASET = PROCESSED_DATA_DIR / "test_dataset.csv"

# ==============================================================================
# TRAINED MODEL DIRECTORY
# ==============================================================================

MODEL_DIR = ML_ROOT / "trained_models"

RANDOM_FOREST_MODEL = MODEL_DIR / "random_forest.pkl"

XGBOOST_MODEL = MODEL_DIR / "xgboost.pkl"

LABEL_ENCODER = MODEL_DIR / "label_encoder.pkl"

# ==============================================================================
# EXPERIMENT DIRECTORY
# ==============================================================================

EXPERIMENT_DIR = ML_ROOT / "experiments"

# ==============================================================================
# RANDOMNESS
# ==============================================================================

RANDOM_STATE = 42

# ==============================================================================
# DATA SPLITS
# ==============================================================================

TRAIN_SIZE = 0.70

VALIDATION_SIZE = 0.15

TEST_SIZE = 0.15

# ==============================================================================
# RANDOM FOREST CONFIGURATION
# ==============================================================================

RF_CONFIG = {

    "n_estimators": 200,

    "max_depth": 15,

    "min_samples_split": 5,

    "min_samples_leaf": 2,

    "max_features": "sqrt",

    "bootstrap": True,

    "random_state": RANDOM_STATE,

    "class_weight": "balanced"

}

# ==============================================================================
# XGBOOST CONFIGURATION
# ==============================================================================

XGB_CONFIG = {

    "n_estimators": 300,

    "learning_rate": 0.05,

    "max_depth": 6,

    "subsample": 0.8,

    "colsample_bytree": 0.8,

    "objective": "multi:softprob",

    "eval_metric": "mlogloss",

    "random_state": RANDOM_STATE

}

# ==============================================================================
# FEATURE ENGINEERING
# ==============================================================================

FEATURE_COLUMNS = [

    "parent_type",

    "parent_section",

    "category",

    "change_type",

    "added_lines",

    "removed_lines",

    "modified_lines",

    "child_command_count",

    "total_changes",

    "configuration_complexity",

    "routing_change",

    "interface_change",

    "switching_change",

    "security_change",

    "management_change",

    "services_change",

    "system_change"

]

TARGET_COLUMN = "risk_label"

# ==============================================================================
# ENCODING
# ==============================================================================

LABEL_ENCODING = {

    "Low": 0,

    "Medium": 1,

    "High": 2

}

LABEL_DECODING = {

    0: "Low",

    1: "Medium",

    2: "High"

}

# ==============================================================================
# PREPROCESSING
# ==============================================================================

MISSING_VALUE_STRATEGY = "most_frequent"

ENABLE_SCALING = False

ENABLE_ONE_HOT_ENCODING = True

REMOVE_DUPLICATES = True

# ==============================================================================
# SYNTHETIC DATASET
# ==============================================================================

GENERATE_SYNTHETIC_DATA = True

SYNTHETIC_SAMPLE_SIZE = 1000

# ==============================================================================
# MODEL EVALUATION
# ==============================================================================

CROSS_VALIDATION_FOLDS = 5

SCORING_METRICS = [

    "accuracy",

    "precision_macro",

    "recall_macro",

    "f1_macro"

]

# ==============================================================================
# SHAP CONFIGURATION
# ==============================================================================

ENABLE_SHAP = True

SHAP_BACKGROUND_SAMPLES = 100

MAX_DISPLAY_FEATURES = 20

# ==============================================================================
# LOGGING
# ==============================================================================

LOG_LEVEL = "INFO"

LOG_FILE = PROJECT_ROOT / "logs" / "ml_pipeline.log"

# ==============================================================================
# REPORTING
# ==============================================================================

SAVE_CONFUSION_MATRIX = True

SAVE_FEATURE_IMPORTANCE = True

SAVE_SHAP_PLOTS = True

SAVE_CLASSIFICATION_REPORT = True

# ==============================================================================
# DIRECTORY INITIALIZATION
# ==============================================================================

DIRECTORIES = [

    RAW_DATA_DIR,

    SYNTHETIC_DATA_DIR,

    PROCESSED_DATA_DIR,

    MODEL_DIR,

    EXPERIMENT_DIR,

    LOG_FILE.parent

]


def initialize_directories():
    """
    Create required project directories if they do not exist.
    """

    for directory in DIRECTORIES:
        directory.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":

    initialize_directories()

    print("Machine Learning configuration initialized successfully.")