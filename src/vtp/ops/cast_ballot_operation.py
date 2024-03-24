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
Logic of operation for casting a ballot.  Normally this is
interactive, but it can also just return the blank ballot so that some
other client/voter can fill it in.  If so, that file will need to be
supplied to accept-ballot to generate the ballot check and add it to
the Merkle tree.
"""

# Standard imports
import pprint
import random

import pyinputplus

# Project imports
from vtp.core.address import Address
from vtp.core.ballot import Ballot, BlankBallot
from vtp.core.contest import Contest
from vtp.core.election_config import ElectionConfig

# Local imports
from .operation import Operation


class CastBallotOperation(Operation):
    """
    A class to implememt the cast-ballot operation.  See the
    cast-ballot help output or read the parse_argument argparse
    description (immediately below this) in the source file.
    """

    def make_random_selection(self, the_ballot, the_contest):
        """Will randomly make selections on a contest"""
        # get the possible choices
        choices = the_contest.get("choices")
        tally = the_contest.get("tally")
        picks = list(range(len(choices)))
        # For plurality and max=1, the first choice is the only
        # choice.  For plurality and max>1, the order does not matter
        # - a selection is a selection.  For RCV, the order does
        # matter as that is the ranking.
        #
        # Choose something randomly
        random.shuffle(picks)
        if "plurality" == tally:
            loop = the_contest.get("max")
        elif "rcv" == tally:
            loop = len(choices)
        else:
            raise KeyError(f"Unspoorted tally ({tally})")
        while loop > 0:
            #            import pdb; pdb.set_trace()
            the_ballot.add_selection(the_contest, picks.pop(0))
            loop -= 1

    def get_user_selection(self, the_ballot, the_contest, count, total_contests):
        """Print the contest and get the selection(s) from the user"""
        choices = the_contest.get("choices")
        tally = the_contest.get("tally")
        max_votes = the_contest.get("max")
        # Print something
        print(f"################ ({count} of {total_contests})")
        print(f"Contest {the_contest.get('uid')}: {the_contest.get('name')}")
        if tally == "plurality":
            print(f"- This is a {tally} tally")
            print(
                f"- The voting is for {max_votes} open "
                f"position{'s'[:max_votes^1]}/choice{'s'[:max_votes^1]} - "
                f"only {max_votes} selection{'s'[:max_votes^1]} can be choosen."
            )
        else:
            print(
                f"- This is a {tally} tally with {max_votes} open "
                f"position{'s'[:max_votes^1]}/choice{'s'[:max_votes^1]}.  "
                f"Up to {len(choices)} selection{'s'[:len(choices)^1]} can be rank choosen."
            )

        # Need to print the choices first up front
        count = 0
        for choice_index, choice in enumerate(choices):
            # If it is a ticket, need to pretty print the ticket
            #            import pdb; pdb.set_trace()
            if the_contest.is_contest_a_ticket_choice(choice_index):
                print(
                    f"  [{count}] {choice} - {the_contest.pretty_print_ticket(choice_index)}"
                )
            else:
                print(f"  [{count}] {choice}")
            count += 1

        def validate_multichoice(text):
            """Will validate the space separated user input choice
            string.  Note - this is never called by this code - it is passed to
            pyinputplus.inputCustom as a function.  As such it technically not an
            instance method and does not have a self.
            """
            selections = text.split()
            choice_max = len(choices)
            errors = []
            validated_selections = []
            for num in selections:
                if not num.isnumeric():
                    errors.append(f"The supplied choice ({num}) is not a number")
                    continue
                num = int(num)
                if num < 0 or num > choice_max:
                    errors.append(
                        f"The supplied choice ({num}) is not a valid selection "
                        f"(must be between 0 and {choice_max - 1} inclusive)"
                    )
                    continue
                if tally == "plurality" and len(selections) > choice_max:
                    errors.append(
                        f"This contest is limited to at most {max_votes} selection(s): "
                        f"you supplied {len(selections)}"
                    )
                    continue
                #            import pdb; pdb.set_trace()
                if num in validated_selections:
                    errors.append(
                        f"The selection {num} was supplied more than once.  "
                        "Each selection can only be supplied once."
                    )
                    continue
                validated_selections.append(num)
            if errors:
                err_string = "\n".join(errors)
                raise ValueError(
                    "Warning - you selections have the following errors\n"
                    f"{err_string}"
                )
            # If still here, set the selection.  Since it is possible to self
            # adjudicate a contest, always explicitly clear the selection
            # before adding
            the_ballot.clear_selection(the_contest)
            for sel in validated_selections:
                the_ballot.add_selection(the_contest, sel)

        if tally == "plurality":
            if max_votes > 1:
                prompt = (
                    f"Please enter the numbers for your choices (max={max_votes}) "
                    "separated by spaces: "
                )
            else:
                prompt = "Please enter the number for your choice: "
            pyinputplus.inputCustom(validate_multichoice, prompt=prompt, blank=True)
        else:
            # Then prompt for input
            prompt = "Please enter in rank order the numbers of your choices separated by spaces: "
            pyinputplus.inputCustom(validate_multichoice, prompt=prompt, blank=True)

    # pylint: disable=too-many-branches
    def loop_over_contests(self, a_ballot, demo_mode):
        """Will loop over the contests in a ballot and either ask the user
        for a choice or if in demo mode will randomly choose one.
        """
        contests = a_ballot.get("contests")
        total_contests = len(contests)
        count = 0
        contest_uids = []
        for contest in contests:
            contest_uids.append(contest.get("uid"))
            if demo_mode:
                self.make_random_selection(a_ballot, contest)
            else:
                # Display the tally type and choices and allow the user to manually
                # enter something.  Might as well validate legal selections (in
                # this demo) as that is the long-term VTP vision.
                count += 1
                self.get_user_selection(a_ballot, contest, count, total_contests)
        # pylint: disable=too-many-nested-blocks
        if not demo_mode:
            # UX wise replicate the self adjudication experince.  This is
            # basically another endless loop until done
            while True:
                # Print the selections
                for contest in contests:
                    print(f"Contest {contest.get('uid')} - {contest.get('name')}:")
                    # Loop over selections - there can be more than
                    # one but they are ALWAYS ordered
                    if len(contest.get("selection")) == 0:
                        print(
                            "    ATTENTION - no selection was made and "
                            "you are casting an empty vote!"
                        )
                    else:
                        for selection in contest.get("selection"):
                            #                        import pdb; pdb.set_trace()
                            offset, name = Contest.split_selection(selection)
                            if contest.is_contest_a_ticket_choice(offset):
                                print(
                                    f"    {contest.pretty_print_ticket(offset)} - {name}"
                                )
                            else:
                                print(f"    {name}")
                prompt = (
                    "Is this correct?  "
                    "Enter yes to accept the ballot, no to reject the ballot: "
                )
                if "yes" == pyinputplus.inputYesNo(prompt):
                    break
                prompt = (
                    "Enter a contest uid to redo that contest, "
                    "enter nothing (leave blank and hit enter) to start completely over: "
                )
                response = pyinputplus.inputChoice(contest_uids + [""], prompt)
                if response == "":
                    count = 0
                    for contest in contests:
                        count += 1
                        self.get_user_selection(
                            a_ballot, contest, count, total_contests
                        )
                else:
                    for contest in contests:
                        if contest.get("uid") == response:
                            self.get_user_selection(a_ballot, contest, 1, 1)
                            break
        # For a convenient side effect, return the contests
        return contests

    def run(
        self,
        an_address: Address = None,
        blank_ballot: str = "",
        demo_mode: bool = False,
        return_bb: bool = False,
    ) -> str:
        """Main function - see -h for more info"""

        # Create a VTP ElectionData object if one does not already exist
        the_election_config = ElectionConfig.configure_election(
            self, self.election_data_dir
        )

        # Create a ballot
        a_ballot = BlankBallot(self)

        # process the provided address
        if blank_ballot:
            # Read the specified blank_ballot
            with self.changed_cwd(the_election_config.get("git_rootdir")):
                a_ballot.read_a_blank_ballot("", the_election_config, blank_ballot)
        else:
            if isinstance(an_address, str):
                # need to convert the csv string to an Address
                an_address = Address(csv=an_address)
            # Use the specified address
            an_address.map_ggos(the_election_config)
            # get the ballot for the specified address
            a_ballot.read_a_blank_ballot(an_address, the_election_config)

        if return_bb:
            return a_ballot

        # If still here, prompt the user to vote for each contest
        contests = self.loop_over_contests(a_ballot, demo_mode)
        self.imprimir(
            f"And the ballot looks like:\n{pprint.pformat(a_ballot.dict())}", 5
        )

        # Validate at least something
        a_ballot.verify_cast_ballot_data(the_election_config)

        if self.printonly:
            ballot_file = Ballot.gen_cast_ballot_location(
                the_election_config, a_ballot.get("ballot_subdir")
            )
        else:
            ballot_file = a_ballot.write_a_cast_ballot(the_election_config)
        # example of digging deeply into ElectionConfig data ...
        #    import pdb; pdb.set_trace()
        voting_centers = the_election_config.get_node(
            a_ballot.get("ballot_node"), "config"
        )["voting centers"]
        for vote_center in voting_centers:
            self.imprimir(
                f"Casting a {contests.len()} contest ballot at VC {vote_center}", 3
            )
            self.imprimir(f"Cast ballot file: {ballot_file}", 3)
        # return the cast ballot location
        return ballot_file


# EOF
