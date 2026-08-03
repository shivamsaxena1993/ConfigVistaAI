"""
=============================================================

ConfigVista AI

Business Service Generator Tests

=============================================================
"""

from enterprise.generators.business_service_generator import (
    BusinessServiceGenerator,
)

from enterprise.generators.enterprise_generator import (
    EnterpriseGenerationConfig,
)

from enterprise.models import (
    BusinessService,
)


# ==========================================================
# Helpers
# ==========================================================

def build_generator():

    return BusinessServiceGenerator()


# ==========================================================
# Constructor
# ==========================================================

def test_constructor():

    generator = build_generator()

    assert generator.generated_services == []


# ==========================================================
# Generation
# ==========================================================

def test_generate():

    generator = build_generator()

    services = generator.generate(

        EnterpriseGenerationConfig(),

    )

    assert len(services) == 12

    assert len(generator) == 12


def test_return_type():

    generator = build_generator()

    services = generator.generate(

        EnterpriseGenerationConfig(),

    )

    assert isinstance(

        services,

        list,

    )

    assert all(

        isinstance(service, BusinessService)

        for service in services

    )


# ==========================================================
# Service Catalog
# ==========================================================

def test_total_services():

    generator = build_generator()

    services = generator.generate(

        EnterpriseGenerationConfig(),

    )

    assert len(services) == 12


def test_service_names():

    generator = build_generator()

    services = generator.generate(

        EnterpriseGenerationConfig(),

    )

    names = [

        service.service_name

        for service in services

    ]

    assert "Corporate WAN" in names

    assert "Internet Edge" in names

    assert "Data Center Fabric" in names

    assert "Branch Connectivity" in names


def test_service_ids_unique():

    generator = build_generator()

    services = generator.generate(

        EnterpriseGenerationConfig(),

    )

    service_ids = [

        service.service_id

        for service in services

    ]

    assert len(service_ids) == len(

        set(service_ids)

    )


# ==========================================================
# Criticality
# ==========================================================

def test_critical_service_count():

    generator = build_generator()

    services = generator.generate(

        EnterpriseGenerationConfig(),

    )

    critical = [

        service

        for service in services

        if service.criticality == "Critical"

    ]

    assert len(critical) == 4

# ==========================================================
# Criticality Distribution
# ==========================================================

def test_high_service_count():

    generator = build_generator()

    services = generator.generate(

        EnterpriseGenerationConfig(),

    )

    high = [

        service

        for service in services

        if service.criticality == "High"

    ]

    assert len(high) == 5


def test_medium_service_count():

    generator = build_generator()

    services = generator.generate(

        EnterpriseGenerationConfig(),

    )

    medium = [

        service

        for service in services

        if service.criticality == "Medium"

    ]

    assert len(medium) == 3


# ==========================================================
# SLA / Availability
# ==========================================================

def test_sla_values():

    generator = build_generator()

    services = generator.generate(

        EnterpriseGenerationConfig(),

    )

    assert all(

        0 <= service.sla_percent <= 100

        for service in services

    )


def test_availability_values():

    generator = build_generator()

    services = generator.generate(

        EnterpriseGenerationConfig(),

    )

    assert all(

        0 <= service.availability_percent <= 100

        for service in services

    )


# ==========================================================
# Enterprise Metadata
# ==========================================================

def test_owner_populated():

    generator = build_generator()

    services = generator.generate(

        EnterpriseGenerationConfig(),

    )

    assert all(

        service.owner != ""

        for service in services

    )


def test_business_unit_populated():

    generator = build_generator()

    services = generator.generate(

        EnterpriseGenerationConfig(),

    )

    assert all(

        service.business_unit != ""

        for service in services

    )


def test_description_populated():

    generator = build_generator()

    services = generator.generate(

        EnterpriseGenerationConfig(),

    )

    assert all(

        service.description != ""

        for service in services

    )


# ==========================================================
# Lookup Helpers
# ==========================================================

def test_get_service():

    generator = build_generator()

    generator.generate(

        EnterpriseGenerationConfig(),

    )

    service = generator.get_service(

        "Corporate WAN"

    )

    assert service is not None

    assert service.service_name == "Corporate WAN"


def test_unknown_service():

    generator = build_generator()

    generator.generate(

        EnterpriseGenerationConfig(),

    )

    assert (

        generator.get_service(

            "Unknown Service"

        )

        is None

    )


def test_critical_services():

    generator = build_generator()

    generator.generate(

        EnterpriseGenerationConfig(),

    )

    critical = generator.critical_services()

    assert len(critical) == 4

    assert all(

        service.criticality == "Critical"

        for service in critical

    )


def test_high_priority_services():

    generator = build_generator()

    generator.generate(

        EnterpriseGenerationConfig(),

    )

    high = generator.high_priority_services()

    assert len(high) == 5

    assert all(

        service.criticality == "High"

        for service in high

    )
# ==========================================================
# Statistics
# ==========================================================

def test_statistics():

    generator = build_generator()

    generator.generate(

        EnterpriseGenerationConfig(),

    )

    stats = generator.statistics()

    assert stats["total_services"] == 12

    assert stats["critical"] == 4

    assert stats["high"] == 5

    assert stats["medium"] == 3


def test_statistics_consistency():

    generator = build_generator()

    generator.generate(

        EnterpriseGenerationConfig(),

    )

    stats = generator.statistics()

    assert (

        stats["critical"]

        + stats["high"]

        + stats["medium"]

        == stats["total_services"]

    )


# ==========================================================
# Reset
# ==========================================================

def test_reset():

    generator = build_generator()

    generator.generate(

        EnterpriseGenerationConfig(),

    )

    assert len(generator) == 12

    generator.reset()

    assert len(generator) == 0

    assert generator.generated_services == []


# ==========================================================
# Utility Methods
# ==========================================================

def test_len():

    generator = build_generator()

    generator.generate(

        EnterpriseGenerationConfig(),

    )

    assert len(generator) == 12


def test_repr():

    generator = build_generator()

    generator.generate(

        EnterpriseGenerationConfig(),

    )

    representation = repr(generator)

    assert "BusinessServiceGenerator" in representation

    assert "services=12" in representation

    assert "critical=4" in representation

    assert "high=5" in representation

    assert "medium=3" in representation


# ==========================================================
# Deterministic Generation
# ==========================================================

def test_generation_is_deterministic():

    generator = build_generator()

    first = generator.generate(

        EnterpriseGenerationConfig(),

    )

    names1 = [

        service.service_name

        for service in first

    ]

    second = generator.generate(

        EnterpriseGenerationConfig(),

    )

    names2 = [

        service.service_name

        for service in second

    ]

    assert names1 == names2


# ==========================================================
# Integrity
# ==========================================================

def test_service_names_unique():

    generator = build_generator()

    services = generator.generate(

        EnterpriseGenerationConfig(),

    )

    names = [

        service.service_name

        for service in services

    ]

    assert len(names) == len(

        set(names)

    )


def test_required_fields_populated():

    generator = build_generator()

    services = generator.generate(

        EnterpriseGenerationConfig(),

    )

    for service in services:

        assert service.service_name != ""

        assert service.owner != ""

        assert service.business_unit != ""

        assert service.criticality != ""

        assert service.description != ""


def test_dependency_list_initialized():

    generator = build_generator()

    services = generator.generate(

        EnterpriseGenerationConfig(),

    )

    assert all(

        isinstance(

            service.dependent_device_ids,

            list,

        )

        for service in services

    )


def test_default_availability():

    generator = build_generator()

    services = generator.generate(

        EnterpriseGenerationConfig(),

    )

    assert all(

        service.availability_percent == 100.0

        for service in services

    )