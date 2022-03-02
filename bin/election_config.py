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
    _root_config_keys = ['GGOs', 'contests', 'submodules', 'vote centers']
    _root_address_map_keys = ['includes']

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
        self.address_map = {}
        # Determine the directory of the root config.yaml file
        result = Shellout.run(["git", "rev-parse", "--show-superproject-working-tree"],
                                      check=False, capture_output=True, text=True)
        if not result.stdout == "":
            raise EnvironmentError(("The CWD of the current process is not in the superproject"
                                    f"working tree ({result.stdout})"))
        result = Shellout.run(["git", "rev-parse", "--show-toplevel"], check=True,
                                  capture_output=True, text=True)
        if result.stdout == "":
            raise EnvironmentError("Cannot determine workspace top level via 'git rev-parse'")
        self.git_rootdir = result.stdout.strip()
        self.root_config_file = os.path.join(self.git_rootdir, Globals.get("CONFIG_FILE"))
        self.root_address_map_file = os.path.join(self.git_rootdir, Globals.get("ADDRESS_MAP_FILE"))
        self.parsed_configs = ["."]

    def get_root_key(self, name):
        """A generic top level key getter - will raise a NameError if name is not defined"""
        if name in ElectionConfig._root_config_keys:
            return getattr(self, name)
        raise NameError(f"Name {name} not accepted/defined for set()")

    def parse_configs(self):
        """Will inspect the data in the root config and load the
        entire election config tree.  The walk is depth first and
        hitting a node twice is an error.

        The GGOs and config.yaml basically represent a double entry
        accounting system - both must exist for the specific
        config.yaml to be loaded.

        This will load both the config and address_map yaml data
        """

        # read the root config and address_map files
        with open(self.root_config_file, 'r', encoding="utf8") as file:
            self.config = yaml.load(file, Loader=yaml.FullLoader)
        # sanity-check it
        bad_keys = [key for key in self.config if not key in ElectionConfig._root_config_keys]
        if bad_keys:
            raise KeyError(f"The following config keys are not supported: {bad_keys}")

        # read the root address_map and sanity check that
        with open(self.root_address_map_file, 'r', encoding="utf8") as file:
            self.address_map = yaml.load(file, Loader=yaml.FullLoader)
        bad_keys = [key for key in self.address_map if not key in
                        ElectionConfig._root_address_map_keys]
        if bad_keys:
            raise KeyError(f"The following address_map keys are not supported: {bad_keys}")

        def recursively_parse_tree(subdir, subtree):
            """Something to recursivelty parse the GGO tree"""
            # If there are GGOs, parse each one
            if "GGOs" in subtree:
                for ggo_kind, ggo_list in subtree["GGOs"].items():
                    ElectionConfig.is_valid_ggo_string(ggo_kind)
                    if not isinstance(ggo_list, list):
                        raise TypeError(f"The GGO kind value is not a list ({ggo_kind})")
                    ggo_subdir_abspath = os.path.join(self.git_rootdir, subdir, ggo_kind)
                    ggo_index = 0
                    for ggo in ggo_list:
                        ElectionConfig.is_valid_ggo_string(ggo)
                        ggo_file = os.path.join(ggo_subdir_abspath, ggo, Globals.get("CONFIG_FILE"))
                        # read the child config
                        with open(ggo_file, 'r', encoding="utf8") as file:
                            this_config = yaml.load(file, Loader=yaml.FullLoader)
                            # sanity-check it
                            bad_keys = [key for key in this_config
                                            if not key in ElectionConfig._root_config_keys]
                            if bad_keys:
                                raise KeyError(("The following config keys are not supported: "
                                                    f"{bad_keys}"))

                            # Do not hit a node twice - it is a config error if so
                            next_subdir = os.path.join(subdir, ggo_kind, ggo)
                            if next_subdir in self.parsed_configs:
                                raise LookupError(("Atttempting to load the config file located at "
                                                       f"({next_subdir}) a second time"))
                            self.parsed_configs.append(next_subdir)

                            # Replace the array value (a string) with
                            # a dictionary of this current config at
                            # the correct index
                            new_node = {"ggo-name": ggo, "ggo-subdir": next_subdir,
                                            "ggo-subtree": this_config}
                            subtree["GGOs"][ggo_kind][ggo_index] = new_node

                            # Before recursing, read in address_map
                            address_map_file = os.path.join(ggo_subdir_abspath, ggo,
                                                            Globals.get("ADDRESS_MAP_FILE"))
                            with open(address_map_file, 'r', encoding="utf8") as am_file:
                                this_address_map = yaml.load(am_file, Loader=yaml.FullLoader)
                                # sanity-check it
                                bad_keys = [key for key in this_address_map
                                                if not key in ElectionConfig._root_address_map_keys]
                                if bad_keys:
                                    raise KeyError(("The following address_map keys are not "
                                                        f"supported: {bad_keys}"))
                                # Add the incoming address_map dictionary to the dictionary
                                new_address_map = {"address-map": this_address_map}
                                subtree["GGOs"][ggo_kind][ggo_index].update(new_address_map)

                            # Recurse - depth first is ok
                            import pdb; pdb.set_trace()
                            recursively_parse_tree(os.path.join(subtree["GGO-subdir"], "GGOs"),
                                                       subtree["GGO-subtree"][ggo_kind][ggo])
                            # bump the index
                            ggo_index += 1

        # Now recursively walk the tree (depth first)
        recursively_parse_tree ("GGOs", self.config)

# EOF
