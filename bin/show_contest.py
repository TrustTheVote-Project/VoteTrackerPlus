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

"""show_contest.py - command line level test script to automatically cast a ballot.

See './show_contest.py -h' for usage information.

See ../docs/tech/executable-overview.md for the context in which this file was created.

"""

# pylint: disable=wrong-import-position
import os
import sys
import argparse
import logging

# Local imports
from common import Globals, Shellout
from election_config import ElectionConfig

################
# Functions
################


################
# arg parsing
################
# pylint: disable=duplicate-code
def parse_arguments():
    """Parse command line arguments
    """

    parser = argparse.ArgumentParser(description=\
    """show_contest.py simply prints the contest from the VTP repos
    """)

    parser.add_argument("-c", "--contest-check",
                            help="the contest check to display")
    parser.add_argument("-v", "--verbosity", type=int, default=3,
                            help="0 critical, 1 error, 2 warning, 3 info, 4 debug (def=3)")
    parser.add_argument("-n", "--printonly", action="store_true",
                            help="will printonly and not write to disk (def=True)")
    parsed_args = parser.parse_args()
    verbose = {0: logging.CRITICAL, 1: logging.ERROR, 2: logging.WARNING,
                   3: logging.INFO, 4: logging.DEBUG}
    logging.basicConfig(format='%(message)s',
                            level=verbose[parsed_args.verbosity], stream=sys.stdout)
    # Validate required args
    if not parsed_args.contest_check:
        raise ValueError("The contest check is required")
    return parsed_args

################
# main
################
# pylint: disable=duplicate-code
def main():
    """Main function - see -h for more info"""

    # Check the ElectionData
    the_election_config = ElectionConfig()
    the_election_config.parse_configs()
    election_data_dir = os.path.join(
        the_election_config.get('git_rootdir'), Globals.get('ROOT_ELECTION_DATA_SUBDIR'))

    # Just cd into the ElectionData repo and run the git command
    with Shellout.changed_cwd(election_data_dir):
        Shellout.run(
            ['git', 'log', '-1', args.contest_check],
            check=True)

if __name__ == '__main__':
    args = parse_arguments()
    main()

# EOF
