"""
Parser regression tests for ConfigVista AI Artifact-1.

These tests protect the normalized parser contract consumed by
comparison, semantic analysis, feature extraction and the UI.
"""

from parser.parsers.interface_parser import InterfaceParser
from parser.parsers.config_parser import ConfigParser


def parse_interfaces(config: str):
    lines = [
        line.rstrip()
        for line in config.splitlines()
    ]

    parser = InterfaceParser(lines)

    return parser.parse(), parser


def test_abbreviated_interface_name_is_normalized():

    config = """
interface Gi0/0
 description WAN
 ip address 10.10.10.1 255.255.255.0
!
"""

    interfaces, _ = parse_interfaces(config)

    assert len(interfaces) == 1

    assert (
        interfaces[0]["name"]
        == "GigabitEthernet0/0"
    )


def test_canonical_interface_name_remains_unchanged():

    config = """
interface GigabitEthernet0/0
 description WAN
 ip address 10.10.10.1 255.255.255.0
!
"""

    interfaces, _ = parse_interfaces(config)

    assert len(interfaces) == 1

    assert (
        interfaces[0]["name"]
        == "GigabitEthernet0/0"
    )


def test_interface_normalization_is_idempotent():

    parser = InterfaceParser([])

    normalized = parser._normalize_interface_name(
        "Gi0/0"
    )

    assert normalized == "GigabitEthernet0/0"

    assert (
        parser._normalize_interface_name(normalized)
        == normalized
    )


def test_layer3_interface_parsing():

    config = """
interface Gi0/0
 description WAN Uplink
 ip address 10.10.10.1 255.255.255.0
 ip helper-address 10.1.1.10
 ip helper-address 10.1.1.20
 mtu 1500
 bandwidth 100000
 no ip redirects
 no ip proxy-arp
 no shutdown
!
"""

    interfaces, _ = parse_interfaces(config)

    interface = interfaces[0]

    assert interface["ip_address"] == "10.10.10.1"

    assert (
        interface["subnet_mask"]
        == "255.255.255.0"
    )

    assert interface["mtu"] == 1500
    assert interface["bandwidth"] == 100000

    assert interface["redirects"] is False
    assert interface["proxy_arp"] is False

    assert interface["shutdown"] is False

    assert interface["semantic"]["is_routed"] is True

    assert interface["helper_addresses"] == [
        "10.1.1.10",
        "10.1.1.20",
    ]


def test_shutdown_state():

    config = """
interface Gi0/1
 shutdown
!
"""

    interfaces, _ = parse_interfaces(config)

    assert interfaces[0]["shutdown"] is True


def test_access_switchport_parsing():

    config = """
interface Gi1/0/10
 description USER ACCESS
 switchport mode access
 switchport access vlan 20
 switchport voice vlan 30
 spanning-tree portfast
 spanning-tree bpduguard enable
!
"""

    interfaces, _ = parse_interfaces(config)

    interface = interfaces[0]

    assert interface["switchport_mode"] == "access"
    assert interface["access_vlan"] == 20
    assert interface["voice_vlan"] == 30

    assert interface["portfast"] is True
    assert interface["bpduguard"] is True

    assert interface["semantic"]["is_switchport"] is True
    assert interface["semantic"]["is_access"] is True
    assert interface["semantic"]["is_trunk"] is False


def test_trunk_vlan_range_expansion():

    config = """
interface Gi1/0/48
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 10,20-22,100
!
"""

    interfaces, _ = parse_interfaces(config)

    interface = interfaces[0]

    assert interface["switchport_mode"] == "trunk"

    assert interface["native_vlan"] == 99

    assert interface["allowed_vlans"] == [
        10,
        20,
        21,
        22,
        100,
    ]

    assert interface["semantic"]["is_trunk"] is True


def test_acl_and_qos_parsing():

    config = """
interface Gi0/0
 ip address 10.10.10.1 255.255.255.0
 ip access-group branch-in in
 ip access-group branch-out out
 service-policy input wan-input
 service-policy output wan-output
!
"""

    interfaces, _ = parse_interfaces(config)

    interface = interfaces[0]

    assert interface["inbound_acl"] == "BRANCH-IN"
    assert interface["outbound_acl"] == "BRANCH-OUT"

    assert (
        interface["service_policy_input"]
        == "WAN-INPUT"
    )

    assert (
        interface["service_policy_output"]
        == "WAN-OUTPUT"
    )

    assert interface["semantic"]["has_acl"] is True
    assert interface["semantic"]["has_qos"] is True


def test_qos_validation_observation_uses_correct_name():

    config = """
interface GigabitEthernet0/0
 ip address 10.10.10.1 255.255.255.0
 service-policy output WAN-OUTPUT
!
"""

    _, parser = parse_interfaces(config)

    observations = parser.statistics[
        "validation_results"
    ]

    assert len(observations) == 1

    assert observations[0].startswith(
        "GigabitEthernet0/0:"
    )

    assert (
        "GigabitEthernetgabitEthernet"
        not in observations[0]
    )


def test_interface_statistics():

    config = """
interface Gi0/0
 ip address 10.10.10.1 255.255.255.0
!
interface Lo0
 ip address 1.1.1.1 255.255.255.255
!
interface Vl100
 ip address 192.168.100.1 255.255.255.0
!
interface Gi1/0/1
 switchport mode access
 switchport access vlan 100
!
"""

    interfaces, parser = parse_interfaces(config)

    assert len(interfaces) == 4

    stats = parser.statistics

    assert stats["interfaces"] == 4
    assert stats["loopbacks"] == 1
    assert stats["svis"] == 1
    assert stats["access_ports"] == 1

    assert stats["routed"] == 3
    assert stats["switchports"] == 1


def test_config_parser_orchestration():

    config = """
hostname Branch-RTR01
!
interface Gi0/0
 description WAN
 ip address 10.10.10.1 255.255.255.0
!
interface Lo0
 ip address 1.1.1.1 255.255.255.255
!
"""

    parser = ConfigParser(config)

    result = parser.parse()

    assert result["hostname"] == "Branch-RTR01"

    assert result["interface_count"] == 2

    assert result["physical_interface_count"] == 1

    assert result["loopback_count"] == 1

    assert (
        result["parser_metadata"]["version"]
        == "3.0"
    )

    assert (
        result["parser_metadata"]["errors"]
        == 0
    )

    assert (
        result["parser_metadata"]["parsers_executed"]
        == 7
    )