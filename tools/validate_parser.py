import sys
import csv
import json
import time
from pathlib import Path

# -------------------------------------------------------
# Add project root to Python path
# -------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(PROJECT_ROOT))

# -------------------------------------------------------
# Imports
# -------------------------------------------------------

from parser.parsers.config_parser import (
    load_config,
    ConfigParser,
)


# ==============================================================
# Configuration
# ==============================================================

CONFIG_ROOT = Path("data/sample_configs")

REPORT_DIR = Path("tools")

REPORT_DIR.mkdir(exist_ok=True)


# ==============================================================
# Find all configuration files
# ==============================================================

config_files = sorted(CONFIG_ROOT.rglob("*.txt"))

results = []

total_time = 0


print("=" * 70)
print("CONFIGVISTA AI PARSER VALIDATION")
print("=" * 70)
print()


# ==============================================================
# Parse every configuration
# ==============================================================

for cfg in config_files:

    print(f"Parsing : {cfg.name}")

    try:

        start = time.perf_counter()

        config = load_config(cfg)

        parser = ConfigParser(config)

        data = parser.parse()

        elapsed = time.perf_counter() - start

        total_time += elapsed

        result = {

            "device": cfg.name,

            "status": "PASS",

            "parse_time_sec": round(elapsed, 4),

            "hostname": data.get("hostname"),

            "device_role": data.get("device_role"),

            "interfaces": len(data.get("interfaces", [])),

            "physical_interfaces": len(data.get("physical_interfaces", [])),

            "loopbacks": len(data.get("loopbacks", [])),

            "svis": len(data.get("svis", [])),

            "port_channels": len(data.get("port_channels", [])),

            "vlans": len(data.get("vlans", [])),

            "vrfs": len(data.get("vrfs", [])),

            "routing_protocols": ", ".join(
                data.get("routing_protocols", [])
            ),

            "ospf_processes": len(
                data.get("ospf_processes", [])
            ),

            "bgp_neighbors": len(
                data.get("bgp_neighbors", [])
            ),

            "bgp_as": data.get("bgp_as"),

            "static_routes": len(
                data.get("static_routes", [])
            ),

            "route_maps": len(
                data.get("route_maps", [])
            ),

            "prefix_lists": len(
                data.get("prefix_lists", [])
            ),

            "acls": len(
                data.get("acl_names", [])
            ),

            "hsrp_groups": len(
                data.get("hsrp_groups", [])
            ),

            "dhcp_helpers": len(
                data.get("dhcp_helpers", [])
            ),

            "ntp_servers": len(
                data.get("ntp_servers", [])
            ),

            "logging_servers": len(
                data.get("logging_servers", [])
            ),

            "snmp": data.get("snmp_enabled"),

            "aaa": data.get("aaa_enabled"),

            "ssh": data.get("ssh_enabled"),

            "stp_mode": data.get("stp_mode"),

        }

    except Exception as exc:

        result = {

            "device": cfg.name,

            "status": "FAIL",

            "error": str(exc),

        }

    results.append(result)

print()

print("=" * 70)

print("Validation Complete")

print("=" * 70)


# ==============================================================
# CSV Report
# ==============================================================

csv_file = REPORT_DIR / "parser_report.csv"

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


# ==============================================================
# JSON Report
# ==============================================================

json_file = REPORT_DIR / "parser_report.json"

with open(json_file, "w", encoding="utf-8") as f:

    json.dump(
        results,
        f,
        indent=4,
    )


# ==============================================================
# Summary
# ==============================================================

passed = sum(
    1
    for r in results
    if r["status"] == "PASS"
)

failed = len(results) - passed

summary_file = REPORT_DIR / "parser_summary.txt"

with open(summary_file, "w", encoding="utf-8") as f:

    f.write("CONFIGVISTA AI PARSER VALIDATION\n")

    f.write("=" * 50 + "\n\n")

    f.write(f"Configurations Parsed : {len(results)}\n")

    f.write(f"Passed                : {passed}\n")

    f.write(f"Failed                : {failed}\n")

    f.write(
        f"Average Parse Time    : "
        f"{total_time / max(1, len(results)):.4f} sec\n"
    )

    f.write("\n")

    if failed:

        f.write("FAILED CONFIGURATIONS\n")

        f.write("-" * 30 + "\n")

        for r in results:

            if r["status"] == "FAIL":

                f.write(
                    f"{r['device']} : {r['error']}\n"
                )


print()

print(f"CSV Report     : {csv_file}")

print(f"JSON Report    : {json_file}")

print(f"Summary Report : {summary_file}")

print()

print("=" * 70)

print(f"Configurations : {len(results)}")

print(f"Passed         : {passed}")

print(f"Failed         : {failed}")

print(f"Average Time   : {total_time / max(1, len(results)):.4f} sec")

print("=" * 70)