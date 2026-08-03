"""
=============================================================

ConfigVista AI

Enterprise Business Service Generator

Artifact-2

=============================================================
"""

from __future__ import annotations

from enterprise.models import (
    BusinessService,
)

from enterprise.generators.enterprise_generator import (
    EnterpriseGenerationConfig,
)


# ============================================================
# SERVICE CATALOG
# ============================================================

SERVICE_CATALOG = [

    (
        "Corporate WAN",
        "Critical",
        99.99,
        "Network Operations",
        "Infrastructure",
    ),

    (
        "Internet Edge",
        "Critical",
        99.99,
        "Network Operations",
        "Infrastructure",
    ),

    (
        "Data Center Fabric",
        "Critical",
        99.99,
        "Data Center Team",
        "Infrastructure",
    ),

    (
        "Identity Services",
        "High",
        99.95,
        "Identity Team",
        "Security",
    ),

    (
        "DNS Services",
        "High",
        99.95,
        "Network Services",
        "Infrastructure",
    ),

    (
        "Voice Services",
        "High",
        99.95,
        "Collaboration Team",
        "Unified Communications",
    ),

    (
        "VPN Services",
        "High",
        99.95,
        "Security Operations",
        "Security",
    ),

    (
        "Wireless LAN",
        "Medium",
        99.90,
        "Wireless Team",
        "Infrastructure",
    ),

    (
        "Guest WiFi",
        "Medium",
        99.50,
        "Workplace Services",
        "End User Services",
    ),

    (
        "Monitoring Platform",
        "High",
        99.95,
        "NOC",
        "Operations",
    ),

    (
        "Backup Network",
        "Medium",
        99.90,
        "Infrastructure Team",
        "Infrastructure",
    ),

    (
        "Branch Connectivity",
        "Critical",
        99.99,
        "WAN Operations",
        "Infrastructure",
    ),

]


# ============================================================
# BUSINESS SERVICE GENERATOR
# ============================================================

class BusinessServiceGenerator:
    """
    Generates enterprise business services.

    Device relationships are intentionally
    created later by RelationshipService.
    """

    def __init__(self):

        self.generated_services = []

    # --------------------------------------------------------

    def generate(
        self,
        config: EnterpriseGenerationConfig,
    ) -> list[BusinessService]:
        """
        Generate enterprise business services.
        """

        self.generated_services = []

        for index, (

            service_name,

            criticality,

            sla,

            owner,

            business_unit,

        ) in enumerate(

            SERVICE_CATALOG,

            start=1,

        ):

            service = BusinessService(

                service_name=service_name,

                owner=owner,

                business_unit=business_unit,

                criticality=criticality,

                sla_percent=sla,

                availability_percent=100.0,

                description=(
                    f"Enterprise service providing {service_name}"
                ),

            )

            self.generated_services.append(
                service
            )

        return self.generated_services
    
    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------

    def statistics(
        self,
    ) -> dict:
        """
        Return generation statistics.
        """

        return {

            "total_services": len(
                self.generated_services
            ),

            "critical": sum(

                1

                for service

                in self.generated_services

                if service.criticality == "Critical"

            ),

            "high": sum(

                1

                for service

                in self.generated_services

                if service.criticality == "High"

            ),

            "medium": sum(

                1

                for service

                in self.generated_services

                if service.criticality == "Medium"

            ),

        }

    # --------------------------------------------------------
    # Lookup Helpers
    # --------------------------------------------------------

    def get_service(
        self,
        service_name: str,
    ) -> BusinessService | None:
        """
        Return a business service by name.
        """

        for service in self.generated_services:

            if service.service_name == service_name:

                return service

        return None


    def critical_services(
        self,
    ) -> list[BusinessService]:
        """
        Return all critical services.
        """

        return [

            service

            for service

            in self.generated_services

            if service.criticality == "Critical"

        ]


    def high_priority_services(
        self,
    ) -> list[BusinessService]:
        """
        Return all high priority services.
        """

        return [

            service

            for service

            in self.generated_services

            if service.criticality == "High"

        ]
    
    # --------------------------------------------------------
    # Reset
    # --------------------------------------------------------

    def reset(
        self,
    ) -> None:
        """
        Clear generated services.
        """

        self.generated_services.clear()

    # --------------------------------------------------------
    # Utility Methods
    # --------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return len(
            self.generated_services
        )


    def __repr__(
        self,
    ) -> str:

        stats = self.statistics()

        return (

            "BusinessServiceGenerator("

            f"services={stats['total_services']}, "

            f"critical={stats['critical']}, "

            f"high={stats['high']}, "

            f"medium={stats['medium']})"

        )