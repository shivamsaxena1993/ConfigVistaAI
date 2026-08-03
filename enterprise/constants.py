"""
=============================================================
ConfigVista AI
Enterprise Constants
-------------------------------------------------------------
Purpose:
    Centralized enterprise-wide constants, enumerations,
    platform mappings and default values.

Author : Shivam Saxena
Project: ConfigVista AI
Version: 3.0 (Artifact-2)
=============================================================
"""

from enum import Enum

# ============================================================
# Enterprise Metadata
# ============================================================

ENTERPRISE_NAME = "ConfigVista Enterprise Lab"
INDUSTRY = "Manufacturing"
COUNTRY = "India"
TIMEZONE = "Asia/Kolkata"

DATASET_VERSION = "1.0"
GENERATOR_VERSION = "1.0"

RANDOM_SEED = 42

# ============================================================
# Enterprise Scale
# ============================================================

TOTAL_DATA_CENTERS = 1
TOTAL_BRANCHES = 10
TOTAL_SITES = TOTAL_DATA_CENTERS + TOTAL_BRANCHES

TOTAL_DEVICES = 31

# ============================================================
# Enumerations
# ============================================================


class SiteType(Enum):
    DATA_CENTER = "DATA_CENTER"
    MANUFACTURING = "MANUFACTURING"
    LOGISTICS = "LOGISTICS"
    WAREHOUSE = "WAREHOUSE"
    SALES = "SALES"
    CORPORATE = "CORPORATE"
    REGIONAL_OFFICE = "REGIONAL_OFFICE"
    FINANCE = "FINANCE"
    RESEARCH = "RESEARCH"


class DeviceRole(Enum):
    CORE_ROUTER = "CORE_ROUTER"
    DISTRIBUTION_SWITCH = "DISTRIBUTION_SWITCH"
    WAN_EDGE = "WAN_EDGE"
    FIREWALL = "FIREWALL"
    BRANCH_ROUTER = "BRANCH_ROUTER"
    ACCESS_SWITCH = "ACCESS_SWITCH"
    AAA_SERVER = "AAA_SERVER"
    DNS_SERVER = "DNS_SERVER"
    DHCP_SERVER = "DHCP_SERVER"


class Vendor(Enum):
    CISCO = "Cisco"
    LINUX = "Linux"


class Criticality(Enum):
    MISSION_CRITICAL = "MISSION_CRITICAL"
    BUSINESS_CRITICAL = "BUSINESS_CRITICAL"
    STANDARD = "STANDARD"
    NON_CRITICAL = "NON_CRITICAL"


class LifecycleStatus(Enum):
    ACTIVE = "ACTIVE"
    MAINTENANCE = "MAINTENANCE"
    DECOMMISSIONING = "DECOMMISSIONING"
    RETIRED = "RETIRED"


class InterfaceType(Enum):
    PHYSICAL = "PHYSICAL"
    LOOPBACK = "LOOPBACK"
    SVI = "SVI"
    SUBINTERFACE = "SUBINTERFACE"
    PORT_CHANNEL = "PORT_CHANNEL"
    TUNNEL = "TUNNEL"
    VLAN = "VLAN"


class InterfaceLayer(Enum):
    LAYER2 = "LAYER2"
    LAYER3 = "LAYER3"


class InterfaceStatus(Enum):
    UP = "UP"
    DOWN = "DOWN"
    ADMIN_DOWN = "ADMIN_DOWN"


class RoutingProtocol(Enum):
    STATIC = "STATIC"
    OSPF = "OSPF"
    BGP = "BGP"
    EIGRP = "EIGRP"


class ChangeOutcome(Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    PARTIAL_SUCCESS = "PARTIAL_SUCCESS"
    ROLLED_BACK = "ROLLED_BACK"


class ChangeRisk(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class OperationalHealth(Enum):
    HEALTHY = "HEALTHY"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


# ============================================================
# Platform Mapping
# ============================================================

DEVICE_PLATFORM = {

    DeviceRole.CORE_ROUTER:
        "Cisco Catalyst 9500",

    DeviceRole.DISTRIBUTION_SWITCH:
        "Cisco Catalyst 9300",

    DeviceRole.ACCESS_SWITCH:
        "Cisco Catalyst 9200",

    DeviceRole.BRANCH_ROUTER:
        "Cisco ISR 4451",

    DeviceRole.WAN_EDGE:
        "Cisco Catalyst 8500",

    DeviceRole.FIREWALL:
        "Cisco Firepower 2140",

    DeviceRole.AAA_SERVER:
        "Cisco ISE",

    DeviceRole.DNS_SERVER:
        "Ubuntu Server 24.04",

    DeviceRole.DHCP_SERVER:
        "Ubuntu Server 24.04"
}

# ============================================================
# Vendor Mapping
# ============================================================

DEVICE_VENDOR = {

    DeviceRole.CORE_ROUTER:
        Vendor.CISCO,

    DeviceRole.DISTRIBUTION_SWITCH:
        Vendor.CISCO,

    DeviceRole.ACCESS_SWITCH:
        Vendor.CISCO,

    DeviceRole.BRANCH_ROUTER:
        Vendor.CISCO,

    DeviceRole.WAN_EDGE:
        Vendor.CISCO,

    DeviceRole.FIREWALL:
        Vendor.CISCO,

    DeviceRole.AAA_SERVER:
        Vendor.CISCO,

    DeviceRole.DNS_SERVER:
        Vendor.LINUX,

    DeviceRole.DHCP_SERVER:
        Vendor.LINUX
}

# ============================================================
# Software Versions
# ============================================================

OS_VERSION = {

    DeviceRole.CORE_ROUTER:
        "IOS-XE 17.9.4",

    DeviceRole.DISTRIBUTION_SWITCH:
        "IOS-XE 17.9.4",

    DeviceRole.ACCESS_SWITCH:
        "IOS-XE 17.9.4",

    DeviceRole.BRANCH_ROUTER:
        "IOS-XE 17.9.4",

    DeviceRole.WAN_EDGE:
        "IOS-XE 17.9.4",

    DeviceRole.FIREWALL:
        "FTD 7.4.1",

    DeviceRole.AAA_SERVER:
        "Cisco ISE 3.3",

    DeviceRole.DNS_SERVER:
        "Ubuntu 24.04 LTS",

    DeviceRole.DHCP_SERVER:
        "Ubuntu 24.04 LTS"
}

# ============================================================
# Default Device Criticality
# ============================================================

DEVICE_CRITICALITY = {

    DeviceRole.CORE_ROUTER:
        Criticality.MISSION_CRITICAL,

    DeviceRole.WAN_EDGE:
        Criticality.MISSION_CRITICAL,

    DeviceRole.FIREWALL:
        Criticality.MISSION_CRITICAL,

    DeviceRole.DISTRIBUTION_SWITCH:
        Criticality.BUSINESS_CRITICAL,

    DeviceRole.BRANCH_ROUTER:
        Criticality.BUSINESS_CRITICAL,

    DeviceRole.ACCESS_SWITCH:
        Criticality.STANDARD,

    DeviceRole.AAA_SERVER:
        Criticality.MISSION_CRITICAL,

    DeviceRole.DNS_SERVER:
        Criticality.BUSINESS_CRITICAL,

    DeviceRole.DHCP_SERVER:
        Criticality.BUSINESS_CRITICAL
}

# ============================================================
# Business Services
# ============================================================

BUSINESS_SERVICES = [

    "ERP",

    "Manufacturing Execution System",

    "Warehouse Management",

    "Voice",

    "Video Conferencing",

    "Corporate LAN",

    "Internet Access",

    "Active Directory",

    "DNS",

    "DHCP",

    "Email",

    "Remote VPN"
]

# ============================================================
# Enterprise Sites
# ============================================================

SITE_CODES = [

    "DC01",

    "BR01",

    "BR02",

    "BR03",

    "BR04",

    "BR05",

    "BR06",

    "BR07",

    "BR08",

    "BR09",

    "BR10"
]

# ============================================================
# Default Operational Baseline
# ============================================================

DEFAULT_CPU = 12
DEFAULT_MEMORY = 35
DEFAULT_TEMPERATURE = 39

DEFAULT_INTERFACE_UTILIZATION = 18
DEFAULT_INTERFACE_ERRORS = 0
DEFAULT_PACKET_DROPS = 0

DEFAULT_HEALTH_SCORE = 100

DEFAULT_INTERFACE_SPEED = "1G"
DEFAULT_MTU = 1500

# ============================================================
# Network Defaults
# ============================================================

DEFAULT_DOMAIN_NAME = "configvista.lab"

DEFAULT_SNMP_COMMUNITY = "CONFIGVISTA"

DEFAULT_TIMEZONE = "Asia/Kolkata"

DEFAULT_NTP_SERVER = "10.0.0.20"

DEFAULT_DNS_SERVER = "10.0.0.30"

DEFAULT_SYSLOG_SERVER = "10.0.0.40"

# ============================================================
# Feature Engineering Defaults
# ============================================================

MAX_CHANGE_HISTORY = 100

MAX_INCIDENT_HISTORY = 100

MAX_ROLLBACK_HISTORY = 50

ML_TRAIN_SPLIT = 0.70
ML_VALIDATION_SPLIT = 0.15
ML_TEST_SPLIT = 0.15

# ============================================================
# Dataset Generation Targets
# ============================================================

TARGET_CHANGE_RECORDS = 2000

TARGET_INCIDENT_RECORDS = 300

TARGET_ROLLBACK_RECORDS = 120

TARGET_CONFIGURATION_SNAPSHOTS = 500

TARGET_OPERATIONAL_SNAPSHOTS = 1000

ROLE_SUPPORTED_DOMAINS = {

    DeviceRole.CORE_ROUTER: [
        "SYSTEM",
        "INTERFACE",
        "ROUTING",
        "QOS",
        "SERVICES"
    ],

    DeviceRole.DISTRIBUTION_SWITCH: [
        "SYSTEM",
        "INTERFACE",
        "SWITCHING",
        "SECURITY",
        "SERVICES"
    ],

    DeviceRole.ACCESS_SWITCH: [
        "SYSTEM",
        "INTERFACE",
        "SWITCHING",
        "SECURITY"
    ],

    DeviceRole.BRANCH_ROUTER: [
        "SYSTEM",
        "INTERFACE",
        "ROUTING",
        "SECURITY",
        "QOS",
        "SERVICES"
    ],

    DeviceRole.WAN_EDGE: [
        "SYSTEM",
        "INTERFACE",
        "ROUTING",
        "QOS",
        "SECURITY"
    ],

    DeviceRole.FIREWALL: [
        "SYSTEM",
        "INTERFACE",
        "SECURITY",
        "SERVICES"
    ],

    DeviceRole.AAA_SERVER: [
        "SYSTEM",
        "SERVICES"
    ],

    DeviceRole.DNS_SERVER: [
        "SYSTEM",
        "SERVICES"
    ],

    DeviceRole.DHCP_SERVER: [
        "SYSTEM",
        "SERVICES"
    ]
}

ROLE_ROUTING_PROTOCOLS = {

    DeviceRole.CORE_ROUTER: [
        RoutingProtocol.OSPF,
        RoutingProtocol.BGP,
        RoutingProtocol.STATIC
    ],

    DeviceRole.WAN_EDGE: [
        RoutingProtocol.BGP,
        RoutingProtocol.OSPF,
        RoutingProtocol.STATIC
    ],

    DeviceRole.BRANCH_ROUTER: [
        RoutingProtocol.OSPF,
        RoutingProtocol.STATIC
    ],

    DeviceRole.DISTRIBUTION_SWITCH: [
        RoutingProtocol.OSPF,
        RoutingProtocol.STATIC
    ],

    DeviceRole.ACCESS_SWITCH: [],

    DeviceRole.FIREWALL: [],

    DeviceRole.AAA_SERVER: [],

    DeviceRole.DNS_SERVER: [],

    DeviceRole.DHCP_SERVER: []
}

ROLE_INTERFACE_TEMPLATE = {

    DeviceRole.CORE_ROUTER: {
        "physical": 16,
        "loopback": 1,
        "port_channel": 4,
        "tunnel": 2,
        "svi": 0
    },

    DeviceRole.DISTRIBUTION_SWITCH: {
        "physical": 48,
        "loopback": 1,
        "port_channel": 2,
        "svi": 20
    },

    DeviceRole.ACCESS_SWITCH: {
        "physical": 48,
        "loopback": 1,
        "port_channel": 2,
        "svi": 10
    },

    DeviceRole.BRANCH_ROUTER: {
        "physical": 4,
        "loopback": 1,
        "subinterface": 2,
        "tunnel": 1
    },

    DeviceRole.WAN_EDGE: {
        "physical": 8,
        "loopback": 1,
        "port_channel": 2,
        "tunnel": 2
    },

    DeviceRole.FIREWALL: {
        "physical": 8,
        "port_channel": 2,
        "subinterface": 10
    },

    DeviceRole.AAA_SERVER: {
        "physical": 2
    },

    DeviceRole.DNS_SERVER: {
        "physical": 2
    },

    DeviceRole.DHCP_SERVER: {
        "physical": 2
    }
}

ROLE_CHANGE_TYPES = {

    DeviceRole.CORE_ROUTER: [
        "Routing",
        "QoS",
        "Interface",
        "System"
    ],

    DeviceRole.BRANCH_ROUTER: [
        "Routing",
        "Interface",
        "Security",
        "QoS",
        "Services"
    ],

    DeviceRole.ACCESS_SWITCH: [
        "VLAN",
        "STP",
        "Port Security",
        "Access Port",
        "Trunk"
    ],

    DeviceRole.FIREWALL: [
        "ACL",
        "NAT",
        "Security Policy",
        "VPN"
    ]
}

ROLE_DEPENDENT_SERVICES = {

    DeviceRole.CORE_ROUTER: [
        "ERP",
        "Voice",
        "Internet Access",
        "Manufacturing Execution System"
    ],

    DeviceRole.WAN_EDGE: [
        "Internet Access",
        "Voice",
        "VPN"
    ],

    DeviceRole.FIREWALL: [
        "Internet Access",
        "Remote VPN"
    ],

    DeviceRole.DNS_SERVER: [
        "DNS"
    ],

    DeviceRole.DHCP_SERVER: [
        "DHCP"
    ]
}

ROLE_MONITORED_METRICS = {

    DeviceRole.CORE_ROUTER: [
        "CPU",
        "Memory",
        "BGP Peers",
        "OSPF Neighbors",
        "Interface Errors",
        "Routing Table Size"
    ],

    DeviceRole.BRANCH_ROUTER: [
        "CPU",
        "Memory",
        "WAN Utilization",
        "Packet Loss",
        "OSPF Neighbor"
    ],

    DeviceRole.ACCESS_SWITCH: [
        "CPU",
        "Memory",
        "STP Status",
        "MAC Table",
        "Port Errors"
    ],

    DeviceRole.FIREWALL: [
        "CPU",
        "Memory",
        "Connection Count",
        "Session Utilization"
    ]
}

