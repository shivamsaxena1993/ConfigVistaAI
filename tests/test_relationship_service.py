"""
=============================================================

ConfigVista AI

Relationship Service Tests

=============================================================
"""

from enterprise.models import (
    Device,
    Site,
    BusinessService,
)

from enterprise.services.inventory_service import (
    InventoryService,
)

from enterprise.services.relationship_service import (
    RelationshipService,
)


# ==========================================================
# Test Inventory Builder
# ==========================================================

def build_inventory():

    inventory = InventoryService()

    #
    # Site
    #

    site = Site(
        site_name="India Campus"
    )

    inventory.register_site(site)

    #
    # Business Service
    #

    service = BusinessService(
        service_name="SAP"
    )

    inventory.register_business_service(
        service
    )

    #
    # Devices
    #

    core = Device(
        hostname="CORE01"
    )

    distribution = Device(
        hostname="DIST01"
    )

    access = Device(
        hostname="ACCESS01"
    )

    #
    # Relationships
    #

    core.site_id = site.site_id
    distribution.site_id = site.site_id
    access.site_id = site.site_id

    core.add_business_service(service.service_id)

    distribution.add_business_service(
        service.service_id
    )

    inventory.register_device(core)
    inventory.register_device(distribution)
    inventory.register_device(access)

    return (
        inventory,
        site,
        service,
        core,
        distribution,
        access,
    )


# ==========================================================
# Constructor
# ==========================================================

def test_constructor():

    inventory, *_ = build_inventory()

    relationship = RelationshipService(
        inventory
    )

    assert relationship.relationships_built


def test_validate():

    inventory, *_ = build_inventory()

    relationship = RelationshipService(
        inventory
    )

    assert relationship.validate()


def test_rebuild():

    inventory, *_ = build_inventory()

    relationship = RelationshipService(
        inventory
    )

    relationship.rebuild()

    assert relationship.relationships_built

    assert relationship.validate()


# ==========================================================
# Device Lookup
# ==========================================================

def test_has_device():

    inventory, _, _, core, _, _ = build_inventory()

    relationship = RelationshipService(
        inventory
    )

    assert relationship.has_device(
        core.device_id
    )


def test_unknown_device():

    inventory, *_ = build_inventory()

    relationship = RelationshipService(
        inventory
    )

    assert not relationship.has_device(
        "UNKNOWN"
    )


def test_get_device():

    inventory, _, _, core, _, _ = build_inventory()

    relationship = RelationshipService(
        inventory
    )

    device = relationship.get_device(
        core.device_id
    )

    assert device.hostname == "CORE01"


# ==========================================================
# Site Lookup
# ==========================================================

def test_get_site():

    inventory, site, *_ = build_inventory()

    relationship = RelationshipService(
        inventory
    )

    result = relationship.get_site(
        site.site_id
    )

    assert result.site_id == site.site_id


def test_get_device_site():

    inventory, site, _, core, _, _ = build_inventory()

    relationship = RelationshipService(
        inventory
    )

    result = relationship.get_device_site(
        core.device_id
    )

    assert result.site_id == site.site_id


def test_site_devices():

    inventory, site, *_ = build_inventory()

    relationship = RelationshipService(
        inventory
    )

    devices = relationship.get_site_devices(
        site.site_id
    )

    assert len(devices) == 3

# ==========================================================
# Business Service Queries
# ==========================================================

def test_get_business_service():

    inventory, _, service, *_ = build_inventory()

    relationship = RelationshipService(
        inventory
    )

    result = relationship.get_business_service(
        service.service_id
    )

    assert result.service_id == service.service_id


def test_get_device_services():

    inventory, _, service, core, _, _ = build_inventory()

    relationship = RelationshipService(
        inventory
    )

    services = relationship.get_device_services(
        core.device_id
    )

    assert len(services) == 1

    assert (
        services[0].service_id
        == service.service_id
    )


def test_get_service_devices():

    inventory, _, service, *_ = build_inventory()

    relationship = RelationshipService(
        inventory
    )

    devices = relationship.get_service_devices(
        service.service_id
    )

    assert len(devices) == 2

    hostnames = {
        device.hostname
        for device in devices
    }

    assert "CORE01" in hostnames

    assert "DIST01" in hostnames


# ==========================================================
# Historical Changes
# ==========================================================

def test_device_changes_empty():

    inventory, _, _, core, _, _ = build_inventory()

    relationship = RelationshipService(
        inventory
    )

    changes = relationship.get_device_changes(
        core.device_id
    )

    assert changes == []


# ==========================================================
# Historical Incidents
# ==========================================================

def test_device_incidents_empty():

    inventory, _, _, core, _, _ = build_inventory()

    relationship = RelationshipService(
        inventory
    )

    incidents = relationship.get_device_incidents(
        core.device_id
    )

    assert incidents == []


# ==========================================================
# Relationship Summary
# ==========================================================

def test_relationship_summary():

    inventory, *_ = build_inventory()

    relationship = RelationshipService(
        inventory
    )

    summary = relationship.relationship_summary()

    assert summary.devices == 3

    assert summary.sites == 1

    assert summary.business_services == 1

    assert summary.changes == 0

    assert summary.incidents == 0


# ==========================================================
# Unknown Lookups
# ==========================================================

def test_unknown_site():

    inventory, *_ = build_inventory()

    relationship = RelationshipService(
        inventory
    )

    assert relationship.get_site(
        "UNKNOWN"
    ) is None


def test_unknown_business_service():

    inventory, *_ = build_inventory()

    relationship = RelationshipService(
        inventory
    )

    assert relationship.get_business_service(
        "UNKNOWN"
    ) is None


def test_unknown_device_site():

    inventory, *_ = build_inventory()

    relationship = RelationshipService(
        inventory
    )

    assert relationship.get_device_site(
        "UNKNOWN"
    ) is None


def test_unknown_device_services():

    inventory, *_ = build_inventory()

    relationship = RelationshipService(
        inventory
    )

    assert (
        relationship.get_device_services(
            "UNKNOWN"
        )
        == []
    )


def test_unknown_service_devices():

    inventory, *_ = build_inventory()

    relationship = RelationshipService(
        inventory
    )

    assert (
        relationship.get_service_devices(
            "UNKNOWN"
        )
        == []
    )


def test_unknown_device_changes():

    inventory, *_ = build_inventory()

    relationship = RelationshipService(
        inventory
    )

    assert (
        relationship.get_device_changes(
            "UNKNOWN"
        )
        == []
    )


def test_unknown_device_incidents():

    inventory, *_ = build_inventory()

    relationship = RelationshipService(
        inventory
    )

    assert (
        relationship.get_device_incidents(
            "UNKNOWN"
        )
        == []
    )
# ==========================================================
# Site Relationship Queries
# ==========================================================

def test_get_site_services():

    inventory, site, service, *_ = build_inventory()

    relationship = RelationshipService(
        inventory
    )

    services = relationship.get_site_services(
        site.site_id
    )

    assert len(services) == 1

    assert (
        services[0].service_id
        == service.service_id
    )


def test_get_site_changes():

    inventory, site, *_ = build_inventory()

    relationship = RelationshipService(
        inventory
    )

    changes = relationship.get_site_changes(
        site.site_id
    )

    assert changes == []


def test_get_site_incidents():

    inventory, site, *_ = build_inventory()

    relationship = RelationshipService(
        inventory
    )

    incidents = relationship.get_site_incidents(
        site.site_id
    )

    assert incidents == []


# ==========================================================
# Statistics
# ==========================================================

def test_statistics():

    inventory, *_ = build_inventory()

    relationship = RelationshipService(
        inventory
    )

    stats = relationship.statistics()

    assert stats["devices"] == 3

    assert stats["sites"] == 1

    assert stats["business_services"] == 1

    assert stats["changes"] == 0

    assert stats["incidents"] == 0

    assert stats["relationships_built"]


# ==========================================================
# Utility Methods
# ==========================================================

def test_len():

    inventory, *_ = build_inventory()

    relationship = RelationshipService(
        inventory
    )

    assert len(relationship) == 3


def test_repr():

    inventory, *_ = build_inventory()

    relationship = RelationshipService(
        inventory
    )

    representation = repr(
        relationship
    )

    assert "RelationshipService" in representation

    assert "devices=3" in representation


# ==========================================================
# Rebuild Consistency
# ==========================================================

def test_multiple_rebuilds():

    inventory, *_ = build_inventory()

    relationship = RelationshipService(
        inventory
    )

    relationship.rebuild()

    relationship.rebuild()

    relationship.rebuild()

    assert relationship.validate()

    assert len(relationship) == 3


def test_rebuild_preserves_statistics():

    inventory, *_ = build_inventory()

    relationship = RelationshipService(
        inventory
    )

    before = relationship.statistics()

    relationship.rebuild()

    after = relationship.statistics()

    assert before == after


# ==========================================================
# Empty Inventory
# ==========================================================

def test_empty_inventory():

    inventory = InventoryService()

    relationship = RelationshipService(
        inventory
    )

    assert relationship.validate()

    assert len(relationship) == 0

    stats = relationship.statistics()

    assert stats["devices"] == 0

    assert stats["sites"] == 0

    assert stats["business_services"] == 0

    assert stats["changes"] == 0

    assert stats["incidents"] == 0


# ==========================================================
# Stability
# ==========================================================

def test_relationship_build_flag():

    inventory, *_ = build_inventory()

    relationship = RelationshipService(
        inventory
    )

    assert relationship.relationships_built


def test_relationship_summary_after_rebuild():

    inventory, *_ = build_inventory()

    relationship = RelationshipService(
        inventory
    )

    before = relationship.relationship_summary()

    relationship.rebuild()

    after = relationship.relationship_summary()

    assert before.devices == after.devices

    assert before.sites == after.sites

    assert (
        before.business_services
        == after.business_services
    )

    assert before.changes == after.changes

    assert before.incidents == after.incidents


# ==========================================================
# Unknown Site Queries
# ==========================================================

def test_unknown_site_services():

    inventory, *_ = build_inventory()

    relationship = RelationshipService(
        inventory
    )

    assert relationship.get_site_services(
        "UNKNOWN"
    ) == []


def test_unknown_site_changes():

    inventory, *_ = build_inventory()

    relationship = RelationshipService(
        inventory
    )

    assert relationship.get_site_changes(
        "UNKNOWN"
    ) == []


def test_unknown_site_incidents():

    inventory, *_ = build_inventory()

    relationship = RelationshipService(
        inventory
    )

    assert relationship.get_site_incidents(
        "UNKNOWN"
    ) == []