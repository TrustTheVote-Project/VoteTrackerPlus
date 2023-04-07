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

"""Logic of operation for generating blank ballots."""

# Standard imports
import logging
import os
import pprint

# Project imports
from vtp.core.address import Address
from vtp.core.ballot import BlankBallot
from vtp.core.common import Common
from vtp.core.election_config import ElectionConfig

# Local imports
from .operation import Operation


# pylint: disable=too-few-public-methods
class GenerateAllBlankBallotsOperation(Operation):
    """
    A class to implememt the generate-all-blank-ballots operation.  See the
    generate-all-blank-ballots help output.
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
    def run(self):
        """Main function - see -h for more info"""

        # Configure logging
        Common.configure_logging(self.verbosity)

        # Create a VTP ElectionData object if one does not already exist
        the_election_config = ElectionConfig.configure_election(self.election_data_dir)

        # Walk a topo sort of the DAG and for any node with
        # 'unique-ballots', add them all.  If the subdir does not match
        # REQUIRED_GGO_ADDRESS_FIELDS, place the blank ballot
        for node in the_election_config.get_dag("topo"):
            address_map = the_election_config.get_node(node, "address_map")
            if "unique-ballots" in address_map:
                for unique_ballot in address_map["unique-ballots"]:
                    subdir = the_election_config.get_node(node, "subdir")
                    ggos = unique_ballot.get("ggos")
                    # if the subdir is not a state/town, shorten it to that
                    subdir = os.path.sep.join(subdir.split(os.path.sep)[0:6])
                    # Now create a generic address on the list of ggos, an
                    # associated generic blank ballot, and store it out
                    generic_address = Address.create_generic_address(
                        the_election_config, subdir, ggos
                    )
                    generic_ballot = BlankBallot()
                    generic_ballot.create_blank_ballot(
                        generic_address, the_election_config
                    )
                    logging.info(
                        "Active GGOs for blank ballot (%s): %s",
                        generic_address,
                        generic_ballot.get("active_ggos"),
                    )
                    logging.debug(
                        "And the blank ballot looks like:\n%s",
                        pprint.pformat(generic_ballot.dict()),
                    )
                    # Write it out
                    if self.printonly:
                        ballot_file = the_election_config.gen_blank_ballot_location(
                            generic_address.active_ggos,
                            generic_address.ballot_subdir,
                            "json",
                        )
                    else:
                        ballot_file = generic_ballot.write_blank_ballot(
                            the_election_config
                        )
                    logging.info("Blank ballot file: %s", ballot_file)


# EOF
