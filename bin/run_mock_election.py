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
run_mock_election.py - command line level script to merge CVR contest
branches into the master branch

See './run_mock_election.py -h' for usage information.

See ../docs/tech/run_mock_election.md for the context in which this
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
# pylint: disable=duplicate-code
def parse_arguments():
    """Parse arguments from a command line"""

    parser = argparse.ArgumentParser(description=
    """run_mock_election.py will run a mock election with N ballots
    for a given town/GGO and the blank ballots contained within:

        - will randomly cast each blank ballot N times

        - will tally each of race and report the winner

    Currently only a serial mock election is supported (need more
    quality pizza to support parallel and multi process/threaded
    elections).
    """,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    Address.add_address_args(parser, True)
    parser.add_argument("-b", "--ballots", type=int, default=3,
                            help="the number of unique blank ballots to cast")
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
# pylint: disable=duplicate-code
def main():
    """Main function - see -h for more info"""

    # Create an VTP election config object
    the_election_config = ElectionConfig()
    the_election_config.parse_configs()

    # Set the three EV's
    os.environ['GIT_AUTHOR_DATE'] = '2022-01-01T12:00:00'
    os.environ['GIT_COMMITTER_DATE'] = '2022-01-01T12:00:00'
    os.environ['GIT_EDITOR'] = 'true'

    # Note - this is a serial synchronous mock election loop.  A
    # parallel loop would have one VTP server git workspace somewhere
    # and N VTP scanner workspaces someplace else.  Depending on the
    # network topology, it is also possible to start up VTP scanner
    # workspaces on other machines as long as the git remotes and
    # clones are properly configured (with access etc).

    # While a mock election is running, it is also possible to use yet
    # another VTP scanner workspace to personally cast/insert
    # individual ballots for interactive purposes.

    # Get list of available blank ballots

    # Loop over the list N times

    # - cast a ballot
    # - accept the ballot
    # - merge the ballot (first 100 will be a noop)

    # merge the remaining contests

    # tally the contests

if __name__ == '__main__':
    args = parse_arguments()
    main()

# EOF
