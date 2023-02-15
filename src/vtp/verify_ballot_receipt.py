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
Command line level script to verify a voters ballot receipt.  Supports several interesting options.

See 'verify_ballot_receipt.py -h' for usage information.
"""

# Standard imports
# pylint: disable=wrong-import-position   # import statements not top of file
import sys

from vtp.script_libs.verify_ballot_receipt_lib import VerifyBallotReceiptLib


def main():
    """If called via a python local install entrypoint"""
    _main = VerifyBallotReceiptLib(sys.argv[1:])
    _main.main()


# If called as a script entrypoint
if __name__ == "__main__":
    main()
