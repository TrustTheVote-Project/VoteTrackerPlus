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
setup_vtp_demo.py - command line level script set up a VTP demo

See './setup_vtp_demo -h' for usage information.

See ../../docs/tech/run_mock_election.md for the context in which this
file was created.
"""

# Standard imports
# pylint: disable=wrong-import-position   # import statements not top of file
import argparse
import logging
import os
import secrets
import sys

# Local import
from vtp.utils.common import Globals, Shellout


class SetupVtpDemoLib:
    """A class to wrap the run_mock_election.py script."""

    # Note - all three of these folders hold git repos where the
    # remote is a bare clone of the upstream/remote GitHub
    # ElectionData repo. In an attempt at clarity, the word
    # 'workspace' here refers to a non bare repo, 'upstream' is the
    # parent repo, and 'remote' means non-local to this computer
    # (requires a TPC/IP connection to get to).

    # The subdirectory where the FastAPI connection git workspaces are stored
    _guid_client_dirname = "guid-client-store"
    # The subdirectory where the local tabulation git workspace is stored
    _tabulation_server_dirname = "tabulation-server"
    # The subdirectory where the mock scanner git workspaces are stored
    _mock_client_dirname = "mock-clients"

    def __init__(self, argv):
        """Only to module-ize the scripts and keep things simple and idiomatic."""
        # Unparsed args nominally from argv or the constructor caller
        # - must be strings
        self.argv = argv
        # Parsed args
        self.parsed_args = None
        # The absolute path to the local bare clone of the upstream
        # GitHub ElectionData remote repo
        self.tabulation_local_upstream_absdir = ""
        # hrmph, parse the args now even though it is in the constructor
        self.parse_arguments()

    def __str__(self):
        """Boilerplate"""
        return (
            "argv="
            + str(self.argv)
            + "\nparsed_args="
            + str(self.parsed_args)
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
            with Shellout.changed_cwd(clone_dir):
                Shellout.run(
                    ["git", "clone", upstream_url],
                    self.parsed_args.printonly,
                    verbosity=self.parsed_args.verbosity,
                )

    ################
    # arg parsing
    ################
    # pylint: disable=duplicate-code
    def parse_arguments(self):
        """Parse arguments from a command line"""

        parser = argparse.ArgumentParser(
            description="""Will leverage this current git repository
                        (VoteTrackerPlus) and the associated
                        ElectionData repo(s) to nominally create in
                        /opt/VoteTrackerPlus (the default) a demo
                        election mock with 4 mock ballot scanner apps
                        and one tabulation server app.  The initial
                        demo idea is to have three scanners scanning
                        random ballots while one scanner is used
                        interactively.

                        All five apps run in separate git repos that
                        are clones of the same ElectionData repo(s).
                        The (4) mock scanner app clones are located in
                        the 'mock-clients' folder, the one tabulation
                        server is located in the 'tabulation-server'
                        folder, and the FASTapi clients are located in
                        the 'client-store' folder via two subfolders
                        driven by a GUID for each FASTapi client.

                        If the --guid_client_store option is set,
                        instead of setting up the demo this script
                        will create a new GUID based FASTapi clone and
                        return the GUID.
                        """
        )
        parser.add_argument(
            "-s",
            "--scanners",
            type=int,
            default=4,
            help="specify a number of scanner app instances (def=4)",
        )
        parser.add_argument(
            "-g",
            "--guid_client_store",
            action="store_true",
            help="if set will create a single GUID based ballot-store and return the GUID",
        )
        parser.add_argument(
            "-l",
            "--location",
            default="/opt/VoteTrackerPlus/demo.01",
            help="specify the location of VTP demo (def=/opt/VoteTrackerPlus/demo.01)",
        )
        parser.add_argument(
            "-v",
            "--verbosity",
            type=int,
            default=3,
            help="0 critical, 1 error, 2 warning, 3 info, 4 debug (def=3)",
        )
        parser.add_argument(
            "-n",
            "--printonly",
            action="store_true",
            help="will printonly and not write to disk (def=True)",
        )
        self.parsed_args = parser.parse_args([str(x) for x in self.argv])
        verbose = {
            0: logging.CRITICAL,
            1: logging.ERROR,
            2: logging.WARNING,
            3: logging.INFO,
            4: logging.DEBUG,
        }
        logging.basicConfig(
            format="%(message)s",
            level=verbose[self.parsed_args.verbosity],
            stream=sys.stdout,
        )
        # Validate required args
        if self.parsed_args.scanners < 1 or self.parsed_args.scanners > 16:
            raise ValueError(
                "The demo needs at least one TVP scanner app "
                "and arbitrarily limits a demo to 16."
            )
        # Check the root of the demo
        if not os.path.isdir(self.parsed_args.location):
            raise FileNotFoundError(
                f"The root demo folder, {self.parsed_args.location}, does not exit.  "
                "It needs to pre-exist - please manually create it."
            )
        test_dir = os.path.join(
            self.parsed_args.location, SetupVtpDemoLib._tabulation_server_dirname
        )
        if self.parsed_args.guid_client_store and not os.path.isdir(test_dir):
            raise FileNotFoundError(
                f"The tabulation server workspace ({test_dir}) does not exit.  "
                "It needs to pre-exist and is created when setup-vtp-demo is executed "
                "in setup mode (without the -g switch)."
            )

    def create_a_guid_workspace_folder(self):
        """creates guid workspace"""
        guid = secrets.token_hex(10)
        folder1 = guid[:2]
        folder2 = guid[2:]
        # Note - mkdir raises an error if the directory exists. So
        # just try creating them.
        path1 = os.path.join(self.parsed_args.location, folder1)
        try:
            logging.debug("creating (%s) if it does not exist", path1)
            os.mkdir(path1)
        except FileExistsError:
            pass
        # make sure it is a directory
        if not os.path.isdir(path1):
            raise RuntimeError(
                f"Run time error - {folder1} is not a directory" f" (for path {path1})"
            )
        # if after 3 tries it still does not work, raise an error
        count = 0
        while True:
            count += 1
            path2 = os.path.join(path1, folder2)
            try:
                logging.debug("creating (%s)", path2)
                os.mkdir(path2)
            except FileExistsError as exc:
                if count > 3:
                    # raise an error
                    raise RuntimeError(
                        "could not create a GUID directory after 3 tries - giving up"
                    ) from exc
                # otherwise try again
                folder2 = secrets.token_hex(8)
                continue
            # success
            break

        # Clone the repo from the local clone, not the GitHub remote clone
        self.create_client_repos([path2], self.tabulation_local_upstream_absdir)
        # return the GUID
        return guid

    ################
    # main
    ################
    # pylint: disable=duplicate-code
    def main(self, the_election_config):
        """Main function - see -h for more info"""

        # Get the ElectionData directory
        election_data_dir = os.path.join(
            the_election_config.get("git_rootdir"),
            Globals.get("ROOT_ELECTION_DATA_SUBDIR"),
        )

        # Get the election data native GitHub remote clone name from _here_
        with Shellout.changed_cwd(election_data_dir):
            election_data_remote_url = Shellout.run(
                ["git", "config", "--get", "remote.origin.url"],
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
            self.parsed_args.location,
            SetupVtpDemoLib._tabulation_server_dirname,
            os.path.basename(election_data_remote_url),
        )

        # When creating a GUID workspace ...
        if self.parsed_args.guid_client_store:
            return self.create_a_guid_workspace_folder()

        # ... or the initial setup of the non-GUID client and server workspaces

        # First clone the bare upstream remote GitHub ElectionData repo
        with Shellout.changed_cwd(self.tabulation_local_upstream_absdir):
            Shellout.run(
                ["git", "clone", "--bare", election_data_remote_url],
                self.parsed_args.printonly,
                verbosity=self.parsed_args.verbosity,
            )

        # Create the first subdirectory level
        for subdir in [
            SetupVtpDemoLib._guid_client_dirname,
            SetupVtpDemoLib._tabulation_server_dirname,
            SetupVtpDemoLib._mock_client_dirname,
        ]:
            full_dir = os.path.join(self.parsed_args.location, subdir)
            if not os.path.isdir(full_dir):
                logging.debug("creating (%s)", full_dir)
                if not self.parsed_args.printonly:
                    os.mkdir(full_dir)

        # Create the mock scanner client subdirs
        clone_dirs = []
        for count in range(self.parsed_args.scanners):
            full_dir = os.path.join(
                self.parsed_args.location,
                SetupVtpDemoLib._mock_client_dirname,
                "scanner." + f"{count:02d}",
            )
            if not os.path.isdir(full_dir):
                logging.debug("creating (%s)", full_dir)
                if not self.parsed_args.printonly:
                    os.mkdir(full_dir)
            clone_dirs.append(full_dir)

        # Create the tabulation client subdir
        full_dir = os.path.join(
            self.parsed_args.location, SetupVtpDemoLib._mock_client_dirname, "server"
        )
        if not os.path.isdir(full_dir):
            logging.debug("creating (%s)", full_dir)
            if not self.parsed_args.printonly:
                os.mkdir(full_dir)
        clone_dirs.append(full_dir)

        # With the GitHub remote ElectionData repo cloned (bare) and
        # with all the necessary client workspaces created, create the
        # client workspaces.
        self.create_client_repos(clone_dirs, self.tabulation_local_upstream_absdir)

        # return something
        return 0


# End Of Class

# EOF
