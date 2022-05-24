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
verify_ballot_receipt.py - command line level script to verify a
voters ballot receipt.

See './verify_ballot_receipt.py -h' for usage information.

See ../docs/tech/*.md for the context in which this file was created.
"""

# Standard imports
import sys
# pylint: disable=wrong-import-position   # import statements not top of file
import argparse
import logging
import re
import json
from logging import error

# Local import
from address import Address
from ballot import Ballot
from election_config import ElectionConfig
from common import Shellout
# Functions


################
# arg parsing
################
# pylint: disable=duplicate-code
def parse_arguments():
    """Parse arguments from a command line"""

    parser = argparse.ArgumentParser(description=
    """verify_ballot_receipt.py will read a voter's ballot receipt and
    validate all the digests contained therein.  If a contest has been
    merged to the master branch, will report the current ballot tally
    number (which ballot in the actula tally cound is the voter's).
    """,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    Address.add_address_args(parser, True)
    parser.add_argument("-f", "--receipt_file", default='',
                            help="specify the ballot receipt location - overrides an address")
    parser.add_argument("-r", "--row", default='',
                            help="specify a row to further inspect and show (1 based, not 0)")
    parser.add_argument("-v", "--verbosity", type=int, default=3,
                            help="0 critical, 1 error, 2 warning, 3 info, 4 debug (def=3)")
#    parser.add_argument("-n", "--printonly", action="store_true",
#                            help="will printonly and not write to disk (def=True)")

    parsed_args = parser.parse_args()
    verbose = {0: logging.CRITICAL, 1: logging.ERROR, 2: logging.WARNING,
                   3: logging.INFO, 4: logging.DEBUG}
    logging.basicConfig(format="%(message)s", level=verbose[parsed_args.verbosity],
                            stream=sys.stdout)

    # Validate required args
    return parsed_args

################
# main
################
# pylint: disable=duplicate-code
def main():
    """Main function - see -h for more info"""

    # Create an VTP election config object
    the_election_config = ElectionConfig()
    the_election_config.parse_configs()

    # Create a ballot to read the receipt file
    a_ballot = Ballot()
    lines = []
    if args.receipt_file:
        # Can read the receipt file directly without any Ballot info
        lines = a_ballot.read_receipt_csv(the_election_config, receipt_file=args.receipt_file)
    else:
        # Need to use the address to locate the last created receipt file
        the_address = Address.create_address_from_args(args,
                        ['verbosity', 'receipt_file', 'row'], generic_address=True)
        the_address.map_ggos(the_election_config, skip_ggos=True)
        lines = a_ballot.read_receipt_csv(the_election_config, address=the_address)

    # Loop over each row and grab the header line (the list of UIDs of
    # interest) and the validate the row one at a time. Validation is
    # multiple steps: 1) does the digest exist; 2) is it the correct
    # uid?; 3) is the digest in the tally (legally in master). Some
    # future meta tests could be: 4) does the receipt have a repeated
    # digest?; 5) does it have a valid election uid beyond a valid
    # digest and contest uid (TBD - not implemented yet)
    headers = lines.pop(0)
    uids = [ re.match(r'([0-9]+)', column).group(0) for column in headers ]
    error_strings = []
    error_digests = set()
    requested_row = []
    for index, row in enumerate(lines):
        # Note - result errors are ignored/not returned, so walk the list
        cvrs = Shellout.cvr_parse_git_log_output(
            ['git', 'log', '--no-walk', '--pretty=format:%H%B'] + row,
            the_election_config, grouped_by_uid=False)
        if args.row != '' and int(args.row) - 1 == index:
#            import pdb; pdb.set_trace()
            requested_row = cvrs
        column = -1
        for digest in row:
            column += 1
            if digest not in cvrs:
                error_strings.append(
                    f"MISSING DIGEST: row {row} column {column} "
                    "contest {headers[column]} digest={digest}")
                error_digests.add(digest)
                continue
            if cvrs[digest]['CVR']['uid'] != uids[column]:
                error_strings.append(
                    f"BAD CONTEST UID: row {row} column {column} "
                    "contest {headers[column]} != {cvrs[digest]['CVR']['uid']} digest={digest}")
                error_digests.add(digest)
                continue
    # Summerize
    if error_strings:
        error(f"The supplied ballot receipt had {error_digests} errors.  They are:\n"
                  '\n'.join(error_strings))
    else:
        print("No digest errors found")
    # If a row is specified, will print the context index in the
    # actual contest tally - which basically tells the voter 'your
    # contest is in the tally at index N'
    if args.row:
        for digest in lines[int(args.row) - 1]:
            if digest in error_digests:
                print(f"Digest {digest} is invalid")
                break
            print(f"{json.dumps(requested_row[digest], indent=5, sort_keys=True)}")
        # Print the offset in the actual tally, but to do that, need
        # to get the actual complete tally for the contests of
        # interest.  And at the moment might as well do that for all
        # contests (unless one cat create the git grep query syntax to
        # just pull the uids of interest).
        contest_batches = Shellout.cvr_parse_git_log_output(
            ['git', 'log', '--topo-order', '--no-merges', '--pretty=format:%H%B'],
            the_election_config)
        unmerged_uids = []
        for uid in uids:
            # For this contest loop over the reverse ordered CVRs (since it
            # seems TBD that it makes sense to ballot #1 as the first ballot on
            # master).
            contest_votes = len(contest_batches[uid])
            found = False
            for count, contest in enumerate(contest_batches[uid]):
#                import pdb; pdb.set_trace()
                if contest['digest'] in requested_row:
                    print(
                        f"Contest '{contest['CVR']['uid']} - {contest['CVR']['name']}' "
                        f"({contest['digest']}) is vote {contest_votes - count} out "
                        f"of {contest_votes} votes")
                    found = True
                    break
            if found is False:
                unmerged_uids.append(uid)
        if unmerged_uids:
            print("The following contests are not merged to master yet:")
            print('\n'.join(unmerged_uids))

if __name__ == '__main__':
    args = parse_arguments()
    main()

# EOF
