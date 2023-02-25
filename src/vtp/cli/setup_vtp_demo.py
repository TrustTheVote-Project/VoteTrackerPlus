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
Command line level script script set up a VTP demo.  Can also set up
individual GUID based ballot-stores and return the GUID

See 'setup_vtp_demo -h' for usage information.
"""

# Global imports
import sys

# Local imports
from vtp.ops.setup_vtp_demo_operation import SetupVtpDemoOperation


def main():
    """
    Called via a python local install entrypoint or by running this
    file.  Simply wraps the scripts constructor and calls the run
    method.  See the script's help output or read the
    vtp.ops.setup_vtp_demo_operation.py (argparse) description in the
    source file.
    """

    # do it
    svdo = SetupVtpDemoOperation(sys.argv[1:])
    guid = svdo.run()
    if isinstance(guid, str):
        print(guid)


# If called directly via this file
if __name__ == "__main__":
    main()
