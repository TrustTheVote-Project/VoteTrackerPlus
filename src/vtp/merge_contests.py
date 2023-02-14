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
merge_contests.py - command line level script to merge CVR contest
branches into the master branch

See './merge_contests.py -h' for usage information.

See ../../docs/tech/merge_contests.md for the context in which this
file was created.
"""

# Standard imports
# pylint: disable=wrong-import-position   # import statements not top of file
import sys

from vtp.script_libs.merge_contests_lib import MergeContestsLib


def main():
    """If called via a python local install entrypoint"""
    _main = MergeContestsLib(sys.argv[1:])
    _main.main()


# If called as a script entrypoint
if __name__ == "__main__":
    main()
