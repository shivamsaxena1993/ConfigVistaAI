"""
====================================================================
File: parser_utils.py

Project : ConfigVista AI

Purpose
-------
Common utility functions used by all parser modules.

====================================================================
"""

import ipaddress
from typing import List, Optional


# ==============================================================
# Line Helpers
# ==============================================================

def clean_line(line: str) -> str:
    """
    Remove leading/trailing whitespace.
    """

    return line.strip()


def is_blank(line: str) -> bool:
    """
    Check if line is empty.
    """

    return not line.strip()


def is_comment(line: str) -> bool:
    """
    Cisco comment line.
    """

    return line.strip().startswith("!")


# ==============================================================
# Token Helpers
# ==============================================================

def tokens(line: str) -> List[str]:
    """
    Split configuration line.
    """

    return line.strip().split()


def first_token(line: str) -> str:
    """
    Return first token.
    """

    parts = tokens(line)

    return parts[0] if parts else ""


# ==============================================================
# Prefix Matching
# ==============================================================

def starts_with(line: str, prefix: str) -> bool:
    """
    Safe startswith().
    """

    return line.strip().startswith(prefix)


# ==============================================================
# Interface Helpers
# ==============================================================

def is_interface(line: str) -> bool:

    return starts_with(line, "interface ")


def interface_name(line: str) -> Optional[str]:

    parts = tokens(line)

    if len(parts) >= 2:

        return parts[1]

    return None


# ==============================================================
# IP Helpers
# ==============================================================

def is_ip(value: str) -> bool:
    """
    Validate IPv4 address.
    """

    try:

        ipaddress.ip_address(value)

        return True

    except ValueError:

        return False


# ==============================================================
# List Helpers
# ==============================================================

def unique_append(items: List, value):
    """
    Append only if value not already present.
    """

    if value not in items:

        items.append(value)


# ==============================================================
# Boolean Helpers
# ==============================================================

def to_bool(value) -> bool:

    return bool(value)