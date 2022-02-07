#!/usr/bin/env python

"""Command line level script to accept a ballot.  See
'./accept_ballot.py -h'"""

import subprocess
import json
import sys
import argparse
import logging
#  Not currently used/imported:  critical, error, info, warning, debug
from logging import info

# save the user from themselves
if not sys.version_info.major == 3 and sys.version_info.minor >= 9:
    print("Python 3.9 or higher is required.")
    print(f"You are using Python {sys.version_info.major}.{sys.version_info.minor}.")
    sys.exit(1)

# Globals for now
CONTEST_FILE = "CVRs/contest.cvr"
"""Temporary global variable for the location of the contest cvr file"""
GIT_TIMEOUT = 30
"""How long to wait for a git command to complete - maybe a bad idea """

def run_git_cmd(argv):
    """Run a git command with logging and error handling.  Raises a
    CalledProcessError if the git command fails - the caller needs to
    deal with that.  Can also raise a TimeoutExpired exception.

    Nominally returns a CompletedProcess instance.

    See for example https://docs.python.org/3.9/library/subprocess.html
    """
    info(f"Running git({', '.join(argv)})")
    argv = ["echo", "git"] + argv
    return subprocess.run(argv, timeout=GIT_TIMEOUT, check=True)

def checkout_new_contest_branch():
    """Will checkout a new branch for a specific contest
    """
    branch = "foo/12345678"
    info(f"Checking out a new contest branch {branch}")
    return branch

def create_json_content():
    """Will create the JSON payload for this contest and place it in the CVR file
    """
    info("Creating the JSON payload")
    return 0

def add_commit_push_contest(branch):
    """Will git add and commit the new contest content
    """
    # If this fails,
    run_git_cmd(["add", CONTEST_FILE])
    run_git_cmd(["commit", "-F", CONTEST_FILE])
    # Note - if there is a collision, pick another random number and try again
    run_git_cmd(["push", "origin", branch])
    return 0

################
# arg parsing
################
def parse_arguments():
    """Parse arguments from a command line
    """
    parser = argparse.ArgumentParser(description='Arguments get parsed via --commands')
    parser.add_argument('-v', metavar='verbosity', type=int, default=3,
        help='Verbosity (0 critical, 1 error, 2 warning, 3 info, 4 debug)')

    args = parser.parse_args()
    verbose = {0: logging.CRITICAL, 1: logging.ERROR, 2: logging.WARNING,
                   3: logging.INFO, 4: logging.DEBUG}
    logging.basicConfig(format='%(message)s', level=verbose[args.v], stream=sys.stdout)
    return args

################
# main
################
def main():
    """Main function - see -h for more info.  At the moment no error
    handling, but in theory something might go here once a UX error
    model has been chosen.
    """
    branch = checkout_new_contest_branch()
    create_json_content()
    add_commit_push_contest(branch)

if __name__ == '__main__':
    my_args = parse_arguments()
    main()
