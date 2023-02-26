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
import argparse
import logging
import pprint

# Local import
from vtp.core.address import Address
from vtp.core.ballot import BlankBallot
from vtp.core.common import Common
from vtp.core.election_config import ElectionConfig


class CreateBlankBallotOperation:
    """
    A class to implememt the create-blank-ballot operation.  See the
    create-blank-ballot help output or read the parse_argument argparse
    description (immediately below this) in the source file.
    """

    @staticmethod
    def parse_arguments(argv):
        """Parse arguments from a command line or from the constructor"""

        safe_args = Common.cast_thing_to_list(argv)
        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description="""
    Will parse all the config and address_map yaml files in the current
    VTP ElectionData git tree and create a blank ballot based on the
    supplied address.
    """,
        )
        Address.add_address_args(parser)
        Common.add_election_data(parser)
        parser.add_argument(
            "-l",
            "--language",
            default="en",
            help="will print the ballot in the specified language",
        )
        Common.add_verbosity(parser)
        Common.add_printonly(parser)
        parsed_args = parser.parse_args(safe_args)
        # Verify arguments
        Common.verify_election_data(parsed_args)
        return parsed_args

    def __init__(self, unparsed_args):
        """Only to module-ize the scripts and keep things simple and idiomatic."""
        self.parsed_args = CreateBlankBallotOperation.parse_arguments(unparsed_args)

    def run(self):
        """Main function - see -h for more info"""

        # Configure logging
        Common.configure_logging(self.parsed_args.verbosity)

        # Create a VTP ElectionData object if one does not already exist
        the_election_config = ElectionConfig.configure_election()

        # Parse the address nominally supplied via the args. ZZZ -
        # existing address parsing packages look out-of-date and US
        # centric. But the idea is that the actual town will know the
        # latest and greatest and that any other data may/will be out of
        # date, particularly if the voting center can update records on
        # the fly. So, for now assume that the street address map will be
        # imported somehow and that each GGO for the address will also be
        # imported somehow. And all that comes later - for now just map an
        # address to a town.
        the_address = Address.create_address_from_args(
            self.parsed_args, ["election_data", "language", "printonly", "verbosity"]
        )
        the_address.map_ggos(the_election_config)

        # print some debugging info
        logging.debug("The election config ggos are: %s", the_election_config)
        logging.debug("And the address is: %s", str(the_address))
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
        the_ballot.create_blank_ballot(the_address, the_election_config)
        logging.info("Active GGOs: %s", the_ballot.get("active_ggos"))
        logging.debug(
            "And the blank ballot looks like:\n%s", pprint.pformat(the_ballot.dict())
        )

        # Write it out
        if not self.parsed_args.printonly:
            ballot_file = the_ballot.write_blank_ballot(the_election_config)
            logging.info("Blank ballot file: %s", ballot_file)


# End Of Class

# EOF
