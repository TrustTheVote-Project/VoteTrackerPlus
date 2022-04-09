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
tally_contests.py - command line level script to merge CVR contest
branches into the master branch

See './tally_contests.py -h' for usage information.

See ../docs/tech/tally_contests.md for the context in which this
file was created.
"""

# Standard imports
# pylint: disable=wrong-import-position   # import statements not top of file
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
    """tally_contests.py will tally all the contests so far merged to
    the master branch.
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

    # Validate required args
    return parsed_args

################
# main
################
def main():
    """Main function - see -h for more info"""

    # Create an VTP election config object
    the_election_config = ElectionConfig()
    the_election_config.parse_configs()

    # Will process all the CVR commits on the master branch and tally
    # all the contests found.

if __name__ == '__main__':
    args = parse_arguments()
    main()

# EOF
