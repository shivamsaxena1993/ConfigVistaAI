"""
=============================================================

ConfigVista AI

Site Generator Tests

=============================================================
"""

from enterprise.generators.site_generator import (
    SiteGenerator,
)

from enterprise.generators.enterprise_generator import (
    EnterpriseGenerationConfig,
)

from enterprise.models import (
    Site,
)


# ==========================================================
# Helper
# ==========================================================

def build_generator():

    return SiteGenerator()


# ==========================================================
# Constructor
# ==========================================================

def test_constructor():

    generator = build_generator()

    assert generator.generated_sites == []


# ==========================================================
# Generation
# ==========================================================

def test_generate():

    generator = build_generator()

    sites = generator.generate(
        EnterpriseGenerationConfig()
    )

    assert len(sites) == 40

    assert len(generator) == 40


def test_return_type():

    generator = build_generator()

    sites = generator.generate(
        EnterpriseGenerationConfig()
    )

    assert isinstance(
        sites,
        list,
    )

    assert all(
        isinstance(site, Site)
        for site in sites
    )


# ==========================================================
# Data Centers
# ==========================================================

def test_data_center_count():

    generator = build_generator()

    generator.generate(
        EnterpriseGenerationConfig()
    )

    data_centers = [

        site

        for site

        in generator.generated_sites

        if site.site_type == "Data Center"

    ]

    assert len(data_centers) == 2


def test_data_center_names():

    generator = build_generator()

    generator.generate(
        EnterpriseGenerationConfig()
    )

    names = {

        site.site_name

        for site

        in generator.generated_sites

        if site.site_type == "Data Center"

    }

    assert "DC-NORTH" in names

    assert "DC-SOUTH" in names


# ==========================================================
# Regional Offices
# ==========================================================

def test_regional_count():

    generator = build_generator()

    generator.generate(
        EnterpriseGenerationConfig()
    )

    regional = [

        site

        for site

        in generator.generated_sites

        if site.site_type == "Regional Office"

    ]

    assert len(regional) == 8


def test_regional_names():

    generator = build_generator()

    generator.generate(
        EnterpriseGenerationConfig()
    )

    names = {

        site.site_name

        for site

        in generator.generated_sites

        if site.site_type == "Regional Office"

    }

    assert "REG-BENGALURU" in names

    assert "REG-MUMBAI" in names

    assert "REG-DELHI" in names

# ==========================================================
# Branch Offices
# ==========================================================

def test_branch_count():

    generator = build_generator()

    generator.generate(
        EnterpriseGenerationConfig()
    )

    branches = [

        site

        for site

        in generator.generated_sites

        if site.site_type == "Branch"

    ]

    assert len(branches) == 30


def test_branch_names():

    generator = build_generator()

    generator.generate(
        EnterpriseGenerationConfig()
    )

    names = {

        site.site_name

        for site

        in generator.generated_sites

        if site.site_type == "Branch"

    }

    assert "BRANCH-001" in names

    assert "BRANCH-030" in names


# ==========================================================
# Site Codes
# ==========================================================

def test_site_codes_unique():

    generator = build_generator()

    generator.generate(
        EnterpriseGenerationConfig()
    )

    codes = [

        site.site_code

        for site

        in generator.generated_sites

    ]

    assert len(codes) == len(set(codes))


def test_site_code_formats():

    generator = build_generator()

    generator.generate(
        EnterpriseGenerationConfig()
    )

    assert generator.generated_sites[0].site_code == "DC-01"

    assert generator.generated_sites[1].site_code == "DC-02"

    assert generator.generated_sites[2].site_code == "REG-01"

    assert generator.generated_sites[-1].site_code == "BR-030"


# ==========================================================
# Country / Timezone
# ==========================================================

def test_country():

    generator = build_generator()

    generator.generate(
        EnterpriseGenerationConfig()
    )

    assert all(

        site.country == "India"

        for site

        in generator.generated_sites

    )


def test_timezone():

    generator = build_generator()

    generator.generate(
        EnterpriseGenerationConfig()
    )

    assert all(

        site.timezone == "Asia/Kolkata"

        for site

        in generator.generated_sites

    )


# ==========================================================
# Criticality
# ==========================================================

def test_data_center_criticality():

    generator = build_generator()

    generator.generate(
        EnterpriseGenerationConfig()
    )

    critical = [

        site

        for site

        in generator.generated_sites

        if site.site_type == "Data Center"

    ]

    assert all(

        site.criticality == "Critical"

        for site

        in critical

    )


def test_regional_criticality():

    generator = build_generator()

    generator.generate(
        EnterpriseGenerationConfig()
    )

    regional = [

        site

        for site

        in generator.generated_sites

        if site.site_type == "Regional Office"

    ]

    assert all(

        site.criticality == "High"

        for site

        in regional

    )


def test_branch_criticality():

    generator = build_generator()

    generator.generate(
        EnterpriseGenerationConfig()
    )

    branches = [

        site

        for site

        in generator.generated_sites

        if site.site_type == "Branch"

    ]

    assert all(

        site.criticality == "Medium"

        for site

        in branches

    )


# ==========================================================
# Statistics
# ==========================================================

def test_statistics():

    generator = build_generator()

    generator.generate(
        EnterpriseGenerationConfig()
    )

    stats = generator.statistics()

    assert stats["total_sites"] == 40

    assert stats["data_centers"] == 2

    assert stats["regional_offices"] == 8

    assert stats["branch_offices"] == 30

# ==========================================================
# Reset
# ==========================================================

def test_reset():

    generator = build_generator()

    generator.generate(
        EnterpriseGenerationConfig()
    )

    assert len(generator) == 40

    generator.reset()

    assert len(generator) == 0

    assert generator.generated_sites == []


# ==========================================================
# Utility Methods
# ==========================================================

def test_len():

    generator = build_generator()

    generator.generate(
        EnterpriseGenerationConfig()
    )

    assert len(generator) == 40


def test_repr():

    generator = build_generator()

    generator.generate(
        EnterpriseGenerationConfig()
    )

    representation = repr(generator)

    assert "SiteGenerator" in representation

    assert "sites=40" in representation

    assert "dc=2" in representation

    assert "regional=8" in representation

    assert "branches=30" in representation


# ==========================================================
# Custom Configuration
# ==========================================================

def test_custom_configuration():

    generator = build_generator()

    config = EnterpriseGenerationConfig(

        data_centers=1,

        regional_sites=2,

        branch_sites=5,

    )

    generator.generate(config)

    stats = generator.statistics()

    assert stats["total_sites"] == 8

    assert stats["data_centers"] == 1

    assert stats["regional_offices"] == 2

    assert stats["branch_offices"] == 5


# ==========================================================
# Multiple Generation
# ==========================================================

def test_multiple_generation_runs():

    generator = build_generator()

    first = generator.generate(
        EnterpriseGenerationConfig()
    )

    second = generator.generate(
        EnterpriseGenerationConfig()
    )

    assert len(first) == 40

    assert len(second) == 40

    assert len(generator) == 40


def test_generation_is_deterministic():

    generator = build_generator()

    first = generator.generate(
        EnterpriseGenerationConfig()
    )

    names1 = [

        site.site_name

        for site in first

    ]

    second = generator.generate(
        EnterpriseGenerationConfig()
    )

    names2 = [

        site.site_name

        for site in second

    ]

    assert names1 == names2


# ==========================================================
# Statistics Consistency
# ==========================================================

def test_statistics_consistency():

    generator = build_generator()

    generator.generate(
        EnterpriseGenerationConfig()
    )

    stats = generator.statistics()

    assert stats["total_sites"] == len(generator)

    assert (

        stats["data_centers"]

        + stats["regional_offices"]

        + stats["branch_offices"]

        == stats["total_sites"]

    )


# ==========================================================
# Site Integrity
# ==========================================================

def test_all_sites_have_required_fields():

    generator = build_generator()

    generator.generate(
        EnterpriseGenerationConfig()
    )

    for site in generator.generated_sites:

        assert site.site_name != ""

        assert site.site_code != ""

        assert site.site_type != ""

        assert site.country != ""

        assert site.timezone != ""


def test_site_names_unique():

    generator = build_generator()

    generator.generate(
        EnterpriseGenerationConfig()
    )

    names = [

        site.site_name

        for site in generator.generated_sites

    ]

    assert len(names) == len(set(names))


def test_site_codes_unique_again():

    generator = build_generator()

    generator.generate(
        EnterpriseGenerationConfig()
    )

    codes = [

        site.site_code

        for site in generator.generated_sites

    ]

    assert len(codes) == len(set(codes))