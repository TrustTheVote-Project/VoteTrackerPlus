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
import re

# local
from .common import Globals


class Contest:
    """
    A class to handle the rules of engagement regarding a specific
    contest.  A contest is a dict.

    Some historical design notes.  A ballot originally had contests
    being a funky dict in version 0.1.0. However, in version 0.2.0
    contests was changed to an ordered list, greatly simplifying some
    low level logic.  The git log entry in 0.1.0 also ended up having
    an analogous dictionary with an outer "CVR" key.  This has also
    become OBE and so in 0.2.0 the git log entry is now just a simple
    one level dictionary.

    At the same time in an effort to simplify things, the contest
    selection logic was moved from the Ballot class to this class
    while changing the Ballot class to _always_ create Contest objects
    when it encounters a contest.
    """

    # Legitimate Contest keys.  Note 'selection', 'uid', 'cloak', and
    # 'name' are not legitimate keys for blank ballots
    _config_keys = [
        "choices",
        "tally",
        "win_by",
        "max",
        "write_in",
        "description",
        "contest_type",
        "ticket_titles",
        "election_upstream_remote",
        "contest_name",
        "ggo",
    ]
    _blank_ballot_keys = _config_keys + ["uid"]
    _cast_keys = _blank_ballot_keys + ["selection", "cast_branch"]
    _choice_keys = ["name", "party", "ticket_names"]

    # A simple numerical n digit uid
    _uids = {}
    _nextuid = 0

    @staticmethod
    def set_uid(a_contest_blob: dict, ggo: str):
        """Will add a contest uid (only good within the context of this
        specific election) to the supplied contest.
        """
        if "uid" in a_contest_blob:
            raise IndexError(
                f"The uid of contest {a_contest_blob['contest_name']} is already set"
            )
        a_contest_blob["uid"] = str(Contest._nextuid).rjust(4, "0")
        if Contest._nextuid not in Contest._uids:
            Contest._uids[Contest._nextuid] = {}
        Contest._uids[Contest._nextuid]["contest_name"] = a_contest_blob["contest_name"]
        Contest._uids[Contest._nextuid]["ggo"] = ggo
        Contest._nextuid += 1

    @staticmethod
    # pylint: disable=too-many-branches
    def check_contest_choices(choices: list, a_contest_blob: dict):
        """
        Will validate the syntax of the contest choices.  To validate
        a ticket contest, the outer context node now contains the
        ticket_titles while the inner node choice contains the paired
        ticket_names.  A a_contest_blob can be either a_contest_blob or
        a_cvr_blob.
        """
        # if this is a ticket contest, need to validate uber ticket syntax
        check_ticket = (
            "contest_type" in a_contest_blob
            and a_contest_blob["contest_type"] == "ticket"
        )
        for choice in choices:
            if isinstance(choice, str):
                continue
            if isinstance(choice, dict):
                bad_keys = [key for key in choice if key not in Contest._choice_keys]
                if bad_keys:
                    raise KeyError(
                        "the following keys are not valid Contest choice keys: "
                        f"{','.join(bad_keys)}"
                    )
                if check_ticket:
                    if "ticket_names" not in choice:
                        raise KeyError(
                            "Contest type is a ticket contest but does not contain ticket_names"
                        )
                    if len(choice["ticket_names"]) != len(
                        a_contest_blob["ticket_titles"]
                    ):
                        raise KeyError(
                            "when either 'ticket_names' or 'ticket_titles' are specified"
                            "the length of each array mush match - "
                            f"{len(choice['ticket_names'])} != {len(choice['ticket_names'])}"
                        )
                    if not isinstance(choice["ticket_names"], list):
                        raise KeyError("the key 'ticket_names' can only be a list")
                    if not isinstance(a_contest_blob["ticket_titles"], list):
                        raise KeyError("the key 'ticket_names' can only be a list")
                elif "ticket_names" in choice:
                    raise KeyError(
                        "contest_type is not a ticket contest but contains ticket_names"
                    )
                continue
            if isinstance(choice, bool):
                continue

    @staticmethod
    def check_contest_type(a_contest_blob: dict):
        """Will validate the value of contest_type"""
        if "contest_type" not in a_contest_blob or a_contest_blob[
            "contest_type"
        ] not in [
            "candidate",
            "ticket",
            "question",
        ]:
            raise KeyError(
                f"contest_type ({a_contest_blob['contest_type']}) must be specified "
                "as either: candidate, ticket, or question"
            )

    @staticmethod
    def check_selection(a_contest_blob: dict):
        """Will check the syntaz of the selection array"""

    @staticmethod
    def check_contest_blob_syntax(
        a_contest_blob: dict,
        filename: str = "",
        digest: str = "",
        set_defaults: bool = False,
    ):
        """
        Will check the synatx of a contest.

        Note - the filename and digest parameters only adjust
        potential error messages.

        If set_defaults is set, missing default values will be set.

        Three adjustments can be made: 1 - if there is mo max, will
        set it (plurality:1 and RCV:len(choices)) 2 - will add the
        Globals.ELECTION_UPSTREAM_REMOTE to the contest (so that it
        flows out through the CVR and beyond - for voter UX purposes
        only 3 - if a contest choice is a string, set the name key to
        that value
        """
        legal_fields = Contest._cast_keys
        bad_keys = [key for key in a_contest_blob if key not in legal_fields]
        if bad_keys:
            if filename:
                raise KeyError(
                    f"File ({filename}): "
                    f"the following keys are not valid Contest keys: "
                    f"{','.join(bad_keys)}"
                )
            if digest:
                raise KeyError(
                    f"Commit digest ({digest}): "
                    f"the following keys are not valid Contest keys: "
                    f"{','.join(bad_keys)}"
                )
            raise KeyError(
                f"the following keys are not valid Contest keys: "
                f"{','.join(bad_keys)}"
            )
        # Need to validate choices sub data structure as well
        Contest.check_contest_choices(a_contest_blob["choices"], a_contest_blob)
        Contest.check_contest_type(a_contest_blob)
        if "selection" in a_contest_blob:
            Contest.check_selection(a_contest_blob)
        if set_defaults:
            # if max is not set, set it
            # import pdb; pdb.set_trace()
            if "max" not in a_contest_blob:
                if a_contest_blob["tally"] == "plurality":
                    a_contest_blob["max"] = 1
                else:
                    a_contest_blob["max"] = len(a_contest_blob["choices"])
            # If the contest choice is a string, convert it to dict (name)
            for index, choice in enumerate(a_contest_blob["choices"]):
                if isinstance(choice, str):
                    a_contest_blob["choices"][index] = {"name": choice}
            # For voter UX, add ELECTION_UPSTREAM_REMOTE
            a_contest_blob["election_upstream_remote"] = Globals.get(
                "ELECTION_UPSTREAM_REMOTE"
            )

    @staticmethod
    def get_choices_from_contest(choices: list):
        """Will smartly return just the pure list of choices sans all
        values and sub dictionaries.  An individual choice can either
        be a simple string, a regulare 1D dictionary, or it turns out
        a bool.
        """
        # Returns a pure list of choices sans any other values or sub dictionaries
        if isinstance(choices[0], str):
            return choices
        if isinstance(choices[0], dict):
            return [entry["name"] for entry in choices]
        if isinstance(choices[0], bool):
            return ["True", "False"] if choices[0] else ["False", "True"]
        raise ValueError(
            f"unknown/unsupported contest choices data structure ({choices})"
        )

    @staticmethod
    def split_selection(selection: str):
        """Will split the selection into (2) parts again."""
        offset, name = re.split(r":\s+", selection, 1)
        return int(offset), name

    @staticmethod
    def extract_offest_from_selection(selection: str):
        """
        Will extract the int selection choice from the verbose
        selection string
        """
        return int(Contest.split_selection(selection)[0])

    @staticmethod
    def extract_name_from_selection(selection: str):
        """
        Will extract the name selection choice from the verbose
        selection string
        """
        return Contest.split_selection(selection)[1]

    def __init__(
        self,
        a_contest_blob: dict,
        cast_branch: str = "",
        set_defaults: bool = False,
    ):
        """Construct the object placing the contest info in an attribute
        while recording the meta data
        """
        # ZZZ import pdb; pdb.set_trace()
        # Note - Contest.check_contest_blob_syntax will set missing defaults
        Contest.check_contest_blob_syntax(
            a_contest_blob,
            set_defaults=set_defaults,
        )
        self.contest = a_contest_blob
        self.cast_branch = cast_branch
        self.cloak = False

    def __str__(self):
        """Return the contest contents as a print-able json string - careful ..."""
        # Note - keep cloak out of it until proven safe to include
        contest_dict = {
            key: self.contest[key] for key in Contest._cast_keys if key in self.contest
        }
        contest_dict.update({"cast_branch": self.cast_branch})
        return json.dumps(contest_dict, sort_keys=True, indent=4, ensure_ascii=False)

    def pretty_print_a_ticket(self, choice_index: int):
        """Will pretty print a ticket"""
        ticket = []
        for ticket_index, name in enumerate(
            self.contest["choices"][choice_index]["ticket_names"]
        ):
            ticket.append(f"{name} ({self.contest['ticket_titles'][ticket_index]})")
        return "; ".join(ticket)

    def get(self, thing: str):
        """Generic getter - can raise KeyError"""
        # Return the choices
        # ZZZ        import pdb; pdb.set_trace()
        if thing == "contest":
            return self.contest
        if thing == "choices":
            return Contest.get_choices_from_contest(self.contest["choices"])
        # Return contest 'meta' data
        if thing in ["cast_branch", "cloak"]:
            return getattr(self, thing)
        # Note - a 'selection' is a aggregated string of the selected
        # offset and the 'name', which for a ticket based contest is
        # not useful.  So support the extraction of just the offset.
        if thing == "selection-offset":
            return Contest.extract_offest_from_selection(
                getattr(self, "contest")["selection"]
            )
        # Else return contest data itself indexed by thing
        return getattr(self, "contest")[thing]

    def set(self, thing: str, value: str):
        """Generic setter - need to be able to set the cast_branch when committing the contest"""
        if thing in ["cast_branch", "cloak"]:
            setattr(self, thing, value)
            return
        raise ValueError(f"Illegal value for Contest attribute ({thing})")

    def clear_selection(self):
        """Clear the selection (as when self adjudicating)"""
        self.contest["selection"] = []

    def delete_contest_field(self, thing: str):
        """Generic deleter - need to be able to delete nodes"""
        if thing in Contest._cast_keys:
            if thing in self.contest:
                del self.contest[thing]
            return
        raise ValueError(f"Illegal value for Contest attribute ({thing})")

    def get_selections_indices(self):
        """Will return the ordered list of index numbers for the selection array"""
        indexes = []
        if "selection" in self.contest:
            for sel in self.contest["selection"]:
                indexes.append(Contest.extract_offest_from_selection(sel))
        return indexes

    def add_selection(self, selection_offset: int):
        """Will add the specified contest choice, the offset into the ordered
        choices array, to the specified contest.  This is an
        'add' since in plurality one may be voting for more than one
        choice, or in RCV one needs to rank the choices.  In both the
        order is the rank but in plurality rank does not matter.
        """
        # Some minimal sanity checking
        if selection_offset > len(self.contest["choices"]):
            raise ValueError(
                f"The choice offset ({selection_offset}) is greater "
                f"than the number of choices ({len(self.contest['choices'])})"
            )
        if selection_offset < 0:
            raise ValueError(
                f"Only positive offsets are supported ({selection_offset})"
            )
        if "selection" not in self.contest:
            self.contest["selection"] = []
        elif selection_offset in self.get_selections_indices():
            raise ValueError(
                (
                    f"The selection ({selection_offset}) has already been "
                    f"selected for contest ({self.contest['contest_name']}) "
                    f"for GGO ({self.contest['ggo']})"
                )
            )
        # For end voter UX, add the selection as the offset + ': ' +
        # name just because a string is more understandable than json
        # list syntax
        self.contest["selection"].append(
            str(selection_offset)
            + ": "
            + self.contest["choices"][selection_offset]["name"]
        )


# EOF
