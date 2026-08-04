"""
=============================================================

ConfigVista AI

Enterprise Historical Change Generator

Artifact-2

=============================================================
"""

from __future__ import annotations

from enterprise.models import (
    Device,
    Site,
    BusinessService,
    HistoricalChange,
    CHANGE_TYPES,
    CHANGE_SCOPES,
)

from enterprise.generators.enterprise_generator import (
    EnterpriseGenerationConfig,
)


# ============================================================
# STATIC DATA
# ============================================================

IMPLEMENTERS = [

    "Network Automation",

    "Core Network Team",

    "Data Center Team",

    "WAN Operations",

    "Security Operations",

]

APPROVERS = [

    "CAB",

    "Technical Review Board",

    "Network Manager",

]

MAINTENANCE_WINDOWS = [

    "Sunday 01:00",

    "Sunday 03:00",

    "Saturday 22:00",

    "Wednesday 23:00",

]

CHANGE_CATEGORIES = [

    "Standard",

    "Normal",

    "Emergency",

]

BUSINESS_IMPACTS = [

    "None",

    "Low",

    "Medium",

    "High",

]

# ============================================================
# CHANGE GENERATOR
# ============================================================

class ChangeGenerator:
    """
    Generates realistic enterprise historical
    network change records.

    The generated data forms the primary
    historical dataset used for AI training,
    risk prediction and dashboard analytics.
    """

    def __init__(self):

        self.generated_changes = []

        # --------------------------------------------------------

    def generate(

        self,

        config: EnterpriseGenerationConfig,

        sites: list[Site],

        devices: list[Device],

        business_services: list[BusinessService],

    ) -> list[HistoricalChange]:

        """
        Generate deterministic enterprise
        historical changes.
        """

        self.generated_changes.clear()

        schedule = self._build_change_schedule(
            config,
            devices,
        )

        total_changes = len(schedule)

        for index, primary_device in enumerate(schedule):
        
            scope = self._select_scope(index,total_changes,)

            affected_devices = self._select_devices(
                scope,
                devices,
                primary_device,
            )

            site = next(
                (
                    s
                    for s in sites
                    if s.site_id == primary_device.site_id
                ),
                sites[0],
            )

            service = business_services[
                index % len(business_services)
            ]

            change = self._create_change(
            
                index=index,

                primary_device=primary_device,

                affected_devices=affected_devices,

                site=site,

                service=service,

                scope=scope,

            )

            self.generated_changes.append(change)

        return self.generated_changes
    
    # ========================================================
    # Deployment Schedule
    # ========================================================

    def _build_change_schedule(
        self,
        config: EnterpriseGenerationConfig,
        devices: list[Device],
    ) -> list[Device]:

        schedule = []

        for device in devices:

            count = self._device_change_frequency(device,config,)

            schedule.extend(
                [device] * count
            )

        return schedule

    # --------------------------------------------------------

    def _device_change_frequency(

        self,
    
        device: Device,
    
        config: EnterpriseGenerationConfig,
    
    ) -> int:
        """
        Determine how many historical changes should
        be generated for a device.
        """
    
        role = (
        
            device.role.upper()
    
            if device.role
    
            else ""
    
        )
    
        frequency_map = {
        
            "CORE": config.core_device_change_frequency,
    
            "DIST": config.distribution_device_change_frequency,
    
            "FW": config.firewall_change_frequency,
    
            "ACCESS": config.access_device_change_frequency,
    
            "WAN": config.default_device_change_frequency,
    
        }
    
        return frequency_map.get(
        
            role,
    
            config.default_device_change_frequency,
    
        )
    
    # --------------------------------------------------------
    # Enterprise Selection Helpers
    # --------------------------------------------------------

    def _select_scope(

        self,

        index: int,

        total_changes: int,

    ) -> str:
        """
        Select deployment scope using
        percentage-based distribution.
        """

        progress = (

            index

            /

            max(

                1,

                total_changes,

            )

        )

        if progress < 0.60:

            return "Single Device"

        if progress < 0.80:

            return "Device Pair"

        if progress < 0.95:

            return "Site"

        if progress < 0.99:

            return "Regional"

        return "Global"


    # --------------------------------------------------------

    def _select_devices(

        self,

        scope: str,

        devices: list[Device],

        primary,

    ) -> list[Device]:
        """
        Select affected devices based on
        enterprise deployment scope.

        The selection is deterministic.
        """

        #
        # Single Device
        #

        if scope == "Single Device":

            return self._normalize_affected_devices(
            
                primary,
        
                [primary],
        
            )

        #
        # Same Site Devices
        #

        same_site = [

            device

            for device

            in devices

            if device.site_id == primary.site_id

        ]

        if scope == "Device Pair":

            return self._normalize_affected_devices(
            
                primary,

                same_site[:2],

            )

        if scope == "Site":

            return self._normalize_affected_devices(
            
                primary,

                same_site,

            )

        #
        # Regional
        #
        # Approximation:
        # first 20 devices beginning
        # with this site.
        #

        if scope == "Regional":

            start = devices.index(primary)

            end = min(

                start + 20,

                len(devices),

            )

            return self._normalize_affected_devices(

                primary,

                devices[start:end],

            )

        #
        # Global
        #

        return self._normalize_affected_devices(

            primary,

            devices,

        )
    
    # --------------------------------------------------------

    def _normalize_affected_devices(

        self,

        primary: Device,

        devices: list[Device],

    ) -> list[Device]:
        """
        Ensure the primary device is always
        the first affected device.
        """

        normalized = [

            primary,

        ]

        normalized.extend(

            device

            for device in devices

            if device.device_id != primary.device_id

        )

        return normalized


    # --------------------------------------------------------

    def _select_change_type(
        self,
        index: int,
    ) -> str:
        """
        Deterministically rotate through
        enterprise change types.
        """

        return CHANGE_TYPES[

            index % len(CHANGE_TYPES)

        ]


    # --------------------------------------------------------

    def _business_impact(

        self,

        risk_score: float,

    ) -> str:

        if risk_score >= 80:

            return "Critical"

        if risk_score >= 60:

            return "High"

        if risk_score >= 30:

            return "Medium"

        return "Low"



    # --------------------------------------------------------
    # Internal Helpers
    # --------------------------------------------------------

    def _create_change(

        self,

        index: int,

        primary_device: Device,

        affected_devices: list[Device],

        site: Site,

        service: BusinessService,

        scope: str,

    ) -> HistoricalChange:
        """
        Create a deterministic enterprise historical change.
        """

        category = CHANGE_CATEGORIES[
            index % len(CHANGE_CATEGORIES)
        ]

        change_type = self._select_change_type(
            index
        )

        risk_score = self._risk_score(
            category
        )

        #
        # Increase risk based on deployment scope
        #

        if scope == "Device Pair":

            risk_score += 5

        elif scope == "Site":

            risk_score += 10

        elif scope == "Regional":

            risk_score += 15

        elif scope == "Global":

            risk_score += 20

        risk_score = min(
            risk_score,
            100,
        )

        confidence = self._confidence_score(
            category
        )

        predicted_risk = self._predicted_risk(
            risk_score
        )

        successful = self._deployment_success(

            risk_score,

            scope,

            primary_device,

            index,

        )

        rollback = not successful

        business_impact = self._business_impact(
            risk_score
        )

        change = HistoricalChange(

            change_number=f"CHG-{index + 1:06d}",

            site_id=site.site_id,

            business_service_id=service.service_id,

            change_category=category,

            change_type=change_type,

            primary_device_id=(
                primary_device.device_id
            ),

            affected_device_ids=[

                device.device_id

                for device

                in affected_devices

            ],

            change_scope=scope,

            configuration_before=(
                f"baseline-{primary_device.hostname}"
            ),

            configuration_after=(
                f"candidate-{primary_device.hostname}"
            ),

            operational_before="Healthy",

            operational_after=(

                "Healthy"

                if successful

                else "Degraded"

            ),

            risk_score=risk_score,

            confidence_score=confidence,

            predicted_risk=predicted_risk,

            actual_outcome=(

                "Successful"

                if successful

                else "Failed"

            ),

            implemented_by=IMPLEMENTERS[
                index % len(IMPLEMENTERS)
            ],

            approved_by=APPROVERS[
                index % len(APPROVERS)
            ],

            maintenance_window=MAINTENANCE_WINDOWS[
                index % len(
                    MAINTENANCE_WINDOWS
                )
            ],

            duration_minutes=15 + (
                index % 46
            ),

            rollback_required=rollback,

            rollback_completed=rollback,

            business_impact=business_impact,

            comments=(

                f"{category} "

                f"{change_type} "

                f"change affecting "

                f"{len(affected_devices)} "

                f"device(s)"

            ),

        )

        return change


    # --------------------------------------------------------

    def _deployment_success(

        self,

        risk_score: int,

        scope: str,

        device: Device,

        seed: int,

    ) -> bool:

        import random

        random.seed(seed)

        probability = 0.95

        probability -= risk_score / 200

        if scope == "Site":

            probability -= 0.05

        elif scope == "Regional":

            probability -= 0.10

        elif scope == "Global":

            probability -= 0.15

        if device.criticality == "Critical":

            probability -= 0.05

        return random.random() < probability

    def _risk_score(
        self,
        category: str,
    ) -> int:

        if category == "Standard":

            return 20

        if category == "Normal":

            return 50

        return 85


    # --------------------------------------------------------

    def _confidence_score(
        self,
        category: str,
    ) -> float:

        if category == "Standard":

            return 97.5

        if category == "Normal":

            return 93.0

        return 88.0


    # --------------------------------------------------------

    def _predicted_risk(
        self,
        risk_score: int,
    ) -> str:

        if risk_score >= 75:

            return "High"

        if risk_score >= 40:

            return "Medium"

        return "Low"
    
    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------
    
    def statistics(
        self,
    ) -> dict:

        return {

            "total_changes": len(
                self.generated_changes
            ),

            "successful": sum(

                1

                for c

                in self.generated_changes

                if c.actual_outcome == "Successful"

            ),

            "failed": sum(

                1

                for c

                in self.generated_changes

                if c.actual_outcome == "Failed"

            ),

            "single_device": sum(

                1

                for c

                in self.generated_changes

                if c.change_scope == "Single Device"

            ),

            "device_pair": sum(

                1

                for c

                in self.generated_changes

                if c.change_scope == "Device Pair"

            ),

            "site": sum(

                1

                for c

                in self.generated_changes

                if c.change_scope == "Site"

            ),

            "regional": sum(

                1

                for c

                in self.generated_changes

                if c.change_scope == "Regional"

            ),

            "global": sum(

                1

                for c

                in self.generated_changes

                if c.change_scope == "Global"

            ),

            "high_risk": sum(

                1

                for c

                in self.generated_changes

                if c.predicted_risk == "High"

            ),

            "medium_risk": sum(

                1

                for c

                in self.generated_changes

                if c.predicted_risk == "Medium"

            ),

            "low_risk": sum(

                1

                for c

                in self.generated_changes

                if c.predicted_risk == "Low"

            ),

        }

    # --------------------------------------------------------
    # Lookup Helpers
    # --------------------------------------------------------

    def get_change(
        self,
        change_number: str,
    ) -> HistoricalChange | None:
        """
        Return a change by change number.
        """

        for change in self.generated_changes:

            if change.change_number == change_number:

                return change

        return None


    def successful_changes(
        self,
    ) -> list[HistoricalChange]:

        return [

            change

            for change

            in self.generated_changes

            if change.actual_outcome == "Successful"

        ]


    def failed_changes(
        self,
    ) -> list[HistoricalChange]:

        return [

            change

            for change

            in self.generated_changes

            if change.actual_outcome == "Failed"

        ]


    def rollback_changes(
        self,
    ) -> list[HistoricalChange]:

        return [

            change

            for change

            in self.generated_changes

            if change.rollback_required

        ]

    # --------------------------------------------------------
    # Reset
    # --------------------------------------------------------

    def reset(
        self,
    ) -> None:

        self.generated_changes.clear()

    # --------------------------------------------------------
    # Utility Methods
    # --------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return len(
            self.generated_changes
        )


    def __repr__(self) -> str:

        stats = self.statistics()

        return (

            "ChangeGenerator("

            f"changes={stats['total_changes']}, "

            f"successful={stats['successful']}, "

            f"failed={stats['failed']}, "

            f"single={stats['single_device']}, "

            f"pair={stats['device_pair']}, "

            f"site={stats['site']}, "

            f"regional={stats['regional']}, "

            f"global={stats['global']})"

        )
    
