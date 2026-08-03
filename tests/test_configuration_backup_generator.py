"""
=============================================================

ConfigVista AI

Configuration Backup Generator Tests

=============================================================
"""

from enterprise.generators.enterprise_generator import (
    EnterpriseGenerationConfig,
)

from enterprise.generators.site_generator import (
    SiteGenerator,
)

from enterprise.generators.device_generator import (
    DeviceGenerator,
)

from enterprise.generators.configuration_backup_generator import (
    ConfigurationBackupGenerator,
)

from enterprise.models import (
    ConfigurationBackup,
)


# ==========================================================
# Helpers
# ==========================================================

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

    return ConfigurationBackupGenerator()


# ==========================================================
# Constructor
# ==========================================================

def test_constructor():

    generator = build_generator()

    assert generator.generated_backups == []


# ==========================================================
# Generation
# ==========================================================

def test_generate():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    backups = generator.generate(

        config,

        devices,

    )

    assert len(backups) > 0

    assert len(generator) == len(backups)


def test_return_type():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    backups = generator.generate(

        config,

        devices,

    )

    assert isinstance(

        backups,

        list,

    )

    assert all(

        isinstance(

            backup,

            ConfigurationBackup,

        )

        for backup

        in backups

    )


# ==========================================================
# Counts
# ==========================================================

def test_total_backups():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    backups = generator.generate(

        config,

        devices,

    )

    assert len(backups) == (

        len(devices) * 2

    )


def test_running_count():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    generator.generate(

        config,

        devices,

    )

    assert len(

        generator.running_backups()

    ) == len(devices)


def test_startup_count():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    generator.generate(

        config,

        devices,

    )

    assert len(

        generator.startup_backups()

    ) == len(devices)


# ==========================================================
# Identity
# ==========================================================

def test_backup_ids_unique():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    backups = generator.generate(

        config,

        devices,

    )

    ids = [

        backup.backup_id

        for backup

        in backups

    ]

    assert len(ids) == len(

        set(ids)

    )


def test_hostnames_populated():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    backups = generator.generate(

        config,

        devices,

    )

    assert all(

        backup.hostname != ""

        for backup

        in backups

    )

# ==========================================================
# Backup Metadata
# ==========================================================

def test_device_ids_present():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    backups = generator.generate(

        config,

        devices,

    )

    assert all(

        backup.device_id is not None

        for backup

        in backups

    )


def test_device_roles_present():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    backups = generator.generate(

        config,

        devices,

    )

    valid = {

        "CORE",

        "DISTRIBUTION",

        "ACCESS",

        "FIREWALL",

        "WAN",

    }

    assert all(

        backup.device_role in valid

        for backup

        in backups

    )


def test_backup_type():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    backups = generator.generate(

        config,

        devices,

    )

    valid = {

        "Running",

        "Startup",

    }

    assert all(

        backup.backup_type in valid

        for backup

        in backups

    )


def test_configuration_version():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    backups = generator.generate(

        config,

        devices,

    )

    assert all(

        backup.configuration_version == "v1"

        for backup

        in backups

    )


def test_configuration_text():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    backups = generator.generate(

        config,

        devices,

    )

    assert all(

        len(

            backup.configuration_text

        ) > 0

        for backup

        in backups

    )


def test_configuration_hash():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    backups = generator.generate(

        config,

        devices,

    )

    assert all(

        backup.configuration_hash != ""

        for backup

        in backups

    )


def test_checksum():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    backups = generator.generate(

        config,

        devices,

    )

    assert all(

        backup.checksum != ""

        for backup

        in backups

    )


def test_line_count():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    backups = generator.generate(

        config,

        devices,

    )

    assert all(

        backup.line_count > 0

        for backup

        in backups

    )


def test_feature_summary():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    backups = generator.generate(

        config,

        devices,

    )

    assert all(

        isinstance(

            backup.feature_summary,

            dict,

        )

        for backup

        in backups

    )

    assert all(

        len(

            backup.feature_summary

        ) > 0

        for backup

        in backups

    )

# ==========================================================
# Lookup Helpers
# ==========================================================

def test_running_backups():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    generator.generate(

        config,

        devices,

    )

    running = generator.running_backups()

    assert all(

        backup.backup_type == "Running"

        for backup

        in running

    )


def test_startup_backups():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    generator.generate(

        config,

        devices,

    )

    startup = generator.startup_backups()

    assert all(

        backup.backup_type == "Startup"

        for backup

        in startup

    )


def test_get_backup():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    backups = generator.generate(

        config,

        devices,

    )

    first = backups[0]

    found = generator.get_backup(

        first.backup_id

    )

    assert found is not None

    assert (

        found.backup_id

        == first.backup_id

    )


def test_unknown_backup():

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

        generator.get_backup(

            "CFG-999999"

        )

        is None

    )


# ==========================================================
# Statistics
# ==========================================================

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

    assert (

        stats["total_backups"]

        == len(generator)

    )


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

        stats["running"]

        +

        stats["startup"]

        ==

        stats["total_backups"]

    )

    assert (

        stats["core"]

        +

        stats["distribution"]

        +

        stats["access"]

        +

        stats["firewall"]

        +

        stats["wan"]

        ==

        stats["total_backups"]

    )


# ==========================================================
# Validation
# ==========================================================

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


# ==========================================================
# Reset
# ==========================================================

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

    assert len(generator) == 0

    assert generator.generated_backups == []


# ==========================================================
# Utility Methods
# ==========================================================

def test_len():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    backups = generator.generate(

        config,

        devices,

    )

    assert len(generator) == len(backups)


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

    assert "ConfigurationBackupGenerator" in representation

    assert "backups=" in representation

    assert "running=" in representation

    assert "startup=" in representation

# ==========================================================
# Deterministic Generation
# ==========================================================

def test_generation_is_deterministic():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    first = generator.generate(

        config,

        devices,

    )

    first_hashes = [

        backup.configuration_hash

        for backup

        in first

    ]

    generator.reset()

    second = generator.generate(

        config,

        devices,

    )

    second_hashes = [

        backup.configuration_hash

        for backup

        in second

    ]

    assert first_hashes == second_hashes

# ==========================================================
# Integrity
# ==========================================================

def test_required_fields_populated():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    backups = generator.generate(

        config,

        devices,

    )

    assert all(

        backup.hostname != ""

        for backup

        in backups

    )

    assert all(

        backup.configuration_text != ""

        for backup

        in backups

    )

    assert all(

        backup.configuration_hash != ""

        for backup

        in backups

    )

    assert all(

        backup.checksum != ""

        for backup

        in backups

    )


def test_hash_length():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    backups = generator.generate(

        config,

        devices,

    )

    assert all(

        len(

            backup.configuration_hash

        ) == 64

        for backup

        in backups

    )


def test_checksum_length():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    backups = generator.generate(

        config,

        devices,

    )

    assert all(

        len(

            backup.checksum

        ) == 32

        for backup

        in backups

    )


def test_configuration_size():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    backups = generator.generate(

        config,

        devices,

    )

    assert all(

        backup.configuration_size > 0

        for backup

        in backups

    )


def test_feature_summary_content():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    backups = generator.generate(

        config,

        devices,

    )

    required = {

        "interfaces",

        "ospf",

        "bgp",

        "acl",

        "nat",

        "qos",

        "vlans",

    }

    for backup in backups:

        assert required.issubset(

            backup.feature_summary.keys()

        )


def test_running_startup_distribution():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    backups = generator.generate(

        config,

        devices,

    )

    running = sum(

        1

        for backup

        in backups

        if backup.backup_type == "Running"

    )

    startup = sum(

        1

        for backup

        in backups

        if backup.backup_type == "Startup"

    )

    assert running == startup

    assert running == len(devices)


def test_device_relationships():

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

        device.backup_count == 2

        for device

        in devices

    )


def test_configuration_contains_hostname():

    (

        config,

        devices,

    ) = build_environment()

    generator = build_generator()

    backups = generator.generate(

        config,

        devices,

    )

    for backup in backups:

        assert (

            f"hostname {backup.hostname}"

            in backup.configuration_text

        )