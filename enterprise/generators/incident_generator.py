"""
=============================================================

ConfigVista AI

Enterprise Incident Generator

Artifact-2

=============================================================
"""

from __future__ import annotations

from datetime import timedelta

from enterprise.models import (

    Incident,

    HistoricalChange,

    Device,

    Site,

    BusinessService,

)

from enterprise.generators.enterprise_generator import (

    EnterpriseGenerationConfig,

)


# ============================================================
# STATIC DATA
# ============================================================

ROOT_CAUSES = {

    "Routing": "Routing Failure",

    "Switching": "Layer-2 Loop",

    "Firewall": "Firewall Policy Error",

    "VPN": "Tunnel Failure",

    "QoS": "QoS Misconfiguration",

    "Wireless": "Wireless Controller Issue",

    "System": "System Configuration Error",

    "Software Upgrade": "Software Defect",

    "Interface": "Interface Failure",

    "Security Policy": "Security Policy Error",

}


RESOLUTION_CODES = {

    "Routing": "Configuration Fix",

    "Switching": "Configuration Rollback",

    "Firewall": "Configuration Rollback",

    "VPN": "Tunnel Re-established",

    "QoS": "QoS Policy Updated",

    "Wireless": "Controller Synchronization",

    "System": "System Restart",

    "Software Upgrade": "Software Patch",

    "Interface": "Interface Reset",

    "Security Policy": "Policy Updated",

}


ASSIGNMENT_GROUPS = {

    "Routing": "Core Network",

    "Switching": "Data Center",

    "Firewall": "Security Operations",

    "VPN": "WAN Operations",

    "QoS": "Core Network",

    "Wireless": "Wireless Operations",

    "System": "Automation Team",

    "Software Upgrade": "Automation Team",

    "Interface": "WAN Operations",

    "Security Policy": "Security Operations",

}


# ============================================================
# INCIDENT GENERATOR
# ============================================================

class IncidentGenerator:
    """
    Enterprise Incident Generator.

    Generates realistic incidents from
    historical changes to simulate an
    operational enterprise environment.
    """

    def __init__(self):

        self.generated_incidents = []

        self._processed_changes = 0

    # --------------------------------------------------------

    def generate(

        self,

        config: EnterpriseGenerationConfig,

        sites: list[Site],

        devices: list[Device],

        business_services: list[BusinessService],

        historical_changes: list[HistoricalChange],

    ) -> list[Incident]:
        """
        Generate enterprise incidents.

        Incidents are derived from
        historical changes rather than
        being generated independently.
        """

        self.generated_incidents.clear()

        self._processed_changes = len(

            historical_changes

        )

        incident_index = 1

        for change in historical_changes:

            if not self._should_generate_incident(

                change

            ):

                continue

            count = self._incident_count(

                change

            )

            for occurrence in range(count):

                incident = self._create_incident(
                
                    incident_index,

                    occurrence,

                    change,

                    sites,

                    devices,

                    business_services,

                )

                self.generated_incidents.append(

                    incident

                )

                incident_index += 1

        return self.generated_incidents
    
    # ========================================================
    # Incident Generation
    # ========================================================

    def _incident_count(

        self,

        change: HistoricalChange,

    ) -> int:
        """
        Determine how many incidents
        are created from an eligible change.
        """

        count = 1

        if change.predicted_risk.lower() == "high":

            count += 1

        if change.change_scope == "Global":

            count += 1

        elif change.change_scope == "Regional":

            count += 1

        if change.business_impact == "High":

            count += 1

        return min(count, 3)

    # --------------------------------------------------------
    # Internal Helpers
    # --------------------------------------------------------

    def _should_generate_incident(

        self,

        change: HistoricalChange,

    ) -> bool:
        """
        Determine whether a historical
        change generates one or more incidents.

        Rules

        Failed Change
            -> Always

        Successful High Risk
            -> Every 20th

        Successful Medium Risk
            -> Every 50th
        """

        if change.actual_outcome.lower() == "failed":

            return True

        number = int(

            change.change_number.split("-")[-1]

        )

        if (

            change.predicted_risk.lower() == "high"

            and number % 20 == 0

        ):

            return True

        if (

            change.predicted_risk.lower() == "medium"

            and number % 50 == 0

        ):

            return True

        return False
    
    # ========================================================
    # Incident Profiles
    # ========================================================
    
    def _incident_profile(
    
        self,
    
        occurrence: int,
    
    ) -> dict:
        """
        Return a deterministic incident profile.
        """
    
        profiles = [
        
            {
            
                "category": "Interface",
    
                "summary": "Interface instability detected",
    
                "assignment_group": "Network Operations",
    
                "root_cause": "Interface configuration mismatch",
    
            },
    
            {
            
                "category": "Routing",
    
                "summary": "Routing adjacency lost",
    
                "assignment_group": "Routing Engineering",
    
                "root_cause": "Routing protocol convergence failure",
    
            },
    
            {
            
                "category": "Application",
    
                "summary": "Application reachability degraded",
    
                "assignment_group": "Application Support",
    
                "root_cause": "Traffic forwarding disruption",
    
            },
    
        ]
    
        return profiles[
            occurrence % len(profiles)
        ]
    
    # --------------------------------------------------------

    def _create_incident(

        self,

        incident_index: int,

        occurrence: int,

        change: HistoricalChange,

        sites: list[Site],

        devices: list[Device],

        business_services: list[BusinessService],

    ) -> Incident:
        """
        Build one enterprise incident
        from a historical change.
        """

        #
        # Resolve objects
        #

        primary_device = next(

            (

                device

                for device

                in devices

                if device.device_id
                == change.primary_device_id

            ),

            None,

        )

        site = next(

            (

                site

                for site

                in sites

                if site.site_id
                == change.site_id

            ),

            None,

        )

        #
        # Incident Profile
        #

        hostname = (
        
            primary_device.hostname

            if primary_device

            else "Unknown Device"

        )

        site_name = (
        
            site.site_name

            if site

            else "Unknown Site"

        )

        number = int(
            change.change_number.split("-")[-1]
        )

        profile = self._incident_profile(
            number + occurrence
        )

        title = (
        
            f"{profile['summary']} "

            f"on {hostname} "

            f"({site_name})"

        )

        #
        # Mappings
        #

        severity = self._severity(

            change,

        )

        assignment_group = self._assignment_group(
            change,
            profile,
        )

        root_cause = self._root_cause(
            change,
            profile,
        )

        resolution_code = (
        
            self._resolution_code(
            
                change,

            )

        )

        #
        # Create Incident
        #

        # --------------------------------------------------------
        # Ensure primary device is always included
        # --------------------------------------------------------

        affected_devices = list(
        
            change.affected_device_ids

        )

        if (
        
            change.primary_device_id

            not in affected_devices

        ):

            affected_devices.insert(
            
                0,

                change.primary_device_id,

            )

        incident = Incident(

            incident_number=(
                f"INC-{incident_index:06d}"
            ),

            title=title,

            severity=severity,

            status="Closed",

            incident_category=(

                profile["category"]

            ),

            assignment_group=(
                assignment_group
            ),

            business_impact=(
                change.business_impact
            ),

            affected_device_ids=affected_devices,

            related_change_id=(
                change.change_id
            ),

            site_id=change.site_id,

            business_service_id=(
                change.business_service_id
            ),

            primary_device_id=(
                change.primary_device_id
            ),

            root_cause=root_cause,

            resolution=resolution_code,

            service_restored=True,

            resolution_code=(
                resolution_code
            ),

        )

        #
        # Realistic duration
        #

        duration = (

            15 +

            (

                incident_index % 12

            ) * 15

        )

        incident.opened_at -= timedelta(

            minutes=duration

        )

        incident.close(

            resolution_code

        )

        #
        # Maintain bidirectional
        # relationship
        #

        change.add_incident(

            incident.incident_id

        )

        return incident
    
     # --------------------------------------------------------
    # Enterprise Mapping Helpers
    # --------------------------------------------------------

    def _severity(

        self,

        change: HistoricalChange,

    ) -> str:
        """
        Determine incident severity.
        """

        if change.predicted_risk.lower() == "high":

            if change.change_scope in (
                "Regional",
                "Global",
            ):
                return "Critical"

            return "High"

        if change.predicted_risk.lower() == "medium":

            return "Medium"

        return "Low"


    # --------------------------------------------------------

    def _assignment_group(

        self,

        change: HistoricalChange,

        profile: dict | None = None,

    ) -> str:
        """
        Return responsible support group.
        """
        if profile is not None:
            return profile["assignment_group"]
        
        return ASSIGNMENT_GROUPS.get(

            change.change_type,

            "Core Network",

        )


    # --------------------------------------------------------

    def _root_cause(

        self,

        change: HistoricalChange,

        profile: dict | None = None,

    ) -> str:
        """
        Return enterprise root cause.
        """
        if profile is not None:
            return profile["root_cause"]

        return ROOT_CAUSES.get(

            change.change_type,

            "Configuration Error",

        )


    # --------------------------------------------------------

    def _resolution_code(

        self,

        change: HistoricalChange,

    ) -> str:
        """
        Return enterprise resolution code.
        """

        return RESOLUTION_CODES.get(

            change.change_type,

            "Manual Recovery",

        )


    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------

    def statistics(
        self,
    ) -> dict:
        """
        Incident generation statistics.
        """

        total = len(
            self.generated_incidents
        )

        average_incidents_per_change = round(

            total

            /

            max(

                1,

                self._processed_changes,

            ),

            2,

        )

        return {

            "total_incidents": total,

            "critical": sum(

                1

                for incident

                in self.generated_incidents

                if incident.severity == "Critical"

            ),

            "high": sum(

                1

                for incident

                in self.generated_incidents

                if incident.severity == "High"

            ),

            "medium": sum(

                1

                for incident

                in self.generated_incidents

                if incident.severity == "Medium"

            ),

            "low": sum(

                1

                for incident

                in self.generated_incidents

                if incident.severity == "Low"

            ),

            "closed": sum(

                1

                for incident

                in self.generated_incidents

                if incident.status == "Closed"

            ),

            "open": sum(

                1

                for incident

                in self.generated_incidents

                if incident.status == "Open"

            ),

            "service_restored": sum(

                1

                for incident

                in self.generated_incidents

                if incident.service_restored

            ),

            "average_incidents_per_change":

                average_incidents_per_change,

        }
    # --------------------------------------------------------
    # Lookup Helpers
    # --------------------------------------------------------

    def get_incident(

        self,

        incident_number: str,

    ) -> Incident | None:
        """
        Return incident by incident number.
        """

        for incident in self.generated_incidents:

            if incident.incident_number == incident_number:

                return incident

        return None


    # --------------------------------------------------------

    def critical_incidents(
        self,
    ) -> list[Incident]:

        return [

            incident

            for incident

            in self.generated_incidents

            if incident.severity == "Critical"

        ]


    # --------------------------------------------------------

    def high_incidents(
        self,
    ) -> list[Incident]:

        return [

            incident

            for incident

            in self.generated_incidents

            if incident.severity == "High"

        ]


    # --------------------------------------------------------

    def medium_incidents(
        self,
    ) -> list[Incident]:

        return [

            incident

            for incident

            in self.generated_incidents

            if incident.severity == "Medium"

        ]


    # --------------------------------------------------------

    def low_incidents(
        self,
    ) -> list[Incident]:

        return [

            incident

            for incident

            in self.generated_incidents

            if incident.severity == "Low"

        ]


    # --------------------------------------------------------

    def open_incidents(
        self,
    ) -> list[Incident]:

        return [

            incident

            for incident

            in self.generated_incidents

            if incident.status == "Open"

        ]


    # --------------------------------------------------------

    def closed_incidents(
        self,
    ) -> list[Incident]:

        return [

            incident

            for incident

            in self.generated_incidents

            if incident.status == "Closed"

        ]


    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    def validate_relationships(
        self,
    ) -> bool:
        """
        Validate that every incident is
        linked to enterprise entities.
        """

        for incident in self.generated_incidents:

            if incident.related_change_id is None:

                return False

            if incident.primary_device_id is None:

                return False

            if incident.site_id is None:

                return False

            if incident.business_service_id is None:

                return False

            if len(

                incident.affected_device_ids

            ) == 0:

                return False

        return True


    # --------------------------------------------------------
    # Reset
    # --------------------------------------------------------

    def reset(
        self,
    ) -> None:

        self.generated_incidents.clear()

        self._processed_changes = 0


    # --------------------------------------------------------
    # Utility Methods
    # --------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return len(

            self.generated_incidents

        )


    # --------------------------------------------------------

    def __repr__(
        self,
    ) -> str:
    
        stats = self.statistics()
    
        return (
        
            "IncidentGenerator("
    
            f"incidents={stats['total_incidents']}, "
    
            f"critical={stats['critical']}, "
    
            f"high={stats['high']}, "
    
            f"medium={stats['medium']}, "
    
            f"low={stats['low']}, "
    
            f"avg_incidents_per_change="
            f"{stats['average_incidents_per_change']})"
    
        )