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

import os
import json
import csv
from logging import debug
# Local imports
from common import Globals
from contest import Contest

class Contests:
    """An iteratable object for the contests in a ballot"""

    def __init__(self, a_ballot):
        """
        Need to cache enough data here so to be able to iterate AND
        create valid Contest objects
        """
        self.ballot_ref = a_ballot
        # Need the (ordered) list of ggos supplying contests
        self.ggos = [*a_ballot.get('contests')]
        self.ggo_max = len(self.ggos)
        self.ggo_index = 0
        self.contest_index = 0
        self.contest_max = len(a_ballot.get('contests')[self.ggos[0]])
#        import pdb; pdb.set_trace()
#        inner_blob = next(iter((a_ballot.get('contests')[self.ggos[0]][0].values())))
#        self.contest_max = len(inner_blob['max']) if 'max' in inner_blob else 1

    def __iter__(self):
        """boilerplate"""
        # start - be kind and reset things
        self.ggo_index = 0
        self.contest_index = 0
        self.contest_max = len(self.ballot_ref.get('contests')[self.ggos[0]])
        return self

    def __next__(self):
        """
        Because of the blobiness nature of the data model of a contest
        within a ballot dictionary, this is ugly.  Need to iterate over
        the correct ordered list of ggos (self.ggos) and within each of
        those iterations, iterate over the contests which is an ordered
        list of single entry dictionaries.

        Note - the code below post increments the index alues which is
        not the common pattern ?
        """
        if self.ggo_max == 0:
            # just in case
            raise StopIteration
        # cache this ggo
        ggo = self.ggos[self.ggo_index]
        # if there is a contest here, return it
        if self.contest_index < self.contest_max:
#            contest_content = \
#              next(iter((self.ballot_ref.get('contests')[ggo][self.contest_index].values())))
            # return the next contest in this ggo group
            this_contest = Contest(self.ballot_ref.get('contests')[ggo][self.contest_index],
                                       ggo, self.contest_index, accept_all_keys=True)
            self.contest_index += 1
            return this_contest

        # If here, bump the ggo_index and reset the contest index and try again
        self.ggo_index += 1
        self.contest_index = 0

        # Now test to see if there is a next ggo group and if so, return
        # its first contest
        if self.ggo_index < self.ggo_max:
            ggo = self.ggos[self.ggo_index]
            self.contest_max = len(self.ballot_ref.get('contests')[ggo])
            if self.contest_index < self.contest_max:
                this_contest = \
                  Contest(self.ballot_ref.get('contests')[ggo][self.contest_index],
                              ggo, 0, accept_all_keys=True)
                self.contest_index += 1
                return this_contest
        # done - be kind and reset things
        self.ggo_index = 0
        self.contest_index = 0
        self.contest_max = len(self.ballot_ref.get('contests')[self.ggos[0]])
        raise StopIteration

    def len(self):
        """Not my language, but still very cool"""
        return sum(1 for _ in self)

class Ballot:
    """A class to hold a ballot.  A ballot is always a function of an
    address defined within the context of VTP election configuration
    as defined by the aggregated data in the config and address_map
    files.
    """

    @staticmethod
    def gen_cast_ballot_location(config, subdir):
        """Return the file location of a cast ballot"""
        return os.path.join(config.get('git_rootdir'),
                    Globals.get('ROOT_ELECTION_DATA_SUBDIR'),
                    subdir,
                    Globals.get('CONTEST_FILE_SUBDIR'),
                    Globals.get('BALLOT_FILE'))

    @staticmethod
    def gen_contest_location(config, subdir):
        """Return the contest.json file location"""
        return os.path.join(config.get('git_rootdir'),
                    Globals.get('ROOT_ELECTION_DATA_SUBDIR'),
                    subdir,
                    Globals.get('CONTEST_FILE_SUBDIR'),
                    Globals.get('CONTEST_FILE'))

    @staticmethod
    def gen_receipt_location(config, subdir):
        """Return the receipt.csv file location"""
        return os.path.join(config.get('git_rootdir'),
                    Globals.get('ROOT_ELECTION_DATA_SUBDIR'),
                    subdir,
                    Globals.get('CONTEST_FILE_SUBDIR'),
                    Globals.get('RECEIPT_FILE'))

    @staticmethod
    def get_cast_from_blank(blank_ballot):
        """Given a blank ballot relative or absolute path, will map that
        to the state/town cast ballot location, which is basically up
        three and down one.
        """
        return os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(blank_ballot))),
            Globals.get('CONTEST_FILE_SUBDIR'),
            Globals.get('BALLOT_FILE'))

    def __init__(self):
        """Constructor - just creates the dictionary and returns the
        object
        """
        self.contests = {}
        self.active_ggos = []
        self.ballot_subdir = ""
        self.ballot_node = ""

    def get(self, name):
        """A generic getter - will raise a NameError if name is invalid"""
        if name in ['ggos', 'active_ggos']:
            return self.active_ggos
        if name == 'contests':
            return self.contests
        if name == 'ballot_subdir':
            return self.ballot_subdir
        if name == 'ballot_node':
            return self.ballot_node
        raise NameError(f"Name {name} not accepted/defined for Ballot.get()")

    def get_contest_name_by_uid(self, uid):
        """Given a blank ballot or better, will return the contest name
        given a uid.  Will raise an error if the ballot does not contain
        that uid.
        """
        for contest in Contests(self):
            if uid == contest.get('uid'):
                return contest.get('name')
        raise KeyError(f"There is no matching contest uid ({uid}) in the supplied balloot")

    def dict(self):
        """Return a dictionary of the ballot by making a copy"""
        return dict({'contests': self.contests,
                    'active_ggos': self.active_ggos,
                    'ballot_node': self.ballot_node,
                    'ballot_subdir': self.ballot_subdir})

    def __str__(self):
        """Boilerplate"""
        ballot = {'contests': self.contests,
                      'active_ggos': self.active_ggos,
                      'ballot_node': self.ballot_node,
                      'ballot_subdir': self.ballot_subdir}
        return json.dumps(ballot, sort_keys=True, indent=4, ensure_ascii=False)

    def clear_selection(self, contest):
        """Clear the selection (as when self adjudicating)"""
        self.contests[contest.get('ggo')][contest.get('index')][contest.get('name')]['selection'] \
          = []

    def add_selection(self, contest, selection_offset):
        """Will add the specified contest choice (offset into the ordered
        choices array) to the specified contest.  This is an
        'add' since in plurality one may be voting for more than one
        choice, or in RCV one needs to rank the choices.  In both the
        order is the rank but in plurality rank does not matter.
        """
        # Some minimal sanity checking
        if selection_offset > len(contest.get('choices')):
            raise ValueError(f"The choice offset ({selection_offset}) is greater "
                             f"than the number of choices ({len(contest.get('choices'))})")
        if selection_offset < 0:
            raise ValueError(f"Only positive offsets are supported ({selection_offset})")
        contest_index = contest.get('index')
        contest_ggo = contest.get('ggo')
        contest_name = contest.get('name')
        if 'selection' not in self.contests[contest_ggo][contest_index][contest_name].keys():
            self.contests[contest_ggo][contest_index][contest_name]['selection'] = []
        # pylint: disable=line-too-long
        elif selection_offset in self.contests[contest_ggo][contest_index][contest_name]['selection']:
            raise ValueError((f"The selection ({selection_offset}) has already been "
                                  f"selected for contest ({contest_name}) "
                                  f"for GGO ({contest_ggo})"))
        # For end voter UX, add the selection as the offset + ': ' +
        # name just because a string is more understandable than json
        # list syntax
        self.contests[contest_ggo][contest_index][contest_name]['selection'].append(
            str(selection_offset) + ': ' + contest.get('choices')[selection_offset])

    # def verify_cast_ballot(self):
    #     """Will validate the ballot contest choices are legitimate.
    #     Will raise an error with the list of invalid contests and
    #     returns the number of contests with either blank of less than
    #     legal selections.
    #     """
    #     raise NotImplementedError("verify_cast_ballot is not yet implemented")

    def get_cvr_parent_dir(self, config):
        """Return the directory that contains the CVR directory for this ballot"""
        return os.path.join(config.get('git_rootdir'),
                                Globals.get('ROOT_ELECTION_DATA_SUBDIR'),
                                self.ballot_subdir)

    def read_a_cast_ballot(self, address, config, ballot_file=""):
        """
        Will return the dictionary of a cast ballot.  Needs an address
        so to get the correct ballot_subdir to read the caste ballot
        from.
        """
        if not ballot_file:
            ballot_file = Ballot.gen_cast_ballot_location(config, address.get('ballot_subdir'))
        debug(f"Reading {ballot_file}")
        with open(ballot_file, 'r', encoding="utf8") as file:
            json_doc = json.load(file)
            self.contests = json_doc['contests']
            self.active_ggos = json_doc['active_ggos']
            self.ballot_subdir = json_doc['ballot_subdir']
            self.ballot_node = json_doc['ballot_node']

    def write_a_cast_ballot(self, config):
        """
        Will write out a cast ballot in json
        """
        ballot_file = Ballot.gen_cast_ballot_location(config, self.ballot_subdir)
        os.makedirs(os.path.dirname(ballot_file), exist_ok=True)
        # might was well write out everything, yes?
        the_aggregate = {'contests': self.contests,
                         'active_ggos': self.active_ggos,
                         'ballot_subdir': self.ballot_subdir,
                         'ballot_node': self.ballot_node}
        with open(ballot_file, 'w', encoding="utf8") as outfile:
            json.dump(the_aggregate, outfile, sort_keys=True, indent=4, ensure_ascii=False)
        return ballot_file

    def write_contest(self, contest, config):
        """Write out the voter's contest"""
        contest_file = Ballot.gen_contest_location(config, self.ballot_subdir)
        # Prepend the dictionary with a CVR key
        the_aggregate = {'CVR': contest.get('dict')}
        # The parent directory better exist or something is wrong
        with open(contest_file, 'w', encoding="utf8") as outfile:
            json.dump(the_aggregate, outfile, sort_keys=True, indent=4, ensure_ascii=False)
        return contest_file

    def write_receipt_csv(self, lines, config, receipt_file=''):
        """Write out the voter's ballot receipt"""
        if not receipt_file:
            receipt_file = Ballot.gen_receipt_location(config, self.ballot_subdir)
        # The parent directory better exist or something is wrong
        with open(receipt_file, 'w', encoding="utf8") as outfile:
            for line in lines:
                outfile.write(f"{line}\n")
        return receipt_file

    def read_receipt_csv(self, config, receipt_file='', address=''):
        """Read the voter's ballot receipt"""
        if not receipt_file:
            receipt_file = Ballot.gen_receipt_location(config, address.get('ballot_subdir'))
        # The parent directory better exist or something is wrong
        lines = []
        with open(receipt_file, 'r', encoding="utf8") as infile:
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
        for node in address.get('active_ggos'):
            cfg = config.get_node(node, 'config')
            if 'contests' in cfg:
                self.contests[node] = cfg['contests']

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
        self.ballot_subdir = address.get('ballot_subdir')
        self.ballot_node = address.get('ballot_node')
        # cache the active ggos as well
        self.active_ggos = address.get('active_ggos')

    def gen_unique_blank_ballot_name(self, config, filename):
        """
        ZZZ - this will need to be re-written at some point - tries to
        generate a unique ballot name per unique address across the set
        of active GGOs
        """
        ggo_unique_name = [config.get_node(ggo, 'uid') for ggo in self.active_ggos]
        # alphanumerically sort the string
        ggo_unique_name.sort(key=int)
        # for now, no error checking ...
        ggo_unique_name.append(filename)
        return ','.join(ggo_unique_name)

    def gen_blank_ballot_location(self, config, style='json'):
        """Return the file location of a blank ballot"""
        return os.path.join(
            config.get('git_rootdir'),
            Globals.get('ROOT_ELECTION_DATA_SUBDIR'),
            self.ballot_subdir,
            Globals.get('BLANK_BALLOT_SUBDIR'),
            style,
            self.gen_unique_blank_ballot_name(config, Globals.get('BALLOT_FILE')))

    def write_blank_ballot(self, config, ballot_file='', style='json'):
        """
        will write out a blank ballot to a file in some format.
        """
        if not ballot_file:
            ballot_file = self.gen_blank_ballot_location(config, style)
            os.makedirs(os.path.dirname(ballot_file), exist_ok=True)
        if style == 'json':
            # When the style is json, print all three dictionaries as one
            the_aggregate = {'contests': self.contests,
                                 'active_ggos': self.active_ggos,
                                 'ballot_subdir': self.ballot_subdir,
                                 'ballot_node': self.ballot_node}
            with open(ballot_file, 'w', encoding="utf8") as outfile:
                json.dump(the_aggregate, outfile, sort_keys=True, indent=4, ensure_ascii=False)
        elif style == 'pdf':
            # See https://github.com/rst2pdf/rst2pdf
            raise NotImplementedError(("Apologies but printing the pdf of a ballot "
                                           "is not implemented yet"))
        else:
            raise NotImplementedError(f"Unsupported Ballot type ({style}) for writing")
        return ballot_file

    def read_a_blank_ballot(self, address, config, ballot_file="", style='json'):
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
            self.active_ggos = address.get('active_ggos')
            self.ballot_subdir = address.get('ballot_subdir')
            self.ballot_node = address.get('ballot_node')
            ballot_file = self.gen_blank_ballot_location(config, style)
        if style == 'json':
            debug(f"Reading {ballot_file}")
            with open(ballot_file, 'r', encoding="utf8") as file:
                json_doc = json.load(file)
                self.contests = json_doc['contests']
                self.active_ggos = json_doc['active_ggos']
                self.ballot_subdir = json_doc['ballot_subdir']
                self.ballot_node = json_doc['ballot_node']
        else:
            raise NotImplementedError(f"Unsupported Ballot type ({style}) for reading")

# EOF
