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

"""accept_ballot.py - command line level script to accept a ballot.

See './accept_ballot.py -h' for usage information.

"""

import argparse
import sys

from vtp.ops.accept_ballot_operation import AcceptBallotOperation
from vtp.utils.address import Address


################
# arg parsing
################
# pylint: disable=duplicate-code
def parse_arguments():
    """Parse arguments from a command line"""

    parser = argparse.ArgumentParser(
        description="""Will run the git based workflow on a VTP
                    scanner node to accept the json rendering of the
                    cast vote record of a voter's ballot.  The json
                    file is read, the contests are extraced and
                    submitted to separate git branches, one per
                    contest, and pushed back to the Voter Center's VTP
                    remote.

                    In addition a voter's ballot receipt and offset
                    are optionally printed.

                    Either the location of the ballot_file or the
                    associated address is required.
                    """
    )

    Address.add_address_args(parser, True)
    parser.add_argument(
        "-m",
        "--merge_contests",
        action="store_true",
        help="Will immediately merge the ballot contests (to master)",
    )
    parser.add_argument(
        "--cast_ballot",
        help="overrides an address - specifies a specific cast ballot",
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

    return parser.parse_args()



# pylint: disable=duplicate-code
def main():
    """
    Called via a python local install entrypoint or this file.  Simply
    wraps the scripts constructor, creates and ElectionConfig instance
    (which parses VTP's election data file which is implemented as a
    directory tree), and calls its main function.
    """

    # do it
    abo = AcceptBallotOperation(parse_arguments())
    abo.run()


# If called directly via this file
if __name__ == "__main__":
    main()
