# VoteTrackerPlus Development and Usage

This is significantly incomplete and needs more thought and work but it is a start.

## Terminology

For basic terminology see the [NIST](https://pages.nist.gov/ElectionGlossary/) glossary page.

The acronym for VoteTrackerPlus is VTP.

See [../docs/project-overview.md](../docs/project-overview.md) file in this git repo if you are unfamiliar with the VoteTrackerPlus directory structure.  That page contains a diagram of how a VoteTrackerPlus election is organized directory structure wise.

What is a VTP election tree (a.k.a. a VTP election directory tree)?

A VTP election tree is the directory structure that represents a specific election.  It is rooted with a clone of this repository and has zero or more additional git submodules organized in a specific manner.

This root repo contains all the python executables and libraries in this bin subdirectory that are necessary to run an election with respect to anything that directly reads or writes into these repos.  When a specific election is configured, the ./config.yaml and ./address_map.yaml files in this root repository are modified.  This initial modification will recursively define Geographical Geopolitical Overlays (GGOs - NIST calls this a [geopolitical units](https://pages.nist.gov/ElectionGlossary/#geopolitical-unit)).  More specifically, this root repo via the config.yaml and address-map.yaml files define the direct child GGOs (there can be multiple children), and those children config and address-map files define their potentially multiple children.  This effectively define an Directed Acyclic Graph (DAG) of election configuration yaml data.

This GGO based DAG election data can more or less arbitrarily span git submodules.  The git submodule splitting occurs when election official define a specific physical location in which VTP will be processing ballots __and__ when that location needs to scan the ballots or be able to scan the ballots disconnected network wise from other VTP locations.   A git submodule allows a voting center to operate without network connectivity with other VTP locations.  The election configuration DAG and the git submodule tree, which is also a DAG, need not be the same tree/graph.

Also, though disconnected network wise, each VTP location processes ballots with a full and complete distributed copy of all the VTP repos that comprise the election.

So, to create a VTP election configuration is to create these yaml files and git submodules either from scratch or to import/merge them from a previous or similar election.  Once imported/merged they can be updated and modified.  And once imported, the unit, functional, and mock election tests can be run locally as they are always executed as part of the VTP development process as part of the GitHub devsecops infrastructure.

## Background and Caveats

The VoteTrackerPlus project with respect to executable programs currently consists of a handfull of python scripts and libraries all in this directory.  To run these scripts the CWD (current working directory) for the programs can either be the git workspace root or this bin directory.  Other CWD's may not work as they are not currently part of the test matrix.

It is important that the end-voter usage model be as simple as possible and as immune as possible to false narratives and conspiracy theories.  A primary goal of VoteTrackerPlus is election and ballot trustworthiness.  As such a design goal of VoteTrackerPlus is that this git repo along with the various git submodules will comprise a specific election, statically, both in terms of code __and__ election configuration data __and__ [Cast Vote Records (CVRs)](https://pages.nist.gov/ElectionGlossary/#cast-vote-record).  By avoiding a python installation step the end-user (the end-voter) usage model is simplified while also minimizing the potential attack surface in the end-user's environment.  The intent is that the end-voter can clone this repo and with no further installation run the commands placed here as is, with as little mystery as possible from the point of view of someone with no software coding experience.  An entire VTP election tree is relocatable, reclone-able tree of files.  Only the python environment itself needs to be installed.

Therefor, there is no setup.py file for this project as there is no __pip install votetracker+__ or similar installation step.  As there is no VTP installation step, tests are run directly via pylint and  pytest and not via tox.  It is important that end-voters can also run the all the VTP tests on their computers.

## Development Process Target Goal

It is a goal to create a development process that eventually includes the following:

- Every commit is signed with a PGP key
- Standard GitHub pull request (PR) development models are in play
- All pull-requests and un-squashed commits pass pylint with at least a 9.9 score
- All pull-requests and un-squashed commits pass pytest
- A TBD level of unit and functional test coverage (pytest coverage)
- A TBD level of mock election test coverage (system testing)

This project is not there yet.

## Current Development Process

Note - this is very much in flux as the project is still being designed and framed out as code is being written.  This documentation may also be behind the actual code development.

### 1) One time python environment setup

Note - I am currently using [miniconda](https://docs.conda.io/en/latest/miniconda.html) - there are requirements.txt and environment.yml files that in theory should work.  Currently using python 3.9:

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

Note - can install matplotlib (conda install matplotlib) to see visual graphs of some of the data.

### 2) Clone this repo and an ElectionData repo

Note - currently using a symlink instead of a git submodule:

```bash
# clone both repos
$ git clone git@github.com:TrustTheVote-Project/VTP-root-repo.git
$ git clone git@github.com:TrustTheVote-Project/VTP-mock-election.US.<nn>.git
$ cd VTP-root-repo
$ ln -s ../VTP-mock-election.US.<nn> ElectionData

Where <nn> is the most recent mock election

```

See [VTP-mock-election.US.09](https://github.com/TrustTheVote-Project/VTP-mock-election.US.09) as an example

Each ElectionData repo can represent a different election.  Some repos may be already configured and can be immediately used to run an election.  Or the repo may be of a past election.  Others may be designed so that an election can be configured.

Regardless, to run a real or mock election one will need a usable ElectionData repo.

### 3) Running a mock election

With nominally both repos in place and assuming at this time no git submodules, run the setup_vtp_demo.py script.  This script will nominally create a mock election with four VTP scanner _apps_ and one VTP local-remote server _app_ as if all ballots were being cast in a single voting center.  By default it will place the git repos in /opt/VotetrackerPlus with the 5 clients (the four scanner apps and one server app) in the _clients_ folder with the two local git upstream bare repositories in the _local-remote-server_ folder.  The directory tree looks like this:

```
/opt/VotetrackerPlus/demo.01/clients/scanner.00/VTP-mock-election.US.01/.git
                                                VTP-root-repo/.git
                                     scanner.01/VTP-mock-election.US.01/.git
                                                VTP-root-repo/.git
                                     scanner.02/VTP-mock-election.US.01/.git
                                                VTP-root-repo/.git
                                     scanner.03/VTP-mock-election.US.01/.git
                                                VTP-root-repo/.git
                                     server/VTP-mock-election.US.01/.git
                                                VTP-root-repo/.git
/opt/VotetrackerPlus/demo.01/local-remote-server/VTP-mock-election.US.01.git
                                                 VTP-root-repo.git
```

The git repositories in the _clients_ subfolder all have workspaces as that is where the various commands run to simulate an individual ballot scanner application.  The two bare repostitories in local-remote-server mimick the actual voting center local (bare) git remote repositories for both the VTP scanner and server apps.

The basic demo idea is to start a separate __run_mock_election.py -d scanner__ instance in the first three scanner subfolders.  And then in the fourth scanner.04 subfolder manually and interactively cast ballots.  This will simulate a voter at an active voting center.  A VTP server app should be run in the server subfolder.

Here is an example of running a 4 VTP scanner and 1 VTP server app mock demo election.  This simulates an in-person voting center with 4 ballot scanners producing ballot receipts for the voters.  The first three are submitting random ballots while the fourth someone at the keyboard can manually submit one ballot at a time.

```bash
# In terminal window #1
$ cd /opt/VotetrackerPlus/demo.01/clients/scanner.00/VTP-mock-election.US.01/bin
$ conda activate vtp.01
$ ./run_mock_election.py -s California -t Alameda -a "123 Main Street" -d server

# In terminal window #2
$ cd /opt/VotetrackerPlus/demo.01/clients/scanner.00/VTP-mock-election.US.01/bin
$ conda activate vtp.01
# Auto cast 100 random ballots
$ ./run_mock_election.py -s California -t Alameda -a "123 Main Street" -d scanner -i 100

# In terminal window #3
$ cd /opt/VotetrackerPlus/demo.01/clients/scanner.01/VTP-mock-election.US.01/bin
$ conda activate vtp.01
# Auto cast 100 random ballots
$ ./run_mock_election.py -s California -t Alameda -a "123 Main Street" -d scanner -i 100

# In terminal window #4
$ cd /opt/VotetrackerPlus/demo.01/clients/scanner.02/VTP-mock-election.US.01/bin
$ conda activate vtp.01
# Auto cast 100 random ballots
$ ./run_mock_election.py -s California -t Alameda -a "123 Main Street" -d scanner -i 100

# In terminal window #5
$ cd /opt/VotetrackerPlus/demo.01/clients/scanner.03/VTP-mock-election.US.01/bin
$ conda activate vtp.01

# To manually vote and cast one ballot, run vote.py.  The receipt.cvs will be printed to a file
# as this mock demo is software only.  Please note the ballot's offset row number that is
# printed to STDOUT at the end of the execution of vote.py.
$ ./vote.py -s California -t Alameda -a "123 Main Street"
```

The last few lines printed by ./vote.py should look something like this:

```
############
### Receipt file: /opt/VoteTrackerPlus/demo.01/clients/scanner.01/VTP-root-repo/ElectionData/GGOs/states/California/GGOs/towns/Alameda/CVRs/receipt.csv
### Voter's row: 78
############
```

To validate the digests on/in the ballot receipt (use your row, not 74):

```
$ ./verify_ballot_receipt.py -f /opt/VoteTrackerPlus/demo.01/clients/scanner.03/VTP-root-repo/ElectionData/GGOs/states/California/GGOs/towns/Alameda/CVRs/receipt.csv -r 74
```

An example ballot is saved off in ElectionData/receipts/receipt.74.csv.  When that receipt is verified, the output currently looks like the following:

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

Note that five of the seven contests have been merged to master and as such now have a fixed offset in the _official_ tally of those contests.  This allows the voter who cast this ballot to say, with a very high level of trust, that their vote in contest '0000 - US president' is 71.  As more contest CVRs are added to the tally (merged to master), the 71 will not change.

Ta Da

Two of the contests above remain in the ballot cache and can still be randomly included in some other ballot receipt.  At some future random time they will be merged to master.  When all the polls close and the vote center has no more incoming ballots, the cache is completely drained and merged to master.

Running the above demo does not modify the VTP-root-repo repo and does not push any changes in the VTP-mock-election.US.nn repository back to the upstream GitHub repositories.  This is because by design the four scanner and server app repo pairs have the git origin pointing to the local bare repositories found in the local-remote-server folder in the demo.nn directory.

At any time and in any repository cloned from the local-remote-server VTP-mock-election.US.nn.git repository (that is not running something else) one can run inspect the current tally by:

```bash
$ ./tally_contests.py
```

However, as of this version, the ./vote.py program does not automatically pull the ElectionData repo as the VTP scanner and server apps do and as such, the ElectionData repo needs to manually 'git pull'ed for it to be updated in the workspace that is manually casting ballots.

### 4) Development cycle

New development should use a feature branch directly in this repo.  New ElectionData repositories can be created at will.  Signed commits are required in both repos.

1) Create a well named feature git branch
2) Develop code/tests
3) Maybe update the requirements.txt and environment.yml files
4) Validate pylint and pytest
5) Validate the mock election tests
6) Push code
7) Create a pull request
