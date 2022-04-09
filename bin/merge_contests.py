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
    """merge_contests.py will run the git based workflow on a VTP
    server node so to merge pending CVR contest branches into the
    master git branch.

    If there are less then the prerequisite number of already cast
    contests, a warning will be printed/logged but no error will be
    raised.
    """,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("-f", "--flush", action='store_true',
                            help="will flush the remaining unmerged contest branches")
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

    # Set the three EV's
    os.environ['GIT_AUTHOR_DATE'] = '2022-01-01T12:00:00'
    os.environ['GIT_COMMITTER_DATE'] = '2022-01-01T12:00:00'
    os.environ['GIT_EDITOR'] = 'true'

    """
$ git pull
$ git merge --no-ff --no-commit <contest>/<short GUID>
$ openssl rand -base64 48 > CVRs/contest.cvr
$ GIT_EDITOR=true git commit
$ git branch -d <contest>/<short GUID>
$ git push origin master
$ git push origin :<contest>/<short GUID>
    """

    # loop over contests
    branches = []
    with Shellout.changed_cwd(a_ballot.get_cvr_parent_dir(the_election_config)):
        # So, the CWD in this block is the state/town subfolder
        for contest in contests:

    debug(f"Ballot's digests:\n{ballot_receipts}")

if __name__ == '__main__':
    args = parse_arguments()
    main()

# EOF
