"""
====================================================================
File: base_parser.py

Project : ConfigVista AI

Purpose
-------
Base class for all parser modules.

Provides common helper methods for navigating
Cisco configuration files.

====================================================================
"""

from typing import List, Optional

from parser.parsers.parser_utils import (
    clean_line,
    is_blank,
    is_comment
)


class BaseParser:
    """
    Base parser providing common utilities.
    """

    def __init__(self, lines: List[str]):

        self.lines = lines

        self.index = 0

    # ==========================================================
    # Navigation
    # ==========================================================

    def has_next(self) -> bool:

        return self.index < len(self.lines)

    def current(self) -> str:

        if self.has_next():

            return clean_line(
                self.lines[self.index]
            )

        return ""

    def next(self) -> str:

        self.index += 1

        return self.current()

    def peek(self) -> str:

        if self.index + 1 < len(self.lines):

            return clean_line(
                self.lines[self.index + 1]
            )

        return ""

    # ==========================================================
    # Helpers
    # ==========================================================

    def skip(self):

        self.index += 1

    def reset(self):

        self.index = 0

    def eof(self) -> bool:

        return self.index >= len(self.lines)

    def is_blank(self) -> bool:

        return is_blank(
            self.current()
        )

    def is_comment(self) -> bool:

        return is_comment(
            self.current()
        )

    # ==========================================================
    # Search
    # ==========================================================

    def find(self, prefix: str) -> Optional[int]:
        """
        Find first line beginning with prefix.
        """

        for i, line in enumerate(self.lines):

            if clean_line(line).startswith(prefix):

                return i

        return None