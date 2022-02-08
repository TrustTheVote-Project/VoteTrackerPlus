#!/usr/bin/env python

"""Command line level script to accept a ballot.  See './accept_ballot.py -h'"""

import subprocess
# import json
import sys
import argparse
import logging
#  Not currently used/imported:  critical, error, info, warning, debug
from logging import error, warning, info
import secrets

# save the user from themselves
if not sys.version_info.major == 3 and sys.version_info.minor >= 9:
    print("Python 3.9 or higher is required.")
    print(f"You are using Python {sys.version_info.major}.{sys.version_info.minor}.")
    sys.exit(1)

# Globals for now
CONTEST_FILE = "CVRs/contest.cvr"
"""Temporary global variable for the location of the contest cvr file"""
SHELL_TIMEOUT = 30
"""How long to wait for a generic shell command to complete - maybe a bad idea"""
ARGV = {}
"""The program's args for the moment"""

def run_shell_cmd(argv):
    """Run a shell command with logging and error handling.  Raises a
    CalledProcessError if the shell command fails - the caller needs to
    deal with that.  Can also raise a TimeoutExpired exception.

    Nominally returns a CompletedProcess instance.

    See for example https://docs.python.org/3.9/library/subprocess.html
    """
    info(f"Running \"{' '.join(argv)}\"")
    if ARGV['printonly']:
        return subprocess.CompletedProcess(argv, 0, stdout=None, stderr=None)
    return subprocess.run(argv, timeout=SHELL_TIMEOUT, check=True)

def checkout_new_contest_branch(contest, branchpoint):
    """Will checkout a new branch for a specific contest
    """
    branch = contest + "/" + secrets.token_hex(9)
    # if after 3 tries it still does not work, raise an error
    max_tries = 3
    count = 1
    while count < max_tries:
        count += 1
        args = ["git", "checkout", "-b", branch, branchpoint]
        try:
            cmd1 = run_shell_cmd(args)
        except subprocess.TimeoutExpired:
            warning(f"previous command \"{' '.join(args)}\" timed out!")
            break
        if cmd1.returncode == 0:
            # Created the local branch - see if it is push-able
            args = ["git", "push", "origin", branch]
            try:
                cmd2 = run_shell_cmd(args)
            except subprocess.TimeoutExpired:
                warning(f"previous command \"{' '.join(args)}\" timed out!")
                break
            if cmd2.returncode == 0:
                # branch has been successfully created locally and remotely
                return branch
    # No handled exceptions and no remote branch created - fail
    error(f"could not create git branch {branch}")
    # ZZZ need to clean up defunct branches
    return None

def add_commit_push_contest(branch):
    """Will git add and commit the new contest content
    """
    # If this fails,
    run_shell_cmd(["git", "add", CONTEST_FILE])
    run_shell_cmd(["git", "commit", "-F", CONTEST_FILE])
    # Note - if there is a collision, pick another random number and try again
    run_shell_cmd(["git", "push", "origin", branch])
    return 0

################
# arg parsing
################
def parse_arguments():
    """Parse arguments from a command line
    """
    parser = argparse.ArgumentParser(description='Arguments get parsed via --commands')
    parser.add_argument('-v', metavar='verbosity', type=int, default=3,
                            help='0 critical, 1 error, 2 warning, 3 info, 4 debug (def=3)')
    parser.add_argument('-n', metavar='printonly', type=bool, default=True,
                            help='will printonly and not write to disk (def=True)')

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

    # read in ballot.json

    # the voter's row of digests
    contest_receipts = []

    # loop over contests
    contest = "foo"
    # select a branchpoint
    branchpoint = "bar"
    # atomically create the branch locally and remotely
    branch = checkout_new_contest_branch(contest, branchpoint)
    # commit the voter's choice and push it
    digest = add_commit_push_contest(branch)
    contest_receipts.append(digest)

    # if possible print the ballot receipt

    # if possible, print the voter's offset

if __name__ == '__main__':
    ARGS = parse_arguments()
    main()
