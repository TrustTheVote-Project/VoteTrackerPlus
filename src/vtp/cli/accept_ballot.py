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

"""accept-ballot - command line level script to accept a ballot.

See 'accept-ballot -h' for usage information.
"""

# Global imports
import argparse

# Project imports
from vtp.core.address import Address
from vtp.ops.accept_ballot_operation import AcceptBallotOperation

# Local imports
from ._arguments import Arguments


def parse_arguments():
    """Parse arguments from a command line or from the constructor"""

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
Will run the git based workflow on a VTP scanner node to accept the json
rendering of the cast vote record of a voter's ballot. The json file is read,
the contests are extraced and submitted to separate git branches, one per
contest, and pushed back to the Voter Center's VTP remote.

In addition a voter's ballot receipt and offset are optionally printed.

Either the location of the ballot_file or the associated address is required.
""",
    )

    Arguments.add_address_args(parser, True)
    Arguments.add_election_data_dir(parser)
    parser.add_argument(
        "--cast_ballot",
        help="overrides an address - specifies a specific cast ballot",
    )
    Arguments.add_verbosity(parser)
    Arguments.add_printonly(parser)
    return parser.parse_args()


# pylint: disable=duplicate-code
def main():
    """Entry point for 'accept-ballot'."""

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
    abo = AcceptBallotOperation(
        parsed_args.election_data_dir, parsed_args.verbosity, parsed_args.printonly
    )
    abo.run(
        an_address=an_address,
        cast_ballot=parsed_args.cast_ballot,
    )


# If called directly via this file
if __name__ == "__main__":
    main()
