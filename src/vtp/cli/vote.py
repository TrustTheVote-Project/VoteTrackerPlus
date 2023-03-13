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
vote.py - command line level script to allow an end voter to vote - it
simply wraps a call to cast_ballot.py and accept_ballot.py.

See 'vote.py -h' for usage information.
"""

# Global imports
import argparse
import sys

# Local imports
from vtp.core.address import Address
from vtp.core.common import Common
from vtp.ops.vote_operation import VoteOperation


def parse_arguments(argv):
    """Parse arguments from a command line or from the constructor"""

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
    Common.add_election_data_dir(parser)
    Common.add_blank_ballot(parser)
    Common.add_verbosity(parser)
    Common.add_printonly(parser)
    return parser.parse_args(safe_args)


def main():
    """
    Called via a python local install entrypoint or by running this
    file.  Simply wraps the scripts constructor and calls the run
    method.  See the script's help output or read the
    vtp.ops.vote_operation.py (argparse) description in the source
    file.
    """

    # Parse args
    parsed_args = parse_arguments(sys.argv)

    # Convert the address args into an Address
    an_address = Address(
        address=parsed_args.address,
        substreet=parsed_args.substreet,
        town=parsed_args.town,
        state=parsed_args.state,
        )

    # do it
    vote_op = VoteOperation(
        parsed_args.election_data_dir,
        parsed_args.verbosity,
        parsed_args.printonly)
    vote_op.run(
        an_address=an_address,
        blank_ballot=parsed_args.blank_ballot,
    )


# If called directly via this file
if __name__ == "__main__":
    main()
