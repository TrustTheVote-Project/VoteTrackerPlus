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
Library backend to command line level script to tally the contests of
a election.

See 'tally_contests.py -h' for usage information.
"""

# Standard imports
import logging

# Local imports
from vtp.utils.ballot import Ballot
from vtp.utils.common import Common, Shellout
from vtp.utils.contest import Tally
from vtp.utils.election_config import ElectionConfig
from vtp.utils.exceptions import TallyException


# pylint: disable=too-few-public-methods
class TallyContestsOperation:
    """A class to wrap the tally_contests.py script."""

    def __init__(self, parsed_args):
        """Only to module-ize the scripts and keep things simple and idiomatic."""
        self.parsed_args = parsed_args

    ################
    # main
    ################
    # pylint: disable=duplicate-code
    def run(self):
        """Main function - see -h for more info"""

        # Configure logging
        Common.configure_logging(self.parsed_args.verbosity)

        # Create a VTP ElectionData object if one does not already exist
        the_election_config = ElectionConfig.configure_election()

        # git pull the ElectionData repo so to get the latest set of
        # remote CVRs branches
        a_ballot = Ballot()
        with Shellout.changed_cwd(a_ballot.get_cvr_parent_dir(the_election_config)):
            Shellout.run(
                ["git", "pull"], verbosity=self.parsed_args.verbosity, check=True
            )

        # Will process all the CVR commits on the master branch and tally
        # all the contests found.  Note - even if a contest is specified,
        # as a first pass it is easier to just perform a git log across
        # all the contests and then filter later for the contest of
        # interest than to try to create a git grep query against the CVR
        # payload.
        contest_batches = Shellout.cvr_parse_git_log_output(
            ["git", "log", "--topo-order", "--no-merges", "--pretty=format:%H%B"],
            the_election_config,
        )

        # Note - though plurality voting can be counted within the above
        # loop, tallies such as rcv cannot.  So far now, just count
        # everything in a separate loop.
        for contest_batch in sorted(contest_batches):
            # Maybe skip
            if self.parsed_args.contest_uid != "":
                if (
                    contest_batches[contest_batch][0]["CVR"]["uid"]
                    != self.parsed_args.contest_uid
                ):
                    continue
            # Create a Tally object for this specific contest
            the_tally = Tally(contest_batches[contest_batch][0])
            logging.info(
                "Scanned %s contests for contest (%s) uid=%s, tally=%s, max=%s, win-by>%s",
                len(contest_batches[contest_batch]),
                contest_batches[contest_batch][0]["CVR"]["name"],
                contest_batches[contest_batch][0]["CVR"]["uid"],
                contest_batches[contest_batch][0]["CVR"]["tally"],
                the_tally.get("max"),
                the_tally.get("win-by"),
            )
            # Tally all the contests for this contest
            #        import pdb; pdb.set_trace()
            try:
                the_tally.tallyho(
                    contest_batches[contest_batch], self.parsed_args.track_contests
                )
                # Print stuff
                the_tally.print_results()
            except TallyException as tally_error:
                logging.error(
                    "[ERROR]: %s\nContinuing with other contests ...", tally_error
                )

    # End Of Class


# EOF
