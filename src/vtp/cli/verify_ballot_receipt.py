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
Command line level script to verify a voters ballot receipt.  Supports several interesting options.

See 'verify-ballot-receipt -h' for usage information.
"""

# Standard imports
import argparse

# Project imports
from vtp.ops.verify_ballot_receipt_operation import VerifyBallotReceiptOperation

# Local imports
from ._arguments import Arguments


def parse_arguments():
    """Parse arguments from a command line or from the constructor"""

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

    Arguments.add_election_data_dir(parser)
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
        help="specify a specific row to inspect (the first row is 1, not 0)",
    )
    parser.add_argument(
        "-c",
        "--cvr",
        action="store_true",
        help="display the contents of the CVRs when specifying a row",
    )
    Arguments.add_verbosity(parser)

    parsed_args = parser.parse_args()

    # Validate required args
    if not parsed_args.receipt_file:
        raise ValueError(
            "A receipt file must be provided"
        )
    return parsed_args


# pylint: disable=duplicate-code
def main():
    """Entry point for 'verify-ballot-receipt'."""

    # Parse args
    parsed_args = parse_arguments()

    # do it
    vbro = VerifyBallotReceiptOperation(
        parsed_args.election_data_dir,
        parsed_args.verbosity,
        False,
    )
    vbro.run(
        receipt_file=parsed_args.receipt_file,
        row=parsed_args.row,
        cvr=parsed_args.cvr,
    )


# If called directly via this file
if __name__ == "__main__":
    main()
