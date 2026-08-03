"""
=============================================================

ConfigVista AI

Topology Generator Tests

=============================================================
"""

from enterprise.generators.topology_generator import (
    TopologyGenerator,
)

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
    TopologyLink,
)


# ==========================================================
# Helpers
# ==========================================================

def build_sites():

    config = EnterpriseGenerationConfig()

    return SiteGenerator().generate(config)


def build_devices():

    config = EnterpriseGenerationConfig()

    sites = build_sites()

    return DeviceGenerator().generate(

        config,

        sites,

        [],

    )


def build_generator():

    return TopologyGenerator()


# ==========================================================
# Constructor
# ==========================================================

def test_constructor():

    generator = build_generator()

    assert generator.generated_links == []


# ==========================================================
# Generation
# ==========================================================

def test_generate():

    generator = build_generator()

    links = generator.generate(

        EnterpriseGenerationConfig(),

        build_devices(),

    )

    assert isinstance(

        links,

        list,

    )

    assert len(links) > 0

    assert len(generator) == len(links)


def test_return_type():

    generator = build_generator()

    links = generator.generate(

        EnterpriseGenerationConfig(),

        build_devices(),

    )

    assert all(

        isinstance(link, TopologyLink)

        for link in links

    )


# ==========================================================
# Core Links
# ==========================================================

def test_core_links_exist():

    generator = build_generator()

    links = generator.generate(

        EnterpriseGenerationConfig(),

        build_devices(),

    )

    core_links = [

        link

        for link

        in links

        if link.bandwidth == "100G"

    ]

    assert len(core_links) > 0


def test_core_links_are_up():

    generator = build_generator()

    links = generator.generate(

        EnterpriseGenerationConfig(),

        build_devices(),

    )

    core_links = [

        link

        for link

        in links

        if link.bandwidth == "100G"

    ]

    assert all(

        link.operational_status == "UP"

        for link

        in core_links

    )

    assert all(

        link.admin_status == "UP"

        for link

        in core_links

    )


# ==========================================================
# Distribution Links
# ==========================================================

def test_distribution_links_exist():

    generator = build_generator()

    links = generator.generate(

        EnterpriseGenerationConfig(),

        build_devices(),

    )

    distribution = [

        link

        for link

        in links

        if link.bandwidth == "40G"

    ]

    assert len(distribution) == 80

