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

"""Command line script to automatically cast a ballot.

Run with '--help' for usage information.
"""

# Standard imports
import argparse
import re

# Project imports
from vtp.ops.show_contests_operation import ShowContestsOperation

# Local imports
from ._arguments import Arguments


def parse_arguments():
    """Parse arguments from a command line or from the constructor"""

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
will print the CVRs (Cast Vote Records) for the supplied contest(s)
""",
    )
    Arguments.add_election_data_dir(parser)
    parser.add_argument(
        "-c",
        "--contest-check",
        help="a comma separate list of contests digests to validate/display",
    )

    Arguments.add_verbosity(parser)
    Arguments.add_printonly(parser)
    parsed_args = parser.parse_args()

    # Validate required args
    if not parsed_args.contest_check:
        raise ValueError("The contest check is required")
    if not bool(re.match("^[0-9a-f,]", parsed_args.contest_check)):
        raise ValueError(
            "The contest_check parameter only accepts a comma separated (no spaces) "
            "list of contest checks/digests to track."
        )
    return parsed_args


# pylint: disable=duplicate-code
def main():
    """Entry point for 'show-contests'."""

    # Parse args
    parsed_args = parse_arguments()

    # do it
    sco = ShowContestsOperation(
        election_data_dir=parsed_args.election_data_dir,
        verbosity=parsed_args.verbosity,
        printonly=parsed_args.printonly,
    )
    sco.run(
        contest_check=parsed_args.contest_check,
    )


# If called directly via this file
if __name__ == "__main__":
    main()
