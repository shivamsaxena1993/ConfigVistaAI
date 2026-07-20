
"""
====================================================================
File: metadata_parser.py

Project : ConfigVista AI

Purpose
-------
Enterprise metadata parser for Cisco IOS configurations.

Parses:
- Hostname
- Device Role
- Vendor
- Platform
- Software Version
- Domain Name
- Timezone
- Serial Number (if present)
- Site (from banner/comment)
- Environment (Lab/Dev/UAT/Prod)
====================================================================
"""

import re


class MetadataParser:

    def __init__(self, lines):
        self.lines = lines

    def parse(self):

        data = {
            "hostname": None,
            "device_role": None,
            "vendor": "Cisco",
            "platform": None,
            "software_version": None,
            "serial_number": None,
            "domain_name": None,
            "timezone": None,
            "site": None,
            "environment": None,
        }

        for raw in self.lines:
            line = raw.strip()

            if line.startswith("hostname "):
                data["hostname"] = line.split()[1]

            elif line.startswith("version "):
                data["software_version"] = line.split()[1]

            elif line.startswith("ip domain name "):
                data["domain_name"] = line.split()[-1]

            elif line.startswith("clock timezone "):
                parts = line.split()
                if len(parts) >= 3:
                    data["timezone"] = parts[2]

            elif line.startswith("! Device Role"):
                data["device_role"] = line.split(":", 1)[1].strip()

            elif line.startswith("! Platform"):
                data["platform"] = line.split(":", 1)[1].strip()

            elif line.startswith("! Site"):
                data["site"] = line.split(":", 1)[1].strip()

            elif line.startswith("! Environment"):
                data["environment"] = line.split(":", 1)[1].strip()

            elif "Processor board ID" in line:
                m = re.search(r"Processor board ID\s+(\S+)", line)
                if m:
                    data["serial_number"] = m.group(1)

        if data["device_role"] is None:
            text = "\n".join(self.lines).lower()

            if "zone security" in text:
                data["device_role"] = "Firewall"
            elif "crypto isakmp" in text or "tunnel " in text:
                data["device_role"] = "VPN Gateway"
            elif "router bgp" in text:
                data["device_role"] = "Core Router"
            elif "spanning-tree mode" in text and "standby " in text:
                data["device_role"] = "Distribution Switch"
            elif "spanning-tree mode" in text:
                data["device_role"] = "Access Switch"
            elif "router ospf" in text:
                data["device_role"] = "Branch Router"
            else:
                data["device_role"] = "Unknown"

        if data["environment"] is None:
            hostname = (data["hostname"] or "").lower()
            if hostname.startswith(("core", "dist", "access", "branch", "edge", "vpn")):
                data["environment"] = "Production"

        if data["platform"] is None:
            text = "\n".join(self.lines)
            if "GigabitEthernet" in text:
                data["platform"] = "Cisco IOS-XE"

        return data
