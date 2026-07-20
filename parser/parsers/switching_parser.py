
"""
====================================================================
File: switching_parser.py

Project : ConfigVista AI

Purpose
-------
Enterprise switching parser for Cisco IOS configurations.

Parses:
- VLANs
- HSRP
- Spanning Tree
- Port-Channels
- VTP
- DHCP Snooping
- Dynamic ARP Inspection
- Loop Guard
- UDLD
- Jumbo MTU
====================================================================
"""

import re


class SwitchingParser:

    def __init__(self, lines):
        self.lines = lines

    def parse(self):

        data = {
            "vlans": [],
            "stp_mode": None,
            "stp_priorities": [],
            "vtp_mode": None,
            "hsrp_groups": [],
            "port_channels": [],
            "dhcp_snooping": False,
            "dhcp_snooping_vlans": [],
            "arp_inspection": [],
            "loop_guard": False,
            "udld": False,
            "jumbo_mtu": None,
        }

        current_vlan = None
        current_int = None

        for raw in self.lines:
            line = raw.strip()

            if line.startswith("system mtu jumbo"):
                data["jumbo_mtu"] = line.split()[-1]

            elif line.startswith("vtp mode"):
                data["vtp_mode"] = line.split()[-1]

            elif line.startswith("spanning-tree mode"):
                data["stp_mode"] = line.split()[-1]

            elif line.startswith("spanning-tree vlan"):
                data["stp_priorities"].append(line)

            elif line.startswith("spanning-tree loopguard"):
                data["loop_guard"] = True

            elif line.startswith("udld"):
                data["udld"] = True

            elif line.startswith("vlan "):
                parts = line.split()
                if len(parts) > 1 and parts[1].isdigit():
                    current_vlan = {"id": int(parts[1]), "name": ""}
                    data["vlans"].append(current_vlan)
                continue

            elif current_vlan and line.startswith("name "):
                current_vlan["name"] = line[5:]

            elif line.startswith("interface "):
                current_int = line.split()[1]
                if current_int.startswith("Port-channel"):
                    data["port_channels"].append(current_int)
                continue

            elif current_int:
                m = re.match(r"standby\s+(\d+)\s+ip\s+(\S+)", line)
                if m:
                    data["hsrp_groups"].append({
                        "group": int(m.group(1)),
                        "virtual_ip": m.group(2),
                        "priority": None,
                        "preempt": False,
                    })
                    continue

                m = re.match(r"standby\s+(\d+)\s+priority\s+(\d+)", line)
                if m:
                    for g in reversed(data["hsrp_groups"]):
                        if g["group"] == int(m.group(1)):
                            g["priority"] = int(m.group(2))
                            break
                    continue

                m = re.match(r"standby\s+(\d+)\s+preempt", line)
                if m:
                    for g in reversed(data["hsrp_groups"]):
                        if g["group"] == int(m.group(1)):
                            g["preempt"] = True
                            break

            if line == "ip dhcp snooping":
                data["dhcp_snooping"] = True

            elif line.startswith("ip dhcp snooping vlan"):
                vlans = line.split("vlan",1)[1]
                data["dhcp_snooping_vlans"] = [v.strip() for v in vlans.split(",")]

            elif line.startswith("ip arp inspection vlan"):
                vlans = line.split("vlan",1)[1]
                data["arp_inspection"] = [v.strip() for v in vlans.split(",")]

        data["port_channels"] = sorted(set(data["port_channels"]))
        return data
