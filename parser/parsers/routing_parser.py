
"""
====================================================================
File: routing_parser.py

Project : ConfigVista AI

Purpose
-------
Enterprise routing parser for Cisco IOS configurations.

Parses:
- OSPF
- BGP
- EIGRP
- RIP
- Static Routes
- VRFs
- Prefix Lists
- Route Maps
====================================================================
"""

import re


class RoutingParser:

    def __init__(self, lines):
        self.lines = lines

    def parse(self):

        routing = {
            "routing_protocols": [],
            "ospf_processes": [],
            "ospf_router_id": None,
            "ospf_networks": [],
            "ospf_passive_interfaces": [],
            "bgp_as": None,
            "bgp_router_id": None,
            "bgp_neighbors": [],
            "eigrp_processes": [],
            "rip_enabled": False,
            "static_routes": [],
            "default_routes": [],
            "vrfs": [],
            "route_maps": [],
            "prefix_lists": [],
        }

        current_protocol = None

        for raw in self.lines:
            line = raw.strip()

            if line.startswith("vrf definition "):
                routing["vrfs"].append(line.split()[2])

            elif line.startswith("router ospf"):
                current_protocol = "OSPF"
                routing["routing_protocols"].append("OSPF")
                routing["ospf_processes"].append(line.split()[-1])

            elif line.startswith("router bgp"):
                current_protocol = "BGP"
                routing["routing_protocols"].append("BGP")
                routing["bgp_as"] = line.split()[-1]

            elif line.startswith("router eigrp"):
                current_protocol = "EIGRP"
                routing["routing_protocols"].append("EIGRP")
                routing["eigrp_processes"].append(line.split()[-1])

            elif line.startswith("router rip"):
                current_protocol = "RIP"
                routing["routing_protocols"].append("RIP")
                routing["rip_enabled"] = True

            elif current_protocol == "OSPF":
                if line.startswith("router-id"):
                    routing["ospf_router_id"] = line.split()[-1]
                elif line.startswith("network"):
                    routing["ospf_networks"].append(line)
                elif line.startswith("passive-interface"):
                    routing["ospf_passive_interfaces"].append(line.split()[-1])

            elif current_protocol == "BGP":
                if line.startswith("bgp router-id"):
                    routing["bgp_router_id"] = line.split()[-1]
                elif line.startswith("neighbor"):
                    m = re.match(r"neighbor\s+(\S+)\s+remote-as\s+(\S+)", line)
                    if m:
                        routing["bgp_neighbors"].append({
                            "neighbor": m.group(1),
                            "remote_as": m.group(2)
                        })

            if line.startswith("ip route"):
                routing["static_routes"].append(line)
                if line.startswith("ip route 0.0.0.0 0.0.0.0"):
                    routing["default_routes"].append(line)

            elif line.startswith("route-map"):
                routing["route_maps"].append(line.split()[1])

            elif line.startswith("ip prefix-list"):
                routing["prefix_lists"].append(line)

        routing["routing_protocols"] = sorted(set(routing["routing_protocols"]))
        routing["route_maps"] = sorted(set(routing["route_maps"]))
        routing["prefix_lists"] = sorted(set(routing["prefix_lists"]))

        return routing
