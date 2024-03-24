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

"""How to manage a VTP specific contest"""

import json
import operator
from fractions import Fraction

# local
from .contest import Contest
from .exceptions import TallyException


# pylint: disable=too-many-instance-attributes # (8/7 - not worth it at this time)
class Tally:
    """
    A class to tally ballot contests a.k.a. CVRs.  The three primary
    functions of the class are the contructor, a tally function, and a
    print-the-tally function.
    """

    @staticmethod
    def get_choices_from_round(choices, what: str = ""):
        """Will smartly return just the pure list of choices sans all
        values and sub dictionaries from a round
        """
        if what == "count":
            return [choice[1] for choice in choices]
        return [choice[0] for choice in choices]

    def __init__(self, a_git_cvr: dict, operation_self: dict):
        """Given a contest as parsed from the git log, a.k.a the
        contest digest and CVR json payload, will construct a Tally.
        A tally object can validate and tally a contest.

        Note - the constructor is per specific contest and tally
        results of the contest are stored in an attribute of the
        object.

        The operation_self is how STDOUT is being handled as defined by
        the outer ops class/object.  That object just passes down its
        print function to the Tally constructor so that each (contest)
        tally can handle printing as desired.
        """
        #        import pdb; pdb.set_trace()
        self.operation_self = operation_self
        self.digest = a_git_cvr["digest"]
        self.contest = a_git_cvr["CVR"]
        Contest.check_contest_blob_syntax(self.contest, digest=self.digest)
        # Something to hold the actual tallies.  During RCV rounds these
        # will change with last place finishers being decremented to 0.
        self.selection_counts = {
            choice: 0
            for choice in Contest.get_choices_from_contest(self.contest["choices"])
        }
        # Total vote count for this contest.  RCV rounds will not effect
        # this.
        self.vote_count = 0
        # Ordered list of winners - a list of tuples and not dictionaries.
        self.winner_order = []
        # Used in both plurality and rcv, but only round 0 is used in
        # plurality.  Note - rcv_round's are an ordered list of tuples
        # as is winner_order.  The code below expects the current round
        # (beginning as an empty list) to exist within the list.
        self.rcv_round = []
        self.rcv_round.append([])

        # win_by and max are optional but have known defaults.
        # Determine the win_by if is not specified by the
        # ElectionConfig.
        self.defaults = {}
        self.defaults["max"] = 1 if "max" not in self.contest else self.contest["max"]
        self.defaults["win_by"] = (
            (1.0 / float(1 + self.defaults["max"]))
            if "win_by" not in self.contest
            else Fraction(self.contest["win_by"])
        )

        # Need to keep track of a selections/choices that are no longer
        # viable - key=choice['name'] value=obe round
        self.obe_choices = {}

        # At this point any contest tallied against this contest must
        # match all the fields with the exception of selection and
        # write-in, but that check is done in tallyho below.
        if not (self.contest["tally"] == "plurality" or self.contest["tally"] == "rcv"):
            raise NotImplementedError(
                f"the specified tally ({self.contest['tally']}) is not yet implemented"
            )

    def get(self, name: str):
        """Simple limited functionality getter"""
        # ZZZ import pdb; pdb.set_trace()
        if name in ["max", "win_by"]:
            return self.defaults[name]
        if name in [
            "digest",
            "contest",
            "selection_counts",
            "vote_count",
            "winner_order",
            "rcv_round",
        ]:
            return getattr(self, name)
        raise NameError(f"Name {name} not accepted/defined for Tally.get()")

    def __str__(self):
        """Return the Tally in a partially print-able json string - careful ..."""
        # Note - keep cloak out of it until proven safe to include
        tally_dict = {
            "name": self.contest["name"],
            "vote_count": self.vote_count,
            "winner_order": self.winner_order,
        }
        return json.dumps(tally_dict, sort_keys=True, indent=4, ensure_ascii=False)

    def select_name_from_choices(self, selection: str):
        """Will smartly return just the pure selection name sans all
        values and sub dictionaries from a round
        """
        pick = self.contest["choices"][Contest.extract_offest_from_selection(selection)]
        if isinstance(pick, str):
            return pick
        if isinstance(pick, dict):
            return pick["name"]
        if isinstance(pick, bool):
            return "True" if pick else "False"
        raise ValueError(f"unknown/unsupported contest choices data structure ({pick})")

    def tally_a_plurality_contest(
        self, contest: dict, provenance_digest: str, vote_count: int
    ):
        """plurality tally"""
        for count in range(self.defaults["max"]):
            if 0 <= count < len(contest["selection"]):
                # yes this can be one line, but the reader may
                # be interested in verifying the explicit
                # values
                selection = contest["selection"][count]
                # depending on version, selection could be an int or a string
                if isinstance(selection, str):
                    selection = Contest.extract_offest_from_selection(selection)
                choice = Contest.get_choices_from_contest(contest["choices"])[selection]
                self.selection_counts[choice] += 1
                self.vote_count += 1
                if provenance_digest:
                    self.operation_self.imprimir(
                        f"Counted {provenance_digest} as vote {vote_count}: choice={choice}",
                        0,
                    )
            else:
                if provenance_digest:
                    self.operation_self.imprimir(
                        f"No-vote {provenance_digest}: BLANK", 0
                    )

    def tally_a_rcv_contest(
        self, contest: dict, provenance_digest: str, vote_count: int
    ):
        """RCV tally"""
        if len(contest["selection"]):
            # the voter can still leave a RCV contest blank
            selection = contest["selection"][0]
            # depending on version, selection could be an int or a string
            if isinstance(selection, str):
                selection = Contest.extract_offest_from_selection(selection)
            choice = Contest.get_choices_from_contest(contest["choices"])[selection]
            self.selection_counts[choice] += 1
            self.vote_count += 1
            if provenance_digest:
                self.operation_self.imprimir(
                    f"Counted {provenance_digest} as vote {vote_count}: choice={choice}",
                    0,
                )
        else:
            if provenance_digest:
                self.operation_self.imprimir(f"No vote {provenance_digest}: BLANK", 0)

    def safely_determine_last_place_names(self, current_round: int) -> list:
        """Safely determine the next set of last_place_names for which
        to re-distribute the next RCV round of voting.  Can raise
        various exceptions.  If possible will return the
        last_place_names (which can be greater than length 1 if there
        is tie amongst the losers of a round).

        Note - it is up to the caller to resolve RCV edge cases such
        as multiple and simultaneous losers, a N-way tie of all
        remaining choices, returning a tie which undercuts the max
        number of votes (as in, pick 3 of 5 and a RCV round tie
        results in 1 or 2 choices instead of 3).
        """
        # Note - self.rcv_round[current_round] is the ordered array of
        # all RCV choice tuples
        self.operation_self.imprimir(f"{self.rcv_round[current_round]}", 3)

        # Step 1: remove self.obe_choices from current round
        working_copy = []
        for a_tuple in self.rcv_round[current_round]:
            if a_tuple[0] not in self.obe_choices:
                working_copy.append(a_tuple)

        # tep 2: walk the list backwards returning the set of counts
        # with the same minimum count.
        last_place_names = []
        previous_count = 0
        for offset, a_tuple in enumerate(reversed(working_copy)):
            # Note - current_round is 0 indexed from left, which means
            # it needs an additional decrement when indexing from the
            # right
            current_count = a_tuple[1]
            if offset == 0 or current_count == previous_count:
                last_place_names.append(a_tuple[0])
                previous_count = current_count
            else:
                break
        # import pdb; pdb.set_trace()
        return last_place_names

    def safely_remove_obe_selections(self, contest: dict):
        """For the specified contest, will 'pop' the current first place
        selection.  If the next selection is already a loser, will pop
        that as well.  self.contest['selection'] may or may not have any
        choices left (it can be empty, have one choice, or multiple
        choices left).

        Prints nothing - assumes caller handles any info/debug printing.
        """
        a_copy = contest["selection"].copy()
        for selection in a_copy:
            if (
                self.select_name_from_choices(selection) in self.obe_choices
                and selection in contest["selection"]
            ):
                contest["selection"].remove(selection)

    def restore_proper_rcv_round_ordering(self, this_round: int):
        """Restore the 'proper' ordering of the losers in the current
        and previous rcv rounds.  Note: at this point the
        self.rcv_round has been sorted by count with the obe_choices
        effectively randomized.  Also note that new incoming
        last_place_names are not yet in self.obe_choices and will not
        be until post the safely_determine_last_place_names call
        below.
        """
        loser_order = []
        for loser in sorted(
            self.obe_choices.items(), key=operator.itemgetter(1), reverse=True
        ):
            loser_order.append(loser)
        # Replace the effectively improperly unordered losers with a
        # properly ordered list of losers. One way is to replace the
        # last N entries with the properly ordered losers.
        if len(loser_order) > 1:
            for index, item in enumerate(reversed(loser_order)):
                self.rcv_round[this_round][-index - 1] = (item[0], 0)

    def get_total_vote_count(self, this_round: int):
        """
        To get the correct denominator to determine the minimum
        required win amount, all the _current_ candidate counts need
        to be added since some ballots may either be blank OR have
        less then the maximum number of rank choices.  Note -
        """
        return sum(
            self.selection_counts[choice]
            for choice in Tally.get_choices_from_round(self.rcv_round[this_round])
        )

    # pylint: disable=too-many-return-statements # what is a poor man to do
    def next_rcv_round_precheck(self, last_place_names: list, this_round: int) -> int:
        """
        Run the checks against the incoming last_place_names to make
        sure that it is ok to have another RCV round.  Returns non 0
        if no more rounds should be performed.
        """

        # 'this_round' is actually the 'next round' with the very
        # first round being round 0.  So, the first time this can be
        # called is the beginning of the second round (this_round =
        # 1).
        non_zero_count_choices = 0
        for choice in self.rcv_round[this_round - 1]:
            non_zero_count_choices += 1 if choice[1] else 0

        # If len(last_place_names) happens to be zero, raise an error.
        # However, though raising an error 'could be' the best test
        # prior to entering another round (calling this function
        # here), not raising an error and allowing such edge case tp
        # print the condition and simply return might be the better
        # design option.  Doing that.
        if not last_place_names:
            self.operation_self.imprimir(
                "No more choices/candidates to recast - no more RCV rounds", 0
            )
            return 1
        if this_round > 64:
            raise TallyException("RCV rounds exceeded safety limit of 64 rounds")
        if this_round >= len(self.rcv_round[0]):
            self.operation_self.imprimir("There are no more RCV rounds", 0)
            return 1
        if not non_zero_count_choices:
            self.operation_self.imprimir("There are no votes for any choice", 0)
            return 1
        if non_zero_count_choices < self.get("max"):
            self.operation_self.imprimir(
                f"There are only {non_zero_count_choices} viable choices "
                f"left which is less than the contest max ({self.get('max')})",
                0,
            )
            return 1
        if non_zero_count_choices == self.get("max"):
            self.operation_self.imprimir(
                f"The contest max number of choices ({self.get('max')}) has been reached",
                0,
            )
            return 1
        if non_zero_count_choices == 1:
            self.operation_self.imprimir(
                "There is only one remaining viable choice left - halting more RCV rounds",
                0,
            )
            return 1

        # Note - by the time the execution gets here, this rcv_round have been
        # vote count ordered.  But there could be any number of zero count
        # choices depending on the (edge case) details.

        # If len(last_place_names) leaves the exact number of max
        # choices left, this is a runner-up tie which is still ok -
        # return and print that.
        if non_zero_count_choices - len(last_place_names) == 0:
            self.operation_self.imprimir(
                f"This contest ends in a {non_zero_count_choices} way tie", 0
            )
            return 1

        # If len(last_place_names) leaves less than the max but one or
        # more choices left, this is a tie on losing.  Not sure what
        # to do, so print that and return.
        if non_zero_count_choices - len(last_place_names) < self.get("max"):
            self.operation_self.imprimir(
                f"There is a last place tie ({len(last_place_names)} way) which results "
                f"in LESS THAN the max ({non_zero_count_choices}) of choices",
                0,
            )
            return 1

        # And, the recursive stack here should probably be returning a
        # success/failure back out of the Contest.tallyho...
        return 0

    def recast_votes(self, last_place_names: list, contest_batch: list, checks: list):
        """
        Loops over the list of CVRs of interest (a contest worth) and
        recasts a voter's selection if that selection is a loser in
        this RCV round.  If there is no next choice, the there is no
        recast and the vote is dropped.
        """

        # Loop over CVRs
        for uid in contest_batch:
            contest = uid["CVR"]
            digest = uid["digest"]
            if digest in checks:
                self.operation_self.imprimir(
                    f"INSPECTING: {digest} (contest={contest['name']})", 4
                )
            # Note - if there is no selection, there is no selection
            if not contest["selection"]:
                continue
            for last_place_name in last_place_names:
                # Note - as the rounds go by, the
                # contest["selection"]'s will get trimmed to an empty
                # list.  Once empty, the vote/voter is done.
                if (
                    contest["selection"]
                    and self.select_name_from_choices(contest["selection"][0])
                    == last_place_name
                ):
                    # Safely pop the current first choice and reset
                    # contest['selection'].  Note that
                    # self.obe_choices has _already_ been updated with
                    # this_round's OBE in the caller such that
                    # safely_remove_obe_selections will effectively
                    # remove last_place_name from contest['selection']
                    self.safely_remove_obe_selections(contest)
                    # Regardless of the next choice, the current choice is decremented
                    self.selection_counts[last_place_name] -= 1
                    # Either retarget the vote or let it drop
                    if len(contest["selection"]):
                        # The voter can still leave a RCV contest blank
                        # Note - selection is the new selection for this contest
                        new_selection = contest["selection"][0]
                        # Select from self.contest['choices'] as that is the
                        # set-in-stone ordering w.r.t. selection
                        new_choice_name = self.select_name_from_choices(new_selection)
                        self.selection_counts[new_choice_name] += 1
                        # original variant: if digest in checks or loglevel == "DEBUG":
                        if digest in checks or self.operation_self.verbosity >= 4:
                            self.operation_self.imprimir(
                                f"RCV: {digest} (contest={contest['name']}) last place "
                                f"pop and count ({last_place_name} -> {new_choice_name})",
                                0,
                            )
                    else:
                        if digest in checks or self.operation_self.verbosity >= 4:
                            self.operation_self.imprimir(
                                f"RCV: {digest} (contest={contest['name']}) last place "
                                f"pop and drop ({last_place_name} -> BLANK)",
                                0,
                            )

    def handle_another_rcv_round(
        self, this_round: int, last_place_names: list, contest_batch: list, checks: list
    ):
        """For the lowest vote getter, for those CVR's that have
        that as their current first/active-round choice, will
        slice off that choice off and re-count the now first
        selection choice (if there is one)
        """
        self.operation_self.imprimir(f"RCV: round {this_round}", 0)

        # ZZZ - create a function to validate incoming last place
        # names and call that.  Maybe in the furure once more is know
        # support GLOBAL configs to determine how edge cases are
        # handled.  That function can cause a return if the the
        # current RCV tally should not proceed to more rounds.  Or
        # raise an RCV-tally error (which can be handled by the caller
        # when printing - prints a warning).
        if self.next_rcv_round_precheck(last_place_names, this_round):
            return

        # Loop over contest_batch and actually re-cast votes
        self.recast_votes(last_place_names, contest_batch, checks)
        # Order the winners of this round.  This is a tuple, not a
        # list or dict.  Note - the rcv round losers should not be
        # re-ordered as there is value to retaining that order
        self.rcv_round[this_round] = sorted(
            self.selection_counts.items(), key=operator.itemgetter(1), reverse=True
        )
        self.restore_proper_rcv_round_ordering(this_round)
        # Create the next round list
        self.rcv_round.append([])
        # Get the correct current total vote count for this round
        total_current_vote_count = self.get_total_vote_count(this_round)
        self.operation_self.imprimir(f"Total vote count: {total_current_vote_count}", 0)
        for choice in Tally.get_choices_from_round(self.rcv_round[this_round]):
            # Note the test is '>' and NOT '>='
            if (
                float(self.selection_counts[choice]) / float(total_current_vote_count)
            ) > self.defaults["win_by"]:
                # A winner.  Depending on the win_by (which is a
                # function of max), there could be multiple
                # winners in this round.
                self.winner_order.append((choice, self.selection_counts[choice]))
        #        import pprint
        #        import pdb; pdb.set_trace()
        # If there are anough winners, stop and return
        if len(self.winner_order) >= self.defaults["max"]:
            return
        # If not, safely determine the next set of last_place_names and
        # execute another RCV round.
        last_place_names = self.safely_determine_last_place_names(this_round)
        # Add this loser to the obe record
        for last_place_name in last_place_names:
            self.obe_choices[last_place_name] = this_round
        self.handle_another_rcv_round(
            this_round + 1, last_place_names, contest_batch, checks
        )
        return

    def parse_all_contests(self, contest_batch: list, checks: list):
        """Will parse all the contests validating each"""
        errors = {}
        vote_count = 0
        for a_git_cvr in contest_batch:
            vote_count += 1
            contest = a_git_cvr["CVR"]
            digest = a_git_cvr["digest"]
            Contest.check_contest_blob_syntax(contest, digest=digest)
            # Maybe print an provenance log for the tally of this contest
            provenance_digest = digest if digest in checks else ""
            # Validate the values that should be the same as self
            for field in [
                "choices",
                "tally",
                "win_by",
                "max",
                "ggo",
                "uid",
                "name",
                "contest_type",
                "election_upstream_remote",
            ]:
                if field in self.contest:
                    if self.contest[field] != contest[field]:
                        errors[digest].append(
                            f"{field} field does not match: "
                            f"{self.contest[field]} != {contest[field]}"
                        )
                elif field in contest:
                    errors[digest].append(
                        f"{field} field is not present in Tally object but "
                        "is present in digest"
                    )
            # Tally the contest - this is just the first pass of a
            # tally.  It just so happens that with plurality tallies
            # the tally can be completed with a single pass over
            # the CVRs.  And that can be done here.  But with more
            # complicated tallies such as RCV, the additional passes
            # are done outside of this for loop.
            if contest["tally"] == "plurality":
                self.tally_a_plurality_contest(contest, provenance_digest, vote_count)
            elif contest["tally"] == "rcv":
                # Since this is the first round on a rcv tally, just
                # grap the first selection
                self.tally_a_rcv_contest(contest, provenance_digest, vote_count)
            else:
                # This code block should never be executed as the
                # constructor or the Validate values clause above will
                # catch this type of error.  It is here only as a
                # safety check during development time when adding
                # support for more tallies.
                raise NotImplementedError(
                    f"the specified tally ({contest['tally']}) is not yet implemented"
                )

        # Will the potential CVR errors found, report them all
        if errors:
            raise TallyException(
                "The following CVRs have structural errors:" f"{errors}"
            )

    def tallyho(
        self,
        contest_batch: list,
        checks: list,
    ):
        """
        Will verify and tally the suppllied unique contest across all
        the CVRs.  contest_batch is the list of contest CVRs from git
        and checks is a list of optional CVR digests (from the voter)
        to check.
        """
        # Read all the contests, validate, and count votes
        if self.contest["tally"] == "plurality":
            self.operation_self.imprimir("Plurality - one round", 0)
        else:
            self.operation_self.imprimir("RCV: round 0", 0)
        self.parse_all_contests(contest_batch, checks)

        # For all tallies order what has been counted so far (a tuple)
        self.rcv_round[0] = sorted(
            self.selection_counts.items(), key=operator.itemgetter(1), reverse=True
        )
        self.rcv_round.append([])

        # If plurality, the tally is done
        if self.contest["tally"] == "plurality":
            # record the winner order
            self.winner_order = self.rcv_round[0]
            return

        # The rest of this block handles RCV

        # See if another RCV round is necessary.  When max=1 there is
        # only one RCV winner.  However, not only can max>1 but win_by
        # might be 2/3 and not just a simple majority.  So only if there
        # are enough winners with enough votes is this contest done.

        # Get the correct current total vote count for this round
        total_current_vote_count = self.get_total_vote_count(0)
        self.operation_self.imprimir(f"Total vote count: {total_current_vote_count}", 0)

        # Determine winners if any ...
        for choice in Tally.get_choices_from_round(self.rcv_round[0]):
            # Note the test is '>' and NOT '>='
            if (
                float(self.selection_counts[choice]) / float(total_current_vote_count)
            ) > self.defaults["win_by"]:
                # A winner.  Depending on the win_by (which is a
                # function of max), there could be multiple
                # winners in this round.
                self.winner_order.append((choice, self.selection_counts[choice]))

        # If there are anough winners, stop and return.
        if self.winner_order and len(self.winner_order) >= self.defaults["max"]:
            return
        # More RCV rounds are needed.  Loop until we have enough RCV
        # winners.

        # Safely determine the next set of last_place_names and
        # execute a RCV round.  Note that all zero vote choices will
        # already be sorted last in self.rcv_round[0].
        last_place_names = self.safely_determine_last_place_names(0)
        for name in last_place_names:
            self.obe_choices[name] = 0
        # Go.  handle_another_rcv_round will return somehow at some point
        self.handle_another_rcv_round(1, last_place_names, contest_batch, checks)
        return

    def print_results(self):
        """Will print the results of the tally"""
        self.operation_self.imprimir(
            f"Final results for contest {self.contest['name']} (uid={self.contest['uid']}):",
            0,
        )
        #        import pdb; pdb.set_trace()
        # Note - better to print the last self.rcv_round than
        # self.winner_order since the former is a full count across all
        # choices while the latter is a partial list
        for result in self.rcv_round[-2]:
            self.operation_self.imprimir(f"  {result}")


# EOF
