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

# Project imports
from vtp.core.address import Address
from vtp.ops.cast_ballot_operation import CastBallotOperation

# Local imports
from ._arguments import Arguments


def parse_arguments():
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

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
Given either an address or a specific blank ballot, will either read a
blank ballot and allow a user to manually select choices or when in
demo mode, cast_ballot.py will randominly select choices.
""",
    )

    Arguments.add_address_args(parser)
    # ZZZ - cloaked contests are enabled at cast_ballot time
    #    parser.add_argument('-k', "--cloak", action="store_true",
    #                            help="if possible provide a cloaked ballot offset")
    Arguments.add_election_data_dir(parser)
    parser.add_argument(
        "--demo_mode",
        action="store_true",
        help="set demo mode to automatically cast random ballots",
    )
    parser.add_argument(
        "-r",
        "--return_blank_ballot",
        action="store_true",
        help="Will return the blank JSON ballot",
    )
    Arguments.add_blank_ballot(parser)
    Arguments.add_verbosity(parser)
    Arguments.add_printonly(parser)
    return parser.parse_args()


# pylint: disable=duplicate-code
def main():
    """Entry point for 'cast-ballot'."""

    # Parse args
    parsed_args = parse_arguments()

    # Convert the address args into an Address
    an_address = Address(
        address=parsed_args.address,
        substreet=parsed_args.substreet,
        town=parsed_args.town,
        state=parsed_args.state,
    )

    # do it
    cbo = CastBallotOperation(
        parsed_args.election_data_dir, parsed_args.verbosity, parsed_args.printonly
    )
    return_string = cbo.run(
        an_address=an_address,
        blank_ballot=parsed_args.blank_ballot,
        demo_mode=parsed_args.demo_mode,
        return_bb=parsed_args.return_blank_ballot,
    )
    print(return_string)


# If called directly via this file
if __name__ == "__main__":
    main()
