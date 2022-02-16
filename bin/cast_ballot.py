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

"""cast_a_ballot.py - command line level test script to automatically cast a ballot.

See './cast_a_ballot.py -h' for usage information.

See ../docs/tech/executable-overview.md for the context in which this file was created.

"""

# pylint: disable=C0413   # import statements not top of file
import json
import sys
import argparse
import logging
#  Not currently used/imported:  critical, error, warning, info, debug
#from logging import info
#import secrets

# Globals for now
# ZZZ needs to be classed or moved to a config file somewhere
CONTEST_FILE = "CVRs/contest.json"
"""Temporary global variable for the location of the contest cvr file"""

SHELL_TIMEOUT = 15
"""How long to wait for a generic shell command to complete - maybe a bad idea"""

BALLOT_FILE = "CVRs/ballot.json"
"""The default location from the CWD of this program, which is different than
the installation location, of the location of the incoming ballot.json file
for the current incoming scanned ballot."""

BLANK_BALLOT_FILE = "CVRs/blank_ballot.json"
"""The default location from the CWD of this program, which is different than
the installation location, of the location of a blank ballot associated with
the address that is being tested.  The json version only includes the ballot
data - https://pages.nist.gov/ElectionGlossary/#ballot-data - and not
instructions or descriptions or verbiage associated with a contest or ballot.
contests"""

# Functions
# ZZZ this probably wants to shift to a class at some point
def slurp_a_ballot(ballot_file):
    """Will return the dictionary of a json ballot file"""

    # OS and json syntax errors are just raised at this point
    # ZZZ - need an gestalt error handling plan at some point
    with open(ballot_file, 'r', encoding="utf8") as file:
        json_doc = json.load(file)
    return json_doc

def create_a_mock_ballot(ballot):
    """Will create a (mock) ballot.json file."""

    json_file = BALLOT_FILE
    # OS and json syntax errors are just raised at this point
    # ZZZ - need an gestalt error handling plan at some point
    if args.printonly:
        print(f"{json.dumps(ballot)}")
        return
    with open(json_file, 'w', encoding="utf8") as outfile:
        json.dump(ballot, outfile)
    return

################
# arg parsing
################
def parse_arguments():
    """Parse command line arguments
    """

    parser = argparse.ArgumentParser(description=\
    """ accept_ballot.py will run the git based workflow on a VTP
    scanner node to accept the json rendering of the cast vote record
    of a voter's ballot. The json file is read, the contests are
    extraced and submitted to separate git branches, one per contest,
    and pushed back to the Voter Center's VTP remote.

    In addition a voter's ballot receipt and offset are optionally
    printed.
    """)

    parser.add_argument('-v', metavar='verbosity', type=int, default=3,
                            help='0 critical, 1 error, 2 warning, 3 info, 4 debug (def=3)')
    parser.add_argument("-n", "--printonly", action="store_true",
                            help='will printonly and not write to disk (def=True)')

    parsed_args = parser.parse_args()
    verbose = {0: logging.CRITICAL, 1: logging.ERROR, 2: logging.WARNING,
                   3: logging.INFO, 4: logging.DEBUG}
    logging.basicConfig(format='%(message)s', level=verbose[parsed_args.v], stream=sys.stdout)
    return parsed_args

################
# main
################
def main():
    """Main function - see -h for more info.  At the moment no error
    handling, but in theory something might go here once a UX error
    model has been chosen.
    """

    # create a dictionary of the ballot of interest
    a_ballot = slurp_a_ballot(BLANK_BALLOT_FILE)

    # loop over contests
    for contest in a_ballot.contests:
        # choose something
        a_ballot.vote_a_contest(contest, choose=1)

    # write it out
    create_a_mock_ballot(a_ballot)

if __name__ == '__main__':
    args = parse_arguments()
    main()
