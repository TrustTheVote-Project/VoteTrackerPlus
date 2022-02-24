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

"""A kitchen sync for VTP classes for the moment"""

import os
import subprocess
#  Other imports:  critical, error, warning, info, debug
from logging import info
import yaml

class Globals:
    """
    A placeholder for python code constants, not to be confused with VTP
    election tree constants which are located in the config.yaml files.
    """
    __config = {
        # The default location from the CWD of this program, which is different than
        # the location of the incoming ballot.json file etc
        "BALLOT_FILE": os.path.join("CVRs", "ballot.json"),
        # the location of the config file for this GGO
        "CONFIG_FILE": "config.yaml",
        # the location of the contest cvr file
        "CONTEST_FILE": os.path.join("CVRs", "contest.json"),
        # how long to wait for a git shell command to complete - maybe a bad idea
        "SHELL_TIMEOUT": 15,
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

# pylint: disable=R0903   # ZZZ - remove this later
class Shellout:
    """A class to wrap the control & management of subprocesses"""

    @staticmethod
    def run(argv, check=False, printonly=False):
        """Run a shell command with logging and error handling.  Raises a
        CalledProcessError if the shell command fails - the caller needs to
        deal with that.  Can also raise a TimeoutExpired exception.

        Nominally returns a CompletedProcess instance.

        See for example https://docs.python.org/3.9/library/subprocess.html
        """

        info(f"Running \"{' '.join(argv)}\"")
        if printonly:
            return subprocess.CompletedProcess(argv, 0, stdout="", stderr="")
        return subprocess.run(argv, timeout=Globals.get('SHELL_TIMEOUT'), check=check)

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

class ElectionConfig:
    """A class to parse all the VTP election config.yaml files and
    return a VTP election config.

    Basically, as of 2022/02/22 the schema of the config.yaml is as
    follows:

    The top level config will list the next level 'child' GGOs.  Each
    GGO will have one and only one config file, but there can be
    multiple children (a.k.a. sibling) config files, such as a state
    having towns and counties or a town having school districts,
    alderpersons, or board members.  The name of the GGO is defined in
    the parent config file and the explicit list of instances thereof
    is an ordered list for that dictionary.

    This aggregate GGO data structure, referred to as the VTP election
    config, is a directed acyclic tree, ultimately ending in leaf
    nodes that do not contain a GGO section.

    There is another key for submoules which basically define the git
    submoduel tree.  The git submodule tree is used to create
    independent git repos so that a physical VTP geographic location
    can operate disconnected network/communication wise from the other
    git repos.  There is no required or prescribed connection between
    GGO subtrees and git submodules though in practice one will be
    created that probably is the most practical for a given election
    jurisdiction.

    For testing purposes, there need not be any git submodules, or
    rather that is part of the test configuration matrix.

    It is possible that a GGO only has a config file and a ballot.rst
    file in that it is not a GGO that is responsible for counting
    ballots.  A GGO that has the responsibility of counting ballots
    will contain a CVRs subdirectory in which to record the CVRs.

    The contests key lists the contests for this GGO.  The contests
    are an ordered list of dictionaries, the 'name' being the name of
    the contest and tally being the ty[e of tally.  A contest can then
    either contain condidate options or ballot measure options.  The
    legitimate options for a specific GGO are as they are listed in
    the GGO's contest dictionary.

    CURRENT RUNTIME RESTRICTIONS:

    The CWD must either be the root of workspace for the VTP election
    tree.  From a child submodule this would be the equivilent of

    $ git rev-parse --show-superproject-working-tree

    And from the root git workspace it is the equivilent of

    $ git rev-parse --show-toplevel
    """

    # Legitimate top-level keys
    __static_keys = ['GGOs', 'contests', 'submodules', 'vote centers']

    def __init__(self):
        """Stubbed out for now - returns an object reading to be
        populated with _this_ election config data.
        """

        # Determine the directory of the root config.yaml file
        result = Shellout.run(["git", "--rev-parse", "--show-superproject-working-tree"],
                                      check=True)
        if not result.stdout == "":
            raise EnvironmentError(f"The CWD of the current process is not in the superprohect \
            working tree ({result.stdout})")
        result = Shellout.run(["git", "--rev-parse", "--show-toplevel"], check=True)
        if result.stdout == "":
            raise EnvironmentError("The CWD of the current process is not in the a VTP git \
            root workspace")
        self.git_rootdir = result.stdout.strip

    def get_static_key(self, name):
        """A generic top level key getter - will raise a NameError if name is not defined"""
        if name in ElectionConfig.__static_keys:
            return getattr(self, name)
        raise NameError(f"Name {name} not accepted/defined for set()")

    def slurp_root_config(self):
        """Given an ElectionConfig, read the root config"""

        config_file = os.path.join(self.git_rootdir, Globals.get("CONFIG_FILE"))
        # read it
        with open(config_file, 'r', encoding="utf8") as file:
            yaml_doc = yaml.load(file, Loader=yaml.FullLoader)

        # sanity-check it
        bad_keys = [key for key in yaml_doc if not key in ElectionConfig.__static_keys]
        if bad_keys:
            raise KeyError(f"The following keys are not supported: {bad_keys}")

        return yaml_doc
