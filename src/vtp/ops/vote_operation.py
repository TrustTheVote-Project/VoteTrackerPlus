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

"""Logic of operation for voting."""

from vtp.core.ballot import Ballot
from vtp.core.common import Common, Shellout
from vtp.core.election_config import ElectionConfig

# Local libraries
from vtp.ops.accept_ballot_operation import AcceptBallotOperation
from vtp.ops.cast_ballot_operation import CastBallotOperation


# pylint: disable=too-few-public-methods
class VoteOperation:
    """Implementation of 'vote' operation."""

    def __init__(self, args):
        """Only to module-ize the scripts and keep things simple and idiomatic."""
        self.args = args

    def run(self):
        # Configure logging
        Common.configure_logging(self.args.verbosity)

        # Create a VTP ElectionData object if one does not already exist
        the_election_config = ElectionConfig.configure_election()

        # git pull the ElectionData repo so to get the latest set of
        # remote CVRs branches
        a_ballot = Ballot()
        with Shellout.changed_cwd(a_ballot.get_cvr_parent_dir(the_election_config)):
            Shellout.run(
                ["git", "pull"],
                printonly=self.args.printonly,
                verbosity=self.args.verbosity,
                check=True,
            )

        # If an address was used, use that
        cast_args = {
            "verbosity": self.args.verbosity,
            "printonly": self.args.printonly,
        }
        accept_args = {
            "verbosity": self.args.verbosity,
            "printonly": self.args.printonly,
        }
        if not self.args.blank_ballot:
            if self.args.state:
                cast_args["state"] = self.args.state
                accept_args["state"] = self.args.state
            if self.args.town:
                cast_args["town"] = self.args.town
                accept_args["town"] = self.args.town
            if self.args.substreet:
                cast_args["substreet"] = self.args.substreet
            if self.args.address:
                cast_args["address"] = self.args.address
        else:
            cast_args["blank_ballot"] = self.args.blank_ballot
            accept_args["blank_ballot"] = self.args.blank_ballot

        # Basically only do as little as necessary to call cast_ballot.py
        # followed by accept_ballot.py
        # Cast a ballot
        a_cast_ballot_operation = CastBallotOperation(cast_args)
        a_cast_ballot_operation.run()
        # Accept the ballot
        a_accept_ballot_operation = AcceptBallotOperation(accept_args)
        a_accept_ballot_operation.run()
