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
        # the location of the incoming ballot.json file etc
        "BALLOT_FILE": os.path.join("CVRs", "ballot.json"),
        # the location of the config file for this GGO
        "CONFIG_FILE": "config.yaml",
        "ADDRESS_MAP_FILE": "address_map.yaml",
        # the location of the contest cvr file
        "CONTEST_FILE": os.path.join("CVRs", "contest.json"),
        # how long to wait for a git shell command to complete - maybe a bad idea
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
    """A class to wrap the control & management of subprocesses"""

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
    in a conanical dictionary form.  With GGO maps, will eventually
    support address validation et al.

    Implementation note - individual address fields are never set to
    NoneType - if empty/blank, they are set to "".
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
            address_fields = [x.strip() for x in kwargs['csv'].split(',')]
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
# EOF
