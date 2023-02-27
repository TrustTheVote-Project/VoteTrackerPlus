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

"""Command line script to verify a voter's ballot receipt.

Supports several interesting options.

Run with '--help' for usage information.
"""

# Standard imports
import argparse
import sys

# Local imports
from vtp.core.address import Address
from vtp.core.common import Common
from vtp.ops.verify_ballot_receipt_operation import VerifyBallotReceiptOperation

from ._arguments import Arguments


def parse_arguments(argv):
    safe_args = Common.cast_thing_to_list(argv)
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
Will read a voter's ballot receipt and validate all the digests
contained therein.  If a contest has been merged to the main branch,
will report the current ballot tally number (which ballot in the
actula tally cound is the voter's).

An address is also supported as an argument in which case the last
ballot check is read from the default location for the specified
address.

Can also optionally print the ballot's CVRs when a specific ballot
check row is provided.
""",
    )
    Arguments.add_address(parser, True)
    parser.add_argument(
        "-f",
        "--receipt_file",
        default="",
        help="specify the ballot receipt location - overrides an address",
    )
    parser.add_argument(
        "-r",
        "--row",
        default="",
        help="specify a row to inspect that row (the first row is 1, not 0)",
    )
    parser.add_argument(
        "-c",
        "--cvr",
        action="store_true",
        help="display the contents of the content CVRs specifying a row",
    )
    parser.add_argument(
        "-x",
        "--do_not_pull",
        action="store_true",
        help="Before tallying the votes, pull the ElectionData repo",
    )
    Arguments.add_verbosity(parser)
    # Arguments.add_print_only(parser)

    args = parser.parse_args(safe_args)

    # Validate required args
    if not (args.receipt_file or (args.state and args.town)):
        raise ValueError(
            "Either an explicit or implicit (via an address) receipt file must be provided"
        )

    address_args, parsed = Arguments.separate_addresses(args)
    parsed["address"] = Address(generic_address=True, **address_args)
    return parsed


def main():
    """Entry point for 'verify-ballot-receipt'."""

    args = parse_arguments(sys.argv[1:])
    op = VerifyBallotReceiptOperation(**args)
    op.run()


# If called directly via this file
if __name__ == "__main__":
    main()
