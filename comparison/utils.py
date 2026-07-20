"""
comparison/utils.py

Utility functions for the Configuration Comparison Framework.

Enhancements
------------
- Removes parser artifacts (end, ^)
- Collapses banner motd into a logical block
- Preserves indentation
- Provides improved parent section mapping
- Backward compatible with existing DiffEngine,
  ChangeClassifier and ComparisonEngine.

Author : Shivam Saxena
Project : ConfigVista AI
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List


# ==========================================================
# INTERNAL CONSTANTS
# ==========================================================

IGNORED_COMMANDS = {
    "end",
}

BANNER_START_PATTERN = re.compile(
    r"^banner\s+\S+\s+\^$",
    re.IGNORECASE,
)


# ==========================================================
# FILE OPERATIONS
# ==========================================================

def read_configuration(file_path: str) -> List[str]:
    """
    Read a configuration file and return a normalized list
    of configuration lines.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {file_path}"
        )

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:

        lines = file.readlines()

    return normalize_configuration(lines)


# ==========================================================
# NORMALIZATION
# ==========================================================

def normalize_configuration(
    lines: List[str],
) -> List[str]:
    """
    Normalize Cisco configuration.

    Processing performed

    • remove blank lines
    • remove comments (!)
    • remove 'end'
    • remove standalone '^'
    • collapse banner blocks
    • normalize whitespace
    • preserve indentation
    """

    normalized: List[str] = []

    inside_banner = False
    banner_parent = ""
    banner_lines: List[str] = []

    for raw_line in lines:

        line = raw_line.rstrip("\n").rstrip("\r")

        stripped = line.strip()

        # --------------------------------------------
        # Ignore blank lines
        # --------------------------------------------

        if not stripped:
            continue

        # --------------------------------------------
        # Ignore comments
        # --------------------------------------------

        if stripped.startswith("!"):
            continue

        # --------------------------------------------
        # Ignore parser artifacts
        # --------------------------------------------

        if stripped.lower() in IGNORED_COMMANDS:
            continue

        # --------------------------------------------
        # Banner start
        #
        # Example
        #
        # banner motd ^
        # *****************
        # Authorized
        # *****************
        # ^
        # --------------------------------------------

        if not inside_banner and BANNER_START_PATTERN.match(stripped):

            inside_banner = True

            banner_parent = stripped[:-1].strip()

            normalized.append(banner_parent)

            banner_lines = []

            continue

        # --------------------------------------------
        # Banner body
        # --------------------------------------------

        if inside_banner:

            if stripped == "^":

                inside_banner = False

                if banner_lines:

                    banner_text = " ".join(
                        x.strip()
                        for x in banner_lines
                        if x.strip()
                    )

                    if banner_text:

                        normalized.append(
                            " " + banner_text
                        )

                banner_parent = ""
                banner_lines = []

                continue

            banner_lines.append(stripped)

            continue

        # --------------------------------------------
        # Ignore standalone ^
        # --------------------------------------------

        if stripped == "^":
            continue

        # --------------------------------------------
        # Preserve indentation
        # --------------------------------------------

        leading_spaces = len(line) - len(line.lstrip())

        content = re.sub(
            r"\s+",
            " ",
            stripped,
        )

        normalized.append(
            (" " * leading_spaces) + content
        )

    return normalized


def normalize_line(
    line: str,
) -> str:
    """
    Normalize a single configuration line.

    Used throughout the comparison engine.
    """

    return re.sub(
        r"\s+",
        " ",
        line.strip(),
    )
# ==========================================================
# HOSTNAME
# ==========================================================

def find_hostname(
    lines: List[str],
) -> str:
    """
    Extract hostname from configuration.

    Returns
    -------
    Hostname if present, otherwise "Unknown".
    """

    for line in lines:

        stripped = line.strip()

        if stripped.lower().startswith("hostname "):

            parts = stripped.split(maxsplit=1)

            if len(parts) == 2:
                return parts[1]

    return "Unknown"


# ==========================================================
# INDENTATION
# ==========================================================

def indentation_level(
    line: str,
) -> int:
    """
    Return indentation level.

    Parent commands have zero indentation.
    Child commands begin with one or more spaces.
    """

    return len(line) - len(line.lstrip())


def is_parent_command(
    line: str,
) -> bool:
    """
    Determine whether a line represents a parent command.

    Examples
    --------
    interface GigabitEthernet0/0

    router ospf 1

    ip access-list standard MGMT

    banner motd

    vlan 100

    line vty 0 4
    """

    return indentation_level(line) == 0


# ==========================================================
# SECTION EXTRACTION
# ==========================================================

def split_configuration(
    lines: List[str],
) -> List[List[str]]:
    """
    Split configuration into logical parent sections.

    Each returned block contains

        Parent command
            Child command
            Child command

    Banner blocks are already normalized by
    normalize_configuration(), therefore they naturally become

        banner motd
         Authorized Access Only
    """

    sections: List[List[str]] = []

    current_section: List[str] = []

    for line in lines:

        if is_parent_command(line):

            if current_section:
                sections.append(current_section)

            current_section = [line]

        else:

            if not current_section:
                current_section = [line]
            else:
                current_section.append(line)

    if current_section:
        sections.append(current_section)

    return sections


def build_section_map(
    lines: List[str],
) -> Dict[int, str]:
    """
    Build mapping

        line_number -> parent_section

    Example

        interface GigabitEthernet0/0
         description WAN
         ip address ...

    becomes

        1 -> interface GigabitEthernet0/0
        2 -> interface GigabitEthernet0/0
        3 -> interface GigabitEthernet0/0

    Banner blocks also map correctly

        banner motd
         Authorized Access Only

        20 -> banner motd
        21 -> banner motd
    """

    section_map: Dict[int, str] = {}

    current_parent = ""

    for line_number, line in enumerate(lines, start=1):

        if is_parent_command(line):

            current_parent = normalize_line(line)

        section_map[line_number] = current_parent

    return section_map


def parent_type(
    parent_section: str,
) -> str:
    """
    Return a richer parent type for downstream
    classification and ML feature extraction.

    Examples

    interface Gig0/0
        -> interface

    router ospf 1
        -> ospf

    router bgp 65000
        -> bgp

    ip access-list standard MGMT
        -> acl

    ip route ...
        -> static_route

    ntp server ...
        -> ntp

    logging host ...
        -> logging

    snmp-server ...
        -> snmp

    banner motd
        -> banner
    """

    if not parent_section:
        return ""

    text = parent_section.lower()

    if text.startswith("interface"):
        return "interface"

    if text.startswith("router ospf"):
        return "ospf"

    if text.startswith("router bgp"):
        return "bgp"

    if text.startswith("router eigrp"):
        return "eigrp"

    if text.startswith("router rip"):
        return "rip"

    if text.startswith("ip access-list"):
        return "acl"

    if text.startswith("ip route"):
        return "static_route"

    if text.startswith("vlan"):
        return "vlan"

    if text.startswith("line vty"):
        return "line_vty"

    if text.startswith("hostname"):
        return "hostname"

    if text.startswith("banner"):
        return "banner"

    if text.startswith("logging"):
        return "logging"

    if text.startswith("ntp"):
        return "ntp"

    if text.startswith("snmp-server"):
        return "snmp"

    if text.startswith("service"):
        return "service"

    return parent_section.split()[0].lower()

# ==========================================================
# SEARCH HELPERS
# ==========================================================

def contains_keyword(
    line: str,
    keyword: str,
) -> bool:
    """
    Case-insensitive keyword search.

    Parameters
    ----------
    line : str
        Configuration line.

    keyword : str
        Keyword to search.

    Returns
    -------
    bool
    """

    if not keyword:
        return False

    return keyword.lower() in line.lower()


def find_lines(
    lines: List[str],
    keyword: str,
) -> List[str]:
    """
    Return all configuration lines containing a keyword.
    """

    return [
        line
        for line in lines
        if contains_keyword(line, keyword)
    ]


# ==========================================================
# COMPARISON HELPERS
# ==========================================================

def lines_equal(
    line1: str,
    line2: str,
) -> bool:
    """
    Compare two configuration lines after normalization.

    Whitespace differences are ignored.
    """

    return normalize_line(line1) == normalize_line(line2)


def block_to_string(
    block: List[str],
) -> str:
    """
    Convert a configuration block into a printable string.
    """

    if not block:
        return ""

    return "\n".join(block)


def is_same_parent(
    parent1: str,
    parent2: str,
) -> bool:
    """
    Compare parent sections.

    Used by the DiffEngine when deciding whether a change
    belongs to an existing section or represents a new one.
    """

    return normalize_line(parent1) == normalize_line(parent2)


def section_name(
    line: str,
) -> str:
    """
    Return a normalized section name.

    Example

        interface GigabitEthernet0/0

    becomes

        interface GigabitEthernet0/0
    """

    return normalize_line(line)


# ==========================================================
# MISC HELPERS
# ==========================================================

def safe_value(
    value: str | None,
) -> str:
    """
    Convert None into an empty string.
    """

    return value or ""


def unique_sorted(
    items: List[str],
) -> List[str]:
    """
    Return unique sorted values while ignoring blanks.
    """

    return sorted(
        {
            item
            for item in items
            if item
        }
    )


def first_non_empty(
    *values: str,
) -> str:
    """
    Return the first non-empty value.

    Useful when old/new values are optional.
    """

    for value in values:

        if value and value.strip():

            return value

    return ""


def clean_text(
    text: str,
) -> str:
    """
    Normalize arbitrary text.

    Used for comparisons and report generation.
    """

    return normalize_line(text)


def flatten_sections(
    sections: List[List[str]],
) -> List[str]:
    """
    Convert a list of configuration blocks back into
    a single list of configuration lines.

    Example

    [
        [
            "interface Gig0/0",
            " ip address ..."
        ],
        [
            "router ospf 1",
            " network ..."
        ]
    ]

    becomes

    [
        "interface Gig0/0",
        " ip address ...",
        "router ospf 1",
        " network ..."
    ]
    """

    flattened: List[str] = []

    for block in sections:

        flattened.extend(block)

    return flattened