from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:

    sys.path.insert(

        0,

        str(PROJECT_ROOT),

    )

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

from enterprise.models import (
    FeatureVector,
)


# ============================================================
# Helpers
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

    return (

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    )


def build_generator():

    return FeatureGenerator()


# ============================================================
# Constructor
# ============================================================

def test_constructor():

    generator = build_generator()

    assert len(

        generator.generated_features

    ) == 0


# ============================================================
# Generate
# ============================================================

def test_generate():

    (

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    ) = build_environment()

    generator = build_generator()

    features = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    )

    assert len(

        features

    ) == len(

        changes

    )


def test_return_type():

    (

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    ) = build_environment()

    generator = build_generator()

    features = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    )

    assert all(

        isinstance(

            feature,

            FeatureVector,

        )

        for feature

        in features

    )


def test_total_features():

    (

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    ) = build_environment()

    generator = build_generator()

    features = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    )

    assert len(

        features

    ) == len(

        changes

    )


# ============================================================
# Identity
# ============================================================

def test_feature_vector_ids_unique():

    (

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    ) = build_environment()

    generator = build_generator()

    features = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    )

    ids = {

        feature.feature_vector_id

        for feature

        in features

    }

    assert len(

        ids

    ) == len(

        features

    )


def test_change_ids_present():

    (

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    ) = build_environment()

    generator = build_generator()

    features = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    )

    assert all(

        feature.change_id

        is not None

        for feature

        in features

    )

# ============================================================
# Identity
# ============================================================

def test_device_ids_present():

    (

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    ) = build_environment()

    generator = build_generator()

    features = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    )

    assert all(

        feature.device_id

        is not None

        for feature

        in features

    )


def test_site_ids_present():

    (

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    ) = build_environment()

    generator = build_generator()

    features = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    )

    assert all(

        feature.site_id

        is not None

        for feature

        in features

    )


def test_business_service_ids_present():

    (

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    ) = build_environment()

    generator = build_generator()

    features = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    )

    assert all(

        feature.business_service_id

        is not None

        for feature

        in features

    )


# ============================================================
# Change Features
# ============================================================

def test_change_scope_present():

    (

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    ) = build_environment()

    generator = build_generator()

    features = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    )

    assert all(

        feature.change_scope != ""

        for feature

        in features

    )


def test_change_category_present():

    (

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    ) = build_environment()

    generator = build_generator()

    features = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    )

    assert all(

        feature.change_category != ""

        for feature

        in features

    )


def test_change_type_present():

    (

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    ) = build_environment()

    generator = build_generator()

    features = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    )

    assert all(

        feature.change_type != ""

        for feature

        in features

    )


def test_predicted_risk_present():

    (

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    ) = build_environment()

    generator = build_generator()

    features = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    )

    valid = {

        "Low",

        "Medium",

        "High",

    }

    assert all(

        feature.predicted_risk

        in valid

        for feature

        in features

    )


def test_risk_score_range():

    (

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    ) = build_environment()

    generator = build_generator()

    features = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    )

    assert all(

        0 <= feature.risk_score <= 100

        for feature

        in features

    )


def test_confidence_score_range():

    (

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    ) = build_environment()

    generator = build_generator()

    features = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    )

    assert all(

        0 <= feature.confidence_score <= 100

        for feature

        in features

    )


def test_business_impact_present():

    (

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    ) = build_environment()

    generator = build_generator()

    features = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    )

    assert all(

        feature.business_impact != ""

        for feature

        in features

    )

# ============================================================
# Device Features
# ============================================================

def test_device_role_present():

    (

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    ) = build_environment()

    generator = build_generator()

    features = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    )

    valid = {

        "CORE",

        "DIST",

        "ACCESS",

        "FW",

        "WAN",

    }

    assert all(

        feature.device_role

        in valid

        for feature

        in features

    )


def test_vendor_present():

    (

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    ) = build_environment()

    generator = build_generator()

    features = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    )

    assert all(

        feature.vendor != ""

        for feature

        in features

    )


def test_platform_information_present():

    (

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    ) = build_environment()

    generator = build_generator()

    features = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    )

    assert all(

        feature.model != ""

        and

        feature.os_version != ""

        for feature

        in features

    )


def test_health_score_range():

    (

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    ) = build_environment()

    generator = build_generator()

    features = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    )

    assert all(

        0 <= feature.current_health_score <= 100

        for feature

        in features

    )


def test_availability_range():

    (

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    ) = build_environment()

    generator = build_generator()

    features = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    )

    assert all(

        0 <= feature.availability_percent <= 100

        for feature

        in features

    )


# ============================================================
# Operational Features
# ============================================================

def test_cpu_range():

    (

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    ) = build_environment()

    generator = build_generator()

    features = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    )

    assert all(

        0 <= feature.cpu_utilization <= 100

        for feature

        in features

    )


def test_memory_range():

    (

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    ) = build_environment()

    generator = build_generator()

    features = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    )

    assert all(

        0 <= feature.memory_utilization <= 100

        for feature

        in features

    )


def test_latency_positive():

    (

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    ) = build_environment()

    generator = build_generator()

    features = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    )

    assert all(

        feature.latency_ms >= 0

        for feature

        in features

    )


def test_packet_loss_range():

    (

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    ) = build_environment()

    generator = build_generator()

    features = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    )

    assert all(

        0 <= feature.packet_loss_percent <= 100

        for feature

        in features

    )


def test_routing_convergence_boolean():

    (

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    ) = build_environment()

    generator = build_generator()

    features = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    )

    assert all(

        isinstance(

            feature.routing_converged,

            bool,

        )

        for feature

        in features

    )


# ============================================================
# Configuration Features
# ============================================================

def test_backup_type_present():

    (

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    ) = build_environment()

    generator = build_generator()

    features = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    )

    valid = {

        "Running",

        "Startup",

    }

    assert all(

        feature.backup_type

        in valid

        for feature

        in features

    )


def test_configuration_size_positive():

    (

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    ) = build_environment()

    generator = build_generator()

    features = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    )

    assert all(

        feature.configuration_size > 0

        for feature

        in features

    )


def test_line_count_positive():

    (

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    ) = build_environment()

    generator = build_generator()

    features = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    )

    assert all(

        feature.line_count > 0

        for feature

        in features

    )


def test_feature_count_positive():

    (

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    ) = build_environment()

    generator = build_generator()

    features = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    )

    assert all(

        feature.feature_count > 0

        for feature

        in features

    )

# ============================================================
# Historical Features
# ============================================================

def test_previous_incidents_positive():

    (

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    ) = build_environment()

    generator = build_generator()

    features = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    )

    assert all(

        feature.previous_incidents >= 0

        for feature

        in features

    )


def test_critical_incidents_positive():

    (

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    ) = build_environment()

    generator = build_generator()

    features = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    )

    assert all(

        feature.critical_incidents >= 0

        for feature

        in features

    )


def test_change_history_counts():

    (

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    ) = build_environment()

    generator = build_generator()

    features = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    )

    assert all(

        (

            feature.successful_changes

            +

            feature.failed_changes

        )

        == 1

        for feature

        in features

    )


def test_rollback_history_boolean():

    (

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    ) = build_environment()

    generator = build_generator()

    features = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    )

    assert all(

        feature.rollback_history

        in {0, 1}

        for feature

        in features

    )


# ============================================================
# Business Features
# ============================================================

def test_service_criticality_present():

    (

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    ) = build_environment()

    generator = build_generator()

    features = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    )

    valid = {

        "Critical",

        "High",

        "Medium",

        "Low",

    }

    assert all(

        feature.service_criticality

        in valid

        for feature

        in features

    )


def test_site_type_present():

    (

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    ) = build_environment()

    generator = build_generator()

    features = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    )

    valid = {

        "Data Center",
    
        "Regional Office",
    
        "Branch",
    
    }

    assert all(

        feature.site_type

        in valid

        for feature

        in features

    )


def test_redundancy_boolean():

    (

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    ) = build_environment()

    generator = build_generator()

    features = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    )

    assert all(

        isinstance(

            feature.redundancy,

            bool,

        )

        for feature

        in features

    )


# ============================================================
# Target
# ============================================================

def test_deployment_successful_boolean():

    (

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    ) = build_environment()

    generator = build_generator()

    features = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    )

    assert all(

        isinstance(

            feature.deployment_successful,

            bool,

        )

        for feature

        in features

    )


# ============================================================
# Lookup
# ============================================================

def test_get_feature_vector():

    (

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    ) = build_environment()

    generator = build_generator()

    features = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    )

    feature = generator.get_feature_vector(

        features[0].feature_vector_id

    )

    assert feature is not None

    assert (

        feature.feature_vector_id

        ==

        features[0].feature_vector_id

    )


def test_unknown_feature_vector():

    (

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    ) = build_environment()

    generator = build_generator()

    generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    )

    assert (

        generator.get_feature_vector(

            "UNKNOWN"

        )

        is None

    )


# ============================================================
# Statistics
# ============================================================

def test_statistics():

    (

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    ) = build_environment()

    generator = build_generator()

    generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    )

    stats = generator.statistics()

    assert stats["total_features"] == len(changes)

    assert "average_risk" in stats

    assert "average_confidence" in stats


def test_statistics_consistency():

    (

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    ) = build_environment()

    generator = build_generator()

    generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    )

    stats = generator.statistics()

    assert (

        stats["high_risk"]

        +

        stats["medium_risk"]

        +

        stats["low_risk"]

        ==

        stats["total_features"]

    )

    assert (

        stats["successful"]

        +

        stats["failed"]

        ==

        stats["total_features"]

    )


# ============================================================
# Validation
# ============================================================

def test_validate_relationships():

    (

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    ) = build_environment()

    generator = build_generator()

    generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

        incidents,

        backups,

        snapshots,

    )

    assert (

        generator.validate_relationships()

        is True

    )

