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

# Standard imports
import logging

# Project imports
from vtp.core.address import Address
from vtp.core.ballot import Ballot
from vtp.core.common import Shellout
from vtp.core.election_config import ElectionConfig
from vtp.ops.accept_ballot_operation import AcceptBallotOperation
from vtp.ops.cast_ballot_operation import CastBallotOperation

# Local imports
from .operation import Operation


# pylint: disable=too-few-public-methods
class VoteOperation(Operation):
    """
    A class to implememt the vote operation.  See the
    vote help output or read the parse_argument argparse
    description (immediately below this) in the source file.
    """

    def __init__(
        self,
        election_data_dir: str = "",
        guid: str = "",
        verbosity: int = 3,
        printonly: bool = False,
    ):
        """
        Primarily to module-ize the scripts and keep things simple,
        idiomatic, and in different namespaces.
        """
        super().__init__(election_data_dir, verbosity, printonly, guid)

    # pylint: disable=duplicate-code
    def run(
        self,
        an_address: Address,
        blank_ballot: str = "",
        merge_contests: bool = False,
    ) -> tuple[dict, int]:
        """Main function - see -h for more info"""

        # Create a VTP ElectionData object if one does not already exist
        the_election_config = ElectionConfig.configure_election(self.election_data_dir)

        # git pull the ElectionData repo so to get the latest set of
        # remote CVRs branches
        a_ballot = Ballot()
        with Shellout.changed_cwd(a_ballot.get_cvr_parent_dir(the_election_config)):
            Shellout.run(
                ["git", "pull"],
                printonly=self.printonly,
                verbosity=self.verbosity,
                check=True,
            )

        # Basically only do as little as necessary to call cast_ballot.py
        # followed by accept_ballot.py
        # Cast a ballot
        a_cast_ballot_operation = CastBallotOperation(
            election_data_dir=self.election_data_dir,
            verbosity=self.verbosity,
            printonly=self.printonly,
        )
        logging.debug("Calling CastBallotOperation.run")
        a_cast_ballot_operation.run(
            an_address=an_address,
            blank_ballot=blank_ballot,
        )
        # Accept a ballot
        a_accept_ballot_operation = AcceptBallotOperation(
            election_data_dir=self.election_data_dir,
            verbosity=self.verbosity,
            printonly=self.printonly,
        )
        # return what accept_ballot returns
        logging.debug("Calling AcceptBallotOperation.run")
        a_accept_ballot_operation.run(
            an_address=an_address,
            cast_ballot=blank_ballot,
            merge_contests=merge_contests,
        )


# EOF
