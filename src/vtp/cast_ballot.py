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

See './cast_ballot.py -h' for usage information.

See ../../docs/tech/executable-overview.md for the context in which this file was created.

"""

# pylint: disable=wrong-import-position
import sys

from vtp.script_libs.cast_ballot_lib import CastBallotLib


def main():
    """If called via a python local install entrypoint"""
    main_castballotlib = CastBallotLib(sys.argv[1:])
    main_castballotlib.main()


# If called as a script entrypoint
if __name__ == "__main__":
    main()
