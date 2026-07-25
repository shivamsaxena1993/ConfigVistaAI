"""
tests/test_pipeline.py

End-to-End Artifact-1 Pipeline Tests

Validates the active ConfigVista AI workflow using dynamically
created Cisco IOS configuration files.

Pipeline:

Raw Configuration
        ↓
Configuration Files
        ↓
ComparisonEngine
        ↓
Normalization / Context Mapping
        ↓
Diff Detection
        ↓
Change Classification
        ↓
Rule-Based Risk Evaluation
        ↓
ComparisonResult

Project: ConfigVista AI
"""

from pathlib import Path

import pytest

from comparison.comparison_engine import ComparisonEngine
from comparison.models import (
    ChangeCategory,
    ChangeType,
    ComparisonResult,
    RiskLevel,
)


# ==========================================================
# TEST CONFIGURATIONS
# ==========================================================

BASELINE_CONFIG = """
hostname Branch-RTR01
!
interface GigabitEthernet0/0
 description WAN Uplink
 ip address 10.10.10.1 255.255.255.0
 no shutdown
!
interface GigabitEthernet0/1
 description LAN
 ip address 192.168.10.1 255.255.255.0
 no shutdown
!
router ospf 10
 network 192.168.10.0 0.0.0.255 area 0
!
ip access-list extended BRANCH-IN
 permit tcp any host 192.168.10.10 eq 443
!
logging host 192.168.10.20
!
end
"""


CANDIDATE_CONFIG = """
hostname Branch-RTR01
!
interface GigabitEthernet0/0
 description WAN Uplink
 ip address 10.10.20.1 255.255.255.0
 no shutdown
!
interface GigabitEthernet0/1
 description LAN
 ip address 192.168.10.1 255.255.255.0
 no shutdown
!
router ospf 10
 network 192.168.10.0 0.0.0.255 area 0
 network 10.10.20.0 0.0.0.255 area 0
!
ip access-list extended BRANCH-IN
 permit tcp any host 192.168.10.10 eq 443
 deny ip any any
!
logging host 192.168.10.20
!
ntp server 192.168.10.30
!
end
"""


# ==========================================================
# FIXTURE
# ==========================================================

@pytest.fixture(scope="module")
def pipeline_result(tmp_path_factory) -> ComparisonResult:
    """
    Create temporary Cisco configurations and execute
    the complete Artifact-1 assessment pipeline.
    """

    temp_dir = tmp_path_factory.mktemp(
        "configvista_pipeline"
    )

    baseline_path = temp_dir / "baseline.cfg"
    candidate_path = temp_dir / "candidate.cfg"

    baseline_path.write_text(
        BASELINE_CONFIG,
        encoding="utf-8",
    )

    candidate_path.write_text(
        CANDIDATE_CONFIG,
        encoding="utf-8",
    )

    engine = ComparisonEngine()

    return engine.compare(
        str(baseline_path),
        str(candidate_path),
        export_csv=False,
    )


# ==========================================================
# END-TO-END TESTS
# ==========================================================

def test_pipeline_returns_comparison_result(
    pipeline_result,
):
    assert isinstance(
        pipeline_result,
        ComparisonResult,
    )


def test_pipeline_identifies_devices(
    pipeline_result,
):
    assert (
        pipeline_result.baseline_hostname
        == "Branch-RTR01"
    )

    assert (
        pipeline_result.candidate_hostname
        == "Branch-RTR01"
    )


def test_pipeline_detects_changes(
    pipeline_result,
):
    assert pipeline_result.statistics.total_changes > 0

    assert (
        pipeline_result.statistics.total_changes
        == len(pipeline_result.changes)
    )


def test_pipeline_detects_expected_change_types(
    pipeline_result,
):
    change_types = {
        change.change_type
        for change in pipeline_result.changes
    }

    assert ChangeType.ADDED in change_types

    assert (
        ChangeType.MODIFIED in change_types
        or ChangeType.REMOVED in change_types
    )


def test_pipeline_classifies_changes(
    pipeline_result,
):
    categories = {
        change.category
        for change in pipeline_result.changes
    }

    assert categories

    assert any(
        category != ChangeCategory.UNKNOWN
        for category in categories
    )


def test_pipeline_generates_risk_assessment(
    pipeline_result,
):
    assert pipeline_result.overall_risk in {
        RiskLevel.LOW,
        RiskLevel.MEDIUM,
        RiskLevel.HIGH,
        RiskLevel.UNKNOWN,
    }

    assert (
        0.0
        <= pipeline_result.average_risk_score
        <= 100.0
    )

    assert (
        0.0
        <= pipeline_result.average_rule_confidence
        <= 100.0
    )


def test_pipeline_generates_recommendation(
    pipeline_result,
):
    assert (
        pipeline_result.deployment_recommendation
    )

    assert (
        pipeline_result.deployment_recommendation.strip()
    )


def test_pipeline_generates_summary(
    pipeline_result,
):
    summary = pipeline_result.summary

    assert summary

    assert "Configuration Changes" in summary
    assert "Overall Risk" in summary
    assert "Average Risk Score" in summary
    assert "Average Rule Confidence" in summary
    assert "Recommendation" in summary


def test_pipeline_category_totals_consistent(
    pipeline_result,
):
    category_total = sum(
        category.total_changes
        for category in pipeline_result.category_summary
    )

    assert (
        category_total
        == pipeline_result.statistics.total_changes
    )