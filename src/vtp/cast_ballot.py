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

"""cast_ballot.py - command line level test script to automatically cast a ballot.

See './cast_ballot.py -h' for usage information.

See ../../docs/tech/executable-overview.md for the context in which this file was created.

"""

# pylint: disable=wrong-import-position
import argparse
import logging
import os
import pprint
import random
import sys
import traceback

import pyinputplus

# Local imports
from vtp.utils.address import Address
from vtp.utils.ballot import Ballot, BlankBallot, Contests
from vtp.utils.common import Globals, Shellout
from vtp.utils.election_config import ElectionConfig


################
# Functions
################
def make_random_selection(the_ballot, the_contest):
    """Will randomly make selections on a contest"""
    # get the possible choices
    choices = the_contest.get("choices")
    tally = the_contest.get("tally")
    # choose something randomly
    picks = list(range(len(choices)))
    # For plurality and max=1, the first choice is the only
    # choice.  For plurality and max>1, the order does not matter
    # - a selection is a selection.  For RCV, the order does
    # matter as that is the ranking.
    random.shuffle(picks)
    if "plurality" == tally:
        loop = the_contest.get("max")
    elif "rcv" == tally:
        loop = len(choices)
    else:
        raise KeyError(f"Unspoorted tally ({tally})")
    while loop > 0:
        the_ballot.add_selection(the_contest, picks.pop(0))
        loop -= 1


def get_user_selection(the_ballot, the_contest, count, total_contests):
    """Print the contest and get the selection(s) from the user"""
    choices = the_contest.get("choices")
    tally = the_contest.get("tally")
    max_votes = the_contest.get("max")
    # Print something
    print(f"################ ({count} of {total_contests})")
    print(f"Contest {the_contest.get('uid')}: {the_contest.get('name')}")
    if tally == "plurality":
        print(f"- This is a {tally} tally")
        print(
            f"- The voting is for {max_votes} open position(s)/choice(s) - "
            "only that number of selections can be choosen."
        )
    else:
        print(
            f"- This is a {tally} tally with {max_votes} open position(s)/choice(s).  "
            f"Regardless up to {len(choices)} selections can be rank choosen."
        )

    # Need to print the choices first up front
    count = 0
    for choice in choices:
        print(f"  [{count}] {choice}")
        count += 1

    def validate_multichoice(text):
        """Will validate the space separated user input choice string"""
        selections = text.split()
        choice_max = len(choices)
        errors = []
        validated_selections = []
        for num in selections:
            if not num.isnumeric():
                errors.append(f"The supplied choice ({num}) is not a number")
                continue
            num = int(num)
            if num < 0 or num > choice_max:
                errors.append(
                    f"The supplied choice ({num}) is not a valid selection "
                    f"(must be between 0 and {choice_max - 1} inclusive)"
                )
                continue
            if tally == "plurality" and len(selections) > choice_max:
                errors.append(
                    f"This contest is limited to at most {max_votes} selection(s): "
                    f"you supplied {len(selections)}"
                )
                continue
            #            import pdb; pdb.set_trace()
            if num in validated_selections:
                errors.append(
                    f"The selection {num} was supplied more than once.  "
                    "Each selection can only be supplied once."
                )
                continue
            validated_selections.append(num)
        if errors:
            err_string = "\n".join(errors)
            raise Exception(
                "Warning - you selections have the following errors\n" f"{err_string}"
            )
        # if still here, set the selection
        try:
            # Since it is possible to self adjudicate a contest, always
            # explicitly clear the selection before adding
            the_ballot.clear_selection(the_contest)
            for sel in validated_selections:
                the_ballot.add_selection(the_contest, sel)
        # pylint: disable=broad-except
        except Exception:
            # blow out of the internal pyinputplus try/catch
            traceback.print_exc()
            sys.exit(1)

    if tally == "plurality":
        if max_votes > 1:
            prompt = (
                f"Please enter the numbers for your choices (max={max_votes}) "
                "separated by spaces: "
            )
        else:
            prompt = "Please enter the number for your choice: "
        pyinputplus.inputCustom(validate_multichoice, prompt=prompt, blank=True)
    else:
        # Then prompt for input
        prompt = "Please enter in rank order the numbers of your choices separated by spaces: "
        pyinputplus.inputCustom(validate_multichoice, prompt=prompt, blank=True)


def loop_over_contests(a_ballot):
    """Will loop over the contests in a ballot and either ask the user
    for a choice or if in demo mode will randomly choose one.
    """
    contests = Contests(a_ballot)
    total_contests = contests.len()
    count = 0
    contest_uids = []
    for contest in contests:
        contest_uids.append(contest.get("uid"))
        if ARGS.demo_mode:
            make_random_selection(a_ballot, contest)
        else:
            # Display the tally type and choices and allow the user to manually
            # enter something.  Might as well validate legal selections (in
            # this demo) as that is the long-term VTP vision.
            count += 1
            get_user_selection(a_ballot, contest, count, total_contests)
    if not ARGS.demo_mode:
        # UX wise replicate the self adjudication experince.  This is
        # basically another endless loop until done
        while True:
            # Print the selections
            for contest in contests:
                print(
                    f"Contest {contest.get('uid')} - {contest.get('name')}: "
                    f"{contest.get('selection')}"
                )
            prompt = "Is this correct?  Enter yes to accept the ballot, no to reject the ballot: "
            if "yes" == pyinputplus.inputYesNo(prompt):
                break
            prompt = (
                "Enter a contest uid to redo that contest, "
                "enter nothing (leave blank and hit enter) to start completely over: "
            )
            response = pyinputplus.inputChoice(contest_uids + [""], prompt)
            if response == "":
                count = 0
                for contest in contests:
                    count += 1
                    get_user_selection(a_ballot, contest, count, total_contests)
            else:
                for contest in contests:
                    if contest.get("uid") == response:
                        get_user_selection(a_ballot, contest, 1, 1)
                        break
    # For a convenient side effect, return the contests
    return contests


################
# arg parsing
################
# pylint: disable=duplicate-code
def parse_arguments():
    """Parse command line arguments"""

    parser = argparse.ArgumentParser(
        description="""cast_ballot.py can either read a blank ballot and allow a user
    to manually select choices or when in demo mode, cast_ballot.py
    will randominly select choices.
    """
    )

    Address.add_address_args(parser)
    # ZZZ - cloaked contests are enabled at cast_ballot time
    #    parser.add_argument('-k', "--cloak", action="store_true",
    #                            help="if possible provide a cloaked ballot offset")
    parser.add_argument(
        "--demo_mode",
        action="store_true",
        help="set demo mode to automatically cast random ballots",
    )
    parser.add_argument(
        "--blank_ballot",
        help="overrides an address - specifies the specific blank ballot",
    )
    parser.add_argument(
        "-v",
        "--verbosity",
        type=int,
        default=3,
        help="0 critical, 1 error, 2 warning, 3 info, 4 debug (def=3)",
    )
    parser.add_argument(
        "-n",
        "--printonly",
        action="store_true",
        help="will printonly and not write to disk (def=True)",
    )
    parsed_args = parser.parse_args()
    verbose = {
        0: logging.CRITICAL,
        1: logging.ERROR,
        2: logging.WARNING,
        3: logging.INFO,
        4: logging.DEBUG,
    }
    logging.basicConfig(
        format="%(message)s", level=verbose[parsed_args.verbosity], stream=sys.stdout
    )
    return parsed_args


################
# main
################

ARGS = None

# pylint: disable=duplicate-code
def main():
    """Main function - see -h for more info"""

    # pylint: disable=global-statement
    global ARGS
    ARGS = parse_arguments()

    # Create an VTP election config object
    the_election_config = ElectionConfig()
    the_election_config.parse_configs()

    # Create a ballot
    a_ballot = BlankBallot()

    # process the provided address
    if ARGS.blank_ballot:
        # Read the specified blank_ballot
        with Shellout.changed_cwd(
            os.path.join(
                the_election_config.get("git_rootdir"),
                Globals.get("ROOT_ELECTION_DATA_SUBDIR"),
            )
        ):
            a_ballot.read_a_blank_ballot("", the_election_config, ARGS.blank_ballot)
    else:
        # Use the specified address
        the_address = Address.create_address_from_args(
            ARGS, ["verbosity", "printonly", "blank_ballot", "demo_mode"]
        )
        the_address.map_ggos(the_election_config)
        # get the ballot for the specified address
        a_ballot.read_a_blank_ballot(the_address, the_election_config)

    contests = loop_over_contests(a_ballot)
    logging.debug("And the ballot looks like:\n%s", pprint.pformat(a_ballot.dict()))

    # ZZZ - for this program there is no call to verify_cast_ballot to
    # verify that the ballot has been filled out correctly and offer
    # to the voter a chance to redo it.

    if ARGS.printonly:
        ballot_file = Ballot.gen_cast_ballot_location(
            the_election_config, a_ballot.get("ballot_subdir")
        )
    else:
        ballot_file = a_ballot.write_a_cast_ballot(the_election_config)
    # example of digging deeply into ElectionConfig data ...
    #    import pdb; pdb.set_trace()
    voting_centers = the_election_config.get_node(
        a_ballot.get("ballot_node"), "config"
    )["voting centers"]
    for vote_center in voting_centers:
        logging.info(
            "Casting a %s contest ballot at VC %s", contests.len(), vote_center
        )
        logging.info("Cast ballot file: %s", ballot_file)


if __name__ == "__main__":
    main()

# EOF
