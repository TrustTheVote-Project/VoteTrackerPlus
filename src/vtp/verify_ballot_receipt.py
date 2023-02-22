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

See 'verify_ballot_receipt.py -h' for usage information.
"""

# Standard imports
import argparse

from vtp.utils.address import Address
from vtp.ops.verify_ballot_receipt_operation import VerifyBallotReceiptOperation


################
# arg parsing
################
# pylint: disable=duplicate-code
def parse_arguments():
    """Parse arguments from a command line"""

    parser = argparse.ArgumentParser(
        description="""Will read a voter's ballot receipt and validate
                    all the digests contained therein.  If a contest
                    has been merged to the master branch, will report
                    the current ballot tally number (which ballot in
                    the actula tally cound is the voter's).

                    An address is also supported as an argument in
                    which case the last ballot check is read from the
                    default location for the specified address.

                    Can also optionally print the ballot's CVRs when a
                    specific ballot check row is provided.
                    """
    )

    Address.add_address_args(parser, True)
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
    parser.add_argument(
        "-v",
        "--verbosity",
        type=int,
        default=3,
        help="0 critical, 1 error, 2 warning, 3 info, 4 debug (def=3)",
    )
    #    parser.add_argument("-n", "--printonly", action="store_true",
    #                            help="will printonly and not write to disk (def=True)")

    parsed_args = parser.parse_args()

    # Validate required args
    if not (
        parsed_args.receipt_file
        or (parsed_args.state and parsed_args.town)
    ):
        raise ValueError(
            "Either an explicit or implicit (via an address) receipt file must be provided"
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
    vbro = VerifyBallotReceiptOperation(parse_arguments())
    vbro.run()


# If called directly via this file
if __name__ == "__main__":
    main()
