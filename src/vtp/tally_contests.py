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
tally_contests.py - command line level script to tally the contests of
a election.

See './tally_contests.py -h' for usage information.

See ../docs/tech/*.md for the context in which this file was created.
"""

# pylint: disable=wrong-import-position   # import statements not top of file
# Standard imports
import argparse
import logging
import re
import sys

# Local import
from .utils.ballot import Ballot
from .utils.common import Shellout
from .utils.contest import Tally
from .utils.election_config import ElectionConfig
from .utils.exceptions import TallyException

# Functions


################
# arg parsing
################
# pylint: disable=duplicate-code
def parse_arguments():
    """Parse arguments from a command line"""

    parser = argparse.ArgumentParser(description=
    """tally_contests.py will tally all the contests so far merged to
    the master branch and report the results.  The results are
    computed on a voting center basis (git submodule) basis.

    Note - the current implementation relies on git submodules
    (individual git repos) to break up the tally data of an election.
    If there is only one git repository and the election is large,
    then a potentiallu large amount of memory will be used in
    executing the tallies.  One short term fix for this is to limit
    the number of contests being tallied.

    Also note that the current implementation does not yet support
    tallying across git submodules/repos.
    """,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("-c", "--contest_uid", default="",
                            help="limit the tally to a specific contest uid")
    parser.add_argument("-t", "--track_contests", default="",
                            help="a comma separated list of contests checks to track")
    parser.add_argument("-x", "--do_not_pull", action="store_true",
                            help="Before tallying the votes, pull the ElectionData repo")
    parser.add_argument("-v", "--verbosity", type=int, default=3,
                            help="0 critical, 1 error, 2 warning, 3 info, 4 debug (def=3)")
#    parser.add_argument("-n", "--printonly", action="store_true",
#                            help="will printonly and not write to disk (def=True)")

    parsed_args = parser.parse_args()
    verbose = {0: logging.CRITICAL, 1: logging.ERROR, 2: logging.WARNING,
                   3: logging.INFO, 4: logging.DEBUG}
    logging.basicConfig(format="%(message)s", level=verbose[parsed_args.verbosity],
                            stream=sys.stdout)

    # Validate required args
    if parsed_args.track_contests:
        if not bool(re.match('^[0-9a-f,]', parsed_args.track_contests)):
            raise ValueError(
                "The track_contests parameter only accepts a comma separated (no spaces) "
                "list of contest checks/digests to track.")
        parsed_args.track_contests = parsed_args.track_contests.split(',')
    else:
        parsed_args.track_contests = []
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

    # git pull the ElectionData repo so to get the latest set of
    # remote CVRs branches
    a_ballot = Ballot()
    with Shellout.changed_cwd(a_ballot.get_cvr_parent_dir(the_election_config)):
        Shellout.run(
            ["git", "pull"],
            verbosity=args.verbosity,
            check=True)

    # Will process all the CVR commits on the master branch and tally
    # all the contests found.  Note - even if a contest is specified,
    # as a first pass it is easier to just perform a git log across
    # all the contests and then filter later for the contest of
    # interest than to try to create a git grep query against the CVR
    # payload.
    contest_batches = Shellout.cvr_parse_git_log_output(
        ['git', 'log', '--topo-order', '--no-merges', '--pretty=format:%H%B'],
        the_election_config)

    # Note - though plurality voting can be counted within the above
    # loop, tallies such as rcv cannot.  So far now, just count
    # everything in a separate loop.
    for contest_batch in sorted(contest_batches):
        # Maybe skip
        if args.contest_uid != '':
            if contest_batches[contest_batch][0]['CVR']['uid'] != args.contest_uid:
                continue
        # Create a Tally object for this specific contest
        the_tally = Tally(contest_batches[contest_batch][0])
        logging.info(
            "Scanned %s contests for contest (%s) uid=%s, tally=%s, max=%s, win-by>%s",
            len(contest_batches[contest_batch]),
            contest_batches[contest_batch][0]['CVR']['name'],
            contest_batches[contest_batch][0]['CVR']['uid'],
            contest_batches[contest_batch][0]['CVR']['tally'],
            the_tally.get('max'),
            the_tally.get('win-by'))
        # Tally all the contests for this contest
#        import pdb; pdb.set_trace()
        try:
            the_tally.tallyho(contest_batches[contest_batch], args.track_contests)
            # Print stuff
            the_tally.print_results()
        except TallyException as tally_error:
            logging.error("[ERROR]: %s\nContinuing with other contests ...", tally_error)

if __name__ == '__main__':
    args = parse_arguments()
    main()

# EOF
