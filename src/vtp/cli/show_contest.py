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

"""Command line level script to automatically cast a ballot.

See 'show_contest.py -h' for usage information.
"""

# Standard imports
import argparse
import re
import sys

# Local imports
from vtp.core.common import Common
from vtp.ops.show_contests_operation import ShowContestsOperation


def parse_arguments(argv):
    """Parse arguments from a command line or from the constructor"""

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
will print the CVRs (Cast Vote Records) for the supplied contest(s)
""",
    )
    Common.add_election_data_dir(parser)
    parser.add_argument(
        "-c",
        "--contest-check",
        help="a comma separate list of contests digests to validate/display",
    )

    Common.add_verbosity(parser)
    Common.add_printonly(parser)
    parsed_args = parser.parse_args(argv)

    # Validate required args
    if not parsed_args.contest_check:
        raise ValueError("The contest check is required")
    if not bool(re.match("^[0-9a-f,]", parsed_args.contest_check)):
        raise ValueError(
            "The contest_check parameter only accepts a comma separated (no spaces) "
            "list of contest checks/digests to track."
        )
    return parsed_args

def main():
    """
    Called via a python local install entrypoint or by running this
    file.  Simply wraps the scripts constructor and calls the run
    method.  See the script's help output or read the
    vtp.ops.show_contests_operation.py (argparse) description in the
    source file.
    """

    # Parse args
    parsed_args = parse_arguments(sys.argv)

    # do it
    sco = ShowContestsOperation(
        parsed_args.election_data_dir,
        parsed_args.verbosity,
        parsed_args.printonly)
    sco.run(
        contest_check=parsed_args.contest_check,
        )


# If called directly via this file
if __name__ == "__main__":
    main()
