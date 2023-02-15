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

"""Command line level script to automatically cast a ballot.

See 'show_contest.py -h' for usage information.
"""

# Standard imports
# pylint: disable=wrong-import-position   # import statements not top of file
import sys

from vtp.script_libs.show_contests_lib import ShowContestsLib
from vtp.utils.election_config import ElectionConfig


# pylint: disable=duplicate-code
def main():
    """If called via a python local install entrypoint"""

    # Parse args first (ZZZ note logging interface)
    _main = ShowContestsLib(sys.argv[1:])

    # Create an VTP election config object
    the_election_config = ElectionConfig()
    the_election_config.parse_configs()

    # do it
    _main.main(the_election_config)


# If called as a script entrypoint
if __name__ == "__main__":
    main()
