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
import sys
import argparse
import logging
import random

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
    """cast_ballot.py will read the blank ballot for a given address
    and by default randomly make a selection for each
    contest/question.  It will then cast the ballot in the
    corresponding CVRs directory.

    The switches are basically the same as create_blank_ballot.py
    """)

#    _keys = ['number', 'street', 'substreet', 'town', 'state', 'country', 'zipcode']
    parser.add_argument('-c', "--csv",
                            help="a comma separated address")
    parser.add_argument('-a', "--address",
                            help="the number and name of the street address (space separated)")
    parser.add_argument('-r', "--street",
                            help="the street/road field of an address")
    parser.add_argument('-b', "--substreet",
                            help="the substreet field of an address")
    parser.add_argument('-t', "--town",
                            help="the town field of an address")
    parser.add_argument('-s', "--state",
                            help="the state/province field of an address")
    parser.add_argument('-z', "--zipcode",
                            help="the zipcode field of an address")
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
        my_args['number'], my_args['street'] = \
        Address.convert_address_to_num_street(my_args['address'])
    del my_args['address']
    the_address = Address(**my_args)
    the_address.map_ggos(the_election_config)

    # get the ballot for the specified address
    a_ballot = Ballot()
    import pdb; pdb.set_trace()
    a_ballot.read_a_ballot(the_address, the_election_config)

    # loop over contests
    for contest in a_ballot:
        # get the possible choices
        choices = contest.get('choices')
        tally = contest.get('tally')
        # choose something randomly
        picks = list(range(len(choices)))
        random.shuffle(picks)
        if 'plurality' == tally:
            loop = contest.get('max')
        elif 'rcv' == tally:
            loop = len(choices)
        else:
            raise KeyError(f"Unspoorted tally ({tally})")
        while loop > 0:
            contest.select(picks.pop(0))
            loop -= 1

    # write the voted ballot out
    # pylint: disable=W0104  # ZZZ
    if args.printonly:
        a_ballot.pprint
    else:
        a_ballot.write_a_cast_ballot(the_election_config)

if __name__ == '__main__':
    args = parse_arguments()
    main()
