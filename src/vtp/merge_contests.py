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
branches into the master branch

See 'merge_contests.py -h' for usage information.
"""

# Standard imports
import argparse

from vtp.ops.merge_contests_operation import MergeContestsOperation


################
# arg parsing
################
# pylint: disable=duplicate-code
def parse_arguments():
    """Parse arguments from a command line"""

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
Will run the git based workflow on a VTP server node so to merge
pending CVR contest branches into the master git branch.

If there are less then the prerequisite number of already cast
contests, a warning will be printed/logged but no error will be
raised.  Supplying -f will flush all remaining contests to the master
branch.
""",
    )

    parser.add_argument(
        "-b", "--branch", default="", help="specify a specific branch to merge"
    )
    parser.add_argument(
        "-m",
        "--minimum_cast_cache",
        type=int,
        default=100,
        help="the minimum number of cast ballots required prior to merging (def=100)",
    )
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

    return parser.parse_args()


# pylint: disable=duplicate-code
def main():
    """
    Called via a python local install entrypoint or this file.  Simply
    wraps the scripts constructor and calls run.
    """

    # do it
    mco = MergeContestsOperation(parse_arguments())
    mco.run()


# If called directly via this file
if __name__ == "__main__":
    main()
