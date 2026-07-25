"""
comparison/diff_engine.py

Context-aware configuration difference engine.

Enhancements
------------
- Better Added / Removed detection
- Improved Replace handling
- Preserves configuration hierarchy
- Backward compatible with ConfigVista AI

Author : Shivam Saxena
Project : ConfigVista AI
"""

from __future__ import annotations

from difflib import SequenceMatcher
from typing import List

from comparison.models import (
    ChangeType,
    ConfigurationChange,
)

from comparison.utils import (
    build_section_map,
    normalize_configuration,
    parent_type,
)


class DiffEngine:
    """
    Context-aware configuration comparison engine.

    The engine performs line-by-line comparison while
    preserving parent configuration hierarchy.

    SequenceMatcher opcodes are interpreted as

        equal
            ignored

        insert
            Added

        delete
            Removed

        replace
            Smart comparison that separates

                Modified
                Added
                Removed

    rather than converting everything into Modified.
    """

    # ======================================================
    # INTERNAL HELPERS
    # ======================================================

    def _create_change(
        self,
        *,
        change_type: ChangeType,
        line_number: int,
        old_value: str = "",
        new_value: str = "",
        parent: str = "",
    ) -> ConfigurationChange:
        """
        Build a ConfigurationChange object.
        """

        return ConfigurationChange(
            change_type=change_type,
            line_number=line_number,
            old_value=old_value,
            new_value=new_value,
            parent_section=parent,
            parent_type=parent_type(parent),
            section=parent,
        )

    # ------------------------------------------------------

    @staticmethod
    def _is_blank(value: str) -> bool:
        """
        True if value is empty.
        """

        return not value.strip()

    # ------------------------------------------------------

    @staticmethod
    def _same_parent(
        baseline_parent: str,
        candidate_parent: str,
    ) -> bool:
        """
        Compare parent sections.

        Parent equality is used to determine whether a
        replacement is likely to be a modification or
        whether it represents an insertion/deletion.
        """

        return (
            baseline_parent.strip().lower()
            ==
            candidate_parent.strip().lower()
        )

    @staticmethod
    def _same_command(old_line: str, new_line: str) -> bool:
        """
        Returns True when two configuration lines
        represent the same IOS command with different
        parameter values.
        """

        old_line = old_line.strip().lower()
        new_line = new_line.strip().lower()

        COMMAND_PREFIXES = [

            "version",

            "hostname",

            "description",

            "ip address",

            "ip helper-address",

            "logging buffered",

            "logging host",

            "ntp server",

            "snmp-server community",

            "service-policy input",

            "service-policy output",

            "router-id",

            "network",

            "passive-interface",

            "duplex",

            "speed",

            "shutdown",

            "no shutdown",

        ]

        for prefix in COMMAND_PREFIXES:

            if (
                old_line.startswith(prefix)
                and
                new_line.startswith(prefix)
            ):
                return True

        return False
    
    
    # ------------------------------------------------------

    @staticmethod
    def _is_parent_command(
        line: str,
    ) -> bool:
        """
        Parent commands have no indentation.

        Examples

            interface Gig0/0

            router ospf 1

            vlan 100

            banner motd
        """

        return line and not line.startswith(" ")

    # ======================================================
    # MAIN COMPARISON
    # ======================================================

    def compare(
        self,
        baseline: List[str],
        candidate: List[str],
    ) -> List[ConfigurationChange]:
        """
        Compare two configurations.

        Returns
        -------
        List[ConfigurationChange]
        """

        baseline = normalize_configuration(
            baseline
        )

        candidate = normalize_configuration(
            candidate
        )

        baseline=[
        x
        for x in baseline
        if not x.strip().startswith("!")
        ]
        
        candidate=[
        x
        for x in candidate
        if not x.strip().startswith("!")
        ]
        
        baseline_sections = build_section_map(
            baseline
        )

        candidate_sections = build_section_map(
            candidate
        )

        matcher = SequenceMatcher(
            None,
            baseline,
            candidate,
        )

        changes: List[
            ConfigurationChange
        ] = []

        # --------------------------------------------------
        # Process SequenceMatcher operations
        # --------------------------------------------------

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():

            # ==================================================
            # EQUAL
            # ==================================================

            if tag == "equal":
                continue

            # ==================================================
            # DELETE
            # ==================================================

            if tag == "delete":

                for index in range(i1, i2):
                
                    parent = baseline_sections.get(
                        index + 1,
                        "",
                    )

                    changes.append(
                        self._create_change(
                            change_type=ChangeType.REMOVED,
                            line_number=index + 1,
                            old_value=baseline[index],
                            parent=parent,
                        )
                    )

                continue

            # ==================================================
            # INSERT
            # ==================================================

            if tag == "insert":

                for index in range(j1, j2):

                    parent = candidate_sections.get(
                        index + 1,
                        "",
                    )

                    changes.append(
                        self._create_change(
                            change_type=ChangeType.ADDED,
                            line_number=index + 1,
                            new_value=candidate[index],
                            parent=parent,
                        )
                    )

                continue

            # ==================================================
            # REPLACE
            #
            # SequenceMatcher frequently groups
            #
            # delete + insert
            #
            # into a replace block.
            #
            # This logic attempts to recover the
            # intended operation.
            # ==================================================

            # ==================================================
            # REPLACE
            # ==================================================

            if tag == "replace":
            
                old_lines = baseline[i1:i2]
                new_lines = candidate[j1:j2]

                common = min(len(old_lines), len(new_lines))

                #
                # Compare matching positions
                #

                for offset in range(common):
                
                    old_line = old_lines[offset]
                    new_line = new_lines[offset]

                    baseline_parent = baseline_sections.get(
                        i1 + offset + 1,
                        ""
                    )

                    candidate_parent = candidate_sections.get(
                        j1 + offset + 1,
                        ""
                    )

                    parent = (
                        candidate_parent
                        if candidate_parent
                        else baseline_parent
                    )

                    #
                    # Ignore identical lines
                    #

                    if old_line.strip() == new_line.strip():
                        continue
                    
                    #
                    # FIRST
                    # Same command -> Modified
                    #

                    if self._same_command(old_line, new_line):
                    
                        changes.append(
                            self._create_change(
                                change_type=ChangeType.MODIFIED,
                                line_number=i1 + offset + 1,
                                old_value=old_line,
                                new_value=new_line,
                                parent=parent,
                            )
                        )

                        continue
                    
                    #
                    # SECOND
                    # Different commands
                    #

                    changes.append(
                        self._create_change(
                            change_type=ChangeType.REMOVED,
                            line_number=i1 + offset + 1,
                            old_value=old_line,
                            parent=baseline_parent,
                        )
                    )

                    changes.append(
                        self._create_change(
                            change_type=ChangeType.ADDED,
                            line_number=j1 + offset + 1,
                            new_value=new_line,
                            parent=candidate_parent,
                        )
                    )

                #
                # Remaining old lines
                #

                for offset in range(common, len(old_lines)):
                
                    parent = baseline_sections.get(
                        i1 + offset + 1,
                        ""
                    )

                    changes.append(
                        self._create_change(
                            change_type=ChangeType.REMOVED,
                            line_number=i1 + offset + 1,
                            old_value=old_lines[offset],
                            parent=parent,
                        )
                    )

                #
                # Remaining new lines
                #

                for offset in range(common, len(new_lines)):
                
                    parent = candidate_sections.get(
                        j1 + offset + 1,
                        ""
                    )

                    changes.append(
                        self._create_change(
                            change_type=ChangeType.ADDED,
                            line_number=j1 + offset + 1,
                            new_value=new_lines[offset],
                            parent=parent,
                        )
                    )

                continue
        
        return changes
    # ======================================================
    # FILE COMPARISON
    # ======================================================

    def compare_files(
        self,
        baseline_file: str,
        candidate_file: str,
    ) -> List[ConfigurationChange]:
        """
        Compare two configuration files.

        Parameters
        ----------
        baseline_file : str
            Baseline configuration file.

        candidate_file : str
            Candidate configuration file.

        Returns
        -------
        List[ConfigurationChange]
        """

        with open(
            baseline_file,
            "r",
            encoding="utf-8",
        ) as file:

            baseline = file.readlines()

        with open(
            candidate_file,
            "r",
            encoding="utf-8",
        ) as file:

            candidate = file.readlines()

        return self.compare(
            baseline,
            candidate,
        )

    # ======================================================
    # DEBUG HELPERS
    # ======================================================

    @staticmethod
    def summarize_changes(
        changes: List[ConfigurationChange],
    ) -> dict:
        """
        Return a quick summary of detected changes.

        Useful for debugging and unit tests.
        """

        summary = {
            "added": 0,
            "removed": 0,
            "modified": 0,
        }

        for change in changes:

            if change.change_type == ChangeType.ADDED:
                summary["added"] += 1

            elif change.change_type == ChangeType.REMOVED:
                summary["removed"] += 1

            elif change.change_type == ChangeType.MODIFIED:
                summary["modified"] += 1

        summary["total"] = (
            summary["added"]
            + summary["removed"]
            + summary["modified"]
        )

        return summary

    # ------------------------------------------------------

    @staticmethod
    def print_summary(
        changes: List[ConfigurationChange],
    ) -> None:
        """
        Convenience function for debugging.
        """

        summary = DiffEngine.summarize_changes(
            changes
        )

        print("=" * 60)
        print("Diff Summary")
        print("=" * 60)

        print(
            f"Added    : {summary['added']}"
        )

        print(
            f"Removed  : {summary['removed']}"
        )

        print(
            f"Modified : {summary['modified']}"
        )

        print(
            f"Total    : {summary['total']}"
        )

        print("=" * 60)