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

# standard imports
import json
import os
import re

# local imports
from .common import Globals


class WebAPI:
    """Helper functions to support the web-api"""

    @staticmethod
    def verify_election_data_dir(election_data_dir: str):
        """
        Verify that election_data_dir is an existing directory.
        """
        if not os.path.isdir(election_data_dir):
            raise ValueError(
                f"The provided --election_data value ({election_data_dir}) does not exist"
            )

    @staticmethod
    def get_generic_ro_edf_dir() -> str:
        """
        Will return a generic EDF workspace so to be able to execute
        generic/readonly commands.  It is 'readonly' because any
        number of processes could be executing in this one git
        workspace at the same time and if any them wrote anything, it
        would be bad.
        """
        edf_path = os.path.join(
            Globals.get("DEFAULT_RUNTIME_LOCATION"),
            Globals.get("MOCK_CLIENT_DIRNAME"),
            "scanner.00",
        )
        # Need to verify that there is only _one_ directory in the edf_path
        dirs = [
            name
            for name in os.listdir(edf_path)
            if os.path.isdir(os.path.join(edf_path, name))
        ]
        if len(dirs) > 1:
            raise ValueError(
                f"The mock client directory ({edf_path}) ",
                "contains multiple subdirs - there can only be one ",
                "as there should only be one EDF clone in this directory",
            )
        if len(dirs) == 0:
            raise ValueError(
                f"The mock client directory ({edf_path}) ",
                "is empty - there needs to be exactly one git clone ",
                "of a ElectionData repo",
            )
        return os.path.join(edf_path, dirs[0])

    @staticmethod
    def get_guid_based_edf_dir(guid: str) -> str:
        """
        Return the default runtime location for a guid based
        workspace.  The actual ElectionData clone directory can be
        named anything.  HOWEVER it is assumed (REQUIRED) that there
        is only one clone in this directory, which is reasonable given
        that the whole tree from '/' is nominally created by the
        setup-vtp-demo operation.
        """
        if len(guid) != 40:
            raise ValueError(f"The provided guid is not 40 characters long: {guid}")
        if not re.match("^[0-9a-f]+$", guid):
            raise ValueError(
                f"The provided guid contains characters other than [0-9a-f]: {guid}"
            )
        edf_path = os.path.join(
            Globals.get("DEFAULT_RUNTIME_LOCATION"),
            Globals.get("GUID_CLIENT_DIRNAME"),
            guid[:2],
            guid[2:],
        )
        # Need to verify that the _only_ directory in edf_path is a
        # valid EDF tree via some clone
        dirs = [
            name
            for name in os.listdir(edf_path)
            if os.path.isdir(os.path.join(edf_path, name))
        ]
        if len(dirs) > 1:
            raise ValueError(
                f"The provided guid ({guid}) based path ({edf_path}) ",
                "contains multiple subdirs - there can only be one",
            )
        if len(dirs) == 0:
            raise ValueError(
                f"The guid directory ({edf_path}) ",
                "is empty - there needs to be exactly one git clone ",
                "of a ElectionData repo",
            )
        return os.path.join(edf_path, dirs[0])

    @staticmethod
    def convert_git_log(stdout: list):
        """
        Will convert the STDOUT of git log -1 <digest> to a dictionary
        """
        output = {}
        log_string = ""
        regex = re.compile(r"\s+")
        blank = re.compile(r"^\s*$")
        for index, line in enumerate(stdout):
            match index:
                case 0:
                    output["commit"] = regex.split(line, maxsplit=1)[1]
                case 1:
                    output["Author"] = regex.split(line, maxsplit=1)[1]
                case 2:
                    output["Date"] = regex.split(line, maxsplit=1)[1]
                case 3:
                    pass
                case _:
                    if blank.match(line):
                        continue
                    log_string += line.strip()
        output["Log"] = json.loads(log_string)
        return output
