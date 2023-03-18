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

"""create-blank-ballot - command line level test script to automatically cast a ballot.

See 'create-blank-ballot -h' for usage information.

See ../../docs/tech/executable-overview.md for the context in which this file was created.

"""

# Standard imports
import argparse

# Project imports
from vtp.core.address import Address
from vtp.ops.create_blank_ballot_operation import CreateBlankBallotOperation

# Local imports
from ._arguments import Arguments


def parse_arguments():
    """Parse arguments from a command line or from the constructor"""

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
Will parse all the config and address_map yaml files in the current
VTP ElectionData git tree and create a blank ballot based on the
supplied address.
""",
    )
    Address.add_address_args(parser)
    Arguments.add_election_data_dir(parser)
    parser.add_argument(
        "-l",
        "--language",
        default="en",
        help="will print the ballot in the specified language",
    )
    Arguments.add_verbosity(parser)
    Arguments.add_printonly(parser)
    return parser.parse_args()


# pylint: disable=duplicate-code
def main():
    """Entry point for 'create-blank-ballot'."""

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
    cbbo = CreateBlankBallotOperation(
        parsed_args.election_data_dir, parsed_args.verbosity, parsed_args.printonly
    )
    cbbo.run(
        an_address=an_address,
        language=parsed_args.language,
    )


# If called directly via this file
if __name__ == "__main__":
    main()

# EOF
