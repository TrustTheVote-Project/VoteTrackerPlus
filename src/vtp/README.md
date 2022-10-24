# VoteTracker+ Development and Usage

This is a work in progress and may not be completely up-to-date.

## 1) Terminology

For basic terminology see the [NIST](https://pages.nist.gov/ElectionGlossary/) glossary page.

VoteTracker+ (VTP) URL's and PATH references have the '+' spelled out (VoteTrackerPlus).

See [../docs/project-overview.md](../docs/project-overview.md) for more general VTP information.  In particular see [../../docs/project-overview.md](../../docs/tech-details/more-tech-details.md) for details of the VTP election directory layout.  The directory layout is key to better understand the VoteTracker+ solution and how election data is organized the directory, file, and git repository levels.

A VTP election in essence is the directory structure that represents a specific election.  The directory structure is rooted with a clone of a root election repository, representing either a real or mock election, that contains this repository as a direct submodule.  The election may have zero or more additional git submodules organized in a specific manner, primarily a function of voting precinct and/or computer network isolation.  One potentially common layout/deployment is one git repo per voting center.

This repo contains all the python executables and libraries necessary to run an election and does not contain any election specific information, configuration or [Cast Vote Records (CVRs)](https://pages.nist.gov/ElectionGlossary/#cast-vote-record).

When a specific election is configured, either for real or for mock/testing purposes, the ./config.yaml and ./address_map.yaml files in the election repositories are modified accordingly.  This initial modification will define Geographical Geopolitical Overlays (GGOs - NIST calls this a [geopolitical units](https://pages.nist.gov/ElectionGlossary/#geopolitical-unit)).  More specifically, the config and address-map files define the direct child GGOs (there can be multiple children), and those children config and address-map files define their potentially multiple children.  This effectively define an Directed Acyclic Graph (DAG) of election configuration data.

The GGO based DAG election data can also more or less arbitrarily span git submodules.  The git submodule splitting occurs when election official define a specific physical location in which VTP will be processing ballots __and__ when that location needs to scan the ballots or be able to scan the ballots disconnected network wise from other VTP locations.   A git submodule allows a voting center to operate without network connectivity with other VTP locations.  The election configuration DAG and the git submodule tree, which is also a DAG, need not be the same tree/graph.

Also, though disconnected network wise, each VTP location processes ballots with a full and complete distributed copy of all the VTP repos that comprise the election.

In summary, to create a VTP election configuration is to create these yaml files and git submodules either from scratch or to import/merge them from a previous or similar election.  Once imported/merged they can be updated and modified.  And once imported, the unit, functional, and mock election tests can be run locally as they are always executed as part of the VTP development process as part of the GitHub devsecops infrastructure.

## 2) Background and Caveats

The VoteTracker+ project with respect to executable programs currently consists of a handfull of python scripts in this directory and a few libraries in the utils subdirectory.  To run these scripts simply cd into this directory and run them.  Running them from other directories within this git repo in theory may work but is not tested.

It is important that the end-voter usage model be as simple as possible and as immune as possible to false narratives and conspiracy theories.  A primary goal of VoteTracker+ is election and ballot trustworthiness.  As such a design goal of VoteTracker+ is that this git repo along with the various git submodules will comprise a specific election, statically, both in terms of code __and__ election configuration data  __including__ all the [Cast Vote Records (CVRs)](https://pages.nist.gov/ElectionGlossary/#cast-vote-record).  By avoiding a python installation step the end-user (the end-voter) usage model is simplified while also minimizing the potential attack surface.  The intent is that the end-voter can clone this repo and with no further installation run the commands located here as is, with as little mystery as possible from the point of view of someone with no software coding experience.  An entire VTP election tree is relocatable, reclone-able tree of files.  Only the python environment itself needs to be installed.

Therefor, there is no setup.py file for this project as there is no __pip install votetracker+__ or similar installation step.  As there is no VTP installation step, tests are run directly via pylint and  pytest and not via tox.  It is important that end-voters can also run the all the VTP tests on their computers.

Currently both poetry and conda/miniconda python virtual environment frameworks are tested for compatibility.

## 3) Development Process Target Goal

It is a goal to create a development process that eventually includes the following:

- Every commit is signed with a PGP key
- Standard GitHub pull request (PR) development models are in play
- All pull-requests and un-squashed commits pass pylint with at least a 9.9 score
- All pull-requests and un-squashed commits pass pytest
- A TBD level of unit and functional test coverage (pytest coverage)
- A TBD level of mock election test coverage (system testing)

This project is not there yet.

## 4) Current Development Process

The current development process is in flux as the project is still being designed / framed out as code is being written.  This documentation may also be behind the actual code development.

### 4.1) One time python (poetry) environment setup

Currently Votetracker+ is using [poetry](https://python-poetry.org/) as the python package and dependency manager.  The base python is currently 3.9.

```bash
# install poetry (Mac example) - see https://python-poetry.org/docs/ for poetry documentation
$ mkdir repos && cd repos
$ git clone https://github.com/python-poetry/poetry.git
$ cd install.python-poetry.org
$ python3 install-poetry.py
```
Note the [poetry installation](https://python-poetry.org/docs/#installation) directions regarding shell integrations

For conda/miniconda:

```bash
# install conda (Mac example) - download from https://docs.conda.io/en/latest/miniconda.html
$ curl https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -o Downloads/Miniconda3-latest-MacOSX-x86_64.sh

# validate digest
$ openssl sha256 Downloads/Miniconda3-latest-MacOSX-x86_64.sh

# install it - see conda instructions!
$ bash Downloads/Miniconda3-latest-MacOSX-x86_64.sh

# create an python 3.9 environment
$ conda create -n vtp.01 python=3.9
$ conda activate vtp.01
$ conda install pylint pytest pyyaml networkx
$ pip install pyinputplus
```

### 4.2) Clone this repo and an ElectionData repo

```bash
# pull the Votetracker+ project - clone both repositories - and create an ElectionData symlink
$ cd ..
$ git clone --recurse-submodules git@github.com:TrustTheVote-Project/VTP-mock-election.US.10.git
$ cd VTP-mock-election.US.10/
```

Each VTP election data repository, mock or otherwise, represents a different election.  Some repos may be already configured and can be immediately used to run an election, or the repos may be of a past election.  Regardless, to run a real or mock election one will need a usable VTP election data repository.

### 4.3) Create/set the python environment

Poetry:

```bash
$ poetry init
$ poetry shell
```

Conda:

```bash
$ conda activate vtp.01
```

### 4.4) Running a mock election

To run a mock election, run the setup_vtp_demo.py script.  This script will nominally create a mock election with four VTP scanner _apps_ and one VTP local-remote server _app_ as if all ballots were being cast in a single voting center with four separate and independent ballot scanners.  By default it will place the git repos in /opt/VotetrackerPlus with the 5 clients (the four scanner apps and one server app) in the _clients_ folder with the two local git upstream bare repositories in the _local-remote-server_ folder.  The directory tree looks like this:

```
/opt/VotetrackerPlus/demo.01/clients/scanner.00/VTP-mock-election.US.<nn>/VoteTrackerPlus
                                     scanner.01/VTP-mock-election.US.<nn>/VoteTrackerPlus
                                     scanner.02/VTP-mock-election.US.<nn>/VoteTrackerPlus
                                     scanner.03/VTP-mock-election.US.<nn>/VoteTrackerPlus
                                     server/VTP-mock-election.US.<nn>/VoteTrackerPlus
/opt/VotetrackerPlus/demo.01/local-remote-server/VTP-mock-election.US.<nn>.git
                                                 VoteTrackerPlus.git
```

The git repositories in the _clients_ subfolder all have workspaces as that is where the various commands run to simulate an individual ballot scanner application.  The two bare repostitories in local-remote-server mimick the actual voting center local (bare) git remote repositories for both the VTP scanner and server apps.

The basic demo idea is to start a separate __run_mock_election.py -d scanner__ instance in the first three scanner subfolders.  And then in the fourth scanner.04 subfolder manually and interactively cast ballots.  This will simulate a voter at an active voting center.  A VTP server app should be run in the server subfolder.

Here is an example of running a 4 VTP scanner and 1 VTP server app mock demo election.  This simulates an in-person voting center with 4 ballot scanners producing the anonymized ballot checks for the voters.  The first three are submitting random ballots while the fourth someone at the keyboard can manually submit one ballot at a time.

```bash
# In terminal window #1, run a VTP remote-local server
# Note - this assumes the explicit setup steps above - note the poetry pyproject.toml location
$ cd repos/VTP-mock-election.US.10/VoteTrackerPlus
$ poetry shell
$ cd /opt/VotetrackerPlus/demo.01/clients/server/VoteTrackerPlus/src/vtp
$ ./run_mock_election.py -s California -t Alameda -a "123 Main Street" -d server

# In terminal window #2, run a VTP scanner in mock election mode
$ cd repos/VTP-mock-election.US.10/VoteTrackerPlus
$ poetry shell
$ cd /opt/VotetrackerPlus/demo.01/clients/scanner.01/VoteTrackerPlus/src/vtp
# Auto cast 100 random ballots
$ ./run_mock_election.py -s California -t Alameda -a "123 Main Street" -d scanner -i 100

# In terminal window #3, run a second VTP scanner in mock election mode
$ cd repos/VTP-mock-election.US.10/VoteTrackerPlus
$ poetry shell
$ cd /opt/VotetrackerPlus/demo.01/clients/scanner.02/VoteTrackerPlus/src/vtp
# Auto cast 100 random ballots
$ ./run_mock_election.py -s California -t Alameda -a "123 Main Street" -d scanner -i 100

# In terminal window #4, run an interactive VTP scanner to cast ballots
$ cd repos/VTP-mock-election.US.10/VoteTrackerPlus
$ poetry shell
$ cd /opt/VotetrackerPlus/demo.01/clients/scanner.00/VoteTrackerPlus/src/vtp

# To manually vote and cast one ballot, run vote.py.  The receipt.csv will be printed to a file
# and the row offset will be printed to the screen (STDOUT).
$ ./vote.py -s California -t Alameda -a "123 Main Street"
```

The last few lines printed by ./vote.py should look something like this:

```
############
### Receipt file: /opt/VoteTrackerPlus/demo.01/clients/scanner.00/VoteTrackerPlus/ElectionData/GGOs/states/California/GGOs/towns/Alameda/CVRs/receipt.csv
### Voter's row: 78
############
```

See [../../docs/E2EV.md](../../docs/E2EV.md) for more details regarding casting and inspecting ballots.  To validate the digests on/in the ballot receipt (use your row, not 78):

```
$ ./verify_ballot_receipt.py -f /opt/VoteTrackerPlus/demo.01/clients/scanner.00/VoteTrackerPlus/ElectionData/GGOs/states/California/GGOs/towns/Alameda/CVRs/receipt.csv -r 78
```

An random example ballot is saved off in ElectionData/receipts/receipt.74.csv.  When that receipt is verified, the output currently looks like the following:

```
$ ./verify_ballot_receipt.py -f ../ElectionData/receipts/receipt.74.csv -r 74
Running "git rev-parse --show-toplevel"
Running "git cat-file --buffer --batch-check=%(objectname) %(objecttype)"
Contest '0000 - US president' (fad4eb1c97b5f547a921c377d8d683d0837f7ff8) is vote 71 out of 146 votes
Contest '0003 - County Clerk' (7d3e7f992628931d416de2095e0420436ce8f53f) is vote 100 out of 146 votes
Contest '0005 - mayor' (c9734a3be4ef3533b4c1df0f14305bebe118b031) is vote 96 out of 146 votes
Contest '0006 - Question 1 - school budget override' (92b70d29cbd677418ffd6166e5c455dedcf4033b) is vote 45 out of 146 votes
Contest '0007 - Question 2 - new firehouse land purchase' (e4ae73730cf6d00e499af328d17c41f88599711c) is vote 65 out of 146 votes
The following contests are not merged to master yet:
0001 - US senate (0a9682dccf6ab5cb83d8a5ce43786e74514ce3ef)
0002 - governor (ef1b88c931222669997639a0c45f26a4ff0a7342)
############
### Ballot receipt VALID - no digest errors found
############
```

Note that five of the seven contests have been merged to master and as such now have a fixed offset in the _official_ tally of those contests.  This allows the voter who cast this ballot to say, with a very high level of trust, that their vote in contest '0000 - US president' is number 71 out of N.  As more contest CVRs are added to the tally (merged to master), the 71 will not change for this repo/precinct.  However, the vote number will change as precincts are aggregated.

Two of the contests above remain in the ballot cache and can still be randomly included in some other anonymized ballot check.  They will be merged to master by the VTP server at some point, either randomly during the voting or once the voting ceases at the polling location.

Running the above demo does not modify the VoteTrackerPlus repo and does not push any changes in the VTP-mock-election.US.nn repository back to the upstream GitHub repositories.  This is because by design the VTP scanner and server app repo pairs have the git origin pointing to the local bare repositories found in the local-remote-server folder in the demo.nn directory.

At any time and in any repository cloned from the local-remote-server VTP-mock-election.US.nn.git repository (that is not running something else) one can run inspect the current tally by:

```bash
$ ./tally_contests.py
```

tally_contests.py can be restricted to a single contest or report on all the contests that span all the ballot types.  It also supports a verbose switch so that one can see details about the tally.  This is helpful with RCV as one can then inspect the RCV rounds and what is happening to the candidates:

```bash
% ./tally_contests.py -c 0000 -v 3
Running "git rev-parse --show-toplevel"
Running "git pull"
Already up to date.
Running "git log --topo-order --no-merges --pretty=format:%H%B"
Scanned 186 contests for contest (US president) uid=0000, tally=rcv, max=1, win-by>0.5
RCV: round 0
[('Phil Scott', 38), ('Mitt Romney', 36), ('Kamala Harris', 34), ("Beta O'rourke", 30), ('Cory Booker', 28), ('Ron DeSantis', 20)]
RCV: round 1
[('Phil Scott', 41), ('Mitt Romney', 40), ('Kamala Harris', 38), ("Beta O'rourke", 37), ('Cory Booker', 30), ('Ron DeSantis', 0)]
RCV: round 2
[('Mitt Romney', 49), ('Kamala Harris', 47), ("Beta O'rourke", 46), ('Phil Scott', 44), ('Cory Booker', 0), ('Ron DeSantis', 0)]
RCV: round 3
[("Beta O'rourke", 64), ('Mitt Romney', 62), ('Kamala Harris', 60), ('Phil Scott', 0), ('Cory Booker', 0), ('Ron DeSantis', 0)]
RCV: round 4
Contest US president (uid=0000):
  ('Mitt Romney', 94)
  ("Beta O'rourke", 92)
  ('Kamala Harris', 0)
  ('Phil Scott', 0)
  ('Cory Booker', 0)
  ('Ron DeSantis', 0)
```
FYI - with -v4 and RCV contests, how each specific voter's ranked choice selection gets re-directed from their last place loosing candidate to their next choice candidate is printed, offering full transparency to RVC contests.  See [../../docs/E2EV.md](../../docs/E2EV.md) for more details.

### 4.5) Development cycle

New development should use a feature branch directly in this repo.  New ElectionData repositories can be created at will.  Signed commits are required in both repos.

1) Create a well named feature git branch
2) Develop code/tests
3) Maybe update the requirements.txt and environment.yml files
4) Validate pylint and pytest
5) Validate the mock election tests
6) Push code
7) Create a pull request
