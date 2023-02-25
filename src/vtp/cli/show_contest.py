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
import sys

# Local imports
from vtp.core.address import Address
from vtp.core.common import Common
from vtp.ops.show_contests_operation import ShowContestsOperation


def parse_arguments(argv):
    safe_args = Common.cast_thing_to_list(argv)
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
will print the CVRs (Cast Vote Records) for the supplied contest(s)
""",
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
    parsed_args = parser.parse_args(safe_args)

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
    """Entry point for 'show-contest'."""

    args = parse_arguments(sys.argv[1:])
    op = ShowContestsOperation(args)
    op.run()


# If called directly via this file
if __name__ == "__main__":
    main()
