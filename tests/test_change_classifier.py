"""
tests/test_change_classifier.py

Unit tests for ChangeClassifier.

Author : Shivam Saxena
Project : ConfigVista AI
"""

from comparison.change_classifier import ChangeClassifier
from comparison.models import (
    ChangeCategory,
    ChangeType,
    ConfigurationChange,
)


classifier = ChangeClassifier()


# ==========================================================
# INTERFACE
# ==========================================================

def test_interface_classification():

    change = ConfigurationChange(
        change_type=ChangeType.MODIFIED,
        parent_section="interface GigabitEthernet0/0",
        parent_type="interface",
        new_value=" ip address 10.1.2.1 255.255.255.0",
    )

    classifier.classify([change])

    assert change.category == ChangeCategory.INTERFACE
    assert change.section == "interface GigabitEthernet0/0"

    print("✓ test_interface_classification PASSED")


# ==========================================================
# ROUTING
# ==========================================================

def test_routing_classification():

    change = ConfigurationChange(
        change_type=ChangeType.MODIFIED,
        parent_section="router ospf 1",
        parent_type="router",
        new_value=" network 10.1.2.0 0.0.0.255 area 0",
    )

    classifier.classify([change])

    assert change.category == ChangeCategory.ROUTING
    assert change.section == "router ospf 1"

    print("✓ test_routing_classification PASSED")


# ==========================================================
# SECURITY
# ==========================================================

def test_security_classification():

    change = ConfigurationChange(
        change_type=ChangeType.MODIFIED,
        parent_section="ip access-list standard MGMT",
        parent_type="ip",
        new_value=" permit 192.168.2.0 0.0.0.255",
    )

    classifier.classify([change])

    assert change.category == ChangeCategory.SECURITY
    assert change.section == "ip access-list standard MGMT"

    print("✓ test_security_classification PASSED")


# ==========================================================
# SERVICES
# ==========================================================

def test_services_classification():

    change = ConfigurationChange(
        change_type=ChangeType.MODIFIED,
        parent_section="ntp server 10.20.20.20",
        parent_type="ntp",
        new_value="ntp server 10.20.20.20",
    )

    classifier.classify([change])

    assert change.category == ChangeCategory.SERVICES

    print("✓ test_services_classification PASSED")


# ==========================================================
# SWITCHING
# ==========================================================

def test_switching_classification():

    change = ConfigurationChange(
        change_type=ChangeType.ADDED,
        parent_section="vlan 100",
        parent_type="vlan",
        new_value=" name USERS",
    )

    classifier.classify([change])

    assert change.category == ChangeCategory.SWITCHING

    print("✓ test_switching_classification PASSED")


# ==========================================================
# MANAGEMENT
# ==========================================================

def test_management_classification():

    change = ConfigurationChange(
        change_type=ChangeType.MODIFIED,
        parent_section="hostname Branch-R2",
        parent_type="hostname",
        new_value="hostname Branch-R2",
    )

    classifier.classify([change])

    assert change.category == ChangeCategory.MANAGEMENT

    print("✓ test_management_classification PASSED")


# ==========================================================
# SYSTEM
# ==========================================================

def test_system_classification():

    change = ConfigurationChange(
        change_type=ChangeType.MODIFIED,
        parent_section="boot system flash:c800.bin",
        parent_type="boot",
        new_value="boot system flash:c800.bin",
    )

    classifier.classify([change])

    assert change.category == ChangeCategory.SYSTEM

    print("✓ test_system_classification PASSED")


# ==========================================================
# UNKNOWN
# ==========================================================

def test_unknown_classification():

    change = ConfigurationChange(
        change_type=ChangeType.MODIFIED,
        parent_section="custom feature xyz",
        parent_type="custom",
        new_value="my proprietary command",
    )

    classifier.classify([change])

    assert change.category == ChangeCategory.UNKNOWN

    print("✓ test_unknown_classification PASSED")


# ==========================================================
# DESCRIPTION
# ==========================================================

def test_description_generation():

    change = ConfigurationChange(
        change_type=ChangeType.MODIFIED,
        parent_section="router ospf 1",
        parent_type="router",
        new_value=" network 10.1.2.0 0.0.0.255 area 0",
    )

    classifier.classify([change])

    assert "Routing" in change.description
    assert "router ospf 1" in change.description

    print("✓ test_description_generation PASSED")


# ==========================================================
# RUNNER
# ==========================================================

def run_all_tests():

    print("=" * 60)
    print("Running ChangeClassifier Unit Tests")
    print("=" * 60)

    test_interface_classification()
    test_routing_classification()
    test_security_classification()
    test_services_classification()
    test_switching_classification()
    test_management_classification()
    test_system_classification()
    test_unknown_classification()
    test_description_generation()

    print("=" * 60)
    print("All ChangeClassifier tests PASSED")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()