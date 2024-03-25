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
Logic of operation for merging contests.  Contests are merged when the
CVR branch is merged to main.  Note that the original commit digest
for the CVR stays intact in a Merkle tree sense.
"""

# Standard imports
import os
import random
import re

# Project import
from vtp.core.common import Globals
from vtp.core.election_config import ElectionConfig

# Local imports
from .operation import Operation


class MergeContestsOperation(Operation):
    """
    A class to implememt the merge-contests operation.  See the
    merge-contests help output or read the parse_argument argparse
    description (immediately below this) in the source file.
    """

    def merge_receipt_branch(self, branch: str, remote: bool):
        """Merge a specific receipt branch"""
        # This command is duplicate from merge_receipt_branch below
        contest_file = self.shell_out(
            ["git", "diff-tree", "--no-commit-id", "-r", "--name-only", branch],
            incoming_printlevel=True,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        # This command is duplicate from merge_receipt_branch below
        if not contest_file:
            self.imprimir(
                "(receipt) 'git diff-tree --no-commit-d -r --name-only "
                f"{branch}' returned no files.  Skipping",
                1,
            )
            return
        # For receipts the content stays intact AND the branch is
        # unique, so there should never be a conflict on the branch -
        # it should always successfully auto-merge as there are not
        # file overlaps.
        self.shell_out(["git", "merge", branch], incoming_printlevel=5)
        self.shell_out(
            ["git", "push", "origin", "main"], check=True, incoming_printlevel=5
        )
        # Delete the local and remote branch if this is a local branch
        if not remote:
            self.shell_out(
                ["git", "push", "origin", "-d", branch],
                check=True,
                incoming_printlevel=5,
            )
            self.shell_out(
                ["git", "branch", "-d", branch],
                check=True,
                incoming_printlevel=5,
            )
        else:
            # otherwise just delete the remote
            self.shell_out(
                ["git", "push", "origin", "-d", branch.removeprefix("origin/")],
                check=True,
                incoming_printlevel=5,
            )

    def merge_contest_branch(self, branch: str, remote: bool):
        """Merge a specific contest branch"""
        # If the VTP server is processing contests from different
        # voting centers, then the contest.json could be in different
        # locations on different branches.
        contest_file = self.shell_out(
            ["git", "diff-tree", "--no-commit-id", "-r", "--name-only", branch],
            incoming_printlevel=True,
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
            self.imprimir(
                "(contest) 'git diff-tree --no-commit-d -r --name-only "
                f"{branch}' returned no files.  Skipping",
                1,
            )
            return
        # Merge the branch / file.  Note - for contests there will
        # always be a conflict so this command will always return non
        # zero
        self.shell_out(
            ["git", "merge", "--no-ff", "--no-commit", branch],
            incoming_printlevel=5,
        )
        # ZZZ - replace this with an run-time cryptographic value
        # derived from the run-time election private key (diffent from
        # the git commit run-time value).  This will basically slam
        # the contents of the contest file to a second runtime digest
        # (the first one being contained in the commit itself).
        result = self.shell_out(
            ["openssl", "rand", "-base64", "48"],
            incoming_printlevel=True,
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
        self.shell_out(
            ["git", "add", contest_file],
            check=True,
            incoming_printlevel=5,
        )
        # Note - apparently git places the commit msg on STDERR - hide it
        if not self.printonly:
            self.imprimir(
                "Running \"git commit -m 'auto commit - thank you for voting'\"",
                4,
            )
        self.shell_out(
            ["git", "commit", "-m", "auto commit - thank you for voting"],
            check=True,
            incoming_printlevel=5,
        )
        self.shell_out(
            ["git", "push", "origin", "main"], check=True, incoming_printlevel=5
        )
        # Delete the local and remote branch if this is a local branch
        if not remote:
            self.shell_out(
                ["git", "push", "origin", "-d", branch],
                check=True,
                incoming_printlevel=5,
            )
            self.shell_out(
                ["git", "branch", "-d", branch],
                check=True,
                incoming_printlevel=5,
            )
        else:
            # otherwise just delete the remote
            self.shell_out(
                ["git", "push", "origin", "-d", branch.removeprefix("origin/")],
                check=True,
                incoming_printlevel=5,
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
                self.imprimir(
                    f"Contest {uid} not merged - only {len(batch)} available",
                    3,
                )
                return 0
        else:
            count = len(batch) - minimum_cast_cache
        loop = count
        self.imprimir(f"Merging {count} contests for contest {uid}", 4)
        while loop:
            pick = random.randrange(len(batch))
            branch = batch[pick]
            self.merge_contest_branch(branch, remote)
            # End of loop maintenance
            del batch[pick]
            loop -= 1
        self.imprimir(f"Merged {count} {uid} contests", 4)
        return count

    # pylint: disable=duplicate-code
    def run(
        self,
        branch: str = "",
        flush: bool = False,
        remote: bool = False,
        minimum_cast_cache: int = 100,
        style: str = "contest",
    ):
        """
        Main function - see -h for more info.  Note that the merge
        operation is subtly different depending on whether remote is
        False or True.

        If False, that implies a git workspace that contains the
        (local) branch, and both the local and remote branch will be
        deleted when the merge-to-main occurs.

        If True, there is no local branch (since the merge direction
        is from the specified branch to the main branch which is the
        branch that has been locally checkout'ed) and in this case
        only the remote branch needs to be deleted.  Note that the
        actual branch specification in this case contains an 'origin/'
        prefix which needs to be stripped as git nominally does not
        want that when deleting remote branches.
        """

        # Create a VTP ElectionData object if one does not already exist
        the_election_config = ElectionConfig.configure_election(
            self,
            self.election_data_dir,
        )

        # Set the three EV's
        os.environ["GIT_AUTHOR_DATE"] = Globals.get("ELECTION_DATETIME")
        os.environ["GIT_COMMITTER_DATE"] = Globals.get("ELECTION_DATETIME")
        os.environ["GIT_EDITOR"] = "true"

        # For best results (so to use the 'correct' git submodule or
        # tranverse the correct symlink or not), use the CWD as when
        # accepting the ballot (accept_ballot.py).
        merged = 0
        with self.changed_cwd(the_election_config.get("git_rootdir")):
            # So, the CWD in this block is the state/town subfolder
            # Pull the remote
            self.shell_out(
                ["git", "pull"],
                check=True,
                incoming_printlevel=5,
            )
            if branch:
                if style == "contest":
                    self.merge_contest_branch(branch, remote)
                else:
                    self.merge_receipt_branch(branch, remote)
                self.imprimir(f"Merged '{branch}'", 4)
                return
            # Get the pending CVR branches
            cmds = ["git", "branch"]
            cvr_regex = f"{Globals.get('CONTEST_FILE_SUBDIR')}/([^/]+?)/"
            if remote:
                cmds.append("-r")
                cvr_regex = "^origin/" + cvr_regex
            else:
                cvr_regex = "^" + cvr_regex
            # Note - the re.search will strip non CVRs lines, and then
            # after that each result is strip'ed
            cvr_branches = [
                this_branch.strip()
                for this_branch in self.shell_out(
                    cmds,
                    incoming_printlevel=True,
                    check=True,
                    capture_output=True,
                    text=True,
                ).stdout.splitlines()
                if re.search(cvr_regex, this_branch.strip())
            ]
            #            import pdb; pdb.set_trace()
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
                if current_uid != "-1":
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
        self.imprimir(f"Merged {merged} contest branches", 3)


# EOF
