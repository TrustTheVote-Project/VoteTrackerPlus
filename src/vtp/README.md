# VoteTracker+ Development and Usage

This is a work in progress and may not be completely up-to-date.

## 1) Terminology

For basic terminology see the [NIST](https://pages.nist.gov/ElectionGlossary/) glossary page.

VoteTracker+ (VTP) URL's and PATH references have the '+' spelled out (VoteTrackerPlus).

See [../../docs/project-overview.md](../../docs/project-overview.md) for more general VTP information.  In particular see [../../docs/tech-details/more-tech-details.md](../../docs/tech-details/more-tech-details.md) for details of the VTP election directory layout.  The directory layout is key to better understand the VoteTracker+ solution and how election data is organized the directory, file, and git repository levels.

A VTP election configuration data, a.k.a. the ElectionData, in essence is the directory structure that represents a specific election.  The directory structure is rooted with a clone of a root election repository, representing either a real or mock election.  The ElectionData repo may have zero or more additional git submodules organized in a specific manner as a function of voting precinct and/or computer network isolation.  One potentially common layout/deployment is one git repo per voting center.

This repo contains all the python executables and libraries necessary to run an election and does not contain ElectionData specific information (such as [Cast Vote Records][Cast Vote Records]) other than basic configuration names and locations.

When a specific election is configured, either for real or for mock/testing purposes, the ./config.yaml and ./address_map.yaml files in the election repositories are modified accordingly.  This initial modification will define Geographical Geopolitical Overlays (GGOs - NIST calls this a [geopolitical units](https://pages.nist.gov/ElectionGlossary/#geopolitical-unit)).  More specifically, the config and address-map files define the direct child GGOs (there can be multiple children), and those children config and address-map files define their potentially multiple children.  This effectively define an Directed Acyclic Graph (DAG) of election configuration data.

The GGO based DAG election data can also more or less arbitrarily span git submodules.  The git submodule splitting occurs when election official define a specific physical location in which VTP will be processing ballots __and__ when that location needs to scan the ballots or be able to scan the ballots disconnected network wise from other VTP locations.   A git submodule allows a voting center to operate without network connectivity with other VTP locations.  The election configuration DAG and the git submodule tree, which is also a DAG, need not be the same tree/graph.

Also, though disconnected network wise, each VTP location processes ballots with a full and complete distributed copy of all the VTP repos that comprise the election.

In summary, to create a VTP election configuration is to create these yaml files and git submodules either from scratch or to import/merge them from a previous or similar election.  Once imported/merged they can be updated and modified.  And once imported, the unit, functional, and mock election tests can be run locally as they are always executed as part of the VTP development process as part of the GitHub devsecops infrastructure.

## 2) Background and Caveats

The VoteTracker+ project with respect to executable programs currently consists of a handfull of python scripts in this repository, a web-api repository containing a FastAPI restful interface, and a html/css/javascript client browser front end.  See the [VTP-dev-env](https://github.com/TrustTheVote-Project/VTP-dev-env) repo for more info.

It is important that the end-voter usage model be as simple as possible and as immune as possible to false narratives and conspiracy theories.  A primary goal of VoteTracker+ is election and ballot trustworthiness.  As such a design goal of VoteTracker+ is that this git repo along with the various git submodules will comprise a specific election, statically, both in terms of code __and__ election configuration data (a.k.a. the ElectionData)  __including__ all the [Cast Vote Records][Cast Vote Record].

## 3) Development Process Target Goal

The VoteTracker+ development process is currently more or less the following:

- Commits are required to be signed.  See [https://github.com/TrustTheVote-Project/VoteTrackerPlus/blob/main/docs/informal-security-overview.md](https://github.com/TrustTheVote-Project/VoteTrackerPlus/blob/main/docs/informal-security-overview.md)
- Standard GitHub pull request (PR) development models are in play
- All pull-requests are squashed-merged onto main - main maintains a linear history
- All pull-requests pass isort, black, and pylint with a pylint score of 10.0
- All pull-requests pass pytest (assuming that there are tests)
- A TBD level of unit and functional test coverage (pytest coverage)
- A TBD level of mock election test coverage (system testing)

This project is not yet completely there process wise.

## 4) Current Development Process

The current development process is in flux as the project is still being occasionally refactored as needed.

### 4.1) One time poetry installation

Currently Votetracker+ is using [poetry](https://python-poetry.org/) as the python package and dependency manager.  The base python is currently 3.10.  However, any python environment manager the employs pyproject.toml files can be used.

Mac example:

```bash
# install homebrew - see https://brew.sh/ and https://docs.brew.sh/Installation
$/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# install pipx via homebrew - see https://pipx.pypa.io/stable/installation/
$ brew install pipx

# install poetry - see https://python-poetry.org/docs#installation
$ pipx install poetry
```

### 4.2) Clone a mock election repo and this repo

The VotetrackerPlus repo is typically included as a submodule, and that is the case with the [VTP-mock-election.US.10](https://github.com/TrustTheVote-Project/VTP-mock-election.US.10) repo.  Clone that repo enabling submodules:

```bash
$ mkdir vtp.repos && cd vtp.repos
$ git clone --recurse-submodules git@github.com:TrustTheVote-Project/VTP-dev-env.git
```

Each VTP ElectionData repository, mock or otherwise, represents a different election.  An election data repo may be already configured, or may be of a past election, or may be a test/mock election.  The VTP-mock-election.US.10 election data repo is a test/mock election.

### 4.3) Create a python environment in which to run VTP

See [_tools/build/README.md](../../_tools/build/README.md) for directions of how to set up a python environment and perform a local install so that the VoteTrackerPlus scripts contained in the repo can properly when the python environment is activated.

### 4.4) Activate the python environment

If using poetry, from the same root of the VoteTrackerPlus git repo:

```bash
$ poetry shell
```

### 4.5) Odds and Ends

As VoteTrackerPlus leverages git, one must have a git "user.name" and "user.email" defined somewhere.  One way to accomplish this is the following:

```bash
$ git config --global user.email "you@example.com"
$ git config --global user.name "your name"
```

### 4.6) Running a mock election

To run a mock election, run the setup_vtp_demo.py script (which per python's local install described above is installed in the python environment as _setup-vtp-demo_).  This script will nominally create a mock election with four VTP scanner _apps_ and one VTP tabulation server _app_ as if all ballots were being cast in a single voting center with four separate and independent ballot scanners.  By default it will place the git repos in /opt/VotetrackerPlus with the 5 clients (the four scanner apps and one server app) in the _clients_ folder with the two local git upstream bare repositories in the _tabulation-server_ folder.

```
% setup-vtp-demo -e ../VTP-mock-election.US.16
Running "git rev-parse --show-toplevel"
Running "git config --get remote.origin.url"
Running "git clone --bare git@github.com:TrustTheVote-Project/VTP-mock-election.US.16.git"
Running "git clone /opt/VoteTrackerPlus/demo.01/tabulation-server/VTP-mock-election.US.16.git"
Running "git clone /opt/VoteTrackerPlus/demo.01/tabulation-server/VTP-mock-election.US.16.git"
Running "git clone /opt/VoteTrackerPlus/demo.01/tabulation-server/VTP-mock-election.US.16.git"
Running "git clone /opt/VoteTrackerPlus/demo.01/tabulation-server/VTP-mock-election.US.16.git"
Running "git clone /opt/VoteTrackerPlus/demo.01/tabulation-server/VTP-mock-election.US.16.git"
```

The resulting directory tree looks like this:

```
% cd /opt/VoteTrackerPlus/demo.01
% tree
.
├── guid-client-store
├── mock-clients
│   ├── scanner.00
│   │   └── VTP-mock-election.US.16
│   │       ├── GGOs
│   │       │   └── states
│   │       │       └── Massachusetts
│   │       │           ├── GGOs
│   │       │           │   ├── counties
│   │       │           │   │   └── Middlesex
│   │       │           │   │       └── config.yaml
│   │       │           │   └── towns
│   │       │           │       └── Concord
│   │       │           │           ├── CVRs
│   │       │           │           │   └── contest.json
│   │       │           │           ├── address_map.yaml
│   │       │           │           └── config.yaml
│   │       │           └── config.yaml
│   │       ├── LICENSE
│   │       ├── Makefile
│   │       ├── README.md
│   │       └── config.yaml
│   ├── scanner.01
│   │   └── VTP-mock-election.US.16
[... ditto ...]
│   ├── scanner.02
│   │   └── VTP-mock-election.US.16
[... ditto ...]
│   ├── scanner.03
│   │   └── VTP-mock-election.US.16
[... ditto ...]
│   └── server
│       └── VTP-mock-election.US.16
[... ditto ...]
└── tabulation-server
    └── VTP-mock-election.US.16.git
        ├── HEAD
        ├── config
        ├── description
        ├── hooks
        │   ├── applypatch-msg.sample
        │   ├── commit-msg.sample
        │   ├── fsmonitor-watchman.sample
        │   ├── post-update.sample
        │   ├── pre-applypatch.sample
        │   ├── pre-commit.sample
        │   ├── pre-merge-commit.sample
        │   ├── pre-push.sample
        │   ├── pre-rebase.sample
        │   ├── pre-receive.sample
        │   ├── prepare-commit-msg.sample
        │   ├── push-to-checkout.sample
        │   └── update.sample
        ├── info
        │   └── exclude
        ├── objects
        │   ├── info
        │   └── pack
        │       ├── pack-036a7570a9631e18f0435e1070dc5258af19a6a3.idx
        │       └── pack-036a7570a9631e18f0435e1070dc5258af19a6a3.pack
        ├── packed-refs
        └── refs
            ├── heads
            └── tags

67 directories, 65 files
```

The git repositories in the _clients_ subfolder all have workspaces as that is where the various commands run to simulate an individual ballot scanner application.  The two bare repostitories in tabulation-server mimick the actual voting center local (bare) git remote repositories for both the VTP scanner and server apps.

The basic demo idea is to start a separate __run-mock-election -d scanner__ instance in the first three scanner subfolders.  And then in the fourth scanner.04 subfolder manually and interactively cast ballots.  This will simulate a voter at an active voting center.  A VTP server app should be run in the server subfolder.

Here is an example of running a 4 VTP scanner and 1 VTP server app mock demo election.  This simulates an in-person voting center with 4 ballot scanners producing the anonymized ballot checks for the voters.  The first three are submitting random ballots while the fourth someone at the keyboard can manually submit one ballot at a time.

```bash
# In terminal window #1, run a VTP tabulation server
# Note - this assumes the explicit setup steps above - note the poetry pyproject.toml location
$ cd vtp.repos/VTP-mock-election.US.16/VoteTrackerPlus
$ poetry shell
$ cd /opt/VotetrackerPlus/demo.01/clients/server/VoteTrackerPlus
$ run-mock-election -s Massachusetts -t Concord -a "123 Main Street" -d server

# In terminal window #2, run a VTP scanner in mock election mode
$ cd vtp.repos/VTP-mock-election.US.16/VoteTrackerPlus
$ poetry shell
$ cd /opt/VotetrackerPlus/demo.01/clients/scanner.01/VoteTrackerPlus
# Auto cast 100 random ballots
$ run-mock-election -s Massachusetts -t Concord -a "123 Main Street" -d scanner -i 100

# In terminal window #3, run a second VTP scanner in mock election mode
$ cd vtp.repos/VTP-mock-election.US.16/VoteTrackerPlus
$ poetry shell
$ cd /opt/VotetrackerPlus/demo.01/clients/scanner.02/VoteTrackerPlus
# Auto cast 100 random ballots
$ run-mock-election -s Massachusetts -t Concord -a "123 Main Street" -d scanner -i 100

# In terminal window #4, run an interactive VTP scanner to cast ballots
$ cd vtp.repos/VTP-mock-election.US.16/VoteTrackerPlus
$ poetry shell
$ cd /opt/VotetrackerPlus/demo.01/clients/scanner.00/VoteTrackerPlus

# To manually vote and cast one ballot, run vote.py.  The receipt.csv will be printed to a file
# and the row offset will be printed to the screen (STDOUT).
$ vote -s Massachusetts -t Concord -a "123 Main Street"
```

The last few lines printed by ./vote.py should look something like this:

```
############
### Receipt file: /opt/VoteTrackerPlus/demo.01/clients/scanner.00/VoteTrackerPlus/ElectionData/GGOs/states/Massachusetts/GGOs/towns/Concord/CVRs/receipt.csv
### Voter's row: 78
############
```

See [../../docs/E2EV.md][E2EV.md] for more details regarding casting and inspecting ballots.  To validate the digests on/in the ballot receipt (use your row, not 78):

```
$ verify-ballot-receipt -f /opt/VoteTrackerPlus/demo.01/clients/scanner.00/VoteTrackerPlus/ElectionData/GGOs/states/Massachusetts/GGOs/towns/Concord/CVRs/receipt.csv -r 78
```

An random example ballot is saved off in ElectionData/receipts/receipt.74.csv.  When that receipt is verified, the output currently looks like the following:

```
% verify-ballot-receipt -f receipts/receipt.59.csv -r 59
Running "git rev-parse --show-toplevel"
Running "git pull"
Already up to date.
Running "git cat-file --buffer --batch-check=%(objectname) %(objecttype)"
Contest '0000 - U.S. President' (20ec3a9080ce8d4167b41843b1ffc6905a172263) is vote 304 out of 304 votes
Contest '0001 - U.S. Senate' (8bef5f87658c40bbe7dcda814422a59e844b204d) is vote 303 out of 303 votes
Contest '0002 - Governor' (f088442581dfac4332d8633239c0272f83f8ee2a) is vote 303 out of 303 votes
Contest '0003 - County Clerk' (dacba213d14d28e5fb6dc4c5d8be88d37b6c8166) is vote 304 out of 304 votes
Contest '0004 - Question 1 - should the starting time of the annual town meeting be moved to 6:30 PM?' (2cbf5011576f0a6dc49817c5619df237726358e0) is vote 304 out of 304 votes
############
[GOOD]: ballot receipt VALID - no digest errors found
############
```

Note that five of the seven contests have been merged to main and as such now have a fixed offset in the _official_ tally of those contests.  This allows the voter who cast this ballot to say, with a very high level of trust, that their vote in contest '0000 - US president' is number 71 out of N.  As more contest CVRs are added to the tally (merged to main), the 71 will not change for this repo/precinct.  However, the vote number will change as precincts are aggregated.

Two of the contests above remain in the ballot cache and can still be randomly included in some other anonymized ballot check.  They will be merged to main by the VTP server at some point, either randomly during the voting or once the voting ceases at the polling location.

Running the above demo does not modify the VoteTrackerPlus repo and does not push any changes in the VTP-mock-election.US.nn repository back to the upstream GitHub repositories.  This is because by design the VTP scanner and server app repo pairs have the git origin pointing to the local bare repositories found in the tabulation-server folder in the demo.nn directory.

At any time and in any repository cloned from the tabulation-server VTP-mock-election.US.nn.git repository (that is not running something else) one can run inspect the current tally by:

```bash
$ tally-contests
```

tally_contests.py can be restricted to a single contest or report on all the contests that span all the ballot types.  It also supports a verbose switch so that one can see details about the tally.  This is helpful with RCV as one can then inspect the RCV rounds and what is happening to the candidates:

```bash
% tally-contests -c 0001
Running "git rev-parse --show-toplevel"
Running "git pull"
Already up to date.
Running "git log --topo-order --no-merges --pretty=format:%H%B"
Scanned 303 contests for contest (U.S. Senate) uid=0001, tally=rcv, max=1, win_by>0.5
RCV: round 0
Total vote count: 303
[('Gloria Gamma', 65), ('Anthony Alpha', 53), ('David Delta', 47), ('Emily Echo', 47), ('Francis Foxtrot', 47), ('Betty Beta', 44)]
RCV: round 1
Total vote count: 303
[('Gloria Gamma', 71), ('Anthony Alpha', 65), ('Francis Foxtrot', 57), ('David Delta', 55), ('Emily Echo', 55), ('Betty Beta', 0)]
RCV: round 2
Total vote count: 303
[('Anthony Alpha', 106), ('Gloria Gamma', 102), ('Francis Foxtrot', 95), ('Emily Echo', 0), ('David Delta', 0), ('Betty Beta', 0)]
RCV: round 3
Total vote count: 303
Final results for contest U.S. Senate (uid=0001):
  ('Gloria Gamma', 152)
  ('Anthony Alpha', 151)
  ('Francis Foxtrot', 0)
  ('Emily Echo', 0)
  ('David Delta', 0)
  ('Betty Beta', 0)
```
FYI - with -v4 and RCV contests, how each specific voter's ranked choice selection gets re-directed from their last place loosing candidate to their next choice candidate is printed, offering full transparency to RVC contests.  See [../../docs/E2EV.md][E2EV.md] for more details.

## 5) Development cycle

New development should use a feature branch directly in this repo.  New ElectionData repositories can be created at will.  Signed commits are required in both repos.

1) Create a well named feature git branch
2) Develop code/tests
3) Maybe update the requirements.txt and environment.yml files
4) Run "make pylint"
5) Validate the mock election tests
6) Push code
7) Create a pull request

[Cast Vote Record]: https://pages.nist.gov/ElectionGlossary/#cast-vote-record
[E2EV.md]: ../../docs/E2EV.md
