"""
=============================================================

ConfigVista AI

Enterprise Relationship Service

Artifact-2

Enterprise Relationship Engine

=============================================================
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Dict

from enterprise.models import (
    Device,
    DeviceId,
    Site,
    SiteId,
    BusinessService,
    BusinessServiceId,
    HistoricalChange,
    ChangeId,
    Incident,
    IncidentId,
)

from enterprise.services.inventory_service import (
    InventoryService,
)


# ============================================================
# RELATIONSHIP SUMMARY
# ============================================================

@dataclass(slots=True)
class RelationshipSummary:
    """
    Lightweight relationship statistics.
    """

    devices: int = 0

    sites: int = 0

    business_services: int = 0

    changes: int = 0

    incidents: int = 0


# ============================================================
# RELATIONSHIP SERVICE
# ============================================================

class RelationshipService:
    """
    Enterprise Relationship Engine.

    Responsibilities
    ----------------

    • Device ↔ Site

    • Device ↔ Business Service

    • Device ↔ Change

    • Device ↔ Incident

    • Site ↔ Business Service

    Future

    • Blast Radius

    • Dependency Chains

    • Service Impact

    • ML Feature Extraction
    """

    # --------------------------------------------------------
    # Constructor
    # --------------------------------------------------------

    def __init__(
        self,
        inventory: InventoryService,
    ):

        self.inventory = inventory

        #
        # Cached lookups
        #

        self.device_lookup: Dict[
            DeviceId,
            Device,
        ] = {}

        self.site_lookup: Dict[
            SiteId,
            Site,
        ] = {}

        self.service_lookup: Dict[
            BusinessServiceId,
            BusinessService,
        ] = {}

        self.change_lookup: Dict[
            ChangeId,
            HistoricalChange,
        ] = {}

        self.incident_lookup: Dict[
            IncidentId,
            Incident,
        ] = {}

        #
        # Relationship indexes
        #

        self.device_to_site = defaultdict(set)

        self.site_to_devices = defaultdict(set)

        self.device_to_service = defaultdict(set)

        self.service_to_devices = defaultdict(set)

        self.device_to_change = defaultdict(set)

        self.device_to_incident = defaultdict(set)

        #
        # Status
        #

        self.relationships_built = False

        #
        # Build indexes
        #

        self.build_relationships()

    # --------------------------------------------------------

    def rebuild(self):

        """
        Rebuild all relationship indexes.
        """

        self.device_lookup.clear()

        self.site_lookup.clear()

        self.service_lookup.clear()

        self.change_lookup.clear()

        self.incident_lookup.clear()

        self.device_to_site.clear()

        self.site_to_devices.clear()

        self.device_to_service.clear()

        self.service_to_devices.clear()

        self.device_to_change.clear()

        self.device_to_incident.clear()

        self.relationships_built = False

        self.build_relationships()

    # --------------------------------------------------------

    def build_relationships(self):

        """
        Build enterprise relationship indexes.

        This method reads the InventoryService
        and creates optimized lookup structures.
        """

        #
        # Cache enterprise objects
        #

        self.device_lookup = dict(
            self.inventory.devices
        )

        self.site_lookup = dict(
            self.inventory.sites
        )

        self.service_lookup = dict(
            self.inventory.business_services
        )

        self.change_lookup = dict(
            self.inventory.changes
        )

        self.incident_lookup = dict(
            self.inventory.incidents
        )

        #
        # Device → Site
        #

        for device in self.device_lookup.values():

            if device.site_id is None:
                continue

            self.device_to_site[
                device.device_id
            ].add(
                device.site_id
            )

            self.site_to_devices[
                device.site_id
            ].add(
                device.device_id
            )

        #
        # Device → Business Service
        #

        for device in self.device_lookup.values():

            for service_id in device.business_service_ids:

                self.device_to_service[
                    device.device_id
                ].add(
                    service_id
                )

                self.service_to_devices[
                    service_id
                ].add(
                    device.device_id
                )

        #
        # Device → Historical Changes
        #

        for device in self.device_lookup.values():

            for change_id in device.historical_change_ids:

                self.device_to_change[
                    device.device_id
                ].add(
                    change_id
                )

        #
        # Device → Incidents
        #

        for device in self.device_lookup.values():

            for incident_id in device.incident_ids:

                self.device_to_incident[
                    device.device_id
                ].add(
                    incident_id
                )

        self.relationships_built = True

    # --------------------------------------------------------

    def validate(self) -> bool:
        """
        Basic validation.
        """

        return self.relationships_built

    # --------------------------------------------------------
    # Device Queries
    # --------------------------------------------------------

    def get_device(
        self,
        device_id: DeviceId,
    ) -> Device | None:
        """
        Return a device by ID.
        """

        return self.device_lookup.get(
            device_id
        )

    # --------------------------------------------------------

    def has_device(
        self,
        device_id: DeviceId,
    ) -> bool:
        """
        Returns True when the device exists.
        """

        return device_id in self.device_lookup

    # --------------------------------------------------------
    # Site Queries
    # --------------------------------------------------------

    def get_site(
        self,
        site_id: SiteId,
    ) -> Site | None:
        """
        Return a site by ID.
        """

        return self.site_lookup.get(
            site_id
        )

    # --------------------------------------------------------

    def get_device_site(
        self,
        device_id: DeviceId,
    ) -> Site | None:
        """
        Returns the site that owns a device.
        """

        site_ids = self.device_to_site.get(
            device_id,
            set(),
        )

        if not site_ids:
            return None

        site_id = next(iter(site_ids))

        return self.site_lookup.get(
            site_id
        )

    # --------------------------------------------------------

    def get_site_devices(
        self,
        site_id: SiteId,
    ) -> list[Device]:
        """
        Returns all devices in a site.
        """

        devices = []

        for device_id in sorted(
            self.site_to_devices.get(
                site_id,
                set(),
            )
        ):

            device = self.device_lookup.get(
                device_id
            )

            if device is not None:

                devices.append(device)

        return devices

    # --------------------------------------------------------
    # Business Service Queries
    # --------------------------------------------------------

    def get_business_service(
        self,
        service_id: BusinessServiceId,
    ) -> BusinessService | None:
        """
        Return a business service by ID.
        """

        return self.service_lookup.get(
            service_id
        )

    # --------------------------------------------------------

    def get_device_services(
        self,
        device_id: DeviceId,
    ) -> list[BusinessService]:
        """
        Returns all business services
        hosted by a device.
        """

        services = []

        for service_id in sorted(
            self.device_to_service.get(
                device_id,
                set(),
            )
        ):

            service = self.service_lookup.get(
                service_id
            )

            if service is not None:

                services.append(service)

        return services

    # --------------------------------------------------------

    def get_service_devices(
        self,
        service_id: BusinessServiceId,
    ) -> list[Device]:
        """
        Returns all devices supporting
        a business service.
        """

        devices = []

        for device_id in sorted(
            self.service_to_devices.get(
                service_id,
                set(),
            )
        ):

            device = self.device_lookup.get(
                device_id
            )

            if device is not None:

                devices.append(device)

        return devices

    # --------------------------------------------------------
    # Historical Change Queries
    # --------------------------------------------------------

    def get_device_changes(
        self,
        device_id: DeviceId,
    ) -> list[HistoricalChange]:
        """
        Returns historical changes
        for a device.
        """

        changes = []

        for change_id in sorted(
            self.device_to_change.get(
                device_id,
                set(),
            )
        ):

            change = self.change_lookup.get(
                change_id
            )

            if change is not None:

                changes.append(change)

        return changes

    # --------------------------------------------------------
    # Incident Queries
    # --------------------------------------------------------

    def get_device_incidents(
        self,
        device_id: DeviceId,
    ) -> list[Incident]:
        """
        Returns historical incidents
        for a device.
        """

        incidents = []

        for incident_id in sorted(
            self.device_to_incident.get(
                device_id,
                set(),
            )
        ):

            incident = self.incident_lookup.get(
                incident_id
            )

            if incident is not None:

                incidents.append(incident)

        return incidents

    # --------------------------------------------------------
    # Relationship Summary
    # --------------------------------------------------------

    def relationship_summary(
        self,
    ) -> RelationshipSummary:
        """
        Returns relationship statistics.
        """

        return RelationshipSummary(

            devices=len(
                self.device_lookup
            ),

            sites=len(
                self.site_lookup
            ),

            business_services=len(
                self.service_lookup
            ),

            changes=len(
                self.change_lookup
            ),

            incidents=len(
                self.incident_lookup
            ),
        )
    # --------------------------------------------------------
    # Site Relationship Queries
    # --------------------------------------------------------

    def get_site_services(
        self,
        site_id: SiteId,
    ) -> list[BusinessService]:
        """
        Returns all business services
        hosted within a site.
        """

        services = {}

        for device in self.get_site_devices(
            site_id
        ):

            for service in self.get_device_services(
                device.device_id
            ):

                services[
                    service.service_id
                ] = service

        return sorted(
            services.values(),
            key=lambda s: s.service_name,
        )

    # --------------------------------------------------------

    def get_site_changes(
        self,
        site_id: SiteId,
    ) -> list[HistoricalChange]:
        """
        Returns all historical changes
        associated with a site.
        """

        changes = {}

        for device in self.get_site_devices(
            site_id
        ):

            for change in self.get_device_changes(
                device.device_id
            ):

                changes[
                    change.change_id
                ] = change

        return sorted(
            changes.values(),
            key=lambda c: c.change_id,
        )

    # --------------------------------------------------------

    def get_site_incidents(
        self,
        site_id: SiteId,
    ) -> list[Incident]:
        """
        Returns all historical incidents
        associated with a site.
        """

        incidents = {}

        for device in self.get_site_devices(
            site_id
        ):

            for incident in self.get_device_incidents(
                device.device_id
            ):

                incidents[
                    incident.incident_id
                ] = incident

        return sorted(
            incidents.values(),
            key=lambda i: i.incident_id,
        )

    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------

    def statistics(self) -> dict:
        """
        Relationship statistics.
        """

        return {

            "devices":
                len(self.device_lookup),

            "sites":
                len(self.site_lookup),

            "business_services":
                len(self.service_lookup),

            "changes":
                len(self.change_lookup),

            "incidents":
                len(self.incident_lookup),

            "relationships_built":
                self.relationships_built,

        }

    # --------------------------------------------------------
    # Utility Methods
    # --------------------------------------------------------

    def __len__(self) -> int:
        """
        Number of devices managed by
        the relationship engine.
        """

        return len(
            self.device_lookup
        )

    # --------------------------------------------------------

    def __repr__(self) -> str:

        stats = self.statistics()

        return (

            "RelationshipService("

            f"devices={stats['devices']}, "

            f"sites={stats['sites']}, "

            f"services={stats['business_services']})"

        )