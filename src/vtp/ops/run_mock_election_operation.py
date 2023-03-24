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
Logic of operation for running a mock election.  See the --help output
or the README.md file in the src/vtp directory for details.
"""

# Standard imports
import logging
import os
import time

# Project imports
from vtp.core.address import Address
from vtp.core.ballot import Ballot
from vtp.core.common import Shellout
from vtp.core.election_config import ElectionConfig
from vtp.ops.accept_ballot_operation import AcceptBallotOperation
from vtp.ops.cast_ballot_operation import CastBallotOperation
from vtp.ops.merge_contests_operation import MergeContestsOperation
from vtp.ops.tally_contests_operation import TallyContestsOperation

# Local imports
from .operation import Operation


class RunMockElectionOperation(Operation):
    """
    A class to implememt the run-mock-election operation.  See the
    run-mock-election help output or read the parse_argument argparse
    description (immediately below this) in the source file.
    """

    def __init__(self, election_data_dir: str, verbosity: int, printonly: bool):
        """
        Primarily to module-ize the scripts and keep things simple,
        idiomatic, and in different namespaces.
        """
        super().__init__(election_data_dir, verbosity, printonly)

    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-branches
    # problem child
    def scanner_mockup(
        self,
        the_election_config: ElectionConfig,
        ballot: str,
        iterations: int,
        device: str,
        flush_mode: int,
        minimum_cast_cache: int,
        duration: int,
    ):
        """Simulate a VTP scanner"""

        # Get list of available blank ballots
        blank_ballots = []
        if ballot:
            # a blank ballot location was specified (either directly or via an address)
            blank_ballots.append(ballot)
        else:
            with Shellout.changed_cwd(the_election_config.get("git_rootdir")):
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
        start_time = time.time()
        seconds = 60 * duration
        count = 0
        while True:
            count += 1
            for blank_ballot in blank_ballots:
                if duration:
                    logging.info(
                        "Iteration %s - processing %s",
                        count,
                        blank_ballot,
                    )
                else:
                    logging.info(
                        "Iteration %s of %s - processing %s",
                        count,
                        iterations,
                        blank_ballot,
                    )
                # - cast a ballot
                #            import pdb; pdb.set_trace()
                with Shellout.changed_cwd(the_election_config.get("git_rootdir")):
                    Shellout.run(
                        ["git", "pull"],
                        printonly=self.printonly,
                        verbosity=self.verbosity,
                        no_touch_stds=True,
                        timeout=None,
                        check=True,
                    )
                cast_ballot = CastBallotOperation(
                    self.election_data_dir,
                    self.verbosity,
                    self.printonly,
                )
                cast_ballot.run(
                    blank_ballot=blank_ballot,
                    demo_mode=True,
                )
                # - accept the ballot
                accept_ballot = AcceptBallotOperation(
                    self.election_data_dir,
                    self.verbosity,
                    self.printonly,
                )
                accept_ballot.run(
                    cast_ballot=Ballot.get_cast_from_blank(blank_ballot),
                )
                if device == "both":
                    # - merge the ballot's contests
                    if flush_mode == 2:
                        # Since casting and merging is basically
                        # synchronous, no need for an extra large timeout
                        merge_contests = MergeContestsOperation(
                            self.election_data_dir,
                            self.verbosity,
                            self.printonly,
                        )
                        merge_contests.run(
                            flush=True,
                        )
                    else:
                        # Should only need to merge one ballot worth of
                        # contests - also no need for an extra large
                        # timeout
                        merge_contests = MergeContestsOperation(
                            self.election_data_dir,
                            self.verbosity,
                            self.printonly,
                        )
                        merge_contests.run(
                            minimum_cast_cache=minimum_cast_cache,
                        )
                    # don't let too much garbage build up
                    if count % 10 == 9:
                        Shellout.run(
                            ["git", "gc"],
                            printonly=self.printonly,
                            verbosity=self.verbosity,
                            no_touch_stds=True,
                            timeout=None,
                            check=True,
                        )
            if iterations and count >= iterations:
                break
            if seconds:
                elapsed_time = time.time() - start_time
                if elapsed_time > seconds:
                    break
        if device == "both":
            # merge the remaining contests
            # Note - this needs a longer timeout as it can take many seconds
            merge_contests = MergeContestsOperation(
                self.election_data_dir,
                self.verbosity,
                self.printonly,
            )
            merge_contests.run(
                flush=True,
            )
            # tally the contests
            tally_contests = TallyContestsOperation(
                self.election_data_dir,
                self.verbosity,
                self.printonly,
            )
            tally_contests.run()
        # clean up git just in case
        Shellout.run(
            ["git", "gc"],
            printonly=self.printonly,
            verbosity=self.verbosity,
            no_touch_stds=True,
            timeout=None,
            check=True,
        )

    def server_mockup(
        self,
        the_election_config: ElectionConfig,
        flush_mode: int,
        duration: int,
        minimum_cast_cache: int,
        iterations: int,
    ):
        """Simulate a VTP server"""
        # This is the VTP server simulation code.  In this case, the VTP
        # scanners are pushing to an ElectionData remote and this (server)
        # needs to pull from the ElectionData remote.  And, in this case
        # the branches to be merged are remote and not local.
        start_time = time.time()
        # Loop for a day and sleep for 10 seconds
        seconds = 60 * duration
        count = 0

        while True:
            count += 1
            with Shellout.changed_cwd(the_election_config.get("git_rootdir")):
                Shellout.run(
                    ["git", "pull"],
                    self.printonly,
                    self.verbosity,
                    no_touch_stds=True,
                    timeout=None,
                    check=True,
                )
            if flush_mode == 2:
                merge_contests = MergeContestsOperation(
                    self.election_data_dir,
                    self.verbosity,
                    self.printonly,
                )
                merge_contests.run(
                    remote=True,
                    flush=True,
                )
                tally_contests = TallyContestsOperation(
                    self.election_data_dir,
                    self.verbosity,
                    self.printonly,
                )
                tally_contests.run()
                return
            merge_contests = MergeContestsOperation(
                self.election_data_dir,
                self.verbosity,
                self.printonly,
            )
            merge_contests.run(
                remote=True,
                minimum_cast_cache=minimum_cast_cache,
            )
            if iterations and count >= iterations:
                break
            logging.info("Sleeping for 10 (iteration=%s)", count)
            time.sleep(10)
            elapsed_time = time.time() - start_time
            if elapsed_time > seconds:
                break
        if flush_mode in [1, 2]:
            print("Cleaning up remaining unmerged ballots")
            merge_contests = MergeContestsOperation(
                self.election_data_dir,
                self.verbosity,
                self.printonly,
            )
            merge_contests.run(
                remote=True,
                flush=True,
            )
        # tally the contests
        tally_contests = TallyContestsOperation(
            self.election_data_dir,
            self.verbosity,
            self.printonly,
        )
        tally_contests.run()

    # pylint: disable=duplicate-code
    # pylint: disable=too-many-arguments
    def run(
        self,
        an_address: Address = None,
        blank_ballot: str = "",
        device: str = "",
        minimum_cast_cache: int = 100,
        flush_mode: int = 0,
        iterations: int = 10,
        duration: int = 0,
    ):
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

        # Create a VTP ElectionData object if one does not already exist
        the_election_config = ElectionConfig.configure_election(self.election_data_dir)

        # If an address was used, use that
        if an_address is not None:
            an_address.map_ggos(the_election_config)
            blank_ballot = the_election_config.gen_blank_ballot_location(
                an_address.active_ggos, an_address.ballot_subdir
            )

        # the VTP scanner mock simulation
        if device in ["scanner", "both"]:
            self.scanner_mockup(
                the_election_config=the_election_config,
                ballot=blank_ballot,
                iterations=iterations,
                device=device,
                flush_mode=flush_mode,
                minimum_cast_cache=minimum_cast_cache,
                duration=duration,
            )
        elif device == "server":
            self.server_mockup(
                the_election_config=the_election_config,
                flush_mode=flush_mode,
                duration=duration,
                minimum_cast_cache=minimum_cast_cache,
                iterations=iterations,
            )
        else:
            raise ValueError(f"an illegal value was supplied for device ({device})")


# EOF
