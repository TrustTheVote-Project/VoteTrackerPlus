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

"""generate-all-blank-ballots - generate all possible blank ballots

See 'generate-all-blank-ballots -h' for usage information.
"""

# Standard imports
import argparse
import sys

# Project imports
from vtp.ops.generate_all_blank_ballots_operation import (
    GenerateAllBlankBallotsOperation,
)

# Local imports
from ._arguments import Arguments


def parse_arguments(argv):
    """Parse arguments from a command line or from the constructor"""

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
Will crawl the ElectionData tree and determine all possible blank
ballots and generate them.  They will be placed in the town's
blank-ballots subdir.
""",
    )

    Arguments.add_election_data_dir(parser)
    Arguments.add_verbosity(parser)
    Arguments.add_printonly(parser)
    return parser.parse_args(argv)


# pylint: disable=duplicate-code
def main():
    """Entry point for 'generate-all-blank-ballots'."""

    # Parse args
    parsed_args = parse_arguments(sys.argv)

    # do it
    gabbo = GenerateAllBlankBallotsOperation(
        parsed_args.election_data, parsed_args.verbosity, parsed_args.printonly
    )
    gabbo.run()


# If called directly via this file
if __name__ == "__main__":
    main()

# EOF
