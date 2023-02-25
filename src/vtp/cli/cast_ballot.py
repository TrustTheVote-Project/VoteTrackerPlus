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
from vtp.core.common import Common
from vtp.ops.cast_ballot_operation import CastBallotOperation

from ._arguments import Arguments


def parse_arguments(argv):
    """
    Parse command line arguments.  This can be called either with
    sys.argv sans the first arg which is the 'script name', in
    which case argv is a list of strings, or with a dictionary, in
    which case is converted to a list of strings.

    So to match native argparse argv parsing, if a dict value is a
    boolean, the value is removed from the list and the key is
    either kept (True) or deleted (False).  If the value is None,
    the key is removed.
    """

    safe_args = Common.cast_thing_to_list(argv)
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
Given either an address or a specific blank ballot, will either read a
blank ballot and allow a user to manually select choices or when in
demo mode, cast_ballot.py will randominly select choices.
""",
    )

    Arguments.add_address(parser)
    # ZZZ - cloaked contests are enabled at cast_ballot time
    #    parser.add_argument('-k', "--cloak", action="store_true",
    #                            help="if possible provide a cloaked ballot offset")
    parser.add_argument(
        "--demo_mode",
        action="store_true",
        help="set demo mode to automatically cast random ballots",
    )
    parser.add_argument(
        "--blank_ballot",
        help="overrides an address - specifies the specific blank ballot",
    )
    Arguments.add_verbosity(parser)
    Arguments.add_print_only(parser)

    return parser.parse_args(safe_args)


# pylint: disable=duplicate-code
def main():
    """Entry point for 'cast-ballot'."""

    args = parse_arguments(sys.argv[1:])
    op = CastBallotOperation(args)
    op.run()


# If called directly via this file
if __name__ == "__main__":
    main()
