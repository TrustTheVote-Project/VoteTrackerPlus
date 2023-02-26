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
Library backend to command line level script to allow an end voter to
vote - it simply wraps a call to cast_ballot.py and accept_ballot.py.

See 'vote.py -h' for usage information.
"""

# Standard imports
import argparse

from vtp.core.address import Address
from vtp.core.ballot import Ballot
from vtp.core.common import Common, Shellout
from vtp.core.election_config import ElectionConfig

# Local libraries
from vtp.ops.accept_ballot_operation import AcceptBallotOperation
from vtp.ops.cast_ballot_operation import CastBallotOperation


# pylint: disable=too-few-public-methods
class VoteOperation:
    """
    A class to implememt the vote operation.  See the
    vote help output or read the parse_argument argparse
    description (immediately below this) in the source file.
    """

    @staticmethod
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
        Common.add_election_data(parser)
        Common.add_merge_contests(parser)
        Common.add_blank_ballot(parser)
        Common.add_verbosity(parser)
        Common.add_printonly(parser)
        parsed_args = parser.parse_args(safe_args)
        # Validate required args
        Common.verify_election_data(parsed_args)
        return parsed_args

    def __init__(self, unparsed_args):
        """Only to module-ize the scripts and keep things simple and idiomatic."""
        self.parsed_args = VoteOperation.parse_arguments(unparsed_args)

    ################
    # main
    ################
    def run(self):
        """Main function - see -h for more info"""

        # Configure logging
        Common.configure_logging(self.parsed_args.verbosity)

        # Create a VTP ElectionData object if one does not already exist
        the_election_config = ElectionConfig.configure_election()

        # git pull the ElectionData repo so to get the latest set of
        # remote CVRs branches
        a_ballot = Ballot()
        with Shellout.changed_cwd(a_ballot.get_cvr_parent_dir(the_election_config)):
            Shellout.run(
                ["git", "pull"],
                printonly=self.parsed_args.printonly,
                verbosity=self.parsed_args.verbosity,
                check=True,
            )

        # If an address was used, use that
        cast_args = {
            "verbosity": self.parsed_args.verbosity,
            "printonly": self.parsed_args.printonly,
        }
        accept_args = {
            "verbosity": self.parsed_args.verbosity,
            "printonly": self.parsed_args.printonly,
        }
        if not self.parsed_args.blank_ballot:
            if self.parsed_args.state:
                cast_args["state"] = self.parsed_args.state
                accept_args["state"] = self.parsed_args.state
            if self.parsed_args.town:
                cast_args["town"] = self.parsed_args.town
                accept_args["town"] = self.parsed_args.town
            if self.parsed_args.substreet:
                cast_args["substreet"] = self.parsed_args.substreet
            if self.parsed_args.address:
                cast_args["address"] = self.parsed_args.address
        else:
            cast_args["blank_ballot"] = self.parsed_args.blank_ballot
            accept_args["blank_ballot"] = self.parsed_args.blank_ballot

        # Basically only do as little as necessary to call cast_ballot.py
        # followed by accept_ballot.py
        # Cast a ballot
        a_cast_ballot_operation = CastBallotOperation(cast_args)
        a_cast_ballot_operation.run()
        # Accept the ballot
        a_accept_ballot_operation = AcceptBallotOperation(accept_args)
        a_accept_ballot_operation.run()

    # End Of Class


# EOF
