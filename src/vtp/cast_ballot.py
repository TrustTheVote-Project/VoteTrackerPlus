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

"""cast_ballot.py - command line level test script to automatically cast a ballot.

See 'cast_ballot.py -h' for usage information.
"""

import argparse

from vtp.ops.cast_ballot_operation import CastBallotOperation
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
Given either an address or a specific blank ballot, will either read a
blank ballot and allow a user to manually select choices or when in
demo mode, cast_ballot.py will randominly select choices.
""",
    )

    Address.add_address_args(parser)
    # ZZZ - cloaked contests are enabled at cast_ballot time
    #    parser.add_argument('-k', "--cloak", action="store_true",
    #                            help="if possible provide a cloaked ballot offset")
    parser.add_argument(
        "--demo_mode",
        action="store_true",
        help="set demo mode to automatically cast random ballots",
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
    return parser.parse_args()


# pylint: disable=duplicate-code
def main():
    """
    Called via a python local install entrypoint or this file.  Simply
    wraps the scripts constructor and calls run.
    """

    # do it
    cbo = CastBallotOperation(parse_arguments())
    cbo.run()


# If called directly via this file
if __name__ == "__main__":
    main()
