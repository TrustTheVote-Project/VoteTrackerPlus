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

"""Base class of operations."""

from vtp.core.common import Common


# pylint: disable=too-few-public-methods
class Operation:
    """
    Generic operation base class constructor - covers
    election_data_dir, guid, verbosity, and printonly.  Also will
    configure (global) logging and validate the existance of
    election_data_dir.
    """

    def __init__(
        self,
        election_data_dir: str = "",
        verbosity: int = 3,
        printonly: bool = False,
        stdout_printing: bool = True,
    ):
        self.election_data_dir = election_data_dir
        self.printonly = printonly
        self.verbosity = verbosity
        # Configure logging
        Common.configure_logging(verbosity)
        # Validate the election_data_dir arg here and now
        Common.verify_election_data_dir(self.election_data_dir)
        # Configure printing
        self.stdout_printing = stdout_printing
        self.stdout_output = []

    def imprimir(self, a_line: str, incoming_printlevel: int = 3):
        """Either prints a line of text to STDOUT or appends it to a list"""
        if incoming_printlevel <= self.verbosity:
            if self.stdout_printing:
                print(a_line)
            else:
                self.stdout_output.append(a_line)
        return self.verbosity

    def get_imprimir(self) -> list:
        """Return the stored output string"""
        return self.stdout_output
