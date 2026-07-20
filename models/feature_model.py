"""
feature_model.py

Canonical Feature Model for ConfigVista AI.

This dataclass defines the standard feature contract shared between:
    - Parser Framework
    - Feature Normalizer
    - Change Comparison Engine
    - Risk Engine
    - Machine Learning Pipeline
    - Streamlit Dashboard

Every assessment should use this model rather than raw dictionaries.
"""

from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any


@dataclass
class FeatureModel:
    """
    Canonical feature model.
    """

    # ==========================================================
    # Device Metadata
    # ==========================================================
    hostname: str = ""
    device_role: str = "Unknown"
    vendor: str = ""
    model: str = ""
    os_version: str = ""
    serial_number: str = ""

    site: str = ""
    environment: str = "Unknown"
    criticality: str = "Medium"

    # ==========================================================
    # Interface Features
    # ==========================================================
    interface_count: int = 0
    loopback_count: int = 0
    portchannel_count: int = 0

    # ==========================================================
    # Routing Features
    # ==========================================================
    has_ospf: bool = False
    has_bgp: bool = False
    has_eigrp: bool = False
    has_rip: bool = False
    has_static_routes: bool = False
    has_vrf: bool = False

    ospf_neighbor_count: int = 0
    bgp_neighbor_count: int = 0
    static_route_count: int = 0
    vrf_count: int = 0

    # ==========================================================
    # Switching Features
    # ==========================================================
    has_vlan: bool = False
    has_stp: bool = False
    has_hsrp: bool = False
    has_port_security: bool = False
    has_etherchannel: bool = False

    vlan_count: int = 0

    # ==========================================================
    # Security Features
    # ==========================================================
    has_acl: bool = False
    has_aaa: bool = False
    has_ssh: bool = False
    has_nat: bool = False

    acl_count: int = 0

    # ==========================================================
    # Management Features
    # ==========================================================
    has_snmp: bool = False
    has_syslog: bool = False
    has_ntp: bool = False

    # ==========================================================
    # Service Features
    # ==========================================================
    has_qos: bool = False
    has_dhcp_helper: bool = False
    has_netflow: bool = False
    has_ip_sla: bool = False
    has_vpn: bool = False

    # ==========================================================
    # Future Telemetry (Optional)
    # ==========================================================
    cpu_utilization: Optional[float] = None
    memory_utilization: Optional[float] = None

    interface_errors: int = 0
    active_alerts: int = 0

    # ==========================================================
    # Historical Intelligence (Future)
    # ==========================================================
    previous_failures: int = 0
    previous_rollbacks: int = 0
    similar_change_count: int = 0
    similar_change_success_rate: float = 0.0

    # ==========================================================
    # Change Metadata (Future)
    # ==========================================================
    devices_in_change: int = 1
    change_type: str = "Standard"
    maintenance_window: str = ""
    rollback_available: bool = False

    # ==========================================================
    # ML Output (Future)
    # ==========================================================
    predicted_risk: Optional[str] = None
    risk_score: Optional[float] = None
    confidence_score: Optional[float] = None

    # ==========================================================
    # Helper Methods
    # ==========================================================
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert dataclass to dictionary.
        """
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FeatureModel":
        """
        Create FeatureModel from dictionary.
        Unknown keys are ignored.
        """

        valid_fields = cls.__dataclass_fields__.keys()

        filtered = {
            k: v
            for k, v in data.items()
            if k in valid_fields
        }

        return cls(**filtered)

    def update(self, values: Dict[str, Any]) -> None:
        """
        Update existing FeatureModel using dictionary values.
        Unknown keys are ignored.
        """

        for key, value in values.items():
            if hasattr(self, key):
                setattr(self, key, value)