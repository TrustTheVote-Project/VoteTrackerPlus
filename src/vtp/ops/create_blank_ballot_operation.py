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

"""Logic of operation for creating a blank ballot."""

# Standard imports
import pprint

# Project imports
from vtp.core.address import Address
from vtp.core.ballot import BlankBallot
from vtp.core.common import Common
from vtp.core.election_config import ElectionConfig

# Local imports
from .operation import Operation


# pylint: disable=too-few-public-methods
class CreateBlankBallotOperation(Operation):
    """
    A class to implememt the create-blank-ballot operation.  See the
    create-blank-ballot help output or read the parse_argument argparse
    description (immediately below this) in the source file.
    """

    # pylint: disable=duplicate-code
    def run(
        self,
        an_address: Address,
        language: str = "",
    ):
        """Main function - see -h for more info"""

        # Create a VTP ElectionData object if one does not already exist
        the_election_config = ElectionConfig.configure_election(self.election_data_dir)

        # Set the ggos for the address
        an_address.map_ggos(the_election_config)

        # print some debugging info
        self.imprimir(f"The election config ggos are: {the_election_config}", 5)
        self.imprimir(f"And the address is: {str(an_address)}", 5)
        self.imprimir(f"And language is: {language}", 5)

        # Construct a blank ballot
        the_ballot = BlankBallot()
        the_ballot.create_blank_ballot(an_address, the_election_config)
        self.imprimir(f"Active GGOs: {the_ballot.get('active_ggos')}", 4)
        self.imprimir(
            f"And the blank ballot looks like:\n{pprint.pformat(the_ballot.dict())}", 5)
        )

        # Maybe display some node info
        node = the_ballot.get("ballot_node")
        self.imprimir(
            f"And a/the node ({node}) looks like:\n{pprint.pformat(the_election_config.get_node(node, 'ALL'))}",
            5,
        )
        self.imprimir(
            f"And the edges are: {pprint.pformat(the_election_config.get_dag('edges'))}",
            5,
        )

        # Write it out
        ballot_file = the_ballot.write_blank_ballot(
            the_election_config, printonly=self.printonly
        )
        self.imprimir(f"Blank ballot file: {ballot_file}", 3)


# EOF
