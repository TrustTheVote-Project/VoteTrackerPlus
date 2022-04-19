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
import os
import sys
import re
import subprocess
import json
# pylint: disable=wrong-import-position   # import statements not top of file
import argparse
import logging
from logging import info, error

# Local import
from election_config import ElectionConfig
from common import Globals, Shellout
from contest import Tally
from exceptions import TallyException
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
#    parser.add_argument("-n", "--printonly", action="store_true",
#                            help="will printonly and not write to disk (def=True)")

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
    contest_batches = {}
    with Shellout.changed_cwd(os.path.join(
        the_election_config.get('git_rootdir'), Globals.get('ROOT_ELECTION_DATA_SUBDIR'))):
        with subprocess.Popen(
            ['git', 'log', '--topo-order', '--no-merges', '--pretty=format:%H%B'],
            stdout=subprocess.PIPE,
            text=True,
            encoding="utf8") as git_output:
            # read lines until there is a complete json object, then
            # add the object for that contest.
            block = ''
            digest = ''
            recording = False
            # question - how to get "for line in
            # git_output.stdout.readline():" not to effectively return
            # the characters in line as opposed to the entire line
            # itself?
            while True:
                line = git_output.stdout.readline()
                if not line:
                    break
                if match := re.match('^([a-f0-9]{40}){', line):
                    digest = match.group(1)
                    recording = True
                    block = '{'
                    continue
                if recording:
                    block += line.strip()
                    if re.match('^}', line):
                        # this loads the contest under the CVR key
                        cvr = json.loads(block)
                        cvr['digest'] = digest
                        if cvr['CVR']['uid'] in contest_batches:
                            contest_batches[cvr['CVR']['uid']].append(cvr)
                        else:
                            contest_batches[cvr['CVR']['uid']] = [cvr]
                        block = ''
                        digest = ''
                        recording = False
    # Note - though plurality voting can be counted within the above
    # loop, tallies such as rcv cannot.  So far now, just count
    # everything in a separate loop.
    for contest_batch in sorted(contest_batches):
        # Create a Tally object for this specific contest
        the_tally = Tally(contest_batches[contest_batch][0])
        info(
            f"Scanned {len(contest_batches[contest_batch])} contests for contest "
            f"({contest_batches[contest_batch][0]['CVR']['name']}) "
            f"uid={contest_batches[contest_batch][0]['CVR']['uid']}, "
            f"tally={contest_batches[contest_batch][0]['CVR']['tally']}, "
            f"max={the_tally.get('max')}, "
            f"win-by>{the_tally.get('win-by')}"
            )
        # Tally all the contests for this contest
#        import pdb; pdb.set_trace()
        try:
            the_tally.tallyho(contest_batches[contest_batch])
            # Print stuff
            the_tally.print_results()
        except TallyException as tally_error:
            error(f"[ERROR]: {tally_error}  "
                  "Continuing with other contests ...")

if __name__ == '__main__':
    args = parse_arguments()
    main()

# EOF
