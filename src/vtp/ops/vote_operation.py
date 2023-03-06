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

# Project imports
from vtp.core.address import Address
from vtp.core.ballot import Ballot
from vtp.core.common import Common, Shellout
from vtp.core.election_config import ElectionConfig

# Local imports
from .operation import Operation
from .accept_ballot_operation import AcceptBallotOperation
from .cast_ballot_operation import CastBallotOperation


# pylint: disable=too-few-public-methods
class VoteOperation(Operation):
    """Implementation of 'vote' operation."""

    def __init__(
        self,
        address: Address,
        merge_contests: bool = False,
        blank_ballot: str = "",
        **base_options,
    ):
        """Create a vote operation."""
        super().__init__(**base_options)
        self._address = address
        self._merge_contests = merge_contests
        self._blank_ballot = blank_ballot

    def run(self):
        # Configure logging
        Common.configure_logging(self._verbosity)

        # Create a VTP ElectionData object if one does not already exist
        the_election_config = ElectionConfig.configure_election()

        # git pull the ElectionData repo so to get the latest set of
        # remote CVRs branches
        a_ballot = Ballot()
        with Shellout.changed_cwd(a_ballot.get_cvr_parent_dir(the_election_config)):
            Shellout.run(
                ["git", "pull"],
                printonly=self._printonly,
                verbosity=self._verbosity,
                check=True,
            )

        # If an address was used, use that
        cast_args = {
            "address": self._address if not self._blank_ballot else Address(),
            "printonly": self._printonly,
            "verbosity": self._verbosity,
        }
        accept_args = {
            "address": self._address if not self._blank_ballot else Address(),
            "printonly": self._printonly,
            "verbosity": self._verbosity,
        }

        # Basically only do as little as necessary to call cast_ballot.py
        # followed by accept_ballot.py
        # Cast a ballot
        a_cast_ballot_operation = CastBallotOperation(**cast_args)
        a_cast_ballot_operation.run()
        # Accept the ballot
        a_accept_ballot_operation = AcceptBallotOperation(**accept_args)
        a_accept_ballot_operation.run()
