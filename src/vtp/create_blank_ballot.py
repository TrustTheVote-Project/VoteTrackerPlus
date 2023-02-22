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

"""create_blank_ballot.py - command line level test script to automatically cast a ballot.

See './create_blank_ballot.py -h' for usage information.

See ../../docs/tech/executable-overview.md for the context in which this file was created.

"""

# Standard imports
import argparse

from vtp.ops.create_blank_ballot_operation import CreateBlankBallotOperation

# Local imports
from vtp.utils.address import Address


################
# arg parsing
################
# pylint: disable=duplicate-code
def parse_arguments():
    """Parse command line arguments"""

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
Will parse all the config and address_map yaml files in the current
VTP ElectionData git tree and create a blank ballot based on the
supplied address.
""",
    )

    Address.add_address_args(parser)
    parser.add_argument(
        "-l",
        "--language",
        default="en",
        help="will print the ballot in the specified language",
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


################
# main
################

# pylint: disable=duplicate-code
def main():
    """
    Called via a python local install entrypoint or this file.  Simply
    wraps the scripts constructor and calls run.
    """

    # do it
    cbbo = CreateBlankBallotOperation(parse_arguments())
    cbbo.run()


# If called directly via this file
if __name__ == "__main__":
    main()

# EOF
