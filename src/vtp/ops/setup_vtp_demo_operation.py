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
Library operation for command line level script set up a VTP demo
See 'setup_vtp_demo -h' for usage information.
"""

# Standard imports
import argparse
import logging
import os
import secrets

# Local import
from vtp.core.common import Common, Globals, Shellout
from vtp.core.election_config import ElectionConfig


class SetupVtpDemoOperation:
    """
    A class to implememt the setup-vtp-demo operation.  See the
    setup-vtp-demo help output or read the parse_argument argparse
    description (immediately below this) in the source file.
    """

    @staticmethod
    def parse_arguments(argv):
        """Parse arguments from a command line or from the constructor"""

        safe_args = Common.cast_thing_to_list(argv)
        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description="""
Will leverage this current git repository (VoteTrackerPlus) and the
associated ElectionData repo(s) to nominally create in
/opt/VoteTrackerPlus (the default) a demo election with 4 mock ballot
scanner apps and one tabulation server app. The initial demo idea is
to have three scanners scanning random ballots while one scanner is
used interactively.

All five apps run in separate git workspaces that are clones of the
same ElectionData repo(s). The (4) mock scanner app clones are located
in one folder, the one tabulation server is located in another, and
the FastAPI clients are located in a third. The FastAPI clients are
separated by a GUID based subdirectory similar to the native Git
storage idiom.

If the --guid_client_store option is set, instead of setting up the
demo this script will create a new GUID based FASTapi clone and return
the GUID.
""",
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
        parsed_args = parser.parse_args(safe_args)
        # Validate required args
        if parsed_args.scanners < 1 or parsed_args.scanners > 16:
            raise ValueError(
                "The demo needs at least one TVP scanner app "
                "and arbitrarily limits a demo to 16."
            )
        # Check the root of the demo
        if not os.path.isdir(parsed_args.location):
            raise FileNotFoundError(
                f"The root demo folder, {parsed_args.location}, does not exit.  "
                "It needs to pre-exist - please manually create it."
            )
        test_dir = os.path.join(
            parsed_args.location, Globals.get("TABULATION_SERVER_DIRNAME")
        )
        if parsed_args.guid_client_store and not os.path.isdir(test_dir):
            raise FileNotFoundError(
                f"The tabulation server workspace ({test_dir}) does not exit.  "
                "It needs to pre-exist and is created when setup-vtp-demo is executed "
                "in setup mode (without the -g switch)."
            )
        return parsed_args

    def __init__(self, unparsed_args):
        """Only to module-ize the scripts and keep things simple and idiomatic."""
        self.parsed_args = SetupVtpDemoOperation.parse_arguments(unparsed_args)
        # The absolute path to the local bare clone of the upstream
        # GitHub ElectionData remote repo
        self.tabulation_local_upstream_absdir = ""

    def __repr__(self):
        """Boilerplate"""
        return (
            "parsed_args="
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
            if not self.parsed_args.printonly:
                with Shellout.changed_cwd(clone_dir):
                    Shellout.run(
                        ["git", "clone", upstream_url],
                        self.parsed_args.printonly,
                        verbosity=self.parsed_args.verbosity,
                        check=True,
                    )
            else:
                logging.debug("Entering dir (%s):", clone_dir)
                logging.info("Running git clone %s", upstream_url)
                logging.debug("Leaving dir (%s):", clone_dir)

    def create_a_guid_workspace_folder(self):
        """creates guid workspace"""
        guid = secrets.token_hex(20)
        folder1 = guid[:2]
        folder2 = guid[2:]
        # Note - mkdir raises an error if the directory exists. So
        # just try creating them.
        path1 = os.path.join(
            self.parsed_args.location,
            Globals.get("GUID_CLIENT_DIRNAME"),
            folder1,
        )
        path2 = os.path.join(path1, folder2)
        if not self.parsed_args.printonly:
            try:
                logging.debug("creating (%s) if it does not exist", path1)
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
                    logging.debug("creating (%s)", path2)
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
            logging.debug("creating (%s) if it does not exist", path1)
            logging.debug("creating (%s) if it does not exist", path2)

        # Clone the repo from the local clone, not the GitHub remote clone
        self.create_client_repos([path2], self.tabulation_local_upstream_absdir)
        # return the GUID
        logging.debug("returning %s", guid)
        return guid

    ################
    # main
    ################
    # pylint: disable=duplicate-code
    def run(self):
        """Main function - see -h for more info"""

        # Configure logging
        Common.configure_logging(self.parsed_args.verbosity)

        # Create a VTP ElectionData object if one does not already exist
        the_election_config = ElectionConfig.configure_election()

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
            Globals.get("TABULATION_SERVER_DIRNAME"),
            os.path.basename(election_data_remote_url),
        )
        # Need both the above and the dirname of the above
        bare_clone_path = os.path.dirname(self.tabulation_local_upstream_absdir)
        # When creating a GUID workspace ...
        if self.parsed_args.guid_client_store:
            return self.create_a_guid_workspace_folder()

        # ... or the initial setup of the non-GUID client and server workspaces

        # Only run if the directory is empty
        if len(os.listdir(self.parsed_args.location)) != 0:
            raise RuntimeError(
                f"the directory ({self.parsed_args.location}) is not empty - "
                "setup-vtp-demo can only be run on an empty directory"
            )

        # First create the necessary subdirectories
        for subdir in [
            Globals.get("GUID_CLIENT_DIRNAME"),
            Globals.get("TABULATION_SERVER_DIRNAME"),
            Globals.get("MOCK_CLIENT_DIRNAME"),
        ]:
            full_dir = os.path.join(self.parsed_args.location, subdir)
            if not os.path.isdir(full_dir):
                logging.debug("creating (%s)", full_dir)
                if not self.parsed_args.printonly:
                    os.mkdir(full_dir)

        # Second clone the bare upstream remote GitHub ElectionData repo
        if not self.parsed_args.printonly:
            with Shellout.changed_cwd(bare_clone_path):
                Shellout.run(
                    ["git", "clone", "--bare", election_data_remote_url],
                    self.parsed_args.printonly,
                    verbosity=self.parsed_args.verbosity,
                    check=True,
                )
        else:
            logging.debug("Entering dir (%s):", bare_clone_path)
            logging.info("Running git clone --bare %s", election_data_remote_url)
            logging.debug("Leaving dir (%s):", bare_clone_path)

        # Third create the mock scanner client subdirs
        clone_dirs = []
        for count in range(self.parsed_args.scanners):
            full_dir = os.path.join(
                self.parsed_args.location,
                Globals.get("MOCK_CLIENT_DIRNAME"),
                "scanner." + f"{count:02d}",
            )
            if not os.path.isdir(full_dir):
                logging.debug("creating (%s)", full_dir)
                if not self.parsed_args.printonly:
                    os.mkdir(full_dir)
            clone_dirs.append(full_dir)

        # Fourth create the tabulation client subdir
        full_dir = os.path.join(
            self.parsed_args.location,
            Globals.get("MOCK_CLIENT_DIRNAME"),
            "server",
        )
        if not os.path.isdir(full_dir):
            logging.debug("creating (%s)", full_dir)
            if not self.parsed_args.printonly:
                os.mkdir(full_dir)
        clone_dirs.append(full_dir)

        # Fifth, with the GitHub remote ElectionData repo cloned
        # (bare) and with all the necessary client workspaces created,
        # create the client workspaces.
        self.create_client_repos(clone_dirs, self.tabulation_local_upstream_absdir)

        # return something
        return None


# End Of Class

# EOF
