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

"""Command line script set up a VTP demo.

Can also set up individual GUID based ballot-stores and return the GUID.

Run with '--help' for usage information.
"""

# Standard imports
import argparse
import os
import sys

# Local imports
from vtp.core.common import Common, Globals
from vtp.ops.setup_vtp_demo_operation import SetupVtpDemoOperation

from ._arguments import Arguments


def parse_arguments(argv):
    safe_args = Common.cast_thing_to_list(argv)
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
Will leverage this current git repository (VoteTrackerPlus) and the
associated ElectionData repo(s) to nominally create in
/opt/VoteTrackerPlus (the default) a demo election with 4 mock ballot
scanner apps and one tabulation server app. The initial demo idea is
to have three scanners scanning random ballots while one scanner is
used interactively.

All five apps run in separate git workspaces that are clones of the
same ElectionData repo(s). The (4) mock scanner app clones are located
in one folder, the one tabulation server is located in another, and
the FastAPI clients are located in a third. The FastAPI clients are
separated by a GUID based subdirectory similar to the native Git
storage idiom.

If the --guid_client_store option is set, instead of setting up the
demo this script will create a new GUID based FASTapi clone and return
the GUID.
""",
    )
    parser.add_argument(
        "-s",
        "--scanners",
        type=int,
        default=4,
        help="specify a number of scanner app instances (def=4)",
    )
    parser.add_argument(
        "-g",
        "--guid_client_store",
        action="store_true",
        help="if set will create a single GUID based ballot-store and return the GUID",
    )
    parser.add_argument(
        "-l",
        "--location",
        default="/opt/VoteTrackerPlus/demo.01",
        help="specify the location of VTP demo (def=/opt/VoteTrackerPlus/demo.01)",
    )
    Arguments.add_verbosity(parser)
    Arguments.add_print_only(parser)

    parsed_args = Arguments.parse_arguments(parser, safe_args)

    # Validation
    if parsed_args["scanners"] < 1 or parsed_args["scanners"] > 16:
        raise ValueError(
            "The demo needs at least one TVP scanner app "
            "and arbitrarily limits a demo to 16."
        )
    # Check the root of the demo
    if not os.path.isdir(parsed_args["location"]):
        raise FileNotFoundError(
            f"The root demo folder, {parsed_args['location']}, does not exit.  "
            "It needs to pre-exist - please manually create it."
        )
    test_dir = os.path.join(
        parsed_args["location"], Globals.get("TABULATION_SERVER_DIRNAME")
    )
    if parsed_args["guid_client_store"] and not os.path.isdir(test_dir):
        raise FileNotFoundError(
            f"The tabulation server workspace ({test_dir}) does not exit.  "
            "It needs to pre-exist and is created when setup-vtp-demo is executed "
            "in setup mode (without the -g switch)."
        )

    return parsed_args


def main():
    """Entry point for 'setup-vtp-demo'."""

    args = parse_arguments(sys.argv[1:])
    op = SetupVtpDemoOperation(**args)
    guid = op.run()
    if isinstance(guid, str):
        print(guid)


# If called directly via this file
if __name__ == "__main__":
    main()
