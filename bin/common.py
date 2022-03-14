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

import json
import os
import re
import subprocess
#  Other imports:  critical, error, warning, info, debug
from logging import info

class Globals:
    """
    A placeholder for python code constants, not to be confused with VTP
    election tree constants which are located in the config.yaml files.
    """
    _config = {
        # The default location from the CWD of this program, which is different than
        # The location of the incoming ballot.json file etc
        'BALLOT_FILE': os.path.join('CVRs', 'ballot.json'),
        # The blank ballot folder location
        'BLANK_BALLOT_SUBDIR': 'blank-ballots',
        # The location/name of the config and address map files for this GGO
        'CONFIG_FILE': 'config.yaml',
        'ADDRESS_MAP_FILE': 'address_map.yaml',
        # The location of the contest cvr file
        'CONTEST_FILE': os.path.join('CVRs', 'contest.json'),
        # The required address fields for an address. There are two
        # types - GGO and non GGO.
        'REQUIRED_GGO_ADDRESS_FIELDS': ['state', 'town'],
        'REQUIRED_NG_ADDRESS_FIELDS': ['street', 'number'],
        # Root Election Data subdir
        'ROOT_ELECTION_DATA_SUBDIR': 'ElectionData',
        # How long to wait for a git shell command to complete - maybe a bad idea
        'SHELL_TIMEOUT': 15,
        }

    # Legitimate setters
    _setters = []

    @staticmethod
    def get(name):
        """A generic getter"""
        return Globals._config[name]

    @staticmethod
    def set(name, value):
        """A generic setter"""
        if name in Globals._setters:
            Globals._config[name] = value
        else:
            raise NameError("Name not accepted in set() method")

# pylint: disable=R0903   # ZZZ - remove this later
class Shellout:
    """
    A class to wrap the control & management of shell subprocesses,
    nominally git commands.
    """

    @staticmethod
    def run(argv, printonly=False, **kwargs):
        """Run a shell command with logging and error handling.  Raises a
        CalledProcessError if the shell command fails - the caller needs to
        deal with that.  Can also raise a TimeoutExpired exception.

        Nominally returns a CompletedProcess instance.

        See for example https://docs.python.org/3.9/library/subprocess.html
        """

        info(f"Running \"{' '.join(argv)}\"")
        if printonly:
            return subprocess.CompletedProcess(argv, 0, stdout="", stderr="")
        # pylint: disable=W1510 # the caller desides on whether check is set or not
        return subprocess.run(argv, timeout=Globals.get('SHELL_TIMEOUT'), **kwargs)

class Address:
    """A class to create an address object, which is just an address
    in a conanical dictionary form.  This just holds the address and
    will not validate it against a config and addpress_map data.  The
    class supports return the Address as either a string or a
    dictionary.

    Implementation note - individual address fields are never set to
    NoneType - if empty/blank, they are set to the empty string "".
    And all fields are strings, not numbers.
    """

    # Legitimate keys in the correct order
    _keys = ['number', 'street', 'substreet', 'town', 'state',
                 'country', 'zipcode']

    def __init__(self, **kwargs):
        """At the moment support only support a csv keyword and a
        reasonable dictionary set of keywords.
        """

        ok_keys = ['csv'] + Address._keys
        bad_keys = [key for key in kwargs if not key in ok_keys]
        if bad_keys:
            raise KeyError(f"The following Address keys are not supported: {bad_keys}")

        self.address = {}
        self.address['number'] = ""
        self.address['street'] = ""
        self.address['substreet'] = ""
        self.address['town'] = ""
        self.address['state'] = ""
        self.address['country'] = ""
        self.address['zipcode'] = ""

        if kwargs['csv']:
            address_fields = [x.strip() for x in re.split(r'\s*,\s*', kwargs['csv'])]
            self.address['number'] = address_fields[0]
            self.address['street'] = address_fields[1]
            if address_fields == 5:
                self.address['substreet'] = address_fields[2]
                self.address['town'] = address_fields[3]
                self.address['state'] = address_fields[4]
            else:
                self.address['substreet'] = ""
                self.address['town'] = address_fields[2]
                self.address['state'] = address_fields[3]
        else:
            for key, value in kwargs.items():
                if key == 'csv':
                    continue
                Address.set(self, key, value)

        # Note - an address needs all 'required' address fields to be specified
        required_fields = Globals.get('REQUIRED_GGO_ADDRESS_FIELDS') + \
          Globals.get('REQUIRED_NG_ADDRESS_FIELDS')
        missing_keys = [key for key in required_fields
                            if not Address.get(self, key)]
        if missing_keys:
            raise NameError(("Addresses must include values for the following fields: "
                                 f"{required_fields}"
                                 "The following fields are undefined: "
                                 f"{missing_keys}"))

    def __iter__(self):
        """Return an iterator for the address attribute"""
        return iter(self.address)

    def __str__(self):
        """Return a space separated string of the address"""
        nice_string = ""
        for key in Address._keys:
            if self.address[key]:
                nice_string += " " + self.address[key]
        return nice_string.strip()

    def get(self, name):
        """A generic getter - will raise a NameError if name is not defined"""
        if name in Address._keys:
            return self.address[name]
        if name == 'str_address':
            # return the number and street - ZZZ ignore substreet for now
            nice_string = self.address['number'] + ' ' + self.address['street']
            return nice_string.strip()
        raise NameError(f"Name {name} not accepted/defined for set()")

    def set(self, name, value):
        """A generic setter - will raise a NameError if name is not defined """
        if name in Address._keys:
            value = "" if value is None else value
            self.address[name] = value
        else:
            raise NameError(f"Name {name} not accepted/defined for Address.set()")

    def dict(self):
        """Return a dictionary of the address"""
        address = {}
        for key in Address._keys:
            address[key] = self.address[key]
        return address

class Ballot:
    """A class to hold a ballot.  A ballot is always a function of an
    address defined within the context of VTP election configuration
    as defined by the aggregated data in the config and address_map
    files.
    """

    # Map the ElectionConfig 'kind' to the Address 'kind'
    _kinds_map = {'state':'states', 'town':'towns', 'county':'counties',
                      'SchoolDistrict':'SchoolDistricts',
                      'CouncilDistrict':'CouncilDistricts',
                      'Precinct':'Precincts'}

    def __init__(self):
        """Constructor - just creates the dictionary and returns the
        object
        """
        self.ballot = {}
        self.active_ggos = []

    def get(self, name):
        """A generic getter - will raise a NameError if name is invalid"""
        if name == 'ggos':
            return self.active_ggos
        if name == 'ballot':
            return self.ballot
        raise NameError(f"Name {name} not accepted/defined for set()")

    def __str__(self):
        """Return the serialization of this instance's ElectionConfig dictionary"""
        return str(self.ballot)

    def dict(self):
        """Return a dictionary of the ballot"""
        return dict(self.ballot)

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

        footsteps = set()
        def find_ancestors(node_of_interest):
            """Will find all the ancestor of this node"""
            for parent in config.ancestors(node_of_interest):
                if parent in footsteps:
                    continue
                if parent not in self.active_ggos:
                    self.active_ggos.append(parent)
                footsteps.add(parent)
                find_ancestors(parent)

        def find_descendants(node_of_interest):
            """Will find all descendantss of this node"""
            for child in config.descendants(node_of_interest):
                if child in footsteps:
                    continue
                if child not in self.active_ggos:
                    self.active_ggos.append(child)
                footsteps.add(child)
                find_descendants(child)

        # Note - the root GGO always contributes
        self.active_ggos.append('root')
        # Walk the address in DAG order from root to a leaf.
        for field in Globals.get('REQUIRED_GGO_ADDRESS_FIELDS'):
            # For this field in the address, get the correct ggo kind and instance
            node = Ballot._kinds_map[field] + '/' + address.get(field)
            # Better to sanity check now later
            if not config.is_node(node):
                raise ValueError(f"Bad ElectionConfig node name ({node})")
            self.active_ggos.append(node)

        # Note that the first node in active_ggos is the root and the
        # last is the leaf most implicit node. However, there can be
        # descendant nodes (within this leaf node). For simplicity and
        # without knowing more at this time, only support ancestors
        # from this node and not from descendants of this node.
        the_address_node = self.active_ggos[-1]
        find_ancestors(the_address_node)

        # Now find any descendantss
        find_descendants(the_address_node)

        # With the list of active GGOs, add in the contests for each one
        # ZZZ

    def export(self, file="", syntax=""):
        """
        Will export a blank ballot to a file in some format.  If file
        is nil, will print to STDOUT.
        """
        if syntax in ('json', ''):
            if file == "":
                print(json.dumps(Ballot.dict(self)))
            else:
                with open(file, 'w', encoding="utf8") as outfile:
                    json.dump(Ballot.dict(self), outfile)
        elif syntax == 'pdf':
            # See https://github.com/rst2pdf/rst2pdf
            raise NotImplementedError(("Apologies but printing the pdf of a ballot "
                                           "is not implemented yet"))
        else:
            raise NotImplementedError(f"Unsupported Ballot export type ({syntax})")

# EOF
