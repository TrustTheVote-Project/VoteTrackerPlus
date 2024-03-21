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
Logic of operation for setting up a VTP demo.  See the --help output
or the README.md file in the src/vtp directory for details.
"""

# Standard imports
import os
import re
import secrets

# Project imports
from vtp.core.common import Globals
from vtp.core.election_config import ElectionConfig

# Local imports
from .operation import Operation


class SetupVtpDemoOperation(Operation):
    """
    A class to implememt the setup-vtp-demo operation.  See the
    setup-vtp-demo help output or read the parse_argument argparse
    description (immediately below this) in the source file.
    """

    @staticmethod
    def get_all_guid_workspaces() -> list:
        """
        Will return a list of all the existing guid workspaces
        """
        guid_dir = os.path.join(
            Globals.get("DEFAULT_RUNTIME_LOCATION"),
            Globals.get("GUID_CLIENT_DIRNAME"),
        )
        file_list = os.listdir(guid_dir)
        guids = []
        for thing in file_list:
            path = os.path.join(guid_dir, thing)
            if not os.path.isdir(path) or not re.match("^[0-9a-f]{2}$", thing):
                continue
            for subdir in os.listdir(path):
                if os.path.isdir(os.path.join(path, subdir)) and re.match(
                    "^[0-9a-f]{38}$", subdir
                ):
                    guids.append(thing + subdir)
        return guids

    def __init__(
        self,
        election_data_dir: str = "",
        verbosity: int = 3,
        printonly: bool = False,
    ):
        """
        Primarily to module-ize the scripts and keep things simple,
        idiomatic, and in different namespaces.
        """
        super().__init__(election_data_dir, verbosity, printonly)
        # The absolute path to the local bare clone of the upstream
        # GitHub ElectionData remote repo
        self.tabulation_local_upstream_absdir = ""

    def __repr__(self):
        """Boilerplate"""
        return (
            "election_data_dir="
            + self.election_data_dir
            + "\ntabulation server="
            + self.tabulation_local_upstream_absdir
        )

    def create_client_repos(self, clone_dirs, upstream_url):
        """
        Create demo clients workspaces.  The first arg is an list of
        directories in which to create the clone.  The second arg is
        the remote URL which can be a path
        """
        # Now locally clone those as needed.  With the python/poetry
        # local install idiom, the demo location no longer needs the
        # submodules to be cloned.
        for clone_dir in clone_dirs:
            if not self.printonly:
                with self.changed_cwd(clone_dir):
                    self.shell_out(
                        ["git", "clone", upstream_url],
                        check=True,
                    )
            else:
                self.imprimir(f"Entering dir ({clone_dir}):", 5)
                self.imprimir(f"Running git clone {upstream_url}", 3)
                self.imprimir(f"Leaving dir ({clone_dir}):", 5)

    def create_a_guid_workspace_folder(self, location: str):
        """creates guid workspace"""
        guid = secrets.token_hex(20)
        folder1 = guid[:2]
        folder2 = guid[2:]
        # Note - mkdir raises an error if the directory exists. So
        # just try creating them.
        path1 = os.path.join(
            location,
            Globals.get("GUID_CLIENT_DIRNAME"),
            folder1,
        )
        path2 = os.path.join(path1, folder2)
        if not self.printonly:
            try:
                self.imprimir(f"creating ({path1}) if it does not exist", 5)
                os.mkdir(path1)
            except FileExistsError:
                pass
            # make sure it is a directory
            if not os.path.isdir(path1):
                raise RuntimeError(
                    f"Run time error - {folder1} is not a directory"
                    f" (for path {path1})"
                )
            # if after 3 tries it still does not work, raise an error
            count = 0
            while True:
                count += 1
                try:
                    self.imprimir(f"creating ({path2})", 5)
                    os.mkdir(path2)
                except FileExistsError as exc:
                    if count > 3:
                        # raise an error
                        raise RuntimeError(
                            "could not create a GUID directory after 3 tries - giving up"
                        ) from exc
                    # otherwise try again
                    folder2 = secrets.token_hex(18)
                    continue
                # success
                break
        else:
            self.imprimir(f"creating ({path1}) if it does not exist", 5)
            self.imprimir(f"creating ({path2}) if it does not exist", 5)

        # Clone the repo from the local clone, not the GitHub remote clone
        self.create_client_repos([path2], self.tabulation_local_upstream_absdir)
        # return the GUID
        self.imprimir(f"returning guid ({guid})", 5)
        return guid

    # pylint: disable=duplicate-code
    def run(
        self,
        scanners: int = 4,
        guid_client_store: bool = False,
        location: str = Globals.get("DEFAULT_RUNTIME_LOCATION"),
    ) -> str:
        """Main function - see -h for more info"""

        # Create a VTP ElectionData object if one does not already exist
        the_election_config = ElectionConfig.configure_election(
            self, self.election_data_dir
        )

        # Get the election data native GitHub remote clone name from _here_
        with self.changed_cwd(the_election_config.get("git_rootdir")):
            election_data_remote_url = self.shell_out(
                ["git", "config", "--get", "remote.origin.url"],
                printonly_override=True,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()

        # Need the complete absolute path to the local upstream bare
        # repo (a.k.a. the tabulation server). Since it will be bare,
        # that name will contain a .git suffix while the client
        # workspaces (client and server) will not have that suffix
        # (and not be bare).
        self.tabulation_local_upstream_absdir = os.path.join(
            location,
            Globals.get("TABULATION_SERVER_DIRNAME"),
            os.path.basename(election_data_remote_url),
        )
        # Need both the above and the dirname of the above
        bare_clone_path = os.path.dirname(self.tabulation_local_upstream_absdir)
        # When creating a GUID workspace ...
        if guid_client_store:
            return self.create_a_guid_workspace_folder(location)

        # ... or the initial setup of the non-GUID client and server workspaces

        # Only run if the directory is empty
        if len(os.listdir(location)) != 0:
            raise RuntimeError(
                f"the directory ({location}) is not empty - "
                "setup-vtp-demo can only be run on an empty directory"
            )

        # First create the necessary subdirectories
        for subdir in [
            Globals.get("GUID_CLIENT_DIRNAME"),
            Globals.get("TABULATION_SERVER_DIRNAME"),
            Globals.get("MOCK_CLIENT_DIRNAME"),
        ]:
            full_dir = os.path.join(location, subdir)
            if not os.path.isdir(full_dir):
                self.imprimir(f"creating ({full_dir})", 5)
                if not self.printonly:
                    os.mkdir(full_dir)

        # Second clone the bare upstream remote GitHub ElectionData repo
        if not self.printonly:
            with self.changed_cwd(bare_clone_path):
                self.shell_out(
                    ["git", "clone", "--bare", election_data_remote_url],
                    check=True,
                )
        else:
            self.imprimir(f"Entering dir ({bare_clone_path}):", 5)
            self.imprimir(f"Running git clone --bare {election_data_remote_url}", 3)
            self.imprimir(f"Leaving dir ({bare_clone_path}):", 5)

        # Third create the mock scanner client subdirs
        clone_dirs = []
        for count in range(scanners):
            full_dir = os.path.join(
                location,
                Globals.get("MOCK_CLIENT_DIRNAME"),
                "scanner." + f"{count:02d}",
            )
            if not os.path.isdir(full_dir):
                self.imprimir(f"creating ({full_dir})", 5)
                if not self.printonly:
                    os.mkdir(full_dir)
            clone_dirs.append(full_dir)

        # Fourth create the tabulation client subdir
        full_dir = os.path.join(
            location,
            Globals.get("MOCK_CLIENT_DIRNAME"),
            "server",
        )
        if not os.path.isdir(full_dir):
            self.imprimir(f"creating ({full_dir})", 5)
            if not self.printonly:
                os.mkdir(full_dir)
        clone_dirs.append(full_dir)

        # Fifth, with the GitHub remote ElectionData repo cloned
        # (bare) and with all the necessary client workspaces created,
        # create the client workspaces.
        self.create_client_repos(clone_dirs, self.tabulation_local_upstream_absdir)

        # return something
        return ""


# EOF
