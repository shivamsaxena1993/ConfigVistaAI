"""
====================================================================
File: feature_validator.py

Project : ConfigVista AI

Purpose
-------
Validates and normalizes extracted features before they are
consumed by the Risk Engine.

Responsibilities
----------------
1. Ensure required fields exist
2. Apply default values
3. Prevent invalid values
4. Normalize data types
5. Support both dict and FeatureModel inputs

====================================================================
"""

from copy import deepcopy


class FeatureValidator:
    """
    Validates extracted configuration features.

    Returns:
        dict
    """

    # ----------------------------------------------------------
    # Required schema with default values
    # ----------------------------------------------------------

    DEFAULTS = {

        # Device
        "hostname": "Unknown",
        "vendor": "Unknown",
        "model": "Unknown",

        # Interfaces
        "interface_count": 0,

        # Routing
        "has_bgp": False,
        "has_ospf": False,
        "has_eigrp": False,
        "has_rip": False,
        "static_route_count": 0,

        # Switching
        "vlan_count": 0,
        "vrf_count": 0,

        # Security
        "acl_count": 0,
        "has_nat": False,
        "has_vpn": False,
        "has_qos": False,

        # Management
        "has_snmp": False,
        "has_aaa": False,
        "has_ssh": False,

        # Derived
        "routing_protocol_count": 0,
        "security_feature_count": 0,
        "management_feature_count": 0,
        "complexity_score": 0,
    }

    BOOLEAN_FIELDS = {

        "has_bgp",
        "has_ospf",
        "has_eigrp",
        "has_rip",
        "has_nat",
        "has_vpn",
        "has_qos",
        "has_snmp",
        "has_aaa",
        "has_ssh",
    }

    NUMERIC_FIELDS = {

        "interface_count",
        "static_route_count",
        "vlan_count",
        "vrf_count",
        "acl_count",
        "routing_protocol_count",
        "security_feature_count",
        "management_feature_count",
        "complexity_score",
    }

    # ----------------------------------------------------------

    @classmethod
    def validate(cls, features):
        """
        Validate extracted features.

        Parameters
        ----------
        features : dict | FeatureModel

        Returns
        -------
        dict
        """

        # Convert FeatureModel if required

        if hasattr(features, "to_dict"):
            features = features.to_dict()

        validated = deepcopy(cls.DEFAULTS)

        validated.update(features)

        # ------------------------------
        # Normalize Boolean Fields
        # ------------------------------

        for field in cls.BOOLEAN_FIELDS:
            validated[field] = bool(validated.get(field, False))

        # ------------------------------
        # Normalize Numeric Fields
        # ------------------------------

        for field in cls.NUMERIC_FIELDS:

            value = validated.get(field, 0)

            try:
                value = int(value)
            except Exception:
                value = 0

            if value < 0:
                value = 0

            validated[field] = value

        # ------------------------------
        # Normalize Strings
        # ------------------------------

        validated["hostname"] = str(
            validated.get("hostname", "Unknown")
        )

        validated["vendor"] = str(
            validated.get("vendor", "Unknown")
        )

        validated["model"] = str(
            validated.get("model", "Unknown")
        )

        # ------------------------------
        # Recalculate Derived Values
        # ------------------------------

        validated["routing_protocol_count"] = sum([

            validated["has_bgp"],

            validated["has_ospf"],

            validated["has_eigrp"],

            validated["has_rip"]

        ])

        validated["security_feature_count"] = sum([

            validated["acl_count"] > 0,

            validated["has_nat"],

            validated["has_vpn"]

        ])

        validated["management_feature_count"] = sum([

            validated["has_snmp"],

            validated["has_aaa"],

            validated["has_ssh"]

        ])

        return validated