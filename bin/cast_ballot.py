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

# pylint: disable=wrong-import-position
import sys
import argparse
import logging
from logging import info, debug
import random
import pprint

# Local imports
from address import Address
from ballot import Ballot, Contests
from election_config import ElectionConfig

################
# arg parsing
################
def parse_arguments():
    """Parse command line arguments
    """

    parser = argparse.ArgumentParser(description=\
    """cast_ballot.py will read the blank ballot for a given address
    and by default randomly make a selection for each
    contest/question.  It will then cast the ballot in the
    corresponding CVRs directory.
    """)

    Address.add_address_args(parser)
    parser.add_argument("-v", "--verbosity", type=int, default=3,
                            help="0 critical, 1 error, 2 warning, 3 info, 4 debug (def=3)")
    parser.add_argument("-n", "--printonly", action="store_true",
                            help="will printonly and not write to disk (def=True)")

    parsed_args = parser.parse_args()
    verbose = {0: logging.CRITICAL, 1: logging.ERROR, 2: logging.WARNING,
                   3: logging.INFO, 4: logging.DEBUG}
    logging.basicConfig(format='%(message)s',
                            level=verbose[parsed_args.verbosity], stream=sys.stdout)
    return parsed_args

################
# main
################
def main():
    """Main function - see -h for more info"""

    # Create an VTP election config object
    the_election_config = ElectionConfig()
    the_election_config.parse_configs()

    # process the provided address
    the_address = Address.create_address_from_args(args, ['verbosity', 'printonly'])
    the_address.map_ggos(the_election_config)

    # get the ballot for the specified address
    a_ballot = Ballot()
    a_ballot.read_a_blank_ballot(the_address, the_election_config)

    # loop over contests
    contests = Contests(a_ballot)
    for contest in contests:
        # get the possible choices
        choices = contest.get('choices')
        tally = contest.get('tally')
        # choose something randomly
        picks = list(range(len(choices)))
        # For plurality and max=1, the first choice is the only
        # choice.  For plurality and max>1, the order does not matter
        # - a selection is a selection.  For RCV, the order does
        # matter as that is the ranking.
        random.shuffle(picks)
        if 'plurality' == tally:
            loop = contest.get('max')
        elif 'rcv' == tally:
            loop = len(choices)
        else:
            raise KeyError(f"Unspoorted tally ({tally})")
        while loop > 0:
            a_ballot.add_selection(contest, picks.pop(0))
            loop -= 1
    debug("And the ballot looks like:\n" + pprint.pformat(a_ballot.dict()))

    # write the voted ballot out
#    import pdb; pdb.set_trace()
    if args.printonly:
        pprint.pprint(a_ballot.dict())
    else:
        ballot_file = a_ballot.write_a_cast_ballot(the_election_config)
        info(f"Cast ballot file: {ballot_file}")
    # example of digging deeply into ElectionConfig data ...
    voting_centers = iter(the_election_config.get_node(a_ballot.get('ballot_node'),
                                                           'config')['vote centers'].items())
    info(f"Casting a {contests.len()} contest ballot at "
             f"{next(voting_centers)}")


if __name__ == '__main__':
    args = parse_arguments()
    main()
