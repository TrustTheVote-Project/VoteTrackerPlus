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

"""How to manage a VTP Ballot"""

import csv
import json
import os
from copy import deepcopy

from deepdiff import DeepDiff

# Local imports
from .common import Globals
from .contest import Contest


class Ballot:
    """A class to hold a ballot.  A ballot is always a function of an
    address defined within the context of VTP election configuration
    as defined by the aggregated data in the config and address_map
    files.
    """

    # Legitimate Ballot keys.  Note - valid Contest keys are defined in
    # the Contest class
    _ballot_keys = [
        "contests",
        "active_ggos",
        "ballot_subdir",
        "ballot_node",
        "ballot_filename",
    ]

    @staticmethod
    def gen_cast_ballot_location(config, subdir):
        """Return the file location of a cast ballot"""
        return os.path.join(
            config.get("git_rootdir"),
            subdir,
            Globals.get("CONTEST_FILE_SUBDIR"),
            Globals.get("BALLOT_FILE"),
        )

    @staticmethod
    def gen_contest_location(config, subdir):
        """Return the contest.json file location"""
        return os.path.join(
            config.get("git_rootdir"),
            subdir,
            Globals.get("CONTEST_FILE_SUBDIR"),
            Globals.get("CONTEST_FILE"),
        )

    @staticmethod
    def gen_receipt_location(
        config,
        subdir: str,
        branch: str,
        style: str,
    ) -> str:
        """
        Return either a csv or md receipt file location.  Note that
        the receipt.csv version is stored next to the unversioned
        ballot.json and the ephemeral contest.json files in the CVRs
        subdirectory while the version receipt.md is stored in the
        RECEIPT_FILE_SUBDIR tree.
        """
        if style == "csv":
            return os.path.join(
                config.get("git_rootdir"),
                subdir,
                Globals.get("CONTEST_FILE_SUBDIR"),
                Globals.get("RECEIPT_FILE"),
            )
        return os.path.join(
            config.get("git_rootdir"),
            subdir,
            branch,
            Globals.get("RECEIPT_FILE_MD"),
        )

    @staticmethod
    def get_cast_from_blank(blank_ballot):
        """Given a blank ballot relative or absolute path, will map that
        to the state/town cast ballot location, which is basically up
        three and down one.
        """
        return os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(blank_ballot))),
            Globals.get("CONTEST_FILE_SUBDIR"),
            Globals.get("BALLOT_FILE"),
        )

    @staticmethod
    def verify_ballot_outer_keys(ballot):
        """Will verify the outermost keys of a blank or cast ballot"""
        bad_keys = [key for key in ballot if key not in Ballot._ballot_keys]
        if bad_keys:
            raise KeyError(
                "the following keys are not valid Ballot keys: " f"{','.join(bad_keys)}"
            )
        missing_keys = [key for key in Ballot._ballot_keys if key not in ballot]
        if missing_keys:
            raise KeyError(
                "the following required Ballot keys are missing: "
                f"{','.join(missing_keys)}"
            )

    def __init__(self, operation_self):
        """Constructor - just creates the dictionary and returns the
        object.
        """
        self.contests = []
        self.active_ggos = []
        self.ballot_subdir = ""
        self.ballot_node = ""
        self.ballot_filename = ""
        self.operation_self = operation_self

    def verify_cast_ballot_data(self, config):
        """Will validate an incoming cast ballot against the
        associated blank ballot.  This is done by first verifying the
        ballot syntax, including the selection node.  Then after
        del'ing the selection node from the incoming_cast_ballot, a
        key sorted json.dump of that against the source blank ballot
        is performed.

        If incoming_cast_ballot is not JSON or broken, this function
        will raise an error.
        """

        # 0) just for safety
        # Ballot.verify_ballot_outer_keys(self)

        # Get the blank ballot
        the_bb = BlankBallot(self.operation_self)
        the_bb.read_a_blank_ballot(
            None,
            config,
            config.gen_blank_ballot_location_from_filename(
                self.ballot_subdir,
                self.ballot_filename,
            ),
        )

        # ... and make a dict out of it
        blank = the_bb.dict()
        # Create a local dict copy that we can manipulate
        cast_ballot = deepcopy(self.dict())

        # 1) Loop over contests and a) validate the selection, b) that
        # the blank_ballot is legit, and c) that it matches
        for contest in cast_ballot["contests"]:
            # Note - if selection is not a valid key, a KeyError will be raised
            if not isinstance(contest.get("selection"), list):
                raise KeyError(
                    "the incoming cast ballot selection is not a list (it can be empty)"
                )
            # Validate the selection node
            for pick in contest.get("selection"):
                index, name = Contest.split_selection(pick)
                # Does the index equal the name
                if contest.get("choices")[index] != name:
                    raise KeyError(
                        f"the selection index ({index}) name ({name}) "
                        f"does not match the choice name ({contest[1][index]['name']})"
                    )
            # Now remove the selection
            contest.delete_contest_field("selection")

        # 2) Compare incoming_cast_ballot to the associated blank
        # ballot.  Since the blank ballot needs to be read in, it is
        # easier to add the selection node to that than to make a deep
        # copy of the cast ballot and remove the selection node from
        # that.
        result = DeepDiff(blank, cast_ballot)
        # import pdb; pdb.set_trace()
        if result:
            raise KeyError(
                "the incoming cast ballot does not match the upstream blank ballot"
                "the diff follows:\n"
                f"{result}"
            )

    def set_ballot_data(self, incoming_ballot_json, a_cast_ballot: bool = False):
        """
        Will set this Ballot instance to the incoming ballot json.
        This _assumes_ that incoming_ballot_json is all json and has
        not yet been converted to contest objects.
        """
        Ballot.verify_ballot_outer_keys(incoming_ballot_json)
        self.active_ggos = incoming_ballot_json["active_ggos"]
        self.ballot_subdir = incoming_ballot_json["ballot_subdir"]
        self.ballot_node = incoming_ballot_json["ballot_node"]
        self.ballot_filename = incoming_ballot_json["ballot_filename"]
        # now handle the contests (with or without a selection entry)
        # Need to create Contest (objects) for each contest
        self.contests = []
        for contest in incoming_ballot_json["contests"]:
            self.contests.append(Contest(contest), a_cast_ballot=a_cast_ballot)

    def get(self, name: str):
        """A generic getter - will raise a NameError if name is invalid"""
        if name in ["ggos", "active_ggos"]:
            return self.active_ggos
        if name == "contests":
            return self.contests
        if name == "ballot_subdir":
            return self.ballot_subdir
        if name == "ballot_node":
            return self.ballot_node
        if name == "ballot_filename":
            return self.ballot_filename
        raise NameError(f"Name {name} not accepted/defined for Ballot.get()")

    def get_contest_name_by_uid(self, uid: str):
        """Given a blank ballot or better, will return the contest name
        given a uid.  Will raise an error if the ballot does not contain
        that uid.
        """
        for contest in self.contests:
            if uid == contest.get("uid"):
                return contest.get("contest_name")
        raise KeyError(
            f"There is no matching contest uid ({uid}) in the supplied balloot"
        )

    def dict(self):
        """Return a dictionary of the ballot by making a copy"""
        return dict(
            {
                "contests": self.contests,
                "active_ggos": self.active_ggos,
                "ballot_node": self.ballot_node,
                "ballot_subdir": self.ballot_subdir,
                "ballot_filename": self.ballot_filename,
            }
        )

    def __str__(self):
        """Boilerplate"""
        ballot = {
            "contests": self.contests,
            "active_ggos": self.active_ggos,
            "ballot_node": self.ballot_node,
            "ballot_subdir": self.ballot_subdir,
            "ballot_filename": self.ballot_filename,
        }
        return json.dumps(ballot, sort_keys=True, indent=4, ensure_ascii=False)

    def get_contest_index(self, contest: dict):
        """
        Will return the contest's contests array index (via the
        contest's uid)
        """
        uid = contest.get("uid")
        for index, value in enumerate(self.contests):
            if value["uid"] == uid:
                return index
        raise ValueError(
            f"Internal error - a contest uid ({uid}) was not found in containing ballot"
        )

    def get_cvr_parent_dir(self, config):
        """Return the directory that contains the CVR directory for this ballot"""
        return os.path.join(
            config.get("git_rootdir"),
            self.ballot_subdir,
        )

    def read_a_cast_ballot(self, address, config, ballot_file=""):
        """
        Will return the dictionary of a cast ballot.  Needs an address
        so to get the correct ballot_subdir to read the caste ballot
        from.
        """
        if not ballot_file:
            ballot_file = Ballot.gen_cast_ballot_location(
                config, address.get("ballot_subdir")
            )
        self.operation_self.imprimir(f"Reading {ballot_file}", 5)
        with open(ballot_file, "r", encoding="utf8") as file:
            json_doc = json.load(file)
            contests = json_doc["contests"]
            self.active_ggos = json_doc["active_ggos"]
            self.ballot_subdir = json_doc["ballot_subdir"]
            self.ballot_node = json_doc["ballot_node"]
            self.ballot_filename = json_doc["ballot_filename"]
        # Need to create Contest (objects) for each contest
        self.contests = []
        for contest in contests:
            self.contests.append(Contest(contest))

    def write_a_cast_ballot(self, config):
        """
        Will write out a cast ballot in json
        """
        ballot_file = Ballot.gen_cast_ballot_location(config, self.ballot_subdir)
        os.makedirs(os.path.dirname(ballot_file), exist_ok=True)
        # need to convert the Contests into a dictionary
        contests = []
        for contest in self.contests:
            contests.append(contest.get("contest"))
        # might was well write out everything, yes?
        the_aggregate = {
            "contests": contests,
            "active_ggos": self.active_ggos,
            "ballot_subdir": self.ballot_subdir,
            "ballot_node": self.ballot_node,
            "ballot_filename": self.ballot_filename,
        }
        with open(ballot_file, "w", encoding="utf8") as outfile:
            json.dump(
                the_aggregate, outfile, sort_keys=True, indent=4, ensure_ascii=False
            )
        return ballot_file

    def write_contest(self, contest, config):
        """Write out the voter's contest"""
        contest_file = Ballot.gen_contest_location(config, self.ballot_subdir)
        # Prepend the dictionary with a CVR key
        the_aggregate = {"contestCVR": contest.get("dict")}
        # The parent directory better exist or something is wrong
        with open(contest_file, "w", encoding="utf8") as outfile:
            json.dump(
                the_aggregate, outfile, sort_keys=True, indent=4, ensure_ascii=False
            )
        return contest_file

    def write_receipt_csv(self, lines, config, receipt_file=""):
        """Write out the voter's ballot receipt"""
        if not receipt_file:
            receipt_file = Ballot.gen_receipt_location(
                config, self.ballot_subdir, "", "csv"
            )
        # The parent directory better exist or something is wrong
        with open(receipt_file, "w", encoding="utf8") as outfile:
            for line in lines:
                outfile.write(f"{line}\n")
        return receipt_file

    # pylint: disable=too-many-locals
    # pylint: disable=too-many-arguments
    def write_receipt_md(
        self,
        lines: list,
        config: dict,
        receipt_branch: str,
        qr_file: str = "",
        qr_url: str = "",
    ) -> str:
        """Write out the voter's ballot receipt as a markdown table with hyperlinks"""
        receipt_file = Ballot.gen_receipt_location(
            config, self.ballot_subdir, receipt_branch, "md"
        )
        if qr_file:
            receipt_file = receipt_file.rstrip(".md") + "-qr.md"
        url_root = "/".join(
            [
                Globals.get("ELECTION_UPSTREAM_REMOTE"),
                "commit",
            ]
        )
        # The directory will rarely exist in this case as receipt_file
        # will be the first file to be placed there
        if not os.path.isdir(
            os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.dirname(receipt_file)))
            )
        ):
            raise OSError(
                f"the receipt markdown file is being placed someplace outside the expected tree"
                f"{receipt_file}"
            )
        os.makedirs(os.path.dirname(receipt_file), exist_ok=True)
        with open(receipt_file, "w", encoding="utf8") as outfile:
            if qr_file:
                # add the voter's QR code to the markdown
                outfile.write(f"![{qr_url}]({qr_file} 'Ballot Voucer')\n\n")
            header = ""
            for col in lines[0].split(","):
                uid, title = col.split(" - ", 1)
                header += "| " + uid[1:] + "<br>" + title[:-1] + " "
            outfile.write(f"| Index {header}|\n")
            outfile.write("|:---:" * len(lines[1].split(",")) + "|:---:|\n")
            for index, line in enumerate(lines[1:]):
                newline = ""
                for dig in line.split(","):
                    if qr_file:
                        newline += f"| [{dig[0:8]}...]({url_root}/{dig}) "
                    else:
                        newline += f"| [<sub><sup>{dig}</sup></sub>]({url_root}/{dig}) "
                outfile.write(f"| {index + 1} {newline}|\n")
        return receipt_file

    def read_receipt_csv(self, config, receipt_file="", address=""):
        """Read the voter's ballot receipt"""
        if not receipt_file:
            receipt_file = Ballot.gen_receipt_location(
                config, address.get("ballot_subdir"), "", "cvs"
            )
        # The parent directory better exist or something is wrong
        lines = []
        with open(receipt_file, "r", encoding="utf8") as infile:
            lines = list(csv.reader(infile))
        return lines


class BlankBallot(Ballot):
    """
    A child class of Ballot - Ballot was getting too large but at the
    moment blank ballot is just a regular ballot with a few more
    methods.
    """

    def create_blank_ballot(self, address, config):
        """Given an Address and a ElectionConfig, will generate the
        appropriate blank ballot.  Implementation note - this function
        needs to be smart in that it needs to deal with various regex
        and other rules/conventions/specs of the address_map files.  The
        development of the support of that is an R&D iterative process.

        Initially this class/functions only understand two address_map
        syntaxes (defined in ElectionConfig which is what parses the
        address_map files).

        'address_map': {'ggos': {<ggo-kind>: ['.*']}

        'address_map': {'addresses': ['.*']}

        Where <ggo-kind> is the name of the child GGO group (there can
        be different 'kinds' of GGO children).  The above syntax follows
        what is known 'regex' expressions.

        The first defines that the addresses for this GGO are handled by
        the ggo-kind/ggo specified, which is in this case all ggos of
        the specified kind.  In other words, the parent GGO accepts all
        the addresses that specified child GGOs accept.

        The second defines that all the addresses in this specific GGO
        are valid for this GGO.

        Note the value of the required address fields in the Globals
        class - the implicit algorithm used to map an address to the
        active GGOs is dependent on the defined fields.
        """

        # With the list of active GGOs, add in the contests for each one
        candidate_order = []
        question_order = []
        for node in address.get("active_ggos"):
            cfg = config.get_node(node, "config")
            if "contests" in cfg:
                for contest in cfg["contests"]:
                    # first fill in the rest of the autofilled fields
                    contest["ggo"] = node
                    # ZZZ - at this point the question of order is still
                    # an underconstrained TBD.  For now, while maintaining
                    # the relative order, have the non-question contests
                    # come first and the question contests come last.
                    # Note - the whole GGO thing probably should be
                    # deleted assuming the contest uid question can be
                    # solved in a more reasonable manner.
                    #                    import pdb; pdb.set_trace()
                    if contest["contest_type"] == "question":
                        question_order.append(contest)
                    else:
                        candidate_order.append(contest)
        self.contests = candidate_order
        self.contests.extend(question_order)

        # To determine the location of the blank ballot, the real
        # solution is probably something like determining the
        # addresses for each unique blank ballot and generate a unique
        # filename or directory based on that and put them in the
        # 'proper' leaf node off 'the_address_node'.  However, there
        # no budget for that now and it would probably be better to
        # see what real life constraints and requirements exist.  So
        # punt that for now - just place this ballot in the proper
        # leaf node assuming 100% overlapping/coherent boundaries at
        # state/town heiracrchy.
        self.ballot_subdir = address.get("ballot_subdir")
        self.ballot_node = address.get("ballot_node")
        # cache the active ggos as well
        self.active_ggos = address.get("active_ggos")
        self.ballot_filename = config.gen_unique_ggo_name(
            self.active_ggos, Globals.get("BALLOT_FILE")
        )

    def write_blank_ballot(self, config, ballot_file="", style="json", printonly=False):
        """
        will write out a blank ballot to a file in some format.
        """
        if not ballot_file:
            ballot_file = config.gen_blank_ballot_location(
                self.active_ggos, self.ballot_subdir, style
            )
            if not printonly:
                os.makedirs(os.path.dirname(ballot_file), exist_ok=True)
        if printonly:
            return ballot_file
        if style == "json":
            # When the style is json, print all three dictionaries as one
            the_aggregate = {
                "contests": self.contests,
                "active_ggos": self.active_ggos,
                "ballot_subdir": self.ballot_subdir,
                "ballot_node": self.ballot_node,
                "ballot_filename": self.ballot_filename,
            }
            with open(ballot_file, "w", encoding="utf8") as outfile:
                json.dump(
                    the_aggregate, outfile, sort_keys=True, indent=4, ensure_ascii=False
                )
        elif style == "pdf":
            # See https://github.com/rst2pdf/rst2pdf
            raise NotImplementedError(
                ("Apologies but printing the pdf of a ballot is not implemented yet")
            )
        else:
            raise NotImplementedError(f"Unsupported Ballot type ({style}) for writing")
        return ballot_file

    def read_a_blank_ballot(self, address, config, ballot_file="", style="json"):
        """
        Will return the dictionary of a blank ballot (given an address
        so to be able to find the correct blank ballot)
        """
        if not ballot_file:
            # hackito ergo sum - since the ballot has not yet been
            # read, the ballot attributes are not yet known.  But the
            # ones that overlap with address attributes are the same
            # as those.  They will be re-written later anyway with the
            # same value when the ballot is read...
            self.active_ggos = address.get("active_ggos")
            self.ballot_subdir = address.get("ballot_subdir")
            self.ballot_node = address.get("ballot_node")
            ballot_file = config.gen_blank_ballot_location(
                self.active_ggos, self.ballot_subdir, style
            )
        if style == "json":
            self.operation_self.imprimir(f"Reading {ballot_file}", 5)
            with open(ballot_file, "r", encoding="utf8") as file:
                json_doc = json.load(file)
                contests = json_doc["contests"]
                self.active_ggos = json_doc["active_ggos"]
                self.ballot_subdir = json_doc["ballot_subdir"]
                self.ballot_node = json_doc["ballot_node"]
                self.ballot_filename = json_doc["ballot_filename"]
            # Need to create Contest (objects) for each contest
            self.contests = []
            for contest in contests:
                self.contests.append(Contest(contest))
        else:
            raise NotImplementedError(f"Unsupported Ballot type ({style}) for reading")


# EOF
