"""
=============================================================
ConfigVista AI
Enterprise Domain Models

Artifact-2
Part 1

Enterprise Digital Twin Core

Author : Shivam Saxena
Project: ConfigVista AI
=============================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, UTC
from itertools import count
from typing import Optional
from typing import NewType

from enterprise.constants import (
    InterfaceLayer,
    InterfaceStatus,
    InterfaceType,
    ENTERPRISE_NAME,
    COUNTRY,
    INDUSTRY,
    TIMEZONE,
    DATASET_VERSION,
    GENERATOR_VERSION,
)

# ============================================================
# STRONGLY TYPED IDENTIFIERS
# ============================================================

DeviceId = NewType("DeviceId", str)
SiteId = NewType("SiteId", str)
InterfaceId = NewType("InterfaceId", str)
ChangeId = NewType("ChangeId", str)
IncidentId = NewType("IncidentId", str)
BusinessServiceId = NewType("BusinessServiceId", str)
TopologyLinkId = NewType("TopologyLinkId", str)
ConfigurationSnapshotId = NewType(
    "ConfigurationSnapshotId",
    str
)

OperationalSnapshotId = NewType(
    "OperationalSnapshotId",
    str
)

FeatureVectorId = NewType(
    "FeatureVectorId",
    str
)

ConfigurationBackupId = NewType(
    "ConfigurationBackupId",
    str,
)

# ============================================================
# ID GENERATORS
# ============================================================


_DEVICE_COUNTER = count(1)
_SITE_COUNTER = count(1)
_CHANGE_COUNTER = count(1)
_INCIDENT_COUNTER = count(1)
_SERVICE_COUNTER = count(1)
_TOPOLOGY_COUNTER = count(1)
_CONFIGURATION_BACKUP_COUNTER = count(1)
_INTERFACE_COUNTER = count(1)
_CONFIG_COUNTER = count(1)
_OPERATION_COUNTER = count(1)
_FEATURE_COUNTER = count(1)


def generate_device_id() -> DeviceId:
    return DeviceId(f"DEV-{next(_DEVICE_COUNTER):06d}")

def generate_site_id() -> SiteId:

    return SiteId(
        f"SITE-{next(_SITE_COUNTER):06d}"
    )

def generate_change_id() -> ChangeId:
    return ChangeId(f"CHG-{next(_CHANGE_COUNTER):06d}")


def generate_configuration_backup_id(
) -> ConfigurationBackupId:

    return ConfigurationBackupId(

        f"CFG-{next(_CONFIGURATION_BACKUP_COUNTER):06d}"

    )

def generate_incident_id() -> IncidentId:
    return IncidentId(f"INC-{next(_INCIDENT_COUNTER):06d}")


def generate_business_service_id() -> BusinessServiceId:
    return BusinessServiceId(f"SRV-{next(_SERVICE_COUNTER):06d}")

def generate_topology_link_id() -> TopologyLinkId:
    return TopologyLinkId(f"LNK-{next(_TOPOLOGY_COUNTER):06d}")

def generate_feature_vector_id() -> FeatureVectorId:

    return FeatureVectorId(

        f"FV-{next(_FEATURE_COUNTER):06d}"

    )

def generate_interface_id() -> str:
    return f"IF-{next(_INTERFACE_COUNTER):06d}"


def generate_configuration_snapshot_id(
) -> ConfigurationSnapshotId:

    return ConfigurationSnapshotId(
        f"CFG-{next(_CONFIG_COUNTER):06d}"
    )


def generate_operational_snapshot_id(
) -> OperationalSnapshotId:

    return OperationalSnapshotId(
        f"OPS-{next(_OPERATION_COUNTER):06d}"
    )

# ============================================================
# DEVICE ROLE MAPPING
# ============================================================

DEVICE_ROLE_MAPPING = {

    "CORE": "CORE",

    "DIST": "DISTRIBUTION",

    "ACCESS": "ACCESS",

    "FW": "FIREWALL",

    "WAN": "WAN",

}

# ============================================================
# BASE MODEL
# ============================================================


@dataclass(slots=True)
class BaseModel:
    """
    Common functionality shared by all enterprise objects.
    """

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    updated_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    def to_dict(self):
        return asdict(self)

    def touch(self):
        self.updated_at = datetime.now(UTC)

    def __str__(self):
        return f"{self.__class__.__name__}({self.to_dict()})"


# ============================================================
# ENTERPRISE METADATA
# ============================================================


@dataclass(slots=True)
class EnterpriseMetadata(BaseModel):

    enterprise_name: str = ENTERPRISE_NAME

    country: str = COUNTRY

    industry: str = INDUSTRY

    timezone: str = TIMEZONE

    dataset_version: str = DATASET_VERSION

    generator_version: str = GENERATOR_VERSION


# ============================================================
# ENTERPRISE STATISTICS
# ============================================================


@dataclass(slots=True)
class EnterpriseStatistics(BaseModel):

    total_sites: int = 0

    total_devices: int = 0

    total_interfaces: int = 0

    total_topology_links: int = 0

    total_business_services: int = 0

    total_configuration_snapshots: int = 0

    total_configuration_backups: int = 0

    total_operational_snapshots: int = 0

    total_changes: int = 0

    total_incidents: int = 0


# ============================================================
# INTERFACE
# ============================================================


@dataclass(slots=True)
class Interface(BaseModel):

    interface_id: str = field(
        default_factory=generate_interface_id
    )

    name: str = ""

    interface_type: InterfaceType = InterfaceType.PHYSICAL

    layer: InterfaceLayer = InterfaceLayer.LAYER3

    description: str = ""

    admin_status: InterfaceStatus = InterfaceStatus.UP

    operational_status: InterfaceStatus = InterfaceStatus.UP

    mtu: int = 1500

    speed: str = "1G"

    vrf: str = "default"

    vlan: Optional[int] = None

    ip_address: Optional[str] = None

    subnet_mask: Optional[str] = None

    mac_address: Optional[str] = None

    neighbor_device: Optional[str] = None

    neighbor_interface: Optional[str] = None

    device_id: DeviceId | None = None

    def __post_init__(self):

        if self.mtu <= 0:
            raise ValueError("MTU must be greater than zero")

        if self.vlan is not None:

            if not (1 <= self.vlan <= 4094):
                raise ValueError(
                    "VLAN must be between 1 and 4094"
                )


# ============================================================
# CONFIGURATION SNAPSHOT
# ============================================================


@dataclass(slots=True)
class ConfigurationSnapshot(BaseModel):

    snapshot_id: ConfigurationSnapshotId = field(
        default_factory=generate_configuration_snapshot_id
    )

    configuration_version: int = 1

    configuration_hash: str = ""

    parser_version: str = "3.0"

    configuration_text: str = ""

    def __post_init__(self):

        if self.configuration_version <= 0:
            raise ValueError(
                "Configuration version must be positive"
            )



# ============================================================
# OPERATIONAL SNAPSHOT
# ============================================================

@dataclass(slots=True)
class OperationalSnapshot(BaseModel):

    # --------------------------------------------------------
    # Identity
    # --------------------------------------------------------

    snapshot_id: OperationalSnapshotId = field(
        default_factory=generate_operational_snapshot_id
    )

    device_id: DeviceId | None = None

    hostname: str = ""

    site_id: SiteId | None = None

    collected_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    # --------------------------------------------------------
    # Device Health
    # --------------------------------------------------------

    cpu_utilization: float = 0.0

    memory_utilization: float = 0.0

    temperature_celsius: float = 0.0

    uptime_days: int = 0

    # --------------------------------------------------------
    # Interface Health
    # --------------------------------------------------------

    interfaces_up: int = 0

    interfaces_down: int = 0

    input_errors: int = 0

    output_errors: int = 0

    crc_errors: int = 0

    packet_drops: int = 0

    # --------------------------------------------------------
    # Routing Health
    # --------------------------------------------------------

    ospf_neighbors: int = 0

    bgp_neighbors: int = 0

    eigrp_neighbors: int = 0

    routing_converged: bool = True

    # --------------------------------------------------------
    # Network Health
    # --------------------------------------------------------

    latency_ms: float = 0.0

    jitter_ms: float = 0.0

    packet_loss_percent: float = 0.0

    availability_percent: float = 100.0

    # --------------------------------------------------------
    # Environmental Health
    # --------------------------------------------------------

    power_supply_status: str = "Healthy"

    fan_status: str = "Healthy"

    hardware_health: str = "Healthy"

    # --------------------------------------------------------
    # Monitoring
    # --------------------------------------------------------

    snmp_status: bool = True

    ntp_status: bool = True

    syslog_status: bool = True

    # --------------------------------------------------------
    # Overall Health
    # --------------------------------------------------------

    health_score: float = 100.0

    overall_status: str = "Healthy"

    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    def __post_init__(self):

        if not (0 <= self.cpu_utilization <= 100):
            raise ValueError(
                "CPU utilization must be between 0 and 100."
            )

        if not (0 <= self.memory_utilization <= 100):
            raise ValueError(
                "Memory utilization must be between 0 and 100."
            )

        if self.temperature_celsius < 0:
            raise ValueError(
                "Temperature cannot be negative."
            )

        if self.uptime_days < 0:
            raise ValueError(
                "Uptime cannot be negative."
            )

        if self.interfaces_up < 0:
            raise ValueError(
                "Interfaces up cannot be negative."
            )

        if self.interfaces_down < 0:
            raise ValueError(
                "Interfaces down cannot be negative."
            )

        if self.input_errors < 0:
            raise ValueError(
                "Input errors cannot be negative."
            )

        if self.output_errors < 0:
            raise ValueError(
                "Output errors cannot be negative."
            )

        if self.crc_errors < 0:
            raise ValueError(
                "CRC errors cannot be negative."
            )

        if self.packet_drops < 0:
            raise ValueError(
                "Packet drops cannot be negative."
            )

        if self.ospf_neighbors < 0:
            raise ValueError(
                "OSPF neighbors cannot be negative."
            )

        if self.bgp_neighbors < 0:
            raise ValueError(
                "BGP neighbors cannot be negative."
            )

        if self.eigrp_neighbors < 0:
            raise ValueError(
                "EIGRP neighbors cannot be negative."
            )

        if self.latency_ms < 0:
            raise ValueError(
                "Latency cannot be negative."
            )

        if self.jitter_ms < 0:
            raise ValueError(
                "Jitter cannot be negative."
            )

        if not (0 <= self.packet_loss_percent <= 100):
            raise ValueError(
                "Packet loss must be between 0 and 100."
            )

        if not (0 <= self.availability_percent <= 100):
            raise ValueError(
                "Availability must be between 0 and 100."
            )

        if not (0 <= self.health_score <= 100):
            raise ValueError(
                "Health score must be between 0 and 100."
            )

    # --------------------------------------------------------
    # Status Helpers
    # --------------------------------------------------------

    def mark_healthy(self):

        self.overall_status = "Healthy"

        self.touch()

    def mark_warning(self):

        self.overall_status = "Warning"

        self.touch()

    def mark_critical(self):

        self.overall_status = "Critical"

        self.touch()


@dataclass(slots=True)
class FeatureVector(BaseModel):

    # ========================================================
    # Identity
    # ========================================================

    feature_vector_id: FeatureVectorId = field(
        default_factory=generate_feature_vector_id
    )

    change_id: ChangeId | None = None

    device_id: DeviceId | None = None

    site_id: SiteId | None = None

    business_service_id: BusinessServiceId | None = None

    # ========================================================
    # Change Features
    # ========================================================

    change_scope: str = ""

    change_category: str = ""

    change_type: str = ""

    predicted_risk: str = ""

    actual_outcome: str = ""

    risk_score: float = 0.0

    confidence_score: float = 0.0

    rollback_required: bool = False

    business_impact: str = ""

    # ========================================================
    # Device Features
    # ========================================================

    device_role: str = ""

    vendor: str = ""

    model: str = ""

    os_version: str = ""

    criticality: str = ""

    operational_status: str = ""

    current_health_score: float = 100.0

    availability_percent: float = 100.0

    # ========================================================
    # Operational Features
    # ========================================================

    cpu_utilization: float = 0.0

    memory_utilization: float = 0.0

    temperature_celsius: float = 0.0

    latency_ms: float = 0.0

    jitter_ms: float = 0.0

    packet_loss_percent: float = 0.0

    interfaces_down: int = 0

    crc_errors: int = 0

    routing_converged: bool = True

    # ========================================================
    # Configuration Features
    # ========================================================

    backup_type: str = ""

    configuration_version: str = ""

    configuration_size: int = 0

    line_count: int = 0

    feature_count: int = 0

    # ========================================================
    # Historical Features
    # ========================================================

    previous_incidents: int = 0

    critical_incidents: int = 0

    successful_changes: int = 0

    failed_changes: int = 0

    rollback_history: int = 0

    # ========================================================
    # Business Features
    # ========================================================

    service_criticality: str = ""

    site_type: str = ""

    redundancy: bool = True

    # ========================================================
    # Target
    # ========================================================

    deployment_successful: bool = True

    # ========================================================
    # Validation
    # ========================================================

    def __post_init__(self):

        if not (0 <= self.risk_score <= 100):
            raise ValueError(
                "Risk score must be between 0 and 100."
            )

        if not (0 <= self.confidence_score <= 100):
            raise ValueError(
                "Confidence score must be between 0 and 100."
            )

        if not (0 <= self.current_health_score <= 100):
            raise ValueError(
                "Health score must be between 0 and 100."
            )

        if not (0 <= self.availability_percent <= 100):
            raise ValueError(
                "Availability must be between 0 and 100."
            )

        if self.configuration_size < 0:
            raise ValueError(
                "Configuration size cannot be negative."
            )

        if self.line_count < 0:
            raise ValueError(
                "Line count cannot be negative."
            )
        
    # ========================================================
    # Deployment Helpers
    # ========================================================

    def mark_successful(self):

        self.deployment_successful = True

        self.touch()


    def mark_failed(self):

        self.deployment_successful = False

        self.touch()


# ============================================================
# CONFIGURATION BACKUP
# ============================================================

@dataclass(slots=True)
class ConfigurationBackup(BaseModel):

    backup_id: ConfigurationBackupId = field(
        default_factory=generate_configuration_backup_id
    )

    device_id: DeviceId | None = None

    hostname: str = ""

    device_role: str = ""

    backup_type: str = "Running"

    configuration_version: str = "v1"

    configuration_text: str = ""

    configuration_hash: str = ""

    line_count: int = 0

    feature_summary: dict[
        str,
        int | bool,
    ] = field(
        default_factory=dict
    )

    backup_source: str = "Generated"

    collected_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    generated_from_template: bool = True

    checksum: str = ""

    def __post_init__(self):

        if self.line_count < 0:

            raise ValueError(
                "Line count cannot be negative."
            )

    @property
    def configuration_size(self) -> int:

        return len(
            self.configuration_text
        )

    def update_configuration(
        self,
        configuration: str,
    ):

        self.configuration_text = configuration

        self.line_count = len(
            configuration.splitlines()
        )

        self.touch()

# ============================================================
# HISTORICAL CHANGE
# ============================================================

CHANGE_TYPES = [

        "Routing",

        "Switching",

        "Firewall",

        "VPN",

        "QoS",

        "Wireless",

        "System",

        "Software Upgrade",

        "Interface",

        "Security Policy",

    ]

CHANGE_SCOPES = [

    "Single Device",

    "Device Pair",

    "Site",

    "Regional",

    "Global",

    ]

@dataclass(slots=True)
class HistoricalChange(BaseModel):

    change_id: ChangeId = field(
        default_factory=generate_change_id
    )

    change_number: str = ""

    site_id: SiteId | None = None

    business_service_id: BusinessServiceId | None = None

    change_category: str = ""

    change_type: str = ""

    primary_device_id: DeviceId | None = None

    affected_device_ids: list[DeviceId] = field(
        default_factory=list
    )

    change_scope: str = "Single Device"

    

    configuration_before: str = ""

    configuration_after: str = ""

    operational_before: str = ""

    operational_after: str = ""

    risk_score: float = 0.0

    confidence_score: float = 0.0

    predicted_risk: str = "UNKNOWN"

    actual_outcome: str = "UNKNOWN"

    implemented_by: str = ""

    approved_by: str = ""

    maintenance_window: str = ""

    duration_minutes: int = 0

    rollback_required: bool = False

    rollback_completed: bool = False

    business_impact: str = ""

    related_incident_ids: list[IncidentId] = field(
        default_factory=list
    )

    comments: str = ""

    def __post_init__(self):

        if not (0 <= self.risk_score <= 100):
            raise ValueError("Risk score must be between 0 and 100.")

        if not (0 <= self.confidence_score <= 100):
            raise ValueError("Confidence score must be between 0 and 100.")

        if self.duration_minutes < 0:
            raise ValueError("Duration cannot be negative.")

    def mark_success(self):

        self.actual_outcome = "SUCCESS"

        self.touch()

    def mark_failed(self):

        self.actual_outcome = "FAILED"

        self.touch()

    def mark_rollback(self):

        self.rollback_required = True

        self.rollback_completed = True

        self.touch()

    def add_incident(self, incident_id: IncidentId):

        if incident_id not in self.related_incident_ids:

            self.related_incident_ids.append(incident_id)

            self.touch()

# ============================================================
# INCIDENT
# ============================================================

@dataclass(slots=True)
class Incident(BaseModel):

    # Identity

    incident_id: IncidentId = field(
        default_factory=generate_incident_id
    )

    incident_number: str = ""

    title: str = ""

    # Classification

    severity: str = "Low"

    status: str = "Open"

    incident_category: str = ""

    assignment_group: str = ""

    business_impact: str = ""

    # Relationships

    affected_device_ids: list[DeviceId] = field(
        default_factory=list
    )

    related_change_id: ChangeId | None = None

    site_id: SiteId | None = None

    business_service_id: BusinessServiceId | None = None

    primary_device_id: DeviceId | None = None

    # RCA

    root_cause: str = ""

    resolution: str = ""

    service_restored: bool = True

    resolution_code: str = ""

    # Timeline

    opened_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    closed_at: datetime | None = None

    def close(self, resolution: str):

        self.status = "Closed"

        self.resolution = resolution

        self.closed_at = datetime.now(UTC)

        self.touch()

    @property
    def duration_minutes(self) -> int:

        if self.closed_at is None:
            return 0

        delta = self.closed_at - self.opened_at

        return int(delta.total_seconds() // 60)
    
# ============================================================
# BUSINESS SERVICE
# ============================================================

@dataclass(slots=True)
class BusinessService(BaseModel):

    service_id: BusinessServiceId = field(
        default_factory=generate_business_service_id
    )

    service_name: str = ""

    owner: str = ""

    business_unit: str = ""

    criticality: str = "Medium"

    sla_percent: float = 99.9

    availability_percent: float = 100.0

    dependent_device_ids: list[DeviceId] = field(
        default_factory=list
    )

    description: str = ""

    def __post_init__(self):

        if not (0 <= self.sla_percent <= 100):
            raise ValueError("Invalid SLA percentage.")

        if not (0 <= self.availability_percent <= 100):
            raise ValueError("Invalid availability percentage.")

    def add_dependency(self, device_id: DeviceId):

        if device_id not in self.dependent_device_ids:

            self.dependent_device_ids.append(device_id)

            self.touch()

    def remove_dependency(self, device_id: DeviceId):

        if device_id in self.dependent_device_ids:

            self.dependent_device_ids.remove(device_id)

            self.touch()

# ============================================================
# TOPOLOGY LINK
# ============================================================

@dataclass(slots=True)
class TopologyLink(BaseModel):
    """
    Represents a discovered or manually defined Layer-2/Layer-3
    relationship between two network devices.

    This class forms the foundation of the Enterprise Digital Twin
    graph and will later support topology-aware risk propagation,
    blast-radius calculation, and dependency analysis.
    """

    link_id: TopologyLinkId = field(
        default_factory=generate_topology_link_id
    )

    source_device_id: DeviceId | None = None

    destination_device_id: DeviceId | None = None

    source_interface_id: InterfaceId | None = None

    destination_interface_id: InterfaceId | None = None

    source_hostname: str = ""

    destination_hostname: str = ""

    source_interface_name: str = ""

    destination_interface_name: str = ""

    discovery_protocol: str = "LLDP"

    link_type: str = "Ethernet"

    media_type: str = "Copper"

    bandwidth: str = "1G"

    utilization_percent: float = 0.0

    operational_status: str = "UP"

    admin_status: str = "UP"

    relationship_confidence: float = 100.0

    bidirectional: bool = True

    latency_ms: float = 0.0

    packet_loss_percent: float = 0.0

    error_rate_percent: float = 0.0

    business_critical: bool = False

    last_discovered: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    discovery_source: str = "LLDP"

    notes: str = ""

    def __post_init__(self):

        if not (0 <= self.utilization_percent <= 100):
            raise ValueError(
                "Utilization must be between 0 and 100."
            )

        if not (0 <= self.relationship_confidence <= 100):
            raise ValueError(
                "Relationship confidence must be between 0 and 100."
            )

        if self.latency_ms < 0:
            raise ValueError(
                "Latency cannot be negative."
            )

        if not (0 <= self.packet_loss_percent <= 100):
            raise ValueError(
                "Packet loss must be between 0 and 100."
            )

        if not (0 <= self.error_rate_percent <= 100):
            raise ValueError(
                "Error rate must be between 0 and 100."
            )

    # --------------------------------------------------------
    # Discovery
    # --------------------------------------------------------

    def update_discovery(self):

        self.last_discovered = datetime.now(UTC)

        self.touch()

    # --------------------------------------------------------

    def mark_down(self):

        self.operational_status = "DOWN"

        self.touch()

    # --------------------------------------------------------

    def mark_up(self):

        self.operational_status = "UP"

        self.touch()

    # --------------------------------------------------------

    def update_utilization(
        self,
        utilization: float
    ):

        if not (0 <= utilization <= 100):
            raise ValueError(
                "Utilization must be between 0 and 100."
            )

        self.utilization_percent = utilization

        self.touch()

    # --------------------------------------------------------

    def update_latency(
        self,
        latency_ms: float
    ):

        if latency_ms < 0:
            raise ValueError(
                "Latency cannot be negative."
            )

        self.latency_ms = latency_ms

        self.touch()

    # --------------------------------------------------------

    def update_packet_loss(
        self,
        packet_loss: float
    ):

        if not (0 <= packet_loss <= 100):
            raise ValueError(
                "Packet loss must be between 0 and 100."
            )

        self.packet_loss_percent = packet_loss

        self.touch()

    # --------------------------------------------------------

    def update_error_rate(
        self,
        error_rate: float
    ):

        if not (0 <= error_rate <= 100):
            raise ValueError(
                "Error rate must be between 0 and 100."
            )

        self.error_rate_percent = error_rate

        self.touch()

    # --------------------------------------------------------

    @property
    def is_healthy(self) -> bool:
        """
        Returns True when the topology relationship
        is operational and carrying traffic within
        acceptable thresholds.
        """

        return (
            self.operational_status == "UP"
            and self.utilization_percent < 90
            and self.packet_loss_percent < 1
            and self.error_rate_percent < 1
        )

    # --------------------------------------------------------

    @property
    def endpoints(self) -> tuple[str, str]:
        """
        Returns a tuple containing the source and
        destination hostnames.
        """

        return (
            self.source_hostname,
            self.destination_hostname,
        )

    # --------------------------------------------------------

    @property
    def interface_pair(self) -> tuple[str, str]:
        """
        Returns the interface names participating
        in the topology relationship.
        """

        return (
            self.source_interface_name,
            self.destination_interface_name,
        )
    
# ============================================================
# SITE
# ============================================================

@dataclass(slots=True)
class Site(BaseModel):
    """
    Represents a physical enterprise location.

    A Site can represent:
        - Headquarters
        - Data Center
        - Branch
        - Manufacturing Plant
        - Warehouse
        - Regional Office
        - Cloud Region
        - DR Site

    Devices belong to a Site.
    Business Services can also be associated with a Site.
    """

    site_id: SiteId = field(
        default_factory=generate_site_id
    )

    site_code: str = ""

    site_name: str = ""

    site_type: str = "Branch"

    country: str = COUNTRY

    state: str = ""

    city: str = ""

    region: str = ""

    timezone: str = TIMEZONE

    address: str = ""

    latitude: float | None = None

    longitude: float | None = None

    business_unit: str = ""

    operational_status: str = "Active"

    criticality: str = "Medium"

    maintenance_window: str = ""

    primary_contact: str = ""

    secondary_contact: str = ""

    notes: str = ""

    # -------------------------------------------------------
    # Relationships
    # -------------------------------------------------------

    device_ids: list[DeviceId] = field(
        default_factory=list
    )

    business_service_ids: list[
        BusinessServiceId
    ] = field(default_factory=list)

    incident_ids: list[
        IncidentId
    ] = field(default_factory=list)

    historical_change_ids: list[
        ChangeId
    ] = field(default_factory=list)

    topology_link_ids: list[
        TopologyLinkId
    ] = field(default_factory=list)

    # -------------------------------------------------------
    # Validation
    # -------------------------------------------------------

    def __post_init__(self):

        if self.latitude is not None:

            if not (-90 <= self.latitude <= 90):

                raise ValueError(
                    "Latitude must be between -90 and 90."
                )

        if self.longitude is not None:

            if not (-180 <= self.longitude <= 180):

                raise ValueError(
                    "Longitude must be between -180 and 180."
                )

    # -------------------------------------------------------
    # Device Relationship Methods
    # -------------------------------------------------------

    def add_device(
        self,
        device_id: DeviceId
    ):

        if device_id not in self.device_ids:

            self.device_ids.append(device_id)

            self.touch()

    def remove_device(
        self,
        device_id: DeviceId
    ):

        if device_id in self.device_ids:

            self.device_ids.remove(device_id)

            self.touch()

    # -------------------------------------------------------
    # Business Service Relationship
    # -------------------------------------------------------

    def add_business_service(
        self,
        service_id: BusinessServiceId
    ):

        if service_id not in self.business_service_ids:

            self.business_service_ids.append(
                service_id
            )

            self.touch()

    # -------------------------------------------------------

    def remove_business_service(
        self,
        service_id: BusinessServiceId
    ):

        if service_id in self.business_service_ids:

            self.business_service_ids.remove(
                service_id
            )

            self.touch()

    # -------------------------------------------------------
    # Incident Relationship
    # -------------------------------------------------------

    def add_incident(
        self,
        incident_id: IncidentId
    ):

        if incident_id not in self.incident_ids:

            self.incident_ids.append(
                incident_id
            )

            self.touch()

    # -------------------------------------------------------
    # Historical Change Relationship
    # -------------------------------------------------------

    def add_change(
        self,
        change_id: ChangeId
    ):

        if change_id not in self.historical_change_ids:

            self.historical_change_ids.append(
                change_id
            )

            self.touch()

    # -------------------------------------------------------
    # Topology Relationship
    # -------------------------------------------------------

    def add_topology_link(
        self,
        topology_link_id: TopologyLinkId
    ):

        if topology_link_id not in self.topology_link_ids:

            self.topology_link_ids.append(
                topology_link_id
            )

            self.touch()

    # -------------------------------------------------------
    # Operational Helpers
    # -------------------------------------------------------

    @property
    def device_count(self) -> int:

        return len(self.device_ids)

    @property
    def business_service_count(self) -> int:

        return len(self.business_service_ids)

    @property
    def incident_count(self) -> int:

        return len(self.incident_ids)

    @property
    def change_count(self) -> int:

        return len(self.historical_change_ids)

    @property
    def topology_count(self) -> int:

        return len(self.topology_link_ids)

    # -------------------------------------------------------

    @property
    def is_active(self) -> bool:

        return self.operational_status.lower() == "active"

    # -------------------------------------------------------

    @property
    def coordinates(self) -> tuple[float | None, float | None]:

        return (
            self.latitude,
            self.longitude,
        )

    # -------------------------------------------------------

    def summary(self) -> dict:

        return {

            "site_id": self.site_id,

            "site_name": self.site_name,

            "site_code": self.site_code,

            "site_type": self.site_type,

            "country": self.country,

            "city": self.city,

            "devices": self.device_count,

            "business_services": self.business_service_count,

            "changes": self.change_count,

            "incidents": self.incident_count,

            "topology_links": self.topology_count,

            "status": self.operational_status,

            "criticality": self.criticality,

        }

# ============================================================
# DEVICE
# ============================================================

@dataclass(slots=True)
class Device(BaseModel):
    """
    Enterprise Network Device.

    Represents a managed Configuration Item (CI) within the
    Enterprise Digital Twin.

    A Device maintains relationships to:

        • Interfaces
        • Configuration Snapshots
        • Operational Snapshots
        • Historical Changes
        • Incidents
        • Business Services
        • Topology Links

    Relationships are maintained through IDs rather than
    nested objects to allow graph traversal and independent
    lifecycle management.
    """

    # ========================================================
    # Identity
    # ========================================================

    device_id: DeviceId = field(
        default_factory=generate_device_id
    )

    hostname: str = ""

    serial_number: str = ""

    asset_tag: str = ""

    management_ip: str = ""

    loopback_ip: str = ""

    mac_address: str = ""

    # ========================================================
    # Enterprise Information
    # ========================================================

    site_id: SiteId | None = None

    role: str = ""

    vendor: str = ""

    platform: str = ""

    model: str = ""

    os_name: str = ""

    os_version: str = ""

    software_image: str = ""

    lifecycle_state: str = "Production"

    criticality: str = "Medium"

    # ========================================================
    # Ownership
    # ========================================================

    support_team: str = ""

    business_owner: str = ""

    technical_owner: str = ""

    business_unit: str = ""

    region: str = ""

    country: str = COUNTRY

    timezone: str = TIMEZONE

    # ========================================================
    # Operational Metadata
    # ========================================================

    operational_status: str = "UP"

    administrative_status: str = "Managed"

    maintenance_window: str = ""

    current_health_score: float = 100.0

    compliance_score: float = 100.0

    availability_percent: float = 100.0

    # ========================================================
    # Important Timestamps
    # ========================================================

    first_discovered: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    last_seen: datetime | None = None

    last_backup: datetime | None = None

    last_configuration_change: datetime | None = None

    last_successful_poll: datetime | None = None

    last_operational_snapshot: datetime | None = None

    # ========================================================
    # Relationships
    # ========================================================

    interface_ids: list[InterfaceId] = field(
        default_factory=list
    )

    configuration_snapshot_ids: list[
        ConfigurationSnapshotId
    ] = field(default_factory=list)

    configuration_backup_ids: list[
        ConfigurationBackupId
    ] = field(
        default_factory=list
    )

    operational_snapshot_ids: list[
        OperationalSnapshotId
    ] = field(default_factory=list)

    historical_change_ids: list[
        ChangeId
    ] = field(default_factory=list)

    incident_ids: list[
        IncidentId
    ] = field(default_factory=list)

    business_service_ids: list[
        BusinessServiceId
    ] = field(default_factory=list)

    topology_link_ids: list[
        TopologyLinkId
    ] = field(default_factory=list)

    # ========================================================
    # Tags / Metadata
    # ========================================================

    tags: list[str] = field(
        default_factory=list
    )

    labels: dict[str, str] = field(
        default_factory=dict
    )

    notes: str = ""

    # ========================================================
    # Validation
    # ========================================================

    def __post_init__(self):

        if not self.hostname:
            raise ValueError(
                "Hostname cannot be empty."
            )

        if not (0 <= self.current_health_score <= 100):
            raise ValueError(
                "Health score must be between 0 and 100."
            )

        if not (0 <= self.compliance_score <= 100):
            raise ValueError(
                "Compliance score must be between 0 and 100."
            )

        if not (0 <= self.availability_percent <= 100):
            raise ValueError(
                "Availability must be between 0 and 100."
            )

    # ========================================================
    # Interface Relationship
    # ========================================================

    def add_interface(
        self,
        interface_id: InterfaceId
    ):

        if interface_id not in self.interface_ids:

            self.interface_ids.append(
                interface_id
            )

            self.touch()

    def remove_interface(
        self,
        interface_id: InterfaceId
    ):

        if interface_id in self.interface_ids:

            self.interface_ids.remove(
                interface_id
            )

            self.touch()

    # ========================================================
    # Configuration Snapshots
    # ========================================================

    def add_configuration_snapshot(
        self,
        snapshot_id: ConfigurationSnapshotId
    ):

        if snapshot_id not in self.configuration_snapshot_ids:

            self.configuration_snapshot_ids.append(
                snapshot_id
            )

            self.last_backup = datetime.now(UTC)

            self.touch()

    # ========================================================
    # Configuration Backups
    # ========================================================


    def add_configuration_backup(

        self,

        backup_id: ConfigurationBackupId,

    ):

        if backup_id not in self.configuration_backup_ids:

            self.configuration_backup_ids.append(
                backup_id
            )

            self.last_backup = datetime.now(UTC)

            self.touch()


    def clear_configuration_backups(self):

        if self.configuration_backup_ids:

            self.configuration_backup_ids.clear()

            self.last_backup = None

            self.touch()
    # ========================================================
    # Operational Snapshots
    # ========================================================

    def add_operational_snapshot(

        self,

        snapshot_id: OperationalSnapshotId,

    ):

        if snapshot_id not in self.operational_snapshot_ids:

            self.operational_snapshot_ids.append(
                snapshot_id
            )

            self.last_operational_snapshot = datetime.now(UTC)

            self.touch()

    def clear_operational_snapshots(self):

        if self.operational_snapshot_ids:

            self.operational_snapshot_ids.clear()

            self.last_operational_snapshot = None

            self.touch()

    # ========================================================
    # Historical Changes
    # ========================================================

    def add_change(
        self,
        change_id: ChangeId
    ):

        if change_id not in self.historical_change_ids:

            self.historical_change_ids.append(
                change_id
            )

            self.last_configuration_change = (
                datetime.now(UTC)
            )

            self.touch()

    # ========================================================
    # Incidents
    # ========================================================

    def add_incident(
        self,
        incident_id: IncidentId
    ):

        if incident_id not in self.incident_ids:

            self.incident_ids.append(
                incident_id
            )

            self.touch()

    # ========================================================
    # Business Services
    # ========================================================

    def add_business_service(
        self,
        service_id: BusinessServiceId
    ):

        if service_id not in self.business_service_ids:

            self.business_service_ids.append(
                service_id
            )

            self.touch()

    # ========================================================
    # Topology Links
    # ========================================================

    def add_topology_link(
        self,
        topology_link_id: TopologyLinkId
    ):

        if topology_link_id not in self.topology_link_ids:

            self.topology_link_ids.append(
                topology_link_id
            )

            self.touch()

    # ========================================================
    # Health Management
    # ========================================================

    def update_health(
        self,
        score: float
    ):

        if not (0 <= score <= 100):

            raise ValueError(
                "Health score must be between 0 and 100."
            )

        self.current_health_score = score

        self.touch()

    def update_compliance(
        self,
        score: float
    ):

        if not (0 <= score <= 100):

            raise ValueError(
                "Compliance score must be between 0 and 100."
            )

        self.compliance_score = score

        self.touch()

    def update_availability(
        self,
        percentage: float
    ):

        if not (0 <= percentage <= 100):

            raise ValueError(
                "Availability must be between 0 and 100."
            )

        self.availability_percent = percentage

        self.touch()

    # ========================================================
    # Lifecycle
    # ========================================================

    def discovered(self):

        self.last_seen = datetime.now(UTC)

        self.touch()

    def backup_completed(self):

        self.last_backup = datetime.now(UTC)

        self.touch()

    def polling_completed(self):

        self.last_successful_poll = datetime.now(UTC)

        self.last_seen = datetime.now(UTC)

        self.touch()

    def configuration_changed(self):

        self.last_configuration_change = (
            datetime.now(UTC)
        )

        self.touch()

    # ========================================================
    # Tag Management
    # ========================================================

    def add_tag(
        self,
        tag: str
    ):

        if tag not in self.tags:

            self.tags.append(tag)

            self.touch()

    def remove_tag(
        self,
        tag: str
    ):

        if tag in self.tags:

            self.tags.remove(tag)

            self.touch()

    # ========================================================
    # Labels
    # ========================================================

    def set_label(
        self,
        key: str,
        value: str
    ):

        self.labels[key] = value

        self.touch()

    # ========================================================
    # Properties
    # ========================================================

    @property
    def interface_count(self) -> int:

        return len(self.interface_ids)

    @property
    def snapshot_count(self) -> int:

        return len(
            self.configuration_snapshot_ids
        )

    @property
    def backup_count(self) -> int:

        return len(
            self.configuration_backup_ids
        )
    
    @property
    def operational_snapshot_count(self) -> int:

        return len(
            self.operational_snapshot_ids
        )

    @property
    def incident_count(self) -> int:

        return len(self.incident_ids)

    @property
    def change_count(self) -> int:

        return len(
            self.historical_change_ids
        )

    @property
    def business_service_count(self) -> int:

        return len(
            self.business_service_ids
        )

    @property
    def topology_count(self) -> int:

        return len(
            self.topology_link_ids
        )

    @property
    def is_healthy(self) -> bool:

        return self.current_health_score >= 80

    @property
    def is_compliant(self) -> bool:

        return self.compliance_score >= 95

    # ========================================================
    # Summary
    # ========================================================

    def summary(self) -> dict:

        return {

            "device_id": self.device_id,

            "hostname": self.hostname,

            "role": self.role,

            "platform": self.platform,

            "site": self.site_id,

            "health": self.current_health_score,

            "interfaces": self.interface_count,

            "configuration_backups": self.backup_count,

            "changes": self.change_count,

            "incidents": self.incident_count,

            "business_services": self.business_service_count,

            "topology_links": self.topology_count,

            "status": self.operational_status,

        }

    # ========================================================
    # Role Helpers
    # ========================================================

    @property
    def normalized_role(self) -> str:
        """
        Returns the canonical enterprise
        device role.

        Example

        DIST -> DISTRIBUTION

        FW -> FIREWALL
        """

        return DEVICE_ROLE_MAPPING.get(

            self.role.upper(),

            self.role.upper(),

        )