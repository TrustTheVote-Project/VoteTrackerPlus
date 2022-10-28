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
import sys

# Local import
from vtp.utils.common import Globals, Shellout
from vtp.utils.election_config import ElectionConfig

# Functions

def create_client_repos(clone_dirs, remote_path):
    """create demo clients workspaces"""
    # Now locally clone those as needed.  With the use of submodules
    # there is no longer an ElectionData symlink to manage.  Record
    # the repos to add them to the superproject later.
    cloned_repos = [] # a list of tuple pairs
    for clone_dir in clone_dirs:
        with Shellout.changed_cwd(clone_dir):
            Shellout.run(
                ['git', 'clone', '--recurse-submodules', remote_path],
                args.printonly, verbosity=args.verbosity)
            # Note - since the repo is not a bare, the ".git" suffix
            # needs to be stripped
            repo_dir_name = os.path.basename(remote_path).removesuffix('.git')
            cloned_repos.append((
                remote_path,
                os.path.join(
                    os.path.basename(os.path.dirname(clone_dir)),
                    os.path.basename(clone_dir),
                    repo_dir_name)))
    return cloned_repos


################
# arg parsing
################
# pylint: disable=duplicate-code
def parse_arguments():
    """Parse arguments from a command line"""

    parser = argparse.ArgumentParser(description=
    """setup_vtp_demo.py will leverage this current git repository
    (VoteTrackerPlus) and the associated ElectionData repos
    nominally create in /opt/VoteTrackerPlus (the default) a demo
    election mock up of 4 ballot scanner apps and one voting center
    server app.  The initial demo idea is to have three scanners
    scanning random ballots while one scanner is used interactively.
    However, any number of scanner apps instances can be started.

    All five apps run in a pair of separate git repos that are clones
    of the same ElectionData repos as this one and are contained in a
    subfolder called 'clients'.  All the client apps' git repos have
    had the remote origin configured to point to two local-remote bare
    clones of the GitHub remotes located in the subfolder
    'local-remote-server'.

    Normally no demo git commits are pushed back to GiHub, but to do
    so one would normally use the bare repos and not the client repos.

    To facilitate the management of all the git repos (8 client and 2
    local-remote), a git superproject repo is initiated at the
    /opt/VoteTrackerPlus directory with all the app and local-remote
    repos configured as git submodules.  The superprject can be
    ignored or leveraged at will.
    """,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument(
        "-s", "--scanners", type=int, default=4,
        help="specify a number of scanner app instances (def=4)")
    parser.add_argument(
        "-l", "--location", default="/opt/VoteTrackerPlus/demo.01",
        help="specify the location of VTP demo (def=/opt/VoteTrackerPlus/demo.01)")
    parser.add_argument(
        "-v", "--verbosity", type=int, default=3,
        help="0 critical, 1 error, 2 warning, 3 info, 4 debug (def=3)")
    parser.add_argument(
        "-n", "--printonly", action="store_true",
        help="will printonly and not write to disk (def=True)")

    parsed_args = parser.parse_args()
    verbose = {0: logging.CRITICAL, 1: logging.ERROR, 2: logging.WARNING,
                   3: logging.INFO, 4: logging.DEBUG}
    logging.basicConfig(format="%(message)s", level=verbose[parsed_args.verbosity],
                            stream=sys.stdout)

    # Validate required args
    if parsed_args.scanners < 1 or parsed_args.scanners > 16:
        raise ValueError("The demo needs at least one TVP scanner app "
                         "and arbitrarily limits a demo to 16.")
    # Check the root of the demo
    if not os.path.isdir(parsed_args.location):
        raise FileNotFoundError(
            f"The root demo folder, {parsed_args.location}, does not exit.  "
            "It needs to pre-exist - please manually create it.")
    return parsed_args


################
# main
################
# pylint: disable=duplicate-code
def main():
    """Main function - see -h for more info"""

    # Check the ElectionData before creating everything
    the_election_config = ElectionConfig()
    the_election_config.parse_configs()
    election_data_dir = os.path.join(
        the_election_config.get('git_rootdir'), Globals.get('ROOT_ELECTION_DATA_SUBDIR'))

    # The first subdirectory level
    for subdir in ['clients', 'local-remote-server']:
        full_dir = os.path.join(args.location, subdir)
        if not os.path.isdir(full_dir):
            logging.debug("creating (%s)", full_dir)
            if not args.printonly:
                os.mkdir(full_dir)
    # The client side scanner app instances
    clone_dirs = []
    for count in range(args.scanners):
        full_dir = os.path.join(args.location, 'clients', 'scanner.' + f"{count:02d}")
        clone_dirs.append(full_dir)
        if not os.path.isdir(full_dir):
            logging.debug("creating (%s)", full_dir)
            if not args.printonly:
                os.mkdir(full_dir)
    # The client side app server instance
    full_dir = os.path.join(args.location, 'clients', 'server')
    clone_dirs.append(full_dir)
    if not os.path.isdir(full_dir):
        logging.debug("creating (%s)", full_dir)
        if not args.printonly:
            os.mkdir(full_dir)

    # Clone the two local-remotes
    full_dir = os.path.join(args.location, 'local-remote-server')
    # Get the two remotes
    with Shellout.changed_cwd(election_data_dir):
        remote_1 = Shellout.run(
            ['git', 'config', '--get', 'remote.origin.url'],
            check=True, capture_output=True, text=True).stdout.strip()
    remote_2 = Shellout.run(
        ['git', 'config', '--get', 'remote.origin.url'],
        check=True, capture_output=True, text=True).stdout.strip()
    # Bare clone them
    with Shellout.changed_cwd(full_dir):
        Shellout.run(
            ['git', 'clone', '--bare', remote_1],
            args.printonly, verbosity=args.verbosity)
        # Note - since the repo is a bare it has the same ".git"
        # suffix as the remote
        remote_1_path = os.path.join(full_dir, os.path.basename(remote_1))
        Shellout.run(
            ['git', 'clone', '--bare', remote_2],
            args.printonly, verbosity=args.verbosity)

    # Create the client repos via the outer/root repo leveraging submodules
    cloned_repos = create_client_repos(clone_dirs, remote_1_path)

    # Note - in theory during a mock election run, it probably is not
    # the normal case that the end user wants to actively develop code
    # there, so no need to tweak the .git/config files with the git
    # submodule UX customizations in the client (local) clones.
    # However, w.r.t. the super project, it may make sense to add
    # it there as an example.

    # Now create a super git project to rule them all
    with Shellout.changed_cwd(args.location):
        # init it
        Shellout.run(
            ['git', 'init'],
            args.printonly, verbosity=args.verbosity)
        # add in all the created submodules
        for clone in cloned_repos:
            Shellout.run(
                ['git', 'submodule', 'add', clone[0], clone[1]],
                args.printonly, verbosity=args.verbosity)
        # Ignore the local remote repos directory
        logging.info('Adding a .gitignore')
        if not args.printonly:
            with open('.gitignore', 'w', encoding="utf8") as outfile:
                outfile.write('# Ignore the local remote repos\n')
                outfile.write('local-remote-server\n')
        Shellout.run(
            ['git', 'add', '.gitignore'],
            args.printonly, verbosity=args.verbosity)

if __name__ == '__main__':
    args = parse_arguments()
    main()

# EOF
