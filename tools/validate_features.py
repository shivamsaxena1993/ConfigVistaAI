"""
====================================================================

ConfigVista AI
Feature Validation Utility

Purpose
-------
Validates extracted parser features for all sample configurations.

Outputs
-------
tools/feature_validation.csv
tools/feature_validation.json
tools/feature_validation_summary.txt

====================================================================
"""

import csv
import json
import sys
from pathlib import Path

# ------------------------------------------------------------
# Add project root to Python path
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from parser.parsers.config_parser import (
    load_config,
    ConfigParser,
)

# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------

CONFIG_ROOT = Path("data/sample_configs")

REPORT_DIR = Path("tools")
REPORT_DIR.mkdir(exist_ok=True)

# ------------------------------------------------------------
# Collect configuration files
# ------------------------------------------------------------

config_files = sorted(
    f
    for f in CONFIG_ROOT.rglob("*.txt")
    if f.name != "sample_router.txt"
)

results = []

print("=" * 70)
print("CONFIGVISTA AI FEATURE VALIDATION")
print("=" * 70)
print()

# ------------------------------------------------------------
# Validate Features
# ------------------------------------------------------------

for cfg in config_files:

    print(f"Validating : {cfg.name}")

    config = load_config(cfg)

    parser = ConfigParser(config)

    data = parser.parse()

    result = {

        "device": cfg.name,

        "hostname": data.get("hostname"),

        "device_role": data.get("device_role"),

        "interfaces": len(data.get("interfaces", [])),
        "physical_interfaces": len(data.get("physical_interfaces", [])),
        "loopbacks": len(data.get("loopbacks", [])),
        "svis": len(data.get("svis", [])),
        "port_channels": len(data.get("port_channels", [])),

        "vlans": len(data.get("vlans", [])),
        "vrfs": len(data.get("vrfs", [])),

        "routing_protocols":
            ", ".join(data.get("routing_protocols", [])),

        "ospf_processes":
            len(data.get("ospf_processes", [])),

        "eigrp_processes":
            len(data.get("eigrp_processes", [])),

        "rip_processes":
            len(data.get("rip_processes", [])),

        "bgp_as":
            data.get("bgp_as"),

        "bgp_neighbors":
            len(data.get("bgp_neighbors", [])),

        "static_routes":
            len(data.get("static_routes", [])),

        "route_maps":
            len(data.get("route_maps", [])),

        "prefix_lists":
            len(data.get("prefix_lists", [])),

        "acls":
            len(data.get("acl_names", [])),

        "hsrp_groups":
            len(data.get("hsrp_groups", [])),

        "dhcp_helpers":
            len(data.get("dhcp_helpers", [])),

        "ntp_servers":
            len(data.get("ntp_servers", [])),

        "logging_servers":
            len(data.get("logging_servers", [])),

        "snmp":
            data.get("snmp_enabled"),

        "aaa":
            data.get("aaa_enabled"),

        "ssh":
            data.get("ssh_enabled"),

        "stp_mode":
            data.get("stp_mode"),
    }

    results.append(result)

print()

print("=" * 70)
print("Feature Validation Complete")
print("=" * 70)

# ------------------------------------------------------------
# CSV Report
# ------------------------------------------------------------

csv_file = REPORT_DIR / "feature_validation.csv"

headers = sorted(
    {
        key
        for row in results
        for key in row.keys()
    }
)

with open(csv_file, "w", newline="", encoding="utf-8") as f:

    writer = csv.DictWriter(
        f,
        fieldnames=headers,
    )

    writer.writeheader()

    writer.writerows(results)

# ------------------------------------------------------------
# JSON Report
# ------------------------------------------------------------

json_file = REPORT_DIR / "feature_validation.json"

with open(json_file, "w", encoding="utf-8") as f:

    json.dump(
        results,
        f,
        indent=4,
    )

# ------------------------------------------------------------
# Coverage Statistics
# ------------------------------------------------------------

coverage = {

    "Hostname":

        sum(
            1
            for r in results
            if r["hostname"]
        ),

    "Device Role":

        sum(
            1
            for r in results
            if r["device_role"]
        ),

    "Interfaces":

        sum(
            1
            for r in results
            if r["interfaces"] > 0
        ),

    "VLANs":

        sum(
            1
            for r in results
            if r["vlans"] > 0
        ),

    "OSPF":

        sum(
            1
            for r in results
            if r["ospf_processes"] > 0
        ),

    "BGP":

        sum(
            1
            for r in results
            if r["bgp_neighbors"] > 0
        ),

    "Static Routes":

        sum(
            1
            for r in results
            if r["static_routes"] > 0
        ),

    "ACLs":

        sum(
            1
            for r in results
            if r["acls"] > 0
        ),

    "HSRP":

        sum(
            1
            for r in results
            if r["hsrp_groups"] > 0
        ),

    "Port-Channels":

        sum(
            1
            for r in results
            if r["port_channels"] > 0
        ),

    "DHCP Helpers":

        sum(
            1
            for r in results
            if r["dhcp_helpers"] > 0
        ),

    "SNMP":

        sum(
            1
            for r in results
            if r["snmp"]
        ),

    "AAA":

        sum(
            1
            for r in results
            if r["aaa"]
        ),

    "SSH":

        sum(
            1
            for r in results
            if r["ssh"]
        ),
}

# ------------------------------------------------------------
# Summary
# ------------------------------------------------------------

summary_file = REPORT_DIR / "feature_validation_summary.txt"

with open(summary_file, "w", encoding="utf-8") as f:

    f.write("CONFIGVISTA AI FEATURE VALIDATION\n")
    f.write("=" * 55 + "\n\n")

    f.write(
        f"Configurations Validated : {len(results)}\n\n"
    )

    f.write("FEATURE COVERAGE\n")
    f.write("-" * 30 + "\n")

    for feature, value in coverage.items():

        percent = value / len(results) * 100

        f.write(
            f"{feature:<20}"
            f"{value:>3}/{len(results)}"
            f"   ({percent:.0f}%)\n"
        )

print()

print(f"CSV Report     : {csv_file}")
print(f"JSON Report    : {json_file}")
print(f"Summary Report : {summary_file}")

print()

print("=" * 70)

print(f"Devices Validated : {len(results)}")

for feature, value in coverage.items():

    percent = value / len(results) * 100

    print(
        f"{feature:<20}"
        f"{value:>2}/{len(results)}"
        f" ({percent:.0f}%)"
    )

print("=" * 70)