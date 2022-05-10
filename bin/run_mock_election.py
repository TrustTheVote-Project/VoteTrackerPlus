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
import os
import sys
import time
import argparse
import logging
from logging import debug, info

# Local import
from common import Globals, Shellout
from ballot import Ballot
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
    across the available blank ballots found in the ElectionData.

    One basic idea is to run this in different windows, one per VTP
    scanner.  The scanner is nominally associated with a town (as
    configured).

    When "-d scanner" is supplied, run_mock_election.py will randomly
    cast and scan ballots.  It will loop over all available/existing
    blank ballots found in the ElectionData.

    When "-d server" is supplied, run_mock_election.py will
    synchronously run the merge_contests.py program which will once
    every 10 seconds.  Note that nominally 100 contgests need to have
    been pushed for merge_contests.py to merge in a contest into the
    master branch.

    If "-d both" is supplied, run_mock_election.py will run a single
    scanner N iterations while also calling the server function.
    run_mock_election.py will then flush the ballot cache before
    printing the tallies and exiting.
    """,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument(
        "-d", "--device", default="",
        help="specify a specific VC local device (scanner or server or both) to mock")
    parser.add_argument(
        "-m", "--minimum_cast_cache", type=int, default=100,
        help="the minimum number of cast ballots required prior to merging (def=100)")
    parser.add_argument(
        "-f", "--flush", action='store_true',
        help="will (force) flush the remaining unmerged contest branches during merge_contests")
    parser.add_argument(
        "-i", "--iterations", type=int, default=10,
        help="the number of unique blank ballots to cast (def=10)")
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
    if parsed_args.device not in ['scanner', 'server', 'both']:
        raise ValueError("The --device parameter only accepts 'device' or 'server' "
                         f"or 'both' - ({parsed_args.device}) was suppllied.")
    return parsed_args

def scanner_mockup(election_data_dir):
    """Simulate a VTP scanner"""
    # Get list of available blank ballots
    blank_ballots = []
    with Shellout.changed_cwd(election_data_dir):
        for dirpath, _, files in os.walk("."):
            for filename in [f for f in files if f.endswith(",ballot.json") \
                    and dirpath.endswith("blank-ballots/json") ]:
                blank_ballots.append(os.path.join(dirpath, filename))
    # Loop over the list N times
    if not blank_ballots:
        raise ValueError("found no blank ballots to cast")
    for count in range(args.iterations):
        for blank_ballot in blank_ballots:
            debug(f"Iteration {count}, processing {blank_ballot}")
            # - cast a ballot
#            import pdb; pdb.set_trace()
            Shellout.run(
                ['./cast_ballot.py', '--blank_ballot=' + blank_ballot, '--demo_mode'],
                args.printonly)
            # - accept the ballot
            Shellout.run(
                ['./accept_ballot.py',
                     '--cast_ballot=' + Ballot.get_cast_from_blank(blank_ballot)],
                args.printonly)
            if args.device == 'both':
                # - merge the ballot's contests
                if args.flush:
                    # Since casting and merging is basically
                    # synchronous, no need for an extra large timeout
                    Shellout.run(['./merge_contests.py', '-f'], args.printonly,
                                     verbosity=args.verbosity, timeout=300)
                else:
                    # Should only need to merge one ballot worth of
                    # contests - also no need for an extra large
                    # timeout
                    Shellout.run(['./merge_contests.py', '-m',
                                    args.minimum_cast_cache], args.printonly,
                                    verbosity=args.verbosity, timeout=300)
                # don't let too much garbage build up
                if count % 10 == 9:
                    Shellout.run(['git', 'gc'], args.printonly)
    if args.device == 'both':
        # merge the remaining contests
        # Note - this needs a longer timeout as it can take many seconds
        Shellout.run(
            ['./merge_contests.py', '-f'],
            args.printonly, verbosity=args.verbosity, timeout=None)
        # tally the contests
        Shellout.run(['./tally_contests.py'], args.printonly)
    # clean up git just in case
    Shellout.run(['git', 'gc'], args.printonly)

def server_mockup(election_data_dir):
    """Simulate a VTP server"""
    # This is the VTP server simulation code.  In this case, the VTP
    # scanners are pushing to an ElectionData remote and this (server)
    # needs to pull from the ElectionData remote.  And, in this case
    # the branches to be merged are remote and not local.
    start_time = time.time()
    # Loop for a day and sleep for 10 seconds
    seconds = 3600 * 24
    while True:
        with Shellout.changed_cwd(election_data_dir):
            Shellout.run(['git', 'pull'], args.printonly)
        if args.flush:
            Shellout.run(['./merge_contests.py', '-r', '-f'], args.printonly,
                             verbosity=args.verbosity, timeout=None)
            Shellout.run(['./tally_contests.py'], args.printonly)
            return
        Shellout.run(['./merge_contests.py', '-r', '-m',
                          args.minimum_cast_cache], args.printonly,
                         verbosity=args.verbosity, timeout=None)
        info("Sleeping for 10")
        time.sleep(10)
        elapsed_time = time.time() - start_time
        if elapsed_time > seconds:
            break
    print("Cleaning up remaining unmerged ballots")
    Shellout.run(
        ['./merge_contests.py', '-r', '-f'],
        printonly=args.printonly, verbosity=args.verbosity, timeout=None)
    # tally the contests
    Shellout.run(['./tally_contests.py'], args.printonly)


################
# main
################
# pylint: disable=duplicate-code
def main():
    """Main function - see -h for more info"""

    # Create an VTP election config object (this will perform an early
    # check on the ElectionData)
    the_election_config = ElectionConfig()
    the_election_config.parse_configs()
    election_data_dir = os.path.join(
        the_election_config.get('git_rootdir'), Globals.get('ROOT_ELECTION_DATA_SUBDIR'))

    # Note - this is a serial synchronous mock election loop.  A
    # parallel loop would have one VTP server git workspace somewhere
    # and N VTP scanner workspaces someplace else.  Depending on the
    # network topology, it is also possible to start up VTP scanner
    # workspaces on other machines as long as the git remotes and
    # clones are properly configured (with access etc).

    # While a mock election is running, it is also possible to use yet
    # another VTP scanner workspace to personally cast/insert
    # individual ballots for interactive purposes.

    # Assumes that each supplied town already has the blank ballots
    # generated and/or already committed.

    # the VTP scanner mock simulation
    if args.device in ['scanner', 'both']:
        scanner_mockup(election_data_dir)
    else:
        server_mockup(election_data_dir)

if __name__ == '__main__':
    args = parse_arguments()
    main()

# EOF
