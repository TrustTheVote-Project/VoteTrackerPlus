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

"""cast_a_ballot.py - command line level test script to automatically cast a ballot.

See './cast_a_ballot.py -h' for usage information.

See ../docs/tech/executable-overview.md for the context in which this file was created.

"""

# pylint: disable=C0413   # import statements not top of file
import re
import sys
import argparse
import logging

# Local imports
from address import Address
from ballot import Ballot
from election_config import ElectionConfig

################
# arg parsing
################
def parse_arguments():
    """Parse command line arguments
    """

    parser = argparse.ArgumentParser(description=\
    """accept_ballot.py will run the git based workflow on a VTP
    scanner node to accept the json rendering of the cast vote record
    of a voter's ballot. The json file is read, the contests are
    extraced and submitted to separate git branches, one per contest,
    and pushed back to the Voter Center's VTP remote.

    In addition a voter's ballot receipt and offset are optionally
    printed.
    """)

    parser.add_argument("-v", "--verbosity", type=int, default=3,
                            help="0 critical, 1 error, 2 warning, 3 info, 4 debug (def=3)")
    parser.add_argument("-n", "--printonly", action="store_true",
                            help="will printonly and not write to disk (def=True)")

    parsed_args = parser.parse_args()
    verbose = {0: logging.CRITICAL, 1: logging.ERROR, 2: logging.WARNING,
                   3: logging.INFO, 4: logging.DEBUG}
    logging.basicConfig(format="%(message)s", level=verbose[parsed_args.v], stream=sys.stdout)
    return parsed_args

################
# main
################
def main():
    """Main function - see -h for more info.  At the moment no error
    handling, but in theory something might go here once a UX error
    model has been chosen.
    """

    # Create an VTP election config object
    the_election_config = ElectionConfig()
    the_election_config.parse_configs()

    # process the provided address
    my_args = dict(vars(args))
    for key in ['verbosity', 'printonly']:
        del my_args[key]
    # if address was supplied, get rid of that too
    if my_args['address']:
        my_args['number'], my_args['street'] = re.split(r'\s+', my_args['address'], 1)
    del my_args['address']
    the_address = Address(**my_args)
    the_address.map_ggos(the_election_config)

    # get the ballot for the specified address
    a_ballot = Ballot()
    a_ballot.read_a_ballot(the_address, the_election_config)

    # loop over contests
    for contest in a_ballot.contests:
        # get the possible choices
        choices = a_ballot.get_contest_choices(contest)
        # choose something
        a_ballot.vote_a_contest(contest, random_choice(choices))

    # write it out
    # pylint: disable=W0104  # ZZZ
    if args.printonly:
        a_ballot.pprint
    else:
        a_ballot.write_a_cast_ballot(the_election_config)

if __name__ == '__main__':
    args = parse_arguments()
    main()
