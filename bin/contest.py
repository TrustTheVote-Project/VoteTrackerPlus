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
from logging import debug
from fractions import Fraction
# local
from exceptions import TallyException

class Contest:
    """A wrapper around the rules of engagement regarding a specific contest"""

    # Legitimate Contest keys.  Note 'selection', 'uid', 'cloak', and
    # 'name' are not legitimate keys for blank ballots
    _config_keys = ['choices', 'tally', 'win-by', 'max', 'write-in']
    _blank_ballot_keys = _config_keys + ['uid']
    _cast_keys = _blank_ballot_keys + ['selection', 'name', 'cast_branch', 'ggo']
    _choice_keys = ['name', 'party']

    # A simple numerical n digit uid
    _uids = {}
    _nextuid = 0

    @staticmethod
    def set_uid(a_contest_blob, ggo):
        """Will add a contest uid (only good within the context of this
        specific election) to the supplied contest.
        """
        name = next(iter(a_contest_blob))
        if 'uid' in a_contest_blob[name]:
            raise IndexError(f"The uid of contest {name} is already set")
        a_contest_blob[name]['uid'] = str(Contest._nextuid).rjust(4, '0')
        if Contest._nextuid not in Contest._uids:
            Contest._uids[Contest._nextuid] = {}
        Contest._uids[Contest._nextuid]['name'] = name
        Contest._uids[Contest._nextuid]['ggo'] = ggo
        Contest._nextuid += 1

    @staticmethod
    def check_contest_choices(choices):
        """Will validate the syntax of the contest choice"""
        for choice in choices:
            if isinstance(choice, str):
                continue
            if isinstance(choice, dict):
                bad_keys = [key for key in choice if key not in Contest._choice_keys]
                if bad_keys:
                    raise KeyError(
                        "the following keys are not valid Contest choice keys: "
                        f"{','.join(bad_keys)}")
                continue
            if isinstance(choice, bool):
                continue

    @staticmethod
    def check_contest_blob_syntax(a_contest_blob, filename='', digest='',
                                      accept_all_keys=False):
        """
        Will check the synatx of a contest somewhat and conveniently
        return the contest name
        """
        ### ZZZ - should sanity check the name
        name = next(iter(a_contest_blob))

        if filename:
            legal_fields = Contest._blank_ballot_keys
        elif digest or accept_all_keys:
            legal_fields = Contest._cast_keys
        else:
            legal_fields = Contest._config_keys
        bad_keys = [key for key in a_contest_blob[name] if key not in legal_fields]
        if bad_keys:
            if filename:
                raise KeyError(f"File ({filename}): "
                               "the following keys are not valid Contest keys: "
                               f"{','.join(bad_keys)}")
            if digest:
                raise KeyError(f"Commit digest ({digest}): "
                               "the following keys are not valid Contest keys: "
                               f"{','.join(bad_keys)}")
            raise KeyError("the following keys are not valid Contest keys: "
                           f"{','.join(bad_keys)}")
        # Need to validate choices sub data structure as well
        Contest.check_contest_choices(a_contest_blob[name]['choices'])
        # good enough
        return name

    @staticmethod
    def check_cvr_blob_syntax(a_cvr_blob, filename='', digest=''):
        """
        Will check the synatx of a cvr
        """
        bad_keys = [key for key in a_cvr_blob if key not in Contest._cast_keys]
        if bad_keys:
            if filename:
                raise KeyError(f"File ({filename}): "
                               "the following keys are not valid Contest keys: "
                               f"{','.join(bad_keys)}")
            if digest:
                raise KeyError(f"Commit digest ({digest}): "
                               "the following keys are not valid Contest keys: "
                               f"{','.join(bad_keys)}")
            raise KeyError("the following keys are not valid Contest keys: "
                           f"{','.join(bad_keys)}")
        # Need to validate choices sub data structure as well
        Contest.check_contest_choices(a_cvr_blob['choices'])

    @staticmethod
    def get_choices_from_contest(choices):
        """Will smartly return just the pure list of choices sans all
        values and sub dictionaries.  An individual choice can either
        be a simple string, a regulare 1D dictionary, or it turns out
        a bool.
        """
        # Returns a pure list of choices sans any other values or sub dictionaries
        if isinstance(choices[0], str):
            return choices
        if isinstance(choices[0], dict):
            return [entry['name'] for entry in choices]
        if isinstance(choices[0], bool):
            return ['true', 'false'] if choices[0] else ['false', 'true']
        raise ValueError(f"unknown/unsupported contest choices data structure ({choices})")

    def __init__(self, a_contest_blob, ggo, contests_index, accept_all_keys=False):
        """Construct the object placing the contest info in an attribute
        while recording the meta data
        """
        self.name = Contest.check_contest_blob_syntax(
            a_contest_blob, '', accept_all_keys=accept_all_keys)
        self.contest = a_contest_blob[self.name]
        self.ggo = ggo
        self.index = contests_index
        self.cast_branch = ""
        self.cloak = False
        # set defaults
        if 'max' not in self.contest:
            if self.contest['tally'] == 'plurality':
                self.contest['max'] = 1
        # Some constructor time sanity checks
        if 'max' in self.contest and self.contest['max'] < 1:
            raise ValueError(f"Illegal value for Contest max ({self.contest['max']}) "
                                 "- must be greater than 0")

    def __str__(self):
        """Return the contest contents as a print-able json string - careful ..."""
        # Note - keep cloak out of it until proven safe to include
        contest_dict = {
            key: self.contest[key] for key in Contest._cast_keys if key in self.contest}
        contest_dict.update({'name': self.name, 'ggo': self.ggo, 'cast_branch': self.cast_branch})
        return json.dumps(contest_dict, sort_keys=True, indent=4, ensure_ascii=False)

    def get(self, name):
        """Generic getter - can raise KeyError"""
        # Return the choices
        if name == 'dict':
            # return the combined psuedo dictionary similar to __str__ above
            contest_dict = \
                { key: self.contest[key] for key in Contest._cast_keys if key in self.contest }
            contest_dict.update(
                {'name': self.name, 'ggo': self.ggo, 'cast_branch': self.cast_branch})
            return contest_dict
        if name == 'choices':
            return Contest.get_choices_from_contest(self.contest['choices'])
        # Return contest 'meta' data
        if name in ['name', 'ggo', 'index', 'contest']:
            return getattr(self, name)
        # Else return contest data indexed by name
        return getattr(self, 'contest')[name]

    def set(self, name, value):
        """Generic setter - need to be able to set the cast_branch when committing the contest"""
        if name in ['name', 'ggo', 'index', 'contest', 'cast_branch', 'cloak']:
            setattr(self, name, value)
            return
        raise ValueError(f"Illegal value for Contest attribute ({name})")

class Tally:
    """
    A class to tally ballot contests a.k.a. CVRs.  The three primary
    functions of the class are the contructor, a tally function, and a
    print-the-tally function.
    """

    @staticmethod
    def get_choices_from_round(choices, what=''):
        """Will smartly return just the pure list of choices sans all
        values and sub dictionaries from a round
        """
        if what == 'count':
            return [choice[1] for choice in choices]
        return [choice[0] for choice in choices]

    def __init__(self, a_git_cvr):
        """Given a contest as parsed from the git log, a.k.a the
        contest digest and CVR json payload, will construct a Tally.
        A tally object can validate and tally a contest.

        Note - the constructor is per specific contest and tally
        results of the contest are stored in an attribute of the
        object.
        """
        self.digest = a_git_cvr['digest']
        self.contest = a_git_cvr['CVR']
        Contest.check_cvr_blob_syntax(self.contest, digest=self.digest)
        # Something to hold the actual tallies
        self.selection_counts = \
            {choice: 0 for choice in Contest.get_choices_from_contest(self.contest['choices'])}
        # Total vote count for this contest
        self.vote_count = 0
        # Ordered list of winners
        self.winner_order = []
        # Used in both plurality and rcv, but only round 0 is used in
        # plurality.  Note - rcv_round's are an ordered list of tuples,
        # not an ordered list of lists or dictionaries.
        self.rcv_round = []
        self.rcv_round.append([])

        # win-by and max are optional but have known defaults.
        # Determine the win-by if is not specified by the
        # ElectionConfig.
        self.defaults = {}
        self.defaults['max'] = 1 if 'max' not in self.contest else self.contest['max']
        self.defaults['win-by'] = (1.0 / float(1 + self.defaults['max'])) \
            if 'win-by' not in self.contest else Fraction(self.contest['win-by'])

        # At this point any contest tallied against this contest must
        # match all the fields with the exception of selection and
        # write-in, but that check is done in tallyho below.
        if not (self.contest['tally'] == 'plurality' or self.contest['tally'] == 'rcv'):
            raise NotImplementedError(
                f"the specified tally ({self.contest['tally']}) is not yet implemented")

    def get(self, name):
        """Simple limited functionality getter"""
        if name in ['max', 'win-by']:
            return self.defaults[name]
        if name in ['digest', 'contest', 'selection_counts',
                    'vote_count', 'winner_order', 'rcv_round']:
            return getattr(self, name)
        raise NameError(f"Name {name} not accepted/defined for Tally.get()")

    def __str__(self):
        """Return the Tally in a partially print-able json string - careful ..."""
        # Note - keep cloak out of it until proven safe to include
        tally_dict = {
            'name': self.contest['name'],
            'vote_count': self.vote_count,
            'winner_order': self.winner_order}
        return json.dumps(tally_dict, sort_keys=True, indent=4, ensure_ascii=False)

    def select_from_choices(self, selection):
        """Will smartly return just the pure selection name sans all
        values and sub dictionaries from a round
        """
        pick = self.contest['choices'][selection]
        if isinstance(pick, str):
            return pick
        if isinstance(pick, dict):
            return pick['name']
        if isinstance(pick, bool):
            return 'true' if pick else 'false'
        raise ValueError(f"unknown/unsupported contest choices data structure ({choices})")

    def tallyho(self, contest_batch):
        """
        Will verify and tally the suppllied unique contest across all
        the CVRs.
        """
        def tally_a_plurality_contest(contest):
            """plurality tally"""
            for count in range(self.defaults['max']):
                if 0 <= count < len(contest['selection']):
                    # yes this can be one line, but the reader may
                    # be interested in verifying the explicit
                    # values
                    selection = contest['selection'][count]
                    choice = Contest.get_choices_from_contest(contest['choices'])[selection]
                    self.selection_counts[choice] += 1
                    self.vote_count += 1
                    debug(
                        f"Vote (plurality): contest={contest['name']} "
                        f"choice={choice} selection={selection}")
                else:
                    debug(f"Vote (plurality): contest={contest['name']} BLANK")

        def tally_a_rcv_contest(contest):
            """RCV tally"""
            if len(contest['selection']):
                # the voter can still leave a RCV contest blank
                selection = contest['selection'][0]
                choice = Contest.get_choices_from_contest(contest['choices'])[selection]
                self.selection_counts[choice] += 1
                self.vote_count += 1
                debug(
                    f"Vote (RCV): contest={contest['name']} "
                    f"choice={choice} (selection={selection})")
            else:
                debug(f"Vote (RCV): contest={contest['name']} BLANK")

        def handle_another_rcv_round(this_round, last_place_name):
            """For the lowest vote getter, for those CVR's that have
            that as their current first/active-round choice, will
            slice off that choice off and re-count the now first
            selection choice (if there is one)
            """
            debug(f"RCV: round {this_round}")
            # Safety check
            if this_round > 64:
                raise TallyException("RCV rounds exceeded safety limit of 64 rounds")
            if last_place_name == None or last_place_name == '':
                raise TallyException("RCV rounds error - cannot pop null")
            # Execute a RCV round
            for uid in contest_batch:
                contest = uid['CVR']
                digest = uid['digest']
                if self.select_from_choices(contest['selection'][0]) == last_place_name:
                    # Remove the current first choice of this contest
                    contest['selection'].pop(0)
                    # decrement the last_place_name by one
                    self.selection_counts[last_place_name] -= 1
                    if len(contest['selection']):
                        debug(
                            f"RCV: {digest} last-place pop and count "
                            f"({last_place_name} -> "
                            f"{self.select_from_choices(contest['selection'][0])})")
                        # the voter can still leave a RCV contest blank
                        # Note - selection is the new selection for this contest
                        selection = contest['selection'][0]
                        # Need to select from self.contest['choices']
                        # as that is the set-in-stone ordering
                        # w.r.t. selection
#                        import pdb; pdb.set_trace()
                        choice = self.select_from_choices(selection)
                        self.selection_counts[choice] += 1
                        self.vote_count += 1
                        debug(f"Vote (RCV): contest={contest['name']} choice={choice} "
                                  f"selection={selection}")
                    else:
                        debug(f"RCV: {digest} last-place pop and count ({last_place_name} -> BLANK")
            # Order the winners of this round.  This is a tuple, not a
            # list or dict.
#            import pdb; pdb.set_trace()
            self.rcv_round[this_round] = sorted(
                self.selection_counts.items(), key=operator.itemgetter(1), reverse=True)
            # Create the next round list
            self.rcv_round.append([])
            # See if there is a wiinner and if so record it
            for choice in Tally.get_choices_from_round(self.rcv_round[this_round]):
                # Note the test is '>' and NOT '>='
                if float(self.selection_counts[choice]) /\
                    float(self.vote_count) > self.defaults['win-by']:
                    # A winner.  Depending on the win-by (which is a
                    # function of max), there could be multiple
                    # winners in this round.
                    self.winner_order.append({choice: self.selection_counts[choice]})
            # If there are anough winners, stop and return
            if len(self.winner_order) >= self.defaults['max']:
                return
            # If not, safely determine the next last_place_name and execute a RCV round
            if self.rcv_round[this_round][-1] == self.rcv_round[this_round][-2]:
                # There are two last_place_name choices - will need more
                # code to handle this situation post MVP development
                raise TallyException(
                    f"There are two last place choices in contest ({contest}), "
                    f"round ({this_round}).  The code for this is not yet implemented.")
            handle_another_rcv_round(this_round + 1, self.rcv_round[this_round][-1][0])
            return

        def parse_all_contests():
            """Will parse all the contests validating each"""
            errors = {}
            for a_git_cvr in contest_batch:
                contest = a_git_cvr['CVR']
                digest = a_git_cvr['digest']
                Contest.check_cvr_blob_syntax(contest, digest=digest)
                # Validate the values that should be the same as self
                for field in ['choices', 'tally', 'win-by', 'max', 'ggo', 'uid', 'name']:
                    if field in self.contest:
                        if self.contest[field] != contest[field]:
                            errors[digest].append(
                                f"{field} field does not match: "
                                f"{self.contest[field]} != {contest[field]}")
                    elif field in contest:
                        errors[digest].append(
                            f"{field} field is not present in Tally object but "
                            "is present in digest")
                # Tally the contest - this is just the first pass of a
                # tally.  It just so happens that with pluraity tallies
                # the tally can be completed with s single pass over over
                # the CVRs.  And that can be done here.  But with more
                # complicated tallies such as RCV, the additional passes
                # are done outside of this for loop.
                if contest['tally'] == 'plurality':
                    tally_a_plurality_contest(contest)
                elif contest['tally'] == 'rcv':
                    # Since this is the first round on a rcv tally, just
                    # grap the first selection
                    tally_a_rcv_contest(contest)
                else:
                    # This code block should never be executed as the
                    # constructor or the Validate values clause above will
                    # catch this type of error.  It is here only as a
                    # safety check during development time when adding
                    # support for more tallies.
                    raise NotImplementedError(
                        f"the specified tally ({contest['tally']}) is not yet implemented")

            # Will the potential CVR errors found, report them all
            if errors:
                raise TallyException(
                    "The following CVRs have structural errors:"
                    f"{errors}")

        # Read all the contests, validate, and count votes
        debug("RCV: round 0")
        parse_all_contests()

        # For all tallies order what has been counted so far (a tuple)
        self.rcv_round[0] = sorted(
            self.selection_counts.items(), key=operator.itemgetter(1), reverse=True)
        self.rcv_round.append([])

        # If plurality, the tally is done
        if self.contest['tally'] == 'plurality':
            # record the winner order
            self.winner_order = self.rcv_round[0]
            return

        # The rest of this block handles RCV

        # When max=1 there is only one RCV winner.  However, not only
        # can max>1 but win-by might be 2/3 and not just a simple
        # majority.

        # See if done by first determining if there are enough winning
        # selection counts
        for choice in Tally.get_choices_from_round(self.rcv_round[0]):
            # Note the test is '>' and NOT '>='
            if float(self.selection_counts[choice]) /\
              float(self.vote_count) > self.defaults['win-by']:
                # A winner.  Depending on the win-by (which is a
                # function of max), there could be multiple
                # winners in this round.
                self.winner_order.append((choice, self.selection_counts[choice]))

        # If there are anough winners, stop and return.  Otherwise,
        # start RCV rounds.
        if self.winner_order and len(self.winner_order) >= self.defaults['max']:
            return

        # The first or more RCV winners need to be determined.  Loop
        # until we have enough RCV winners regardless of win-by as it
        # may work out the last round only includes enough winners of
        # which one or more may may not 1/max votes ...

        # Safely determine the next last_place_name and execute a RCV round
        if Tally.get_choices_from_round(self.rcv_round[0], 'count')[-1] == \
          Tally.get_choices_from_round(self.rcv_round[0], 'count')[-2]:
            # There are two last_place_name choices - will need
            # more code to handle this situation post the MVP demo
            raise TallyException(
                f"There are two last place choices in contest ({self.contest['name']}) "
                f"(uid={self.contest['uid']}) in the first round.  "
                "The code for this is not yet implemented.")
#        import pdb; pdb.set_trace()
        last_place_name = Tally.get_choices_from_round(self.rcv_round[0])[-1]
        handle_another_rcv_round(1, last_place_name)

    def print_results(self, syntax=None):
        """Will print the results of the tally"""
        print(f"Contest {self.contest['name']} (uid={self.contest['uid']}):")
#        import pdb; pdb.set_trace()
        for winner_blob in self.winner_order:
            print(f"  {winner_blob[0]} : {winner_blob[1]}")

# EOF
