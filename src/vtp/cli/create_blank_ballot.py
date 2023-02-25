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

See 'docs/tech/executable-overview.md' for the context in which this file was created.
"""

# Standard imports
import argparse
import sys

# Local imports
from vtp.core.address import Address
from vtp.core.common import Common
from vtp.ops.create_blank_ballot_operation import CreateBlankBallotOperation

from ._arguments import Arguments


def parse_arguments(argv):
    safe_args = Common.cast_thing_to_list(argv)
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
Will parse all the config and address_map yaml files in the current
VTP ElectionData git tree and create a blank ballot based on the
supplied address.
""",
    )

    Address.add_address_args(parser)
    parser.add_argument(
        "-l",
        "--language",
        default="en",
        help="will print the ballot in the specified language",
    )
    Arguments.add_verbosity(parser)
    Arguments.add_print_only(parser)

    return parser.parse_args(safe_args)


def main():
    """Entry point for 'accept-ballot'."""

    args = parse_arguments(sys.argv[1:])
    op = CreateBlankBallotOperation(args)
    op.run()


# If called directly via this file
if __name__ == "__main__":
    main()
