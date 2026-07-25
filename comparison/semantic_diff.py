"""
comparison/semantic_diff.py

Semantic Configuration Difference Engine

Project : ConfigVista AI
Author  : Shivam Saxena

Version : 3.0

Purpose
-------
Semantic comparison of Cisco IOS-XE configurations.

Unlike DiffEngine, which compares configuration
line-by-line using SequenceMatcher, this module
compares parsed configuration objects.

Stage 1
--------
✓ Interface Extraction
✓ Tunnel Extraction
✓ Interface Attribute Parsing
✓ Semantic Object Creation

Stage 2
--------
• Semantic Comparison

Stage 3
--------
• Routing
• VRF

Stage 4
--------
• QoS
• ACL
• Security

Stage 5
--------
• Services
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict
from typing import List
from typing import Optional

import ipaddress

from comparison.models import (
    ChangeType,
    ConfigurationChange,
)

from comparison.utils import (
    parent_type,
)
# ============================================================
# Interface Object
# ============================================================

@dataclass
class InterfaceObject:
    """
    Canonical representation of one interface.

    Every interface from both configurations is
    converted into this structure before comparison.
    """

    name: str

    description: str = ""

    shutdown: bool = False

    vrf: Optional[str] = None

    ip_address: Optional[str] = None

    subnet_mask: Optional[str] = None

    mtu: Optional[int] = None

    bandwidth: Optional[int] = None

    speed: Optional[str] = None

    duplex: Optional[str] = None

    negotiation: Optional[str] = None

    helper_addresses: List[str] = field(default_factory=list)

    inbound_acl: Optional[str] = None

    outbound_acl: Optional[str] = None

    service_policy_input: Optional[str] = None

    service_policy_output: Optional[str] = None

    zone_member: Optional[str] = None

    tunnel_source: Optional[str] = None

    tunnel_destination: Optional[str] = None

    tunnel_mode: Optional[str] = None

    crypto_map: Optional[str] = None

    raw_commands: List[str] = field(default_factory=list)

# ============================================================
# Semantic Diff Engine
# ============================================================

class SemanticDiffEngine:
    """
    Production semantic comparison engine.

    Workflow

    Raw Config

        ↓

    Interface Objects

        ↓

    Compare Attributes

        ↓

    ConfigurationChange

    """

    def __init__(self):

        pass

    # ========================================================
    # Helpers
    # ========================================================

    @staticmethod
    def _safe_int(value):

        try:

            return int(value)

        except Exception:

            return None

    @staticmethod
    def _normalize_ip(ip):

        try:

            return str(
                ipaddress.ip_address(ip)
            )

        except Exception:

            return ip

    @staticmethod
    def _clean(line):

        return line.strip()

    @staticmethod
    def _is_interface_command(line):

        return line.startswith("interface ")

    @staticmethod
    def _create_change(
        change_type,
        interface,
        field_name,
        old="",
        new="",
    ):

        return ConfigurationChange(

            change_type=change_type,

            parent_section=f"interface {interface}",

            parent_type=parent_type(
                f"interface {interface}"
            ),

            section=field_name,

            old_value=str(old),

            new_value=str(new),
        )
    # ========================================================
    # Interface Parser
    # ========================================================

    def parse_interface(
        self,
        name: str,
        block: List[str],
    ) -> InterfaceObject:
        """
        Convert an interface configuration block into a
        normalized InterfaceObject.

        The parser intentionally ignores command ordering.
        Only the resulting interface state is stored.

        Parameters
        ----------
        name : str
            Interface name

        block : List[str]
            Complete interface configuration block

        Returns
        -------
        InterfaceObject
        """

        interface = InterfaceObject(name=name)

        for raw_line in block[1:]:

            line = self._clean(raw_line)

            if not line:
                continue

            interface.raw_commands.append(line)

            # --------------------------------------------
            # Description
            # --------------------------------------------

            if line.startswith("description "):

                interface.description = (
                    line[len("description "):].strip()
                )

                continue

            # --------------------------------------------
            # Shutdown
            # --------------------------------------------

            if line == "shutdown":

                interface.shutdown = True

                continue

            if line == "no shutdown":

                interface.shutdown = False

                continue

            # --------------------------------------------
            # VRF
            # --------------------------------------------

            if line.startswith("vrf forwarding "):

                interface.vrf = (
                    line[len("vrf forwarding "):].strip()
                )

                continue

            # --------------------------------------------
            # IP Address
            # --------------------------------------------

            if line.startswith("ip address "):

                tokens = line.split()

                if len(tokens) >= 4:

                    interface.ip_address = (
                        self._normalize_ip(tokens[2])
                    )

                    interface.subnet_mask = tokens[3]

                continue

            # --------------------------------------------
            # MTU
            # --------------------------------------------

            if line.startswith("mtu "):

                value = line.split(maxsplit=1)[1]

                interface.mtu = self._safe_int(value)

                continue

            # --------------------------------------------
            # Bandwidth
            # --------------------------------------------

            if line.startswith("bandwidth "):

                value = line.split(maxsplit=1)[1]

                interface.bandwidth = self._safe_int(value)

                continue

            # --------------------------------------------
            # Speed
            # --------------------------------------------

            if line.startswith("speed "):

                interface.speed = (
                    line.split(maxsplit=1)[1].strip()
                )

                continue

            # --------------------------------------------
            # Duplex
            # --------------------------------------------

            if line.startswith("duplex "):

                interface.duplex = (
                    line.split(maxsplit=1)[1].strip()
                )

                continue

            # --------------------------------------------
            # Negotiation
            # --------------------------------------------

            if line.startswith("negotiation "):

                interface.negotiation = (
                    line.split(maxsplit=1)[1].strip()
                )

                continue
            
                        # --------------------------------------------
            # IP Helper Addresses
            # --------------------------------------------

            if line.startswith("ip helper-address "):

                helper = line[len("ip helper-address "):].strip()

                helper = self._normalize_ip(helper)

                if helper not in interface.helper_addresses:
                    interface.helper_addresses.append(helper)

                continue

            # --------------------------------------------
            # Input Service Policy
            # --------------------------------------------

            if line.startswith("service-policy input "):

                interface.service_policy_input = (
                    line[len("service-policy input "):].strip()
                )

                continue

            # --------------------------------------------
            # Output Service Policy
            # --------------------------------------------

            if line.startswith("service-policy output "):

                interface.service_policy_output = (
                    line[len("service-policy output "):].strip()
                )

                continue

            # --------------------------------------------
            # Interface ACL
            #
            # Examples
            # ip access-group ACL-IN in
            # ip access-group ACL-OUT out
            # --------------------------------------------

            if line.startswith("ip access-group "):

                tokens = line.split()

                if len(tokens) >= 4:

                    acl_name = tokens[2]
                    direction = tokens[3].lower()

                    if direction == "in":
                        interface.inbound_acl = acl_name

                    elif direction == "out":
                        interface.outbound_acl = acl_name

                continue

            # --------------------------------------------
            # Zone Based Firewall
            #
            # zone-member security INSIDE
            # --------------------------------------------

            if line.startswith("zone-member security "):

                interface.zone_member = (
                    line[len("zone-member security "):].strip()
                )

                continue

            # --------------------------------------------
            # Crypto Map
            #
            # crypto map VPN-MAP
            # --------------------------------------------

            if line.startswith("crypto map "):

                interface.crypto_map = (
                    line[len("crypto map "):].strip()
                )

                continue

            # --------------------------------------------
            # Tunnel Source
            # --------------------------------------------

            if line.startswith("tunnel source "):

                interface.tunnel_source = (
                    line[len("tunnel source "):].strip()
                )

                continue

            # --------------------------------------------
            # Tunnel Destination
            # --------------------------------------------

            if line.startswith("tunnel destination "):

                destination = (
                    line[len("tunnel destination "):].strip()
                )

                interface.tunnel_destination = (
                    self._normalize_ip(destination)
                )

                continue

            # --------------------------------------------
            # Tunnel Mode
            # --------------------------------------------

            if line.startswith("tunnel mode "):

                interface.tunnel_mode = (
                    line[len("tunnel mode "):].strip()
                )

                continue
        return interface
