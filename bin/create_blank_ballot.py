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

See ../docs/tech/executable-overview.md for the context in which this file was created.

"""

# Standard imports
# pylint: disable=C0413   # import statements not top of file
import json
import sys
import argparse
import logging
from logging import info

# Local imports
from common import Globals, Address
from election_config import ElectionConfig

# Functions
def create_a_blank_ballot(address, config):
    """Will create a blank ballot.json file for a given address.
    """

    # lookup up the address across all GGO's and create the ballot
    # dictionary for it
    info(f"Looking up address \"{' '.join(address)}\" in {config}")
    blank_ballot = {}

    # OS and json syntax errors are just raised at this point
    # ZZZ - need an gestalt error handling plan at some point
    if args.printonly:
        print(f"{json.dumps(blank_ballot)}")
        return
    with open(Globals.get('BLANK_BALLOT_FILE'), 'w', encoding="utf8") as outfile:
        json.dump(blank_ballot, outfile)
    return

################
# arg parsing
################
def parse_arguments():
    """Parse command line arguments"""

    parser = argparse.ArgumentParser(description=
    """create_blank_ballot.py will parse all the config.yaml files in
    the current VTP election git tree and create a blank ballot based
    on the supplied address.

    ZZZ - in the future some other argument can be supported to print
    for example all possible unique blank ballots found in the current
    VTP election tree.
    """)

    parser.add_argument('-a', "--address",
                            help="a comma separated address")
    parser.add_argument("-v", "--verbosity", type=int, default=3,
                            help="0 critical, 1 error, 2 warning, 3 info, 4 debug (def=3)")
    parser.add_argument("-n", "--printonly", action="store_true",
                            help="will printonly and not write to disk (def=True)")

    parsed_args = parser.parse_args()
    verbose = {0: logging.CRITICAL, 1: logging.ERROR, 2: logging.WARNING,
                   3: logging.INFO, 4: logging.DEBUG}
    logging.basicConfig(format='%(message)s',
                            level=verbose[parsed_args.verbosity], stream=sys.stdout)
    return parsed_args

################
# main
################
def main():
    """Main function - see -h for more info.  At the moment no error
    handling, but in theory something might go here once a UX error
    model has been chosen.
    """

    # Create an VTP election config object
    the_election_config = ElectionConfig()
    the_election_config.parse_configs()

    # Parse the address nominally supplied via the args. ZZZ -
    # existing packages look out-of-date and US centric. But the idea
    # is that the actual town will know the latest and greatest and
    # that may/will be out of date with regards to any cached info.
    # So, for now assume that the street address map will be imported
    # somehow and that each GGO for the address will also be imported
    # somehow. And all that comes later - for now just map an address
    # to a town.
    the_address = Address(csv=args.address)

    # write it out
    create_a_blank_ballot(the_address, the_election_config)

if __name__ == '__main__':
    args = parse_arguments()
    main()
