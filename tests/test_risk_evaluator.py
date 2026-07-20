"""
tests/test_risk_evaluator.py

Unit tests for RiskEvaluator.

Author : Shivam Saxena
Project : ConfigVista AI
"""

from comparison.risk_evaluator import RiskEvaluator
from comparison.models import (
    ConfigurationChange,
    ChangeCategory,
    ChangeType,
    RiskLevel,
)


risk_evaluator = RiskEvaluator()


# ==========================================================
# INTERFACE
# ==========================================================

def test_interface_risk():

    change = ConfigurationChange(
        change_type=ChangeType.MODIFIED,
        category=ChangeCategory.INTERFACE,
        parent_section="interface GigabitEthernet0/0",
        new_value=" ip address 10.1.2.1 255.255.255.0",
    )

    risk_evaluator.evaluate([change])

    assert change.risk_level == RiskLevel.LOW
    assert change.risk_weight == 30
    assert change.confidence_score == 90

    print("✓ test_interface_risk PASSED")


# ==========================================================
# ROUTING
# ==========================================================

def test_routing_risk():

    change = ConfigurationChange(
        change_type=ChangeType.MODIFIED,
        category=ChangeCategory.ROUTING,
        parent_section="router ospf 1",
        new_value=" network 10.1.2.0 0.0.0.255 area 0",
    )

    risk_evaluator.evaluate([change])

    assert change.risk_level == RiskLevel.HIGH
    assert change.risk_weight >= 90

    print("✓ test_routing_risk PASSED")


# ==========================================================
# SECURITY
# ==========================================================

def test_security_risk():

    change = ConfigurationChange(
        change_type=ChangeType.MODIFIED,
        category=ChangeCategory.SECURITY,
        parent_section="ip access-list standard MGMT",
        new_value=" permit 192.168.2.0 0.0.0.255",
    )

    risk_evaluator.evaluate([change])

    assert change.risk_level == RiskLevel.HIGH
    assert change.risk_weight >= 90

    print("✓ test_security_risk PASSED")


# ==========================================================
# SERVICES
# ==========================================================

def test_services_risk():

    change = ConfigurationChange(
        change_type=ChangeType.MODIFIED,
        category=ChangeCategory.SERVICES,
        parent_section="ntp server 10.20.20.20",
        new_value="ntp server 10.20.20.20",
    )

    risk_evaluator.evaluate([change])

    assert change.risk_level == RiskLevel.MEDIUM
    assert change.risk_weight == 60

    print("✓ test_services_risk PASSED")


# ==========================================================
# SHUTDOWN OVERRIDE
# ==========================================================

def test_shutdown_override():

    change = ConfigurationChange(
        change_type=ChangeType.MODIFIED,
        category=ChangeCategory.INTERFACE,
        parent_section="interface GigabitEthernet0/1",
        new_value=" shutdown",
    )

    risk_evaluator.evaluate([change])

    assert change.risk_level == RiskLevel.MEDIUM
    assert change.risk_weight >= 60

    print("✓ test_shutdown_override PASSED")


# ==========================================================
# DEFAULT ROUTE
# ==========================================================

def test_default_route_override():

    change = ConfigurationChange(
        change_type=ChangeType.MODIFIED,
        category=ChangeCategory.ROUTING,
        parent_section="ip route",
        new_value="ip route 0.0.0.0 0.0.0.0 10.1.1.1",
    )

    risk_evaluator.evaluate([change])

    assert change.risk_level == RiskLevel.HIGH
    assert change.risk_weight == 95

    print("✓ test_default_route_override PASSED")


# ==========================================================
# BGP
# ==========================================================

def test_bgp_override():

    change = ConfigurationChange(
        change_type=ChangeType.MODIFIED,
        category=ChangeCategory.ROUTING,
        parent_section="router bgp 65000",
        new_value=" neighbor 1.1.1.1 remote-as 65001",
    )

    risk_evaluator.evaluate([change])

    assert change.risk_level == RiskLevel.HIGH
    assert change.risk_weight == 95

    print("✓ test_bgp_override PASSED")


# ==========================================================
# UNKNOWN
# ==========================================================

def test_unknown_risk():

    change = ConfigurationChange(
        change_type=ChangeType.MODIFIED,
        category=ChangeCategory.UNKNOWN,
        parent_section="custom feature",
        new_value=" proprietary command",
    )

    risk_evaluator.evaluate([change])

    assert change.risk_level == RiskLevel.UNKNOWN
    assert change.risk_weight == 0

    print("✓ test_unknown_risk PASSED")


# ==========================================================
# OVERALL RISK
# ==========================================================

def test_overall_risk():

    changes = [

        ConfigurationChange(
            change_type=ChangeType.MODIFIED,
            category=ChangeCategory.INTERFACE,
            risk_level=RiskLevel.LOW,
            risk_weight=30,
        ),

        ConfigurationChange(
            change_type=ChangeType.MODIFIED,
            category=ChangeCategory.ROUTING,
            risk_level=RiskLevel.HIGH,
            risk_weight=90,
        ),

    ]

    overall = risk_evaluator.overall_risk(changes)

    assert overall == RiskLevel.HIGH

    print("✓ test_overall_risk PASSED")


# ==========================================================
# AVERAGE RISK SCORE
# ==========================================================

def test_average_risk_score():

    changes = [

        ConfigurationChange(
            change_type=ChangeType.MODIFIED,
            category=ChangeCategory.INTERFACE,
            risk_weight=30,
        ),

        ConfigurationChange(
            change_type=ChangeType.MODIFIED,
            category=ChangeCategory.ROUTING,
            risk_weight=90,
        ),

    ]

    score = risk_evaluator.risk_score(changes)

    assert score == 60.0

    print("✓ test_average_risk_score PASSED")


# ==========================================================
# RECOMMENDATION
# ==========================================================

def test_recommendation_generated():

    change = ConfigurationChange(
        change_type=ChangeType.MODIFIED,
        category=ChangeCategory.ROUTING,
        parent_section="router ospf 1",
        new_value=" network 10.1.2.0 0.0.0.255 area 0",
    )

    risk_evaluator.evaluate([change])

    assert change.recommendation != ""

    print("✓ test_recommendation_generated PASSED")


# ==========================================================
# RUNNER
# ==========================================================

def run_all_tests():

    print("=" * 60)
    print("Running RiskEvaluator Unit Tests")
    print("=" * 60)

    test_interface_risk()
    test_routing_risk()
    test_security_risk()
    test_services_risk()
    test_shutdown_override()
    test_default_route_override()
    test_bgp_override()
    test_unknown_risk()
    test_overall_risk()
    test_average_risk_score()
    test_recommendation_generated()

    print("=" * 60)
    print("All RiskEvaluator tests PASSED")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()