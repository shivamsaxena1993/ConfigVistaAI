"""
=============================================================

ConfigVista AI

Enterprise Configuration Backup Generator

Artifact-2

=============================================================
"""

from __future__ import annotations

import hashlib

from enterprise.models import (

    ConfigurationBackup,
    Device,
    DEVICE_ROLE_MAPPING,

)

from enterprise.generators.enterprise_generator import (

    EnterpriseGenerationConfig,

)


# ============================================================
# CONFIGURATION BACKUP GENERATOR
# ============================================================

class ConfigurationBackupGenerator:
    """
    Generates deterministic Running and Startup
    configuration backups for every enterprise
    device.

    These backups become the source for
    configuration comparison, feature
    extraction and AI-based risk prediction.
    """

    def __init__(self):

        self.generated_backups = []


    # --------------------------------------------------------

    def generate(

        self,

        config: EnterpriseGenerationConfig,

        devices: list[Device],

    ) -> list[ConfigurationBackup]:
        """
        Generate configuration backups.

        Every device receives

        • Running Configuration
        • Startup Configuration
        """

        self.generated_backups.clear()

        for device in devices:

            #
            # Ensure deterministic generation by
            # clearing previous backup relationships.
            #

            device.clear_configuration_backups()

            #
            # Running backup
            #

            running = self._create_backup(
            
                device,

                backup_type="Running",

            )

            #
            # Startup backup
            #

            startup = self._create_backup(
            
                device,

                backup_type="Startup",

            )

            #
            # Store generated backups
            #

            self.generated_backups.extend(
            
                [
                
                    running,

                    startup,

                ]

            )

            #
            # Maintain relationships
            #

            device.add_configuration_backup(
            
                running.backup_id

            )

            device.add_configuration_backup(
            
                startup.backup_id

            )

        return self.generated_backups

    # --------------------------------------------------------
    # Internal Helpers
    # --------------------------------------------------------

    def _create_backup(

        self,

        device: Device,

        backup_type: str,

    ) -> ConfigurationBackup:
        """
        Create a configuration backup for a
        single enterprise device.
        """

        configuration = self._render_configuration(
            device
        )

        configuration_hash = hashlib.sha256(

            configuration.encode("utf-8")

        ).hexdigest()

        checksum = hashlib.md5(

            configuration.encode("utf-8")

        ).hexdigest()

        features = self._feature_summary(
            device
        )

        backup = ConfigurationBackup(

            device_id=device.device_id,

            hostname=device.hostname,

            device_role=device.normalized_role,

            backup_type=backup_type,

            configuration_version="v1",

            configuration_text=configuration,

            configuration_hash=configuration_hash,

            checksum=checksum,

            line_count=len(

                configuration.splitlines()

            ),

            feature_summary=features,

            backup_source="Generated",

            generated_from_template=True,

        )

        return backup


    # --------------------------------------------------------

    def _render_configuration(

        self,

        device: Device,

    ) -> str:
        """
        Select the appropriate configuration template
        based on the device role.
        """

        role = device.normalized_role

        if "CORE" in role:

            return self._core_configuration(device)

        elif "DISTRIBUTION" in role:

            return self._distribution_configuration(device)

        elif "ACCESS" in role:

            return self._access_configuration(device)

        elif "FIREWALL" in role:

            return self._firewall_configuration(device)

        elif "WAN" in role:

            return self._wan_configuration(device)

        # Safe default
        return self._wan_configuration(device)


    # --------------------------------------------------------

    def _feature_summary(

        self,

        device: Device,

    ) -> dict[str, int | bool]:
        """
        Generate a lightweight feature summary.
        """

        role = device.normalized_role

        is_core = "CORE" in role
        is_distribution = "DISTRIBUTION" in role
        is_access = "ACCESS" in role
        is_firewall = "FIREWALL" in role
        is_wan = "WAN" in role

        return {

            "interfaces": 24,

            "ospf": not is_access,

            "bgp": is_core or is_wan,

            "acl": is_core or is_firewall,

            "nat": is_firewall,

            "qos": not is_access,

            "vlans": is_access or is_distribution,

        }
    # --------------------------------------------------------
    # Configuration Templates
    # --------------------------------------------------------

    def _core_configuration(
        self,
        device: Device,
    ) -> str:

        return f"""!
version 17.9
hostname {device.hostname}
!
service timestamps debug datetime msec
service timestamps log datetime msec
!
ip domain-name configvista.local
!
interface Loopback0
 ip address {device.management_ip} 255.255.255.255
!
interface HundredGigE0/0/0
 description CORE-UPLINK-1
 no shutdown
!
interface HundredGigE0/0/1
 description CORE-UPLINK-2
 no shutdown
!
router ospf 100
 router-id {device.management_ip}
 network 0.0.0.0 255.255.255.255 area 0
!
router bgp 65000
 bgp log-neighbor-changes
 neighbor 10.255.255.1 remote-as 65000
 address-family ipv4
  neighbor 10.255.255.1 activate
 exit-address-family
!
snmp-server community public RO
logging host 10.10.10.10
ntp server 10.10.10.20
!
end
"""


    # --------------------------------------------------------

    def _distribution_configuration(
        self,
        device: Device,
    ) -> str:

        return f"""!
version 17.9
hostname {device.hostname}
!
interface Loopback0
 ip address {device.management_ip} 255.255.255.255
!
vlan 10
 name USERS
!
vlan 20
 name VOICE
!
interface Port-channel1
 description CORE-UPLINK
!
interface TenGigabitEthernet1/0/1
 channel-group 1 mode active
!
spanning-tree mode rapid-pvst
!
router ospf 100
 router-id {device.management_ip}
!
ip routing
!
snmp-server community public RO
logging host 10.10.10.10
!
end
"""


    # --------------------------------------------------------

    def _access_configuration(
        self,
        device: Device,
    ) -> str:

        return f"""!
version 17.9
hostname {device.hostname}
!
interface Vlan1
 ip address {device.management_ip} 255.255.255.0
!
interface GigabitEthernet1/0/1
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
!
interface GigabitEthernet1/0/2
 switchport mode access
 switchport access vlan 20
 spanning-tree portfast
!
storm-control broadcast level 5
!
snmp-server community public RO
logging host 10.10.10.10
!
end
"""


    # --------------------------------------------------------

    def _firewall_configuration(
        self,
        device: Device,
    ) -> str:

        return f"""!
hostname {device.hostname}
!
interface GigabitEthernet0/0
 nameif outside
 security-level 0
 ip address {device.management_ip} 255.255.255.0
!
interface GigabitEthernet0/1
 nameif inside
 security-level 100
!
object network INSIDE-NET
 subnet 10.0.0.0 255.255.255.0
!
nat (inside,outside) dynamic interface
!
access-list OUTSIDE-IN permit ip any any
access-group OUTSIDE-IN in interface outside
!
logging enable
snmp-server community public
!
end
"""


    # --------------------------------------------------------

    def _wan_configuration(
        self,
        device: Device,
    ) -> str:

        return f"""!
version 17.9
hostname {device.hostname}
!
interface Loopback0
 ip address {device.management_ip} 255.255.255.255
!
interface GigabitEthernet0/0
 description MPLS
!
interface GigabitEthernet0/1
 description INTERNET
!
router bgp 65100
 bgp log-neighbor-changes
 neighbor 172.16.0.1 remote-as 65000
!
ip sla 1
 icmp-echo 8.8.8.8
 frequency 30
!
track 1 ip sla 1
!
logging host 10.10.10.10
!
end
"""
    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------

    def statistics(
        self,
    ) -> dict:

        total = len(self.generated_backups)

        stats = {

            "total_backups": total,

            "running": 0,

            "startup": 0,

            "core": 0,

            "distribution": 0,

            "access": 0,

            "firewall": 0,

            "wan": 0,

        }

        for backup in self.generated_backups:

            role = backup.device_role

            if backup.backup_type == "Running":
                stats["running"] += 1

            elif backup.backup_type == "Startup":
                stats["startup"] += 1

            if "CORE" in role:
                stats["core"] += 1

            elif "DISTRIBUTION" in role:
                stats["distribution"] += 1

            elif "ACCESS" in role:
                stats["access"] += 1

            elif "FIREWALL" in role:
                stats["firewall"] += 1

            elif "WAN" in role:
                stats["wan"] += 1

        return stats


    # --------------------------------------------------------
    # Lookup Helpers
    # --------------------------------------------------------

    def get_backup(

        self,

        backup_id,

    ) -> ConfigurationBackup | None:
        """
        Return a backup by its ID.
        """

        for backup in self.generated_backups:

            if backup.backup_id == backup_id:

                return backup

        return None


    # --------------------------------------------------------

    def running_backups(
        self,
    ) -> list[ConfigurationBackup]:

        return [

            backup

            for backup

            in self.generated_backups

            if backup.backup_type == "Running"

        ]


    # --------------------------------------------------------

    def startup_backups(
        self,
    ) -> list[ConfigurationBackup]:

        return [

            backup

            for backup

            in self.generated_backups

            if backup.backup_type == "Startup"

        ]


    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    def validate_relationships(
        self,
    ) -> bool:
        """
        Ensure every generated backup
        is associated with a device.
        """

        for backup in self.generated_backups:

            if backup.device_id is None:

                return False

            if backup.hostname == "":

                return False

            if backup.configuration_text == "":

                return False

            if backup.configuration_hash == "":

                return False

            if backup.checksum == "":

                return False

        return True


    # --------------------------------------------------------
    # Reset
    # --------------------------------------------------------

    def reset(
        self,
    ) -> None:

        self.generated_backups.clear()


    # --------------------------------------------------------
    # Utility Methods
    # --------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return len(
            self.generated_backups
        )


    # --------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        stats = self.statistics()

        return (

            "ConfigurationBackupGenerator("

            f"backups={stats['total_backups']}, "

            f"running={stats['running']}, "

            f"startup={stats['startup']}, "

            f"core={stats['core']}, "

            f"distribution={stats['distribution']}, "

            f"access={stats['access']}, "

            f"firewall={stats['firewall']}, "

            f"wan={stats['wan']})"

        )