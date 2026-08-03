"""
=============================================================

ConfigVista AI

Operational Snapshot Generator

=============================================================
"""

from __future__ import annotations

import random

from enterprise.generators.enterprise_generator import (
    EnterpriseGenerationConfig,
)

from enterprise.models import (
    Device,
    OperationalSnapshot,
)


class OperationalSnapshotGenerator:
    """
    Generates operational telemetry snapshots
    for enterprise network devices.
    """

    def __init__(self):

        self.generated_snapshots: list[
            OperationalSnapshot
        ] = []

        self._random = random.Random(42)

    # --------------------------------------------------------
    # Public API
    # --------------------------------------------------------

    def generate(

        self,

        config: EnterpriseGenerationConfig,

        devices: list[Device],

    ) -> list[OperationalSnapshot]:
        """
        Generate one operational snapshot
        for every enterprise device.
        """

        self.generated_snapshots.clear()

        for device in devices:

            device.clear_operational_snapshots()

            snapshot = self._create_snapshot(device)

            self.generated_snapshots.append(snapshot)

            device.add_operational_snapshot(
                snapshot.snapshot_id
            )

            device.polling_completed()

            device.update_health(
                snapshot.health_score
            )

            device.update_availability(
                snapshot.availability_percent
            )

            if snapshot.overall_status == "Healthy":
            
                device.operational_status = "UP"

            elif snapshot.overall_status == "Warning":
            
                device.operational_status = "DEGRADED"

            else:
            
                device.operational_status = "DOWN"

            device.touch()


        return self.generated_snapshots
    
    # --------------------------------------------------------
    # Snapshot Creation
    # --------------------------------------------------------

    def _create_snapshot(
        self,
        device: Device,
    ) -> OperationalSnapshot:
        """
        Create a realistic operational snapshot
        for a single device.
        """

        role = device.normalized_role

        metrics = self._role_metrics(role)

        health_score = self._calculate_health_score(
            metrics
        )

        return OperationalSnapshot(

            device_id=device.device_id,

            hostname=device.hostname,

            site_id=device.site_id,

            cpu_utilization=metrics["cpu"],

            memory_utilization=metrics["memory"],

            temperature_celsius=metrics["temperature"],

            uptime_days=metrics["uptime"],

            interfaces_up=metrics["interfaces_up"],

            interfaces_down=metrics["interfaces_down"],

            input_errors=metrics["input_errors"],

            output_errors=metrics["output_errors"],

            crc_errors=metrics["crc_errors"],

            packet_drops=metrics["packet_drops"],

            ospf_neighbors=metrics["ospf_neighbors"],

            bgp_neighbors=metrics["bgp_neighbors"],

            eigrp_neighbors=metrics["eigrp_neighbors"],

            routing_converged=metrics["routing_converged"],

            latency_ms=metrics["latency"],

            jitter_ms=metrics["jitter"],

            packet_loss_percent=metrics["packet_loss"],

            availability_percent=metrics["availability"],

            power_supply_status=metrics["power_status"],

            fan_status=metrics["fan_status"],

            hardware_health=metrics["hardware_health"],

            snmp_status=metrics["snmp"],

            ntp_status=metrics["ntp"],

            syslog_status=metrics["syslog"],

            health_score=health_score,

            overall_status=self._overall_status(
                health_score
            ),

        )

    # --------------------------------------------------------
    # Role Based Metrics
    # --------------------------------------------------------

    def _role_metrics(
        self,
        role: str,
    ) -> dict:

        rng = self._random

        if role == "CORE":

            return {

                "cpu": rng.uniform(40, 70),

                "memory": rng.uniform(50, 75),

                "temperature": rng.uniform(36, 45),

                "uptime": rng.randint(180, 900),

                "interfaces_up": 60,

                "interfaces_down": rng.randint(0, 2),

                "input_errors": rng.randint(0, 8),

                "output_errors": rng.randint(0, 8),

                "crc_errors": rng.randint(0, 2),

                "packet_drops": rng.randint(0, 15),

                "ospf_neighbors": 12,

                "bgp_neighbors": 8,

                "eigrp_neighbors": 0,

                "routing_converged": True,

                "latency": rng.uniform(1, 5),

                "jitter": rng.uniform(0.1, 1.5),

                "packet_loss": round(
                    rng.uniform(0, 0.2),
                    2,
                ),

                "availability": 99.99,

                "power_status": "Healthy",

                "fan_status": "Healthy",

                "hardware_health": "Healthy",

                "snmp": True,

                "ntp": True,

                "syslog": True,

            }

        elif role == "DISTRIBUTION":

            return {

                "cpu": rng.uniform(25, 55),

                "memory": rng.uniform(35, 60),

                "temperature": rng.uniform(34, 42),

                "uptime": rng.randint(120, 700),

                "interfaces_up": 48,

                "interfaces_down": rng.randint(0, 2),

                "input_errors": rng.randint(0, 5),

                "output_errors": rng.randint(0, 5),

                "crc_errors": rng.randint(0, 1),

                "packet_drops": rng.randint(0, 10),

                "ospf_neighbors": 4,

                "bgp_neighbors": 0,

                "eigrp_neighbors": 0,

                "routing_converged": True,

                "latency": rng.uniform(1, 3),

                "jitter": rng.uniform(0.1, 1),

                "packet_loss": round(
                    rng.uniform(0, 0.1),
                    2,
                ),

                "availability": 99.95,

                "power_status": "Healthy",

                "fan_status": "Healthy",

                "hardware_health": "Healthy",

                "snmp": True,

                "ntp": True,

                "syslog": True,

            }
        
        elif role == "ACCESS":

            return {

                "cpu": rng.uniform(10, 35),

                "memory": rng.uniform(20, 45),

                "temperature": rng.uniform(30, 38),

                "uptime": rng.randint(60, 500),

                "interfaces_up": 24,

                "interfaces_down": rng.randint(0, 2),

                "input_errors": rng.randint(0, 3),

                "output_errors": rng.randint(0, 3),

                "crc_errors": rng.randint(0, 1),

                "packet_drops": rng.randint(0, 5),

                "ospf_neighbors": 0,

                "bgp_neighbors": 0,

                "eigrp_neighbors": 0,

                "routing_converged": True,

                "latency": rng.uniform(0.5, 2),

                "jitter": rng.uniform(0.1, 0.8),

                "packet_loss": round(

                    rng.uniform(0, 0.05),

                    2,

                ),

                "availability": 99.90,

                "power_status": "Healthy",

                "fan_status": "Healthy",

                "hardware_health": "Healthy",

                "snmp": True,

                "ntp": True,

                "syslog": True,

            }


        elif role == "FIREWALL":

            return {

                "cpu": rng.uniform(45, 80),

                "memory": rng.uniform(55, 85),

                "temperature": rng.uniform(38, 48),

                "uptime": rng.randint(150, 800),

                "interfaces_up": 12,

                "interfaces_down": rng.randint(0, 1),

                "input_errors": rng.randint(0, 4),

                "output_errors": rng.randint(0, 4),

                "crc_errors": rng.randint(0, 1),

                "packet_drops": rng.randint(0, 12),

                "ospf_neighbors": 2,

                "bgp_neighbors": 2,

                "eigrp_neighbors": 0,

                "routing_converged": True,

                "latency": rng.uniform(2, 8),

                "jitter": rng.uniform(0.5, 3),

                "packet_loss": round(

                    rng.uniform(0, 0.3),

                    2,

                ),

                "availability": 99.95,

                "power_status": "Healthy",

                "fan_status": "Healthy",

                "hardware_health": "Healthy",

                "snmp": True,

                "ntp": True,

                "syslog": True,

            }


        # Default = WAN

        return {

            "cpu": rng.uniform(20, 50),

            "memory": rng.uniform(30, 60),

            "temperature": rng.uniform(34, 42),

            "uptime": rng.randint(90, 600),

            "interfaces_up": 8,

            "interfaces_down": rng.randint(0, 1),

            "input_errors": rng.randint(0, 4),

            "output_errors": rng.randint(0, 4),

            "crc_errors": rng.randint(0, 2),

            "packet_drops": rng.randint(0, 10),

            "ospf_neighbors": 2,

            "bgp_neighbors": 2,

            "eigrp_neighbors": 0,

            "routing_converged": True,

            "latency": rng.uniform(8, 30),

            "jitter": rng.uniform(2, 8),

            "packet_loss": round(

                rng.uniform(0, 1),

                2,

            ),

            "availability": 99.80,

            "power_status": "Healthy",

            "fan_status": "Healthy",

            "hardware_health": "Healthy",

            "snmp": True,

            "ntp": True,

            "syslog": True,

        }


    # --------------------------------------------------------
    # Health Calculation
    # --------------------------------------------------------

    def _calculate_health_score(
        self,
        metrics: dict,
    ) -> float:
        """
        Calculate an overall health score
        based on operational metrics.
        """

        score = 100.0

        if metrics["cpu"] > 80:
            score -= 10

        if metrics["memory"] > 85:
            score -= 10

        if metrics["packet_loss"] > 1:
            score -= 15

        if metrics["crc_errors"] > 5:
            score -= 10

        if metrics["interfaces_down"] > 2:
            score -= 10

        if not metrics["routing_converged"]:
            score -= 20

        if metrics["temperature"] > 50:
            score -= 10

        return max(

            0.0,

            round(score, 2),

        )


    # --------------------------------------------------------

    def _overall_status(
        self,
        health_score: float,
    ) -> str:
        """
        Convert a health score into an
        operational status.
        """

        if health_score >= 90:

            return "Healthy"

        if health_score >= 70:

            return "Warning"

        return "Critical"
    
    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------

    def statistics(
        self,
    ) -> dict:
        """
        Return operational snapshot statistics.
        """

        total = len(
            self.generated_snapshots
        )

        if total == 0:

            return {

                "total_snapshots": 0,

                "healthy": 0,

                "warning": 0,

                "critical": 0,

                "average_cpu": 0.0,

                "average_memory": 0.0,

                "average_latency": 0.0,

                "average_health": 0.0,

            }

        return {

            "total_snapshots": total,

            "healthy": sum(

                1

                for snapshot

                in self.generated_snapshots

                if snapshot.overall_status == "Healthy"

            ),

            "warning": sum(

                1

                for snapshot

                in self.generated_snapshots

                if snapshot.overall_status == "Warning"

            ),

            "critical": sum(

                1

                for snapshot

                in self.generated_snapshots

                if snapshot.overall_status == "Critical"

            ),

            "average_cpu": round(

                sum(

                    snapshot.cpu_utilization

                    for snapshot

                    in self.generated_snapshots

                ) / total,

                2,

            ),

            "average_memory": round(

                sum(

                    snapshot.memory_utilization

                    for snapshot

                    in self.generated_snapshots

                ) / total,

                2,

            ),

            "average_latency": round(

                sum(

                    snapshot.latency_ms

                    for snapshot

                    in self.generated_snapshots

                ) / total,

                2,

            ),

            "average_health": round(

                sum(
                
                    snapshot.health_score

                    for snapshot

                    in self.generated_snapshots
            
                ) / total,
            
                2,
            
            ),

        }


    # --------------------------------------------------------
    # Lookup Helpers
    # --------------------------------------------------------

    def get_snapshot(

        self,

        snapshot_id,

    ) -> OperationalSnapshot | None:

        for snapshot in self.generated_snapshots:

            if snapshot.snapshot_id == snapshot_id:

                return snapshot

        return None


    # --------------------------------------------------------

    def healthy_snapshots(
        self,
    ) -> list[OperationalSnapshot]:

        return [

            snapshot

            for snapshot

            in self.generated_snapshots

            if snapshot.overall_status == "Healthy"

        ]


    # --------------------------------------------------------

    def warning_snapshots(
        self,
    ) -> list[OperationalSnapshot]:

        return [

            snapshot

            for snapshot

            in self.generated_snapshots

            if snapshot.overall_status == "Warning"

        ]


    # --------------------------------------------------------

    def critical_snapshots(
        self,
    ) -> list[OperationalSnapshot]:

        return [

            snapshot

            for snapshot

            in self.generated_snapshots

            if snapshot.overall_status == "Critical"

        ]


    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    def validate_relationships(
        self,
    ) -> bool:
        """
        Ensure every snapshot belongs
        to a device.
        """

        for snapshot in self.generated_snapshots:

            if snapshot.device_id is None:

                return False

            if snapshot.hostname == "":

                return False

            if snapshot.site_id is None:

                return False
            
            if not (0 <= snapshot.health_score <= 100):

                return False

            if snapshot.overall_status == "":
            
                return False

        return True


    # --------------------------------------------------------
    # Reset
    # --------------------------------------------------------

    def reset(
        self,
    ) -> None:

        self.generated_snapshots.clear()


    # --------------------------------------------------------
    # Utility Methods
    # --------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return len(
            self.generated_snapshots
        )


    # --------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        stats = self.statistics()

        return (

            "OperationalSnapshotGenerator("

            f"snapshots={stats['total_snapshots']}, "

            f"healthy={stats['healthy']}, "

            f"warning={stats['warning']}, "

            f"critical={stats['critical']}, "

            f"avg_cpu={stats['average_cpu']:.2f}, "

            f"avg_memory={stats['average_memory']:.2f}, "

            f"avg_health={stats['average_health']:.2f})"

        )