"""
=============================================================

ConfigVista AI

Enterprise Generator Tests

=============================================================
"""

from enterprise.generators.enterprise_generator import (
    EnterpriseGenerator,
    EnterpriseGenerationConfig,
    GenerationStatistics,
)

from enterprise.services.inventory_service import (
    InventoryService,
)

from enterprise.models import (
    Site,
    BusinessService,
    Device,
)


# ==========================================================
# Mock Generators
# ==========================================================

class MockSiteGenerator:

    def generate(self, config):

        return [

            Site(site_name="DC-01"),

            Site(site_name="Branch-01"),

        ]


class MockBusinessServiceGenerator:

    def generate(self, config):

        return [

            BusinessService(
                service_name="SAP"
            ),

            BusinessService(
                service_name="Voice"
            ),

        ]


class MockDeviceGenerator:

    def generate(

        self,

        config,

        sites,

        services,

    ):

        devices = []

        for index in range(3):

            device = Device(

                hostname=f"DEVICE-{index}"

            )

            device.site_id = sites[0].site_id

            device.add_business_service(

                services[0].service_id

            )

            devices.append(device)

        return devices


class MockTopologyGenerator:

    def generate(

        self,

        config,

        devices,

    ):

        return []


class MockChangeGenerator:

    def generate(

        self,

        config,

        devices,

    ):

        return []


class MockIncidentGenerator:

    def generate(

        self,

        config,

        devices,

    ):

        return []


class MockConfigurationGenerator:

    def generate(

        self,

        config,

        devices,

    ):

        return []


class MockOperationalGenerator:

    def generate(

        self,

        config,

        devices,

    ):

        return []


# ==========================================================
# Helper
# ==========================================================

def build_generator():

    generator = EnterpriseGenerator(

        inventory=InventoryService()

    )

    generator.register_site_generator(

        MockSiteGenerator()

    )

    generator.register_business_service_generator(

        MockBusinessServiceGenerator()

    )

    generator.register_device_generator(

        MockDeviceGenerator()

    )

    generator.register_topology_generator(

        MockTopologyGenerator()

    )

    generator.register_change_generator(

        MockChangeGenerator()

    )

    generator.register_incident_generator(

        MockIncidentGenerator()

    )

    generator.register_configuration_generator(

        MockConfigurationGenerator()

    )

    generator.register_operational_generator(

        MockOperationalGenerator()

    )

    return generator


# ==========================================================
# Constructor
# ==========================================================

def test_constructor():

    generator = EnterpriseGenerator()

    assert isinstance(

        generator.config,

        EnterpriseGenerationConfig,

    )

    assert isinstance(

        generator.statistics,

        GenerationStatistics,

    )

    assert isinstance(

        generator.inventory,

        InventoryService,

    )


def test_default_configuration():

    config = EnterpriseGenerationConfig()

    assert config.data_centers == 2

    assert config.branch_sites == 30

    assert config.historical_changes == 300

    assert config.operational_snapshots == 300


def test_statistics_defaults():

    stats = GenerationStatistics()

    assert stats.sites == 0

    assert stats.devices == 0

    assert stats.completed is False


# ==========================================================
# Registration
# ==========================================================

def test_register_generators():

    generator = build_generator()

    assert generator.site_generator is not None

    assert generator.device_generator is not None

    assert generator.topology_generator is not None

    assert generator.incident_generator is not None


def test_validate_generators():

    generator = build_generator()

    generator.validate_generators()

# ==========================================================
# Enterprise Generation
# ==========================================================

def test_generate():

    generator = build_generator()

    inventory = generator.generate()

    assert inventory is generator.inventory

    assert generator.statistics.completed


def test_generated_sites():

    generator = build_generator()

    generator.generate()

    assert len(

        generator.inventory.sites

    ) == 2

    assert generator.statistics.sites == 2


def test_generated_business_services():

    generator = build_generator()

    generator.generate()

    assert len(

        generator.inventory.business_services

    ) == 2

    assert (

        generator.statistics.business_services

        == 2

    )


def test_generated_devices():

    generator = build_generator()

    generator.generate()

    assert len(

        generator.inventory.devices

    ) == 3

    assert generator.statistics.devices == 3


def test_generated_topology():

    generator = build_generator()

    generator.generate()

    assert len(

        generator.inventory.topology_links

    ) == 0

    assert (

        generator.statistics.topology_links

        == 0

    )


def test_generated_changes():

    generator = build_generator()

    generator.generate()

    assert len(

        generator.inventory.changes

    ) == 0

    assert generator.statistics.changes == 0


def test_generated_incidents():

    generator = build_generator()

    generator.generate()

    assert len(

        generator.inventory.incidents

    ) == 0

    assert generator.statistics.incidents == 0


def test_generated_configuration_backups():

    generator = build_generator()

    generator.generate()

    assert len(

        generator.inventory.configuration_backups

    ) == 0

    assert (

        generator.statistics.configuration_backups

        == 0

    )


def test_generated_operational_snapshots():

    generator = build_generator()

    generator.generate()

    assert len(

        generator.inventory.operational_snapshots

    ) == 0

    assert (

        generator.statistics.operational_snapshots

        == 0

    )


# ==========================================================
# Statistics
# ==========================================================

def test_generation_statistics():

    generator = build_generator()

    generator.generate()

    stats = generator.generation_statistics()

    assert stats.sites == 2

    assert stats.business_services == 2

    assert stats.devices == 3

    assert stats.completed


def test_summary():

    generator = build_generator()

    generator.generate()

    summary = generator.summary()

    assert summary["sites"] == 2

    assert summary["business_services"] == 2

    assert summary["devices"] == 3

    assert summary["completed"]


# ==========================================================
# Inventory Validation
# ==========================================================

def test_inventory_contains_site():

    generator = build_generator()

    generator.generate()

    site = next(

        iter(

            generator.inventory.sites.values()

        )

    )

    assert site.site_name != ""


def test_inventory_contains_device():

    generator = build_generator()

    generator.generate()

    device = next(

        iter(

            generator.inventory.devices.values()

        )

    )

    assert device.hostname.startswith(

        "DEVICE-"

    )


def test_inventory_contains_service():

    generator = build_generator()

    generator.generate()

    service = next(

        iter(

            generator.inventory.business_services.values()

        )

    )

    assert service.service_name in (

        "SAP",

        "Voice",

    )

# ==========================================================
# Reset
# ==========================================================

def test_reset():

    generator = build_generator()

    generator.generate()

    generator.reset()

    assert len(

        generator.inventory.devices

    ) == 0

    assert generator.statistics.devices == 0

    assert not generator.statistics.completed


def test_reset_statistics():

    generator = build_generator()

    generator.generate()

    generator.reset()

    stats = generator.generation_statistics()

    assert stats.sites == 0

    assert stats.business_services == 0

    assert stats.devices == 0

    assert stats.topology_links == 0

    assert stats.changes == 0

    assert stats.incidents == 0


# ==========================================================
# Validation
# ==========================================================

import pytest


def test_missing_generators():

    generator = EnterpriseGenerator()

    with pytest.raises(RuntimeError):

        generator.generate()


# ==========================================================
# Utility Methods
# ==========================================================

def test_len():

    generator = build_generator()

    generator.generate()

    assert len(generator) == 3


def test_repr():

    generator = build_generator()

    generator.generate()

    representation = repr(generator)

    assert "EnterpriseGenerator" in representation

    assert "devices=3" in representation

    assert "completed=True" in representation


# ==========================================================
# Multiple Generation
# ==========================================================

def test_multiple_generation_runs():

    generator = build_generator()

    generator.generate()

    first = generator.summary()

    generator.reset()

    generator = build_generator()

    generator.generate()

    second = generator.summary()

    assert first == second


# ==========================================================
# Configuration Injection
# ==========================================================

def test_custom_configuration():

    config = EnterpriseGenerationConfig(

        data_centers=1,

        branch_sites=5,

        historical_changes=50,

    )

    generator = EnterpriseGenerator(

        config=config

    )

    assert generator.config.data_centers == 1

    assert generator.config.branch_sites == 5

    assert generator.config.historical_changes == 50


# ==========================================================
# Statistics Consistency
# ==========================================================

def test_statistics_summary_consistency():

    generator = build_generator()

    generator.generate()

    stats = generator.generation_statistics()

    summary = generator.summary()

    assert stats.sites == summary["sites"]

    assert (

        stats.business_services

        == summary["business_services"]

    )

    assert stats.devices == summary["devices"]


# ==========================================================
# Inventory Consistency
# ==========================================================

def test_inventory_statistics_match():

    generator = build_generator()

    generator.generate()

    assert (

        len(generator.inventory.devices)

        == generator.statistics.devices

    )

    assert (

        len(generator.inventory.sites)

        == generator.statistics.sites

    )

    assert (

        len(generator.inventory.business_services)

        == generator.statistics.business_services

    )