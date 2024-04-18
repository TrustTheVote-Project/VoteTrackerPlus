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
import os

# Project imports
from vtp.core.election_config import ElectionConfig
from vtp.core.webapi import WebAPI

# Local imports
from .operation import Operation


class ShowContestsOperation(Operation):
    """
    A class to implememt the show-contests operation.  See the
    show-contests help output or read the parse_argument argparse
    description (immediately below this) in the source file.
    """

    def validate_digests(
        self,
        digests: str,
        the_election_config: dict,
        error_digests: set,
        webapi: bool = False,
    ):
        """Will scan the supplied digests for validity.  Will print and
        return the invalid digests.
        """
        errors = 0
        json_errors = []
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
                    incoming_printlevel=5,
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
                if webapi:
                    json_errors.append(f"missing digest: n={count} digest={digest}")
                else:
                    self.imprimir(f"missing digest: n={count} digest={digest}", 1)
                error_digests.add(digest)
                errors += 1
            elif commit_type != "commit":
                if webapi:
                    json_errors.append(
                        f"invalid digest type: n={count} digest={digest} type={commit_type}"
                    )
                else:
                    self.imprimir(
                        f"invalid digest type: n={count} digest={digest} type={commit_type}",
                        1,
                    )
                error_digests.add(digest)
                errors += 1
        if errors:
            if webapi:
                json_errors.append(f"Summary: found {errors} invalid digest(s)")
            else:
                self.imprimir(
                    f"Summary: found {errors} invalid digest(s)",
                    1,
                )
        return json_errors

    # pylint: disable=duplicate-code
    def run(
        self, contest_check: str = "", webapi: bool = False, receipt: bool = False
    ) -> dict:
        """
        Main function - see -h for more info.  If receipt is True,
        contest_check is interpreted as the commit digest of versioned
        ballot receipt in which case the contents of the the versioned
        file is returned.
        """

        # Create a VTP ElectionData object if one does not already exist
        the_election_config = ElectionConfig.configure_election(
            self, self.election_data_dir
        )

        # First validate the digests
        error_digests = set()
        json_errors = self.validate_digests(
            contest_check, the_election_config, error_digests, webapi
        )
        valid_digests = [
            digest for digest in contest_check.split(",") if digest not in error_digests
        ]
        if not receipt:
            # show/log the digests
            with self.changed_cwd(the_election_config.get("git_rootdir")):
                output_lines = (
                    self.shell_out(
                        ["git", "show", "-s"] + valid_digests,
                        incoming_printlevel=5,
                        text=True,
                        check=True,
                        capture_output=True,
                    )
                    .stdout.strip()
                    .splitlines()
                )
            for line in output_lines:
                self.imprimir(line)
            # return a dictionary
            return WebAPI.convert_git_log_to_json(output_lines, json_errors)
        # get the contents of the file via the commit digest.
        # This appears to require two git commands TBD
        receipt_digest = valid_digests[0]
        with self.changed_cwd(the_election_config.get("git_rootdir")):
            # get the filename
            output_lines = (
                self.shell_out(
                    ["git", "show", "--name-only", "--oneline", receipt_digest],
                    incoming_printlevel=5,
                    text=True,
                    check=True,
                    capture_output=True,
                )
                .stdout.strip()
                .splitlines()
            )
            # minimal error checking
            if len(output_lines) != 2:
                json_errors.append(
                    "invalid 'git show ...' results - did not return 2 lines"
                )
            elif os.path.basename(output_lines[1]) != "receipt.csv":
                json_errors.append("'git show ...' did not return a receipt.csv file")
            else:
                # get the contents
                ballot_check = (
                    self.shell_out(
                        ["git", "show", receipt_digest + ":" + output_lines[1]],
                        incoming_printlevel=5,
                        text=True,
                        check=True,
                        capture_output=True,
                    )
                    .stdout.strip()
                    .splitlines()
                )
        # convert this to an array of arrays
        # import pdb; pdb.set_trace()
        return {
            "ballot_check": WebAPI.convert_csv_to_2d_list(ballot_check),
            "backend_errors": json_errors,
        }


# For future reference just in case . . .
# this is a loop of shell commands
#        for digest in contest_check.split(','):
#            if digest not in error_digests:
#                self.shell_out(
#                    ['git', 'log', '-1', digest],
#                    incoming_printlevel=5,
#                    check=True)

# this does not work well enough either
#        input_data = '\n'.join(contest_check.split(',')) + '\n'
#        self.shell_out(
#            ['git', 'cat-file', '--batch=%(objectname)'],
#            incoming_printlevel=5,
#            input=input_data,
#            text=True,
#            check=True)

# EOF
