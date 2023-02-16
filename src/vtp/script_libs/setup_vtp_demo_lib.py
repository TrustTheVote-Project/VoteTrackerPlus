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

    _client_dir_name = "client-store"
    _server_dir_name = "tabulation-server"
    _mock_client_dir_name = "mock-clients"

    def __init__(self, argv):
        """Only to module-ize the scripts and keep things simple and idiomatic."""
        self.argv = argv
        self.parsed_args = None
        self.tabulation_server_dir = ""
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
            + self.tabulation_server_dir
        )

    def create_client_repos(self, clone_dirs, remote_path):
        """create demo clients workspaces"""
        # Now locally clone those as needed.  With the python/poetry
        # local install idiom, the demo location no longer needs the
        # submodules to be cloned.
        for clone_dir in clone_dirs:
            with Shellout.changed_cwd(clone_dir):
                Shellout.run(
                    ["git", "clone", remote_path],
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
        self.tabulation_server_dir = self.parsed_args.location
        client_dir = os.path.join(
            self.tabulation_server_dir, SetupVtpDemoLib._client_dir_name
        )
        if self.parsed_args.guid_client_store and not os.path.isdir(client_dir):
            raise FileNotFoundError(
                f"The git client data store folder ({client_dir}) does not exit.  "
                "It needs to pre-exist and is created when setup-vtp-demo is executed "
                "in setup mode (without the -g switch)."
            )

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

        if self.parsed_args.guid_client_store:
            # generate a GUID for the directory name
            guid = secrets.token_hex(10)
            folder1 = guid[:2]
            folder2 = guid[2:]
            # Need to determine without race conditions if the
            # directory does not exist already.

            # create the subdirs
            for subdir in [folder1, folder2]:
                full_dir = os.path.join(self.parsed_args.location, subdir)
                if not os.path.isdir(full_dir):
                    logging.debug("creating (%s)", full_dir)
                    if not self.parsed_args.printonly:
                        os.mkdir(full_dir)
            # Need to determine on the fly the absolute path to the
            # tabulation-server dir.  We have the parent dir but not
            # the actual git clone folder name.  Get that
            with Shellout.changed_cwd(election_data_dir):
                git_repo_name = os.path.basename(
                    Shellout.run(
                        ["git", "config", "--get", "remote.origin.url"],
                        check=True,
                        capture_output=True,
                        text=True,
                    ).stdout.strip()
                )
            # Clone the repo
            self.create_client_repos(
                [os.path.join(folder1, folder2)],
                os.path.join(self.tabulation_server_dir, git_repo_name),
            )
            # return the GUID
            return guid

        # Initial setup of the demo

        # Create the first subdirectory level
        for subdir in [
            SetupVtpDemoLib._client_dir_name,
            SetupVtpDemoLib._server_dir_name,
            SetupVtpDemoLib._mock_client_dir_name,
        ]:
            full_dir = os.path.join(self.parsed_args.location, subdir)
            if not os.path.isdir(full_dir):
                logging.debug("creating (%s)", full_dir)
                if not self.parsed_args.printonly:
                    os.mkdir(full_dir)

        # Create the mock scanner subdirs
        clone_dirs = []
        for count in range(self.parsed_args.scanners):
            full_dir = os.path.join(
                self.parsed_args.location,
                SetupVtpDemoLib._client_dir_name,
                "scanner." + f"{count:02d}",
            )
            clone_dirs.append(full_dir)
            if not os.path.isdir(full_dir):
                logging.debug("creating (%s)", full_dir)
                if not self.parsed_args.printonly:
                    os.mkdir(full_dir)

        # Create the tabulation server subdir
        full_dir = os.path.join(
            self.parsed_args.location, SetupVtpDemoLib._client_dir_name, "server"
        )
        clone_dirs.append(full_dir)
        if not os.path.isdir(full_dir):
            logging.debug("creating (%s)", full_dir)
            if not self.parsed_args.printonly:
                os.mkdir(full_dir)

        # Clone the election data repo from GitHub as a bare clone
        tabulation_abs_dir = os.path.join(
            self.parsed_args.location, SetupVtpDemoLib._server_dir_name
        )
        # Get the election data remote clone name
        with Shellout.changed_cwd(election_data_dir):
            election_data_remote_name = Shellout.run(
                ["git", "config", "--get", "remote.origin.url"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
        # Note -since the repo is a bare it has the same ".git" suffix
        # as the remote.
        with Shellout.changed_cwd(tabulation_abs_dir):
            Shellout.run(
                ["git", "clone", "--bare", election_data_remote_name],
                self.parsed_args.printonly,
                verbosity=self.parsed_args.verbosity,
            )

        # With the local tabulation bare clone cloned, create the
        # actual mock client and tabulation server clones.
        self.create_client_repos(clone_dirs, tabulation_abs_dir)

        # return something
        return 0


# End Of Class

# EOF
