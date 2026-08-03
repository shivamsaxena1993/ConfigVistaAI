"""
=============================================================

ConfigVista AI

Enterprise Incident Generator Tests

=============================================================
"""

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

from enterprise.models import (
    Incident,
)


# ==========================================================
# Helpers
# ==========================================================

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
        config
    )

    changes = ChangeGenerator().generate(

        config,

        sites,

        devices,

        services,

    )

    return (

        config,

        sites,

        devices,

        services,

        changes,

    )


def build_generator():

    return IncidentGenerator()


# ==========================================================
# Constructor
# ==========================================================

def test_constructor():

    generator = build_generator()

    assert generator.generated_incidents == []


# ==========================================================
# Generation
# ==========================================================

def test_generate():

    (

        config,

        sites,

        devices,

        services,

        changes,

    ) = build_environment()

    generator = build_generator()

    incidents = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

    )

    assert len(incidents) > 0

    assert len(generator) == len(incidents)


def test_return_type():

    (

        config,

        sites,

        devices,

        services,

        changes,

    ) = build_environment()

    generator = build_generator()

    incidents = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

    )

    assert isinstance(

        incidents,

        list,

    )

    assert all(

        isinstance(

            incident,

            Incident,

        )

        for incident

        in incidents

    )


# ==========================================================
# Identity
# ==========================================================

def test_incident_numbers_unique():

    (

        config,

        sites,

        devices,

        services,

        changes,

    ) = build_environment()

    generator = build_generator()

    incidents = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

    )

    numbers = [

        incident.incident_number

        for incident

        in incidents

    ]

    assert len(numbers) == len(

        set(numbers)

    )


def test_title_present():

    (

        config,

        sites,

        devices,

        services,

        changes,

    ) = build_environment()

    generator = build_generator()

    incidents = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

    )

    assert all(

        incident.title != ""

        for incident

        in incidents

    )

# ==========================================================
# Classification
# ==========================================================

def test_severity_present():

    (

        config,

        sites,

        devices,

        services,

        changes,

    ) = build_environment()

    generator = build_generator()

    incidents = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

    )

    valid = {

        "Critical",

        "High",

        "Medium",

        "Low",

    }

    assert all(

        incident.severity in valid

        for incident

        in incidents

    )


def test_status_closed():

    (

        config,

        sites,

        devices,

        services,

        changes,

    ) = build_environment()

    generator = build_generator()

    incidents = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

    )

    assert all(

        incident.status == "Closed"

        for incident

        in incidents

    )


def test_category_present():

    (

        config,

        sites,

        devices,

        services,

        changes,

    ) = build_environment()

    generator = build_generator()

    incidents = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

    )

    assert all(

        incident.incident_category != ""

        for incident

        in incidents

    )


def test_assignment_group_present():

    (

        config,

        sites,

        devices,

        services,

        changes,

    ) = build_environment()

    generator = build_generator()

    incidents = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

    )

    assert all(

        incident.assignment_group != ""

        for incident

        in incidents

    )


def test_business_impact_present():

    (

        config,

        sites,

        devices,

        services,

        changes,

    ) = build_environment()

    generator = build_generator()

    incidents = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

    )

    valid = {

        "Low",

        "Medium",

        "High",

        "Critical",

    }

    assert all(

        incident.business_impact in valid

        for incident

        in incidents

    )


# ==========================================================
# Enterprise Relationships
# ==========================================================

def test_primary_device_present():

    (

        config,

        sites,

        devices,

        services,

        changes,

    ) = build_environment()

    generator = build_generator()

    incidents = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

    )

    assert all(

        incident.primary_device_id is not None

        for incident

        in incidents

    )


def test_affected_devices_present():

    (

        config,

        sites,

        devices,

        services,

        changes,

    ) = build_environment()

    generator = build_generator()

    incidents = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

    )

    assert all(

        len(

            incident.affected_device_ids

        ) >= 1

        for incident

        in incidents

    )


def test_primary_device_in_affected_list():

    (

        config,

        sites,

        devices,

        services,

        changes,

    ) = build_environment()

    generator = build_generator()

    incidents = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

    )

    assert all(

        incident.primary_device_id

        in incident.affected_device_ids

        for incident

        in incidents

    )


def test_related_change_present():

    (

        config,

        sites,

        devices,

        services,

        changes,

    ) = build_environment()

    generator = build_generator()

    incidents = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

    )

    assert all(

        incident.related_change_id

        is not None

        for incident

        in incidents

    )


def test_site_present():

    (

        config,

        sites,

        devices,

        services,

        changes,

    ) = build_environment()

    generator = build_generator()

    incidents = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

    )

    assert all(

        incident.site_id

        is not None

        for incident

        in incidents

    )


def test_business_service_present():

    (

        config,

        sites,

        devices,

        services,

        changes,

    ) = build_environment()

    generator = build_generator()

    incidents = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

    )

    assert all(

        incident.business_service_id

        is not None

        for incident

        in incidents

    )

# ==========================================================
# RCA / Resolution
# ==========================================================

def test_root_cause_present():

    (

        config,

        sites,

        devices,

        services,

        changes,

    ) = build_environment()

    generator = build_generator()

    incidents = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

    )

    assert all(

        incident.root_cause != ""

        for incident

        in incidents

    )


def test_resolution_present():

    (

        config,

        sites,

        devices,

        services,

        changes,

    ) = build_environment()

    generator = build_generator()

    incidents = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

    )

    assert all(

        incident.resolution != ""

        for incident

        in incidents

    )


def test_resolution_code_present():

    (

        config,

        sites,

        devices,

        services,

        changes,

    ) = build_environment()

    generator = build_generator()

    incidents = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

    )

    assert all(

        incident.resolution_code != ""

        for incident

        in incidents

    )


def test_service_restored():

    (

        config,

        sites,

        devices,

        services,

        changes,

    ) = build_environment()

    generator = build_generator()

    incidents = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

    )

    assert all(

        incident.service_restored

        for incident

        in incidents

    )


def test_duration_positive():

    (

        config,

        sites,

        devices,

        services,

        changes,

    ) = build_environment()

    generator = build_generator()

    incidents = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

    )

    assert all(

        incident.duration_minutes > 0

        for incident

        in incidents

    )


# ==========================================================
# Lookup Helpers
# ==========================================================

def test_get_incident():

    (

        config,

        sites,

        devices,

        services,

        changes,

    ) = build_environment()

    generator = build_generator()

    incidents = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

    )

    first = incidents[0]

    found = generator.get_incident(

        first.incident_number

    )

    assert found is not None

    assert (

        found.incident_number

        == first.incident_number

    )


def test_unknown_incident():

    (

        config,

        sites,

        devices,

        services,

        changes,

    ) = build_environment()

    generator = build_generator()

    generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

    )

    assert (

        generator.get_incident(

            "INC-999999"

        )

        is None

    )


# ==========================================================
# Severity Helpers
# ==========================================================

def test_critical_incidents():

    (

        config,

        sites,

        devices,

        services,

        changes,

    ) = build_environment()

    generator = build_generator()

    generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

    )

    critical = generator.critical_incidents()

    assert all(

        incident.severity == "Critical"

        for incident

        in critical

    )


def test_high_incidents():

    (

        config,

        sites,

        devices,

        services,

        changes,

    ) = build_environment()

    generator = build_generator()

    generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

    )

    high = generator.high_incidents()

    assert all(

        incident.severity == "High"

        for incident

        in high

    )


def test_closed_incidents():

    (

        config,

        sites,

        devices,

        services,

        changes,

    ) = build_environment()

    generator = build_generator()

    generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

    )

    closed = generator.closed_incidents()

    assert len(closed) == len(generator)

    assert all(

        incident.status == "Closed"

        for incident

        in closed

    )


def test_open_incidents():

    (

        config,

        sites,

        devices,

        services,

        changes,

    ) = build_environment()

    generator = build_generator()

    generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

    )

    assert generator.open_incidents() == []

# ==========================================================
# Statistics
# ==========================================================

def test_statistics():

    (

        config,

        sites,

        devices,

        services,

        changes,

    ) = build_environment()

    generator = build_generator()

    generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

    )

    stats = generator.statistics()

    assert (

        stats["total_incidents"]

        == len(generator)

    )


def test_statistics_consistency():

    (

        config,

        sites,

        devices,

        services,

        changes,

    ) = build_environment()

    generator = build_generator()

    generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

    )

    stats = generator.statistics()

    assert (

        stats["critical"]

        +

        stats["high"]

        +

        stats["medium"]

        +

        stats["low"]

        ==

        stats["total_incidents"]

    )

    assert (

        stats["closed"]

        +

        stats["open"]

        ==

        stats["total_incidents"]

    )


def test_incident_rate():

    (

        config,

        sites,

        devices,

        services,

        changes,

    ) = build_environment()

    generator = build_generator()

    generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

    )

    stats = generator.statistics()

    assert (

        0

        <=

        stats["incident_rate"]

        <=

        100

    )


# ==========================================================
# Relationship Validation
# ==========================================================

def test_validate_relationships():

    (

        config,

        sites,

        devices,

        services,

        changes,

    ) = build_environment()

    generator = build_generator()

    generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

    )

    assert (

        generator.validate_relationships()

        is True

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

        changes,

    ) = build_environment()

    generator = build_generator()

    generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

    )

    generator.reset()

    assert len(generator) == 0

    assert generator.generated_incidents == []


# ==========================================================
# Utility Methods
# ==========================================================

def test_len():

    (

        config,

        sites,

        devices,

        services,

        changes,

    ) = build_environment()

    generator = build_generator()

    incidents = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

    )

    assert len(generator) == len(incidents)


def test_repr():

    (

        config,

        sites,

        devices,

        services,

        changes,

    ) = build_environment()

    generator = build_generator()

    generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

    )

    representation = repr(generator)

    assert "IncidentGenerator" in representation

    assert "incidents=" in representation

    assert "rate=" in representation


# ==========================================================
# Deterministic Generation
# ==========================================================

def test_generation_is_deterministic():

    (

        config,

        sites,

        devices,

        services,

        changes,

    ) = build_environment()

    generator = build_generator()

    first = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

    )

    first_numbers = [

        incident.incident_number

        for incident

        in first

    ]

    second = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

    )

    second_numbers = [

        incident.incident_number

        for incident

        in second

    ]

    assert first_numbers == second_numbers


# ==========================================================
# Integrity
# ==========================================================

def test_all_incidents_have_required_fields():

    (

        config,

        sites,

        devices,

        services,

        changes,

    ) = build_environment()

    generator = build_generator()

    incidents = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

    )

    assert all(

        incident.title != ""

        for incident

        in incidents

    )

    assert all(

        incident.root_cause != ""

        for incident

        in incidents

    )

    assert all(

        incident.resolution_code != ""

        for incident

        in incidents

    )


def test_every_incident_links_to_change():

    (

        config,

        sites,

        devices,

        services,

        changes,

    ) = build_environment()

    generator = build_generator()

    incidents = generator.generate(

        config,

        sites,

        devices,

        services,

        changes,

    )

    change_ids = {

        change.change_id

        for change

        in changes

    }

    assert all(

        incident.related_change_id

        in change_ids

        for incident

        in incidents

    )
