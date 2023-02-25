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

"""Command line script to generate all possible blank ballots.

Run with '--help' for usage information.
"""

# Standard imports
import argparse
import sys

# Local import
from vtp.core.common import Common
from vtp.ops.generate_all_blank_ballots_operation import (
    GenerateAllBlankBallotsOperation,
)

from ._arguments import Arguments


def parse_arguments(argv):
    safe_args = Common.cast_thing_to_list(argv)
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
Will crawl the ElectionData tree and determine all possible blank
ballots and generate them.  They will be placed in the town's
blank-ballots subdir.
""",
    )

    Arguments.add_verbosity(parser)
    Arguments.add_print_only(parser)

    return parser.parse_args(safe_args)


def main():
    """
    Called via a python local install entrypoint or by running this
    file.  Simply wraps the scripts constructor and calls the run
    method.  See the script's help output or read the
    vtp.ops.generate_all_blank_ballots_operation.py (argparse)
    description in the source file.
    """

    args = parse_arguments(sys.argv[1:])
    op = GenerateAllBlankBallotsOperation(args)
    op.run()


# If called directly via this file
if __name__ == "__main__":
    main()
