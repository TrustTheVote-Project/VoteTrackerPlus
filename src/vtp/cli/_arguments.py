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

"""Argument handling."""

class Arguments:

    """Arguments common to multiple commands.

    Parameters are kept minimal but are provided when one command may have a
    different value than another.
    """

    # Note: If commands were classes this would be a base class.

    @staticmethod
    def add_merge_contests(parser):
        parser.add_argument(
            "-m",
            "--merge_contests",
            action="store_true",
            help="Will immediately merge the ballot contests (to main)",
        )

    @staticmethod
    def add_minimum_cast_cache(parser, default = 100):
        parser.add_argument(
            "-m",
            "--minimum_cast_cache",
            type=int,
            default=default,
            help="the minimum number of cast ballots required prior to merging (def=100)",
        )

    @staticmethod
    def add_print_only(parser):
        parser.add_argument(
            "-n",
            "--printonly",
            action="store_true",
            help="will printonly and not write to disk (def=True)",
        )

    @staticmethod
    def add_verbosity(parser):
        parser.add_argument(
            "-v",
            "--verbosity",
            type=int,
            default=3,
            help="0 critical, 1 error, 2 warning, 3 info, 4 debug (def=3)",
        )
