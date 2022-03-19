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

"""create_blank_ballot.py - command line level test script to automatically cast a ballot.

See './create_blank_ballot.py -h' for usage information.

See ../docs/tech/executable-overview.md for the context in which this file was created.

"""

# Standard imports
# pylint: disable=C0413   # import statements not top of file
import sys
import argparse
import logging
from logging import info, debug
import re
import pprint

# Local imports
from address import Address
from ballot import Ballot
from election_config import ElectionConfig


################
# arg parsing
################
def parse_arguments():
    """Parse command line arguments"""

    parser = argparse.ArgumentParser(description=
    """create_blank_ballot.py will parse all the config and
    address_map yaml files in the current VTP election git tree and
    create a blank ballot based on the supplied address.

    ZZZ - in the future some other argument can be supported to print
    for example all possible unique blank ballots found in the current
    VTP election tree, whatever.
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
    parser.add_argument('-f', "--file",
                            help="override the default blank ballot location")
    parser.add_argument('-l', "--language", default='en',
                            help="will print the ballot in the specified language")
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

    # Parse the address nominally supplied via the args. ZZZ -
    # existing address parsing packages look out-of-date and US
    # centric. But the idea is that the actual town will know the
    # latest and greatest and that any other data may/will be out of
    # date, particularly if the voting center can update records on
    # the fly. So, for now assume that the street address map will be
    # imported somehow and that each GGO for the address will also be
    # imported somehow. And all that comes later - for now just map an
    # address to a town.
    my_args = dict(vars(args))
    for key in ['verbosity', 'printonly', 'language', 'file']:
        del my_args[key]
    # if address was supplied, get rid of that too
    if my_args['address']:
        my_args['number'], my_args['street'] = re.split(r'\s+', my_args['address'], 1)
    del my_args['address']
    the_address = Address(**my_args)
    the_address.map_ggos(the_election_config)

    # print some debugging info
    debug(f"The election config is: {the_election_config}")
    debug("And the address is: " + str(the_address))
    node = 'towns/Oakland'
    debug(f"And node ({node}) looks like:" +
        pprint.pformat(the_election_config.get_node(node, 'ALL')))
    debug("And the edges look like:" +
        pprint.pformat(the_election_config.get_dag('edges')))

    # Construct a blank ballot
    the_ballot = Ballot()
    the_ballot.create_blank_ballot(the_address, the_election_config)

    # Print it
    if args.printonly:
        info(pprint.pformat(the_ballot.get('ballot')))
    else:
#        import pdb; pdb.set_trace()
        ballot_file = the_ballot.write_blank_ballot(the_election_config, args.file)
        info(f"Blank ballot file: {ballot_file}")

if __name__ == '__main__':
    args = parse_arguments()
    main()

# EOF
