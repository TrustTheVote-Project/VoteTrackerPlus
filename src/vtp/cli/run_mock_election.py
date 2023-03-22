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

# Project imports
from vtp.core.address import Address
from vtp.ops.run_mock_election_operation import RunMockElectionOperation

# Local imports
from ._arguments import Arguments


def parse_arguments():
    """Parse arguments from a command line or from the constructor"""

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

    Arguments.add_address_args(parser)
    Arguments.add_election_data_dir(parser)
    Arguments.add_blank_ballot(parser)
    parser.add_argument(
        "-d",
        "--device",
        default="",
        help="specify a specific VC local device (scanner or server or both) to mock",
    )
    Arguments.add_minimum_cast_cache(parser)
    # Note - the black formatter will by default break the help
    # line below into two lines via a '()', which breaks the
    # parser.add_argument.  It is python.
    #
    # fmt: off
    # pylint: disable=line-too-long
    parser.add_argument(
        "-f",
        "--flush_mode",
        type=int,
        default=0,
        help="will either not flush (0 - default), flush on exit (1), or flush on each iteration (2)",
        )
    # fmt: on
    parser.add_argument(
        "-i",
        "--iterations",
        type=int,
        default=10,
        help="the number of unique blank ballots for the mock scanner to cast (def=10)",
    )
    parser.add_argument(
        "-u",
        "--duration",
        type=int,
        default=10,
        help="the number of minutes for the mock server to run (def=10)",
    )
    Arguments.add_verbosity(parser)
    Arguments.add_printonly(parser)
    parsed_args = parser.parse_args()

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
    return parsed_args


# pylint: disable=duplicate-code
def main():
    """Entry point for 'run-mock-election'."""

    # Parse args
    parsed_args = parse_arguments()

    # Convert the address args into an Address
    an_address = Address(
        address=parsed_args.address,
        substreet=parsed_args.substreet,
        town=parsed_args.town,
        state=parsed_args.state,
    )

    # do it
    rmeo = RunMockElectionOperation(
        parsed_args.election_data_dir, parsed_args.verbosity, parsed_args.printonly
    )
    rmeo.run(
        an_address=an_address,
        device=parsed_args.device,
        minimum_cast_cache=parsed_args.minimum_cast_cache,
        flush_mode=parsed_args.flush_mode,
        iterations=parsed_args.iterations,
        duration=parsed_args.duration,
    )


# If called directly via this file
if __name__ == "__main__":
    main()
