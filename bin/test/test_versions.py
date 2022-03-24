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

"""Will test versions of stuff.  A TBD.  Much ZZZ here.

"""

# pylint: disable=wrong-import-position
import sys

# save the user from themselves
def test_python_version():
    """Test python version - needs to run in older versions ..."""
    if not sys.version_info.major == 3 and sys.version_info.minor >= 9:
        print("Python 3.9 or higher is required.")
        print("You are using Python " + str(sys.version_info.major) +
                  "." + str(sys.version_info.minor))
        sys.exit(1)
