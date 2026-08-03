from __future__ import annotations

from enterprise.generators.enterprise_generator import (
    EnterpriseGenerationConfig,
)

from enterprise.generators.site_generator import (
    SiteGenerator,
)

from enterprise.generators.device_generator import (
    DeviceGenerator,
)

from enterprise.generators.operational_snapshot_generator import (
    OperationalSnapshotGenerator,
)

from enterprise.models import (
    OperationalSnapshot,
)


# ============================================================
# Helpers
# ============================================================

def build_environment():

    config = EnterpriseGenerationConfig()

    sites = SiteGenerator().generate(
        config
    )

    devices = DeviceGenerator().generate(
        config,
        sites,
        [],
    )

    return (

        config,

        devices,

    )


def build_generator():

    return OperationalSnapshotGenerator()


# ============================================================
# Constructor
# ============================================================

def test_constructor():

    generator = build_generator()

    assert generator.generated_snapshots == []

    assert len(generator) == 0


# ============================================================
# Generation
# ============================================================

def test_generate():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    snapshots = generator.generate(

        config,

        devices,

    )

    assert len(snapshots) > 0


def test_return_type():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    snapshots = generator.generate(

        config,

        devices,

    )

    assert isinstance(

        snapshots,

        list,

    )

    assert all(

        isinstance(

            snapshot,

            OperationalSnapshot,

        )

        for snapshot

        in snapshots

    )


def test_total_snapshots():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    snapshots = generator.generate(

        config,

        devices,

    )

    assert len(snapshots) == len(devices)

# ============================================================
# Identity
# ============================================================

def test_snapshot_ids_unique():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    snapshots = generator.generate(

        config,

        devices,

    )

    ids = {

        snapshot.snapshot_id

        for snapshot

        in snapshots

    }

    assert len(ids) == len(snapshots)


def test_device_ids_present():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    snapshots = generator.generate(

        config,

        devices,

    )

    assert all(

        snapshot.device_id is not None

        for snapshot

        in snapshots

    )


def test_hostnames_present():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    snapshots = generator.generate(

        config,

        devices,

    )

    assert all(

        snapshot.hostname != ""

        for snapshot

        in snapshots

    )


def test_site_ids_present():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    snapshots = generator.generate(

        config,

        devices,

    )

    assert all(

        snapshot.site_id is not None

        for snapshot

        in snapshots

    )


# ============================================================
# Device Health
# ============================================================

def test_cpu_range():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    snapshots = generator.generate(

        config,

        devices,

    )

    assert all(

        0 <= snapshot.cpu_utilization <= 100

        for snapshot

        in snapshots

    )


def test_memory_range():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    snapshots = generator.generate(

        config,

        devices,

    )

    assert all(

        0 <= snapshot.memory_utilization <= 100

        for snapshot

        in snapshots

    )


def test_temperature_positive():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    snapshots = generator.generate(

        config,

        devices,

    )

    assert all(

        snapshot.temperature_celsius >= 0

        for snapshot

        in snapshots

    )


def test_uptime_positive():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    snapshots = generator.generate(

        config,

        devices,

    )

    assert all(

        snapshot.uptime_days >= 0

        for snapshot

        in snapshots

    )

# ============================================================
# Interface Health
# ============================================================

def test_interfaces_up_positive():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    snapshots = generator.generate(

        config,

        devices,

    )

    assert all(

        snapshot.interfaces_up >= 0

        for snapshot

        in snapshots

    )


def test_interfaces_down_positive():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    snapshots = generator.generate(

        config,

        devices,

    )

    assert all(

        snapshot.interfaces_down >= 0

        for snapshot

        in snapshots

    )


def test_error_counters_positive():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    snapshots = generator.generate(

        config,

        devices,

    )

    assert all(

        snapshot.input_errors >= 0

        and snapshot.output_errors >= 0

        and snapshot.crc_errors >= 0

        and snapshot.packet_drops >= 0

        for snapshot

        in snapshots

    )


# ============================================================
# Routing Health
# ============================================================

def test_routing_neighbors_positive():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    snapshots = generator.generate(

        config,

        devices,

    )

    assert all(

        snapshot.ospf_neighbors >= 0

        and snapshot.bgp_neighbors >= 0

        and snapshot.eigrp_neighbors >= 0

        for snapshot

        in snapshots

    )


def test_routing_convergence_boolean():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    snapshots = generator.generate(

        config,

        devices,

    )

    assert all(

        isinstance(

            snapshot.routing_converged,

            bool,

        )

        for snapshot

        in snapshots

    )


# ============================================================
# Network Health
# ============================================================

def test_latency_positive():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    snapshots = generator.generate(

        config,

        devices,

    )

    assert all(

        snapshot.latency_ms >= 0

        for snapshot

        in snapshots

    )


def test_jitter_positive():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    snapshots = generator.generate(

        config,

        devices,

    )

    assert all(

        snapshot.jitter_ms >= 0

        for snapshot

        in snapshots

    )


def test_packet_loss_range():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    snapshots = generator.generate(

        config,

        devices,

    )

    assert all(

        0 <= snapshot.packet_loss_percent <= 100

        for snapshot

        in snapshots

    )


def test_availability_range():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    snapshots = generator.generate(

        config,

        devices,

    )

    assert all(

        0 <= snapshot.availability_percent <= 100

        for snapshot

        in snapshots

    )


# ============================================================
# Hardware & Monitoring
# ============================================================

def test_hardware_status_present():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    snapshots = generator.generate(

        config,

        devices,

    )

    assert all(

        snapshot.power_supply_status != ""

        and snapshot.fan_status != ""

        and snapshot.hardware_health != ""

        for snapshot

        in snapshots

    )


def test_monitoring_status_boolean():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    snapshots = generator.generate(

        config,

        devices,

    )

    assert all(

        isinstance(

            snapshot.snmp_status,

            bool,

        )

        and isinstance(

            snapshot.ntp_status,

            bool,

        )

        and isinstance(

            snapshot.syslog_status,

            bool,

        )

        for snapshot

        in snapshots

    )
# ============================================================
# Overall Health
# ============================================================

def test_health_score_range():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    snapshots = generator.generate(

        config,

        devices,

    )

    assert all(

        0 <= snapshot.health_score <= 100

        for snapshot

        in snapshots

    )


def test_overall_status_present():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    snapshots = generator.generate(

        config,

        devices,

    )

    valid = {

        "Healthy",

        "Warning",

        "Critical",

    }

    assert all(

        snapshot.overall_status

        in valid

        for snapshot

        in snapshots

    )


# ============================================================
# Lookup Helpers
# ============================================================

def test_get_snapshot():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    snapshots = generator.generate(

        config,

        devices,

    )

    snapshot = generator.get_snapshot(

        snapshots[0].snapshot_id

    )

    assert snapshot is not None

    assert (

        snapshot.snapshot_id

        ==

        snapshots[0].snapshot_id

    )


def test_unknown_snapshot():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    generator.generate(

        config,

        devices,

    )

    assert (

        generator.get_snapshot(

            "UNKNOWN"

        )

        is None

    )


# ============================================================
# Status Helpers
# ============================================================

def test_healthy_snapshots():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    snapshots = generator.generate(

        config,

        devices,

    )

    healthy = generator.healthy_snapshots()

    assert len(healthy) <= len(snapshots)

    assert all(

        snapshot.overall_status

        ==

        "Healthy"

        for snapshot

        in healthy

    )


def test_warning_snapshots():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    snapshots = generator.generate(

        config,

        devices,

    )

    warning = generator.warning_snapshots()

    assert len(warning) <= len(snapshots)

    assert all(

        snapshot.overall_status

        ==

        "Warning"

        for snapshot

        in warning

    )


def test_critical_snapshots():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    snapshots = generator.generate(

        config,

        devices,

    )

    critical = generator.critical_snapshots()

    assert len(critical) <= len(snapshots)

    assert all(

        snapshot.overall_status

        ==

        "Critical"

        for snapshot

        in critical

    )


# ============================================================
# Statistics
# ============================================================

def test_statistics():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    generator.generate(

        config,

        devices,

    )

    stats = generator.statistics()

    assert stats["total_snapshots"] == len(devices)

    assert "average_cpu" in stats

    assert "average_memory" in stats

    assert "average_latency" in stats

    assert "average_health" in stats


def test_statistics_consistency():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    generator.generate(

        config,

        devices,

    )

    stats = generator.statistics()

    assert (

        stats["healthy"]

        +

        stats["warning"]

        +

        stats["critical"]

        ==

        stats["total_snapshots"]

    )


# ============================================================
# Validation
# ============================================================

def test_validate_relationships():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    generator.generate(

        config,

        devices,

    )

    assert (

        generator.validate_relationships()

        is True

    )
# ============================================================
# Utility Methods
# ============================================================

def test_reset():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    generator.generate(

        config,

        devices,

    )

    generator.reset()

    assert len(generator.generated_snapshots) == 0


def test_len():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    generator.generate(

        config,

        devices,

    )

    assert len(generator) == len(devices)


def test_repr():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    generator.generate(

        config,

        devices,

    )

    representation = repr(generator)

    assert "OperationalSnapshotGenerator" in representation

    assert "snapshots=" in representation

    assert "healthy=" in representation


# ============================================================
# Deterministic Generation
# ============================================================

def test_generation_is_deterministic():

    (

        config,

        devices,

    ) = build_environment()

    generator1 = build_generator()

    generator2 = build_generator()

    snapshots1 = generator1.generate(

        config,

        devices,

    )

    snapshots2 = generator2.generate(

        config,

        devices,

    )

    assert len(snapshots1) == len(snapshots2)

    assert (

        snapshots1[0].hostname

        ==

        snapshots2[0].hostname

    )

    assert (

        snapshots1[0].device_id

        ==

        snapshots2[0].device_id

    )


# ============================================================
# Required Fields
# ============================================================

def test_required_fields_populated():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    snapshots = generator.generate(

        config,

        devices,

    )

    assert all(

        snapshot.snapshot_id is not None

        and snapshot.device_id is not None

        and snapshot.hostname != ""

        and snapshot.site_id is not None

        for snapshot

        in snapshots

    )


# ============================================================
# Device Relationships
# ============================================================

def test_device_relationships():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    snapshots = generator.generate(

        config,

        devices,

    )

    snapshot_lookup = {

        snapshot.snapshot_id

        for snapshot

        in snapshots

    }

    for device in devices:

        assert len(

            device.operational_snapshot_ids

        ) == 1

        snapshot_id = device.operational_snapshot_ids[0]

        assert snapshot_id in snapshot_lookup


def test_last_operational_snapshot_updated():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    generator.generate(

        config,

        devices,

    )

    assert all(

        device.last_operational_snapshot

        is not None

        for device

        in devices

    )


def test_last_successful_poll_updated():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    generator.generate(

        config,

        devices,

    )

    assert all(

        device.last_successful_poll

        is not None

        for device

        in devices

    )


def test_device_health_synchronized():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    snapshots = generator.generate(

        config,

        devices,

    )

    lookup = {

        snapshot.device_id: snapshot

        for snapshot

        in snapshots

    }

    for device in devices:

        assert (

            device.current_health_score

            ==

            lookup[device.device_id].health_score

        )


def test_device_availability_synchronized():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    snapshots = generator.generate(

        config,

        devices,

    )

    lookup = {

        snapshot.device_id: snapshot

        for snapshot

        in snapshots

    }

    for device in devices:

        assert (

            device.availability_percent

            ==

            lookup[device.device_id].availability_percent

        )


def test_device_operational_status():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    generator.generate(

        config,

        devices,

    )

    valid = {

        "UP",

        "DEGRADED",

        "DOWN",

    }

    assert all(

        device.operational_status

        in valid

        for device

        in devices

    )