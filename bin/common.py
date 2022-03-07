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
import pprint
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
        "BALLOT_FILE": os.path.join("CVRs", "ballot.json"),
        # The blank ballot folder location
        "BLANK_BALLOT_SUBDIR": "blank-ballots",
        # The location of the config file for this GGO
        "CONFIG_FILE": "config.yaml",
        "ADDRESS_MAP_FILE": "address_map.yaml",
        # The location of the contest cvr file
        "CONTEST_FILE": os.path.join("CVRs", "contest.json"),
        # How long to wait for a git shell command to complete - maybe a bad idea
        "SHELL_TIMEOUT": 15,
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
    """

    # Legitimate keys
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

        self.number = ""
        self.street = ""
        self.substreet = ""
        self.town = ""
        self.state = ""
        self.country = ""
        self.zipcode = ""

        if kwargs['csv']:
            address_fields = [x.strip() for x in re.split(r'\s*,\s*', kwargs['csv'])]
            self.number = address_fields[0]
            self.street = address_fields[1]
            if address_fields == 4:
                self.substreet = address_fields[2]
                self.town = address_fields[3]
            else:
                self.substreet = ""
                self.town = address_fields[2]
        else:
            for key, value in kwargs.items():
                if key == 'csv':
                    continue
                Address.set(self, key, value)

    def __str__(self):
        """Return a space separated string of teh address"""
        return(' '.join([self.number, self.street, self.substreet, self.town,
                   self.state, self.country, self.zipcode]))

    def get(self, name):
        """A generic getter - will raise a NameError if name is not defined"""
        if name in Address._keys:
            return getattr(self, name)
        raise NameError(f"Name {name} not accepted/defined for set()")

    def set(self, name, value):
        """A generic setter - will raise a NameError if name is not defined """
        if name in Address._keys:
            value = "" if value is None else value
            setattr(self, name, value)
        else:
            raise NameError(f"Name {name} not accepted/defined for Address.set()")

    def dict(self):
        """Return a dictionary of the address"""
        address = {}
        for key in Address._keys:
            address[key] = getattr(self, key)
        return address

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
        self.ballot = {}

    def create_blank_ballot(self, address, config):
        """Given an Address and a ElectionConfig, will generate the
        appropriate blank ballot.  Implementation note - this function
        needs to be smart in that it needs to deal with various regex
        and other rules/conventions/specs of the address_map files.
        The development of the support of that is an R&D iterative
        process.

        Initially this class/functions only understand two address_map
        syntaxes (defined in ElectionConfig which is what parses the
        address_map files).

        'address_map': {'ggos': {<ggo-kind>: ['.*']}

        'address_map': {'addresses': ['.*']}

        Where <ggo-kind> is the name of the child GGO group (there can
        be different 'kinds' of GGO children).  The above syntax
        follows what is known 'regex' expressions.

        The first defines that the addresses for this GGO are handled
        by the ggo-kind/ggo specified, which is in this case all ggos
        of the specified kind.  In other words, the parent GGO accepts
        all the addresses that specified child GGOs accept.

        The second defines that all the addresses in this specific GGO
        are valid for this GGO.

        ZZZ
        """
        # For now, error if the address_map tree does not end with a
        # valid address.  Return the blank ballot otherwise.

    def __str__(self):
        """Return the serialization of this instance's ElectionConfig dictionary"""
        return pprint.pformat(self.ballot)

    def dict(self):
        """Return a dictionary of the ballot"""
        return dict(self.ballot)

    def export(self, file="", syntax=""):
        """
        Will export a blank ballot to a file in some format.  If file
        is nil, will print to STDOUT.
        """
        if syntax == 'json':
            if file == "":
                print(json.dumps(self.ballot))
            else:
                with open(file, 'w', encoding="utf8") as outfile:
                    json.dump(self.ballot, outfile)
        elif syntax == 'pdf':
            # See https://github.com/rst2pdf/rst2pdf
            raise NotImplementedError(("Apologies but printing the pdf of a ballot "
                                           "is not implemented yet"))
        else:
            raise NotImplementedError(f"Unsupported Ballot export type ({syntax})")

# EOF
