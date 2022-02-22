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
A placeholder for python code constants, not to be confused with VTP
election tree constants which are located in the config.yaml files.
"""

class Globals:
    """A class for Globals ???"""
    __config = {
        # The default location from the CWD of this program, which is different than
        # the location of the incoming ballot.json file etc
        "BALLOT_FILE": "CVRs/ballot.json",
        # the location of the contest cvr file
        "CONTEST_FILE": "CVRs/contest.json",
        # how long to wait for a git shell command to complete - maybe a bad idea
        "GIT_SHELL_TIMEOUT": 15,
        }

    # Legitimate setters
    __setters = []

    @staticmethod
    def get(name):
        """A generic getter"""
        return Globals.__config[name]

    @staticmethod
    def set(name, value):
        """A generic setter"""
        if name in Globals.__setters:
            Globals.__config[name] = value
        else:
            raise NameError("Name not accepted in set() method")


class Address:
    """A class to create an address object, which is just an address in
    a conanical dictionary form.  With GGO maps, will eventually support
    address validation et al.
    """

    # Legitimate keys
    __keys = ['number', 'street', 'substreet', 'town']

    def __init__(self, **kwargs):
        """At the moment support only support a csv keyword and a
        reasonable dictionary set of keywords.  Eventually
        support more keywords.
        """

        if 'csv' in kwargs:
            address_fields = [x.strip() for x in kwargs['cvs'].split(',')]
            self.number = address_fields[0]
            self.street = address_fields[1]
            if address_fields == 4:
                self.substreet = address_fields[2]
                self.town = address_fields[3]
            else:
                self.substreet = ""
                self.town = address_fields[2]
        elif set(kwargs).issubset(Address.__keys):
            self.number = kwargs['number']
            self.street = kwargs['street']
            self.substreet = "" if 'substreet' not in kwargs else kwargs['substreet']
            self.town = kwargs['town']
        else:
            raise NameError("The only supported constructor keyword at this time is csv")

    def get(self, name):
        """A generic getter - will raise a NameError if name is not defined"""
        if name in Address.__keys:
            return getattr(self, name)
        raise NameError(f"Name {name} not accepted/defined for set()")

    def set(self, name, value):
        """A generic setter - will raise a NameError if name is not defined """
        if name in Address.__keys:
            setattr(self, name, value)
        else:
            raise NameError(f"Name {name} not accepted/defined for set()")
