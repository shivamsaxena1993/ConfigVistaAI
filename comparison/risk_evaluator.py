"""
comparison/risk_evaluator.py

Rule-based risk evaluator for configuration changes.

Author : Shivam Saxena
Project : ConfigVista AI
"""

from __future__ import annotations

from typing import List

from comparison.models import (
    ChangeCategory,
    ConfigurationChange,
    RiskLevel,
)


class RiskEvaluator:
    """
    Evaluates configuration changes and assigns:
        - Risk Level
        - Risk Weight
        - Confidence Score
        - Recommendation
    """

    def __init__(self):

        self.rules = {

            ChangeCategory.ROUTING: (
                RiskLevel.HIGH,
                90,
                95,
                "Validate routing adjacencies and routing table after deployment."
            ),

            ChangeCategory.SECURITY: (
                RiskLevel.HIGH,
                90,
                95,
                "Validate ACL/security policy and confirm management connectivity."
            ),

            ChangeCategory.SYSTEM: (
                RiskLevel.HIGH,
                85,
                90,
                "Verify system health and prepare rollback plan."
            ),

            ChangeCategory.SWITCHING: (
                RiskLevel.MEDIUM,
                70,
                90,
                "Verify VLANs, trunks and STP convergence."
            ),

            ChangeCategory.SERVICES: (
                RiskLevel.MEDIUM,
                60,
                88,
                "Validate dependent network services after deployment."
            ),

            ChangeCategory.MANAGEMENT: (
                RiskLevel.LOW,
                35,
                90,
                "Verify management access after implementation."
            ),

            ChangeCategory.INTERFACE: (
                RiskLevel.LOW,
                30,
                90,
                "Verify interface operational status and traffic flow."
            ),

            ChangeCategory.UNKNOWN: (
                RiskLevel.UNKNOWN,
                0,
                50,
                "Manual review recommended."
            ),
        }

    # ======================================================

    def evaluate(
        self,
        changes: List[ConfigurationChange],
    ) -> List[ConfigurationChange]:
        """
        Evaluate every configuration change.
        """

        for change in changes:

            self.evaluate_single(change)

        return changes

    # ======================================================

    def evaluate_single(
        self,
        change: ConfigurationChange,
    ) -> ConfigurationChange:
        """
        Evaluate one configuration change.
        """

        (
            risk_level,
            weight,
            confidence,
            recommendation,
        ) = self.rules.get(
            change.category,
            self.rules[ChangeCategory.UNKNOWN],
        )

        # --------------------------------------------------
        # Fine tuning using keywords
        # --------------------------------------------------

        text = (
            f"{change.parent_section} "
            f"{change.old_value} "
            f"{change.new_value}"
        ).lower()

        # Interface shutdown is more risky than description/IP changes
        if "shutdown" in text:

            risk_level = RiskLevel.MEDIUM
            weight = max(weight, 60)

            recommendation = (
                "Verify interface shutdown impact before deployment."
            )

        # Default route modification
        if "0.0.0.0" in text:

            risk_level = RiskLevel.HIGH
            weight = 95

            recommendation = (
                "Validate default route reachability before implementation."
            )

        # OSPF
        if "ospf" in text:

            risk_level = RiskLevel.HIGH
            weight = max(weight, 90)

            recommendation = (
                "Verify OSPF adjacency and route propagation."
            )

        # BGP
        if "bgp" in text:

            risk_level = RiskLevel.HIGH
            weight = 95

            recommendation = (
                "Verify BGP neighbor state and advertised prefixes."
            )

        # ACL permit/deny
        if "permit" in text or "deny" in text:

            risk_level = RiskLevel.HIGH
            weight = max(weight, 90)

            recommendation = (
                "Validate ACL behavior to avoid unintended traffic impact."
            )

        # Hostname changes
        if "hostname" in text:

            risk_level = RiskLevel.LOW
            weight = 20

            recommendation = (
                "Verify hostname update across monitoring systems."
            )

        # --------------------------------------------------

        change.risk_level = risk_level
        change.risk_weight = weight
        change.confidence_score = confidence
        change.recommendation = recommendation

        return change

    # ======================================================
    def average_rule_confidence(
        self,
        changes: List[ConfigurationChange],
    ) -> float:
        """
        Calculate average deterministic rule confidence (0-100).
        """

        if not changes:
            return 0.0

        return round(
            sum(c.confidence_score for c in changes) / len(changes),
            2,
        )
    

    def deployment_recommendation(
        self,
        changes: List[ConfigurationChange],
    ) -> str:
        """
        Generate aggregate deployment guidance from rule-based risk.
        """

        overall = self.overall_risk(changes)

        if overall == RiskLevel.HIGH:
            return (
                "Do not deploy without technical validation, "
                "an approved maintenance window, and a rollback plan."
            )

        if overall == RiskLevel.MEDIUM:
            return (
                "Deploy with caution and perform targeted "
                "validation during implementation."
            )

        if overall == RiskLevel.LOW:
            return (
                "Proceed using the standard change process "
                "with normal post-change validation."
            )

        return "Manual review recommended before deployment."
    
    def overall_risk(
        self,
        changes: List[ConfigurationChange],
    ) -> RiskLevel:
        """
        Determine overall risk for the comparison.
        """

        if any(c.risk_level == RiskLevel.HIGH for c in changes):
            return RiskLevel.HIGH

        if any(c.risk_level == RiskLevel.MEDIUM for c in changes):
            return RiskLevel.MEDIUM

        if any(c.risk_level == RiskLevel.LOW for c in changes):
            return RiskLevel.LOW

        return RiskLevel.UNKNOWN

    # ======================================================

    def risk_score(
        self,
        changes: List[ConfigurationChange],
    ) -> float:
        """
        Average weighted risk score (0-100).
        """

        if not changes:
            return 0.0

        return round(
            sum(c.risk_weight for c in changes) / len(changes),
            2,
        )