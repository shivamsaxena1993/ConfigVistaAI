"""
=============================================================

ConfigVista AI

Enterprise Dataset Generator

Artifact-2

Enterprise Generator

=============================================================

Responsible for orchestrating creation of a complete
synthetic enterprise environment.

The EnterpriseGenerator DOES NOT generate data directly.

Instead, it coordinates the individual generators and
populates the Enterprise Inventory.

Generation Flow

    Sites
        ↓
    Business Services
        ↓
    Devices
        ↓
    Topology
        ↓
    Historical Changes
        ↓
    Incidents
        ↓
    Configuration Snapshots
        ↓
    Operational Snapshots

=============================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from enterprise.services.inventory_service import (
    InventoryService,
)


# ============================================================
# CONFIGURATION
# ============================================================

@dataclass(slots=True)
class EnterpriseGenerationConfig:
    """
    Controls the size of the generated enterprise.
    """

    #
    # Sites
    #

    data_centers: int = 2

    regional_sites: int = 8

    branch_sites: int = 30

    #
    # Devices
    #

    core_devices: int = 40

    distribution_devices: int = 80

    access_devices: int = 140

    firewall_devices: int = 20

    wan_edge_devices: int = 20

    #
    # Historical Data
    #

    historical_changes: int = 300

    incidents: int = 200

    #
    # Snapshots
    #

    configuration_backups: int = 300

    operational_snapshots: int = 300

    #
    # Randomness
    #

    random_seed: int = 42


# ============================================================
# GENERATION STATISTICS
# ============================================================

@dataclass(slots=True)
class GenerationStatistics:
    """
    Tracks generated enterprise objects.
    """

    sites: int = 0

    business_services: int = 0

    devices: int = 0

    topology_links: int = 0

    changes: int = 0

    incidents: int = 0

    configuration_backups: int = 0

    operational_snapshots: int = 0

    completed: bool = False


# ============================================================
# ENTERPRISE GENERATOR
# ============================================================

class EnterpriseGenerator:
    """
    Enterprise Dataset Generator.

    This class coordinates all synthetic data
    generators required for ConfigVista AI.

    Individual generators are injected later
    during initialization.
    """

    def __init__(
        self,
        inventory: Optional[InventoryService] = None,
        config: Optional[
            EnterpriseGenerationConfig
        ] = None,
    ):

        #
        # Configuration
        #

        self.config = (
            config
            or EnterpriseGenerationConfig()
        )

        #
        # Inventory
        #

        self.inventory = (
            inventory
            or InventoryService()
        )

        #
        # Statistics
        #

        self.statistics = (
            GenerationStatistics()
        )

        #
        # Generator References
        #

        self.site_generator = None

        self.business_service_generator = None

        self.device_generator = None

        self.topology_generator = None

        self.change_generator = None

        self.incident_generator = None

        self.configuration_generator = None

        self.operational_generator = None

    # --------------------------------------------------------
    # Registration
    # --------------------------------------------------------

    def register_site_generator(
        self,
        generator,
    ) -> None:

        self.site_generator = generator

    # --------------------------------------------------------

    def register_business_service_generator(
        self,
        generator,
    ) -> None:

        self.business_service_generator = generator

    # --------------------------------------------------------

    def register_device_generator(
        self,
        generator,
    ) -> None:

        self.device_generator = generator

    # --------------------------------------------------------

    def register_topology_generator(
        self,
        generator,
    ) -> None:

        self.topology_generator = generator

    # --------------------------------------------------------

    def register_change_generator(
        self,
        generator,
    ) -> None:

        self.change_generator = generator

    # --------------------------------------------------------

    def register_incident_generator(
        self,
        generator,
    ) -> None:

        self.incident_generator = generator

    # --------------------------------------------------------

    def register_configuration_generator(
        self,
        generator,
    ) -> None:

        self.configuration_generator = generator

    # --------------------------------------------------------

    def register_operational_generator(
        self,
        generator,
    ) -> None:

        self.operational_generator = generator
    
    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    def validate_generators(self) -> None:
        """
        Validate that all required generators
        have been registered.
        """

        required = {

            "SiteGenerator":
                self.site_generator,

            "BusinessServiceGenerator":
                self.business_service_generator,

            "DeviceGenerator":
                self.device_generator,

            "TopologyGenerator":
                self.topology_generator,

            "ChangeGenerator":
                self.change_generator,

            "IncidentGenerator":
                self.incident_generator,

            "ConfigurationGenerator":
                self.configuration_generator,

            "OperationalGenerator":
                self.operational_generator,

        }

        missing = [

            name

            for name, generator

            in required.items()

            if generator is None

        ]

        if missing:

            raise RuntimeError(

                "Missing required generators: "

                + ", ".join(missing)

            )

    # --------------------------------------------------------
    # Main Generation Entry Point
    # --------------------------------------------------------

    def generate(self) -> InventoryService:
        """
        Generate a complete synthetic enterprise.
        """

        self.validate_generators()

        self._generate_sites()

        self._generate_business_services()

        self._generate_devices()

        self._generate_topology()

        self._generate_changes()

        self._generate_incidents()

        self._generate_configuration_backups()

        self._generate_operational_snapshots()

        self.statistics.completed = True

        return self.inventory

    # --------------------------------------------------------
    # Site Generation
    # --------------------------------------------------------

    def _generate_sites(self) -> None:

        sites = self.site_generator.generate(
            self.config
        )

        for site in sites:

            self.inventory.register_site(
                site
            )

        self.statistics.sites = len(
            sites
        )

    # --------------------------------------------------------
    # Business Service Generation
    # --------------------------------------------------------

    def _generate_business_services(
        self,
    ) -> None:

        services = (

            self.business_service_generator.generate(

                self.config

            )

        )

        for service in services:

            self.inventory.register_business_service(

                service

            )

        self.statistics.business_services = len(

            services

        )

    # --------------------------------------------------------
    # Device Generation
    # --------------------------------------------------------

    def _generate_devices(
        self,
    ) -> None:

        devices = self.device_generator.generate(

            self.config,

            list(
                self.inventory.sites.values()
            ),

            list(
                self.inventory.business_services.values()
            ),

        )

        for device in devices:

            self.inventory.register_device(
                device
            )

        self.statistics.devices = len(
            devices
        )

    # --------------------------------------------------------
    # Topology Generation
    # --------------------------------------------------------

    def _generate_topology(
        self,
    ) -> None:

        links = self.topology_generator.generate(

            self.config,

            list(
                self.inventory.devices.values()
            ),

        )

        for link in links:

            self.inventory.register_topology_link(
                link
            )

        self.statistics.topology_links = len(
            links
        )

    # --------------------------------------------------------
    # Historical Change Generation
    # --------------------------------------------------------

    def _generate_changes(
        self,
    ) -> None:

        changes = self.change_generator.generate(

            self.config,

            list(
                self.inventory.devices.values()
            ),

        )

        for change in changes:

            self.inventory.register_change(
                change
            )

        self.statistics.changes = len(
            changes
        )

        # --------------------------------------------------------
    # Incident Generation
    # --------------------------------------------------------

    def _generate_incidents(
        self,
    ) -> None:
        """
        Generate historical incidents.
        """

        incidents = self.incident_generator.generate(

            self.config,

            list(
                self.inventory.devices.values()
            ),

        )

        for incident in incidents:

            self.inventory.register_incident(
                incident
            )

        self.statistics.incidents = len(
            incidents
        )

    # --------------------------------------------------------
    # Configuration Snapshot Generation
    # --------------------------------------------------------

    def _generate_configuration_backups(
        self,
    ) -> None:
        """
        Generate configuration snapshots.
        """

        snapshots = self.configuration_generator.generate(

            self.config,

            list(
                self.inventory.devices.values()
            ),

        )

        for snapshot in snapshots:

            self.inventory.register_configuration_snapshot(
                snapshot
            )

        self.statistics.configuration_backups = len(
            snapshots
        )

    # --------------------------------------------------------
    # Operational Snapshot Generation
    # --------------------------------------------------------

    def _generate_operational_snapshots(
        self,
    ) -> None:
        """
        Generate operational snapshots.
        """

        snapshots = self.operational_generator.generate(

            self.config,

            list(
                self.inventory.devices.values()
            ),

        )

        for snapshot in snapshots:

            self.inventory.register_operational_snapshot(
                snapshot
            )

        self.statistics.operational_snapshots = len(
            snapshots
        )

    # --------------------------------------------------------
    # Reset
    # --------------------------------------------------------

    def reset(
        self,
    ) -> None:
        """
        Reset inventory and statistics.
        """

        self.inventory = InventoryService()

        self.statistics = GenerationStatistics()

    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------

    def generation_statistics(
        self,
    ) -> GenerationStatistics:
        """
        Return strongly typed statistics.
        """

        return self.statistics

    # --------------------------------------------------------

    def summary(
        self,
    ) -> dict:
        """
        Enterprise generation summary.
        """

        return {

            "sites":
                self.statistics.sites,

            "business_services":
                self.statistics.business_services,

            "devices":
                self.statistics.devices,

            "topology_links":
                self.statistics.topology_links,

            "changes":
                self.statistics.changes,

            "incidents":
                self.statistics.incidents,

            "configuration_backups":
                self.statistics.configuration_backups,

            "operational_snapshots":
                self.statistics.operational_snapshots,

            "completed":
                self.statistics.completed,

        }

    # --------------------------------------------------------
    # Utility Methods
    # --------------------------------------------------------

    def __len__(
        self,
    ) -> int:
        """
        Number of generated devices.
        """

        return self.statistics.devices

    # --------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (

            "EnterpriseGenerator("

            f"sites={self.statistics.sites}, "

            f"devices={self.statistics.devices}, "

            f"services={self.statistics.business_services}, "

            f"completed={self.statistics.completed})"

        )
