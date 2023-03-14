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

"""
Command line level script to merge CVR contest
branches into the main branch

See 'merge_contests.py -h' for usage information.
"""

# Standard imports
import argparse
import sys

# Local imports
from vtp.core.common import Common
from vtp.ops.merge_contests_operation import MergeContestsOperation


def parse_arguments(argv):
    """Parse arguments from a command line or from the constructor"""

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
Will run the git based workflow on a VTP server node so to merge
pending CVR contest branches into the main git branch.

If there are less then the prerequisite number of already cast
contests, a warning will be printed/logged but no error will be
raised.  Supplying -f will flush all remaining contests to the main
branch.
""",
    )
    Common.add_election_data_dir(parser)
    parser.add_argument(
        "-b",
        "--branch",
        default="",
        help="specify a specific branch to merge",
    )
    Common.add_minimum_cast_cache(parser)
    parser.add_argument(
        "-f",
        "--flush",
        action="store_true",
        help="will flush the remaining unmerged contest branches",
    )
    parser.add_argument(
        "-r",
        "--remote",
        action="store_true",
        help="will merge remote branches instead of local branches",
    )
    Common.add_verbosity(parser)
    Common.add_printonly(parser)
    return parser.parse_args(argv)


def main():
    """
    Called via a python local install entrypoint or by running this
    file.  Simply wraps the scripts constructor and calls the run
    method.  See the script's help output or read the
    vtp.ops.merge_contests_operation.py (argparse) description in the
    source file.
    """

    # Parse args
    parsed_args = parse_arguments(sys.argv)

    # do it
    mco = MergeContestsOperation(
        parsed_args.election_data_dir, parsed_args.verbosity, parsed_args.printonly
    )
    mco.run(
        branch=parsed_args.branch,
        flush=parsed_args.flush,
        remote=parsed_args.remote,
        minimum_cast_cache=parsed_args.minimum_cast_cache,
    )


# If called directly via this file
if __name__ == "__main__":
    main()
