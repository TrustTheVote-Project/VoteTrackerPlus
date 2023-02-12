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
vote.py - command line level script to allow an end voter to vote - it
simply wraps a call to cast_ballot.py and accept_ballot.py.

See './vote.py -h' for usage information.
"""

# pylint: disable=wrong-import-position   # import statements not top of file
import sys

from vtp.script_libs.vote_lib import VoteLib


def main():
    """If called via a python local install entrypoint"""
    main_votelib = VoteLib(sys.argv)
    main_votelib.main()


# If called as a script entrypoint
if __name__ == "__main__":
    _main_votelib = VoteLib(sys.argv)
    _main_votelib.main()

# EOF
