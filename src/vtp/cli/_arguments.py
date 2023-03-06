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

from vtp.core.address import Address


class Arguments:

    """Arguments common to multiple commands.

    Parameters are kept minimal but are provided when one command may have a
    different value than another.
    """

    # Note: If commands were classes this would be a base class.

    @staticmethod
    def add_address(parser, generic_address=False):
        """Add standard address program options"""
        # parser.add_argument('-c', "--csv",
        #     help="a comma separated address")
        #        parser.add_argument('-r', "--street",
        #     help="the street/road field of an address, in which case the address is the number")
        # parser.add_argument('-z', "--zipcode",
        #     help="the zipcode field of an address")
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
    def add_merge_contests(parser):
        parser.add_argument(
            "-m",
            "--merge_contests",
            action="store_true",
            help="Will immediately merge the ballot contests (to main)",
        )

    @staticmethod
    def add_minimum_cast_cache(parser, default=100):
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

    def parse_arguments(parser, args, generic_address=False):
        """Main interface for argument parsing.

        This wraps argparse to allow special case processing, including:
            - Address argument canonicalization.
            - ...

        Parameters:
            parser: Argparse argument parser
            args: List of CLI arguments to parse
            generic_address: Whether a generic address is expected.

        Returns:
            If address arguments are present, 2-tuple:
            - Address arguments as a dictionary.
            - Non-address arguments as a dictionary
            Otherwise all parsed arguments as a single dictionary.

        Notes:
            No argparse namespaces are visible outside of this function.
            Everything is dictionaries.
        """
        parsed_options = parser.parse_args(args)
        # Convert argparse namespace to dictionary.
        parsed_args = dict(vars(parsed_options))
        # Canonicalize address arguments if any
        if Address.has_address_arguments(parsed_args):
            address_args, processed_args = Address.separate_addresses_from_arguments(
                parsed_args
            )
            processed_args["address"] = Address(
                generic_address=generic_address, **address_args
            )
        else:
            processed_args = parsed_args
        return processed_args
