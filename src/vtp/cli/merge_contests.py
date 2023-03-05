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

"""Command line script to merge CVR contest.

Branches into the main branch.

Run with '--help' for usage information.
"""

# Standard imports
import argparse
import sys

# Local imports
from vtp.core.common import Common
from vtp.ops.merge_contests_operation import MergeContestsOperation

from ._arguments import Arguments


def parse_arguments(argv):
    safe_args = Common.cast_thing_to_list(argv)
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
    parser.add_argument(
        "-b", "--branch", default="", help="specify a specific branch to merge"
    )
    Arguments.add_minimum_cast_cache(parser)
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
    Arguments.add_verbosity(parser)
    Arguments.add_print_only(parser)

    parsed_args = Arguments.parse_arguments(parser, safe_args)
    # Validation, if any is needed, goes here
    return parsed_args


# pylint: disable=duplicate-code
def main():
    """Entry point for 'merge-contests'."""

    args = parse_arguments(sys.argv[1:])
    op = MergeContestsOperation(**args)
    op.run()


# If called directly via this file
if __name__ == "__main__":
    main()
