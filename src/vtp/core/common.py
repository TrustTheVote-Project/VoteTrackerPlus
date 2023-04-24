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

# standard imports
import json
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
        # Default runtime location of everything
        "DEFAULT_RUNTIME_LOCATION": "/opt/VoteTrackerPlus/demo.01",
    }

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
    def verify_election_data_dir(election_data_dir: str):
        """
        Verify that election_data_dir is an existing directory.
        """
        if not os.path.isdir(election_data_dir):
            raise ValueError(
                f"The provided --election_data value ({election_data_dir}) does not exist"
            )

    @staticmethod
    def get_generic_ro_edf_dir() -> str:
        """
        Will return a generic EDF workspace so to be able to execute
        generic/readonly commands.  It is 'readonly' because any
        number of processes could be executing in this one git
        workspace at the same time and if any them wrote anything, it
        would be bad.
        """
        edf_path = os.path.join(
            Globals.get("DEFAULT_RUNTIME_LOCATION"),
            Globals.get("MOCK_CLIENT_DIRNAME"),
            "scanner.00",
        )
        # Need to verify that there is only _one_ directory in the edf_path
        dirs = [
            name
            for name in os.listdir(edf_path)
            if os.path.isdir(os.path.join(edf_path, name))
        ]
        if len(dirs) > 1:
            raise ValueError(
                f"The mock client directory ({edf_path}) ",
                "contains multiple subdirs - there can only be one ",
                "as there should only be one EDF clone in this directory",
            )
        if not dirs:
            raise ValueError(
                f"The mock client directory ({edf_path}) ",
                "is empty - there needs to be exactly one git clone ",
                "of a ElectionData repo",
            )
        return os.path.join(edf_path, dirs[0])

    @staticmethod
    def get_guid_based_edf_dir(guid: str) -> str:
        """
        Return the default runtime location for a guid based
        workspace.  The actual ElectionData clone directory can be
        named anything.  HOWEVER it is assumed (REQUIRED) that there
        is only one clone in this directory, which is reasonable given
        that the whole tree from '/' is nominally created by the
        setup-vtp-demo operation.
        """
        if len(guid) != 40:
            raise ValueError(f"The provided guid ({guid}) is not 40 characters long")
        if not re.match("^[0-9a-f]+$", guid):
            raise ValueError(
                f"The provided guid ({guid}) contains characters other than [0-9a-f]"
            )
        edf_path = os.path.join(
            Globals.get("DEFAULT_RUNTIME_LOCATION"),
            Globals.get("GUID_CLIENT_DIRNAME"),
            guid[:2],
            guid[2:],
        )
        # Need to verify that the _only_ directory in edf_path is a
        # valid EDF tree via some clone
        dirs = [
            name
            for name in os.listdir(edf_path)
            if os.path.isdir(os.path.join(edf_path, name))
        ]
        if len(dirs) > 1:
            raise ValueError(
                f"The provided guid ({guid}) based path ({edf_path}) ",
                "contains multiple subdirs - there can only be one",
            )
        if not dirs:
            raise ValueError(
                f"The guid directory ({edf_path}) ",
                "is empty - there needs to be exactly one git clone ",
                "of a ElectionData repo",
            )
        return os.path.join(edf_path, dirs[0])


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
        with Shellout.changed_cwd(election_config.get("git_rootdir")):
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
