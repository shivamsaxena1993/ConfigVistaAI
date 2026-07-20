"""
====================================================================
File: feature_extractor.py

Project : ConfigVista AI

Purpose
-------
Converts parsed configuration data into the canonical FeatureModel
and exposes a dictionary representation for backward compatibility.

This is the single feature engineering layer used by:

    Parser
        ↓
    FeatureExtractor
        ↓
    FeatureModel
        ↓
    Risk Engine
        ↓
    Recommendation Engine

====================================================================
"""

from typing import Dict, Any

from models.feature_model import FeatureModel


class FeatureExtractor:

    def __init__(self, parsed_data: Dict[str, Any]):
        self.data = parsed_data

    def _count(self, key: str) -> int:
        value = self.data.get(key, [])

        if isinstance(value, list):
            return len(value)

        return int(bool(value))

    def extract(self) -> Dict[str, Any]:

        feature = FeatureModel()

        # ======================================================
        # Metadata
        # ======================================================

        feature.hostname = self.data.get("hostname", "")
        feature.device_role = self.data.get("device_role", "Unknown")
        feature.vendor = self.data.get("vendor", "Cisco")
        feature.model = self.data.get("platform", "")

        # ======================================================
        # Inventory
        # ======================================================

        feature.interface_count = self.data.get(
            "interface_count",
            self._count("interfaces"),
        )

        feature.loopback_count = self.data.get(
            "loopback_count",
            self._count("loopbacks"),
        )

        feature.portchannel_count = self.data.get(
            "port_channel_count",
            self._count("port_channel_interfaces"),
        )

        # ======================================================
        # Routing
        # ======================================================

        protocols = {
            p.upper()
            for p in self.data.get("routing_protocols", [])
        }

        feature.has_ospf = "OSPF" in protocols
        feature.has_bgp = "BGP" in protocols
        feature.has_eigrp = "EIGRP" in protocols
        feature.has_rip = "RIP" in protocols
        feature.has_static_routes = (
            self._count("static_routes") > 0
        )

        feature.ospf_neighbor_count = self._count(
            "ospf_neighbors"
        )

        feature.bgp_neighbor_count = self.data.get(
            "bgp_neighbor_count",
            self._count("bgp_neighbors"),
        )

        feature.static_route_count = self._count(
            "static_routes"
        )

        feature.vrf_count = self._count("vrfs")

        feature.has_vrf = feature.vrf_count > 0

        # ======================================================
        # Switching
        # ======================================================

        feature.vlan_count = self._count("vlans")

        feature.has_vlan = feature.vlan_count > 0

        feature.has_hsrp = (
            self._count("hsrp_groups") > 0
        )

        feature.has_stp = (
            self.data.get("stp_mode") is not None
        )

        # ======================================================
        # Security
        # ======================================================

        feature.acl_count = self._count("acl_names")

        feature.has_acl = feature.acl_count > 0

        feature.has_nat = self.data.get(
            "nat_enabled",
            False,
        )

        feature.has_aaa = self.data.get(
            "aaa_enabled",
            False,
        )

        feature.has_ssh = self.data.get(
            "ssh_enabled",
            False,
        )

        feature.has_vpn = self.data.get(
            "vpn_enabled",
            False,
        )

        # ======================================================
        # Management
        # ======================================================

        feature.has_snmp = self.data.get(
            "snmp_enabled",
            False,
        )

        feature.has_ntp = (
            self._count("ntp_servers") > 0
        )

        feature.has_syslog = (
            self._count("logging_hosts") > 0
            or self._count("logging_servers") > 0
        )

        # ======================================================
        # Services
        # ======================================================

        feature.has_qos = (
            self._count("policy_maps") > 0
        )

        feature.has_dhcp_helper = (
            self._count("dhcp_helpers") > 0
        )

        feature.has_netflow = self.data.get(
            "netflow_enabled",
            False,
        )

        feature.has_ip_sla = (
            self._count("ip_sla_operations") > 0
        )

        # ======================================================
        # Derived Values
        # ======================================================

        protocol_count = sum(
            [
                feature.has_ospf,
                feature.has_bgp,
                feature.has_eigrp,
                feature.has_static_routes,
            ]
        )

        security_feature_count = sum(
            [
                feature.has_acl,
                feature.has_nat,
                feature.has_vpn,
                feature.has_aaa,
                feature.has_ssh,
                feature.has_snmp,
            ]
        )

        management_feature_count = sum(
            [
                feature.has_ntp,
                feature.has_syslog,
                feature.has_snmp,
                feature.has_ssh,
            ]
        )

        complexity = (
            feature.interface_count
            + feature.vlan_count
            + protocol_count * 5
            + feature.bgp_neighbor_count * 2
            + feature.acl_count
        )

        feature_dict = feature.to_dict()

        # ======================================================
        # Backward Compatibility
        # ======================================================

        feature_dict.update({

            "routing_protocol_count": protocol_count,

            "security_feature_count": security_feature_count,

            "management_feature_count": management_feature_count,

            "complexity_score": min(100, complexity),

            # -------------------------------------------------
            # Canonical / Legacy Compatibility
            # -------------------------------------------------

            "routing_bgp": int(feature.has_bgp),
            "routing_ospf": int(feature.has_ospf),
            "routing_eigrp": int(feature.has_eigrp),
            "routing_rip": int(feature.has_rip),

            "nat_enabled": int(feature.has_nat),
            "vpn_enabled": int(feature.has_vpn),
            "snmp_enabled": int(feature.has_snmp),
            "aaa_enabled": int(feature.has_aaa),
            "ssh_enabled": int(feature.has_ssh),

            # Additional features required by RiskEngine
            "has_rip": feature.has_rip,
            "route_map_count": self._count("route_maps"),

        })

        return feature_dict