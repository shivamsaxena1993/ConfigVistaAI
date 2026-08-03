"""
=============================================================

ConfigVista AI

Enterprise Topology Generator

Artifact-2

=============================================================
"""

from __future__ import annotations

from enterprise.models import (
    Device,
    TopologyLink,
)

from enterprise.generators.enterprise_generator import (
    EnterpriseGenerationConfig,
)


# ============================================================
# TOPOLOGY GENERATOR
# ============================================================

class TopologyGenerator:
    """
    Generates enterprise topology links.

    Returns TopologyLink objects only.

    Registration into InventoryService is handled
    by EnterpriseGenerator.
    """

    def __init__(self):

        self.generated_links = []

    # --------------------------------------------------------

    def generate(
        self,
        config: EnterpriseGenerationConfig,
        devices: list[Device],
    ) -> list[TopologyLink]:
        """
        Build the enterprise topology.
        """

        self.generated_links = []

        #
        # Device Groups
        #

        core = [

            d

            for d in devices

            if d.role == "CORE"

        ]

        distribution = [

            d

            for d in devices

            if d.role == "DIST"

        ]

        access = [

            d

            for d in devices

            if d.role == "ACCESS"

        ]

        firewalls = [

            d

            for d in devices

            if d.role == "FW"

        ]

        wan = [

            d

            for d in devices

            if d.role == "WAN"

        ]

        #
        # Build Hierarchy
        #

        self._connect_core(
            core
        )

        self._connect_distribution(
            core,
            distribution,
        )

        self._connect_access(
            distribution,
            access,
        )

        self._connect_firewalls(
            core,
            firewalls,
        )

        self._connect_wan(
            core,
            wan,
        )

        return self.generated_links
    
    # --------------------------------------------------------
    # Interface Name Generator
    # --------------------------------------------------------

    def _interface_names(
        self,
        source: Device,
        destination: Device,
    ) -> tuple[str, str]:
        """
        Return realistic interface names based on
        the connected device types.
        """

        #
        # Backbone
        #

        if source.role == "CORE":

            return (

                "HundredGigE0/0/0",

                "FortyGigE1/0/1",

            )

        #
        # Distribution

        if source.role == "DIST":

            return (

                "TenGigabitEthernet1/1/1",

                "TenGigabitEthernet1/1/48",

            )

        #
        # Access

        if source.role == "ACCESS":

            return (

                "GigabitEthernet1/0/48",

                "GigabitEthernet1/0/1",

            )

        #
        # Firewall

        if source.role == "FW":

            return (

                "GigabitEthernet0/0",

                "GigabitEthernet0/1",

            )

        #
        # WAN

        return (

            "GigabitEthernet0/0/0",

            "GigabitEthernet0/0/1",

        )
    
    # --------------------------------------------------------
    # Internal Helper
    # --------------------------------------------------------

    def _create_link(
        self,
        source: Device,
        destination: Device,
        link_type: str = "Ethernet",
        bandwidth: str = "10G",
        media_type: str = "Fiber",
    ) -> None:
        """
        Create a topology link between two devices.

        This method enriches each link with realistic
        operational characteristics that will later be
        consumed by the Digital Twin, ML pipeline,
        dashboard and AI risk engine.
        """

        #
        # Enterprise Defaults
        #

        utilization = 15.0

        latency = 0.4

        business_critical = False

        #
        # Backbone Links
        #

        if bandwidth == "100G":

            utilization = 62.5

            latency = 0.2

            business_critical = True

        elif bandwidth == "40G":

            utilization = 47.5

            latency = 0.4

            business_critical = True

        elif bandwidth == "20G":

            utilization = 33.0

            latency = 0.8

            business_critical = True

        elif bandwidth == "10G":

            utilization = 22.0

            latency = 1.2

        #
        # Simulate healthy enterprise links
        #

        packet_loss = round(
            utilization * 0.002,
            3,
        )

        error_rate = round(
            utilization * 0.0005,
            4,
        )

        #
        # Interface Names
        #
        
        source_if, destination_if = self._interface_names(
            source,
            destination,
        )
        
        #
        # Create Link
        #
        
        link = TopologyLink(
        
            source_device_id=source.device_id,
        
            destination_device_id=destination.device_id,
        
            source_hostname=source.hostname,
        
            destination_hostname=destination.hostname,
        
            source_interface_name=source_if,
        
            destination_interface_name=destination_if,

            #
            # Discovery
            #

            discovery_protocol="LLDP",

            discovery_source="Generated",

            #
            # Link Characteristics
            #

            link_type=link_type,

            media_type=media_type,

            bandwidth=bandwidth,

            utilization_percent=utilization,

            #
            # Operational State
            #

            operational_status="UP",

            admin_status="UP",

            relationship_confidence=99.5,

            bidirectional=True,

            #
            # Telemetry
            #

            latency_ms=latency,

            packet_loss_percent=packet_loss,

            error_rate_percent=error_rate,

            #
            # Business Context
            #

            business_critical=business_critical,

            notes=(
                f"{source.hostname} <-> "
                f"{destination.hostname}"
            ),

        )

        self.generated_links.append(link)

    # --------------------------------------------------------
    # Core Connections
    # --------------------------------------------------------

    def _connect_core(
        self,
        core: list[Device],
    ) -> None:
        """
        Connect core devices together.

        Produces a resilient ring.
        """

        if len(core) < 2:

            return

        for index in range(len(core)):

            source = core[index]

            destination = core[
                (index + 1) % len(core)
            ]

            self._create_link(

                source,

                destination,

                bandwidth="100G",

            )

    # --------------------------------------------------------
    # Distribution Connections
    # --------------------------------------------------------

    def _connect_distribution(
        self,
        core: list[Device],
        distribution: list[Device],
    ) -> None:
        """
        Connect every distribution switch
        to a core switch.
        """

        if not core:

            return

        for index, device in enumerate(

            distribution

        ):

            upstream = core[
                index % len(core)
            ]

            self._create_link(

                upstream,

                device,

                bandwidth="40G",

            )

    # --------------------------------------------------------
    # Access Connections
    # --------------------------------------------------------

    def _connect_access(
        self,
        distribution: list[Device],
        access: list[Device],
    ) -> None:
        """
        Connect every access switch to a
        distribution switch.
        """

        if not distribution:
            return

        for index, device in enumerate(access):

            upstream = distribution[
                index % len(distribution)
            ]

            self._create_link(
                upstream,
                device,
                bandwidth="10G",
                media_type="Fiber",
            )

    # --------------------------------------------------------
    # Firewall Connections
    # --------------------------------------------------------

    def _connect_firewalls(
        self,
        core: list[Device],
        firewalls: list[Device],
    ) -> None:
        """
        Connect firewalls to the core.
        """

        if not core:
            return

        for index, firewall in enumerate(firewalls):

            upstream = core[
                index % len(core)
            ]

            self._create_link(
                upstream,
                firewall,
                bandwidth="20G",
                media_type="Fiber",
            )

    # --------------------------------------------------------
    # WAN Connections
    # --------------------------------------------------------

    def _connect_wan(
        self,
        core: list[Device],
        wan: list[Device],
    ) -> None:
        """
        Connect WAN edge routers to the core.
        """

        if not core:
            return

        for index, router in enumerate(wan):

            upstream = core[
                index % len(core)
            ]

            self._create_link(
                upstream,
                router,
                bandwidth="5G",
                media_type="Fiber",
            )

    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------

    def statistics(self) -> dict:

        return {

            "total_links": len(self.generated_links),

            "wan_links": sum(
                1
                for link in self.generated_links
                if link.bandwidth == "5G"
            ),
            "core_links": sum(
                1
                for link in self.generated_links
                if link.bandwidth == "100G"
            ),

            "distribution_links": sum(
                1
                for link in self.generated_links
                if link.bandwidth == "40G"
            ),

            "firewall_links": sum(
                1
                for link in self.generated_links
                if link.bandwidth == "20G"
            ),

            "access_links": sum(
                1
                for link in self.generated_links
                if link.bandwidth == "10G"
            )
        }

    # --------------------------------------------------------

    def reset(self) -> None:

        self.generated_links.clear()

    # --------------------------------------------------------

    def __len__(self) -> int:

        return len(self.generated_links)

    # --------------------------------------------------------

    def __repr__(self) -> str:

        stats = self.statistics()

        return (

            "TopologyGenerator("

            f"links={stats['total_links']}, "

            f"core={stats['core_links']}, "

            f"distribution={stats['distribution_links']}, "

            f"access={stats['access_links']})"

        )

    
