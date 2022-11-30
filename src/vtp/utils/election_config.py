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

import logging
# standard imports
import os
import os.path
import re

import networkx
import yaml

# local imports
from .common import Globals, Shellout
from .contest import Contest


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

    Regarding the address_map.yaml file, wherever there is one defined
    (via 'unique-ballots'), the address blocks defined thus will
    specify where the matching addresses will drop the blank ballots
    and where the associated CVRs subfolder will also be placed.

    CURRENT RUNTIME RESTRICTIONS:

    The CWD must either be the root of workspace for the VTP election
    tree.  From a child submodule this would be the equivilent of

    $ git rev-parse --show-superproject-working-tree

    And from the root git workspace it is the equivilent of

    $ git rev-parse --show-toplevel
    """

    # Legitimate top-level keys
    _config_keys = ['GGOs', 'contests', 'submodules', 'voting centers']
    _address_map_keys = ['unique-ballots']
    _address_map_subkeys = ['addresses', 'ggos']

    # A simple numerical n digit GGO uid
    _uids = {}
    _nextuid = 0

    @staticmethod
    def get_next_uid(ggo):
        """Will return the next GGO uid (only good within the context of
        this specific election)
        """
        this_uid = str(ElectionConfig._nextuid).rjust(3, '0')
        if this_uid in ElectionConfig._uids:
            raise KeyError(f"A GGO uid cannot be reused (ggo={ggo}, uid={this_uid})")
        ElectionConfig._nextuid += 1
        ElectionConfig._uids[this_uid] = ggo
        return this_uid

    @staticmethod
    def is_valid_ggo_string(arg):
        """Check to see if it is a string without illegal characters."""
        if not isinstance(arg, str):
            raise TypeError(f"The GGO value is not a string ({arg})")
        if re.search(r'[^A-Za-z0-9 _\-\.]', arg):
            raise ValueError(f"The GGO value contains unsupported characters ({arg})")
        # ZZZ need a bunch more QA checks here and one day deal with unicode

    @staticmethod
    def check_config_syntax(config, filename):
        """Validate the config.yaml syntax"""
        bad_keys = [key for key in config if not key in ElectionConfig._config_keys]
        if bad_keys:
            raise KeyError(f"File ({filename}): "
                           f"the following config keys are not supported: {bad_keys}")

    @staticmethod
    def check_address_map_syntax(address_map, filename):
        """Validate the address_map.yaml syntax"""
        bad_keys = [key for key in address_map if not key in
                        ElectionConfig._address_map_keys]
        if bad_keys:
            raise KeyError(f"File ({filename}): "
                           f"the following address_map keys are not supported: {bad_keys}")
        # also check subkeys
        if 'unique-ballots' in address_map:
            for entry in address_map['unique-ballots']:
                bad_keys = [key for key in entry if not key in
                                ElectionConfig._address_map_subkeys]
                if bad_keys:
                    raise KeyError(f"File ({filename}): "
                                   "the following address_map subkeys are not "
                                   f"supported: {bad_keys}")

    @staticmethod
    def read_address_map(filename):
        """
        Read the address_map yaml file return the dictionary but
        only if the file exists.  Check the syntax.
        """
        if os.path.isfile(filename):
            logging.debug("Reading %s", filename)
            with open(filename, 'r', encoding="utf8") as map_file:
                this_address_map = yaml.load(map_file, Loader=yaml.FullLoader)
            # sanity-check it
            ElectionConfig.check_address_map_syntax(this_address_map, filename)
            return this_address_map
        return {}

    @staticmethod
    def read_config_file(filename):
        """
        Read the confgi yaml file return the dictionary and check the syntax.
        """
        logging.debug("Reading %s", filename)
        with open(filename, 'r', encoding="utf8") as config_file:
            config = yaml.load(config_file, Loader=yaml.FullLoader)
        # sanity-check it
        ElectionConfig.check_config_syntax(config, filename)
        # should really sanity check the contests too
        if 'contests' in config:
            for contest in config['contests']:
                Contest.check_contest_blob_syntax(contest, filename)
                Contest.set_uid(contest, '.')
        return config

    def __init__(self):
        """Stubbed out for now - returns an object reading to be
        populated with _this_ election config data.
        """

        # Determine the directory of the root config.yaml file.
        # 2022/05/02: there is no bin dir in any of the ElectionData
        # repos, so this test is no longer interesting (and blocks a
        # super parent repo to control multi scanner/server test
        # jigs).
        # result = Shellout.run(["git", "rev-parse", "--show-superproject-working-tree"],
        #                               check=False, capture_output=True, text=True)
        # if not result.stdout == "":
        #     raise EnvironmentError(("The CWD of the current process is not in the superproject"
        #                             f"working tree ({result.stdout})"))
        result = Shellout.run(["git", "rev-parse", "--show-toplevel"], check=True,
                                  capture_output=True, text=True)
        if result.stdout == "":
            raise EnvironmentError("Cannot determine workspace top level via 'git rev-parse'")
        self.git_rootdir = result.stdout.strip()
        self.root_config_file = os.path.join(self.git_rootdir,
                                                 Globals.get('ROOT_ELECTION_DATA_SUBDIR'),
                                                 Globals.get("CONFIG_FILE"))
        self.root_address_map_file = os.path.join(self.git_rootdir,
                                                      Globals.get('ROOT_ELECTION_DATA_SUBDIR'),
                                                      Globals.get("ADDRESS_MAP_FILE"))
        self.parsed_configs = ["."]
        self.digraph = networkx.DiGraph()
        self.uid = None

    def get(self, name):
        """A generic getter - will raise a NameError if name is not defined"""
        if name in ElectionConfig._config_keys:
            return getattr(self, "config")[name]
        if name in ElectionConfig._address_map_keys:
            return getattr(self, "config")[name]
        if name == "git_rootdir":
            return self.git_rootdir
        raise NameError((f"Name {name} is not a supported root level key "
                             "for the ElectionConfig dictionary"))

    def get_dag(self, what):
        """An ElectionConfig get interface to the underlying DiGraph class."""
        if what == 'nodes':
            return self.digraph.nodes()
        if what == 'edges':
            return self.digraph.edges()
        if what == 'topo':
            return list(networkx.topological_sort(self.digraph))
        if what == 'graph':
            # Danger - exposes implementation
            return self.digraph
        raise NameError(f"Method {what} is not a supported networkx method")

    def node(self, node):
        """Return the networkx node"""
        return self.digraph.nodes[node]

    def get_node(self, node, what):
        """An ElectionConfig get interface to the underlying election configuration data."""
        if what == 'ALL':
            return {'address_map': self.digraph.nodes[node]['address_map'],
                    'config': self.digraph.nodes[node]['config'],
                    'ggo_name': self.digraph.nodes[node]['ggo_name'],
                    'kind': self.digraph.nodes[node]['kind'],
                    'subdir': self.digraph.nodes[node]['subdir'],
                    'uid': self.digraph.nodes[node]['uid']}
        return self.digraph.nodes[node][what]

    def is_node(self, node_name):
        """Returns True/False if node_name exists"""
        if node_name in self.digraph:
            return True
        return False

    def ancestors(self, node):
        """Wrapper"""
        return networkx.ancestors(self.digraph, node)

    def descendants(self, node):
        """Wrapper"""
        return networkx.descendants(self.digraph, node)

    def __str__(self):
        """Return the serialization of this instance's ElectionConfig dictionary"""
        return str(list(self.get_dag('topo')))

    # This defunct with the address_map design change - there are no
    # lnnger any such thing as an implicit address include - all
    # address_map includes are now explicit in the address_map.yaml
    # files themselves. The digraph DAG is just the explicit GGO DAG
    # and not that plus an implicit address_map include.
    def add_additional_edges(self):
        """Will add implicit address includes from one
        parent/sibling to another sibling/child
        """
        for node in networkx.topological_sort(self.digraph):
            if 'unique-ballots' in self.digraph.nodes[node]['address_map']:
                for entry in self.digraph.nodes[node]['address_map']['unique-ballots']:
                    # Each unique-ballot is a unique sorted list of
                    # GGOs. And it is a syntax error if there is not a
                    # ggos subkey.
#                    import pdb; pdb.set_trace()
                    for ggo in entry['ggos']:
                        # if this edge does not exist, add it
                        if not self.digraph.has_edge(node, ggo):
                            self.digraph.add_edge(node, ggo)

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
        config = ElectionConfig.read_config_file(self.root_config_file)

        # read the root address_map and sanity check that
        address_map = ElectionConfig.read_address_map(self.root_address_map_file)

        def recursively_parse_tree(subdir, parent_node_name):
            """Something to recursivelty parse the GGO tree"""
            # If there are GGOs, parse each one
            if "GGOs" in self.digraph.nodes[parent_node_name]['config']:
                for ggo_kind, ggo_list in \
                  self.digraph.nodes[parent_node_name]['config']["GGOs"].items():
                    ElectionConfig.is_valid_ggo_string(ggo_kind)
                    if not isinstance(ggo_list, list):
                        raise TypeError(f"The GGO kind value is not a list ({ggo_kind})")
                    ggo_subdir_abspath = os.path.join(self.git_rootdir,
                                                          Globals.get('ROOT_ELECTION_DATA_SUBDIR'),
                                                          subdir, ggo_kind)
                    for ggo in ggo_list:
                        ElectionConfig.is_valid_ggo_string(ggo)
                        ggo_file = os.path.join(ggo_subdir_abspath, ggo, Globals.get("CONFIG_FILE"))
                        # read the child config
                        this_config = ElectionConfig.read_config_file(ggo_file)

                        # Do not hit a node twice - it is a config error if so
                        next_subdir = os.path.join(subdir, ggo_kind, ggo)
                        if next_subdir in self.parsed_configs:
                            raise LookupError(("Attempting to load the config file located at "
                                                   f"({next_subdir}) a second time"))
                        self.parsed_configs.append(next_subdir)

                        # Before recursing, read in address_map and add it to the node
                        # Note - reading will check syntax
                        this_address_map = ElectionConfig.read_address_map(os.path.join(
                            ggo_subdir_abspath, ggo, Globals.get("ADDRESS_MAP_FILE")))

                        # Now add this ggo_kind and ggo to the DAG.
                        # Always use '/' - nodes in the digraph always
                        # use forward slash, but subdir are os.path.sep
                        this_dag_node = os.path.join(subdir.replace('\\','/'),
                                                           ggo_kind, ggo)
                        if this_dag_node in self.digraph.nodes:
                            raise LookupError(("Attempting to re-add the same node "
                                                   f"into the DAG ({this_dag_node}) "
                                                   f"from file {next_subdir}"))
                        self.digraph.add_node(this_dag_node, kind=ggo_kind, config=this_config,
                            ggo_name=ggo,
                            uid=ElectionConfig.get_next_uid(ggo),
                            address_map=this_address_map,
                            subdir=os.path.join(subdir, ggo_kind, ggo))
                        self.digraph.add_edge(parent_node_name, this_dag_node)

                        # Recurse - depth first is ok
                        recursively_parse_tree(os.path.join(next_subdir, "GGOs"),
                            this_dag_node)

        # Now recursively walk the directory structure of config and
        # address_map files (depth first)
        self.digraph.add_node('.', kind='root', config=config, address_map=address_map,
                                  ggo_name='root',
                                  uid=ElectionConfig.get_next_uid('.'),
                                  subdir=".")
        recursively_parse_tree ("GGOs", '.')

    def gen_unique_ggo_name(self, active_ggos, filename):
        """
        Given a set of active ggos, create a unique ggo name.  For the
        time being, just sort order the ggos UIDs
        """
        ggo_unique_name = [self.get_node(ggo, 'uid') for ggo in active_ggos]
        # alphanumerically sort the string
        ggo_unique_name.sort(key=int)
        # for now, no error checking ...
        ggo_unique_name.append(filename)
        return ','.join(ggo_unique_name)

    def gen_blank_ballot_location(self, active_ggos, ballot_subdir, style='json'):
        """Return the file location of a blank ballot"""
        return os.path.join(
            self.get('git_rootdir'),
            Globals.get('ROOT_ELECTION_DATA_SUBDIR'),
            ballot_subdir,
            Globals.get('BLANK_BALLOT_SUBDIR'),
            style,
            self.gen_unique_ggo_name(
                active_ggos, Globals.get('BALLOT_FILE')))

# EOF
