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

"""show_contest.py - command line level test script to automatically cast a ballot.

See './show_contest.py -h' for usage information.

See ../../docs/tech/executable-overview.md for the context in which this file was created.

"""

import argparse
import logging

# pylint: disable=wrong-import-position
import os
import re
import sys

# Local imports
from vtp.utils.common import Globals, Shellout
from vtp.utils.election_config import ElectionConfig

################
# Functions
################


def validate_digests(digests, election_data_dir, error_digests):
    """Will scan the supplied digests for validity.  Will print and
    return the invalid digests.
    """
    errors = 0
    input_data = "\n".join(digests.split(",")) + "\n"
    with Shellout.changed_cwd(election_data_dir):
        output_lines = (
            Shellout.run(
                [
                    "git",
                    "cat-file",
                    "--batch-check=%(objectname) %(objecttype)",
                    "--buffer",
                ],
                verbosity=ARGS.verbosity,
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
            logging.error("[ERROR]: missing digest: n=%s digest=%s", count, digest)
            error_digests.add(digest)
            errors += 1
        elif commit_type != "commit":
            logging.error(
                "[ERROR]: invalid digest type: n=%s digest=%s type=%s",
                count,
                digest,
                commit_type,
            )
            error_digests.add(digest)
            errors += 1
    if errors:
        raise ValueError(f"Found {errors} invalid digest(s)")


################
# arg parsing
################
# pylint: disable=duplicate-code
def parse_arguments():
    """Parse command line arguments"""

    parser = argparse.ArgumentParser(
        description="""will print the CVRs (Cast Vote Records) for the
                    supplied contest(s)
                    """
    )

    parser.add_argument(
        "-c",
        "--contest-check",
        help="a comma separate list of contests digests to validate/display",
    )
    parser.add_argument(
        "-v",
        "--verbosity",
        type=int,
        default=3,
        help="0 critical, 1 error, 2 warning, 3 info, 4 debug (def=3)",
    )
    parser.add_argument(
        "-n",
        "--printonly",
        action="store_true",
        help="will printonly and not write to disk (def=True)",
    )
    parsed_args = parser.parse_args()
    verbose = {
        0: logging.CRITICAL,
        1: logging.ERROR,
        2: logging.WARNING,
        3: logging.INFO,
        4: logging.DEBUG,
    }
    logging.basicConfig(
        format="%(message)s", level=verbose[parsed_args.verbosity], stream=sys.stdout
    )
    # Validate required args
    if not parsed_args.contest_check:
        raise ValueError("The contest check is required")
    if not bool(re.match("^[0-9a-f,]", parsed_args.contest_check)):
        raise ValueError(
            "The contest_check parameter only accepts a comma separated (no spaces) "
            "list of contest checks/digests to track."
        )
    return parsed_args


################
# main
################

ARGS = None

# pylint: disable=duplicate-code
def main():
    """Main function - see -h for more info"""

    # pylint: disable=global-statement
    global ARGS
    ARGS = parse_arguments()

    # Check the ElectionData
    the_election_config = ElectionConfig()
    the_election_config.parse_configs()
    election_data_dir = os.path.join(
        the_election_config.get("git_rootdir"), Globals.get("ROOT_ELECTION_DATA_SUBDIR")
    )

    # First validate the digests
    error_digests = set()
    validate_digests(ARGS.contest_check, election_data_dir, error_digests)
    valid_digests = [
        digest
        for digest in ARGS.contest_check.split(",")
        if digest not in error_digests
    ]
    # show/log the digests
    with Shellout.changed_cwd(election_data_dir):
        Shellout.run(["git", "show", "-s"] + valid_digests, check=True)


# this is a loop of shell commands
#        for digest in ARGS.contest_check.split(','):
#            if digest not in error_digests:
#                Shellout.run(['git', 'log', '-1', digest], check=True)

# this does not work well enough either
#        input_data = '\n'.join(ARGS.contest_check.split(',')) + '\n'
#        Shellout.run(
#            ['git', 'cat-file', '--batch=%(objectname)'],
#            input=input_data,
#            text=True,
#            check=True,
#            verbosity=ARGS.verbosity)

if __name__ == "__main__":
    main()

# EOF
