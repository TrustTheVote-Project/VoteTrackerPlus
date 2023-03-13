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

"""cast_ballot.py - command line level test script to automatically cast a ballot.

See 'cast_ballot.py -h' for usage information.
"""

# Global imports
import argparse
import sys

# Local imports
from vtp.core.address import Address
from vtp.core.common import Common
from vtp.ops.cast_ballot_operation import CastBallotOperation

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

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
Given either an address or a specific blank ballot, will either read a
blank ballot and allow a user to manually select choices or when in
demo mode, cast_ballot.py will randominly select choices.
""",
    )

    Address.add_address_args(parser)
    # ZZZ - cloaked contests are enabled at cast_ballot time
    #    parser.add_argument('-k', "--cloak", action="store_true",
    #                            help="if possible provide a cloaked ballot offset")
    Common.add_election_data(parser)
    parser.add_argument(
        "--demo_mode",
        action="store_true",
        help="set demo mode to automatically cast random ballots",
    )
    Common.add_blank_ballot(parser)
    Common.add_verbosity(parser)
    Common.add_printonly(parser)
    parsed_args = parser.parse_args(argv)
    # Validate required args
    Common.verify_election_data_dir(parsed_args.election_data)
    return parsed_args


def main():
    """
    Called via a python local install entrypoint or by running this
    file.  Simply wraps the scripts constructor and calls the run
    method.  See the script's help output or read the
    vtp.ops.cast_ballot_operation.py (argparse) description in the
    source file.
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
    cbo = CastBallotOperation(parsed_args.verbosity, parsed_args.printonly)
    cbo.run(
        an_address=an_address,
        blank_ballot=parsed_args.blank_ballot,
        demo_mode=parsed_args.demo_mode,
        election_data=parsed_args.election_data,
        )


# If called directly via this file
if __name__ == "__main__":
    main()
