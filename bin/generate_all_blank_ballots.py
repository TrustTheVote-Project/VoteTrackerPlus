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

"""generate_all_blank_ballots.py - generate all possible blank ballots

See 'generate_all_blank_ballots.py -h' for usage information.

See ../docs/tech/executable-overview.md for the context in which this file was created.

"""

# Standard imports
# pylint: disable=wrong-import-position   # import statements not top of file
import sys
import argparse
import logging
from logging import debug

# Local import
from common import Globals, Shellout
from address import Address
from ballot import Ballot, Contests
from election_config import ElectionConfig

# Functions


################
# arg parsing
################
def parse_arguments():
    """Parse arguments from a command line"""

    parser = argparse.ArgumentParser(description=
    """generate_all_blank_ballots.py will crawl the ElectionData tree
    and determine all possible blank ballots and generate them.  They
    will be placed in the town's blank-ballots subdir.
    """,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("-v", "--verbosity", type=int, default=3,
                            help="0 critical, 1 error, 2 warning, 3 info, 4 debug (def=3)")
    parser.add_argument("-n", "--printonly", action="store_true",
                            help="will printonly and not write to disk (def=True)")

    parsed_args = parser.parse_args()
    verbose = {0: logging.CRITICAL, 1: logging.ERROR, 2: logging.WARNING,
                   3: logging.INFO, 4: logging.DEBUG}
    logging.basicConfig(format="%(message)s", level=verbose[parsed_args.verbosity],
                            stream=sys.stdout)

    # No args need to be validated
    return parsed_args

################
# main
################
def main():
    """Main function - see -h for more info"""

    # Create an VTP election config object
    the_election_config = ElectionConfig()
    the_election_config.parse_configs()

    # Loop over all towns and for each town:
    # - find all the unique-ballot entries and create a blank ballot
    # - do the same for all descendents

    # It is not an error if there are multiple hits

    # This method may want to be in either Address or ElectionConfig TBD

    # ZZZ for now print entire ballot receipt

if __name__ == '__main__':
    args = parse_arguments()
    main()
