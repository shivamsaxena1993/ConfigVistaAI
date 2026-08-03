from pathlib import Path

import pandas as pd

from enterprise.exporters.dataset_exporter import DatasetExporter

from enterprise.generators.enterprise_generator import (
    EnterpriseGenerationConfig,
)

from enterprise.generators.site_generator import (
    SiteGenerator,
)

from enterprise.generators.device_generator import (
    DeviceGenerator,
)

from enterprise.generators.business_service_generator import (
    BusinessServiceGenerator,
)

from enterprise.generators.change_generator import (
    ChangeGenerator,
)

from enterprise.generators.incident_generator import (
    IncidentGenerator,
)

from enterprise.generators.configuration_backup_generator import (
    ConfigurationBackupGenerator,
)

from enterprise.generators.operational_snapshot_generator import (
    OperationalSnapshotGenerator,
)

from enterprise.generators.feature_generator import (
    FeatureGenerator,
)


# ============================================================
# Test Helpers
# ============================================================


def build_environment():

    config = EnterpriseGenerationConfig()

    sites = SiteGenerator().generate(
        config,
    )

    devices = DeviceGenerator().generate(
        config,
        sites,
        [],
    )

    services = BusinessServiceGenerator().generate(
        config,
    )

    changes = ChangeGenerator().generate(
        config,
        sites,
        devices,
        services,
    )

    incidents = IncidentGenerator().generate(
        config,
        sites,
        devices,
        services,
        changes,
    )

    backups = ConfigurationBackupGenerator().generate(
        config,
        devices,
    )

    snapshots = OperationalSnapshotGenerator().generate(
        config,
        devices,
    )

    features = FeatureGenerator().generate(
        config,
        sites,
        devices,
        services,
        changes,
        incidents,
        backups,
        snapshots,
    )

    return (

        config,

        features,

    )


def build_exporter():

    return DatasetExporter()


# ============================================================
# Constructor
# ============================================================


def test_constructor():

    exporter = build_exporter()

    assert exporter.dataset == []


# ============================================================
# DataFrame Export
# ============================================================


def test_export_dataframe():

    (

        config,

        features,

    ) = build_environment()

    exporter = build_exporter()

    dataframe = exporter.export_dataframe(

        features,

    )

    assert isinstance(

        dataframe,

        pd.DataFrame,

    )


def test_return_type():

    (

        config,

        features,

    ) = build_environment()

    exporter = build_exporter()

    dataframe = exporter.export_dataframe(

        features,

    )

    assert isinstance(

        dataframe,

        pd.DataFrame,

    )


def test_total_records():

    (

        config,

        features,

    ) = build_environment()

    exporter = build_exporter()

    dataframe = exporter.export_dataframe(

        features,

    )

    assert len(

        dataframe,

    ) == len(

        features,

    )


def test_dataframe_not_empty():

    (

        config,

        features,

    ) = build_environment()

    exporter = build_exporter()

    dataframe = exporter.export_dataframe(

        features,

    )

    assert not dataframe.empty


def test_dataframe_columns():

    (

        config,

        features,

    ) = build_environment()

    exporter = build_exporter()

    dataframe = exporter.export_dataframe(

        features,

    )

    assert len(

        dataframe.columns,

    ) == len(

        features[0].to_dict(),

    )

# ============================================================
# CSV Export
# ============================================================


def test_export_csv(
    tmp_path,
):

    (

        config,

        features,

    ) = build_environment()

    exporter = build_exporter()

    output_file = (

        tmp_path

        / "feature_dataset.csv"

    )

    dataframe = exporter.export_csv(

        features,

        output_file,

    )

    assert isinstance(

        dataframe,

        pd.DataFrame,

    )


def test_csv_file_created(
    tmp_path,
):

    (

        config,

        features,

    ) = build_environment()

    exporter = build_exporter()

    output_file = (

        tmp_path

        / "feature_dataset.csv"

    )

    exporter.export_csv(

        features,

        output_file,

    )

    assert output_file.exists()


def test_csv_row_count(
    tmp_path,
):

    (

        config,

        features,

    ) = build_environment()

    exporter = build_exporter()

    output_file = (

        tmp_path

        / "feature_dataset.csv"

    )

    exporter.export_csv(

        features,

        output_file,

    )

    dataframe = pd.read_csv(

        output_file,

    )

    assert len(

        dataframe,

    ) == len(

        features,

    )


def test_csv_column_count(
    tmp_path,
):

    (

        config,

        features,

    ) = build_environment()

    exporter = build_exporter()

    output_file = (

        tmp_path

        / "feature_dataset.csv"

    )

    exporter.export_csv(

        features,

        output_file,

    )

    dataframe = pd.read_csv(

        output_file,

    )

    assert len(

        dataframe.columns,

    ) == len(

        features[0].to_dict(),

    )


def test_export_dataframe_consistency(
    tmp_path,
):

    (

        config,

        features,

    ) = build_environment()

    exporter = build_exporter()

    dataframe = exporter.export_dataframe(

        features,

    )

    output_file = (

        tmp_path

        / "feature_dataset.csv"

    )

    exporter.export_csv(

        features,

        output_file,

    )

    csv_dataframe = pd.read_csv(

        output_file,

    )

    assert dataframe.shape == csv_dataframe.shape

# ============================================================
# Statistics
# ============================================================


def test_statistics():

    (

        config,

        features,

    ) = build_environment()

    exporter = build_exporter()

    exporter.export_dataframe(

        features,

    )

    stats = exporter.statistics()

    assert isinstance(

        stats,

        dict,

    )


def test_statistics_records():

    (

        config,

        features,

    ) = build_environment()

    exporter = build_exporter()

    exporter.export_dataframe(

        features,

    )

    stats = exporter.statistics()

    assert (

        stats["records"]

        ==

        len(features)

    )


def test_statistics_columns():

    (

        config,

        features,

    ) = build_environment()

    exporter = build_exporter()

    exporter.export_dataframe(

        features,

    )

    stats = exporter.statistics()

    assert (

        stats["columns"]

        ==

        len(features[0].to_dict())

    )


def test_statistics_success_failed():

    (

        config,

        features,

    ) = build_environment()

    exporter = build_exporter()

    exporter.export_dataframe(

        features,

    )

    stats = exporter.statistics()

    assert (

        stats["successful"]

        +

        stats["failed"]

        ==

        stats["records"]

    )


def test_statistics_average_values():

    (

        config,

        features,

    ) = build_environment()

    exporter = build_exporter()

    exporter.export_dataframe(

        features,

    )

    stats = exporter.statistics()

    assert (

        0

        <=

        stats["average_risk"]

        <=

        100

    )

    assert (

        0

        <=

        stats["average_confidence"]

        <=

        100

    )


# ============================================================
# Dataset Validation
# ============================================================


def test_validate_dataset():

    (

        config,

        features,

    ) = build_environment()

    exporter = build_exporter()

    exporter.export_dataframe(

        features,

    )

    assert exporter.validate_dataset()


def test_validate_empty_dataset():

    exporter = build_exporter()

    assert not exporter.validate_dataset()


def test_validate_after_export():

    (

        config,

        features,

    ) = build_environment()

    exporter = build_exporter()

    exporter.export_dataframe(

        features,

    )

    assert exporter.validate_dataset()


def test_statistics_consistency():

    (

        config,

        features,

    ) = build_environment()

    exporter = build_exporter()

    exporter.export_dataframe(

        features,

    )

    stats = exporter.statistics()

    assert (

        stats["successful"]

        +

        stats["failed"]

        ==

        stats["records"]

    )
# ============================================================
# Reset
# ============================================================


def test_reset():

    (

        config,

        features,

    ) = build_environment()

    exporter = build_exporter()

    exporter.export_dataframe(

        features,

    )

    exporter.reset()

    assert len(

        exporter.dataset,

    ) == 0


# ============================================================
# Length
# ============================================================


def test_len():

    (

        config,

        features,

    ) = build_environment()

    exporter = build_exporter()

    exporter.export_dataframe(

        features,

    )

    assert len(

        exporter,

    ) == len(

        features,

    )


# ============================================================
# Representation
# ============================================================


def test_repr():

    (

        config,

        features,

    ) = build_environment()

    exporter = build_exporter()

    exporter.export_dataframe(

        features,

    )

    representation = repr(

        exporter,

    )

    assert "DatasetExporter" in representation

    assert "records=" in representation

    assert "successful=" in representation

    assert "failed=" in representation


# ============================================================
# Deterministic Export
# ============================================================


def test_export_is_deterministic():

    (

        config,

        features,

    ) = build_environment()

    exporter = build_exporter()

    dataframe_one = exporter.export_dataframe(

        features,

    )

    dataframe_two = exporter.export_dataframe(

        features,

    )

    assert dataframe_one.equals(

        dataframe_two,

    )


# ============================================================
# Data Integrity
# ============================================================


def test_dataframe_matches_feature_count():

    (

        config,

        features,

    ) = build_environment()

    exporter = build_exporter()

    dataframe = exporter.export_dataframe(

        features,

    )

    assert len(

        dataframe,

    ) == len(

        features,

    )


def test_dataframe_contains_target_column():

    (

        config,

        features,

    ) = build_environment()

    exporter = build_exporter()

    dataframe = exporter.export_dataframe(

        features,

    )

    assert (

        "deployment_successful"

        in dataframe.columns

    )


def test_csv_matches_dataframe(

    tmp_path,

):

    (

        config,

        features,

    ) = build_environment()

    exporter = build_exporter()

    dataframe = exporter.export_dataframe(

        features,

    )

    output_file = (

        tmp_path

        / "feature_dataset.csv"

    )

    exporter.export_csv(

        features,

        output_file,

    )

    csv_dataframe = pd.read_csv(

        output_file,

    )

    assert list(

        dataframe.columns,

    ) == list(

        csv_dataframe.columns,

    )


# ============================================================
# Post Reset Statistics
# ============================================================


def test_statistics_after_reset():

    (

        config,

        features,

    ) = build_environment()

    exporter = build_exporter()

    exporter.export_dataframe(

        features,

    )

    exporter.reset()

    stats = exporter.statistics()

    assert stats["records"] == 0

    assert stats["successful"] == 0

    assert stats["failed"] == 0

    assert stats["average_risk"] == 0.0

    assert stats["average_confidence"] == 0.0