"""
tests/test_diff_engine.py

Unit tests for DiffEngine.

Author : Shivam Saxena
Project : ConfigVista AI
"""

from comparison.diff_engine import DiffEngine
from comparison.models import ChangeType


def test_modified_interface_ip():

    baseline = [
        "hostname Branch-R1",
        "interface GigabitEthernet0/0",
        " description WAN",
        " ip address 10.1.1.1 255.255.255.0",
    ]

    candidate = [
        "hostname Branch-R1",
        "interface GigabitEthernet0/0",
        " description WAN",
        " ip address 10.1.2.1 255.255.255.0",
    ]

    engine = DiffEngine()

    changes = engine.compare(baseline, candidate)

    assert len(changes) == 1

    change = changes[0]

    assert change.change_type == ChangeType.MODIFIED
    assert change.parent_section == "interface GigabitEthernet0/0"
    assert change.parent_type == "interface"
    assert "10.1.1.1" in change.old_value
    assert "10.1.2.1" in change.new_value

    print("✓ test_modified_interface_ip PASSED")


def test_added_interface():

    baseline = [
        "hostname Branch-R1",
    ]

    candidate = [
        "hostname Branch-R1",
        "interface GigabitEthernet0/1",
        " description Backup WAN",
        " ip address 172.16.1.1 255.255.255.0",
    ]

    engine = DiffEngine()

    changes = engine.compare(baseline, candidate)

    assert len(changes) == 3

    assert all(
        c.change_type == ChangeType.ADDED
        for c in changes
    )

    assert changes[0].parent_section == "interface GigabitEthernet0/1"

    print("✓ test_added_interface PASSED")


def test_removed_acl():

    baseline = [
        "ip access-list standard MGMT",
        " permit 192.168.1.0 0.0.0.255",
    ]

    candidate = []

    engine = DiffEngine()

    changes = engine.compare(baseline, candidate)

    assert len(changes) == 2

    assert all(
        c.change_type == ChangeType.REMOVED
        for c in changes
    )

    assert changes[1].parent_section == "ip access-list standard MGMT"

    print("✓ test_removed_acl PASSED")


def test_parent_mapping():

    baseline = [
        "router ospf 1",
        " network 10.1.1.0 0.0.0.255 area 0",
    ]

    candidate = [
        "router ospf 1",
        " network 10.2.2.0 0.0.0.255 area 0",
    ]

    engine = DiffEngine()

    changes = engine.compare(baseline, candidate)

    assert len(changes) == 1

    change = changes[0]
    
    assert change.parent_section == "router ospf 1"
    assert change.parent_type == "ospf"

    print("✓ test_parent_mapping PASSED")


def test_no_changes():

    config = [
        "hostname Branch-R1",
        "interface GigabitEthernet0/0",
        " description WAN",
        " ip address 10.1.1.1 255.255.255.0",
    ]

    engine = DiffEngine()

    changes = engine.compare(config, config)

    assert len(changes) == 0

    print("✓ test_no_changes PASSED")


def run_all_tests():

    print("=" * 60)
    print("Running DiffEngine Unit Tests")
    print("=" * 60)

    test_modified_interface_ip()
    test_added_interface()
    test_removed_acl()
    test_parent_mapping()
    test_no_changes()

    print("=" * 60)
    print("All DiffEngine tests PASSED")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()