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

"""generate_all_blank_ballots.py - generate all possible blank ballots

See 'generate_all_blank_ballots.py -h' for usage information.
"""

# Standard imports
import argparse

# Local import
from vtp.ops.generate_all_blank_ballots_operation import (
    GenerateAllBlankBallotsOperation,
)


################
# arg parsing
################
# pylint: disable=duplicate-code
def parse_arguments():
    """Parse arguments from a command line"""

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
Will crawl the ElectionData tree and determine all possible blank
ballots and generate them.  They will be placed in the town's
blank-ballots subdir.
""",
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
    gabbo = GenerateAllBlankBallotsOperation(parse_arguments())
    gabbo.run()


# If called directly via this file
if __name__ == "__main__":
    main()

# EOF
