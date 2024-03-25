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

"""Base class of operations."""

# standard imports
import json
import os
import re
import subprocess
from contextlib import contextmanager

# local imports
from vtp.core.common import Common, Globals


# pylint: disable=too-few-public-methods
class Operation:
    """
    Generic operation base class constructor - covers
    election_data_dir, guid, verbosity, and printonly.  Also will
    configure (global) logging and validate the existance of
    election_data_dir.
    """

    # class constants
    _sha1_regex = re.compile(r"([0-9a-fA-F]{40})")

    # Mmm, there should only really be one instance of Operation and not
    # multiple, so create a singleton class
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        election_data_dir: str = "",
        verbosity: int = 3,
        printonly: bool = False,
        stdout_printing: bool = True,
        style: str = "text",
    ):
        self.election_data_dir = election_data_dir
        self.printonly = printonly
        self.verbosity = verbosity
        self.style = style

        # Design note: originally the logging package was used,  But custom
        # output was added without retiring logging.  And then having two
        # systems became a problem, and the logging package was dropped.

        # The verbosity levels:
        #     0: ALWAYS    - always print the line
        #     1: ERROR     - [ERROR]    is prepended to the line
        #     2: WARNING   - [WARNING]  is prepended to the line
        #     3: INFO      - minimal info
        #     4: VERBOSE   - more info
        #     5: DEBUG     - everything

        # Validate the election_data_dir arg here and now
        Common.verify_election_data_dir(self.election_data_dir)
        # Configure printing
        self.stdout_printing = stdout_printing
        if style == "html":
            self.stdout_output = ["<p>"]
        else:
            self.stdout_output = []

    def imprimir(self, a_line: str, incoming_printlevel: int = 3):
        """Either prints a line of text to STDOUT or appends it to a list,
        in which case the output needs to be retrieved.  If the second
        argument is less than or equal to self.verbosity, the line prints.
        The default self.verbosity is 3."""
        if incoming_printlevel <= self.verbosity:
            if self.style == "html":
                # If self.style == "html", html-ize the line
                # - add digest links for digests
                # - add line breaks per line
                # - convert an array to a table with css class=imprimir
                # ZZZ
                #                import pdb; pdb.set_trace()
                a_line = Operation._sha1_regex.sub(
                    r'<a href="foo/\1" target="_blank">\1</a>', a_line
                )
                match incoming_printlevel:
                    case 1:
                        a_line = '<span class="error">[ERROR] </span>' + a_line
                    case 2:
                        a_line = '<span class="warning">[WARNING] </span>' + a_line
            else:
                match incoming_printlevel:
                    case 1:
                        a_line = "[ERROR] " + a_line
                    case 2:
                        a_line = "[WARNING] " + a_line
            if self.stdout_printing:
                print(a_line)
            else:
                self.stdout_output.append(a_line)

    def get_imprimir(self) -> list:
        """Return the stored output string"""
        return self.stdout_output

    # The below were oringally in the Shellout package

    def shell_out(
        self,
        argv: list,
        no_touch_stds: bool = False,
        printonly_override: bool = False,
        verbosity_override: int = -1,
        **kwargs,
    ):
        """Run a shell command with logging and error handling.
        Raises a CalledProcessError if the shell command fails - the
        caller needs to deal with that.  Can also raise a
        TimeoutExpired exception.

        Nominally returns a CompletedProcess instance.

        See for example
        https://docs.python.org/3.9/library/subprocess.html

        If printonly_override is True, then self.printonly is ignored.
        If verbosity_override is not -1 ([0-5]), then self.verbsoity
        is ignored.
        """
        verbosity = verbosity_override if verbosity_override != -1 else self.verbosity
        # Note - it is ok to pass ints and floats down through argv
        # here, but they need to be individually converted to strings
        # regardless since _everything_ below wants to see strings.
        argv_string = [str(arg) for arg in argv]
        self.imprimir(f'Running ({" ".join(argv_string)})', 5)
        if self.printonly and not printonly_override:
            return subprocess.CompletedProcess(argv_string, 0, stdout="", stderr="")
        # the caller decides on whether check is set or not
        # pylint: disable=subprocess-run-check
        if not no_touch_stds:
            if "capture_output" not in kwargs:
                if "stdout" not in kwargs and verbosity > 4:
                    kwargs["stdout"] = subprocess.DEVNULL
                if "stderr" not in kwargs and verbosity > 4:
                    kwargs["stderr"] = subprocess.DEVNULL
        if "timeout" not in kwargs:
            kwargs["timeout"] = Globals.get("SHELL_TIMEOUT")
        #        import pdb; pdb.set_trace()
        return subprocess.run(argv_string, **kwargs)

    @contextmanager
    def changed_cwd(self, path: str):
        """Context manager for temporarily changing the CWD"""
        oldpwd = os.getcwd()
        try:
            os.chdir(path)
            self.imprimir(f"Entering dir ({path})", 5)
            yield
        finally:
            os.chdir(oldpwd)
            self.imprimir(f"Leaving dir ({path})", 5)

    @contextmanager
    def changed_branch(self, branch: str):
        """
        Context manager for temporarily encapsulating a potential git
        branch change.  Will explicitly switch to the specified branch
        before yielding.
        """
        self.shell_out(["git", "checkout", branch], check=True, verbosity_override=5)
        self.imprimir(f"Entering branch ({branch})", 5)
        try:
            yield
        finally:
            # switch the branch back
            self.shell_out(
                ["git", "checkout", branch], check=True, verbosity_override=5
            )
            self.imprimir(f"Leaving branch ({branch})", 5)

    # ZZZ - could use an optional filter_by_uid argument which is a set object
    def cvr_parse_git_log_output(
        self,
        git_log_command: list,
        election_config: dict,
        grouped_by_uid: bool = True,
        verbosity_override: int = -1,
    ):
        """Will execute the supplied git log command and process the
        output of those commits that are CVRs.  Will return a
        dictionary keyed on the contest UID that is a list of CVRs.
        The CVR is just the CVR from the git log with a 'digest' key
        added.

        Note the the order of the list is git log order and not
        randomized FWIIW.
        """
        # Will process all the CVR commits on the main branch and tally
        # all the contests found.
        git_log_cvrs = {}
        with self.changed_cwd(election_config.get("git_rootdir")):
            self.imprimir(f'Running ({" ".join(git_log_command)})', verbosity_override)
            with subprocess.Popen(
                git_log_command, stdout=subprocess.PIPE, text=True, encoding="utf8"
            ) as git_output:
                # read lines until there is a complete json object, then
                # add the object for that contest.
                block = ""
                digest = ""
                recording = False
                # question - how to get "for line in
                # git_output.stdout.readline():" not to effectively return
                # the characters in line as opposed to the entire line
                # itself?
                while True:
                    line = git_output.stdout.readline()
                    if not line:
                        break
                    if match := re.match("^([a-f0-9]{40}){", line):
                        digest = match.group(1)
                        recording = True
                        block = "{"
                        continue
                    if recording:
                        block += line.strip()
                        if re.match("^}", line):
                            # this loads the contest under the CVR key
                            cvr = json.loads(block)
                            if grouped_by_uid:
#                                import pdb; pdb.set_trace()
                                cvr["digest"] = digest
                                if cvr["contestCVR"]["uid"] in git_log_cvrs:
                                    git_log_cvrs[cvr["contestCVR"]["uid"]].append(cvr)
                                else:
                                    git_log_cvrs[cvr["contestCVR"]["uid"]] = [cvr]
                            else:
                                git_log_cvrs[digest] = cvr
                            block = ""
                            digest = ""
                            recording = False
        return git_log_cvrs
