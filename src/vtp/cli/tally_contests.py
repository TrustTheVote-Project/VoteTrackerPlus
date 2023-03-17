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
tally-contests - command line level script to tally the contests of
a election.

See 'tally-contests -h' for usage information.
"""

# Global imports
import argparse
import re
import sys

# Project imports
from vtp.ops.tally_contests_operation import TallyContestsOperation

# Local imports
from ._arguments import Arguments


def parse_arguments(argv):
    """Parse arguments from a command line or from the constructor"""

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
Will tally all the contests so far merged to the main branch and
report the results.  The results are computed on a voting center basis
(git submodule) basis.

Note - the current implementation relies on git submodules (individual
git repos) to break up the tally data of an election.  If there is
only one git repository and the election is large, then a potentiallu
large amount of memory will be used in executing the tallies.  One
short term fix for this is to limit the number of contests being
tallied.

Also note that the current implementation does not yet support
tallying across git submodules/repos.
""",
    )

    Arguments.add_election_data_dir(parser)
    parser.add_argument(
        "-c",
        "--contest_uid",
        default="",
        help="limit the tally to a specific contest uid",
    )
    parser.add_argument(
        "-t",
        "--track_contests",
        default="",
        help="a comma separated list of contests checks to track",
    )
    Arguments.add_verbosity(parser)
    parsed_args = parser.parse_args(argv)

    # Validate required args
    if parsed_args.track_contests:
        if not bool(re.match("^[0-9a-f,]", parsed_args.track_contests)):
            raise ValueError(
                "The track_contests parameter only accepts a comma separated (no spaces) "
                "list of contest checks/digests to track."
            )
        parsed_args.track_contests = parsed_args.track_contests.split(",")
    else:
        parsed_args.track_contests = []
    return parsed_args


# pylint: disable=duplicate-code
def main():
    """Entry point for 'tally-contests'."""

    # Parse args
    parsed_args = parse_arguments(sys.argv)

    # do it
    tco = TallyContestsOperation(
        parsed_args.election_data_dir,
        parsed_args.verbosity,
        parsed_args.printonly,
    )
    tco.run(
        contest_uid=parsed_args.contest_uid,
        track_contests=parsed_args.track_contests,
    )


# If called directly via this file
if __name__ == "__main__":
    main()
