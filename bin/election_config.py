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

"""The VTP ElectionConfig class - everything needed to parse the config.yaml tree."""

# statndard imports
import os
import re
import yaml

# local imports
from common import Globals, Shellout

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
    _root_keys = ['GGOs', 'contests', 'submodules', 'vote centers']

    @staticmethod
    def is_valid_ggo_string(arg):
        """Check to see if it is a string without illegal characters."""
        if not isinstance(arg, str):
            raise TypeError(f"The GGO value is not a string ({arg})")
        if re.search(r'[^A-Za-z0-9_\-\.]', arg):
            raise ValueError(f"The GGO value contains unsupported characters ({arg})")
        # ZZZ need a bunch more QA checks here and one day deal with unicode

    def __init__(self):
        """Stubbed out for now - returns an object reading to be
        populated with _this_ election config data.
        """
        # The VTP ElectionConfig dictionary of all the parsed config.yaml files
        self.config = {}
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
        self.root_config_file = os.path.join(self.git_rootdir, Globals.get("CONFIG_FILE"))
        self.parsed_configs = ["."]

    def get_root_key(self, name):
        """A generic top level key getter - will raise a NameError if name is not defined"""
        if name in ElectionConfig._root_keys:
            return getattr(self, name)
        raise NameError(f"Name {name} not accepted/defined for set()")

    def parse_configs(self):
        """Will inspect the data in the root config and load the
        entire election config tree.  The walk is depth first and
        hitting a node twice is an error.

        The GGOs and config.yaml basically represent a double entry
        accounting system - both must exist for the specific
        config.yaml to be loaded.
        """
        # read the root config
        with open(self.root_config_file, 'r', encoding="utf8") as file:
            self.config = yaml.load(file, Loader=yaml.FullLoader)
        # sanity-check it
        bad_keys = [key for key in self.config if not key in ElectionConfig._root_keys]
        if bad_keys:
            raise KeyError(f"The following keys are not supported: {bad_keys}")

        def recursively_parse_tree(subdir, subtree):
            """Something to recursivelty parse the GGO tree"""
            # If there are GGOs, parse each one
            if "GGOs" in subtree:
                for ggo_kind, ggo_list in subtree["GGOs"].items():
                    ElectionConfig.is_valid_ggo_string(ggo_kind)
                    if not isinstance(ggo_list, list):
                        raise TypeError(f"The GGO kind value is not a list ({ggo_kind})")
                    ggo_subdir_abspath = os.path.join(self.git_rootdir, subdir, ggo_kind)
                    for ggo in ggo_list:
                        ElectionConfig.is_valid_ggo_string(ggo)
                        ggo_file = os.path.join(ggo_subdir_abspath, ggo)
                        # read the child config
                        with open(ggo_file, 'r', encoding="utf8") as file:
                            this_config = yaml.load(file, Loader=yaml.FullLoader)
                            # sanity-check it
                            bad_keys = [key for key in this_config
                                            if not key in ElectionConfig._root_keys]
                            if bad_keys:
                                raise KeyError(f"The following keys are not supported: {bad_keys}")
                            # Do not hit a node twice - it is a config error if so
                            next_subdir = os.path.join(subdir, ggo_kind, ggo)
                            if next_subdir in self.parsed_configs:
                                raise LookupError(f"Atttempting to load the config file located at \
                                ({next_subdir}) a second time")
                            self.parsed_configs.append(next_subdir)
                            # Add this dictionary and ggo relative subdir
                            if "GGO-tree" not in subtree:
                                subtree["GGO-tree"] = {}
                            if ggo_kind not in subtree["GGO-tree"]:
                                subtree["GGO-tree"][ggo_kind] = {}
                            subtree["GGO-tree"][ggo_kind][ggo] = this_config
                            # Record the relative ggo subdir
                            subtree["GGO-subdir"] = next_subdir
                            # Recurse - depth first is ok
                            recursively_parse_tree(subtree["GGO-subdir"],
                                                       subtree["GGO-tree"][ggo_kind][ggo])

        # Now recursively walk the tree (depth first)
        recursively_parse_tree ("", self.config)

# EOF
