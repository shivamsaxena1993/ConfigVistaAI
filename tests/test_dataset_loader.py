from __future__ import annotations

# ============================================================
# Imports
# ============================================================

from ml.dataset_loader import DatasetLoader


# ============================================================
# Test Helpers
# ============================================================

def build_loader() -> DatasetLoader:
    """
    Create a DatasetLoader instance.
    """

    return DatasetLoader()


# ============================================================
# Constructor
# ============================================================

def test_constructor():

    loader = build_loader()

    assert isinstance(

        loader,

        DatasetLoader,

    )

    assert len(loader) == 0

    assert loader.validate() is False


# ============================================================
# Dataset Loading
# ============================================================

def test_load_all():

    loader = build_loader()

    train, validation, test = loader.load_all()

    total = (

        len(train)

        +

        len(validation)

        +

        len(test)

    )

    assert len(train) == int(

        total * 0.70

    )

    expected_validation = int(

        total * 0.15

    )

    assert abs(

        len(validation)

        - expected_validation

    ) <= 1

    assert (

        len(train)

        +

        len(validation)

        +

        len(test)

        == total

    )

# ============================================================
# Individual Dataset Loading
# ============================================================

def test_load_train():

    loader = build_loader()

    train = loader.load_train()

    metadata = loader.load_metadata()

    assert len(train) > 0

    assert train.shape[1] == metadata["features"]


def test_load_validation():

    loader = build_loader()

    validation = loader.load_validation()

    assert len(validation) == 204

    metadata = loader.load_metadata()

    assert validation.shape[1] == metadata["features"]


def test_load_test():

    loader = build_loader()

    test = loader.load_test()

    assert len(test) == 205

    metadata = loader.load_metadata()

    assert test.shape[1] == metadata["features"]


# ============================================================
# Metadata Loading
# ============================================================

def test_load_metadata():

    loader = build_loader()

    loader.load_all()

    metadata = loader.load_metadata()

    assert isinstance(metadata, dict)

    assert metadata["records"] == len(loader)

    assert metadata["features"] > 0


# ============================================================
# Manifest Loading
# ============================================================

def test_load_manifest():

    loader = build_loader()

    manifest = loader.load_manifest()

    assert isinstance(

        manifest,

        dict,

    )

    assert manifest["dataset_name"] == "ConfigVista AI"

    assert manifest["dataset_version"] == "1.0"

    assert manifest["target_column"] == "deployment_successful"

# ============================================================
# Validation
# ============================================================

def test_validate():

    loader = build_loader()

    loader.load_all()

    loader.load_metadata()

    loader.load_manifest()

    assert loader.validate() is True


def test_validate_before_loading():

    loader = build_loader()

    assert loader.validate() is False


# ============================================================
# Statistics
# ============================================================

def test_statistics():

    loader = build_loader()

    loader.load_all()

    stats = loader.statistics()

    assert (

        stats["train_records"]

        +

        stats["validation_records"]

        +

        stats["test_records"]

        ==

        stats["total_records"]

    )

    metadata = loader.load_metadata()

    assert stats["features"] == metadata["features"]


# ============================================================
# Dataset Profile
# ============================================================

def test_profile():

    loader = build_loader()

    loader.load_all()

    loader.load_metadata()

    loader.load_manifest()

    profile = loader.profile()

    assert profile["train_records"] == 951

    assert profile["validation_records"] == 204

    assert profile["test_records"] == 205

    assert (
        profile["train_records"]
        +
        profile["validation_records"]
        +
        profile["test_records"]
        ==
        profile["total_records"]
    )

    metadata = loader.load_metadata()

    assert profile["features"] == metadata["features"]

    assert profile["missing_values"] == 0

    assert profile["duplicate_rows"] == 0

    assert ( profile["successful"] + profile["failed"] == profile["total_records"] )

    assert round(

        profile["success_ratio"]
    
        +
    
        profile["failure_ratio"],
    
        2,
    
    ) == 100.0

# ============================================================
# Utility Methods
# ============================================================

def test_reset():

    loader = build_loader()

    loader.load_all()

    loader.load_metadata()

    loader.load_manifest()

    loader.reset()

    assert loader.validate() is False

    assert len(loader) == 0


def test_len():

    loader = build_loader()

    loader.load_all()

    stats = loader.statistics()

    assert len(loader) == stats["total_records"]


def test_repr():

    loader = build_loader()

    loader.load_all()

    representation = repr(loader)

    assert "DatasetLoader" in representation

    assert "train=951" in representation

    assert "validation=204" in representation

    assert "test=205" in representation

    metadata = loader.load_metadata()

    assert f"features={metadata['features']}" in representation


# ============================================================
# Consistency
# ============================================================

def test_statistics_consistency():

    loader = build_loader()

    loader.load_all()

    stats = loader.statistics()

    assert (

        stats["train_records"]

        + stats["validation_records"]

        + stats["test_records"]

        == stats["total_records"]

    )


def test_profile_matches_statistics():

    loader = build_loader()

    loader.load_all()

    loader.load_metadata()

    loader.load_manifest()

    stats = loader.statistics()

    profile = loader.profile()

    assert (

        stats["total_records"]

        == profile["total_records"]

    )

    assert (

        stats["features"]

        == profile["features"]

    )