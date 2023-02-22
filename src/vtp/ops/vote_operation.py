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
from vtp.ops.accept_ballot_operation import AcceptBallotOperation
from vtp.ops.cast_ballot_operation import CastBallotOperation

# Local libraries
from vtp.utils.ballot import Ballot
from vtp.utils.common import Common, Shellout
from vtp.utils.election_config import ElectionConfig


# pylint: disable=too-few-public-methods
class VoteOperation:
    """A class to wrap the vote.py script."""

    def __init__(self, parsed_args):
        """Only to module-ize the scripts and keep things simple and idiomatic."""
        self.parsed_args = parsed_args

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
        cast_address_args = []
        accept_address_args = []
        if not self.parsed_args.blank_ballot:
            if self.parsed_args.state:
                cast_address_args += ["-s", self.parsed_args.state]
                accept_address_args += ["-s", self.parsed_args.state]
            if self.parsed_args.town:
                cast_address_args += ["-t", self.parsed_args.town]
                accept_address_args += ["-t", self.parsed_args.town]
            if self.parsed_args.substreet:
                cast_address_args += ["-b", self.parsed_args.substreet]
            if self.parsed_args.address:
                cast_address_args += ["-a", self.parsed_args.address]
        else:
            cast_address_args += ["--blank_ballot", self.parsed_args.blank_ballot]
            accept_address_args += ["--blank_ballot", self.parsed_args.blank_ballot]

        # Basically only do as little as necessary to call cast_ballot.py
        # followed by accept_ballot.py
        # Cast a ballot
        a_cast_ballot_operation = CastBallotOperation(
            ["-v", str(self.parsed_args.verbosity)]
            + cast_address_args
            + (["-n"] if self.parsed_args.printonly else []),
        )
        a_cast_ballot_operation.run()
        # Accept the ballot
        a_accept_ballot_operation = AcceptBallotOperation(
            ["-v", str(self.parsed_args.verbosity)]
            + accept_address_args
            + (["-n"] if self.parsed_args.printonly else [])
            + (["-m"] if self.parsed_args.merge_contests else []),
        )
        a_accept_ballot_operation.run()

    # End Of Class


# EOF
