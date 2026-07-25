"""
comparison/models.py

Data models for the Configuration Comparison Framework.

Author : Shivam Saxena
Project: ConfigVista AI
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


# ==========================================================
# ENUMS
# ==========================================================

class ChangeType(str, Enum):
    """Type of configuration change."""

    ADDED = "Added"
    REMOVED = "Removed"
    MODIFIED = "Modified"


class ChangeCategory(str, Enum):
    """Semantic category of configuration change."""

    INTERFACE = "Interface"
    ROUTING = "Routing"
    SWITCHING = "Switching"
    SECURITY = "Security"
    SERVICES = "Services"
    MANAGEMENT = "Management"
    SYSTEM = "System"
    UNKNOWN = "Unknown"


class RiskLevel(str, Enum):
    """Risk associated with the change."""

    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    UNKNOWN = "Unknown"


# ==========================================================
# CORE DATA MODELS
# ==========================================================

@dataclass
class ConfigurationChange:
    """
    Represents a single configuration difference.
    """

    # Change information
    change_type: ChangeType

    category: ChangeCategory = ChangeCategory.UNKNOWN

    # Configuration hierarchy
    parent_section: str = ""
    parent_type: str = ""

    # Display section
    section: str = ""

    # Line information
    line_number: Optional[int] = None

    # Before / After values
    old_value: str = ""
    new_value: str = ""

    # Risk
    risk_level: RiskLevel = RiskLevel.UNKNOWN
    risk_weight: int = 0

    # Deterministic rule confidence (Artifact-1)
    confidence_score: float = 0.0

    # User readable information
    description: str = ""
    recommendation: str = ""


# ==========================================================

@dataclass
class ComparisonStatistics:
    """
    Summary statistics.
    """

    total_changes: int = 0

    added: int = 0
    removed: int = 0
    modified: int = 0

    high_risk: int = 0
    medium_risk: int = 0
    low_risk: int = 0


# ==========================================================

@dataclass
class CategorySummary:
    """
    Summary for each configuration category.
    """

    category: ChangeCategory

    total_changes: int = 0

    high_risk: int = 0
    medium_risk: int = 0
    low_risk: int = 0


# ==========================================================

@dataclass
class ComparisonResult:
    """
    Final output produced by ComparisonEngine.
    """

    baseline_hostname: str = ""
    candidate_hostname: str = ""

    # -------------------------------------------------
    # Parsed Interface Objects
    # -------------------------------------------------

    baseline_interfaces: List[dict] = field(
        default_factory=list
    )

    candidate_interfaces: List[dict] = field(
        default_factory=list
    )

    # -------------------------------------------------
    # Parser Statistics
    # -------------------------------------------------

    baseline_statistics: dict = field(
        default_factory=dict
    )

    candidate_statistics: dict = field(
        default_factory=dict
    )

    # -------------------------------------------------
    # Validation
    # -------------------------------------------------
    
    baseline_validation: List = field(
        default_factory=list
    )
    
    candidate_validation: List = field(
        default_factory=list
    )

    changes: List[ConfigurationChange] = field(default_factory=list)

    statistics: ComparisonStatistics = field(
        default_factory=ComparisonStatistics
    )

    category_summary: List[CategorySummary] = field(
        default_factory=list
    )

    # Rule-based aggregate assessment
    overall_risk: RiskLevel = RiskLevel.UNKNOWN
    average_risk_score: float = 0.0
    average_rule_confidence: float = 0.0
    deployment_recommendation: str = ""

    summary: str = ""
    device_role: str = "Unknown"
    comparison_time_ms: float = 0.0

    comparison_version: str = "2.1"


# ==========================================================
# HELPERS
# ==========================================================

def calculate_statistics(result: ComparisonResult) -> None:
    """
    Populate summary statistics.
    """

    stats = ComparisonStatistics()

    stats.total_changes = len(result.changes)

    for change in result.changes:

        if change.change_type == ChangeType.ADDED:
            stats.added += 1

        elif change.change_type == ChangeType.REMOVED:
            stats.removed += 1

        elif change.change_type == ChangeType.MODIFIED:
            stats.modified += 1

        if change.risk_level == RiskLevel.HIGH:
            stats.high_risk += 1

        elif change.risk_level == RiskLevel.MEDIUM:
            stats.medium_risk += 1

        elif change.risk_level == RiskLevel.LOW:
            stats.low_risk += 1

    result.statistics = stats


# ==========================================================

def build_category_summary(result: ComparisonResult) -> None:
    """
    Populate category-wise summary.
    """

    summary = {}

    for change in result.changes:

        category = change.category

        if category not in summary:

            summary[category] = CategorySummary(
                category=category
            )

        item = summary[category]

        item.total_changes += 1

        if change.risk_level == RiskLevel.HIGH:
            item.high_risk += 1

        elif change.risk_level == RiskLevel.MEDIUM:
            item.medium_risk += 1

        elif change.risk_level == RiskLevel.LOW:
            item.low_risk += 1

    preferred=[
    ChangeCategory.INTERFACE,
    ChangeCategory.ROUTING,
    ChangeCategory.SECURITY,
    ChangeCategory.MANAGEMENT,
    ChangeCategory.SERVICES,
    ChangeCategory.SYSTEM,
    ChangeCategory.SWITCHING,
    ChangeCategory.UNKNOWN
    ]

    result.category_summary=sorted(
    summary.values(),
    key=lambda x:
    preferred.index(
    x.category
    )
    )