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
Library operation for command line level script set up a VTP demo
See 'create_blank_ballot_operation.py -h' for usage information.
"""

# Standard imports
import logging
import pprint

# Local import
from vtp.core.address import Address
from vtp.core.ballot import BlankBallot
from vtp.core.common import Common
from vtp.core.election_config import ElectionConfig

# pylint: disable=too-few-public-methods
class CreateBlankBallotOperation:
    """
    A class to implememt the create-blank-ballot operation.  See the
    create-blank-ballot help output or read the parse_argument argparse
    description (immediately below this) in the source file.
    """

    def __init__(self, election_data_dir: str, verbosity: int, printonly: bool):
        """Only to module-ize the scripts and keep things simple and idiomatic."""
        self.election_data_dir = election_data_dir
        self.verbosity = verbosity
        self.printonly = printonly
        # Configure logging
        Common.configure_logging(verbosity)

    # pylint: disable=duplicate-code
    def run(
        self,
        an_address: Address,
        language: str = "",
        ):
        """Main function - see -h for more info"""

        # Configure logging
        Common.configure_logging(self.verbosity)

        # Create a VTP ElectionData object if one does not already exist
        the_election_config = ElectionConfig.configure_election(self.election_data_dir)

        # Set the ggos for the address
        an_address.map_ggos(the_election_config)

        # print some debugging info
        logging.debug("The election config ggos are: %s", the_election_config)
        logging.debug("And the address is: %s", str(an_address))
        logging.debug("And language is: %s", language)
        node = "GGOs/states/California/GGOs/towns/Oakland"
        logging.debug(
            "And a/the node (%s) looks like:\n%s",
            node,
            pprint.pformat(the_election_config.get_node(node, "ALL")),
        )
        logging.debug(
            "And the edges are: %s",
            pprint.pformat(the_election_config.get_dag("edges")),
        )

        # Construct a blank ballot
        the_ballot = BlankBallot()
        the_ballot.create_blank_ballot(an_address, the_election_config)
        logging.info("Active GGOs: %s", the_ballot.get("active_ggos"))
        logging.debug(
            "And the blank ballot looks like:\n%s", pprint.pformat(the_ballot.dict())
        )

        # Write it out
        if not self.printonly:
            ballot_file = the_ballot.write_blank_ballot(the_election_config)
            logging.info("Blank ballot file: %s", ballot_file)


# End Of Class

# EOF
