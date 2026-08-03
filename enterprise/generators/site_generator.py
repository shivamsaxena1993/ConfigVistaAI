"""
=============================================================

ConfigVista AI

Enterprise Site Generator

Artifact-2

=============================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from enterprise.models import (
    Site,
)

from enterprise.generators.enterprise_generator import (
    EnterpriseGenerationConfig,
)


# ============================================================
# CONSTANTS
# ============================================================

DATA_CENTER_NAMES = [

    "DC-NORTH",

    "DC-SOUTH",

]

REGIONAL_OFFICES = [

    "BENGALURU",

    "MUMBAI",

    "DELHI",

    "CHENNAI",

    "HYDERABAD",

    "KOLKATA",

    "PUNE",

    "AHMEDABAD",

]

COUNTRY = "India"

TIMEZONE = "Asia/Kolkata"


# ============================================================
# SITE GENERATOR
# ============================================================

class SiteGenerator:
    """
    Generates enterprise sites.

    Returns a list of Site objects.

    Does not register them into InventoryService.
    """

    def __init__(

        self,

    ):

        self.generated_sites = []

    # --------------------------------------------------------

    def generate(

        self,

        config: EnterpriseGenerationConfig,

    ) -> list[Site]:

        self.generated_sites = []

        self._generate_data_centers(

            config

        )

        self._generate_regional_offices(

            config

        )

        self._generate_branch_offices(

            config

        )

        return self.generated_sites
    
    # --------------------------------------------------------
    # Data Centers
    # --------------------------------------------------------

    def _generate_data_centers(
        self,
        config: EnterpriseGenerationConfig,
    ) -> None:
        """
        Generate enterprise data centers.
        """

        for index in range(
            config.data_centers
        ):

            site = Site(

                site_name=DATA_CENTER_NAMES[
                    index
                ],

                site_code=f"DC-{index + 1:02d}",

                site_type="Data Center",

                region="National",

                country=COUNTRY,

                timezone=TIMEZONE,

                criticality="Critical",

            )

            self.generated_sites.append(
                site
            )

    # --------------------------------------------------------
    # Regional Offices
    # --------------------------------------------------------

    def _generate_regional_offices(
        self,
        config: EnterpriseGenerationConfig,
    ) -> None:
        """
        Generate regional offices.
        """

        for index in range(
            config.regional_sites
        ):

            city = REGIONAL_OFFICES[
                index % len(
                    REGIONAL_OFFICES
                )
            ]

            site = Site(

                site_name=f"REG-{city}",

                site_code=f"REG-{index + 1:02d}",

                site_type="Regional Office",

                region=city,

                country=COUNTRY,

                timezone=TIMEZONE,

                criticality="High",

            )

            self.generated_sites.append(
                site
            )

    # --------------------------------------------------------
    # Branch Offices
    # --------------------------------------------------------

    def _generate_branch_offices(
        self,
        config: EnterpriseGenerationConfig,
    ) -> None:
        """
        Generate enterprise branch offices.
        """

        for index in range(
            config.branch_sites
        ):

            site = Site(

                site_name=f"BRANCH-{index + 1:03d}",

                site_code=f"BR-{index + 1:03d}",

                site_type="Branch",

                region=f"Region-{(index % 8) + 1}",

                country=COUNTRY,

                timezone=TIMEZONE,

                criticality="Medium",

            )

            self.generated_sites.append(
                site
            )

    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------

    def statistics(
        self,
    ) -> dict:
        """
        Returns generator statistics.
        """

        data_centers = sum(

            1

            for site in self.generated_sites

            if site.site_type == "Data Center"

        )

        regional = sum(

            1

            for site in self.generated_sites

            if site.site_type == "Regional Office"

        )

        branches = sum(

            1

            for site in self.generated_sites

            if site.site_type == "Branch"

        )

        return {

            "total_sites": len(
                self.generated_sites
            ),

            "data_centers": data_centers,

            "regional_offices": regional,

            "branch_offices": branches,

        }

    # --------------------------------------------------------

    def reset(
        self,
    ) -> None:
        """
        Clear generated sites.
        """

        self.generated_sites.clear()

    # --------------------------------------------------------

    def __len__(
        self,
    ) -> int:
        """
        Number of generated sites.
        """

        return len(
            self.generated_sites
        )

    # --------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        stats = self.statistics()

        return (

            "SiteGenerator("

            f"sites={stats['total_sites']}, "

            f"dc={stats['data_centers']}, "

            f"regional={stats['regional_offices']}, "

            f"branches={stats['branch_offices']})"

        )