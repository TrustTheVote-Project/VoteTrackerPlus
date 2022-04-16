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
import sys
import re
import subprocess
import json
# pylint: disable=wrong-import-position   # import statements not top of file
import argparse
import logging
from logging import info

# Local import
from election_config import ElectionConfig
from contest import Tally
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

    parser.add_argument("-c", "--contest",
                            help="limit the tally to a specific contest")
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

    # Will process all the CVR commits on the master branch and tally
    # all the contests found.
    contests = {}
    with subprocess.Popen(
        ['git', 'log', '--topo-order', '--no-merges', '--pretty=format:"%H%B"'],
        stdout=subprocess.PIPE,
        encoding="utf8") as process:
        # read lines until there is a complete json object, then
        # add the object for that contest.
        block = ''
        digest = ''
        recording = False
        for line in process.stdout.readline():
            if match := re.match('^([a-f0-9]{40}){', line):
                digest = match.group(1)
                recording = True
                block = '{'
                continue
            if recording:
                block += line
                if line == '}':
                    # this loads the contest under the CVR key
                    cast_contest = json.loads(block)
                    cast_contest['digest'] = digest
                    contests[cast_contest['CVR']['uid']].append(cast_contest)
                    block = ''
                    digest = ''
                    recording = False
    # Note - though plurality voting can be counted within the above
    # loop, tallies such as rcv cannot.  So far now, just count
    # everything in a separate loop.
    for uid in sorted(contests):
        info(f"Scanned {len(contests[uid])} contests for contest {uid} ({uid['CVR']['name']})")
        # Create a Tally object for this specific contest
        the_tally = Tally(uid, contests[uid])
        # Tally all the contests for this contest
        the_tally.tallyho(contests)
        # Print stuff
        the_tally.print_results()

if __name__ == '__main__':
    args = parse_arguments()
    main()

# EOF
