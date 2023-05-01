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

# Project imports
from vtp.core.ballot import Ballot
from vtp.core.common import Shellout
from vtp.core.contest import Tally
from vtp.core.election_config import ElectionConfig
from vtp.core.exceptions import TallyException

# Local imports
from .operation import Operation


# pylint: disable=too-few-public-methods
class TallyContestsOperation(Operation):
    """
    A class to implememt the tally-contests operation.  See the
    tally-contests help output or read the parse_argument argparse
    description (immediately below this) in the source file.
    """

    # pylint: disable=duplicate-code
    def run(
        self,
        contest_uid: str = "",
        track_contests: str = "",
    ) -> list:
        """Main function - see -h for more info"""

        # Create a VTP ElectionData object if one does not already exist
        the_election_config = ElectionConfig.configure_election(self.election_data_dir)

        # git pull the ElectionData repo so to get the latest set of
        # remote CVRs branches
        a_ballot = Ballot()
        with Shellout.changed_cwd(a_ballot.get_cvr_parent_dir(the_election_config)):
            Shellout.run(["git", "pull"], verbosity=self.verbosity, check=True)

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
            if contest_uid != "":
                if contest_batches[contest_batch][0]["CVR"]["uid"] != contest_uid:
                    continue
            # Create a Tally object for this specific contest
            the_tally = Tally(contest_batches[contest_batch][0], self.imprimir)
            self.imprimir(
                f"Scanned {len(contest_batches[contest_batch])} contests "
                f"for contest ({contest_batches[contest_batch][0]['CVR']['name']}) "
                f"uid={contest_batches[contest_batch][0]['CVR']['uid']}, "
                f"tally={contest_batches[contest_batch][0]['CVR']['tally']}, "
                f"max={the_tally.get('max')}, "
                f"win-by>{the_tally.get('win-by')}"
            )
            # Tally all the contests for this contest
            #        import pdb; pdb.set_trace()
            try:
                the_tally.tallyho(contest_batches[contest_batch], track_contests)
                # Print stuff
                the_tally.print_results()
            except TallyException as tally_error:
                self.imprimir(f"[ERROR]: {tally_error}")
                self.imprimir("Continuing with other contests ...")
        # can always return the output
        return self.stdout_output


# EOF
