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
Library backend to command line level script to allow an end voter to
vote - it simply wraps a call to cast_ballot.py and accept_ballot.py.

See 'vote.py -h' for usage information.
"""

# pylint: disable=wrong-import-position   # import statements not top of file
# Standard imports
import argparse
import logging
import sys

# Script modules
from vtp.ops.accept_ballot_lib import AcceptBallotLib
from vtp.ops.cast_ballot_lib import CastBallotLib

# Local libraries
from vtp.utils.address import Address
from vtp.utils.ballot import Ballot
from vtp.utils.common import Shellout


class VoteLib:
    """A class to wrap the vote.py script."""

    def __init__(self, argv):
        """Only to module-ize the scripts and keep things simple and idiomatic."""
        self.argv = argv
        self.parsed_args = None
        self.parse_arguments()

    def __str__(self):
        """Boilerplate"""
        return "argv=" + str(self.argv) + "\n" + "parsed_args=" + str(self.parsed_args)

    def parse_arguments(self):
        """Parse arguments from a command line"""

        parser = argparse.ArgumentParser(
            description="""Will interactively allow a voter to vote.  Internally
        it first calls cast_balloy.py followed by accept_ballot.py.  If a
        specific election address or a specific blank ballot is not
        specified, a random blank ballot is chosen.
        """
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

        #        import pdb; pdb.set_trace()
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

    ################
    # main
    ################
    def main(self, the_election_config):
        """Main function - see -h for more info"""

        # git pull the ElectionData repo so to get the latest set of
        # remote CVRs branches
        a_ballot = Ballot()
        with Shellout.changed_cwd(a_ballot.get_cvr_parent_dir(the_election_config)):
            Shellout.run(
                ["git", "pull"],
                printonly=self.parsed_args.printonly,
                verbosity=self.parsed_args.verbosity,
                check=True,
            )

        # If an address was used, use that
        cast_address_args = []
        accept_address_args = []
        if not self.parsed_args.blank_ballot:
            if self.parsed_args.state:
                cast_address_args += ["-s", self.parsed_args.state]
                accept_address_args += ["-s", self.parsed_args.state]
            if self.parsed_args.town:
                cast_address_args += ["-t", self.parsed_args.town]
                accept_address_args += ["-t", self.parsed_args.town]
            if self.parsed_args.substreet:
                cast_address_args += ["-b", self.parsed_args.substreet]
            if self.parsed_args.address:
                cast_address_args += ["-a", self.parsed_args.address]
        else:
            cast_address_args += ["--blank_ballot", self.parsed_args.blank_ballot]
            accept_address_args += ["--blank_ballot", self.parsed_args.blank_ballot]

        # Basically only do as little as necessary to call cast_ballot.py
        # followed by accept_ballot.py
        # Cast a ballot
        a_cast_ballot_lib = CastBallotLib(
            ["-v", str(self.parsed_args.verbosity)]
            + cast_address_args
            + (["-n"] if self.parsed_args.printonly else []),
        )
        a_cast_ballot_lib.main(the_election_config)
        # Accept the ballot
        a_accept_ballot_lib = AcceptBallotLib(
            ["-v", str(self.parsed_args.verbosity)]
            + accept_address_args
            + (["-n"] if self.parsed_args.printonly else [])
            + (["-m"] if self.parsed_args.merge_contests else []),
        )
        a_accept_ballot_lib.main(the_election_config)

    # End Of Class


# EOF
