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

"""Logic of operation for tallying contests."""

# Standard imports
import logging

# Local imports
from vtp.core.ballot import Ballot
from vtp.core.common import Common, Shellout
from vtp.core.contest import Tally
from vtp.core.election_config import ElectionConfig
from vtp.core.exceptions import TallyException

from .operation import Operation


# pylint: disable=too-few-public-methods
class TallyContestsOperation(Operation):
    """Implementation of 'tally-contests' operation."""

    def __init__(
        self,
        contest_uid: str = "",
        # TODO: Use 'list[str]''
        track_contests: str = "",
        do_not_pull: bool = False,
        **base_options,
    ):
        """Create a tally contest operation."""
        super().__init__(**base_options)
        self._contest_uid = contest_uid
        self._track_contests = track_contests
        self._do_not_pull = do_not_pull

    # pylint: disable=duplicate-code
    def run(self):
        # Configure logging
        Common.configure_logging(self._verbosity)

        # Create a VTP ElectionData object if one does not already exist
        the_election_config = ElectionConfig.configure_election()

        # git pull the ElectionData repo so to get the latest set of
        # remote CVRs branches
        a_ballot = Ballot()
        with Shellout.changed_cwd(a_ballot.get_cvr_parent_dir(the_election_config)):
            Shellout.run(["git", "pull"], verbosity=self._verbosity, check=True)

        # Will process all the CVR commits on the main branch and tally
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
            if self._contest_uid != "":
                if contest_batches[contest_batch][0]["CVR"]["uid"] != self._contest_uid:
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
            try:
                the_tally.tallyho(contest_batches[contest_batch], self._track_contests)
                # Print stuff
                the_tally.print_results()
            except TallyException as tally_error:
                logging.error(
                    "[ERROR]: %s\nContinuing with other contests ...", tally_error
                )
