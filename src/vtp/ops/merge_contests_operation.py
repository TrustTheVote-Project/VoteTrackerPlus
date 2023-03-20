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
Library backend to command line level script to merge CVR contest
branches into the main branch

See 'merge-contests -h' for usage information.
"""

# Standard imports
import logging
import os
import random
import re

# Project import
from vtp.core.common import Globals, Shellout
from vtp.core.election_config import ElectionConfig

# Local imports
from .operation import Operation


class MergeContestsOperation(Operation):
    """
    A class to implememt the merge-contests operation.  See the
    merge-contests help output or read the parse_argument argparse
    description (immediately below this) in the source file.
    """

    def __init__(self, election_data_dir: str, verbosity: int, printonly: bool):
        """
        Primarily to module-ize the scripts and keep things simple,
        idiomatic, and in different namespaces.
        """
        super().__init__(election_data_dir, verbosity, printonly)

    def merge_contest_branch(self, branch: str, remote: bool):
        """Merge a specific branch"""
        # If the VTP server is processing contests from different
        # voting centers, then the contest.json could be in different
        # locations on different branches.
        contest_file = Shellout.run(
            ["git", "diff-tree", "--no-commit-id", "-r", "--name-only", branch],
            verbosity=self.verbosity,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        # 2022/06/09: witnessed the above line returning no files several
        # times in an ElectionData repo where I was debugging things. So
        # it could be real or perhaps a false one. Regardless adding an
        # test condition in that if there is no file to merge, there is no
        # file to merge - pass.
        if not contest_file:
            logging.error(
                "Error - 'git diff-tree --no-commit-d -r --name-only %s' returned no files."
                "  Skipping",
                branch,
            )
            return
        # Merge the branch / file.  Note - there will always be a conflict
        # so this command will always return non zero
        Shellout.run(
            ["git", "merge", "--no-ff", "--no-commit", branch],
            printonly=self.printonly,
            verbosity=self.verbosity,
        )
        # ZZZ - replace this with an run-time cryptographic value
        # derived from the run-time election private key (diffent from
        # the git commit run-time value).  This will basically slam
        # the contents of the contest file to a second runtime digest
        # (the first one being contained in the commit itself).
        result = Shellout.run(
            ["openssl", "rand", "-base64", "48"],
            verbosity=self.verbosity,
            capture_output=True,
            text=True,
            check=True,
        )
        if result.stdout == "":
            raise ValueError("'openssl rand' should never return an empty string")
        if not self.printonly:
            # ZZZ need to convert the digest to json format ...
            with open(contest_file, "w", encoding="utf8") as outfile:
                # Write a runtime digest as the actual contents of the
                # merge
                outfile.write(str(result.stdout))
        # Force the git add just in case
        Shellout.run(
            ["git", "add", contest_file],
            printonly=self.printonly,
            verbosity=self.verbosity,
            check=True,
        )
        # Note - apparently git place the commit msg on STDERR - hide it
        Shellout.run(
            ["git", "commit", "-m", "auto commit - thank you for voting"],
            printonly=self.printonly,
            verbosity=1,
            check=True,
        )
        Shellout.run(["git", "push", "origin", "main"], self.printonly, check=True)
        # Delete the local and remote branch if this is a local branch
        if not remote:
            Shellout.run(
                ["git", "push", "origin", "-d", branch],
                printonly=self.printonly,
                verbosity=self.verbosity,
                check=True,
            )
            Shellout.run(
                ["git", "branch", "-d", branch],
                printonly=self.printonly,
                verbosity=self.verbosity,
                check=True,
            )
        else:
            # otherwise just delete the remote
            Shellout.run(
                ["git", "push", "origin", "-d", branch.removeprefix("origin/")],
                printonly=self.printonly,
                verbosity=self.verbosity,
                check=True,
            )

    # pylint: disable=too-many-arguments
    def randomly_merge_contests(
        self, uid: str, batch: list, minimum_cast_cache: int, flush: bool, remote: bool
    ):
        """
        Will randomingly select (len(batch) - BALLOT_RECEIPT_ROWS) contest
        branches from the supplied list of branch and merge them to the
        main branch.

        This is the git merge-to-main sequence.
        """
        if len(batch) <= minimum_cast_cache:
            if flush:
                count = len(batch)
            else:
                logging.info(
                    "Contest %s not merged - only %s available", uid, len(batch)
                )
                return 0
        else:
            count = len(batch) - minimum_cast_cache
        loop = count
        logging.info("Merging %s contests for contest %s", count, uid)
        while loop:
            pick = random.randrange(len(batch))
            branch = batch[pick]
            self.merge_contest_branch(branch, remote)
            # End of loop maintenance
            del batch[pick]
            loop -= 1
        logging.debug("Merged %s %s contests", count, uid)
        return count

    def run(
        self,
        branch: str = "",
        flush: bool = False,
        remote: bool = False,
        minimum_cast_cache: int = 100,
    ):
        """Main function - see -h for more info"""

        # Create a VTP ElectionData object if one does not already exist
        the_election_config = ElectionConfig.configure_election(self.election_data_dir)

        # Set the three EV's
        os.environ["GIT_AUTHOR_DATE"] = "2022-01-01T12:00:00"
        os.environ["GIT_COMMITTER_DATE"] = "2022-01-01T12:00:00"
        os.environ["GIT_EDITOR"] = "true"

        # For best results (so to use the 'correct' git submodule or
        # tranverse the correct symlink or not), use the CWD as when
        # accepting the ballot (accept_ballot.py).
        merged = 0
        with Shellout.changed_cwd(
            os.path.join(
                the_election_config.get("git_rootdir"),
                self.election_data_dir,
            )
        ):
            # So, the CWD in this block is the state/town subfolder
            # Pull the remote
            Shellout.run(
                ["git", "pull"],
                printonly=self.printonly,
                verbosity=self.verbosity,
                check=True,
            )
            if branch:
                self.merge_contest_branch(branch, remote)
                logging.info("Merged '%s'", branch)
                return
            # Get the pending CVR branches
            cmds = ["git", "branch"]
            cvr_regex = f"{Globals.get('CONTEST_FILE_SUBDIR')}/([^/]+?)/"
            if remote:
                cmds.append("-r")
                cvr_regex = "^origin/" + cvr_regex
            else:
                cvr_regex = "^" + cvr_regex
            # Note - the re.search will strip non CVRs lines
            cvr_branches = [
                branch.strip()
                for this_branch in Shellout.run(
                    cmds,
                    verbosity=self.verbosity,
                    check=True,
                    capture_output=True,
                    text=True,
                ).stdout.splitlines()
                if re.search(cvr_regex, this_branch.strip())
            ]
            # Note - sorted alphanumerically on contest UID. Loop over
            # contests and randomly merge extras
            batch = []  # if ordered_set was native would probably use that
            current_uid = "-1"
            for this_branch in cvr_branches:
                uid = re.search(cvr_regex, this_branch).group(1)
                if current_uid == uid:
                    batch.append(this_branch)
                    continue
                # Since cvr_branches is ordered, when there is a new uid
                # that does not match the current_uid then try to merge
                # that contest uid set of branched.  Also try to merge the
                # batch if this is the final iteration of the loop.
                if current_uid:
                    # see if previous batch can be merged
                    merged += self.randomly_merge_contests(
                        uid=current_uid,
                        batch=batch,
                        flush=flush,
                        remote=remote,
                        minimum_cast_cache=minimum_cast_cache,
                    )
                # Start a new next batch
                current_uid = uid
                batch = [this_branch]
            if batch:
                # Always try to merge the remaining batch
                merged += self.randomly_merge_contests(
                    uid=current_uid,
                    batch=batch,
                    flush=flush,
                    remote=remote,
                    minimum_cast_cache=minimum_cast_cache,
                )
        logging.info("Merged %s contest branches", merged)

    # End Of Class


# EOF
