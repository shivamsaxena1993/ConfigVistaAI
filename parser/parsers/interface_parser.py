"""
====================================================================

File: interface_parser.py

Project: ConfigVista AI

Module:
Enterprise Cisco Interface Parser

Version:
3.0

Author:
ConfigVista AI

Purpose
-------
Parses Cisco IOS / IOS-XE interface configuration into
normalized interface objects.

This parser acts as the single source of truth for interface
data used by:

• SemanticDiffEngine
• ComparisonEngine
• RiskEvaluator
• FeatureExtractor
• ReportGenerator

Supported Features
------------------

Layer 3
✓ IPv4 Address
✓ Secondary Address
✓ VRF
✓ Helper Address
✓ MTU
✓ Bandwidth
✓ Speed
✓ Duplex
✓ Negotiation

Layer 2
✓ Switchport
✓ Access VLAN
✓ Voice VLAN
✓ Native VLAN
✓ Allowed VLANs
✓ Channel Group

Security
✓ ACL
✓ Zone Member
✓ Crypto Map

QoS
✓ Service Policy

Tunnel
✓ Tunnel Source
✓ Tunnel Destination
✓ Tunnel Mode

Classification
✓ Physical
✓ Loopback
✓ SVI
✓ Port-channel
✓ Tunnel
✓ Sub-interface

====================================================================
"""

from typing import Dict
from typing import List
from typing import Optional
from typing import Set

import ipaddress
import logging

import hashlib
import json
import re

logger = logging.getLogger(__name__)


class InterfaceParser:
    """
    Enterprise Interface Parser

    Phase 1 only builds the framework.
    Future phases extend parser methods without modifying parse().
    """
    PARSER_VERSION = "3.0"

    INTERFACE_PREFIXES = {

        "Gi": "GigabitEthernet",

        "Fa": "FastEthernet",

        "Te": "TenGigabitEthernet",

        "Twe": "TwentyFiveGigE",

        "Fo": "FortyGigabitEthernet",

        "Hu": "HundredGigE",

        "Eth": "Ethernet",

        "Lo": "Loopback",

        "Po": "Port-channel",

        "Vl": "Vlan",

        "Tu": "Tunnel"
    }
    
    def __init__(self, lines: List[str]):

        self.lines = lines

        self.statistics = {

            "interfaces":0,

            "physical":0,

            "loopbacks":0,

            "svis":0,

            "tunnels":0,

            "port_channels":0,

            "switchports":0,

            "routed":0,

            "trunks":0,

            "access_ports":0,

            "qos_interfaces":0,

            "acl_interfaces":0,

            "validation_results":[],

            "validation_failures":0
        }

    # ==============================================================
    # Public Entry
    # ==============================================================

    def parse(self) -> List[Dict]:

        interface_blocks = self._split_interfaces()

        interfaces = []

        for block in interface_blocks:

            interface = self._create_interface(block)

            self._parse_basic(block, interface)

            # Future phases

            self._parse_layer3(block, interface)

            self._parse_layer2(block, interface)

            self._parse_security(block, interface)

            self._parse_operational(block, interface)

            self._parse_qos(block, interface)

            interfaces.append(interface)

        return self._finalize(interfaces)

    # ==============================================================
    # Split Configuration
    # ==============================================================

    def _split_interfaces(self):

        blocks = []

        current = []

        inside = False

        for line in self.lines:

            stripped = line.rstrip()

            if stripped.startswith("interface "):

                if current:

                    blocks.append(current)

                current = [stripped]

                inside = True

                continue

            if inside:

                if stripped == "!":

                    blocks.append(current)

                    current = []

                    inside = False

                else:

                    current.append(stripped)

        if current:

            blocks.append(current)

        return blocks

    # ==============================================================
    # Create Interface Object
    # ==============================================================

    def _create_interface(self, block):

        raw_name = block[0].split(None, 1)[1]
    
        name = self._normalize_interface_name(
            raw_name
        )

        return {

            # -----------------------------
            # Identity
            # -----------------------------

            "name": name,

            "description": "",

            # -----------------------------
            # Classification
            # -----------------------------

            "physical": False,

            "loopback": False,

            "svi": False,

            "port_channel": False,

            "tunnel": False,

            "subinterface": "." in name,

            # -----------------------------
            # Layer 3
            # -----------------------------

            "shutdown": False,

            "vrf": None,

            "ip_address": None,

            "subnet_mask": None,

            "secondary_ips": [],

            "helper_addresses": [],

            "unnumbered_interface": None,

            "tcp_mss": None,

            "redirects": True,

            "unreachables": True,

            "proxy_arp": True,

            "mtu": None,

            "bandwidth": None,

            "speed": None,

            "duplex": None,

            "negotiation": None,

            # -----------------------------
            # Layer 2
            # -----------------------------

            "switchport_mode": None,

            "access_vlan": None,

            "voice_vlan": None,

            "native_vlan": None,

            "allowed_vlans": [],

            "channel_group": None,

            # Trunk

            "trunk_encapsulation": None,

            # Spanning Tree

            "portfast": False,

            "bpduguard": False,

            "bpdufilter": False,

            "root_guard": False,

            "loop_guard": False,

            # Storm Control

            "storm_control_broadcast": None,

            "storm_control_multicast": None,

            "storm_control_unicast": None,
            # -----------------------------
            # Security
            # -----------------------------

            "inbound_acl": None,

            "outbound_acl": None,

            "ipv6_inbound_acl": None,

            "ipv6_outbound_acl": None,

            "zone_member": None,

            "crypto_map": None,

            "ip_verify_source": False,

            "dhcp_snooping_trust": False,

            "arp_inspection_trust": False,

            # -----------------------------
            # QoS
            # -----------------------------

            "service_policy_input": None,

            "service_policy_output": None,

            "qos_trust": None,

            "priority_queue": False,

            "shape_average": None,

            "police_rate": None,

            # -----------------------------
            # Operational
            # -----------------------------

            "keepalive": True,

            "keepalive_period": None,

            "keepalive_retry": None,

            "load_interval": None,

            "carrier_delay": None,

            "logging_events": [],

            "cdp_enabled": True,

            "lldp_transmit": True,

            "lldp_receive": True,

            "shutdown_reason": None,


            # -----------------------------
            # Tunnel
            # -----------------------------


            "tunnel_source": None,

            "tunnel_destination": None,

            "tunnel_mode": None,

            "tunnel_key": None,

            "tunnel_vrf": None,

            "tunnel_protection": None,

            # -----------------------------
            # Semantic
            # -----------------------------

            "semantic": {},

            "validation_score": 100,

            "semantic_hash": None,


            # -----------------------------
            # Raw Configuration
            # -----------------------------

            "commands": []
        }

    def _safe_int(self, value):

        try:
            return int(str(value).strip())
        except (TypeError, ValueError):
            return None


    def _normalize_ip(self, ip):
    
        try:
            return str(ipaddress.ip_address(ip))
        except (ValueError, TypeError):
            return ip
    
    def _expand_vlan_list(self, vlan_string):
        """
        Expand Cisco VLAN ranges.

        Example

        10,20-22,100

        becomes

        [10,20,21,22,100]
        """

        vlans = []

        if not vlan_string:

            return vlans

        for item in vlan_string.split(","):

            item = item.strip()

            if "-" in item:

                start, end = item.split("-", 1)

                start = self._safe_int(start)

                end = self._safe_int(end)

                if start is None or end is None:
                    continue

                vlans.extend(
                    range(start, end + 1)
                )

            else:

                vlan = self._safe_int(item)

                if vlan is not None:

                    vlans.append(vlan)

        return sorted(
            self._deduplicate(vlans)
        )
    
    def _clean_string(self, value):
    
        if value is None:
            return None
    
        return str(value).strip()
    
    
    def _deduplicate(self, values):
    
        return list(dict.fromkeys(values))

    def _normalize_interface_name(self, name):

        if not name:
            return name

        name = name.strip()

        # Already canonical: preserve it unchanged.
        for full in self.INTERFACE_PREFIXES.values():

            if name.startswith(full):
                return name

        # Expand supported Cisco abbreviations.
        for short, full in self.INTERFACE_PREFIXES.items():

            if name.startswith(short):
                return full + name[len(short):]

        # Unknown interface types remain unchanged.
        return name

    def _normalize_identifier(self, value):

        if value is None:

            return None

        return value.strip().upper()
    
    def _normalize_tunnel_mode(self, value):

        if value is None:

            return None

        return value.strip().lower()
    
    def _normalize_description(self, value):

        if not value:

            return None

        return re.sub(
            r"\s+",
            " ",
            value.strip()
        )
    
    def _normalize_interface(self, interface):

        #
        # Interface Name
        #

        interface["name"] = self._normalize_interface_name(
            interface["name"]
        )

        #
        # Description
        #

        interface["description"] = self._normalize_description(
            interface["description"]
        )

        #
        # ACLs
        #

        interface["inbound_acl"] = self._normalize_identifier(
            interface["inbound_acl"]
        )

        interface["outbound_acl"] = self._normalize_identifier(
            interface["outbound_acl"]
        )

        interface["ipv6_inbound_acl"] = self._normalize_identifier(
            interface["ipv6_inbound_acl"]
        )

        interface["ipv6_outbound_acl"] = self._normalize_identifier(
            interface["ipv6_outbound_acl"]
        )

        #
        # Zone
        #

        interface["zone_member"] = self._normalize_identifier(
            interface["zone_member"]
        )

        #
        # QoS
        #

        interface["service_policy_input"] = self._normalize_identifier(
            interface["service_policy_input"]
        )

        interface["service_policy_output"] = self._normalize_identifier(
            interface["service_policy_output"]
        )

        #
        # Crypto Map
        #

        interface["crypto_map"] = self._normalize_identifier(
            interface["crypto_map"]
        )

        #
        # Tunnel Mode
        #

        interface["tunnel_mode"] = self._normalize_tunnel_mode(
            interface["tunnel_mode"]
        )

        #
        # Logging Events
        #

        interface["logging_events"] = sorted(
            self._deduplicate(
                interface["logging_events"]
            )
        )

        #
        # Secondary IPs
        #

        interface["secondary_ips"] = sorted(

            interface["secondary_ips"],

            key=lambda x: x["ip"]

        )

        #
        # Helper Addresses
        #

        interface["helper_addresses"] = sorted(

            self._deduplicate(

                interface["helper_addresses"]

            )

        )

        #
        # Allowed VLANs
        #

        interface["allowed_vlans"] = sorted(

            self._deduplicate(

                interface["allowed_vlans"]

            )

        )

        #
        # Commands
        #

        interface["commands"] = [

            cmd.rstrip()

            for cmd in interface["commands"]

        ]

    def _build_semantic_metadata(self, interface):

        semantic = {}

        semantic["is_switchport"] = (
            interface["switchport_mode"] is not None
        )

        semantic["is_routed"] = (
            interface["ip_address"] is not None
            or
            interface["unnumbered_interface"] is not None
        )

        semantic["is_access"] = (
            interface["switchport_mode"] == "access"
        )

        semantic["is_trunk"] = (
            interface["switchport_mode"] == "trunk"
        )

        semantic["has_ip"] = (
            interface["ip_address"] is not None
        )

        semantic["has_vrf"] = (
            interface["vrf"] is not None
        )

        semantic["has_acl"] = any([

            interface["inbound_acl"],

            interface["outbound_acl"],

            interface["ipv6_inbound_acl"],

            interface["ipv6_outbound_acl"]

        ])

        semantic["has_qos"] = any([

            interface["service_policy_input"],

            interface["service_policy_output"],

            interface["priority_queue"],

            interface["shape_average"],

            interface["police_rate"]

        ])

        semantic["has_security"] = any([

            semantic["has_acl"],

            interface["zone_member"],

            interface["crypto_map"]

        ])

        semantic["has_tunnel"] = (
            interface["tunnel_source"] is not None
        )

        #
        # Risk Domain
        #

        if interface["tunnel"]:

            semantic["risk_domain"] = "WAN"

        elif semantic["is_trunk"]:

            semantic["risk_domain"] = "Switching"

        elif semantic["is_access"]:

            semantic["risk_domain"] = "Campus"

        elif semantic["is_routed"]:

            semantic["risk_domain"] = "Routing"

        else:

            semantic["risk_domain"] = "General"

        interface["semantic"] = semantic

    def _generate_semantic_hash(self, interface):

        hash_data = {

            key: value

            for key, value in interface.items()

            if key not in [

                "commands",

                "semantic_hash",

                "validation_score"

            ]

        }

        payload = json.dumps(

            hash_data,

            sort_keys=True,

            default=str

        )

        interface["semantic_hash"] = hashlib.sha256(

            payload.encode()

        ).hexdigest()

    # ==============================================================
    # Basic Parser
    # ==============================================================

    def _parse_basic(self, block, interface):

        name = interface["name"]

        interface["loopback"] = name.startswith("Loopback")

        interface["svi"] = name.startswith("Vlan")

        interface["port_channel"] = name.startswith("Port-channel")

        interface["tunnel"] = name.startswith("Tunnel")

        interface["subinterface"] = "." in name

        interface["physical"] = not any([
            interface["loopback"],
            interface["svi"],
            interface["port_channel"],
            interface["tunnel"],
            interface["subinterface"],
        ])

        

        for line in block[1:]:

            line = line.strip()

            if line.startswith("description "):

                interface["description"] = line[12:]

            elif line == "shutdown":

                interface["shutdown"] = True

            interface["commands"].append(line)

    # ==============================================================
    # Phase 2 Placeholder
    # ==============================================================

    def _parse_layer3(self, block, interface):
        """
        Parse Layer 3 interface configuration.
        """

        for raw_line in block[1:]:

            line = raw_line.strip()

            # ----------------------------------
            # VRF
            # ----------------------------------

            if line.startswith("vrf forwarding "):

                interface["vrf"] = self._clean_string(
                    line[len("vrf forwarding "):]
                )

                continue

            # ----------------------------------
            # Primary / Secondary IP
            # ----------------------------------

            if line.startswith("ip address "):

                tokens = line.split()

                if len(tokens) >= 4:

                    ip = self._normalize_ip(tokens[2])
                    mask = tokens[3]

                    if "secondary" in tokens:

                        interface["secondary_ips"].append({

                            "ip": self._normalize_ip(ip),

                            "mask": mask

                        })

                    else:

                        interface["ip_address"] = ip

                        interface["subnet_mask"] = mask

                continue

            # ----------------------------------
            # Unnumbered Interface
            # ----------------------------------

            if line.startswith("ip unnumbered "):

                interface["unnumbered_interface"] = self._clean_string(
                    line[len("ip unnumbered "):].strip()
                )

                continue

            # ----------------------------------
            # Helper Address
            # ----------------------------------

            if line.startswith("ip helper-address "):

                helper = (
                    line[len("ip helper-address "):].strip()
                )

                helper = self._normalize_ip(helper)

                if helper not in interface["helper_addresses"]:

                    interface["helper_addresses"].append(
                        helper
                    )

                continue

            # ----------------------------------
            # MTU
            # ----------------------------------

            if line.startswith("mtu "):

                interface["mtu"] = self._safe_int(
                    line.split()[1]
                )

                continue

            # ----------------------------------
            # Bandwidth
            # ----------------------------------

            if line.startswith("bandwidth "):

                interface["bandwidth"] = self._safe_int(
                    line.split()[1]
                )

                continue

            # ----------------------------------
            # Speed
            # ----------------------------------

            if line.startswith("speed "):

                interface["speed"] = self._clean_string(
                    line[len("speed "):].strip()
                )

                continue

            # ----------------------------------
            # Duplex
            # ----------------------------------

            if line.startswith("duplex "):

                interface["duplex"] = self._clean_string(
                    line[len("duplex "):].strip()
                )

                continue

            # ----------------------------------
            # Negotiation
            # ----------------------------------

            if line.startswith("negotiation "):

                interface["negotiation"] = self._clean_string(
                    line[len("negotiation "):].strip()
                )

                continue

            # ----------------------------------
            # TCP MSS
            # ----------------------------------

            if line.startswith("ip tcp adjust-mss "):

                interface["tcp_mss"] = self._safe_int(
                    line.split()[-1]
                )

                continue

            # ----------------------------------
            # ICMP Redirects
            # ----------------------------------

            if line == "no ip redirects":

                interface["redirects"] = False

                continue

            # ----------------------------------
            # ICMP Unreachables
            # ----------------------------------

            if line == "no ip unreachables":

                interface["unreachables"] = False

                continue

            # ----------------------------------
            # Proxy ARP
            # ----------------------------------

            if line == "no ip proxy-arp":

                interface["proxy_arp"] = False

                continue

    # ==============================================================
    # Phase 3 Placeholder
    # ==============================================================

    def _parse_layer2(self, block, interface):
        """
        Parse Layer 2 interface configuration.
        """

        for raw_line in block[1:]:

            line = raw_line.strip()

            # ----------------------------------
            # Switchport Mode
            # ----------------------------------

            if line.startswith("switchport mode "):

                interface["switchport_mode"] = self._clean_string(
                    line[len("switchport mode "):]
                )

                continue

            # ----------------------------------
            # Access VLAN
            # ----------------------------------

            if line.startswith("switchport access vlan "):

                interface["access_vlan"] = self._safe_int(
                    line.split()[-1]
                )

                continue

            # ----------------------------------
            # Voice VLAN
            # ----------------------------------

            if line.startswith("switchport voice vlan "):

                interface["voice_vlan"] = self._safe_int(
                    line.split()[-1]
                )

                continue

            # ----------------------------------
            # Native VLAN
            # ----------------------------------

            if line.startswith("switchport trunk native vlan "):

                interface["native_vlan"] = self._safe_int(
                    line.split()[-1]
                )

                continue

            # ----------------------------------
            # Allowed VLANs
            # ----------------------------------

            if line.startswith(
                "switchport trunk allowed vlan "
            ):

                vlan_string = line[
                    len("switchport trunk allowed vlan "):
                ]

                interface["allowed_vlans"] = (
                    self._expand_vlan_list(
                        vlan_string
                    )
                )

                continue

            # ----------------------------------
            # Trunk Encapsulation
            # ----------------------------------

            if line.startswith(
                "switchport trunk encapsulation "
            ):

                interface["trunk_encapsulation"] = (
                    self._clean_string(
                        line[
                            len(
                                "switchport trunk encapsulation "
                            ):
                        ]
                    )
                )

                continue

            # ----------------------------------
            # EtherChannel
            # ----------------------------------

            if line.startswith("channel-group "):

                tokens = line.split()

                if len(tokens) >= 2:

                    interface["channel_group"] = (
                        self._safe_int(tokens[1])
                    )

                continue

            # ----------------------------------
            # PortFast
            # ----------------------------------

            if line == "spanning-tree portfast":

                interface["portfast"] = True

                continue

            # ----------------------------------
            # BPDU Guard
            # ----------------------------------

            if line == "spanning-tree bpduguard enable":

                interface["bpduguard"] = True

                continue

            # ----------------------------------
            # BPDU Filter
            # ----------------------------------

            if line == "spanning-tree bpdufilter enable":

                interface["bpdufilter"] = True

                continue

            # ----------------------------------
            # Root Guard
            # ----------------------------------

            if line == "spanning-tree guard root":

                interface["root_guard"] = True

                continue

            # ----------------------------------
            # Loop Guard
            # ----------------------------------

            if line == "spanning-tree guard loop":

                interface["loop_guard"] = True

                continue

            # ----------------------------------
            # Storm Control Broadcast
            # ----------------------------------

            if line.startswith(
                "storm-control broadcast level "
            ):

                interface[
                    "storm_control_broadcast"
                ] = self._clean_string(
                    line.split("level", 1)[1]
                )

                continue

            # ----------------------------------
            # Storm Control Multicast
            # ----------------------------------

            if line.startswith(
                "storm-control multicast level "
            ):

                interface[
                    "storm_control_multicast"
                ] = self._clean_string(
                    line.split("level", 1)[1]
                )

                continue

            # ----------------------------------
            # Storm Control Unicast
            # ----------------------------------

            if line.startswith(
                "storm-control unicast level "
            ):

                interface[
                    "storm_control_unicast"
                ] = self._clean_string(
                    line.split("level", 1)[1]
                )

                continue
        
        
    # ==============================================================
    # Phase 4 Placeholder
    # ==============================================================

    def _parse_security(self, block, interface):
        """
        Parse interface security and tunnel configuration.
        """

        for raw_line in block[1:]:

            line = raw_line.strip()

            # ----------------------------------
            # IPv4 ACL
            # ----------------------------------

            if line.startswith("ip access-group "):

                tokens = line.split()

                if len(tokens) >= 4:

                    acl = tokens[2]

                    direction = tokens[3].lower()

                    if direction == "in":

                        interface["inbound_acl"] = acl

                    elif direction == "out":

                        interface["outbound_acl"] = acl

                continue

            # ----------------------------------
            # IPv6 ACL
            # ----------------------------------

            if line.startswith("ipv6 traffic-filter "):

                tokens = line.split()

                if len(tokens) >= 4:

                    acl = tokens[2]

                    direction = tokens[3].lower()

                    if direction == "in":

                        interface["ipv6_inbound_acl"] = acl

                    elif direction == "out":

                        interface["ipv6_outbound_acl"] = acl

                continue

            # ----------------------------------
            # Zone Based Firewall
            # ----------------------------------

            if line.startswith("zone-member security "):

                interface["zone_member"] = self._clean_string(
                    line[len("zone-member security "):]
                )

                continue

            # ----------------------------------
            # Crypto Map
            # ----------------------------------

            if line.startswith("crypto map "):

                interface["crypto_map"] = self._clean_string(
                    line[len("crypto map "):]
                )

                continue

            # ----------------------------------
            # Tunnel Source
            # ----------------------------------

            if line.startswith("tunnel source "):

                interface["tunnel_source"] = self._clean_string(
                    line[len("tunnel source "):]
                )

                continue

            # ----------------------------------
            # Tunnel Destination
            # ----------------------------------

            if line.startswith("tunnel destination "):

                interface["tunnel_destination"] = self._clean_string(
                    line[len("tunnel destination "):]
                )

                continue

            # ----------------------------------
            # Tunnel Mode
            # ----------------------------------

            if line.startswith("tunnel mode "):

                interface["tunnel_mode"] = self._clean_string(
                    line[len("tunnel mode "):]
                )

                continue

            # ----------------------------------
            # Tunnel Key
            # ----------------------------------

            if line.startswith("tunnel key "):

                interface["tunnel_key"] = self._safe_int(
                    line.split()[-1]
                )

                continue

            # ----------------------------------
            # Tunnel VRF
            # ----------------------------------

            if line.startswith("tunnel vrf "):

                interface["tunnel_vrf"] = self._clean_string(
                    line[len("tunnel vrf "):]
                )

                continue

            # ----------------------------------
            # Tunnel Protection
            # ----------------------------------

            if line.startswith("tunnel protection "):

                interface["tunnel_protection"] = self._clean_string(
                    line[len("tunnel protection "):]
                )

                continue

            # ----------------------------------
            # IP Source Guard
            # ----------------------------------

            if line == "ip verify source":

                interface["ip_verify_source"] = True

                continue

            # ----------------------------------
            # DHCP Snooping Trust
            # ----------------------------------

            if line == "ip dhcp snooping trust":

                interface["dhcp_snooping_trust"] = True

                continue

            # ----------------------------------
            # Dynamic ARP Inspection Trust
            # ----------------------------------

            if line == "ip arp inspection trust":

                interface["arp_inspection_trust"] = True

                continue

    # ==============================================================
    # Phase 5 Placeholder
    # ==============================================================

    def _parse_operational(self, block, interface):
        """
        Parse operational interface settings.
        """

        for raw_line in block[1:]:

            line = raw_line.strip()

            # ----------------------------
            # Keepalive
            # ----------------------------

            if line == "no keepalive":

                interface["keepalive"] = False
                continue

            if line.startswith("keepalive "):

                tokens = line.split()

                interface["keepalive"] = True

                if len(tokens) >= 2:
                    interface["keepalive_period"] = self._safe_int(tokens[1])

                if len(tokens) >= 3:
                    interface["keepalive_retry"] = self._safe_int(tokens[2])

                continue

            # ----------------------------
            # Load Interval
            # ----------------------------

            if line.startswith("load-interval "):

                interface["load_interval"] = self._safe_int(
                    line.split()[-1]
                )

                continue

            # ----------------------------
            # Carrier Delay
            # ----------------------------

            if line.startswith("carrier-delay "):

                interface["carrier_delay"] = self._clean_string(
                    line[len("carrier-delay "):]
                )

                continue

            # ----------------------------
            # Logging Events
            # ----------------------------

            if line.startswith("logging event "):

                interface["logging_events"].append(
                    self._clean_string(
                        line[len("logging event "):]
                    )
                )

                continue

            # ----------------------------
            # CDP
            # ----------------------------

            if line == "no cdp enable":

                interface["cdp_enabled"] = False

                continue

            # ----------------------------
            # LLDP
            # ----------------------------

            if line == "no lldp transmit":

                interface["lldp_transmit"] = False

                continue

            if line == "no lldp receive":

                interface["lldp_receive"] = False

                continue

    # ==============================================================
    # Phase 6 Placeholder
    # ==============================================================

    def _parse_qos(self, block, interface):
        """
        Parse interface QoS configuration.
        """

        for raw_line in block[1:]:

            line = raw_line.strip()

            # ----------------------------
            # Service Policy Input
            # ----------------------------

            if line.startswith("service-policy input "):

                interface["service_policy_input"] = (
                    self._clean_string(
                        line[len("service-policy input "):]
                    )
                )

                continue

            # ----------------------------
            # Service Policy Output
            # ----------------------------

            if line.startswith("service-policy output "):

                interface["service_policy_output"] = (
                    self._clean_string(
                        line[len("service-policy output "):]
                    )
                )

                continue

            # ----------------------------
            # QoS Trust
            # ----------------------------

            if line.startswith("mls qos trust "):

                interface["qos_trust"] = (
                    self._clean_string(
                        line[len("mls qos trust "):]
                    )
                )

                continue

            # ----------------------------
            # Priority Queue
            # ----------------------------

            if line == "priority-queue out":

                interface["priority_queue"] = True

                continue

            # ----------------------------
            # Traffic Shaping
            # ----------------------------

            if line.startswith("shape average "):

                interface["shape_average"] = (
                    self._safe_int(
                        line.split()[-1]
                    )
                )

                continue

            # ----------------------------
            # Policing
            # ----------------------------

            if line.startswith("police "):

                tokens = line.split()

                if len(tokens) >= 2:

                    interface["police_rate"] = (
                        self._safe_int(tokens[1])
                    )

                continue
    

    def _validate_interface(self, interface):
        """
        Validate a parsed interface.

        Validation should never modify parser output.
        It only records warnings/errors.
        """

        self._validate_layer3(interface)

        self._validate_layer2(interface)

        self._validate_security(interface)

        self._validate_tunnel(interface)

        self._validate_qos(interface)


    def _validate_layer3(self, interface):

        name = interface["name"]

        #
        # Primary IP without mask
        #

        if interface["ip_address"] and not interface["subnet_mask"]:

            self.statistics["validation_results"].append(

                f"{name}: IP address missing subnet mask"

            )

        #
        # Duplicate helper addresses
        #

        helpers = interface["helper_addresses"]

        if len(helpers) != len(set(helpers)):

            self.statistics["validation_results"].append(

                f"{name}: Duplicate helper addresses"

            )

        #
        # Unnumbered with IP address
        #

        if (

            interface["unnumbered_interface"]

            and

            interface["ip_address"]

        ):

            self.statistics["validation_results"].append(

                f"{name}: Interface has both IP address and unnumbered configuration"

            )

    def _validate_layer2(self, interface):

        name = interface["name"]

        #
        # Access VLAN on routed interface
        #

        if (
                interface["semantic"]["is_switchport"] is False
                and
                interface["access_vlan"]
            ):

            self.statistics["validation_results"].append(

                f"{name}: Access VLAN configured on routed interface"

            )

        #
        # Access mode with trunk VLANs
        #

        if (

            interface["switchport_mode"] == "access"

            and

            interface["allowed_vlans"]

        ):

            self.statistics["validation_results"].append(

                f"{name}: Access port contains trunk VLAN configuration"

            )

        #
        # Trunk mode without allowed VLANs
        #

        if (

            interface["switchport_mode"] == "trunk"

            and

            not interface["allowed_vlans"]

        ):

            self.statistics["validation_results"].append(

                f"{name}: Trunk interface has no allowed VLANs configured"

            )

    def _validate_security(self, interface):

        name = interface["name"]

        #
        # ACL direction mismatch
        #

        if (

            interface["inbound_acl"]

            ==

            interface["outbound_acl"]

            and

            interface["inbound_acl"]

        ):

            self.statistics["validation_results"].append(

                f"{name}: Same ACL used in both directions"

            )

        #
        # Zone without ACL
        #

        if (

            interface["zone_member"]

            and

            not (

                interface["inbound_acl"]

                or

                interface["outbound_acl"]

            )

        ):

            self.statistics["validation_results"].append(

                f"{name}: Zone member configured without interface ACL"

            )

    def _validate_tunnel(self, interface):

        name = interface["name"]

        #
        # Tunnel source
        #

        if interface["tunnel_source"] and not interface["tunnel_destination"]:

            self.statistics["validation_results"].append(

                f"{name}: Tunnel source configured without destination"

            )

        #
        # Tunnel destination
        #

        if interface["tunnel_destination"] and not interface["tunnel_source"]:

            self.statistics["validation_results"].append(

                f"{name}: Tunnel destination configured without source"

            )

        #
        # Tunnel mode
        #

        if (

            interface["tunnel_mode"]

            and

            not interface["tunnel_source"]

        ):

            self.statistics["validation_results"].append(

                f"{name}: Tunnel mode configured before tunnel source"

            )

    def _validate_qos(self, interface):

        name = interface["name"]

        #
        # Output policy without input
        #

        if (

            interface["service_policy_output"]

            and

            not interface["service_policy_input"]

        ):

            self.statistics["validation_results"].append(

                f"{name}: Output QoS policy detected. Review whether an input policy is also required."

            )

        #
        # Shape smaller than police
        #

        if (

            interface["shape_average"]

            and

            interface["police_rate"]

            and

            interface["shape_average"]

            <

            interface["police_rate"]

        ):

            self.statistics["validation_results"].append(

                f"{name}: Shaping rate lower than policing rate"

            )
    # ==============================================================
    # Final Processing
    # ==============================================================

    def _finalize(self, interfaces):

        for interface in interfaces:

            interface["helper_addresses"] = sorted(
                self._deduplicate(
                    interface["helper_addresses"]
                )
            )

            interface["allowed_vlans"] = sorted(
                self._deduplicate(
                    interface["allowed_vlans"]
                )
            )

        self.statistics["interfaces"] = len(
            interfaces
        )

        logger.info(
            "Parsed %d interfaces",
            len(interfaces)
        )

        for interface in interfaces:

            self._normalize_interface(interface)

            self._build_semantic_metadata(interface)

            if interface["physical"]:
                self.statistics["physical"] += 1

            if interface["loopback"]:
                self.statistics["loopbacks"] += 1

            if interface["svi"]:
                self.statistics["svis"] += 1

            if interface["tunnel"]:
                self.statistics["tunnels"] += 1

            if interface["port_channel"]:
                self.statistics["port_channels"] += 1

            if interface["semantic"]["is_switchport"]:
                self.statistics["switchports"] += 1

            if interface["semantic"]["is_routed"]:
                self.statistics["routed"] += 1

            if interface["semantic"]["is_trunk"]:
                self.statistics["trunks"] += 1

            if interface["semantic"]["is_access"]:
                self.statistics["access_ports"] += 1

            if interface["semantic"]["has_qos"]:
                self.statistics["qos_interfaces"] += 1

            if interface["semantic"]["has_acl"]:
                self.statistics["acl_interfaces"] += 1

            self._validate_interface(interface)

            self._generate_semantic_hash(interface)

        self.statistics["validation_failures"] = len(
            self.statistics["validation_results"]
        )
        
        interfaces.sort(
            key=lambda x: x["name"]
        )

        return interfaces