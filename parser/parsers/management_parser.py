
"""
====================================================================
File: management_parser.py

Project : ConfigVista AI

Purpose
-------
Enterprise management parser for Cisco IOS configurations.

Parses:
- NTP
- Syslog
- SNMP
- DNS
- Archive
- Banner
- Call Home
- Console / VTY
- Login
- SSH
====================================================================
"""

import re


class ManagementParser:

    def __init__(self, lines):
        self.lines = lines

    def parse(self):

        data = {
            "ntp_servers": [],
            "logging_hosts": [],
            "logging_buffered": None,
            "snmp_enabled": False,
            "snmp_communities": [],
            "snmp_location": None,
            "snmp_contact": None,
            "dns_servers": [],
            "domain_name": None,
            "archive_enabled": False,
            "archive_path": None,
            "banner_motd": False,
            "call_home": False,
            "ssh_enabled": False,
            "console_login": False,
            "vty_login": False,
            "transport_input": [],
        }

        section = None

        for raw in self.lines:
            line = raw.strip()

            if line.startswith("ip domain name"):
                data["domain_name"] = line.split()[-1]

            elif line.startswith("ip name-server"):
                data["dns_servers"].extend(line.split()[2:])

            elif line.startswith("ntp server"):
                data["ntp_servers"].append(line.split()[-1])

            elif line.startswith("logging host"):
                data["logging_hosts"].append(line.split()[-1])

            elif line.startswith("logging buffered"):
                data["logging_buffered"] = line

            elif line.startswith("snmp-server"):
                data["snmp_enabled"] = True

                m = re.match(r"snmp-server community\s+(\S+)", line)
                if m:
                    data["snmp_communities"].append(m.group(1))

                m = re.match(r"snmp-server location\s+(.+)", line)
                if m:
                    data["snmp_location"] = m.group(1)

                m = re.match(r"snmp-server contact\s+(.+)", line)
                if m:
                    data["snmp_contact"] = m.group(1)

            elif line.startswith("ip ssh version"):
                data["ssh_enabled"] = True

            elif line.startswith("archive"):
                section = "archive"
                data["archive_enabled"] = True
                continue

            elif section == "archive":
                if line.startswith("path "):
                    data["archive_path"] = line.split(None,1)[1]
                if line == "!":
                    section = None

            elif line.startswith("banner motd"):
                data["banner_motd"] = True

            elif line.startswith("call-home"):
                data["call_home"] = True

            elif line.startswith("line con"):
                section = "console"
                continue

            elif line.startswith("line vty"):
                section = "vty"
                continue

            elif section == "console":
                if line.startswith("login"):
                    data["console_login"] = True

            elif section == "vty":
                if line.startswith("login"):
                    data["vty_login"] = True
                elif line.startswith("transport input"):
                    data["transport_input"] = line.split()[2:]

        for key in ("ntp_servers","logging_hosts","snmp_communities","dns_servers","transport_input"):
            data[key] = sorted(set(data[key]))

        return data
