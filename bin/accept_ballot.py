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
import os
import sys
import argparse
import logging
from logging import debug
import random
import secrets
#import uuid

# Local import
from common import Globals, Shellout
from address import Address
from ballot import Ballot, Contests
from election_config import ElectionConfig

# Functions
def get_random_branchpoint(branch):
    """Return a random branchpoint on the supplied branch

    Requires the CWD to be the parent of the CVRs directory.
    """
    result = Shellout.run(["git", "log", branch, "--pretty=format:'%h'"],
                check=True, capture_output=True, text=True)
    commits = [commit for commit in (line.strip("' ") for line in
                                         result.stdout.splitlines()) if commit]
    # the first record is never a real CVR
    del commits[-1]
    # ZZZ - need to deal with a rolling 100 window
    return random.choice(commits)

def checkout_new_contest_branch(contest, ref_branch):
    """Will checkout a new branch for a specific contest.  Since there
    is no code yet to coordinate the potentially multiple scanners
    pushing to the same VC VTP git remote, use a highly unlikely GUID
    and try up to 3 times to get a unique branch.

    Requires the CWD to be the parent of the CVRs directory.
    """

    # select a branchpoint
    branchpoint = get_random_branchpoint(ref_branch)
    # and attempt at a new unique branch
    branch = contest.get('uid') + "/" + secrets.token_hex(5)
#    branch = contest.get('uid') + "/" + str(uuid.uuid1().hex)[0:10]
    current_branch = Shellout.run(["git", "rev-parse", "--abbrev-ref", "HEAD"],
                        check=True, capture_output=True, text=True).stdout.strip()
    # if after 3 tries it still does not work, raise an error
    for _ in [0, 1, 2]:
        cmd1 = Shellout.run(["git", "checkout", "-b", branch, branchpoint],
                                      printonly=args.printonly)
        if cmd1.returncode == 0:
            # Created the local branch - see if it is push-able
            cmd2 = Shellout.run(["git", "push", "-u", "origin", branch],
                                      printonly=args.printonly)
            if cmd2.returncode == 0:
                # success
                return branch
            # At this point there was some type of push failure - delete the
            # local branch and try again
            Shellout.run(["git", "checkout", current_branch], check=True)
            Shellout.run(["git", "branch", "-D", branch], check=True)
        # At this point the local did not get created - try again
        branch = contest.get('uid') + "/" + secrets.token_hex(5)

    # At this point the remote branch was never created and in theory the local
    # tries have also deleted(?)
    raise Exception(f"could not create git branch {branch} on the third attempt")

def get_n_other_contests(contest, branch):
    """Return a list of N already cast CVRs for the specified contest.

    Requires the CWD to be the parent of the CVRs directory.
    """
    this_uid = contest.get('uid')
    return Shellout.run(['git', 'log', branch, '--oneline', '--all-match',
                             '--grep={"CVR"}',
                             f'--grep="uid": "{this_uid}"'],
                     check=True, capture_output=True, text=True).stdout.strip()

def get_cloaked_contests(contest, branch):
    """Return a list of N cloaked cast CVRs for the specified contest.
    ZZZ - cloaking actually is a difficult problem because a cloaked
    value should only ever be given out once and regardless whatever
    value is given out can be cross checked with other ballot receipts.
    So a cloaked value is really only good if the digest is never
    really checked.

    Requires the CWD to be the parent of the CVRs directory.
    """
    this_uid = contest.get('uid')
    cloak_target = contest.get('cloak')
    return Shellout.run(['git', 'log', branch, '--oneline', '--all-match',
                             '--grep={"CVR"}', f'--grep="uid": "{this_uid}"',
                             f'--grep="cloak": "{cloak_target}"'],
                     check=True, capture_output=True, text=True).stdout.strip()

def contest_add_and_commit(branch):
    """Will git add and commit the new contest content.

    Requires the CWD to be the parent of the CVRs directory.
    """
    # If this fails an shell error will be raised
    contest_file = os.path.join(
        Globals.get('CONTEST_FILE_SUBDIR'), Globals.get('CONTEST_FILE'))
    Shellout.run(['git', 'add', contest_file],
                     printonly=args.printonly)
    Shellout.run(['git', 'commit', '-F', contest_file],
                     printonly=args.printonly)
    # Capture the digest
    digest = Shellout.run(['git', 'log', branch, '-1', '--pretty=format:"%H"'],
                     printonly=args.printonly,
                     check=True, capture_output=True, text=True).stdout.strip()
    return digest


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

    Address.add_address_args(parser, False)
    parser.add_argument('-f', "--file",
                            help="override the default location of the cast ballot file")
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
    if not (parsed_args.file or (parsed_args.town and parsed_args.state)):
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
    voting_center_address = Address(state=args.state,
                                    town=args.town,
                                    voting_center=True)
    voting_center_address.map_ggos(the_election_config)

    # get the ballot for the specified address
    a_ballot = Ballot()
    a_ballot.read_a_cast_ballot(voting_center_address, the_election_config, args.file)

    # the voter's row of digests (indexed by contest uid)
    ballot_receipts = {}
    # a cloaked receipt
    cloak_receipts = {}
    # 100 additional contest receipts
    other_receipts = {}

    # Set the three EV's
    os.environ['GIT_AUTHOR_DATE'] = '2022-01-01T12:00:00'
    os.environ['GIT_COMMITTER_DATE'] = '2022-01-01T12:00:00'
    os.environ['GIT_EDITOR'] = 'true'

    # loop over contests
    branches = []
    contests = Contests(a_ballot)
    with Shellout.changed_cwd(a_ballot.get_cvr_parent_dir(the_election_config)):
        # So, the CWD in this block is the state/town subfolder
        for contest in contests:
            with Shellout.changed_branch('master'):
                # get N other values for each contest for this ballot
                uid = contest.get('uid')
                other_receipts[uid] = get_n_other_contests(contest, 'master')
                # atomically create the branch locally and remotely
                branches.append(checkout_new_contest_branch(contest, 'master'))
                # write out the voter's contest to CVRs/contest.json
                a_ballot.write_contest(contest, the_election_config)
                # commit the voter's contest
                ballot_receipts[uid] = contest_add_and_commit(branches[-1])
                # if cloaking, get those as well
                if 'cloak' in contest.get('contest'):
                    cloak_receipts[uid] = get_cloaked_contests(contest, 'master')
        # After all the contests digests have been generated and the
        # others and cloaks are in as much as possible, then push as
        # atomically as possible all the contests.
#        import pdb; pdb.set_trace()
        for branch in branches:
            Shellout.run(['git', 'push', 'origin', branch],
                         printonly=args.printonly)

    debug(f"Ballot's digests:\n{ballot_receipts}")
    # ZZZ for now print entire ballot receipt

    # for now print the voter's offset

if __name__ == '__main__':
    args = parse_arguments()
    main()
