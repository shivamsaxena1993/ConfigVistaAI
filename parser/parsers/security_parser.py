
"""
====================================================================
File: security_parser.py

Project : ConfigVista AI

Purpose
-------
Enterprise security parser for Cisco IOS configurations.

Parses:
- ACLs
- AAA
- Local Users
- Enable Secret
- SSH
- NAT / PAT
- Zone Based Firewall
- VPN / IPsec
- ISAKMP
- Crypto Maps
- Transform Sets
- Tunnel Interfaces
====================================================================
"""

import re


class SecurityParser:

    def __init__(self, lines):
        self.lines = lines

    def parse(self):

        data = {
            "aaa_enabled": False,
            "ssh_enabled": False,
            "enable_secret": False,
            "local_users": [],
            "acl_names": [],
            "nat_enabled": False,
            "nat_inside_interfaces": [],
            "nat_outside_interfaces": [],
            "zone_firewall": False,
            "zones": [],
            "zone_pairs": [],
            "class_maps": [],
            "policy_maps": [],
            "vpn_enabled": False,
            "isakmp_policies": [],
            "transform_sets": [],
            "crypto_maps": [],
            "tunnel_interfaces": [],
        }

        current_int = None

        for raw in self.lines:
            line = raw.strip()

            if line.startswith("aaa new-model"):
                data["aaa_enabled"] = True

            elif line.startswith("enable secret"):
                data["enable_secret"] = True

            elif line.startswith("username "):
                parts = line.split()
                if len(parts) >= 2:
                    data["local_users"].append(parts[1])

            elif line.startswith("ip ssh version"):
                data["ssh_enabled"] = True

            elif line.startswith("ip access-list"):
                parts = line.split()
                if len(parts) >= 4:
                    data["acl_names"].append(parts[-1])

            elif line.startswith("interface "):
                current_int = line.split()[1]
                if current_int.startswith("Tunnel"):
                    data["tunnel_interfaces"].append(current_int)
                continue

            elif current_int:
                if line == "ip nat inside":
                    data["nat_enabled"] = True
                    data["nat_inside_interfaces"].append(current_int)
                elif line == "ip nat outside":
                    data["nat_enabled"] = True
                    data["nat_outside_interfaces"].append(current_int)

            if line.startswith("zone security"):
                data["zone_firewall"] = True
                data["zones"].append(line.split()[-1])

            elif line.startswith("zone-pair security"):
                data["zone_pairs"].append(line)

            elif line.startswith("class-map"):
                data["class_maps"].append(line)

            elif line.startswith("policy-map"):
                data["policy_maps"].append(line)

            elif line.startswith("crypto isakmp policy"):
                data["vpn_enabled"] = True
                data["isakmp_policies"].append(line.split()[-1])

            elif line.startswith("crypto ipsec transform-set"):
                data["vpn_enabled"] = True
                m = re.match(r"crypto ipsec transform-set\s+(\S+)", line)
                if m:
                    data["transform_sets"].append(m.group(1))

            elif line.startswith("crypto map"):
                data["vpn_enabled"] = True
                m = re.match(r"crypto map\s+(\S+)", line)
                if m:
                    data["crypto_maps"].append(m.group(1))

        for key in (
            "local_users",
            "acl_names",
            "zones",
            "zone_pairs",
            "class_maps",
            "policy_maps",
            "isakmp_policies",
            "transform_sets",
            "crypto_maps",
            "tunnel_interfaces",
            "nat_inside_interfaces",
            "nat_outside_interfaces",
        ):
            data[key] = sorted(set(data[key]))

        return data
