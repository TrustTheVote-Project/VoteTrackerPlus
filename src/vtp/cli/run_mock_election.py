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

"""Command line script to run either a VTP ballot scanner or tabulator app.

Run with '--help' for usage information.
"""

# Standard imports
import argparse
import sys

# Local import
from vtp.core.address import Address
from vtp.core.common import Common
from vtp.ops.run_mock_election_operation import RunMockElectionOperation

from ._arguments import Arguments


def parse_arguments(argv):
    safe_args = Common.cast_thing_to_list(argv)
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
Will run a mock election with N ballots across the available blank
ballots found in the ElectionData.

One basic idea is to run this in different windows, one per VTP
scanner.  The scanner is nominally associated with a town (as
configured).

When "-d scanner" is supplied, run_mock_election.py will randomly
cast and scan ballots.

When "-d server" is supplied, run_mock_election.py will
synchronously run the merge_contests.py program which will once
every 10 seconds.  Note that nominally 100 contgests need to have
been pushed for merge_contests.py to merge in a contest into the
main branch without the --flush_mode option.

If "-d both" is supplied, run_mock_election.py will run a single
scanner N iterations while also calling the server function.  If
--flush_mode is set to 1 or 2, run_mock_election.py will then
flush the ballot cache before printing the tallies and exiting.

By default run_mock_election.py will loop over all available blank
ballots found withint the ElectionData tree.  However, either a
specific blank ballot or an address can be specified to limit the
mock to a single ballot N times.
""",
    )

    Arguments.add_address(parser)
    parser.add_argument(
        "--blank_ballot",
        help="overrides an address - specifies the specific blank ballot",
    )
    parser.add_argument(
        "-d",
        "--device",
        default="",
        help="specify a specific VC local device (scanner or server or both) to mock",
    )
    Arguments.add_minimum_cast_cache(parser)
    parser.add_argument(
        "-f",
        "--flush_mode",
        type=int,
        default=0,
        help="will either not flush (0 - default), flush on exit (1), or flush on each iteration (2)",
    )
    parser.add_argument(
        "-i",
        "--iterations",
        type=int,
        default=10,
        help="the number of unique blank ballots for the scanner app to cast (def=10)",
    )
    parser.add_argument(
        "-u",
        "--duration",
        type=int,
        default=10,
        help="the number of minutes for the server app to run (def=10)",
    )
    Arguments.add_verbosity(parser)
    Arguments.add_print_only(parser)

    parsed_args = parser.parse_args(safe_args)

    # Validate required args

    if parsed_args.device not in ["scanner", "server", "both"]:
        raise ValueError(
            "The --device parameter only accepts 'device' or 'server' "
            f"or 'both' - ({parsed_args.device}) was suppllied."
        )
    if parsed_args.flush_mode not in [0, 1, 2]:
        raise ValueError(
            "The value of flush_mode must be either 0, 1, or 2"
            f" - {parsed_args.flush_mode} was supplied."
        )

    address_args, parsed = Arguments.separate_addresses(parsed_args)
    parsed["address"] = Address(**address_args)
    return parsed


# pylint: disable=duplicate-code
def main():
    """Entry point for 'run-mock-elections'."""

    args = parse_arguments(sys.argv[1:])
    op = RunMockElectionOperation(**args)
    op.run()


# If called directly via this file
if __name__ == "__main__":
    main()
