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
merge_contests.py - command line level script to merge CVR contest
branches into the master branch

See './merge_contests.py -h' for usage information.

See ../docs/tech/merge_contests.md for the context in which this
file was created.
"""

# Standard imports
# pylint: disable=wrong-import-position   # import statements not top of file
import argparse
import logging
import os
import random
import re
import sys

# Local import
from .utils.common import Globals, Shellout
from .utils.election_config import ElectionConfig


# Functions
def merge_contest_branch(branch):
    """Merge a specific branch"""
    # If the VTP server is processing contests from different
    # voting centers, then the contest.json could be in different
    # locations on different branches.
    contest_file = Shellout.run(
        ['git', 'diff-tree', '--no-commit-id', '-r', '--name-only', branch],
        verbosity=args.verbosity,
        capture_output=True, text=True, check=True).stdout.strip()
    # 2022/06/09: witnessed the above line returning no files several
    # times in an ElectionData repo where I was debugging things. So
    # it could be real or perhaps a false one. Regardless adding an
    # test condition in that if there is no file to merge, there is no
    # file to merge - pass.
    if not contest_file:
        logging.error(f"Error - 'git diff-tree --no-commit-d -r --name-only {branch}'"
                  "returned no files.  Skipping")
        return
    # Merge the branch / file.  Note - there will always be a conflict
    # so this command will always return non zero
    Shellout.run(
        ['git', 'merge', '--no-ff', '--no-commit', branch],
        printonly=args.printonly, verbosity=args.verbosity)
    # ZZZ - replace this with an run-time cryptographic value
    # derived from the run-time election private key (diffent from
    # the git commit run-time value).  This will basically slam
    # the contents of the contest file to a second runtime digest
    # (the first one being contained in the commit itself).
    result = Shellout.run(
        ['openssl',  'rand', '-base64',  '48'],
        verbosity=args.verbosity,
        capture_output=True, text=True, check=True)
    if result.stdout == '':
        raise ValueError("'openssl rand' should never return an empty string")
    if not args.printonly:
        # ZZZ need to convert the digest to json format ...
        with open(contest_file, 'w', encoding="utf8") as outfile:
            # Write a runtime digest as the actual contents of the
            # merge
            outfile.write(str(result.stdout))
    # Force the git add just in case
    Shellout.run(
        ['git', 'add', contest_file],
        printonly=args.printonly, verbosity=args.verbosity, check=True)
    # Note - apparently git place the commit msg on STDERR - hide it
    Shellout.run(
        ['git', 'commit', '-m', 'auto commit - thank you for voting'],
        printonly=args.printonly, verbosity=1, check=True)
    Shellout.run(['git', 'push', 'origin', 'master'], args.printonly, check=True)
    # Delete the local and remote branch if this is a local branch
    if not args.remote:
        Shellout.run(
            ['git', 'push', 'origin', '-d', branch],
            printonly=args.printonly, verbosity=args.verbosity, check=True)
        Shellout.run(
            ['git', 'branch', '-d', branch],
            printonly=args.printonly, verbosity=args.verbosity, check=True)
    else:
        # otherwise just delete the remote
        Shellout.run(
            ['git', 'push', 'origin', '-d', branch.removeprefix('origin/')],
            printonly=args.printonly, verbosity=args.verbosity, check=True)

def randomly_merge_contests(uid, batch):
    """
    Will randomingly select (len(batch) - BALLOT_RECEIPT_ROWS) contest
    branches from the supplied list of branch and merge them to the
    master branch.

    This is the git merge-to-master sequence.
    """
    if len(batch) <= args.minimum_cast_cache:
        if args.flush:
            count = len(batch)
        else:
            logging.info(f"Contest {uid} not merged - only {len(batch)} available")
            return 0
    else:
        count = len(batch) - args.minimum_cast_cache
    loop = count
    logging.info(f"Merging {count} contests for contest {uid}")
    while loop:
        pick = random.randrange(len(batch))
        branch = batch[pick]
        merge_contest_branch(branch)
        # End of loop maintenance
        del batch[pick]
        loop -= 1
    logging.debug(f"Merged {count} {uid} contests")
    return count

################
# arg parsing
################
# pylint: disable=duplicate-code
def parse_arguments():
    """Parse arguments from a command line"""

    parser = argparse.ArgumentParser(description=
    """merge_contests.py will run the git based workflow on a VTP
    server node so to merge pending CVR contest branches into the
    master git branch.

    If there are less then the prerequisite number of already cast
    contests, a warning will be printed/logged but no error will be
    raised.  Supplying -f will flush all remaining contests to the
    master branch.
    """,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument(
        "-b", "--branch", default='',
        help="specify a specific branch to merge")
    parser.add_argument(
        "-m", "--minimum_cast_cache", type=int, default=100,
        help="the minimum number of cast ballots required prior to merging (def=100)")
    parser.add_argument(
        "-f", "--flush", action='store_true',
        help="will flush the remaining unmerged contest branches")
    parser.add_argument(
        "-r", "--remote", action='store_true',
        help="will merge remote branches instead of local branches")
    parser.add_argument(
        "-v", "--verbosity", type=int, default=3,
        help="0 critical, 1 error, 2 warning, 3 info, 4 debug (def=3)")
    parser.add_argument(
        "-n", "--printonly", action="store_true",
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

    # For best results (so to use the 'correct' git submodule or
    # tranverse the correct symlink or not), use the CWD as when
    # accepting the ballot (accept_ballot.py).
    merged = 0
    with Shellout.changed_cwd(os.path.join(
        the_election_config.get('git_rootdir'),
        Globals.get('ROOT_ELECTION_DATA_SUBDIR'))):
        # So, the CWD in this block is the state/town subfolder
        # Pull the remote
        Shellout.run(
            ["git", "pull"],
            printonly=args.printonly, verbosity=args.verbosity, check=True)
        if args.branch:
            merge_contest_branch(args.branch)
            logging.info(f"Merged '{args.branch}'")
            return
        # Get the pending CVR branches
        cmds = ['git', 'branch']
        cvr_regex = f"{Globals.get('CONTEST_FILE_SUBDIR')}/([^/]+?)/"
        if args.remote:
            cmds.append('-r')
            cvr_regex = "^origin/" + cvr_regex
        else:
            cvr_regex = "^" + cvr_regex
        # Note - the re.search will strip non CVRs lines
        cvr_branches = [branch.strip() for branch in Shellout.run(
            cmds, verbosity=args.verbosity, check=True, capture_output=True,
            text=True).stdout.splitlines() if re.search(cvr_regex, branch.strip())]
        # Note - sorted alphanumerically on contest UID. Loop over
        # contests and randomly merge extras
        batch = []   # if ordered_set was native would probably use that
        current_uid = None
        for branch in cvr_branches:
            uid = re.search(cvr_regex, branch).group(1)
            if current_uid == uid:
                batch.append(branch)
                continue
            # Since cvr_branches is ordered, when there is a new uid
            # that does not match the current_uid then try to merge
            # that contest uid set of branched.  Also try to merge the
            # batch if this is the final iteration of the loop.
            if current_uid:
                # see if previous batch can be merged
                merged += randomly_merge_contests(current_uid, batch)
            # Start a new next batch
            current_uid = uid
            batch = [branch]
        if batch:
            # Always try to merge the remaining batch
            merged += randomly_merge_contests(current_uid, batch)
    logging.info(f"Merged {merged} contest branches")

if __name__ == '__main__':
    args = parse_arguments()
    main()

# EOF
