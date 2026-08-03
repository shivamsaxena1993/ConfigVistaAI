"""
=============================================================

ConfigVista AI

Historical Change Generator Tests

=============================================================
"""

from enterprise.generators.change_generator import (
    ChangeGenerator,
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

from enterprise.generators.enterprise_generator import (
    EnterpriseGenerationConfig,
)

from enterprise.models import (
    HistoricalChange,
)


# ==========================================================
# Helpers
# ==========================================================

def build_generator():

    return ChangeGenerator()


def build_environment():

    config = EnterpriseGenerationConfig()

    sites = SiteGenerator().generate(
        config
    )

    devices = DeviceGenerator().generate(
        config,
        sites,
        [],
    )

    services = BusinessServiceGenerator().generate(
        config,
    )

    return (

        config,

        sites,

        devices,

        services,

    )


# ==========================================================
# Constructor
# ==========================================================

def test_constructor():

    generator = build_generator()

    assert generator.generated_changes == []


# ==========================================================
# Generation
# ==========================================================

def test_generate():

    (

        config,

        sites,

        devices,

        services,

    ) = build_environment()

    generator = build_generator()

    changes = generator.generate(

        config,

        sites,

        devices,

        services,

    )

    assert len(changes) == len(devices)

    assert len(generator) == len(devices)


def test_return_type():

    (

        config,

        sites,

        devices,

        services,

    ) = build_environment()

    generator = build_generator()

    changes = generator.generate(

        config,

        sites,

        devices,

        services,

    )

    assert isinstance(

        changes,

        list,

    )

    assert all(

        isinstance(

            change,

            HistoricalChange,

        )

        for change

        in changes

    )


# ==========================================================
# Basic Validation
# ==========================================================

def test_total_changes():

    (

        config,

        sites,

        devices,

        services,

    ) = build_environment()

    generator = build_generator()

    changes = generator.generate(

        config,

        sites,

        devices,

        services,

    )

    assert len(changes) == 300


def test_change_numbers_unique():

    (

        config,

        sites,

        devices,

        services,

    ) = build_environment()

    generator = build_generator()

    changes = generator.generate(

        config,

        sites,

        devices,

        services,

    )

    numbers = [

        c.change_number

        for c

        in changes

    ]

    assert len(numbers) == len(

        set(numbers)

    )


def test_primary_device_present():

    (

        config,

        sites,

        devices,

        services,

    ) = build_environment()

    generator = build_generator()

    changes = generator.generate(

        config,

        sites,

        devices,

        services,

    )

    assert all(

        change.primary_device_id is not None

        for change

        in changes

    )


def test_affected_devices_present():

    (

        config,

        sites,

        devices,

        services,

    ) = build_environment()

    generator = build_generator()

    changes = generator.generate(

        config,

        sites,

        devices,

        services,

    )

    assert all(

        len(

            change.affected_device_ids

        ) >= 1

        for change

        in changes

    )


def test_primary_device_in_affected_list():

    (

        config,

        sites,

        devices,

        services,

    ) = build_environment()

    generator = build_generator()

    changes = generator.generate(

        config,

        sites,

        devices,

        services,

    )

    assert all(

        change.primary_device_id

        in change.affected_device_ids

        for change

        in changes

    )

# ==========================================================
# Change Scope
# ==========================================================

def test_change_scope_present():

    (

        config,

        sites,

        devices,

        services,

    ) = build_environment()

    generator = build_generator()

    changes = generator.generate(

        config,

        sites,

        devices,

        services,

    )

    assert all(

        change.change_scope != ""

        for change

        in changes

    )


def test_change_scope_valid():

    (

        config,

        sites,

        devices,

        services,

    ) = build_environment()

    generator = build_generator()

    changes = generator.generate(

        config,

        sites,

        devices,

        services,

    )

    valid = {

        "Single Device",

        "Device Pair",

        "Site",

        "Regional",

        "Global",

    }

    assert all(

        change.change_scope in valid

        for change

        in changes

    )


# ==========================================================
# Change Category / Type
# ==========================================================

def test_change_category_present():

    (

        config,

        sites,

        devices,

        services,

    ) = build_environment()

    generator = build_generator()

    changes = generator.generate(

        config,

        sites,

        devices,

        services,

    )

    assert all(

        change.change_category != ""

        for change

        in changes

    )


def test_change_type_present():

    (

        config,

        sites,

        devices,

        services,

    ) = build_environment()

    generator = build_generator()

    changes = generator.generate(

        config,

        sites,

        devices,

        services,

    )

    assert all(

        change.change_type != ""

        for change

        in changes

    )


# ==========================================================
# Risk / Confidence
# ==========================================================

def test_risk_score_range():

    (

        config,

        sites,

        devices,

        services,

    ) = build_environment()

    generator = build_generator()

    changes = generator.generate(

        config,

        sites,

        devices,

        services,

    )

    assert all(

        0 <= change.risk_score <= 100

        for change

        in changes

    )


def test_confidence_score_range():

    (

        config,

        sites,

        devices,

        services,

    ) = build_environment()

    generator = build_generator()

    changes = generator.generate(

        config,

        sites,

        devices,

        services,

    )

    assert all(

        0 <= change.confidence_score <= 100

        for change

        in changes

    )


def test_predicted_risk_present():

    (

        config,

        sites,

        devices,

        services,

    ) = build_environment()

    generator = build_generator()

    changes = generator.generate(

        config,

        sites,

        devices,

        services,

    )

    valid = {

        "Low",

        "Medium",

        "High",

    }

    assert all(

        change.predicted_risk in valid

        for change

        in changes

    )


# ==========================================================
# Business Impact
# ==========================================================

def test_business_impact_present():

    (

        config,

        sites,

        devices,

        services,

    ) = build_environment()

    generator = build_generator()

    changes = generator.generate(

        config,

        sites,

        devices,

        services,

    )

    valid = {

        "Low",

        "Medium",

        "High",

        "Critical",

    }

    assert all(

        change.business_impact in valid

        for change

        in changes

    )

# ==========================================================
# Outcome / Rollback
# ==========================================================

def test_successful_failed_distribution():

    (

        config,

        sites,

        devices,

        services,

    ) = build_environment()

    generator = build_generator()

    generator.generate(

        config,

        sites,

        devices,

        services,

    )

    successful = generator.successful_changes()

    failed = generator.failed_changes()

    assert len(successful) + len(failed) == len(generator)

    assert len(successful) > 0

    assert len(failed) > 0


def test_rollback_changes():

    (

        config,

        sites,

        devices,

        services,

    ) = build_environment()

    generator = build_generator()

    generator.generate(

        config,

        sites,

        devices,

        services,

    )

    rollbacks = generator.rollback_changes()

    assert all(

        change.rollback_required

        for change

        in rollbacks

    )


# ==========================================================
# Lookup
# ==========================================================

def test_get_change():

    (

        config,

        sites,

        devices,

        services,

    ) = build_environment()

    generator = build_generator()

    changes = generator.generate(

        config,

        sites,

        devices,

        services,

    )

    first = changes[0]

    found = generator.get_change(

        first.change_number

    )

    assert found is not None

    assert (

        found.change_number

        == first.change_number

    )


def test_unknown_change():

    (

        config,

        sites,

        devices,

        services,

    ) = build_environment()

    generator = build_generator()

    generator.generate(

        config,

        sites,

        devices,

        services,

    )

    assert (

        generator.get_change(

            "CHG-999999"

        )

        is None

    )


# ==========================================================
# Statistics
# ==========================================================

def test_statistics():

    (

        config,

        sites,

        devices,

        services,

    ) = build_environment()

    generator = build_generator()

    generator.generate(

        config,

        sites,

        devices,

        services,

    )

    stats = generator.statistics()

    assert (

        stats["total_changes"]

        == len(generator)

    )


def test_statistics_consistency():

    (

        config,

        sites,

        devices,

        services,

    ) = build_environment()

    generator = build_generator()

    generator.generate(

        config,

        sites,

        devices,

        services,

    )

    stats = generator.statistics()

    assert (

        stats["successful"]

        + stats["failed"]

        == stats["total_changes"]

    )

    assert (

        stats["single_device"]

        + stats["device_pair"]

        + stats["site"]

        + stats["regional"]

        + stats["global"]

        == stats["total_changes"]

    )


# ==========================================================
# Reset
# ==========================================================

def test_reset():

    (

        config,

        sites,

        devices,

        services,

    ) = build_environment()

    generator = build_generator()

    generator.generate(

        config,

        sites,

        devices,

        services,

    )

    generator.reset()

    assert len(generator) == 0

    assert generator.generated_changes == []


# ==========================================================
# Utility Methods
# ==========================================================

def test_len():

    (

        config,

        sites,

        devices,

        services,

    ) = build_environment()

    generator = build_generator()

    generator.generate(

        config,

        sites,

        devices,

        services,

    )

    assert len(generator) == 300


def test_repr():

    (

        config,

        sites,

        devices,

        services,

    ) = build_environment()

    generator = build_generator()

    generator.generate(

        config,

        sites,

        devices,

        services,

    )

    representation = repr(generator)

    assert "ChangeGenerator" in representation

    assert "changes=300" in representation


# ==========================================================
# Deterministic Generation
# ==========================================================

def test_generation_is_deterministic():

    (

        config,

        sites,

        devices,

        services,

    ) = build_environment()

    generator = build_generator()

    first = generator.generate(

        config,

        sites,

        devices,

        services,

    )

    first_numbers = [

        c.change_number

        for c

        in first

    ]

    second = generator.generate(

        config,

        sites,

        devices,

        services,

    )

    second_numbers = [

        c.change_number

        for c

        in second

    ]

    assert first_numbers == second_numbers


# ==========================================================
# Integrity
# ==========================================================

def test_all_changes_have_comments():

    (

        config,

        sites,

        devices,

        services,

    ) = build_environment()

    generator = build_generator()

    changes = generator.generate(

        config,

        sites,

        devices,

        services,

    )

    assert all(

        change.comments != ""

        for change

        in changes

    )


def test_site_and_service_present():

    (

        config,

        sites,

        devices,

        services,

    ) = build_environment()

    generator = build_generator()

    changes = generator.generate(

        config,

        sites,

        devices,

        services,

    )

    assert all(

        change.site_id is not None

        for change

        in changes

    )

    assert all(

        change.business_service_id

        is not None

        for change

        in changes

    )
