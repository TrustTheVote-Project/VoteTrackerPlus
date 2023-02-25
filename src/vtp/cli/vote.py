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

"""Command line script to allow an end voter to vote.

Simply wraps a call to cast_ballot.py and accept_ballot.py.

Run with '--help' for usage information.
"""

# Standard imports
import argparse
import sys

# Local imports
from vtp.core.address import Address
from vtp.core.common import Common
from vtp.ops.vote_operation import VoteOperation

from ._arguments import Arguments


def parse_arguments(argv):
    safe_args = Common.cast_thing_to_list(argv)
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
Will interactively allow a voter to vote.  Internally it first calls
cast_balloy.py followed by accept_ballot.py.  If a specific election
address or a specific blank ballot is not specified, a random blank
ballot is chosen.
""",
    )

    Address.add_address_args(parser)
    Arguments.add_merge_contests(parser)
    parser.add_argument(
        "--blank_ballot",
        help="overrides an address - specifies the specific blank ballot",
    )
    Arguments.add_verbosity(parser)
    Arguments.add_print_only(parser)

    return parser.parse_args(safe_args)


# pylint: disable=duplicate-code
def main():
    """Entry point for 'vote'."""

    args = parse_arguments(sys.argv[1:])
    op = VoteOperation(args)
    op.run()


# If called directly via this file
if __name__ == "__main__":
    main()
