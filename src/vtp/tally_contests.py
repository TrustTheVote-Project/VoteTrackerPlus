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
tally_contests.py - command line level script to tally the contests of
a election.

See 'tally_contests.py -h' for usage information.
"""

import argparse
import re

from vtp.ops.tally_contests_operation import TallyContestsOperation


# pylint: disable=duplicate-code
def parse_arguments():
    """Parse arguments from a command line"""

    parser = argparse.ArgumentParser(
        description="""Will tally all the contests so far merged to
    the master branch and report the results.  The results are
    computed on a voting center basis (git submodule) basis.

    Note - the current implementation relies on git submodules
    (individual git repos) to break up the tally data of an election.
    If there is only one git repository and the election is large,
    then a potentiallu large amount of memory will be used in
    executing the tallies.  One short term fix for this is to limit
    the number of contests being tallied.

    Also note that the current implementation does not yet support
    tallying across git submodules/repos.
    """
    )

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
    parser.add_argument(
        "-x",
        "--do_not_pull",
        action="store_true",
        help="Before tallying the votes, pull the ElectionData repo",
    )
    parser.add_argument(
        "-v",
        "--verbosity",
        type=int,
        default=3,
        help="0 critical, 1 error, 2 warning, 3 info, 4 debug (def=3)",
    )
    #    parser.add_argument("-n", "--printonly", action="store_true",
    #                            help="will printonly and not write to disk (def=True)")

    parsed_args = parser.parse_args()

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
    """
    Called via a python local install entrypoint or this file.  Simply
    wraps the scripts constructor, creates and ElectionConfig instance
    (which parses VTP's election data file which is implemented as a
    directory tree), and calls its main function.
    """

    # do it
    tco = TallyContestsOperation(parse_arguments())
    tco.run()


# If called directly via this file
if __name__ == "__main__":
    main()
