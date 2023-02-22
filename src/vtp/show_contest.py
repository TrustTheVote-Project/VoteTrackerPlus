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

from vtp.ops.show_contests_operation import ShowContestsOperation


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
    """
    Called via a python local install entrypoint or this file.  Simply
    wraps the scripts constructor, creates and ElectionConfig instance
    (which parses VTP's election data file which is implemented as a
    directory tree), and calls its main function.
    """

    # do it
    sco = ShowContestsOperation(parse_arguments())
    sco.run()


# If called directly via this file
if __name__ == "__main__":
    main()
