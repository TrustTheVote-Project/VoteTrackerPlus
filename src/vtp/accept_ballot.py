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

"""accept_ballot.py - command line level script to accept a ballot.

See './accept_ballot.py -h' for usage information.

See ../docs/tech/executable-overview.md for the context in which this file was created.

"""

# Standard imports
# pylint: disable=wrong-import-position   # import statements not top of file
import os
import sys
import argparse
import logging
from logging import debug, warning
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
    # ZZZ why is the first record never a real CVR?
#    del commits[-1]
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
    branch = Globals.get('CONTEST_FILE_SUBDIR') + '/' + contest.get('uid') + \
      "/" + secrets.token_hex(5)
#    branch = contest.get('uid') + "/" + str(uuid.uuid1().hex)[0:10]
    current_branch = Shellout.run(["git", "rev-parse", "--abbrev-ref", "HEAD"],
                        check=True, capture_output=True, text=True).stdout.strip()
    # if after 3 tries it still does not work, raise an error
    for _ in [0, 1, 2]:
        cmd1 = Shellout.run(
            ["git", "checkout", "-b", branch, branchpoint],
            printonly=args.printonly,
            verbosity=args.verbosity)
        if cmd1.returncode == 0:
            # Created the local branch - see if it is push-able
            cmd2 = Shellout.run(
                ["git", "push", "-u", "origin", branch],
                printonly=args.printonly,
                verbosity=args.verbosity)
            if cmd2.returncode == 0:
                # success
                return branch
            # At this point there was some type of push failure - delete the
            # local branch and try again
            Shellout.run(
                ["git", "checkout", current_branch],
                check=True, printonly=args.printonly, verbosity=args.verbosity)
            Shellout.run(
                ["git", "branch", "-D", branch],
                check=True, printonly=args.printonly, verbosity=args.verbosity)
        # At this point the local did not get created - try again
        branch = contest.get('uid') + "/" + secrets.token_hex(5)

    # At this point the remote branch was never created and in theory the local
    # tries have also deleted(?)
    raise Exception(f"could not create git branch {branch} on the third attempt")

def get_unmerged_contests(config):
    """Queries git for the unmerged CVRs and returns the list.  See
    Shellout.cvr_parse_git_log_output for more info.  The returned
    list is still in git log order.
    """
    # Mmm, at the moment the thought is that we need all the unmerged
    # contests and ignore anything already merged.  So first get the
    # list of HEAD commits for all the unmerged branches.  Note that
    # since this is per contest, there should only be about 100 or so
    # of them.
    head_commits = Shellout.run(
        ['git', 'rev-list', '--no-walk', '--exclude=refs/heads/master', '--exclude=HEAD',
             '--exclude=refs/remotes/origin/master', '--exclude=refs/remotes/origin/HEAD', '--all'],
        check=True, capture_output=True, text=True).stdout.strip().splitlines()
    # With that list of HEAD exclusion commits, list the rest of the
    # --yes-walk commits and scrape that for the commits of interest.
    return Shellout.cvr_parse_git_log_output(
        ['git', 'log', '--no-walk', '--pretty=format:%H%B'] + head_commits,
        config,
        verbosity=args.verbosity - 1)

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
    return Shellout.run(
        ['git', 'log', branch, '--oneline', '--all-match', '--grep={"CVR"}',
             f'--grep="uid": "{this_uid}"', f'--grep="cloak": "{cloak_target}"'],
        check=True, capture_output=True, text=True).stdout.strip()

def contest_add_and_commit(branch):
    """Will git add and commit the new contest content.
    Requires the CWD to be the parent of the CVRs directory.
    """
    # If this fails a shell error will be raised
    contest_file = os.path.join(
        Globals.get('CONTEST_FILE_SUBDIR'), Globals.get('CONTEST_FILE'))
    Shellout.run(
        ['git', 'add', contest_file], printonly=args.printonly,
        verbosity=args.verbosity)
    # Note - apparently git place the commit msg on STDERR - hide it
    Shellout.run(
        ['git', 'commit', '-F', contest_file],
        printonly=args.printonly, verbosity=1)
    # Capture the digest
    digest = Shellout.run(['git', 'log', branch, '-1', '--pretty=format:%H'],
                     printonly=args.printonly,
                     check=True, capture_output=True, text=True).stdout.strip()
    return digest

def create_ballot_receipt(the_ballot, contest_receipts, unmerged_cvrs, the_election_config):
    """
    Create the voter's receipt.  As of this writing this is basically
    a csv file with a header line with one row in particular being the
    voter's.
    """
    ballot_receipt = []
#    import pdb; pdb.set_trace()
    # Not 0 based
    voters_row = random.randint(1,Globals.get('BALLOT_RECEIPT_ROWS'))
    # When there are not enough unmerged_receipts to print a receipt
    redacted_uids = set()
    # Add column headers - but include the long names as well
    next_row = []
    for uid in contest_receipts:
        next_row.append(
            '"' + uid + ' - ' + the_ballot.get_contest_name_by_uid(uid).replace('"',"'") + '"')
    ballot_receipt.append(','.join(next_row))
    # Loop BALLOT_RECEIPT_ROWS times (the rows) filling in the ballots
    # uids as the columns.  Two notes: the range is the full
    # BALLOT_RECEIPT_ROWS because even though the voter's row is
    # inserted, the voter's digest might have ended up in the
    # unmerged_cvrs list.  When that happens, that digest needs to be
    # skipped and the voter's row digest from unmerged_cvrs used
    # instead.
    for row in range(Globals.get('BALLOT_RECEIPT_ROWS')):
        if row == voters_row - 1:
            # Include the voter's receipts instead
            ballot_receipt.append(','.join(contest_receipts.values()))
            continue
        next_row = []
        # Note - these are the voter's uids and digests
        for uid, digest in contest_receipts.items():
            if uid not in unmerged_cvrs:
                # Actually, there are _no_ other such cast uid's in
                # this case
                redacted_uids.add(uid)
                next_row.append("INSUFFICIENT_CVRS")
            elif row > len(unmerged_cvrs[uid]):
                redacted_uids.add(uid)
                next_row.append("INSUFFICIENT_CVRS")
            elif digest == unmerged_cvrs[uid][row]['digest']:
                # This is the voter's own digest!
                if voters_row - 1 > len(unmerged_cvrs[uid]):
                    redacted_uids.add(uid)
                    next_row.append("INSUFFICIENT_CVRS")
                else:
                    next_row.append(unmerged_cvrs[uid][voters_row - 1]['digest'])
            else:
                next_row.append(unmerged_cvrs[uid][row]['digest'])
        ballot_receipt.append(','.join(next_row))
    # Now need to redact any uid column that contains one or more
    # INSUFFICIENT_CVRS

    # Now write out the ballot_receipt in csv for now - can deal with
    # html (URL links) and a pdf (printable) later - both still a TBD.
    receipt_file = the_ballot.write_receipt_csv(ballot_receipt, the_election_config)
    # print the voter's row to STDOUT for now
    print(f"############\n### Receipt file: {receipt_file}")
    print(f"### Voter's row: {voters_row}\n############")

################
# arg parsing
################
# pylint: disable=duplicate-code
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

    Address.add_address_args(parser, True)
    parser.add_argument("-m", "--merge_contests", action="store_true",
                            help="Will immediately merge the ballot contests (to master)")
    parser.add_argument("--cast_ballot",
                            help="overrides an address - specifies a specific cast ballot")
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

    # Create a ballot
    a_ballot = Ballot()

    # Note - accept_ballot.py currently only deals with generic
    # addresses since all cast ballots, regardless of active ggos, end
    # up in the same spot, nominally in the town subfolder.
    if args.cast_ballot:
        # Read the specified cast_ballot
        with Shellout.changed_cwd(os.path.join(
            the_election_config.get('git_rootdir'), Globals.get('ROOT_ELECTION_DATA_SUBDIR'))):
            a_ballot.read_a_cast_ballot('', the_election_config, args.cast_ballot)
    else:
        # Use the specified address
        the_address = Address.create_address_from_args(
            args,
            ['verbosity', 'printonly', 'cast_ballot', 'merge_contests'],
            generic_address=True)
        the_address.map_ggos(the_election_config, skip_ggos=True)
        # Get the ballot for the specified address.  Note that reading
        # the cast ballot will define the active ggos etc for the
        # ballot even though those fields are not defined for the
        # address.  However, reading a ballot still needs the
        # ballot_subdir field of the address.
        a_ballot.read_a_cast_ballot(the_address, the_election_config)

    # the voter's row of digests (indexed by contest uid)
    contest_receipts = {}
    # a cloaked receipt
    cloak_receipts = {}
    # 100 additional contest receipts
    unmerged_cvrs = {}

    # Set the three EV's
    os.environ['GIT_AUTHOR_DATE'] = '2022-01-01T12:00:00'
    os.environ['GIT_COMMITTER_DATE'] = '2022-01-01T12:00:00'
    os.environ['GIT_EDITOR'] = 'true'

    # loop over contests
    branches = []
    contests = Contests(a_ballot)
    with Shellout.changed_cwd(a_ballot.get_cvr_parent_dir(the_election_config)):
        # So, the CWD in this block is the state/town subfolder

        # It turns out that determining the other not yet merged to
        # master contests is apparently a challangin git query and one
        # that creates a lot of temporary memory requirements.  One
        # current way to slice that pie is to just get all such
        # commits up front similar to the tally_contests.py code.
        # Then extract from that chunk of memory the contest with the
        # matching uid's of interest.  In the end this may be the
        # least expensive as the big reader is thus a stdout PIPE
        # loop.
        unmerged_cvrs = get_unmerged_contests(the_election_config)

        for contest in contests:
            with Shellout.changed_branch('master'):
                # get N other values for each contest for this ballot
                uid = contest.get('uid')
                # atomically create the branch locally and remotely
                branches.append(checkout_new_contest_branch(contest, 'master'))
                # Add the cast_branch to the contest json payload
                contest.set('cast_branch', branches[-1])

                # They is an interest to add a contest runtime digest
                # key value pair which is a cryptographic value
                # derived from the run-time election private key. This
                # value could also read via read_contest and can be
                # validated against the election public key if
                # available. However, the 'lack of appearance of
                # trustworthiness' in that a 'cryptic' number is being
                # written/associated with the contest cvr that by
                # definition would contain something obaque is not an
                # effective improvement. So, do not so this. Leave the
                # insertion of a runtime digest at merge time, which
                # occurs later and independent of contest commit time
                # and any potential voter information.

                # Write out the voter's contest to CVRs/contest.json
                a_ballot.write_contest(contest, the_election_config)
                # commit the voter's contest
                contest_receipts[uid] = contest_add_and_commit(branches[-1])
                # if cloaking, get those as well
                if 'cloak' in contest.get('contest'):
                    cloak_receipts[uid] = get_cloaked_contests(contest, 'master')
        # After all the contests digests have been generated as well
        # as the others and cloaks as much as possible, then push as
        # atomically as possible all the contests.
        for branch in branches:
            Shellout.run(
                ['git', 'push', 'origin', branch],
                printonly=args.printonly, verbosity=args.verbosity)
            # Delete the local as they build up too much.  The local
            # reflog keeps track of the local branches
            Shellout.run(
                ['git', 'branch', '-d', branch],
                printonly=args.printonly, verbosity=args.verbosity)

    # If in demo mode, optionally merge the branches
    if args.merge_contests:
        bin_dir = os.path.join(the_election_config.get('git_rootdir'), 'bin')
        for branch in branches:
            # Merge the branch (but since the local branch should be
            # deleted at this point, merge the remote).  Note -
            # 'origin' is already hardcoded in several places and
            # 'remotes' is enough of a constant for this.
            Shellout.run(
                [os.path.join(bin_dir, 'merge_contests.py'), '-v', args.verbosity,
                     '-b', 'remotes/origin/' + branch, '-r']
                + (['-n'] if args.printonly else []),
                check=True, no_touch_stds=True, timeout=None)

    debug(f"Ballot's digests:\n{contest_receipts}")
    # Shuffled the unmerged_cvrs (an inplace shuffle) - only need to
    # shuffle the uids for this ballot.
#    import pdb; pdb.set_trace()
    skip_receipt = False
    for uid in contest_receipts:
        # if there are no unmerged_cvrs, just warn
        if uid not in unmerged_cvrs:
            warning(f"Warning - no unmerged_cvrs yet for contest {uid}")
            skip_receipt = True
            continue
        if len(unmerged_cvrs[uid]) < Globals.get('BALLOT_RECEIPT_ROWS'):
            warning(
                f"Warning - not enough unmerged CVRs ({len(unmerged_cvrs[uid])}) "
                f"to print receipt for contest {uid}")
            skip_receipt = True
        random.shuffle(unmerged_cvrs[uid])
    # Create the ballot receipt
    if skip_receipt:
        warning("Skipping ballot receipt due to lack of unmerged CVRs")
    else:
        create_ballot_receipt(a_ballot, contest_receipts, unmerged_cvrs, the_election_config)

if __name__ == '__main__':
    args = parse_arguments()
    main()
