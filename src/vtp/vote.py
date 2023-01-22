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
import sys

# Local import
from vtp.utils.address import Address
from vtp.utils.ballot import Ballot
from vtp.utils.common import Shellout
from vtp.utils.election_config import ElectionConfig

# Functions

################
# arg parsing
################
# pylint: disable=duplicate-code
def parse_arguments():
    """Parse arguments from a command line"""

    parser = argparse.ArgumentParser(
        description="""vote.py will interactively allow a voter to vote.  Internally
    it first calls cast_balloy.py followed by accept_ballot.py.  If a
    specific election address or a specific blank ballot is not
    specified, a random blank ballot is chosen.
    """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    Address.add_address_args(parser)
    parser.add_argument(
        "-m",
        "--merge_contests",
        action="store_true",
        help="Will immediately merge the ballot contests (to master)",
    )
    parser.add_argument(
        "--blank_ballot",
        help="overrides an address - specifies the specific blank ballot",
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

    parsed_args = parser.parse_args()
    verbose = {
        0: logging.CRITICAL,
        1: logging.ERROR,
        2: logging.WARNING,
        3: logging.INFO,
        4: logging.DEBUG,
    }
    logging.basicConfig(
        format="%(message)s", level=verbose[parsed_args.verbosity], stream=sys.stdout
    )

    # Validate required args
    return parsed_args


################
# main
################

ARGS = None

# pylint: disable=duplicate-code
def main():
    """Main function - see -h for more info"""

    # pylint: disable=global-statement
    global ARGS
    ARGS = parse_arguments()

    # Create an VTP election config object
    the_election_config = ElectionConfig()
    the_election_config.parse_configs()
    accept_ballot = Shellout.get_script_name("accept_ballot.py", the_election_config)
    cast_ballot = Shellout.get_script_name("cast_ballot.py", the_election_config)

    # git pull the ElectionData repo so to get the latest set of
    # remote CVRs branches
    a_ballot = Ballot()
    with Shellout.changed_cwd(a_ballot.get_cvr_parent_dir(the_election_config)):
        Shellout.run(
            ["git", "pull"],
            printonly=ARGS.printonly,
            verbosity=ARGS.verbosity,
            check=True,
        )

    # If an address was used, use that
    cast_address_args = []
    accept_address_args = []
    if not ARGS.blank_ballot:
        if ARGS.state:
            cast_address_args += ["-s", ARGS.state]
            accept_address_args += ["-s", ARGS.state]
        if ARGS.town:
            cast_address_args += ["-t", ARGS.town]
            accept_address_args += ["-t", ARGS.town]
        if ARGS.substreet:
            cast_address_args += ["-b", ARGS.substreet]
        if ARGS.address:
            cast_address_args += ["-a", ARGS.address]
    else:
        cast_address_args += ["--blank_ballot", ARGS.blank_ballot]
        accept_address_args += ["--blank_ballot", ARGS.blank_ballot]

    # Basically only do as little as necessary to call cast_ballot.py
    # followed by accept_ballot.py
    # Cast a ballot
    Shellout.run(
        [cast_ballot, "-v", ARGS.verbosity]
        + cast_address_args
        + (["-n"] if ARGS.printonly else []),
        check=True,
        no_touch_stds=True,
        timeout=None,
    )
    # Accept the ballot
    Shellout.run(
        [accept_ballot, "-v", ARGS.verbosity]
        + accept_address_args
        + (["-n"] if ARGS.printonly else [])
        + (["-m"] if ARGS.merge_contests else []),
        check=True,
        no_touch_stds=True,
        timeout=None,
    )


if __name__ == "__main__":
    main()

# EOF
