from __future__ import annotations

# ============================================================
# Imports
# ============================================================

from ml.dataset_loader import DatasetLoader
from ml.feature_encoder import FeatureEncoder


# ============================================================
# Test Helpers
# ============================================================

def build_environment():
    """
    Load the generated datasets.
    """

    loader = DatasetLoader()

    train, validation, test = loader.load_all()

    return (

        train,

        validation,

        test,

    )


def build_encoder() -> FeatureEncoder:
    """
    Create a FeatureEncoder instance.
    """

    return FeatureEncoder()


# ============================================================
# Constructor
# ============================================================

def test_constructor():

    encoder = build_encoder()

    assert isinstance(

        encoder,

        FeatureEncoder,

    )

    assert encoder.target_column == "deployment_successful"

    assert len(

        encoder.label_encoders,

    ) == 0


# ============================================================
# Split Features / Target
# ============================================================

def test_split_features_and_target():

    train, validation, test = build_environment()

    encoder = build_encoder()

    encoder.split_features_and_target(

        train,

        validation,

        test,

    )

    assert encoder.X_train.shape[0] == len(train,)

    assert encoder.X_train.shape[1] == 44

    assert encoder.y_train.shape == (

        len(train),

    )

    assert encoder.X_validation.shape == (

        len(validation),

        44,

    )

    assert encoder.y_validation.shape == (

        len(validation),

    )

    assert encoder.X_test.shape == (

        len(test),

        44,

    )

    assert encoder.y_test.shape == (

        len(test),

    )

# ============================================================
# Feature Selection
# ============================================================

def test_drop_excluded_columns():

    train, validation, test = build_environment()

    encoder = build_encoder()

    encoder.split_features_and_target(

        train,

        validation,

        test,

    )

    encoder._drop_excluded_columns()

    assert encoder.X_train.shape[0] == len(

        train,

    )

    assert encoder.X_train.shape[1] == 37

    assert encoder.X_validation.shape == (

        204,

        37,

    )

    assert encoder.X_test.shape == (

        205,

        37,

    )


def test_excluded_columns_removed():

    train, validation, test = build_environment()

    encoder = build_encoder()

    encoder.split_features_and_target(

        train,

        validation,

        test,

    )

    encoder._drop_excluded_columns()

    for column in encoder.excluded_columns:

        assert column not in encoder.X_train.columns


# ============================================================
# Categorical Features
# ============================================================

def test_get_categorical_columns():

    train, validation, test = build_environment()

    encoder = build_encoder()

    encoder.split_features_and_target(

        train,

        validation,

        test,

    )

    encoder._drop_excluded_columns()

    categorical = encoder._get_categorical_columns()

    assert isinstance(

        categorical,

        list,

    )

    assert len(

        categorical,

    ) == 15


def test_expected_categorical_columns():

    train, validation, test = build_environment()

    encoder = build_encoder()

    encoder.split_features_and_target(

        train,

        validation,

        test,

    )

    encoder._drop_excluded_columns()

    categorical = encoder._get_categorical_columns()

    expected = {

        "backup_type",

        "business_impact",

        "change_category",

        "change_scope",

        "change_type",

        "configuration_version",

        "criticality",

        "device_role",

        "model",

        "operational_status",

        "os_version",

        "predicted_risk",

        "service_criticality",

        "site_type",

        "vendor",

    }

    assert set(

        categorical,

    ) == expected

# ============================================================
# Encoding
# ============================================================

def test_fit_encoders():

    train, validation, test = build_environment()

    encoder = build_encoder()

    encoder.split_features_and_target(

        train,

        validation,

        test,

    )

    encoder._drop_excluded_columns()

    encoder.fit_encoders()

    assert len(

        encoder.label_encoders,

    ) == 15


def test_transform():

    train, validation, test = build_environment()

    encoder = build_encoder()

    encoder.split_features_and_target(

        train,

        validation,

        test,

    )

    encoder._drop_excluded_columns()

    encoder.fit_encoders()

    encoder.transform()

    assert encoder.X_train.shape[0] == len(

        train,

    )

    assert encoder.X_train.shape[1] == 37

    assert encoder.X_validation.shape == (

        len(validation),

        37,

    )

    assert encoder.X_test.shape == (

        len(test),
    
        37,
    
    )


def test_encode():

    train, validation, test = build_environment()

    encoder = build_encoder()

    encoder.encode(

        train,

        validation,

        test,

    )

    assert encoder.X_train.shape[0] == len(

        train,

    )

    assert encoder.X_train.shape[1] == 37

    assert encoder.y_train.shape == (

        len(train),

    )


def test_feature_names():

    train, validation, test = build_environment()

    encoder = build_encoder()

    encoder.encode(

        train,

        validation,

        test,

    )

    assert len(

        encoder.feature_names,

    ) == 37

    assert "risk_score" in encoder.feature_names

    assert "vendor" in encoder.feature_names

# ============================================================
# Encoded Dataset
# ============================================================

def test_encoded_columns_are_numeric():

    train, validation, test = build_environment()

    encoder = build_encoder()

    encoder.encode(

        train,

        validation,

        test,

    )

    categorical = [

        "backup_type",

        "business_impact",

        "change_category",

        "change_scope",

        "change_type",

        "configuration_version",

        "criticality",

        "device_role",

        "model",

        "operational_status",

        "os_version",

        "predicted_risk",

        "service_criticality",

        "site_type",

        "vendor",

    ]

    for column in categorical:

        assert encoder.X_train[column].dtype != object


def test_label_encoder_count():

    train, validation, test = build_environment()

    encoder = build_encoder()

    encoder.encode(

        train,

        validation,

        test,

    )

    assert len(

        encoder.label_encoders,

    ) == 15

# ============================================================
# Persistence
# ============================================================

def test_save_encoders():

    train, validation, test = build_environment()

    encoder = build_encoder()

    encoder.encode(

        train,

        validation,

        test,

    )

    encoder.save_encoders()

    assert len(

        list(

            encoder.model_directory.glob(

                "*_encoder.pkl",

            )

        )

    ) == 16


def test_load_encoders():

    train, validation, test = build_environment()

    encoder = build_encoder()

    encoder.encode(

        train,

        validation,

        test,

    )

    encoder.save_encoders()

    encoder.label_encoders.clear()

    assert len(

        encoder.label_encoders,

    ) == 0

    encoder.load_encoders()

    assert len(

        encoder.label_encoders,

    ) == 16


# ============================================================
# Consistency
# ============================================================

def test_feature_count_consistency():

    train, validation, test = build_environment()

    encoder = build_encoder()

    encoder.encode(

        train,

        validation,

        test,

    )

    assert len(

        encoder.feature_names,

    ) == encoder.X_train.shape[1]


def test_target_not_in_features():

    train, validation, test = build_environment()

    encoder = build_encoder()

    encoder.encode(

        train,

        validation,

        test,

    )

    assert (

        encoder.target_column

        not in encoder.X_train.columns

    )


def test_validation_and_test_shapes():

    train, validation, test = build_environment()

    encoder = build_encoder()

    encoder.encode(

        train,

        validation,

        test,

    )

    assert encoder.X_validation.shape[1] == encoder.X_train.shape[1]

    assert encoder.X_test.shape[1] == encoder.X_train.shape[1]