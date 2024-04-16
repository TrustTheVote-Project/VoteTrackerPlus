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

# pylint: disable=too-few-public-methods

# standard imports
import os


class Globals:
    """
    A placeholder for python code constants, not to be confused with VTP
    election tree constants which are located in the config.yaml files.
    """

    # ZZZ - apparently the pythonic way to make these read only is to
    # change them to properties.  For now have no setters.
    _config = {
        # The default location from the CWD of this program, which is different than
        # The location of the incoming ballot.json file etc
        "BALLOT_FILE": "ballot.json",
        "CONTEST_FILE": "contest.json",
        "RECEIPT_FILE": "receipt",
        # The blank ballot folder location
        "BLANK_BALLOT_SUBDIR": "blank-ballots",
        # The location/name of the config and address map files for this GGO
        "CONFIG_FILE": "config.yaml",
        "ADDRESS_MAP_FILE": "address_map.yaml",
        # The location of the contest cvr file
        "CONTEST_FILE_SUBDIR": "CVRs",
        # The location of the ballot receipts (and other QR files etc.
        # Note - files are always explicitly checked in (or .gitognore
        # can be set), so just place the non versioned file in the
        # same directory as the receipt so that it is easier to
        # reference the QR image
        "RECEIPT_FILE_SUBDIR": "RECEIPTs",
        # The required address fields for an address. To get around
        # the difficulty of creating a completely generic
        # address-to-ballot function at this time, these fields are
        # broken into two types.  The first ordered set goes from the
        # root ElectionData node to the lowest leaf level node where
        # the GGO boundaries are required to be coherent (perfectly
        # the same).  The second set optionally continues until there
        # are no more leaf nodes.  This is arbitrary but the current
        # address-to-ballot implemention below is based on this.  In
        # addtion this decision also is reflected in several other
        # spots as well :-( - sorry.  Basically, the REQUIRED_GGO list
        # is where the CVR and blank ballots are placed.
        "REQUIRED_GGO_ADDRESS_FIELDS": ["state", "town"],
        "REQUIRED_NG_ADDRESS_FIELDS": ["street", "number"],
        # Whether or not VTP has been locally installed
        "VTP_LOCAL_INSTALL": True,
        # The default verbosity
        "DEFAULT_VERBOSITY": 3,
        # Where the bin directory is relative from the root of _this_ repo
        "BIN_DIR": "src/vtp",
        # How long to wait for a git shell command to complete - maybe a bad idea
        "SHELL_TIMEOUT": 15,
        # Number of ballots on a ballot receipt
        "BALLOT_RECEIPT_ROWS": 100,
        # Map the ElectionConfig 'kind' to the Address 'kind'
        "kinds_map": {
            "state": "states",
            "town": "towns",
            "county": "counties",
            "SchoolDistrict": "SchoolDistricts",
            "CouncilDistrict": "CouncilDistricts",
            "Precinct": "Precincts",
        },
        # Note - all three of the following folders hold git repos
        # where the remote is a bare clone of the upstream/remote
        # GitHub ElectionData repo. In an attempt at clarity, the word
        # 'workspace' here refers to a non bare repo, 'upstream' is
        # the parent repo, and 'remote' means non-local to this
        # computer (requires a TPC/IP connection to get to).
        # The subdirectory where the FastAPI connection git workspaces are stored
        "GUID_CLIENT_DIRNAME": "guid-client-store",
        # The subdirectory where the local tabulation git workspace is stored
        "TABULATION_SERVER_DIRNAME": "tabulation-server",
        # The subdirectory where the mock scanner git workspaces are stored
        "MOCK_CLIENT_DIRNAME": "mock-clients",
        # Default runtime location of everything
        "DEFAULT_RUNTIME_LOCATION": "/opt/VoteTrackerPlus/demo.01",
        # The election date-time for all ElectionData commits
        "ELECTION_DATETIME": "2024-11-05T12:00:00",
        # The arbitrary election data string
        # "ELECTION_UPSTREAM_REMOTE": "https://github.com/TrustTheVote-Project/"
        # + "VTP-mock-election.US.16",
        "ELECTION_UPSTREAM_REMOTE": "http://127.0.0.1:8000/static",
    }

    @staticmethod
    def get(name):
        """A generic getter"""
        return Globals._config[name]

    @staticmethod
    def set_election_upstream_remote(value):
        """Set the ELECTION_UPSTREAM_REMOTE"""
        Globals._config["ELECTION_UPSTREAM_REMOTE"] = value

    @staticmethod
    def verify_election_data_dir(election_data_dir: str):
        """
        Verify that election_data_dir is an existing directory.
        """
        if not os.path.isdir(election_data_dir):
            raise ValueError(
                f"The provided --election_data value ({election_data_dir}) does not exist"
            )
