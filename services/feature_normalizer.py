"""
feature_normalizer.py

Converts raw parser output into the canonical FeatureModel.

Responsibilities
----------------
1. Merge parser outputs
2. Normalize field names
3. Populate defaults
4. Calculate derived features
5. Validate features
6. Return FeatureModel
"""

from typing import Dict, Any

from models.feature_model import FeatureModel


class FeatureNormalizer:

    def normalize(self, parsed_data: Dict[str, Any]) -> FeatureModel:
        """
        Convert parser output into FeatureModel.
        """

        feature = FeatureModel()

        self._normalize_metadata(feature, parsed_data)
        self._normalize_interfaces(feature, parsed_data)
        self._normalize_routing(feature, parsed_data)
        self._normalize_switching(feature, parsed_data)
        self._normalize_security(feature, parsed_data)
        self._normalize_management(feature, parsed_data)
        self._normalize_services(feature, parsed_data)

        self._calculate_derived_features(feature)

        self._validate(feature)

        return feature

    # ==========================================================
    # Metadata
    # ==========================================================

    def _normalize_metadata(
        self,
        feature: FeatureModel,
        data: Dict[str, Any],
    ):

        feature.hostname = data.get("hostname", "")

        feature.vendor = data.get("vendor", "")

        feature.model = data.get("model", "")

        feature.os_version = data.get("os_version", "")

        feature.serial_number = data.get("serial_number", "")

        feature.device_role = data.get("device_role", "Unknown")

        feature.site = data.get("site", "")

        feature.environment = data.get("environment", "Unknown")

        feature.criticality = data.get("criticality", "Medium")

    # ==========================================================
    # Interfaces
    # ==========================================================

    def _normalize_interfaces(
        self,
        feature: FeatureModel,
        data: Dict[str, Any],
    ):

        interfaces = data.get("interfaces", [])

        feature.interface_count = len(interfaces)

        loopbacks = [
            i for i in interfaces
            if "loopback" in i.lower()
        ]

        feature.loopback_count = len(loopbacks)

        portchannels = [
            i for i in interfaces
            if "port-channel" in i.lower()
            or "portchannel" in i.lower()
        ]

        feature.portchannel_count = len(portchannels)

    # ==========================================================
    # Routing
    # ==========================================================

    def _normalize_routing(
        self,
        feature: FeatureModel,
        data: Dict[str, Any],
    ):

        ospf = data.get("ospf", {})

        bgp = data.get("bgp", {})

        eigrp = data.get("eigrp", {})

        static_routes = data.get("static_routes", [])

        vrfs = data.get("vrfs", [])

        feature.has_ospf = bool(ospf)

        feature.has_bgp = bool(bgp)

        feature.has_eigrp = bool(eigrp)

        feature.has_static_routes = len(static_routes) > 0

        feature.has_vrf = len(vrfs) > 0

        feature.static_route_count = len(static_routes)

        feature.vrf_count = len(vrfs)

        feature.ospf_neighbor_count = len(
            ospf.get("neighbors", [])
        )

        feature.bgp_neighbor_count = len(
            bgp.get("neighbors", [])
        )

    # ==========================================================
    # Switching
    # ==========================================================

    def _normalize_switching(
        self,
        feature: FeatureModel,
        data: Dict[str, Any],
    ):

        vlans = data.get("vlans", [])

        feature.vlan_count = len(vlans)

        feature.has_vlan = len(vlans) > 0

        feature.has_stp = bool(data.get("stp"))

        feature.has_hsrp = bool(data.get("hsrp"))

        feature.has_port_security = bool(
            data.get("port_security")
        )

        feature.has_etherchannel = bool(
            data.get("etherchannel")
        )

    # ==========================================================
    # Security
    # ==========================================================

    def _normalize_security(
        self,
        feature: FeatureModel,
        data: Dict[str, Any],
    ):

        acls = data.get("acls", [])

        feature.acl_count = len(acls)

        feature.has_acl = len(acls) > 0

        feature.has_aaa = bool(data.get("aaa"))

        feature.has_ssh = bool(data.get("ssh"))

        feature.has_nat = bool(data.get("nat"))

    # ==========================================================
    # Management
    # ==========================================================

    def _normalize_management(
        self,
        feature: FeatureModel,
        data: Dict[str, Any],
    ):

        feature.has_snmp = bool(data.get("snmp"))

        feature.has_syslog = bool(data.get("syslog"))

        feature.has_ntp = bool(data.get("ntp"))

    # ==========================================================
    # Services
    # ==========================================================

    def _normalize_services(
        self,
        feature: FeatureModel,
        data: Dict[str, Any],
    ):

        feature.has_qos = bool(data.get("qos"))

        feature.has_dhcp_helper = bool(
            data.get("dhcp_helper")
        )

        feature.has_netflow = bool(
            data.get("netflow")
        )

        feature.has_ip_sla = bool(
            data.get("ip_sla")
        )

        feature.has_vpn = bool(
            data.get("vpn")
        )

    # ==========================================================
    # Derived Features
    # ==========================================================

    def _calculate_derived_features(
        self,
        feature: FeatureModel,
    ):
        """
        Placeholder for calculated fields.

        Future examples:

        - routing_complexity
        - security_score
        - configuration_density
        - protocol_count
        """

        pass

    # ==========================================================
    # Validation
    # ==========================================================

    def _validate(
        self,
        feature: FeatureModel,
    ):

        if feature.interface_count < 0:
            feature.interface_count = 0

        if feature.vlan_count < 0:
            feature.vlan_count = 0

        if feature.acl_count < 0:
            feature.acl_count = 0

        if feature.hostname is None:
            feature.hostname = ""

    # ==========================================================
    # Convenience
    # ==========================================================

    def normalize_to_dict(
        self,
        parsed_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Returns normalized features as dictionary.

        Useful for:

        - SQLite

        - Pandas

        - ML Dataset

        - JSON export
        """

        return self.normalize(parsed_data).to_dict()