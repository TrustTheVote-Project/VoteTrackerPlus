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
Library backend for command line level script to merge CVR contest
branches into the master branch

See 'run_mock_election.py -h' for usage information.
"""

# Standard imports
import logging
import os
import time

# Script modules
from vtp.ops.accept_ballot_operation import AcceptBallotOperation
from vtp.ops.cast_ballot_operation import CastBallotOperation
from vtp.ops.merge_contests_operation import MergeContestsOperation
from vtp.ops.tally_contests_operation import TallyContestsOperation

# Local libraries
from vtp.utils.address import Address
from vtp.utils.ballot import Ballot
from vtp.utils.common import Common, Globals, Shellout
from vtp.utils.election_config import ElectionConfig


class RunMockElectionOperation:
    """
    A class to wrap the run_mock_election.py script.  Constructor
    takes a complete list of valid arguments (either as a type
    Namespace or dict).
    """

    def __init__(self, parsed_args):
        """Only to module-ize the scripts and keep things simple and idiomatic."""
        self.parsed_args = parsed_args

    def scanner_mockup(self, the_election_config, ballot):
        """Simulate a VTP scanner"""

        election_data_dir = os.path.join(
            the_election_config.get("git_rootdir"),
            Globals.get("ROOT_ELECTION_DATA_SUBDIR"),
        )

        # Get list of available blank ballots
        blank_ballots = []
        if ballot:
            # a blank ballot location was specified (either directly or via an address)
            blank_ballots.append(ballot)
        else:
            with Shellout.changed_cwd(election_data_dir):
                for dirpath, _, files in os.walk("."):
                    for filename in [
                        f
                        for f in files
                        if f.endswith(",ballot.json")
                        and dirpath.endswith("blank-ballots/json")
                    ]:
                        blank_ballots.append(os.path.join(dirpath, filename))
        # Loop over the list N times
        if not blank_ballots:
            raise ValueError("found no blank ballots to cast")
        for count in range(self.parsed_args.iterations):
            for blank_ballot in blank_ballots:
                logging.debug(
                    "Iteration %s of %s - processing %s",
                    count,
                    self.parsed_args.iterations,
                    blank_ballot,
                )
                # - cast a ballot
                #            import pdb; pdb.set_trace()
                with Shellout.changed_cwd(election_data_dir):
                    Shellout.run(
                        ["git", "pull"],
                        printonly=self.parsed_args.printonly,
                        verbosity=self.parsed_args.verbosity,
                        no_touch_stds=True,
                        timeout=None,
                        check=True,
                    )
                cast_ballot = CastBallotOperation(
                    {
                        "blank_ballot": blank_ballot,
                        "demo_mode": True,
                        "verbosity": self.parsed_args.verbosity,
                        "printonly": self.parsed_args.printonly,
                    }
                )
                cast_ballot.run()
                # - accept the ballot
                accept_ballot = AcceptBallotOperation(
                    {
                        "cast_ballot": Ballot.get_cast_from_blank(blank_ballot),
                        "verbosity": self.parsed_args.verbosity,
                        "printonly": self.parsed_args.printonly,
                    }
                )
                accept_ballot.run()
                if self.parsed_args.device == "both":
                    # - merge the ballot's contests
                    if self.parsed_args.flush_mode == 2:
                        # Since casting and merging is basically
                        # synchronous, no need for an extra large timeout
                        merge_contests = MergeContestsOperation(
                            {
                                "flush_mode": True,
                                "verbosity": self.parsed_args.verbosity,
                                "printonly": self.parsed_args.printonly,
                            }
                        )
                        merge_contests.run()
                    else:
                        # Should only need to merge one ballot worth of
                        # contests - also no need for an extra large
                        # timeout
                        merge_contests = MergeContestsOperation(
                            {
                                "minimum_cast_cache": self.parsed_args.minimum_cast_cache,
                                "verbosity": self.parsed_args.verbosity,
                                "printonly": self.parsed_args.printonly,
                            }
                        )
                        merge_contests.run()
                    # don't let too much garbage build up
                    if count % 10 == 9:
                        Shellout.run(
                            ["git", "gc"],
                            printonly=self.parsed_args.printonly,
                            verbosity=self.parsed_args.verbosity,
                            no_touch_stds=True,
                            timeout=None,
                            check=True,
                        )
        if self.parsed_args.device == "both":
            # merge the remaining contests
            # Note - this needs a longer timeout as it can take many seconds
            merge_contests = MergeContestsOperation(
                {
                    "flush_mode": True,
                    "verbosity": self.parsed_args.verbosity,
                    "printonly": self.parsed_args.printonly,
                }
            )
            merge_contests.run()
            # tally the contests
            tally_contests = TallyContestsOperation(
                {
                    "verbosity": self.parsed_args.verbosity,
                    "printonly": self.parsed_args.printonly,
                }
            )
            tally_contests.run()
        # clean up git just in case
        Shellout.run(
            ["git", "gc"],
            printonly=self.parsed_args.printonly,
            verbosity=self.parsed_args.verbosity,
            no_touch_stds=True,
            timeout=None,
            check=True,
        )

    def server_mockup(self, the_election_config):
        """Simulate a VTP server"""
        # This is the VTP server simulation code.  In this case, the VTP
        # scanners are pushing to an ElectionData remote and this (server)
        # needs to pull from the ElectionData remote.  And, in this case
        # the branches to be merged are remote and not local.
        start_time = time.time()
        # Loop for a day and sleep for 10 seconds
        seconds = 60 * self.parsed_args.duration
        election_data_dir = os.path.join(
            the_election_config.get("git_rootdir"),
            Globals.get("ROOT_ELECTION_DATA_SUBDIR"),
        )

        while True:
            with Shellout.changed_cwd(election_data_dir):
                Shellout.run(
                    ["git", "pull"],
                    self.parsed_args.printonly,
                    self.parsed_args.verbosity,
                    no_touch_stds=True,
                    timeout=None,
                    check=True,
                )
            if self.parsed_args.flush_mode == 2:
                merge_contests = MergeContestsOperation(
                    {
                        "remote": True,
                        "flush": True,
                        "verbosity": self.parsed_args.verbosity,
                        "printonly": self.parsed_args.printonly,
                    }
                )
                merge_contests.run()
                tally_contests = TallyContestsOperation(
                    {
                        "verbosity": self.parsed_args.verbosity,
                        "printonly": self.parsed_args.printonly,
                    }
                )
                tally_contests.run()
                return
            merge_contests = MergeContestsOperation(
                {
                    "remote": True,
                    "minimum_cast_cache": self.parsed_args.minimum_cast_cache,
                    "verbosity": self.parsed_args.verbosity,
                    "printonly": self.parsed_args.printonly,
                }
            )
            merge_contests.run()
            logging.info("Sleeping for 10")
            time.sleep(10)
            elapsed_time = time.time() - start_time
            if elapsed_time > seconds:
                break
        if self.parsed_args.flush_mode in [1, 2]:
            print("Cleaning up remaining unmerged ballots")
            merge_contests = MergeContestsOperation(
                {
                    "remote": True,
                    "flush": True,
                    "verbosity": self.parsed_args.verbosity,
                    "printonly": self.parsed_args.printonly,
                }
            )
            merge_contests.run()
        # tally the contests
        tally_contests = TallyContestsOperation(
            {
                "verbosity": self.parsed_args.verbosity,
                "printonly": self.parsed_args.printonly,
            }
        )
        tally_contests.run()

    ################
    # main
    ################
    # pylint: disable=duplicate-code
    def run(self):
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

        # Configure logging
        Common.configure_logging(self.parsed_args.verbosity)

        # Create a VTP ElectionData object if one does not already exist
        the_election_config = ElectionConfig.configure_election()

        # If an address was used, use that
        if (
            self.parsed_args.address
            or self.parsed_args.state
            or self.parsed_args.town
            or self.parsed_args.substreet
        ):
            the_address = Address.create_address_from_args(
                self.parsed_args,
                [
                    "blank_ballot",
                    "device",
                    "minimum_cast_cache",
                    "flush_mode",
                    "iterations",
                    "duration",
                    "verbosity",
                    "printonly",
                ],
            )
            the_address.map_ggos(the_election_config)
            blank_ballot = the_election_config.gen_blank_ballot_location(
                the_address.active_ggos, the_address.ballot_subdir
            )
        elif self.parsed_args.blank_ballot:
            blank_ballot = self.parsed_args.blank_ballot

        # the VTP scanner mock simulation
        if self.parsed_args.device in ["scanner", "both"]:
            self.scanner_mockup(the_election_config, blank_ballot)
        else:
            self.server_mockup(the_election_config)

    # End Of Class


# EOF
