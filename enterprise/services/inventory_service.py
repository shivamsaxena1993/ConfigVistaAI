"""
=============================================================
ConfigVista AI

Enterprise Inventory Service

Artifact-2
Enterprise Digital Twin
=============================================================
"""

from __future__ import annotations

from collections import defaultdict
from datetime import UTC, datetime

from enterprise.models import (
    BusinessService,
    ConfigurationBackup,
    Device,
    HistoricalChange,
    Incident,
    Interface,
    OperationalSnapshot,
    Site,
    TopologyLink,
)


class InventoryService:
    """
    Enterprise Inventory Manager.

    Maintains the enterprise Digital Twin inventory.

    Responsibilities
    ----------------

    • Device registration
    • Site registration
    • Interface inventory
    • Snapshot inventory
    • Incident history
    • Change history
    • Business services
    • Topology relationships

    Future Responsibilities
    -----------------------

    • CMDB synchronization
    • ServiceNow integration
    • Topology traversal
    • ML feature extraction
    """

    # =====================================================
    # Constructor
    # =====================================================

    def __init__(self):

        self.devices = {}

        self.sites = {}

        self.interfaces = {}

        self.configuration_backups = {}

        self.operational_snapshots = {}

        self.changes = {}

        self.incidents = {}

        self.business_services = {}

        self.topology_links = {}

        # -------------------------------
        # Relationship indexes
        # -------------------------------

        self.site_devices = defaultdict(list)

        self.device_interfaces = defaultdict(list)

        self.device_changes = defaultdict(list)

        self.device_incidents = defaultdict(list)

        self.device_config_snapshots = defaultdict(list)

        self.device_operational_snapshots = defaultdict(list)

        self.device_services = defaultdict(list)

        self.device_topology = defaultdict(list)

    # =====================================================
    # Device Registration
    # =====================================================

    def register_device(
        self,
        device: Device,
    ) -> Device:

        if device.device_id in self.devices:

            raise ValueError(
                f"Device already exists: {device.device_id}"
            )

        self.devices[device.device_id] = device

        if device.site_id is not None:

            self.site_devices[
                device.site_id
            ].append(
                device.device_id
            )

        return device

    # =====================================================
    # Site Registration
    # =====================================================

    def register_site(
        self,
        site: Site,
    ) -> Site:

        if site.site_id in self.sites:

            raise ValueError(
                f"Site already exists: {site.site_id}"
            )

        self.sites[
            site.site_id
        ] = site

        return site

    # =====================================================
    # Business Service Registration
    # =====================================================

    def register_business_service(
        self,
        service: BusinessService,
    ) -> BusinessService:

        if (
            service.service_id
            in self.business_services
        ):

            raise ValueError(
                "Business Service already exists."
            )

        self.business_services[
            service.service_id
        ] = service

        return service

    # =====================================================
    # Getters
    # =====================================================

    def get_device(
        self,
        device_id,
    ) -> Device | None:

        return self.devices.get(
            device_id
        )

    def get_site(
        self,
        site_id,
    ) -> Site | None:

        return self.sites.get(
            site_id
        )

    def get_business_service(
        self,
        service_id,
    ) -> BusinessService | None:

        return self.business_services.get(
            service_id
        )

    # =====================================================
    # Inventory Counts
    # =====================================================

    @property
    def total_devices(self):

        return len(
            self.devices
        )

    @property
    def total_sites(self):

        return len(
            self.sites
        )

    @property
    def total_business_services(self):

        return len(
            self.business_services
        )

    # =====================================================
    # Enterprise Summary
    # =====================================================

    def summary(self):

        return {

            "devices": self.total_devices,

            "sites": self.total_sites,

            "business_services":
                self.total_business_services,

            "interfaces":
                len(self.interfaces),

            "configuration_backups":
                len(self.configuration_backups),

            "operational_snapshots":
                len(self.operational_snapshots),

            "changes":
                len(self.changes),

            "incidents":
                len(self.incidents),

            "topology_links":
                len(self.topology_links),

            "generated":
                datetime.now(UTC),

        }
    # =====================================================
    # Interface Registration
    # =====================================================

    def register_interface(
        self,
        device_id,
        interface: Interface,
    ) -> Interface:
        """
        Register an interface for a device.

        Updates:
            • inventory registry
            • relationship index
            • Device object
        """

        device = self.get_device(device_id)
        

        if device is None:
            raise ValueError(
                f"Unknown device: {device_id}"
            )
        
        interface.device_id = device.device_id
        
        if interface.interface_id in self.interfaces:
            raise ValueError(
                f"Interface already exists: "
                f"{interface.interface_id}"
            )

        self.interfaces[
            interface.interface_id
        ] = interface

        self.device_interfaces[
            device_id
        ].append(
            interface.interface_id
        )

        device.add_interface(
            interface.interface_id
        )

        return interface

    # =====================================================
    # Interface Lookup
    # =====================================================

    def get_interface(
        self,
        interface_id,
    ) -> Interface | None:

        return self.interfaces.get(
            interface_id
        )

    # =====================================================
    # Device Interface Inventory
    # =====================================================

    def get_device_interfaces(
        self,
        device_id,
    ) -> list[Interface]:

        interface_ids = self.device_interfaces.get(
            device_id,
            [],
        )

        return [
            self.interfaces[i]
            for i in interface_ids
            if i in self.interfaces
        ]

    # =====================================================
    # Interface Removal
    # =====================================================

    def remove_interface(
        self,
        device_id,
        interface_id,
    ) -> bool:

        device = self.get_device(device_id)

        if device is None:
            return False

        if interface_id not in self.interfaces:
            return False

        del self.interfaces[
            interface_id
        ]

        if (
            interface_id
            in self.device_interfaces[
                device_id
            ]
        ):
            self.device_interfaces[
                device_id
            ].remove(
                interface_id
            )

        device.remove_interface(
            interface_id
        )

        return True

    # =====================================================
    # Interface Statistics
    # =====================================================

    @property
    def total_interfaces(self):

        return len(
            self.interfaces
        )
    
    # =====================================================
    # Configuration Snapshot Registration
    # =====================================================

    def register_configuration_backup(
        self,
        device_id,
        snapshot: ConfigurationBackup,
    ) -> ConfigurationBackup:
        """
        Register a configuration snapshot for a device.

        Updates:
            • inventory registry
            • relationship index
            • Device object
        """

        device = self.get_device(device_id)

        if device is None:
            raise ValueError(
                f"Unknown device: {device_id}"
            )
        snapshot.device_id = device.device_id
        
        if (
            snapshot.snapshot_id
            in self.configuration_backups
        ):
            raise ValueError(
                "Configuration snapshot already exists."
            )

        self.configuration_backups[
            snapshot.snapshot_id
        ] = snapshot

        self.device_config_snapshots[
            device_id
        ].append(
            snapshot.snapshot_id
        )

        device.add_configuration_snapshot(
            snapshot.snapshot_id
        )

        return snapshot

    # =====================================================
    # Operational Snapshot Registration
    # =====================================================

    def register_operational_snapshot(
        self,
        device_id,
        snapshot: OperationalSnapshot,
    ) -> OperationalSnapshot:
        """
        Register an operational snapshot for a device.
        """

        device = self.get_device(device_id)

        if device is None:
            raise ValueError(
                f"Unknown device: {device_id}"
            )
        snapshot.device_id = device.device_id

        if (
            snapshot.snapshot_id
            in self.operational_snapshots
        ):
            raise ValueError(
                "Operational snapshot already exists."
            )

        self.operational_snapshots[
            snapshot.snapshot_id
        ] = snapshot

        self.device_operational_snapshots[
            device_id
        ].append(
            snapshot.snapshot_id
        )

        device.add_operational_snapshot(
            snapshot.snapshot_id
        )

        return snapshot

    # =====================================================
    # Snapshot Lookup
    # =====================================================

    def get_configuration_snapshot(
        self,
        snapshot_id,
    ) -> ConfigurationBackup | None:

        return self.configuration_backups.get(
            snapshot_id
        )

    def get_operational_snapshot(
        self,
        snapshot_id,
    ) -> OperationalSnapshot | None:

        return self.operational_snapshots.get(
            snapshot_id
        )

    # =====================================================
    # Device Snapshot Inventory
    # =====================================================

    def get_device_configuration_history(
        self,
        device_id,
    ) -> list[ConfigurationBackup]:

        snapshot_ids = (
            self.device_config_snapshots.get(
                device_id,
                [],
            )
        )

        return [

            self.configuration_backups[snapshot_id]

            for snapshot_id in snapshot_ids

            if snapshot_id
            in self.configuration_backups
        ]

    def get_device_operational_history(
        self,
        device_id,
    ) -> list[OperationalSnapshot]:

        snapshot_ids = (
            self.device_operational_snapshots.get(
                device_id,
                [],
            )
        )

        return [

            self.operational_snapshots[snapshot_id]

            for snapshot_id in snapshot_ids

            if snapshot_id
            in self.operational_snapshots
        ]

    # =====================================================
    # Latest Snapshot Helpers
    # =====================================================

    def get_latest_configuration_snapshot(
        self,
        device_id,
    ) -> ConfigurationBackup | None:

        history = (
            self.get_device_configuration_history(
                device_id
            )
        )

        if not history:
            return None

        return history[-1]

    def get_latest_operational_snapshot(
        self,
        device_id,
    ) -> OperationalSnapshot | None:

        history = (
            self.get_device_operational_history(
                device_id
            )
        )

        if not history:
            return None

        return history[-1]

    # =====================================================
    # Snapshot Statistics
    # =====================================================

    @property
    def total_configuration_backups(self):

        return len(
            self.configuration_backups
        )

    @property
    def total_operational_snapshots(self):

        return len(
            self.operational_snapshots
        )

    # =====================================================
    # Historical Change Registration
    # =====================================================

    def register_change(
        self,
        device_id,
        change: HistoricalChange,
    ) -> HistoricalChange:
        """
        Register a historical change.

        Synchronizes:
            • inventory
            • device relationship
            • lookup indexes
        """

        device = self.get_device(device_id)

        if device is None:
            raise ValueError(
                f"Unknown device: {device_id}"
            )

        if change.change_id in self.changes:
            raise ValueError(
                f"Historical Change already exists: "
                f"{change.change_id}"
            )

        change.device_id = device.device_id

        self.changes[
            change.change_id
        ] = change

        self.device_changes[
            device.device_id
        ].append(
            change.change_id
        )

        device.add_change(
            change.change_id
        )

        return change

    # =====================================================
    # Incident Registration
    # =====================================================

    def register_incident(
        self,
        device_id,
        incident: Incident,
    ) -> Incident:
        """
        Register an incident.

        Synchronizes:
            • inventory
            • device
            • relationship indexes
        """

        device = self.get_device(device_id)

        if device is None:
            raise ValueError(
                f"Unknown device: {device_id}"
            )

        if incident.incident_id in self.incidents:
            raise ValueError(
                f"Incident already exists: "
                f"{incident.incident_id}"
            )

        if device.device_id not in incident.device_ids:

            incident.device_ids.append(
                device.device_id
            )

        self.incidents[
            incident.incident_id
        ] = incident

        self.device_incidents[
            device.device_id
        ].append(
            incident.incident_id
        )

        device.add_incident(
            incident.incident_id
        )

        return incident

    # =====================================================
    # Lookup APIs
    # =====================================================

    def get_change(
        self,
        change_id,
    ) -> HistoricalChange | None:

        return self.changes.get(
            change_id
        )

    def get_incident(
        self,
        incident_id,
    ) -> Incident | None:

        return self.incidents.get(
            incident_id
        )

    # =====================================================
    # Device Timeline
    # =====================================================

    def get_device_changes(
        self,
        device_id,
    ) -> list[HistoricalChange]:

        change_ids = self.device_changes.get(
            device_id,
            [],
        )

        return [

            self.changes[c]

            for c in change_ids

            if c in self.changes
        ]

    def get_device_incidents(
        self,
        device_id,
    ) -> list[Incident]:

        incident_ids = self.device_incidents.get(
            device_id,
            [],
        )

        return [

            self.incidents[i]

            for i in incident_ids

            if i in self.incidents
        ]

    # =====================================================
    # Timeline Helpers
    # =====================================================

    def latest_change(
        self,
        device_id,
    ) -> HistoricalChange | None:

        history = self.get_device_changes(
            device_id
        )

        if not history:
            return None

        return history[-1]

    def latest_incident(
        self,
        device_id,
    ) -> Incident | None:

        history = self.get_device_incidents(
            device_id
        )

        if not history:
            return None

        return history[-1]

    # =====================================================
    # Change / Incident Statistics
    # =====================================================

    @property
    def total_changes(self):

        return len(
            self.changes
        )

    @property
    def total_incidents(self):

        return len(
            self.incidents
        )

    # =====================================================
    # Device Operational History
    # =====================================================

    def device_timeline(
        self,
        device_id,
    ) -> dict:

        return {

            "device": self.get_device(
                device_id
            ),

            "configuration_history":
                self.get_device_configuration_history(
                    device_id
                ),

            "operational_history":
                self.get_device_operational_history(
                    device_id
                ),

            "changes":
                self.get_device_changes(
                    device_id
                ),

            "incidents":
                self.get_device_incidents(
                    device_id
                ),
        }
    
    # =====================================================
    # Business Service Relationship Management
    # =====================================================

    def attach_service_to_device(
        self,
        device_id,
        service_id,
    ) -> bool:
        """
        Associate a Business Service with a Device.
        """

        device = self.get_device(device_id)

        service = self.get_business_service(
            service_id
        )

        if device is None:

            return False

        if service is None:

            return False

        if (
            service_id
            not in self.device_services[
                device_id
            ]
        ):

            self.device_services[
                device_id
            ].append(
                service_id
            )

        device.add_business_service(
            service_id
        )

        if (
            device.device_id
            not in service.device_ids
        ):

            service.device_ids.append(
                device.device_id
            )

            service.touch()

        return True

    # =====================================================
    # Service Lookup
    # =====================================================

    def get_device_services(
        self,
        device_id,
    ) -> list[BusinessService]:

        service_ids = self.device_services.get(
            device_id,
            [],
        )

        return [

            self.business_services[s]

            for s in service_ids

            if s in self.business_services

        ]

    # =====================================================
    # Remove Service Mapping
    # =====================================================

    def detach_service_from_device(
        self,
        device_id,
        service_id,
    ) -> bool:

        device = self.get_device(device_id)

        service = self.get_business_service(
            service_id
        )

        if device is None:

            return False

        if service is None:

            return False

        if (
            service_id
            in self.device_services[
                device_id
            ]
        ):

            self.device_services[
                device_id
            ].remove(
                service_id
            )

        if (
            service_id
            in device.business_service_ids
        ):

            device.business_service_ids.remove(
                service_id
            )

            device.touch()

        if (
            device.device_id
            in service.device_ids
        ):

            service.device_ids.remove(
                device.device_id
            )

            service.touch()

        return True

    # =====================================================
    # Service Statistics
    # =====================================================

    @property
    def total_service_relationships(self):

        return sum(

            len(v)

            for v in self.device_services.values()

        )

    # =====================================================
    # Business Service Summary
    # =====================================================

    def service_summary(
        self,
        service_id,
    ) -> dict | None:

        service = self.get_business_service(
            service_id
        )

        if service is None:

            return None

        return {

            "service_id": service.service_id,

            "service_name": service.service_name,

            "criticality": service.criticality,

            "device_count":
                len(service.device_ids),

            "devices":

                [

                    self.devices[d].hostname

                    for d in service.device_ids

                    if d in self.devices

                ],

        }
    
    # =====================================================
    # Topology Registration
    # =====================================================

    def register_topology_link(
        self,
        topology: TopologyLink,
    ) -> TopologyLink:

        if (
            topology.link_id
            in self.topology_links
        ):

            raise ValueError(
                "Topology link already exists."
            )

        self.topology_links[
            topology.link_id
        ] = topology

        self.device_topology[
            topology.source_device_id
        ].append(
            topology.link_id
        )

        self.device_topology[
            topology.destination_device_id
        ].append(
            topology.link_id
        )

        source = self.get_device(
            topology.source_device_id
        )

        destination = self.get_device(
            topology.destination_device_id
        )

        if source is not None:

            source.add_topology_link(
                topology.link_id
            )

        if destination is not None:

            destination.add_topology_link(
                topology.link_id
            )

        return topology

    # =====================================================
    # Topology Lookup
    # =====================================================

    def get_topology_link(
        self,
        topology_link_id,
    ) -> TopologyLink | None:

        return self.topology_links.get(
            topology_link_id
        )

    def get_device_topology(
        self,
        device_id,
    ) -> list[TopologyLink]:

        topology_ids = self.device_topology.get(
            device_id,
            [],
        )

        return [

            self.topology_links[t]

            for t in topology_ids

            if t in self.topology_links

        ]

    # =====================================================
    # Neighbor Discovery
    # =====================================================

    def get_neighbor_devices(
        self,
        device_id,
    ) -> list[Device]:

        neighbors = []

        for link in self.get_device_topology(
            device_id
        ):

            if (
                link.source_device_id
                == device_id
            ):

                neighbor = self.get_device(
                    link.destination_device_id
                )

            else:

                neighbor = self.get_device(
                    link.source_device_id
                )

            if (
                neighbor is not None
                and neighbor
                not in neighbors
            ):

                neighbors.append(
                    neighbor
                )

        return neighbors

    # =====================================================
    # Topology Statistics
    # =====================================================

    @property
    def total_topology_links(self):

        return len(
            self.topology_links
        )

    # =====================================================
    # Enterprise Statistics
    # =====================================================

    def inventory_statistics(
        self,
    ) -> dict:

        return {

            "sites":
                self.total_sites,

            "devices":
                self.total_devices,

            "interfaces":
                self.total_interfaces,

            "configuration_backups":
                self.total_configuration_backups,

            "operational_snapshots":
                self.total_operational_snapshots,

            "changes":
                self.total_changes,

            "incidents":
                self.total_incidents,

            "business_services":
                self.total_business_services,

            "service_relationships":
                self.total_service_relationships,

            "topology_links":
                self.total_topology_links,

        }

    # =====================================================
    # Reset Inventory
    # =====================================================

    def clear(self):

        self.__init__()