"""
=============================================================

ConfigVista AI

Device Generator Tests

=============================================================
"""

from enterprise.generators.device_generator import (
    DeviceGenerator,
)

from enterprise.generators.site_generator import (
    SiteGenerator,
)

from enterprise.generators.enterprise_generator import (
    EnterpriseGenerationConfig,
)

from enterprise.models import (
    Device,
)


# ==========================================================
# Helpers
# ==========================================================

def build_sites():

    config = EnterpriseGenerationConfig()

    return SiteGenerator().generate(config)


def build_generator():

    return DeviceGenerator()


# ==========================================================
# Constructor
# ==========================================================

def test_constructor():

    generator = build_generator()

    assert generator.generated_devices == []


# ==========================================================
# Generation
# ==========================================================

def test_generate():

    generator = build_generator()

    devices = generator.generate(

        EnterpriseGenerationConfig(),

        build_sites(),

        [],

    )

    assert len(devices) == 300

    assert len(generator) == 300


def test_return_type():

    generator = build_generator()

    devices = generator.generate(

        EnterpriseGenerationConfig(),

        build_sites(),

        [],

    )

    assert isinstance(

        devices,

        list,

    )

    assert all(

        isinstance(device, Device)

        for device in devices

    )


# ==========================================================
# Core Devices
# ==========================================================

def test_core_device_count():

    generator = build_generator()

    generator.generate(

        EnterpriseGenerationConfig(),

        build_sites(),

        [],

    )

    core = [

        device

        for device

        in generator.generated_devices

        if device.role == "CORE"

    ]

    assert len(core) == 40


def test_core_hostname():

    generator = build_generator()

    generator.generate(

        EnterpriseGenerationConfig(),

        build_sites(),

        [],

    )

    core = [

        device

        for device

        in generator.generated_devices

        if device.role == "CORE"

    ]

    assert core[0].hostname == "CORE-001"

    assert core[-1].hostname == "CORE-040"


def test_core_platform():

    generator = build_generator()

    generator.generate(

        EnterpriseGenerationConfig(),

        build_sites(),

        [],

    )

    core = [

        device

        for device

        in generator.generated_devices

        if device.role == "CORE"

    ]

    assert all(

        device.platform == "Cisco Catalyst 9500"

        for device

        in core

    )


def test_core_vendor():

    generator = build_generator()

    generator.generate(

        EnterpriseGenerationConfig(),

        build_sites(),

        [],

    )

    core = [

        device

        for device

        in generator.generated_devices

        if device.role == "CORE"

    ]

    assert all(

        device.vendor == "Cisco"

        for device

        in core

    )


def test_core_os():

    generator = build_generator()

    generator.generate(

        EnterpriseGenerationConfig(),

        build_sites(),

        [],

    )

    core = [

        device

        for device

        in generator.generated_devices

        if device.role == "CORE"

    ]

    assert all(

        device.os_name == "IOS-XE"

        for device

        in core

    )

# ==========================================================
# Distribution Devices
# ==========================================================

def test_distribution_device_count():

    generator = build_generator()

    generator.generate(

        EnterpriseGenerationConfig(),

        build_sites(),

        [],

    )

    distribution = [

        device

        for device

        in generator.generated_devices

        if device.role == "DIST"

    ]

    assert len(distribution) == 80


def test_distribution_platform():

    generator = build_generator()

    generator.generate(

        EnterpriseGenerationConfig(),

        build_sites(),

        [],

    )

    distribution = [

        device

        for device

        in generator.generated_devices

        if device.role == "DIST"

    ]

    assert all(

        device.platform == "Cisco Catalyst 9300"

        for device

        in distribution

    )


# ==========================================================
# Access Devices
# ==========================================================

def test_access_device_count():

    generator = build_generator()

    generator.generate(

        EnterpriseGenerationConfig(),

        build_sites(),

        [],

    )

    access = [

        device

        for device

        in generator.generated_devices

        if device.role == "ACCESS"

    ]

    assert len(access) == 140


def test_access_platform():

    generator = build_generator()

    generator.generate(

        EnterpriseGenerationConfig(),

        build_sites(),

        [],

    )

    access = [

        device

        for device

        in generator.generated_devices

        if device.role == "ACCESS"

    ]

    assert all(

        device.platform == "Cisco Catalyst 9200"

        for device

        in access

    )


# ==========================================================
# Firewalls
# ==========================================================

def test_firewall_count():

    generator = build_generator()

    generator.generate(

        EnterpriseGenerationConfig(),

        build_sites(),

        [],

    )

    firewalls = [

        device

        for device

        in generator.generated_devices

        if device.role == "FW"

    ]

    assert len(firewalls) == 20


def test_firewall_platform():

    generator = build_generator()

    generator.generate(

        EnterpriseGenerationConfig(),

        build_sites(),

        [],

    )

    firewalls = [

        device

        for device

        in generator.generated_devices

        if device.role == "FW"

    ]

    assert all(

        device.platform == "Cisco Firepower 2130"

        for device

        in firewalls

    )

    assert all(

        device.os_name == "FTD"

        for device

        in firewalls

    )


# ==========================================================
# WAN Devices
# ==========================================================

def test_wan_device_count():

    generator = build_generator()

    generator.generate(

        EnterpriseGenerationConfig(),

        build_sites(),

        [],

    )

    wan = [

        device

        for device

        in generator.generated_devices

        if device.role == "WAN"

    ]

    assert len(wan) == 20


def test_wan_platform():

    generator = build_generator()

    generator.generate(

        EnterpriseGenerationConfig(),

        build_sites(),

        [],

    )

    wan = [

        device

        for device

        in generator.generated_devices

        if device.role == "WAN"

    ]

    assert all(

        device.platform == "Cisco Catalyst 8300"

        for device

        in wan

    )


# ==========================================================
# Site Assignment
# ==========================================================

def test_all_devices_have_site():

    generator = build_generator()

    generator.generate(

        EnterpriseGenerationConfig(),

        build_sites(),

        [],

    )

    assert all(

        device.site_id != ""

        for device

        in generator.generated_devices

    )


# ==========================================================
# Management IP
# ==========================================================

def test_management_ip_unique():

    generator = build_generator()

    generator.generate(

        EnterpriseGenerationConfig(),

        build_sites(),

        [],

    )

    ips = [

        device.management_ip

        for device

        in generator.generated_devices

    ]

    assert len(ips) == len(set(ips))

    assert all(

        ip != ""

        for ip

        in ips

    )
# ==========================================================
# Statistics
# ==========================================================

def test_statistics():

    generator = build_generator()

    generator.generate(

        EnterpriseGenerationConfig(),

        build_sites(),

        [],

    )

    stats = generator.statistics()

    assert stats["total_devices"] == 300

    assert stats["core"] == 40

    assert stats["distribution"] == 80

    assert stats["access"] == 140

    assert stats["firewalls"] == 20

    assert stats["wan"] == 20


def test_statistics_consistency():

    generator = build_generator()

    generator.generate(

        EnterpriseGenerationConfig(),

        build_sites(),

        [],

    )

    stats = generator.statistics()

    assert (

        stats["core"]

        + stats["distribution"]

        + stats["access"]

        + stats["firewalls"]

        + stats["wan"]

        == stats["total_devices"]

    )


# ==========================================================
# Reset
# ==========================================================

def test_reset():

    generator = build_generator()

    generator.generate(

        EnterpriseGenerationConfig(),

        build_sites(),

        [],

    )

    assert len(generator) == 300

    generator.reset()

    assert len(generator) == 0

    assert generator.generated_devices == []


# ==========================================================
# Utility Methods
# ==========================================================

def test_len():

    generator = build_generator()

    generator.generate(

        EnterpriseGenerationConfig(),

        build_sites(),

        [],

    )

    assert len(generator) == 300


def test_repr():

    generator = build_generator()

    generator.generate(

        EnterpriseGenerationConfig(),

        build_sites(),

        [],

    )

    representation = repr(generator)

    assert "DeviceGenerator" in representation

    assert "devices=300" in representation

    assert "core=40" in representation

    assert "dist=80" in representation

    assert "access=140" in representation

    assert "fw=20" in representation

    assert "wan=20" in representation


# ==========================================================
# Deterministic Generation
# ==========================================================

def test_generation_is_deterministic():

    generator = build_generator()

    first = generator.generate(

        EnterpriseGenerationConfig(),

        build_sites(),

        [],

    )

    names1 = [

        device.hostname

        for device in first

    ]

    second = generator.generate(

        EnterpriseGenerationConfig(),

        build_sites(),

        [],

    )

    names2 = [

        device.hostname

        for device in second

    ]

    assert names1 == names2


# ==========================================================
# Integrity
# ==========================================================

def test_hostnames_unique():

    generator = build_generator()

    generator.generate(

        EnterpriseGenerationConfig(),

        build_sites(),

        [],

    )

    hostnames = [

        device.hostname

        for device

        in generator.generated_devices

    ]

    assert len(hostnames) == len(set(hostnames))


def test_all_required_fields_populated():

    generator = build_generator()

    generator.generate(

        EnterpriseGenerationConfig(),

        build_sites(),

        [],

    )

    for device in generator.generated_devices:

        assert device.hostname != ""

        assert device.vendor != ""

        assert device.platform != ""

        assert device.os_name != ""

        assert device.role != ""

        assert device.management_ip != ""

        assert device.site_id != ""


# ==========================================================
# Custom Configuration
# ==========================================================

def test_custom_configuration():

    generator = build_generator()

    config = EnterpriseGenerationConfig(

        core_devices=2,

        distribution_devices=3,

        access_devices=4,

        firewall_devices=1,

        wan_edge_devices=1,

    )

    devices = generator.generate(

        config,

        build_sites(),

        [],

    )

    assert len(devices) == 11

    stats = generator.statistics()

    assert stats["total_devices"] == 11

    assert stats["core"] == 2

    assert stats["distribution"] == 3

    assert stats["access"] == 4

    assert stats["firewalls"] == 1

    assert stats["wan"] == 1