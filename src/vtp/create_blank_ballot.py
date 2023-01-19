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

"""create_blank_ballot.py - command line level test script to automatically cast a ballot.

See './create_blank_ballot.py -h' for usage information.

See ../../docs/tech/executable-overview.md for the context in which this file was created.

"""

# Standard imports
# pylint: disable=wrong-import-position
import argparse
import logging
import pprint
import sys

# Local imports
from vtp.utils.address import Address
from vtp.utils.ballot import BlankBallot
from vtp.utils.election_config import ElectionConfig


################
# arg parsing
################
# pylint: disable=duplicate-code
def parse_arguments():
    """Parse command line arguments"""

    parser = argparse.ArgumentParser(
        description="""create_blank_ballot.py will parse all the config and
    address_map yaml files in the current VTP election git tree and
    create a blank ballot based on the supplied address.

    ZZZ - in the future some other argument can be supported to print
    for example all possible unique blank ballots found in the current
    VTP election tree, whatever.
    """
    )

    Address.add_address_args(parser)
    parser.add_argument(
        "-l",
        "--language",
        default="en",
        help="will print the ballot in the specified language",
    )
    parser.add_argument(
        "-v",
        "--verbosity",
        type=int,
        default=3,
        help="0 critical, 1 error, 2 warning, 3 info, 4 debug (def=3)",
    )
    parser.add_argument(
        "-n",
        "--printonly",
        action="store_true",
        help="will printonly and not write to disk (def=True)",
    )

    parsed_args = parser.parse_args()
    verbose = {
        0: logging.CRITICAL,
        1: logging.ERROR,
        2: logging.WARNING,
        3: logging.INFO,
        4: logging.DEBUG,
    }
    logging.basicConfig(
        format="%(message)s", level=verbose[parsed_args.verbosity], stream=sys.stdout
    )
    return parsed_args


################
# main
################

ARGS = None

# pylint: disable=duplicate-code
def main():
    """Main function - see -h for more info"""

    # pylint: disable=global-statement
    global ARGS
    ARGS = parse_arguments()

    # Create an VTP election config object
    the_election_config = ElectionConfig()
    the_election_config.parse_configs()

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
        ARGS, ["verbosity", "printonly", "language"]
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
        "And the edges are: %s", pprint.pformat(the_election_config.get_dag("edges"))
    )

    # Construct a blank ballot
    the_ballot = BlankBallot()
    the_ballot.create_blank_ballot(the_address, the_election_config)
    logging.info("Active GGOs: %s", the_ballot.get("active_ggos"))
    logging.debug(
        "And the blank ballot looks like:\n%s", pprint.pformat(the_ballot.dict())
    )

    # Write it out
    if not ARGS.printonly:
        ballot_file = the_ballot.write_blank_ballot(the_election_config)
        logging.info("Blank ballot file: %s", ballot_file)


if __name__ == "__main__":
    main()

# EOF
