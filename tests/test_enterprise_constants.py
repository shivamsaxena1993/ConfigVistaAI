"""
=============================================================
ConfigVista AI

Unit Tests
Enterprise Constants

Artifact-2
=============================================================
"""

import pytest

from enterprise.constants import *


# ============================================================
# Enterprise Metadata
# ============================================================

def test_enterprise_metadata():

    assert ENTERPRISE_NAME == "ConfigVista Enterprise Lab"
    assert INDUSTRY == "Manufacturing"
    assert COUNTRY == "India"
    assert TIMEZONE == "Asia/Kolkata"


# ============================================================
# Enterprise Scale
# ============================================================

def test_enterprise_scale():

    assert TOTAL_DATA_CENTERS == 1
    assert TOTAL_BRANCHES == 10
    assert TOTAL_SITES == 11
    assert TOTAL_DEVICES == 31


# ============================================================
# Random Seed
# ============================================================

def test_random_seed():

    assert RANDOM_SEED == 42


# ============================================================
# Device Roles
# ============================================================

def test_device_roles():

    assert len(DeviceRole) == 9

    assert DeviceRole.CORE_ROUTER.value == "CORE_ROUTER"
    assert DeviceRole.ACCESS_SWITCH.value == "ACCESS_SWITCH"
    assert DeviceRole.FIREWALL.value == "FIREWALL"


# ============================================================
# Site Types
# ============================================================

def test_site_types():

    assert SiteType.DATA_CENTER.value == "DATA_CENTER"
    assert SiteType.MANUFACTURING.value == "MANUFACTURING"
    assert SiteType.WAREHOUSE.value == "WAREHOUSE"


# ============================================================
# Platform Mapping
# ============================================================

def test_platform_mapping_complete():

    assert len(DEVICE_PLATFORM) == len(DeviceRole)

    for role in DeviceRole:
        assert role in DEVICE_PLATFORM
        assert DEVICE_PLATFORM[role] != ""


# ============================================================
# Vendor Mapping
# ============================================================

def test_vendor_mapping_complete():

    assert len(DEVICE_VENDOR) == len(DeviceRole)

    for role in DeviceRole:
        assert role in DEVICE_VENDOR


# ============================================================
# Operating System Mapping
# ============================================================

def test_os_mapping_complete():

    assert len(OS_VERSION) == len(DeviceRole)

    for role in DeviceRole:
        assert role in OS_VERSION


# ============================================================
# Criticality Mapping
# ============================================================

def test_criticality_mapping_complete():

    assert len(DEVICE_CRITICALITY) == len(DeviceRole)

    for role in DeviceRole:
        assert role in DEVICE_CRITICALITY


# ============================================================
# Business Services
# ============================================================

def test_business_services():

    assert len(BUSINESS_SERVICES) >= 10

    assert "ERP" in BUSINESS_SERVICES
    assert "DNS" in BUSINESS_SERVICES
    assert "DHCP" in BUSINESS_SERVICES
    assert "Email" in BUSINESS_SERVICES


# ============================================================
# Site Inventory
# ============================================================

def test_site_codes():

    assert len(SITE_CODES) == 11

    assert SITE_CODES[0] == "DC01"
    assert SITE_CODES[-1] == "BR10"


# ============================================================
# Default Operational Values
# ============================================================

def test_operational_defaults():

    assert DEFAULT_CPU >= 0
    assert DEFAULT_MEMORY >= 0
    assert DEFAULT_HEALTH_SCORE == 100
    assert DEFAULT_MTU == 1500


# ============================================================
# Dataset Targets
# ============================================================

def test_dataset_targets():

    assert TARGET_CHANGE_RECORDS >= 1000
    assert TARGET_INCIDENT_RECORDS >= 100
    assert TARGET_CONFIGURATION_SNAPSHOTS >= 100


# ============================================================
# Role Supported Domains
# ============================================================

def test_role_supported_domains():

    assert len(ROLE_SUPPORTED_DOMAINS) == len(DeviceRole)

    assert "ROUTING" in ROLE_SUPPORTED_DOMAINS[
        DeviceRole.CORE_ROUTER
    ]

    assert "SECURITY" in ROLE_SUPPORTED_DOMAINS[
        DeviceRole.FIREWALL
    ]


# ============================================================
# Routing Protocol Catalog
# ============================================================

def test_role_routing_protocols():

    assert RoutingProtocol.BGP in ROLE_ROUTING_PROTOCOLS[
        DeviceRole.CORE_ROUTER
    ]

    assert ROLE_ROUTING_PROTOCOLS[
        DeviceRole.ACCESS_SWITCH
    ] == []


# ============================================================
# Interface Templates
# ============================================================

def test_interface_templates():

    assert len(ROLE_INTERFACE_TEMPLATE) == len(DeviceRole)

    assert ROLE_INTERFACE_TEMPLATE[
        DeviceRole.ACCESS_SWITCH
    ]["physical"] == 48

    assert ROLE_INTERFACE_TEMPLATE[
        DeviceRole.BRANCH_ROUTER
    ]["loopback"] == 1


# ============================================================
# Change Type Catalog
# ============================================================

def test_role_change_types():

    assert "Routing" in ROLE_CHANGE_TYPES[
        DeviceRole.CORE_ROUTER
    ]

    assert "ACL" in ROLE_CHANGE_TYPES[
        DeviceRole.FIREWALL
    ]


# ============================================================
# Dependent Services
# ============================================================

def test_role_dependent_services():

    assert "ERP" in ROLE_DEPENDENT_SERVICES[
        DeviceRole.CORE_ROUTER
    ]

    assert "DNS" in ROLE_DEPENDENT_SERVICES[
        DeviceRole.DNS_SERVER
    ]


# ============================================================
# Monitored Metrics
# ============================================================

def test_role_monitored_metrics():

    assert "CPU" in ROLE_MONITORED_METRICS[
        DeviceRole.CORE_ROUTER
    ]

    assert "Memory" in ROLE_MONITORED_METRICS[
        DeviceRole.FIREWALL
    ]


# ============================================================
# ML Split Validation
# ============================================================

def test_ml_split():

    total = (
        ML_TRAIN_SPLIT +
        ML_VALIDATION_SPLIT +
        ML_TEST_SPLIT
    )

    assert total == pytest.approx(1.0)


# ============================================================
# Enterprise Completeness
# ============================================================

def test_all_roles_have_complete_catalogs():

    for role in DeviceRole:

        assert role in DEVICE_PLATFORM
        assert role in DEVICE_VENDOR
        assert role in OS_VERSION
        assert role in DEVICE_CRITICALITY
        assert role in ROLE_SUPPORTED_DOMAINS
        assert role in ROLE_ROUTING_PROTOCOLS
        assert role in ROLE_INTERFACE_TEMPLATE