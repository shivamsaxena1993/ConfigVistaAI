"""
====================================================================

File: config_parser.py

Project : ConfigVista AI

Purpose
-------
Enterprise Configuration Parser Orchestrator

Responsibilities
----------------
• Load configuration
• Execute all parser modules
• Merge parser outputs
• Validate parser results
• Produce unified parsed dictionary
• Provide parser metadata

====================================================================
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Any
import logging
import time

from parser.parsers.metadata_parser import MetadataParser
from parser.parsers.interface_parser import InterfaceParser
from parser.parsers.routing_parser import RoutingParser
from parser.parsers.switching_parser import SwitchingParser
from parser.parsers.security_parser import SecurityParser
from parser.parsers.management_parser import ManagementParser
from parser.parsers.services_parser import ServicesParser


# ============================================================
# Logging
# ============================================================

logger = logging.getLogger(__name__)


# ============================================================
# Helper
# ============================================================

def load_config(path: str) -> str:
    """
    Read configuration file.
    """

    return Path(path).read_text(
        encoding="utf-8"
    )


# ============================================================
# Config Parser
# ============================================================

class ConfigParser:
    """
    Enterprise parser orchestrator.

    Executes all parser modules.

    Returns one unified dictionary.
    """

    PARSER_VERSION = "2.0"

    def __init__(self, config: str):

        self.config = config

        self.lines = [
            line.rstrip()
            for line in config.splitlines()
        ]

        self.results: Dict[str, Any] = {}

        self.statistics = {
            "parsers_executed": 0,
            "execution_time": 0.0,
            "warnings": [],
            "errors": []
        }

        self.parsers = [

            (
                "metadata",
                MetadataParser,
            ),

            (
                "interfaces",
                InterfaceParser,
            ),

            (
                "routing",
                RoutingParser,
            ),

            (
                "switching",
                SwitchingParser,
            ),

            (
                "security",
                SecurityParser,
            ),

            (
                "management",
                ManagementParser,
            ),

            (
                "services",
                ServicesParser,
            ),
        ]

    # =======================================================
    # Utility
    # =======================================================

    @staticmethod
    def _count(value):

        if value is None:
            return 0

        if isinstance(value, list):
            return len(value)

        return int(bool(value))

    # =======================================================
    # Merge helper
    # =======================================================

    def _merge_result(
        self,
        new_data: Dict[str, Any]
    ):

        for key, value in new_data.items():

            if key not in self.results:

                self.results[key] = value

                continue

            current = self.results[key]

            if isinstance(current, list) and isinstance(value, list):

                current.extend(value)

                continue

            self.results[key] = value

    # =======================================================
    # Remove duplicates
    # =======================================================

    def _deduplicate_lists(self):

        for key, value in self.results.items():

            if not isinstance(value, list):
                continue

            try:

                self.results[key] = list(
                    dict.fromkeys(value)
                )

            except TypeError:

                pass

    # =======================================================
    # Execute All Parsers
    # =======================================================

    def parse(self) -> Dict[str, Any]:
        """
        Execute every registered parser and return
        one unified parsed dictionary.
        """

        start_time = time.perf_counter()

        logger.info("Starting ConfigVista parser")

        for parser_name, parser_class in self.parsers:

            try:

                logger.debug(
                    "Executing %s parser",
                    parser_name,
                )

                parser = parser_class(self.lines)

                result = parser.parse()

                self.statistics["parsers_executed"] += 1

                # ------------------------------------------
                # Interface parser returns a LIST
                # ------------------------------------------

                if parser_name == "interfaces":

                    self.results["interfaces"] = result

                    self.results["physical_interfaces"] = [
                        i
                        for i in result
                        if i.get("physical")
                    ]

                    self.results["loopbacks"] = [
                        i
                        for i in result
                        if i.get("loopback")
                    ]

                    self.results["svis"] = [
                        i
                        for i in result
                        if i.get("svi")
                    ]

                    self.results["port_channel_interfaces"] = [
                        i
                        for i in result
                        if i.get("port_channel")
                    ]

                else:

                    self._merge_result(result)

            except Exception as exc:

                logger.exception(
                    "Parser failure : %s",
                    parser_name,
                )

                self.statistics["errors"].append(
                    {
                        "parser": parser_name,
                        "error": str(exc),
                    }
                )

        # ------------------------------------------
        # Cleanup
        # ------------------------------------------

        self._deduplicate_lists()

        # ------------------------------------------
        # Inventory Counts
        # ------------------------------------------

        self.results["interface_count"] = self._count(
            self.results.get("interfaces")
        )

        self.results["physical_interface_count"] = self._count(
            self.results.get("physical_interfaces")
        )

        self.results["loopback_count"] = self._count(
            self.results.get("loopbacks")
        )

        self.results["svi_count"] = self._count(
            self.results.get("svis")
        )

        self.results["port_channel_count"] = self._count(
            self.results.get("port_channel_interfaces")
        )

        # ------------------------------------------
        # Routing
        # ------------------------------------------

        self.results["routing_protocol_count"] = self._count(
            self.results.get("routing_protocols")
        )

        self.results["ospf_process_count"] = self._count(
            self.results.get("ospf_processes")
        )

        self.results["bgp_neighbor_count"] = self._count(
            self.results.get("bgp_neighbors")
        )

        self.results["vrf_count"] = self._count(
            self.results.get("vrfs")
        )

        self.results["static_route_count"] = self._count(
            self.results.get("static_routes")
        )

        # ------------------------------------------
        # Switching
        # ------------------------------------------

        self.results["vlan_count"] = self._count(
            self.results.get("vlans")
        )

        self.results["hsrp_group_count"] = self._count(
            self.results.get("hsrp_groups")
        )

        # ------------------------------------------
        # Security
        # ------------------------------------------

        self.results["acl_count"] = self._count(
            self.results.get("acl_names")
        )

        # ------------------------------------------
        # Services
        # ------------------------------------------

        self.results["dhcp_helper_count"] = self._count(
            self.results.get("dhcp_helpers")
        )

        # ------------------------------------------
        # Management
        # ------------------------------------------

        self.results["ntp_server_count"] = self._count(
            self.results.get("ntp_servers")
        )

        self.results["logging_server_count"] = self._count(
            self.results.get("logging_servers")
        )

        # ------------------------------------------
        # Parser Metadata
        # ------------------------------------------

        elapsed = time.perf_counter() - start_time

        self.statistics["execution_time"] = round(
            elapsed,
            6,
        )

        self.results["parser_metadata"] = {

            "version": self.PARSER_VERSION,

            "execution_time":
                self.statistics["execution_time"],

            "parsers_executed":
                self.statistics["parsers_executed"],

            "errors":
                len(
                    self.statistics["errors"]
                ),

            "warnings":
                len(
                    self.statistics["warnings"]
                ),
        }

        logger.info(
            "Completed parsing in %.4f seconds",
            elapsed,
        )

        return self.results
    
        # =======================================================
        # Validation
        # =======================================================
    
        def validate(self):
            """
            Perform basic validation of parsed results.
            Returns a list of warnings.
            """
    
            warnings = []
    
            if not self.results.get("hostname"):
                warnings.append("Hostname not detected.")
    
            if self.results.get("interface_count", 0) == 0:
                warnings.append("No interfaces detected.")
    
            if not self.results.get("routing_protocols"):
                warnings.append("No routing protocol detected.")
    
            self.statistics["warnings"] = warnings
    
            return warnings
    
        # =======================================================
        # Summary
        # =======================================================
    
        def summary(self):
            """
            Return a lightweight parser summary.
            """
    
            return {
            
                "hostname":
                    self.results.get("hostname"),
    
                "device_role":
                    self.results.get("device_role"),
    
                "interfaces":
                    self.results.get("interface_count"),
    
                "vlans":
                    self.results.get("vlan_count"),
    
                "routing_protocols":
                    self.results.get("routing_protocols"),
    
                "bgp_neighbors":
                    self.results.get("bgp_neighbor_count"),
    
                "ospf_processes":
                    self.results.get("ospf_process_count"),
    
                "acl_count":
                    self.results.get("acl_count"),
    
                "parser_metadata":
                    self.results.get("parser_metadata"),
            }


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":

    import argparse
    import json

    cli = argparse.ArgumentParser(
        description="ConfigVista AI Configuration Parser"
    )

    cli.add_argument(
        "config",
        help="Cisco IOS configuration file",
    )

    args = cli.parse_args()

    config = load_config(args.config)

    parser = ConfigParser(config)

    result = parser.parse()

    parser.validate()

    print(json.dumps(
        result,
        indent=4,
        default=str,
    ))

    print("\nParser Summary\n")

    print(json.dumps(
        parser.summary(),
        indent=4,
    ))