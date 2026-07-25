"""
==============================================================================
File: utils/constants.py

Project : ConfigVista AI
Phase   : Phase 3 - Machine Learning Pipeline

Purpose
-------
Central location for application constants used across the complete
machine learning pipeline.

Used by

    dataset_generator.py
    feature_extractor.py
    preprocessing.py
    validate_dataset.py
    synthetic_generator.py
    train_random_forest.py
    train_xgboost.py
    predict.py
    Streamlit Dashboard

============================================================================== 
"""

from enum import Enum
from pathlib import Path

# ==============================================================================
# APPLICATION
# ==============================================================================

APP_NAME = "ConfigVista AI"

APP_VERSION = "3.0"

AUTHOR = "Shivam Saxena"

ML_PIPELINE_VERSION = "1.0"

DATASET_VERSION = "1.0"

MODEL_VERSION = "1.0"

# ==============================================================================
# RANDOMNESS
# ==============================================================================

RANDOM_STATE = 42

# ==============================================================================
# PROJECT PATHS
# ==============================================================================

PROJECT_ROOT = Path(".")

ML_DIRECTORY = PROJECT_ROOT / "ml"

DATA_DIRECTORY = ML_DIRECTORY / "data"

RAW_DIRECTORY = DATA_DIRECTORY / "raw"

PROCESSED_DIRECTORY = DATA_DIRECTORY / "processed"

SYNTHETIC_DIRECTORY = DATA_DIRECTORY / "synthetic"

MODEL_DIRECTORY = ML_DIRECTORY / "models"

REPORT_DIRECTORY = ML_DIRECTORY / "reports"

# ==============================================================================
# DATASET FILES
# ==============================================================================

RAW_DATASET = RAW_DIRECTORY / "comparison_results.csv"

MASTER_DATASET = PROCESSED_DIRECTORY / "master_dataset.csv"

TRAIN_DATASET = PROCESSED_DIRECTORY / "training_dataset.csv"

VALIDATION_DATASET = PROCESSED_DIRECTORY / "validation_dataset.csv"

TEST_DATASET = PROCESSED_DIRECTORY / "test_dataset.csv"

SYNTHETIC_DATASET = SYNTHETIC_DIRECTORY / "synthetic_changes.csv"

# ==============================================================================
# DATASET SPLITS
# ==============================================================================

TRAIN_SIZE = 0.70

VALIDATION_SIZE = 0.15

TEST_SIZE = 0.15

# ==============================================================================
# VALIDATION RULES
# ==============================================================================

MIN_ROWS_FOR_TRAINING = 500

MAX_NULL_PERCENTAGE = 10

MAX_DUPLICATE_PERCENTAGE = 5

# ==============================================================================
# RISK LABELS
# ==============================================================================


class RiskLabel(str, Enum):

    LOW = "Low"

    MEDIUM = "Medium"

    HIGH = "High"


RISK_LABELS = [
    RiskLabel.LOW.value,
    RiskLabel.MEDIUM.value,
    RiskLabel.HIGH.value,
]

RISK_ENCODING = {
    "Low": 0,
    "Medium": 1,
    "High": 2,
}

RISK_DECODING = {
    0: "Low",
    1: "Medium",
    2: "High",
}

TARGET_COLUMN = "risk_label"

# ==============================================================================
# CHANGE TYPES
# ==============================================================================


class ChangeType(str, Enum):

    ADDED = "Added"

    REMOVED = "Removed"

    MODIFIED = "Modified"


CHANGE_TYPES = [
    ChangeType.ADDED.value,
    ChangeType.REMOVED.value,
    ChangeType.MODIFIED.value,
]

CHANGE_TYPE_ENCODING = {
    "Added": 0,
    "Removed": 1,
    "Modified": 2,
}

# ==============================================================================
# NETWORK CATEGORIES
# ==============================================================================

NETWORK_CATEGORIES = [
    "Interface",
    "Routing",
    "Switching",
    "Security",
    "Management",
    "Services",
    "System",
    "Unknown",
]

# ==============================================================================
# RAW DATASET COLUMNS
# ==============================================================================

RAW_COLUMNS = [

    "comparison_id",
    "timestamp",
    "baseline_hostname",
    "candidate_hostname",
    "category",
    "section",
    "change_type",
    "line_number",
    "old_value",
    "new_value",
    "risk_label",
    "risk_weight",
    "confidence_score",
    "description",
    "recommendation",
]

# ==============================================================================
# ENGINEERED FEATURE COLUMNS
# ==============================================================================

FEATURE_COLUMNS = [

    "parent_type",

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

    "system_change",

    "contains_ip",

    "contains_shutdown",

    "contains_neighbor",

    "contains_network",

    "contains_route",

    "contains_vlan",

    "contains_acl",
]

# ==============================================================================
# FEATURE GROUPS
# ==============================================================================

CATEGORICAL_COLUMNS = [
    "category",
    "change_type",
    "parent_type",
]

NUMERICAL_COLUMNS = [
    "risk_weight",
    "confidence_score",
    "line_number",
    "total_changes",
    "configuration_complexity",
]

BOOLEAN_COLUMNS = [
    "routing_change",
    "interface_change",
    "switching_change",
    "security_change",
    "management_change",
    "services_change",
    "system_change",
]

# ==============================================================================
# KEYWORDS USED FOR FEATURE EXTRACTION
# ==============================================================================

ROUTING_KEYWORDS = [
    "router",
    "ospf",
    "bgp",
    "eigrp",
    "rip",
    "network",
    "neighbor",
    "ip route",
]

INTERFACE_KEYWORDS = [
    "interface",
    "shutdown",
    "ip address",
    "description",
]

SWITCHING_KEYWORDS = [
    "vlan",
    "switchport",
    "spanning-tree",
]

SECURITY_KEYWORDS = [
    "access-list",
    "snmp",
    "aaa",
    "line vty",
]

SERVICES_KEYWORDS = [
    "ntp",
    "logging",
    "service",
]

# ==============================================================================
# MODEL CONFIGURATION
# ==============================================================================

RANDOM_FOREST = "Random Forest"

XGBOOST = "XGBoost"

SUPPORTED_MODELS = [
    RANDOM_FOREST,
    XGBOOST,
]

RF_MODEL_FILE = MODEL_DIRECTORY / "random_forest.pkl"

XGB_MODEL_FILE = MODEL_DIRECTORY / "xgboost.pkl"

LABEL_ENCODER_FILE = MODEL_DIRECTORY / "label_encoder.pkl"

# ==============================================================================
# DEFAULT MODEL PARAMETERS
# ==============================================================================

RF_N_ESTIMATORS = 200

RF_MAX_DEPTH = 15

RF_MIN_SAMPLES_SPLIT = 2

RF_MIN_SAMPLES_LEAF = 1

# ==============================================================================
# METRICS
# ==============================================================================

SUPPORTED_METRICS = [
    "accuracy",
    "precision",
    "recall",
    "f1_score",
    "roc_auc",
]

PRIMARY_METRIC = "f1_score"

# ==============================================================================
# REPORTS
# ==============================================================================

SUPPORTED_REPORT_FORMATS = [
    "html",
    "json",
    "markdown",
    "text",
]

# ==============================================================================
# FILE TYPES
# ==============================================================================

SUPPORTED_CONFIG_EXTENSIONS = [
    ".txt",
    ".cfg",
    ".conf",
]

# ==============================================================================
# STATUS
# ==============================================================================

STATUS_SUCCESS = "SUCCESS"

STATUS_FAILED = "FAILED"

STATUS_WARNING = "WARNING"

# ==============================================================================
# LOGGING
# ==============================================================================

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

DEFAULT_LOG_LEVEL = "INFO"

# ==============================================================================
# DEFAULT CONFIDENCE VALUES
# ==============================================================================

DEFAULT_CONFIDENCE = {
    "Interface": 90,
    "Routing": 95,
    "Switching": 90,
    "Security": 95,
    "Management": 85,
    "Services": 85,
    "System": 80,
    "Unknown": 50,
}

# ==============================================================================
# DEFAULT RISK SCORES
# ==============================================================================

DEFAULT_RISK_SCORE = {
    "Low": 20,
    "Medium": 50,
    "High": 85,
}

# ==============================================================================
# SHAP
# ==============================================================================

TOP_FEATURES_TO_DISPLAY = 15