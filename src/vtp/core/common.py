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

"""A kitchen sync for VTP classes for the moment"""

# pylint: disable=too-few-public-methods
import json

#  Other imports:  critical, error, warning, info, debug
import logging
import os
import re
import subprocess
import sys
from contextlib import contextmanager


class Globals:
    """
    A placeholder for python code constants, not to be confused with VTP
    election tree constants which are located in the config.yaml files.
    """

    # ZZZ - apparently the pythonic way to make these read only is to
    # change them to properties.  For now have no setters.
    _config = {
        # The default location from the CWD of this program, which is different than
        # The location of the incoming ballot.json file etc
        "BALLOT_FILE": "ballot.json",
        "CONTEST_FILE": "contest.json",
        "RECEIPT_FILE": "receipt.csv",
        # The blank ballot folder location
        "BLANK_BALLOT_SUBDIR": "blank-ballots",
        # The location/name of the config and address map files for this GGO
        "CONFIG_FILE": "config.yaml",
        "ADDRESS_MAP_FILE": "address_map.yaml",
        # The location of the contest cvr file
        "CONTEST_FILE_SUBDIR": "CVRs",
        # The required address fields for an address. To get around
        # the difficulty of creating a completely generic
        # address-to-ballot function at this time, these fields are
        # broken into two types.  The first ordered set goes from the
        # root ElectionData node to the lowest leaf level node where
        # the GGO boundaries are required to be coherent (perfectly
        # the same).  The second set optionally continues until there
        # are no more leaf nodes.  This is arbitrary but the current
        # address-to-ballot implemention below is based on this.  In
        # addtion this decision also is reflected in several other
        # spots as well :-( - sorry.  Basically, the REQUIRED_GGO list
        # is where the CVR and blank ballots are placed.
        "REQUIRED_GGO_ADDRESS_FIELDS": ["state", "town"],
        "REQUIRED_NG_ADDRESS_FIELDS": ["street", "number"],
        # Whether or not VTP has been locally installed
        "VTP_LOCAL_INSTALL": True,
        # The Root/Parent Election Data directory.  As of 2022/10/17
        # this repo is a submodule of the root election repo (which
        # used to be a sibling symlink named ElectionData) with
        # python's sys.path being one level above this utils directory
        # for the scripts placed there.  Independent of the python
        # sys.path gyrations, this repo is still one level below the
        # outer most root/parent election repo.  Hence, one set of
        # '..' here since git commands are using this.  As of
        # 2023/01/19 and post the local install idiom, one can be
        # anywhere to run VTP commands, so might as well be at the
        # root of the ElectionData repo ...
        "ROOT_ELECTION_DATA_SUBDIR": ".",
        # Where the bin directory is relative from the root of _this_ repo
        "BIN_DIR": "src/vtp",
        # How long to wait for a git shell command to complete - maybe a bad idea
        "SHELL_TIMEOUT": 15,
        # Number of ballots on a ballot receipt
        "BALLOT_RECEIPT_ROWS": 100,
        # Map the ElectionConfig 'kind' to the Address 'kind'
        "kinds_map": {
            "state": "states",
            "town": "towns",
            "county": "counties",
            "SchoolDistrict": "SchoolDistricts",
            "CouncilDistrict": "CouncilDistricts",
            "Precinct": "Precincts",
        },
        # Note - all three of the following folders hold git repos
        # where the remote is a bare clone of the upstream/remote
        # GitHub ElectionData repo. In an attempt at clarity, the word
        # 'workspace' here refers to a non bare repo, 'upstream' is
        # the parent repo, and 'remote' means non-local to this
        # computer (requires a TPC/IP connection to get to).
        # The subdirectory where the FastAPI connection git workspaces are stored
        "GUID_CLIENT_DIRNAME": "guid-client-store",
        # The subdirectory where the local tabulation git workspace is stored
        "TABULATION_SERVER_DIRNAME": "tabulation-server",
        # The subdirectory where the mock scanner git workspaces are stored
        "MOCK_CLIENT_DIRNAME": "mock-clients",
    }

    # Legitimate setters
    @staticmethod
    def set_electiondatadir(path: str):
        """Will overwrite the default location of the ElectionData tree"""
        Globals._config["ROOT_ELECTION_DATA_SUBDIR"] = path

    @staticmethod
    def get(name):
        """A generic getter"""
        return Globals._config[name]


class Common:
    """Common functions without a better home at this time"""

    # logging should only be configured once and only once (until a
    # logger is set up)
    _configured = False

    @staticmethod
    def configure_logging(verbosity):
        """How VTP is (currently) using logging"""
        if Common._configured:
            return
        verbose = {
            0: logging.CRITICAL,
            1: logging.ERROR,
            2: logging.WARNING,
            3: logging.INFO,
            4: logging.DEBUG,
        }
        logging.basicConfig(
            format="%(message)s",
            level=verbose[verbosity],
            stream=sys.stdout,
        )
        Common._configured = True

    @staticmethod
    def cast_thing_to_list(argv):
        """Primarly used by the argparse function in the operation classes"""
        if isinstance(argv, dict):
            new_argv = []
            for key, value in argv.items():
                if isinstance(value, bool):
                    if value:
                        new_argv.append("--" + key)
                elif value is not None:
                    new_argv.extend(["--" + key, str(value)])
            return new_argv
        return argv

    # Tbe below are options that are shared across the various
    # operations.  Options that are unique to one operation are
    # located in that file.

    @staticmethod
    def add_blank_ballot(parser):
        """Add blank_ballot option"""
        parser.add_argument(
            "--blank_ballot",
            help="overrides an address - specifies the specific blank ballot",
        )

    @staticmethod
    def add_election_data_dir(parser):
        """Add election_data option"""
        defval = Globals.get("ROOT_ELECTION_DATA_SUBDIR")
        parser.add_argument(
            "-e",
            "--election_data_dir",
            default=defval,
            help=f"specify a absolute or relative path to the ElectionData tree (def={defval})",
        )

    @staticmethod
    def add_merge_contests(parser):
        """Add merge_contests option"""
        parser.add_argument(
            "-m",
            "--merge_contests",
            action="store_true",
            help="Will immediately merge the ballot contests (to main)",
        )

    @staticmethod
    def add_minimum_cast_cache(parser):
        """Add minimum_cast_cache option"""
        parser.add_argument(
            "--minimum_cast_cache",
            type=int,
            default=100,
            help="the minimum number of cast ballots required prior to merging (def=100)",
        )

    @staticmethod
    def add_printonly(parser):
        """Add printonly option"""
        parser.add_argument(
            "-n",
            "--printonly",
            action="store_true",
            help="will printonly and not write to disk (def=True)",
        )

    @staticmethod
    def add_verbosity(parser):
        """Add verbosity option"""
        parser.add_argument(
            "-v",
            "--verbosity",
            type=int,
            default=3,
            help="0 critical, 1 error, 2 warning, 3 info, 4 debug (def=3)",
        )

    @staticmethod
    def verify_election_data_dir(election_data_dir: str):
        """
        Verify election_data option.  Note that global constant
        ROOT_ELECTION_DATA_SUBDIR is a default value while the actual
        live election_data_dir value is stored in an upstream ops
        object.
        """
        if not os.path.isdir(election_data_dir):
            raise ValueError(
                f"The provided --election_data value ({election_data_dir}) does not exist"
            )


# pylint: disable=too-few-public-methods   # ZZZ - remove this later
class Shellout:
    """
    A class to wrap the control & management of shell subprocesses,
    nominally git commands.
    """

    @staticmethod
    def get_script_name(script, the_election_config):
        """
        Given a python script name, either return the poetry local
        install name or the relative path from the default execution
        CWD.
        """
        if Globals.get("VTP_LOCAL_INSTALL"):
            return re.sub("_", "-", script).rstrip(".py")
        return os.path.join(
            the_election_config.get("git_rootdir"), Globals.get("BIN_DIR"), script
        )

    @staticmethod
    def run(argv, printonly=False, verbosity=3, no_touch_stds=False, **kwargs):
        """Run a shell command with logging and error handling.  Raises a
        CalledProcessError if the shell command fails - the caller needs to
        deal with that.  Can also raise a TimeoutExpired exception.

        Nominally returns a CompletedProcess instance.

        See for example https://docs.python.org/3.9/library/subprocess.html
        """
        # Note - it is ok to pass ints and floats down through argv
        # here, but they need to be individually converted to strings
        # regardless since _everything_ below wants to see strings.
        argv_string = [str(arg) for arg in argv]
        if verbosity >= 3:
            logging.info('Running "%s"', " ".join(argv_string))
        if printonly:
            return subprocess.CompletedProcess(argv_string, 0, stdout="", stderr="")
        # the caller desides on whether check is set or not
        # pylint: disable=subprocess-run-check
        if not no_touch_stds:
            if "capture_output" not in kwargs:
                if "stdout" not in kwargs and verbosity < 3:
                    kwargs["stdout"] = subprocess.DEVNULL
                if "stderr" not in kwargs and verbosity <= 3:
                    kwargs["stderr"] = subprocess.DEVNULL
        if "timeout" not in kwargs:
            kwargs["timeout"] = Globals.get("SHELL_TIMEOUT")
        return subprocess.run(argv_string, **kwargs)

    @staticmethod
    @contextmanager
    def changed_cwd(path):
        """Context manager for temporarily changing the CWD"""
        oldpwd = os.getcwd()
        try:
            os.chdir(path)
            logging.debug("Entering dir (%s):", path)
            yield
        finally:
            os.chdir(oldpwd)
            logging.debug("Leaving dir (%s):", path)

    @staticmethod
    @contextmanager
    def changed_branch(branch):
        """
        Context manager for temporarily encapsulating a potential git
        branch change.  Will explicitly switch to the specified branch
        before yielding.
        """
        Shellout.run(["git", "checkout", branch], check=True)
        logging.debug("Entering branch (%s):", branch)
        try:
            yield
        finally:
            # switch the branch back
            Shellout.run(["git", "checkout", branch], check=True)
            logging.debug("Leaving branch (%s):", branch)

    @staticmethod
    # ZZZ - could use an optional filter_by_uid argument which is a set object
    def cvr_parse_git_log_output(
        git_log_command, election_config, grouped_by_uid=True, verbosity=3
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
        with Shellout.changed_cwd(
            os.path.join(
                election_config.get("git_rootdir"),
                Globals.get("ROOT_ELECTION_DATA_SUBDIR"),
            )
        ):
            if verbosity >= 3:
                logging.info('Running "%s"', " ".join(git_log_command))
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
                                cvr["digest"] = digest
                                if cvr["CVR"]["uid"] in git_log_cvrs:
                                    git_log_cvrs[cvr["CVR"]["uid"]].append(cvr)
                                else:
                                    git_log_cvrs[cvr["CVR"]["uid"]] = [cvr]
                            else:
                                git_log_cvrs[digest] = cvr
                            block = ""
                            digest = ""
                            recording = False
        return git_log_cvrs


# EOF
