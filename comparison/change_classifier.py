"""
comparison/change_classifier.py

Context-aware semantic classifier for network configuration changes.

Author : Shivam Saxena
Project : ConfigVista AI
"""

from __future__ import annotations

import re
from typing import List

from comparison.models import (
    ChangeCategory,
    ConfigurationChange,
)


class ChangeClassifier:
    """
    Classifies configuration changes into semantic categories.

    Classification Priority
    -----------------------
    1. Parent Section
    2. Parent Type
    3. Changed Line
    """

    def __init__(self):

        self.rules = {

            ChangeCategory.INTERFACE: [
                r"^interface\b",
                r"^description\b",
                r"^switchport\b",
                r"^shutdown\b",
                r"^no shutdown\b",
                r"^ip address\b",
                r"^speed\b",
                r"^duplex\b",
                r"^mtu\b",
                r"^service-policy\b",
                r"^ip helper-address\b",
                r"^vrf forwarding\b",
                r"^negotiation\b",
                r"^tunnel\b",
                r"^crypto map\b",
                r"^zone-member\b",
                r"^encapsulation\b",
                r"^keepalive\b",
            ],

            ChangeCategory.ROUTING: [
                r"^router\b",
                r"^network\b",
                r"^neighbor\b",
                r"^redistribute\b",
                r"^default-information\b",
                r"^passive-interface\b",
                r"^ip route\b",
                r"^route-map\b",
                r"^prefix-list\b",
                r"^ospf\b",
                r"^bgp\b",
                r"^eigrp\b",
                r"^track\b",
                r"^ip sla\b",
                r"^bfd\b",
                r"^mpls\b",
                r"^segment-routing\b",
            ],

            ChangeCategory.SWITCHING: [
                r"^vlan\b",
                r"^spanning-tree\b",
                r"^port-channel\b",
                r"^channel-group\b",
                r"^storm-control\b",
            ],

            ChangeCategory.SECURITY: [
                r"^ip access-list\b",
                r"^access-list\b",
                r"^permit\b",
                r"^deny\b",
                r"^aaa\b",
                r"^username\b",
                r"^crypto\b",
                r"^enable secret\b",
                r"^line vty\b",
                r"^snmp-server\b",
                r"^ssh\b",
                r"^class-map\b",
                r"^policy-map\b",
                r"^object-group\b",
                r"^zone\b",
                r"^inspect\b",
                r"^match\b",
            ],

            ChangeCategory.SERVICES: [
                r"^ntp\b",
                r"^logging\b",
                r"^service\b",
                r"^ip domain\b",
                r"^dns\b",
                r"^call-home\b",
                r"^ip http\b",
                r"^radius-server\b",
                r"^tacacs\b",
            ],

            ChangeCategory.MANAGEMENT: [
                r"^hostname\b",
                r"^banner\b",
                r"^vrf\b",
                r"^management\b",
                r"^ip ssh\b",
                r"^archive\b",
                r"^clock\b",
                r"^scheduler\b",
                r"^parser\b",
                r"^alias\b",
            ],

            ChangeCategory.SYSTEM: [
                r"^version\b",
                r"^boot\b",
                r"^license\b",
                r"^platform\b",
                r"^memory\b",
            ],
        }

    # ==========================================================

    def classify(
        self,
        changes: List[ConfigurationChange],
    ) -> List[ConfigurationChange]:
        """
        Classify every detected configuration change.
        """

        for change in changes:

            lookup_text = self._classification_text(change)

            change.category = self._detect_category(
                lookup_text
            )

            change.section = self._determine_section(change)

            change.description = self._description(change)

        return changes

    # ==========================================================

    def _classification_text(
        self,
        change: ConfigurationChange,
    ) -> str:
        """
        Build the text used for classification.

        Priority:
            Parent Section
            Parent Type
            Changed Line
        """

        values = []

        if change.parent_section:
            values.append(change.parent_section)

        if change.parent_type:
            values.append(change.parent_type)

        if change.new_value:
            values.append(change.new_value)

        if change.old_value:
            values.append(change.old_value)

        return " ".join(values).lower()

    # ==========================================================

    def _detect_category(
        self,
        text: str,
    ) -> ChangeCategory:

        for category, patterns in self.rules.items():

            for pattern in patterns:

                if re.search(pattern, text):

                    return category

        return ChangeCategory.UNKNOWN

    # ==========================================================

    def _determine_section(
        self,
        change: ConfigurationChange,
    ) -> str:
        """
        Determine display section.
        """

        if change.parent_section:
            return change.parent_section

        line = change.new_value or change.old_value

        tokens = line.split()

        if tokens:

            return " ".join(tokens[:2])

        return ""

    # ==========================================================

    def _description(
        self,
        change: ConfigurationChange,
    ) -> str:
        """
        Generate human readable description.
        """

        action = change.change_type.value

        category = change.category.value

        if change.parent_section:

            return (
                f"{action} {category} configuration "
                f"in '{change.parent_section}'"
            )

        return f"{action} {category} configuration"

    # ==========================================================

    def classify_single(
        self,
        change: ConfigurationChange,
    ) -> ConfigurationChange:
        """
        Convenience helper for unit testing.
        """

        return self.classify([change])[0]