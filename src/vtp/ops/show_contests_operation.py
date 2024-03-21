#!/usr/bin/env python

#  VoteTrackerPlus
#   Copyright (C) 2022 Sandy Currier
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program; if not, write to the Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""Logic of operation for showing contests."""

# Standard imports

# Project imports
from vtp.core.election_config import ElectionConfig

# Local imports
from .operation import Operation


class ShowContestsOperation(Operation):
    """
    A class to implememt the show-contests operation.  See the
    show-contests help output or read the parse_argument argparse
    description (immediately below this) in the source file.
    """

    def validate_digests(self, digests, the_election_config, error_digests):
        """Will scan the supplied digests for validity.  Will print and
        return the invalid digests.
        """
        errors = 0
        input_data = "\n".join(digests.split(",")) + "\n"
        with self.changed_cwd(the_election_config.get("git_rootdir")):
            output_lines = (
                self.shell_out(
                    [
                        "git",
                        "cat-file",
                        "--batch-check=%(objectname) %(objecttype)",
                        "--buffer",
                    ],
                    printonly_override=True,
                    input=input_data,
                    text=True,
                    check=True,
                    capture_output=True,
                )
                .stdout.strip()
                .splitlines()
            )
        for count, line in enumerate(output_lines):
            digest, commit_type = line.split()
            if commit_type == "missing":
                self.imprimir(f"missing digest: n={count} digest={digest}", 1)
                error_digests.add(digest)
                errors += 1
            elif commit_type != "commit":
                self.imprimir(
                    f"invalid digest type: n={count} digest={digest} type={commit_type}",
                    1,
                )
                error_digests.add(digest)
                errors += 1
        if errors:
            raise ValueError(f"Found {errors} invalid digest(s)")

    # pylint: disable=duplicate-code
    def run(self, contest_check: str = "") -> list:
        """Main function - see -h for more info"""

        # Create a VTP ElectionData object if one does not already exist
        the_election_config = ElectionConfig.configure_election(
            self, self.election_data_dir
        )

        # First validate the digests
        error_digests = set()
        self.validate_digests(contest_check, the_election_config, error_digests)
        valid_digests = [
            digest for digest in contest_check.split(",") if digest not in error_digests
        ]
        # show/log the digests
        with self.changed_cwd(the_election_config.get("git_rootdir")):
            output_lines = (
                self.shell_out(
                    ["git", "show", "-s"] + valid_digests,
                    printonly_override=True,
                    text=True,
                    check=True,
                    capture_output=True,
                )
                .stdout.strip()
                .splitlines()
            )
        if self.stdout_printing:
            for line in output_lines:
                self.imprimir(line)
        return output_lines


# For future reference just in case . . .
# this is a loop of shell commands
#        for digest in contest_check.split(','):
#            if digest not in error_digests:
#                self.shell_out(
#                    ['git', 'log', '-1', digest],
#                    printonly_override=True,
#                    check=True)

# this does not work well enough either
#        input_data = '\n'.join(contest_check.split(',')) + '\n'
#        self.shell_out(
#            ['git', 'cat-file', '--batch=%(objectname)'],
#            printonly_override=True,
#            input=input_data,
#            text=True,
#            check=True)

# EOF
