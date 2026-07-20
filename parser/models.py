"""
====================================================================
File: models.py

Project : ConfigVista AI

Purpose
-------
Common data models used by the configuration parser.

====================================================================
"""

from dataclasses import dataclass, field
from typing import List, Optional


# ==============================================================
# Device Metadata
# ==============================================================

@dataclass
class DeviceMetadata:

    hostname: Optional[str] = None

    device_role: Optional[str] = None

    vendor: Optional[str] = None

    model: Optional[str] = None

    site: Optional[str] = None

    environment: Optional[str] = None


# ==============================================================
# Interface
# ==============================================================

@dataclass
class Interface:

    name: str

    description: str = ""

    ip_address: Optional[str] = None

    subnet_mask: Optional[str] = None

    shutdown: bool = False

    vrf: Optional[str] = None

    switchport_mode: Optional[str] = None

    access_vlan: Optional[int] = None

    trunk_vlans: List[int] = field(
        default_factory=list
    )


# ==============================================================
# Routing
# ==============================================================

@dataclass
class OspfProcess:

    process_id: str

    router_id: Optional[str] = None

    areas: List[str] = field(
        default_factory=list
    )


@dataclass
class BgpNeighbor:

    neighbor_ip: str

    remote_as: str

    update_source: Optional[str] = None

    route_map_in: Optional[str] = None

    route_map_out: Optional[str] = None


@dataclass
class StaticRoute:

    network: str

    mask: str

    next_hop: str


# ==============================================================
# Switching
# ==============================================================

@dataclass
class VLAN:

    vlan_id: int

    name: str = ""


@dataclass
class HSRPGroup:

    group_id: int

    virtual_ip: Optional[str] = None

    priority: Optional[int] = None

    preempt: bool = False


# ==============================================================
# Security
# ==============================================================

@dataclass
class ACL:

    name: str

    acl_type: str = "extended"


@dataclass
class RouteMap:

    name: str


@dataclass
class PrefixList:

    name: str


# ==============================================================
# Management
# ==============================================================

@dataclass
class Management:

    # -------------------------
    # Management Servers
    # -------------------------

    ntp_servers: List[str] = field(
        default_factory=list
    )

    logging_servers: List[str] = field(
        default_factory=list
    )

    dns_servers: List[str] = field(
        default_factory=list
    )

    domain_name: str = ""

    # -------------------------
    # Security Services
    # -------------------------

    aaa_enabled: bool = False

    ssh_enabled: bool = False

    snmp_enabled: bool = False

    # -------------------------
    # Switching Services
    # -------------------------

    stp_mode: Optional[str] = None

    dhcp_snooping: bool = False

    port_security: bool = False

    # -------------------------
    # Infrastructure Services
    # -------------------------

    ip_sla_enabled: bool = False

    track_objects: List[int] = field(
        default_factory=list
    )

    logging_buffered: bool = False

    service_timestamps: bool = False

    # -------------------------
    # Device Management
    # -------------------------

    archive_enabled: bool = False

    banner_configured: bool = False

    local_users: List[str] = field(
        default_factory=list
    )


@dataclass
class ParseStatistics:

    total_lines: int = 0

    parsed_objects: int = 0

    warnings: List[str] = field(
        default_factory=list
    )

    unsupported_commands: List[str] = field(
        default_factory=list
    )
    
# ==============================================================
# Parsed Configuration
# ==============================================================

@dataclass
class ParsedConfiguration:

    # -------------------------
    # Metadata
    # -------------------------

    metadata: DeviceMetadata = field(
        default_factory=DeviceMetadata
    )

    # -------------------------
    # Interfaces
    # -------------------------

    interfaces: List[Interface] = field(
        default_factory=list
    )

    # -------------------------
    # Switching
    # -------------------------

    vlans: List[VLAN] = field(
        default_factory=list
    )

    hsrp_groups: List[HSRPGroup] = field(
        default_factory=list
    )

    # -------------------------
    # Routing
    # -------------------------

    ospf_processes: List[OspfProcess] = field(
        default_factory=list
    )

    bgp_neighbors: List[BgpNeighbor] = field(
        default_factory=list
    )

    static_routes: List[StaticRoute] = field(
        default_factory=list
    )

    vrfs: List[str] = field(
        default_factory=list
    )

    # -------------------------
    # Security
    # -------------------------

    acls: List[ACL] = field(
        default_factory=list
    )

    route_maps: List[RouteMap] = field(
        default_factory=list
    )

    prefix_lists: List[PrefixList] = field(
        default_factory=list
    )

    # -------------------------
    # Management
    # -------------------------

    management: Management = field(
        default_factory=Management
    )

    statistics: ParseStatistics = field(
        default_factory=ParseStatistics
    )

