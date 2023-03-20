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

    """Arguments common to multiple commands.  Parameters are kept
    minimal but are provided when one command may have a different
    value than another.
    """

    # Note: If commands were classes this would be a base class.

    # Tbe below are options that are shared across the various
    # operations.  Options that are unique to one operation are
    # located in that file.

    @staticmethod
    def add_address_args(parser, generic_address=False):
        """Helper function to add standard address program switches to argparse"""
        #        parser.add_argument('-c', "--csv",
        #                                help="a comma separated address")
        #        parser.add_argument('-r', "--street",
        #                                help="the street/road field of an address, \
        #                                in which case the address is the number")
        #        parser.add_argument('-z', "--zipcode",
        #                                help="the zipcode field of an address")
        if not generic_address:
            parser.add_argument(
                "-a",
                "--address",
                default="",
                help="the number and name of the street address (space separated)",
            )
            parser.add_argument(
                "-b",
                "--substreet",
                default="",
                help="the substreet field of an address",
            )
        parser.add_argument(
            "-t",
            "--town",
            default="",
            help="the town field of an address",
        )
        parser.add_argument(
            "-s",
            "--state",
            default="",
            help="the state/province field of an address",
        )

    @staticmethod
    def add_blank_ballot(parser):
        """Add blank_ballot option"""
        parser.add_argument(
            "--blank_ballot",
            help="overrides an address - specifies the specific blank ballot",
        )

    @staticmethod
    def add_election_data_dir(parser):
        """Add election_data option"""
        parser.add_argument(
            "-e",
            "--election_data_dir",
            default=".",
            help="specify a absolute or relative path to the ElectionData tree (def='.')",
        )

    @staticmethod
    def add_merge_contests(parser):
        """Add merge_contests option"""
        parser.add_argument(
            "-m",
            "--merge_contests",
            action="store_true",
            help="Will immediately merge the ballot contests (to main)",
        )

    @staticmethod
    def add_minimum_cast_cache(parser):
        """Add minimum_cast_cache option"""
        parser.add_argument(
            "-m",
            "--minimum_cast_cache",
            type=int,
            default=100,
            help="the minimum number of cast ballots required prior to merging (def=100)",
        )

    @staticmethod
    def add_printonly(parser):
        """Add printonly option"""
        parser.add_argument(
            "-n",
            "--printonly",
            action="store_true",
            help="will printonly and not write to disk (def=True)",
        )

    @staticmethod
    def add_verbosity(parser, verbosity=3):
        """Add verbosity option"""
        parser.add_argument(
            "-v",
            "--verbosity",
            type=int,
            default=verbosity,
            help=f"0 critical, 1 error, 2 warning, 3 info, 4 debug (def={verbosity})",
        )
