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
from address import Address
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
    cast and scan ballots.

    When "-d server" is supplied, run_mock_election.py will
    synchronously run the merge_contests.py program which will once
    every 10 seconds.  Note that nominally 100 contgests need to have
    been pushed for merge_contests.py to merge in a contest into the
    master branch without the --flush_mode option.

    If "-d both" is supplied, run_mock_election.py will run a single
    scanner N iterations while also calling the server function.  If
    --flush_mode is set to 1 or 2, run_mock_election.py will then
    flush the ballot cache before printing the tallies and exiting.

    By default run_mock_election.py will loop over all available blank
    ballots found withint the ElectionData tree.  However, either a
    specific blank ballot or an address can be specified to limit the
    mock to a single ballot N times.
    """,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    Address.add_address_args(parser)
    parser.add_argument("--blank_ballot",
                            help="overrides an address - specifies the specific blank ballot")
    parser.add_argument(
        "-d", "--device", default="",
        help="specify a specific VC local device (scanner or server or both) to mock")
    parser.add_argument(
        "-m", "--minimum_cast_cache", type=int, default=100,
        help="the minimum number of cast ballots required prior to merging (def=100)")
    parser.add_argument(
        "-f", "--flush_mode", type=int, default=0,
        help="will either not flush (0), flush on exit (1), or flush on each iteration (2)")
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
    if parsed_args.flush_mode not in [0, 1, 2]:
        raise ValueError("The value of flush_mode must be either 0, 1, or 2"
                             f" - {parsed_args.flush_mode} was supplied.")
    return parsed_args

def scanner_mockup(election_data_dir, bin_dir, ballot):
    """Simulate a VTP scanner"""

    # Get list of available blank ballots
    blank_ballots = []
    if ballot:
        # a blank ballot location was specified (either directly or via an address)
        blank_ballots.append(ballot)
    else:
        with Shellout.changed_cwd(election_data_dir):
            for dirpath, _, files in os.walk("."):
                for filename in [f for f in files if f.endswith(",ballot.json") \
                        and dirpath.endswith("blank-ballots/json") ]:
                    blank_ballots.append(os.path.join(dirpath, filename))
    # Loop over the list N times
    if not blank_ballots:
        raise ValueError("found no blank ballots to cast")
    merge_contests = os.path.join(bin_dir, 'merge_contests.py')
    for count in range(args.iterations):
        for blank_ballot in blank_ballots:
            debug(f"Iteration {count} of {args.iterations} - processing {blank_ballot}")
            # - cast a ballot
#            import pdb; pdb.set_trace()
            with Shellout.changed_cwd(election_data_dir):
                Shellout.run(
                    ['git', 'pull'],
                    printonly=args.printonly, verbosity=args.verbosity,
                    no_touch_stds=True, timeout=None, check=True)
            Shellout.run(
                [os.path.join(bin_dir, 'cast_ballot.py'), '--blank_ballot=' + blank_ballot,
                     '--demo_mode'],
                printonly=args.printonly, verbosity=args.verbosity, no_touch_stds=True,
                timeout=None, check=True)
            # - accept the ballot
            Shellout.run(
                [os.path.join(bin_dir, 'accept_ballot.py'),
                     '--cast_ballot=' + Ballot.get_cast_from_blank(blank_ballot)],
                args.printonly, args.verbosity, no_touch_stds=True,
                timeout=None, check=True)
            if args.device == 'both':
                # - merge the ballot's contests
                if args.flush_mode == 2:
                    # Since casting and merging is basically
                    # synchronous, no need for an extra large timeout
                    Shellout.run(
                        [merge_contests, '-f'], printonly=args.printonly,
                        verbosity=args.verbosity, no_touch_stds=True, timeout=None,
                        check=True)
                else:
                    # Should only need to merge one ballot worth of
                    # contests - also no need for an extra large
                    # timeout
                    Shellout.run(
                        [merge_contests, '-m', args.minimum_cast_cache],
                        printonly=args.printonly, verbosity=args.verbosity,
                        no_touch_stds=True, timeout=None, check=True)
                # don't let too much garbage build up
                if count % 10 == 9:
                    Shellout.run(
                        ['git', 'gc'], printonly=args.printonly,
                        verbosity=args.verbosity, no_touch_stds=True, timeout=None,
                        check=True)
    if args.device == 'both':
        # merge the remaining contests
        # Note - this needs a longer timeout as it can take many seconds
        Shellout.run(
            [merge_contests, '-f'], printonly=args.printonly,
            verbosity=args.verbosity, no_touch_stds=True, timeout=None, check=True)
        # tally the contests
        Shellout.run(
            [os.path.join(bin_dir, 'tally_contests.py')], printonly=args.printonly,
            verbosity=args.verbosity, no_touch_stds=True, timeout=None, check=True)
    # clean up git just in case
    Shellout.run(
        ['git', 'gc'], printonly=args.printonly, verbosity=args.verbosity,
        no_touch_stds=True, timeout=None, check=True)

def server_mockup(election_data_dir, bin_dir):
    """Simulate a VTP server"""
    # This is the VTP server simulation code.  In this case, the VTP
    # scanners are pushing to an ElectionData remote and this (server)
    # needs to pull from the ElectionData remote.  And, in this case
    # the branches to be merged are remote and not local.
    start_time = time.time()
    # Loop for a day and sleep for 10 seconds
    seconds = 3600 * 24
    merge_contests = os.path.join(bin_dir, 'merge_contests.py')
    tally_contests = os.path.join(bin_dir, 'tally_contests.py')
    while True:
        with Shellout.changed_cwd(election_data_dir):
            Shellout.run(['git', 'pull'], args.printonly,
            args.verbosity, no_touch_stds=True, timeout=None, check=True)
        if args.flush_mode == 2:
            Shellout.run(
                [merge_contests, '-r', '-f'], args.printonly,
                args.verbosity, no_touch_stds=True, timeout=None, check=True)
            Shellout.run(
                [tally_contests], args.printonly,
                args.verbosity, no_touch_stds=True, timeout=None, check=True)
            return
        Shellout.run(
            [merge_contests, '-r', '-m', args.minimum_cast_cache], args.printonly,
            args.verbosity, no_touch_stds=True, timeout=None, check=True)
        info("Sleeping for 10")
        time.sleep(10)
        elapsed_time = time.time() - start_time
        if elapsed_time > seconds:
            break
    if args.flush_mode in [1, 2]:
        print("Cleaning up remaining unmerged ballots")
        Shellout.run(
            [merge_contests, '-r', '-f'], args.printonly,
            args.verbosity, no_touch_stds=True, timeout=None, check=True)
    # tally the contests
    Shellout.run(
        [tally_contests], args.printonly,
        args.verbosity, no_touch_stds=True, timeout=None, check=True)


################
# main
################
# pylint: disable=duplicate-code
def main():
    """Main function - see -h for more info

    Note - this is a serial synchronous mock election loop.  A
    parallel loop would have one VTP server git workspace somewhere
    and N VTP scanner workspaces someplace else.  Depending on the
    network topology, it is also possible to start up VTP scanner
    workspaces on other machines as long as the git remotes and clones
    are properly configured (with access etc).

    While a mock election is running, it is also possible to use yet
    another VTP scanner workspace to personally cast/insert individual
    ballots for interactive purposes.

    Assumes that each supplied town already has the blank ballots
    generated and/or already committed.
    """

    # Create an VTP election config object (this will perform an early
    # check on the ElectionData)
    the_election_config = ElectionConfig()
    the_election_config.parse_configs()
    election_data_dir = os.path.join(
        the_election_config.get('git_rootdir'), Globals.get('ROOT_ELECTION_DATA_SUBDIR'))

    # If an address was used, use that
    if args.address or args.state or args.town or args.substreet:
        the_address = Address.create_address_from_args(
            args, ['blank_ballot', 'device', 'minimum_cast_cache', 'flush_mode',
                       'iterations', 'verbosity', 'printonly'])
        the_address.map_ggos(the_election_config)
        blank_ballot = the_address.gen_blank_ballot_location(the_election_config)
    elif args.blank_ballot:
        blank_ballot = args.blank_ballot

    # Eventually need the bin dir as well
    bin_dir = os.path.join(the_election_config.get('git_rootdir'), 'bin')
    # the VTP scanner mock simulation
    if args.device in ['scanner', 'both']:
        scanner_mockup(election_data_dir, bin_dir, blank_ballot)
    else:
        server_mockup(election_data_dir, bin_dir)

if __name__ == '__main__':
    args = parse_arguments()
    main()

# EOF
