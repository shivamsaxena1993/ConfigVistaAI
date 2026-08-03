"""
=============================================================

ConfigVista AI

Enterprise Device Generator

Artifact-2

=============================================================
"""

from __future__ import annotations

from enterprise.models import (
    Device,
    Site,
    BusinessService,
)

from enterprise.generators.enterprise_generator import (
    EnterpriseGenerationConfig,
)


# ============================================================
# PLATFORM DEFINITIONS
# ============================================================

DEVICE_TYPES = {

    "CORE": {
        "platform": "Cisco Catalyst 9500",
        "vendor": "Cisco",
        "model": "C9606R",
        "os": "IOS-XE",
        "os_version": "17.12.1",
        "software_image": "cat9k_iosxe.17.12.01.SPA.bin",
    },

    "DIST": {
        "platform": "Cisco Catalyst 9300",
        "vendor": "Cisco",
        "model": "C9300-48UXM",
        "os": "IOS-XE",
        "os_version": "17.9.5",
        "software_image": "cat9k_iosxe.17.09.05.SPA.bin",
    },

    "ACCESS": {
        "platform": "Cisco Catalyst 9200",
        "vendor": "Cisco",
        "model": "C9200L-48P-4X",
        "os": "IOS-XE",
        "os_version": "17.9.5",
        "software_image": "cat9k_iosxe.17.09.05.SPA.bin",
    },

    "FW": {
        "platform": "Cisco Firepower 2130",
        "vendor": "Cisco",
        "model": "FPR2130",
        "os": "FTD",
        "os_version": "7.4.1",
        "software_image": "cisco-ftd.7.4.1.SPA",
    },

    "WAN": {
        "platform": "Cisco Catalyst 8300",
        "vendor": "Cisco",
        "model": "C8300-2N2S-6T",
        "os": "IOS-XE",
        "os_version": "17.12.1",
        "software_image": "c8000be-universalk9.17.12.01.SPA.bin",
    },

}


# ============================================================
# DEVICE GENERATOR
# ============================================================

class DeviceGenerator:
    """
    Generates enterprise devices.

    Returns Device objects only.

    Registration into InventoryService is handled
    by EnterpriseGenerator.
    """

    def __init__(self):

        self.generated_devices = []

    # --------------------------------------------------------

    def generate(
        self,
        config: EnterpriseGenerationConfig,
        sites: list[Site],
        services: list[BusinessService],
    ) -> list[Device]:
        """
        Generate the enterprise device inventory.

        Business services are intentionally ignored
        in this phase. Relationships will be created
        later by the BusinessServiceGenerator.
        """

        self.generated_devices = []

        self._generate_core_devices(
            config,
            sites,
        )

        self._generate_distribution_devices(
            config,
            sites,
        )

        self._generate_access_devices(
            config,
            sites,
        )

        self._generate_firewalls(
            config,
            sites,
        )

        self._generate_wan_devices(
            config,
            sites,
        )

        return self.generated_devices
    
    # --------------------------------------------------------
    # Internal Helper
    # --------------------------------------------------------

    def _create_device(
        self,
        prefix: str,
        number: int,
        site: Site,
    ) -> Device:
        """
        Create a single enterprise device.
        """

        profile = DEVICE_TYPES[prefix]

        device = Device(

            hostname=f"{prefix}-{number:03d}",
        
            vendor=profile["vendor"],
        
            platform=profile["platform"],
        
            model=profile.get(
                "model",
                "",
            ),
        
            os_name=profile["os"],
        
            os_version=profile.get(
                "os_version",
                "",
            ),
        
            software_image=profile.get(
                "software_image",
                "",
            ),
        
        )

        #
        # Enterprise Relationships
        #

        device.site_id = site.site_id

        #
        # Management Address
        #

        global_index = len(self.generated_devices) + 1

        device.management_ip = (
            f"10.{global_index // 255}.{global_index % 255}.1"
        )

        #
        # Device Role
        #

        device.role = prefix

        return device

    # --------------------------------------------------------
    # Core Devices
    # --------------------------------------------------------

    def _generate_core_devices(
        self,
        config: EnterpriseGenerationConfig,
        sites: list[Site],
    ) -> None:
        """
        Generate enterprise core devices.

        Core devices are placed in
        Data Centers.
        """

        dc_sites = [

            site

            for site in sites

            if site.site_type == "Data Center"

        ]

        if not dc_sites:

            return

        for index in range(

            config.core_devices

        ):

            site = dc_sites[
                index % len(dc_sites)
            ]

            device = self._create_device(

                "CORE",

                index + 1,

                site,

            )

            self.generated_devices.append(
                device
            )

    # --------------------------------------------------------
    # Distribution Devices
    # --------------------------------------------------------

    def _generate_distribution_devices(
        self,
        config: EnterpriseGenerationConfig,
        sites: list[Site],
    ) -> None:
        """
        Generate distribution devices.

        Distribution switches are
        spread across Data Centers
        and Regional Offices.
        """

        valid_sites = [

            site

            for site in sites

            if site.site_type in (

                "Data Center",

                "Regional Office",

            )

        ]

        if not valid_sites:

            return

        for index in range(

            config.distribution_devices

        ):

            site = valid_sites[
                index % len(valid_sites)
            ]

            device = self._create_device(

                "DIST",

                index + 1,

                site,

            )

            self.generated_devices.append(
                device
            )

    # --------------------------------------------------------
    # Access Devices
    # --------------------------------------------------------

    def _generate_access_devices(
        self,
        config: EnterpriseGenerationConfig,
        sites: list[Site],
    ) -> None:
        """
        Generate access switches.

        Access switches are placed across
        Regional Offices and Branches.
        """

        valid_sites = [

            site

            for site in sites

            if site.site_type in (

                "Regional Office",

                "Branch",

            )

        ]

        if not valid_sites:

            return

        for index in range(

            config.access_devices

        ):

            site = valid_sites[
                index % len(valid_sites)
            ]

            device = self._create_device(

                "ACCESS",

                index + 1,

                site,

            )

            self.generated_devices.append(
                device
            )

    # --------------------------------------------------------
    # Firewalls
    # --------------------------------------------------------

    def _generate_firewalls(
        self,
        config: EnterpriseGenerationConfig,
        sites: list[Site],
    ) -> None:
        """
        Generate enterprise firewalls.
        """

        dc_sites = [

            site

            for site in sites

            if site.site_type == "Data Center"

        ]

        if not dc_sites:

            return

        for index in range(

            config.firewall_devices

        ):

            site = dc_sites[
                index % len(dc_sites)
            ]

            device = self._create_device(

                "FW",

                index + 1,

                site,

            )

            self.generated_devices.append(
                device
            )

    # --------------------------------------------------------
    # WAN Edge
    # --------------------------------------------------------

    def _generate_wan_devices(
        self,
        config: EnterpriseGenerationConfig,
        sites: list[Site],
    ) -> None:
        """
        Generate WAN edge routers.
        """

        valid_sites = [

            site

            for site in sites

            if site.site_type in (

                "Data Center",

                "Branch",

            )

        ]

        if not valid_sites:

            return

        for index in range(

            config.wan_edge_devices

        ):

            site = valid_sites[
                index % len(valid_sites)
            ]

            device = self._create_device(

                "WAN",

                index + 1,

                site,

            )

            self.generated_devices.append(
                device
            )

    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------

    def statistics(
        self,
    ) -> dict:
        """
        Returns generation statistics.
        """

        return {

            "total_devices": len(
                self.generated_devices
            ),

            "core": sum(

                1

                for d in self.generated_devices

                if d.role == "CORE"

            ),

            "distribution": sum(

                1

                for d in self.generated_devices

                if d.role == "DIST"

            ),

            "access": sum(

                1

                for d in self.generated_devices

                if d.role == "ACCESS"

            ),

            "firewalls": sum(

                1

                for d in self.generated_devices

                if d.role == "FW"

            ),

            "wan": sum(

                1

                for d in self.generated_devices

                if d.role == "WAN"

            ),

        }

    # --------------------------------------------------------
    # Reset
    # --------------------------------------------------------

    def reset(
        self,
    ) -> None:
        """
        Clear generated devices.
        """

        self.generated_devices.clear()

    # --------------------------------------------------------
    # Utility Methods
    # --------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return len(
            self.generated_devices
        )

    # --------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        stats = self.statistics()

        return (

            "DeviceGenerator("

            f"devices={stats['total_devices']}, "

            f"core={stats['core']}, "

            f"dist={stats['distribution']}, "

            f"access={stats['access']}, "

            f"fw={stats['firewalls']}, "

            f"wan={stats['wan']})"

        )