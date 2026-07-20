
"""
====================================================================
File: services_parser.py

Project : ConfigVista AI

Purpose
-------
Enterprise services parser for Cisco IOS configurations.

Parses:
- DHCP Helpers
- IP SLA
- IP SLA Schedule
- Object Tracking
- QoS (Class/Policy/Service Policy)
- NetFlow
- Flexible NetFlow
- EEM
====================================================================
"""

import re


class ServicesParser:

    def __init__(self, lines):
        self.lines = lines

    def parse(self):

        data = {
            "dhcp_helpers": [],
            "ip_sla_operations": [],
            "ip_sla_schedules": [],
            "track_objects": [],
            "class_maps": [],
            "policy_maps": [],
            "service_policies": [],
            "netflow_enabled": False,
            "flow_monitors": [],
            "flow_exporters": [],
            "flow_records": [],
            "eem_enabled": False,
            "eem_applets": [],
        }

        current_int = None

        for raw in self.lines:
            line = raw.strip()

            if line.startswith("interface "):
                current_int = line.split()[1]
                continue

            if current_int and "ip helper-address" in line:
                data["dhcp_helpers"].append({
                    "interface": current_int,
                    "server": line.split()[-1]
                })

            if line.startswith("ip sla "):
                m = re.match(r"ip sla\s+(\d+)", line)
                if m:
                    data["ip_sla_operations"].append(int(m.group(1)))

            elif line.startswith("ip sla schedule"):
                data["ip_sla_schedules"].append(line)

            elif line.startswith("track "):
                data["track_objects"].append(line)

            elif line.startswith("class-map"):
                data["class_maps"].append(line)

            elif line.startswith("policy-map"):
                data["policy_maps"].append(line)

            elif line.startswith("service-policy"):
                data["service_policies"].append(line)

            elif (
                line.startswith("flow exporter")
                or line.startswith("flow monitor")
                or line.startswith("flow record")
                or line.startswith("ip flow")
            ):
                data["netflow_enabled"] = True

                if line.startswith("flow exporter"):
                    data["flow_exporters"].append(line.split()[2])

                elif line.startswith("flow monitor"):
                    data["flow_monitors"].append(line.split()[2])

                elif line.startswith("flow record"):
                    data["flow_records"].append(line.split()[2])

            elif line.startswith("event manager applet"):
                data["eem_enabled"] = True
                data["eem_applets"].append(line.split()[3])

        for key in (
            "ip_sla_operations",
            "ip_sla_schedules",
            "track_objects",
            "class_maps",
            "policy_maps",
            "service_policies",
            "flow_monitors",
            "flow_exporters",
            "flow_records",
            "eem_applets",
        ):
            if isinstance(data[key], list):
                try:
                    data[key] = sorted(set(data[key]))
                except TypeError:
                    pass

        return data
