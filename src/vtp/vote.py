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
vote.py - command line level script to allow an end voter to vote - it
simply wraps a call to cast_ballot.py and accept_ballot.py.

See './vote.py -h' for usage information.
"""

# pylint: disable=wrong-import-position   # import statements not top of file
# Standard imports
import argparse
import logging
import os
import sys

# Local import
from .address import Address
from .ballot import Ballot
from .common import Shellout
from .election_config import ElectionConfig


# Functions

################
# arg parsing
################
# pylint: disable=duplicate-code
def parse_arguments():
    """Parse arguments from a command line"""

    parser = argparse.ArgumentParser(description=
    """vote.py will interactively allow a voter to vote.  Internally
    it first calls cast_balloy.py followed by accept_ballot.py.  If a
    specific election address or a specific blank ballot is not
    specified, a random blank ballot is chosen.
    """,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    Address.add_address_args(parser)
    parser.add_argument("-m", "--merge_contests", action="store_true",
                            help="Will immediately merge the ballot contests (to master)")
    parser.add_argument("--blank_ballot",
                            help="overrides an address - specifies the specific blank ballot")
    parser.add_argument("-v", "--verbosity", type=int, default=3,
                            help="0 critical, 1 error, 2 warning, 3 info, 4 debug (def=3)")
    parser.add_argument("-n", "--printonly", action="store_true",
                            help="will printonly and not write to disk (def=True)")

    parsed_args = parser.parse_args()
    verbose = {0: logging.CRITICAL, 1: logging.ERROR, 2: logging.WARNING,
                   3: logging.INFO, 4: logging.DEBUG}
    logging.basicConfig(format="%(message)s", level=verbose[parsed_args.verbosity],
                            stream=sys.stdout)

    # Validate required args
    return parsed_args

################
# main
################
# pylint: disable=duplicate-code
def main():
    """Main function - see -h for more info"""

    # Create an VTP election config object
    the_election_config = ElectionConfig()
    the_election_config.parse_configs()

    # git pull the ElectionData repo so to get the latest set of
    # remote CVRs branches
    a_ballot = Ballot()
    with Shellout.changed_cwd(a_ballot.get_cvr_parent_dir(the_election_config)):
        Shellout.run(
            ["git", "pull"],
            printonly=args.printonly, verbosity=args.verbosity,
            check=True)

    # If an address was used, use that
    cast_address_args = []
    accept_address_args = []
    if not args.blank_ballot:
        if args.state:
            cast_address_args += ['-s', args.state]
            accept_address_args += ['-s', args.state]
        if args.town:
            cast_address_args += ['-t', args.town]
            accept_address_args += ['-t', args.town]
        if args.substreet:
            cast_address_args += ['-b', args.substreet]
        if args.address:
            cast_address_args += ['-a', args.address]
    else:
        cast_address_args += ['--blank_ballot', args.blank_ballot]
        accept_address_args += ['--blank_ballot', args.blank_ballot]

    # Basically only do as little as necessary to call cast_ballot.py
    # followed by accept_ballot.py
    bin_dir = os.path.join(the_election_config.get('git_rootdir'), 'bin')
    # Cast a ballot
    Shellout.run(
        [os.path.join(bin_dir, 'cast_ballot.py'), '-v', args.verbosity]
        + cast_address_args + (['-n'] if args.printonly else []),
        check=True, no_touch_stds=True, timeout=None)
    # Accept the ballot
    Shellout.run(
        [os.path.join(bin_dir, 'accept_ballot.py'), '-v', args.verbosity]
        + accept_address_args + (['-n'] if args.printonly else [])
        + (['-m'] if args.merge_contests else []),
        check=True, no_touch_stds=True, timeout=None)

if __name__ == '__main__':
    args = parse_arguments()
    main()

# EOF
