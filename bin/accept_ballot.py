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

"""accept_ballot-py - command line level script to accept a ballot.

See './accept_ballot.py -h' for usage information.

See ../docs/tech/executable-overview.md for the context in which this file was created.

"""

# Standard imports
# pylint: disable=wrong-import-position   # import statements not top of file
import json
import sys
import argparse
import logging
import secrets

# Local import
from common import Globals, Shellout
# Local imports
from address import Address
from ballot import Ballot, Contests
from election_config import ElectionConfig

# Functions
def checkout_new_contest_branch(contest, branchpoint):
    """Will checkout a new branch for a specific contest.  Since there
    is no code yet to coordinate the potentially multiple scanners
    pushing to the same VC VTP git remote, use a highly unlikely GUID
    and try up to 3 times to get a unique branch.
    """

    # first attempt at a new unique branch
    branch = contest + "/" + secrets.token_hex(5)
    current_branch = Shellout.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], check=True).stdout
    # if after 3 tries it still does not work, raise an error
    max_tries = 3
    count = 1
    while count < max_tries:
        count += 1
        cmd1 = Shellout.run(["git", "checkout", "-b", branch, branchpoint])
        if cmd1.returncode == 0:
            # Created the local branch - see if it is push-able
            cmd2 = Shellout.run(["git", "push", "-u", "origin", branch])
            if cmd2.returncode == 0:
                # success
                return branch
            # At this point there was some type of push failure - delete the
            # local branch and try again
            Shellout.run(["git", "checkout", current_branch], check=True)
            Shellout.run(["git", "branch", "-D", branch], check=True)
        # At this point the local did not get created - try again
        branch = contest + "/" + secrets.token_hex(9)

    # At this point the remote branch was never created and in theory the local
    # tries are also deleted
    raise Exception(f"could not create git branch {branch} on the third attempt")

def add_commit_push_contest(branch):
    """Will git add and commit the new contest content
    """
    # If this fails,
    Shellout.run(["git", "add", Globals.get('CONTEST_FILE')])
    Shellout.run(["git", "commit", "-F", Globals.get('CONTEST_FILE')])
    # Note - if there is a collision, pick another random number and try again
    Shellout.run(["git", "push", "origin", branch])
    return 0

# ZZZ this probably wants to shift to a class at some point
def slurp_a_ballot(ballot_file):
    """Will slurp the json version of a blank ballot and return it"""

    # OS and json syntax errors are just raised at this point
    # ZZZ - need an gestalt error handling plan at some point
    with open(ballot_file, 'r', encoding="utf8") as file:
        json_doc = json.load(file)
    return json_doc


################
# arg parsing
################
def parse_arguments():
    """Parse arguments from a command line"""

    parser = argparse.ArgumentParser(description=
    """accept_ballot.py will run the git based workflow on a VTP
    scanner node to accept the json rendering of the cast vote record
    of a voter's ballot.  The json file is read, the contests are
    extraced and submitted to separate git branches, one per contest,
    and pushed back to the Voter Center's VTP remote.

    In addition a voter's ballot receipt and offset are optionally
    printed.

    Either the location of the ballot_file or the associated address
    is required.
    """,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    Address.add_address_args(parser)
    parser.add_argument('-f', "--file",
                            help="override the default location of the cast ballot file")
    parser.add_argument("-v", "--verbosity", type=int, default=3,
                            help="0 critical, 1 error, 2 warning, 3 info, 4 debug (def=3)")
    parser.add_argument("-n", "--printonly", action="store_true",
                            help="will printonly and not write to disk (def=True)")

    parsed_args = parser.parse_args()
    verbose = {0: logging.CRITICAL, 1: logging.ERROR, 2: logging.WARNING,
                   3: logging.INFO, 4: logging.DEBUG}
    logging.basicConfig(format="%(message)s", level=verbose[parsed_args.v], stream=sys.stdout)

    # Validate required args
    if not (parsed_args.file or (parsed_args.address and parsed_args.town
                                    and parsed_args.state)):
        parser.error("Either a ballot file (-f <filename>) or an address "
                     "(-a <number street> -t <town> -s <state>) is required")
    return parsed_args

################
# main
################
def main():
    """Main function - see -h for more info"""

    # Create an VTP election config object
    the_election_config = ElectionConfig()
    the_election_config.parse_configs()

    # Process the address so to know where the ballot is.  The address
    # is only necessary of the
    the_address = Address.create_address_from_args(args,
                    ['file', 'verbosity', 'printonly'])

    # get the ballot for the specified address
    a_ballot = Ballot()
    a_ballot.read_a_cast_ballot(the_address, the_election_config, args.file)

    # the voter's row of digests
    contest_receipts = []
    import pdb; pdb.set_trace()

    # loop over contests
    contests = Contests(a_ballot)
    for contest in contests:
        # select a branchpoint
        branchpoint = "bar"
        # atomically create the branch locally and remotely
        branch = checkout_new_contest_branch(contest, branchpoint)
        # commit the voter's choice and push it
        digest = add_commit_push_contest(branch)
        contest_receipts.append(digest)

    # if possible print the ballot receipt

    # if possible, print the voter's offset

if __name__ == '__main__':
    args = parse_arguments()
    main()
