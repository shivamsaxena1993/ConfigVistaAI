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

    assert len(train) == 210

    assert len(validation) == 45

    assert len(test) == 45

# ============================================================
# Individual Dataset Loading
# ============================================================

def test_load_train():

    loader = build_loader()

    train = loader.load_train()

    assert len(train) == 210

    assert train.shape[1] == 47


def test_load_validation():

    loader = build_loader()

    validation = loader.load_validation()

    assert len(validation) == 45

    assert validation.shape[1] == 47


def test_load_test():

    loader = build_loader()

    test = loader.load_test()

    assert len(test) == 45

    assert test.shape[1] == 47


# ============================================================
# Metadata Loading
# ============================================================

def test_load_metadata():

    loader = build_loader()

    metadata = loader.load_metadata()

    assert isinstance(

        metadata,

        dict,

    )

    assert metadata["records"] == 300

    assert metadata["features"] == 47

    assert metadata["target_column"] == "deployment_successful"


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

    assert stats["train_records"] == 210

    assert stats["validation_records"] == 45

    assert stats["test_records"] == 45

    assert stats["total_records"] == 300

    assert stats["features"] == 47


# ============================================================
# Dataset Profile
# ============================================================

def test_profile():

    loader = build_loader()

    loader.load_all()

    loader.load_metadata()

    loader.load_manifest()

    profile = loader.profile()

    assert profile["train_records"] == 210

    assert profile["validation_records"] == 45

    assert profile["test_records"] == 45

    assert profile["total_records"] == 300

    assert profile["features"] == 47

    assert profile["missing_values"] == 0

    assert profile["duplicate_rows"] == 0

    assert profile["successful"] == 270

    assert profile["failed"] == 30

    assert profile["success_ratio"] == 90.0

    assert profile["failure_ratio"] == 10.0

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

    assert len(loader) == 300


def test_repr():

    loader = build_loader()

    loader.load_all()

    representation = repr(loader)

    assert "DatasetLoader" in representation

    assert "train=210" in representation

    assert "validation=45" in representation

    assert "test=45" in representation

    assert "features=47" in representation


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