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
        'BALLOT_FILE': 'ballot.json',
        # The blank ballot folder location
        'BLANK_BALLOT_SUBDIR': 'blank-ballots',
        # The location/name of the config and address map files for this GGO
        'CONFIG_FILE': 'config.yaml',
        'ADDRESS_MAP_FILE': 'address_map.yaml',
        # The location of the contest cvr file
        'CONTEST_FILE_SUBDIR': 'CVRs',
        'CONTEST_FILE': 'contest.json',
        # The required address fields for an address. To get around
        # the difficulty of creating a completely generic
        # address-to-ballot function at this time, these fields are
        # broken into two types.  The first ordered set goes from the
        # root ElectionData node to the lowest leaf level node where
        # the GGO boundaries are required to coherent (perfectly the
        # same).  The second set optionally continues until there are
        # no more leaf nodes.  This is arbitrary but the current
        # address-to-ballot implemention below is based on this.  ZZZ
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

# pylint: disable=too-few-public-methods   # ZZZ - remove this later
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
        # the caller desides on whether check is set or not
        # pylint: disable=subprocess-run-check
        return subprocess.run(argv, timeout=Globals.get('SHELL_TIMEOUT'), **kwargs)

# EOF
