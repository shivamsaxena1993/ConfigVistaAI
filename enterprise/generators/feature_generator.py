from __future__ import annotations

from collections import Counter

from enterprise.generators.enterprise_generator import (
    EnterpriseGenerationConfig,
)

from enterprise.models import (
    BusinessService,
    ConfigurationBackup,
    Device,
    DeviceId,
    FeatureVector,
    HistoricalChange,
    Incident,
    OperationalSnapshot,
    Site
)


class FeatureGenerator:

    """
    Generates machine-learning feature vectors by combining
    enterprise datasets into one engineered record per
    historical change.

    One HistoricalChange
            ↓
    One FeatureVector
    """

    # ========================================================
    # Constructor
    # ========================================================

    def __init__(self):

        self.generated_features: list[
            FeatureVector
        ] = []

    # ========================================================
    # Generation
    # ========================================================

    def generate(

        self,

        config: EnterpriseGenerationConfig,

        sites: list[Site],

        devices: list[Device],

        business_services: list[BusinessService],

        changes: list[HistoricalChange],

        incidents: list[Incident],

        configuration_backups: list[ConfigurationBackup],

        operational_snapshots: list[OperationalSnapshot],

    ) -> list[FeatureVector]:

        self.generated_features.clear()

        device_lookup: dict[DeviceId, Device] = {

            device.device_id: device

            for device

            in devices

        }

        site_lookup: dict[SiteId, Site] = {

            site.site_id: site

            for site

            in sites

        }

        service_lookup: dict[BusinessServiceId, BusinessService,] = {

            service.service_id: service

            for service

            in business_services

        }

        backup_lookup: dict[DeviceId, ConfigurationBackup,] = {

            backup.device_id: backup

            for backup

            in configuration_backups

        }

        snapshot_lookup: dict[DeviceId, OperationalSnapshot,] = {

            snapshot.device_id: snapshot

            for snapshot

            in operational_snapshots

        }

        history = self._initialize_history()

        for change in changes:
        
            feature = self._build_feature_vector(
            
                change,

                device_lookup,

                site_lookup,

                service_lookup,

                backup_lookup,

                snapshot_lookup,

                history,

            )

            self.generated_features.append(
            
                feature,

            )

            current_incidents = self._count_current_incidents(
            
                change,

                incidents,

            )

            self._update_history(

                change.primary_device_id,
            
                history,

                change,

                current_incidents,

            )

        return self.generated_features

    def _initialize_history(
        self,
    ) -> dict:
        """
        Maintain historical statistics per device.
        """

        return {

            "devices": {}

        }
    
    def _get_history_metrics(

        self,

        device_id: DeviceId,

        history: dict,

    ) -> dict:
        """
        Return historical metrics for a device BEFORE
        the current change.
        """

        device_history = history["devices"].setdefault(

            device_id,

            {

                "successful_changes": 0,

                "failed_changes": 0,

                "rollback_history": 0,

                "previous_incidents": 0,

                "critical_incidents": 0,

            },

        )

        return device_history.copy()
    
    def _count_current_incidents(

        self,

        change: HistoricalChange,

        incidents: list[Incident],

    ) -> dict:

        related = [

            incident

            for incident

            in incidents

            if incident.related_change_id
            == change.change_id

        ]

        return {

            "previous_incidents":

                len(related),

            "critical_incidents":

                sum(

                    1

                    for incident

                    in related

                    if incident.severity
                    == "Critical"

                ),

        }
    
    def _update_history(

        self,
    
        device_id: DeviceId,
    
        history: dict,
    
        change: HistoricalChange,
    
        current_incidents: dict,
    
    ) -> None:
        """
        Update device history AFTER generating
        the feature vector.
        """

        device_history = history["devices"].setdefault(

            device_id,

            {

                "successful_changes": 0,

                "failed_changes": 0,

                "rollback_history": 0,

                "previous_incidents": 0,

                "critical_incidents": 0,

            },

        )

        if change.actual_outcome.lower() == "successful":

            device_history["successful_changes"] += 1

        else:

            device_history["failed_changes"] += 1

        if change.rollback_required:

            device_history["rollback_history"] += 1

        device_history["previous_incidents"] += (

            current_incidents["previous_incidents"]

        )

        device_history["critical_incidents"] += (

            current_incidents["critical_incidents"]

        )
    # ========================================================
    # Feature Engineering
    # ========================================================

    def _build_feature_vector(

        self,

        change: HistoricalChange,

        device_lookup: dict,

        site_lookup: dict,

        service_lookup: dict,

        backup_lookup: dict,

        snapshot_lookup: dict,

        history: dict,

    ) -> FeatureVector:

        device = device_lookup.get(

            change.primary_device_id

        )

        site = site_lookup.get(

            change.site_id

        )

        service = service_lookup.get(

            change.business_service_id

        )

        backup = backup_lookup.get(

            change.primary_device_id

        )

        snapshot = snapshot_lookup.get(

            change.primary_device_id

        )

        history_metrics = self._get_history_metrics(

            change.primary_device_id,

            history,

        )

        

        deployment_successful = (

            change.actual_outcome.lower()

            ==

            "successful"

        )

        feature = FeatureVector(

            # ------------------------------------------------
            # Identity
            # ------------------------------------------------

            change_id=change.change_id,

            device_id=change.primary_device_id,

            site_id=change.site_id,

            business_service_id=change.business_service_id,

            # ------------------------------------------------
            # Change Features
            # ------------------------------------------------

            change_scope=change.change_scope,

            change_category=change.change_category,

            change_type=change.change_type,

            predicted_risk=change.predicted_risk,

            risk_score=change.risk_score,

            confidence_score=change.confidence_score,

            business_impact=change.business_impact,

            # ------------------------------------------------
            # Device Features
            # ------------------------------------------------

            device_role=(
                device.role
                if device
                else ""
            ),

            vendor=(
                device.vendor
                if device
                else ""
            ),

            model=(
                device.model
                if device
                else ""
            ),

            os_version=(
                device.os_version
                if device
                else ""
            ),

            criticality=(
                device.criticality
                if device
                else ""
            ),

            operational_status=(
                device.operational_status
                if device
                else ""
            ),

            current_health_score=(
                device.current_health_score
                if device
                else 100.0
            ),

            availability_percent=(
                device.availability_percent
                if device
                else 100.0
            ),

            # ------------------------------------------------
            # Operational Features
            # ------------------------------------------------

            cpu_utilization=(
                snapshot.cpu_utilization
                if snapshot
                else 0.0
            ),

            memory_utilization=(
                snapshot.memory_utilization
                if snapshot
                else 0.0
            ),

            temperature_celsius=(
                snapshot.temperature_celsius
                if snapshot
                else 0.0
            ),

            latency_ms=(
                snapshot.latency_ms
                if snapshot
                else 0.0
            ),

            jitter_ms=(
                snapshot.jitter_ms
                if snapshot
                else 0.0
            ),

            packet_loss_percent=(
                snapshot.packet_loss_percent
                if snapshot
                else 0.0
            ),

            interfaces_down=(
                snapshot.interfaces_down
                if snapshot
                else 0
            ),

            crc_errors=(
                snapshot.crc_errors
                if snapshot
                else 0
            ),

            routing_converged=(
                snapshot.routing_converged
                if snapshot
                else True
            ),

            # ------------------------------------------------
            # Configuration Features
            # ------------------------------------------------

            backup_type=(
                backup.backup_type
                if backup
                else ""
            ),

            configuration_version=(
                backup.configuration_version
                if backup
                else ""
            ),

            configuration_size=(

                len(
                
                    backup.configuration_text

                )

                if backup

                else 0

            ),

            line_count=(
                backup.line_count
                if backup
                else 0
            ),

            feature_count=(
                len(
                    backup.feature_summary
                )
                if backup
                else 0
            ),

            # ------------------------------------------------
            # Historical Features
            # ------------------------------------------------

            previous_incidents=(

                history_metrics[
                    "previous_incidents"
                ]

            ),

            critical_incidents=(
            
                history_metrics[
                    "critical_incidents"
                ]

            ),

            successful_changes=(
            
                history_metrics[
                    "successful_changes"
                ]

            ),

            failed_changes=(
            
                history_metrics[
                    "failed_changes"
                ]

            ),

            rollback_history=(
            
                history_metrics[
                    "rollback_history"
                ]

            ),

            # ------------------------------------------------
            # Business Features
            # ------------------------------------------------

            service_criticality=(

                service.criticality

                if service

                else ""

            ),

            site_type=(

                site.site_type

                if site

                else ""

            ),

            redundancy=True,

            # ------------------------------------------------
            # Target
            # ------------------------------------------------

            deployment_successful=
            deployment_successful,

        )

        return feature
    
    
    
    # ========================================================
    # Lookup
    # ========================================================

    def get_feature_vector(

        self,

        feature_vector_id: str,

    ) -> FeatureVector | None:

        for feature in self.generated_features:

            if (

                feature.feature_vector_id

                ==

                feature_vector_id

            ):

                return feature

        return None


    # ========================================================
    # Statistics
    # ========================================================

    def statistics(self) -> dict:

        total = len(

            self.generated_features

        )

        if total == 0:

            return {

                "total_features": 0,

                "high_risk": 0,

                "medium_risk": 0,

                "low_risk": 0,

                "successful": 0,

                "failed": 0,

                "average_risk": 0.0,

                "average_confidence": 0.0,

            }

        risk_counter = Counter(

            feature.predicted_risk

            for feature

            in self.generated_features

        )

        successful = sum(

            feature.deployment_successful

            for feature

            in self.generated_features

        )

        average_risk = round(

            sum(

                feature.risk_score

                for feature

                in self.generated_features

            )

            /

            total,

            2,

        )

        average_confidence = round(

            sum(

                feature.confidence_score

                for feature

                in self.generated_features

            )

            /

            total,

            2,

        )

        return {

            "total_features": total,

            "high_risk": risk_counter.get(

                "High",

                0,

            ),

            "medium_risk": risk_counter.get(

                "Medium",

                0,

            ),

            "low_risk": risk_counter.get(

                "Low",

                0,

            ),

            "successful": successful,

            "failed": (

                total

                -

                successful

            ),

            "average_risk": average_risk,

            "average_confidence": average_confidence,

        }


    # ========================================================
    # Validation
    # ========================================================

    def validate_relationships(

        self,

    ) -> bool:

        for feature in self.generated_features:

            if feature.change_id is None:

                return False

            if feature.device_id is None:

                return False

            if feature.site_id is None:

                return False

            if (

                feature.business_service_id

                is None

            ):

                return False

        return True
    
    # ========================================================
    # Export
    # ========================================================

    def export_dataframe(self):

        from dataclasses import asdict

        import pandas as pd

        return pd.DataFrame(

            [

                asdict(feature)

                for feature

                in self.generated_features

            ]

        )


    def export_csv(

        self,

        filename: str,

    ):

        dataframe = self.export_dataframe()

        dataframe.to_csv(

            filename,

            index=False,

        )


    # ========================================================
    # Reset
    # ========================================================

    def reset(self):

        self.generated_features.clear()


    # ========================================================
    # Length
    # ========================================================

    def __len__(self):

        return len(

            self.generated_features

        )


    # ========================================================
    # Representation
    # ========================================================

    def __repr__(self):

        stats = self.statistics()

        return (

            "FeatureGenerator("

            f"features={stats['total_features']}, "

            f"high={stats['high_risk']}, "

            f"medium={stats['medium_risk']}, "

            f"low={stats['low_risk']}, "

            f"successful={stats['successful']}, "

            f"failed={stats['failed']}, "

            f"avg_risk={stats['average_risk']:.2f}, "

            f"avg_confidence={stats['average_confidence']:.2f})"

        )

    
    
