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

"""A kitchen sync for VTP classes for the moment"""

import os
import json
import pprint

from common import Globals


class Ballot:
    """A class to hold a ballot.  A ballot is always a function of an
    address defined within the context of VTP election configuration
    as defined by the aggregated data in the config and address_map
    files.
    """

    def __init__(self):
        """Constructor - just creates the dictionary and returns the
        object
        """
        self.contests = {}
        self.active_ggos = []
        self.ballot_subdir = ""

    def get(self, name):
        """A generic getter - will raise a NameError if name is invalid"""
        if name == 'ggos':
            return self.active_ggos
        if name == 'contests':
            return self.contests
        raise NameError(f"Name {name} not accepted/defined for set()")

    def dict(self):
        """Return a dictionary of the ballot"""
        return dict(self.contests)

    def pprint(self, style):
        """Will print to STDOUT a ballot"""
        pprint.pprint({'contests': self.contests,
                           'active_ggos': self.active_ggos,
                           'ballot_subdir': self.ballot_subdir})

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
        # punt that for now - just place this ballot in the porper
        # leaf node (assuming overlapping boundaries).
        self.ballot_subdir = address.get('ballot_subdir')

    def write_blank_ballot(self, config, ballot_file='', style='json'):
        """
        Will write out a blank ballot to a file in some format.
        """
        if not ballot_file:
            ballot_file = os.path.join(config.get('git_rootdir'),
                                    self.ballot_subdir,
                                    Globals.get('BLANK_BALLOT_SUBDIR'),
                                    style)
            os.makedirs(ballot_file, exist_ok=True)
            ballot_file = os.path.join(ballot_file, Globals.get('BALLOT_FILE'))
        if style == 'json':
            # When the style is json, print all three dictionaries as one
            the_aggregate = {'contests': self.contests,
                             'active_ggos': self.active_ggos,
                             'ballot_subdir': self.ballot_subdir}
            with open(ballot_file, 'w', encoding="utf8") as outfile:
                outfile.write(pprint.pformat(the_aggregate))
        elif style == 'pdf':
            # See https://github.com/rst2pdf/rst2pdf
            raise NotImplementedError(("Apologies but printing the pdf of a ballot "
                                           "is not implemented yet"))
        else:
            raise NotImplementedError(f"Unsupported Ballot type ({style}) for writing")
        return ballot_file

    def read_a_ballot(self, address, config, ballot_file="", style='json'):
        """Will return the dictionary of a json ballot file"""
        if not ballot_file:
            ballot_file = os.path.join(config.get('git_rootdir'),
                                    address.get('ballot_node'),
                                    Globals.get('BLANK_BALLOT_SUBDIR'),
                                    style,
                                    Globals.get('BALLOT_FILE'))
        if style == 'json':
            with open(ballot_file, 'r', encoding="utf8") as file:
                json_doc = json.load(file)
                self.contests = json_doc['contest']
                self.active_ggos = json_doc['active_ggos']
                self.ballot_subdir = json_doc['ballot_subdir']
        else:
            raise NotImplementedError(f"Unsupported Ballot type ({style}) for reading")

    def write_a_cast_ballot(self, config, ballot_file=''):
        """
        Will write out a cast ballot in json
        """
        if not ballot_file:
            ballot_file = os.path.join(config.get('git_rootdir'),
                                    self.ballot_subdir,
                                    Globals.get('CONTEST_FILE_SUBDIR'))
            os.makedirs(ballot_file, exist_ok=True)
            ballot_file = os.path.join(ballot_file, Globals.get('CONTEST_FILE'))
        # might was well write out everything, yes?
        the_aggregate = {'contests': self.contests,
                         'active_ggos': self.active_ggos,
                         'ballot_subdir': self.ballot_subdir}
        with open(ballot_file, 'w', encoding="utf8") as outfile:
            outfile.write(pprint.pformat(the_aggregate))
        return ballot_file

# EOF
