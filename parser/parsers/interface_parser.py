"""
====================================================================
File: interface_parser.py

Project : ConfigVista AI

Purpose
-------
Enterprise Interface Parser (Framework)

Phase 1
-------
✓ Split configuration into interface blocks
✓ Build interface inventory
✓ Parse basic interface information
✓ Modular parser architecture

Future Phases
-------------
Phase 2 : Layer-3
Phase 3 : Layer-2
Phase 4 : Security
Phase 5 : Operational
Phase 6 : QoS
====================================================================
"""

from typing import Dict, List


class InterfaceParser:
    """
    Enterprise Interface Parser

    Phase 1 only builds the framework.
    Future phases extend parser methods without modifying parse().
    """

    def __init__(self, lines: List[str]):

        self.lines = lines

    # ==============================================================
    # Public Entry
    # ==============================================================

    def parse(self) -> List[Dict]:

        interface_blocks = self._split_interfaces()

        interfaces = []

        for block in interface_blocks:

            interface = self._create_interface(block)

            self._parse_basic(block, interface)

            # Future phases

            self._parse_layer3(block, interface)

            self._parse_layer2(block, interface)

            self._parse_security(block, interface)

            self._parse_operational(block, interface)

            self._parse_qos(block, interface)

            interfaces.append(interface)

        return self._finalize(interfaces)

    # ==============================================================
    # Split Configuration
    # ==============================================================

    def _split_interfaces(self):

        blocks = []

        current = []

        inside = False

        for line in self.lines:

            stripped = line.rstrip()

            if stripped.startswith("interface "):

                if current:

                    blocks.append(current)

                current = [stripped]

                inside = True

                continue

            if inside:

                if stripped == "!":

                    blocks.append(current)

                    current = []

                    inside = False

                else:

                    current.append(stripped)

        if current:

            blocks.append(current)

        return blocks

    # ==============================================================
    # Create Interface Object
    # ==============================================================

    def _create_interface(self, block):

        name = block[0].split(None, 1)[1]

        return {

            "name": name,

            "description": "",

            "ip_address": None,

            "subnet_mask": None,

            "shutdown": False,

            "vrf": None,

            "switchport_mode": None,

            "access_vlan": None,

            "voice_vlan": None,

            "native_vlan": None,

            "allowed_vlans": [],

            "channel_group": None,

            "physical": False,

            "loopback": False,

            "svi": False,

            "port_channel": False,

        }

    # ==============================================================
    # Basic Parser
    # ==============================================================

    def _parse_basic(self, block, interface):

        name = interface["name"]

        interface["physical"] = (
            not name.startswith("Loopback")
            and not name.startswith("Vlan")
            and not name.startswith("Port-channel")
        )

        interface["loopback"] = name.startswith("Loopback")

        interface["svi"] = name.startswith("Vlan")

        interface["port_channel"] = name.startswith("Port-channel")

        for line in block[1:]:

            line = line.strip()

            if line.startswith("description "):

                interface["description"] = line[12:]

            elif line == "shutdown":

                interface["shutdown"] = True

    # ==============================================================
    # Phase 2 Placeholder
    # ==============================================================

    def _parse_layer3(self, block, interface):

        pass

    # ==============================================================
    # Phase 3 Placeholder
    # ==============================================================

    def _parse_layer2(self, block, interface):

        pass

    # ==============================================================
    # Phase 4 Placeholder
    # ==============================================================

    def _parse_security(self, block, interface):

        pass

    # ==============================================================
    # Phase 5 Placeholder
    # ==============================================================

    def _parse_operational(self, block, interface):

        pass

    # ==============================================================
    # Phase 6 Placeholder
    # ==============================================================

    def _parse_qos(self, block, interface):

        pass

    # ==============================================================
    # Final Processing
    # ==============================================================

    def _finalize(self, interfaces):

        interfaces.sort(key=lambda x: x["name"])

        return interfaces