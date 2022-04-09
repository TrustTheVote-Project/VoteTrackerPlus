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
$ conda create -n votes.01 python=3.9
$ conda activate votes.01
$ conda install pylint pytest pyyaml networkx
```

Note - can install matplotlib (conda install matplotlib) to see visual graphs of some of the data.

### 2) Clone this repo and an ElectionData repo

Note - currently using a symlink instead of a git submodule:

```bash
# clone both repos
$ git clone git@github.com:TrustTheVote-Project/VTP-root-repo.git
$ git clone git@github.com:TrustTheVote-Project/VTP-mock-election.US.01.git
$ cd VTP-root-repo
$ ln -s ../VTP-mock-election.US.01 ElectionData
```

See [VTP-mock-election.US.01](https://github.com/TrustTheVote-Project/VTP-mock-election.US.01) as an example

Each ElectionData repo can represent a different election.  Some repos may be already configured and can be immediately used to run an election.  Or the repo may be of a past election.  Others may be designed so that an election can be configured.

Regardless, to run a real or mock election one will need a usable ElectionData repo.

### 3) Running a mock election

With nominally both repos in place (assuming at this time no git submodules), decide if a serial or parallel election wants to be run.  As of now only serial mock elections are supported.  Eventually more complex election topologies will be supported.

Also configure git with the appropriate remote for the ElectionData repo.  Using the public GitHub is probably not what one wants to do by default.

To run a serial mock election:

```bash
# bin/generate_all_blank_ballots.py
# bin/run_mock_election.py -b <number of unique ballots> -s <state> -t <town>
# bin/tally_contests.py

where:

<number of unique ballots> is the number of GGO unique ballots to cast
<state> and <town> are nominally the state and town to process cast ballots
  (assuming ElectionData configured as such)
```

Once it is supported, one can run mock elections in parallel given the git workspace topology that is chosen.  Another way to say the same thing, parallel mock elections can be executed by configuring the VTP server git workspace and one or more VTP scanner git workspaces.  When a parallel mock election is running, it is possible for interactive ballots to be cast and included within the election.

### 4) Development cycle

New development should use a feature branch directly in this repo as well as in the mock election repos:

1) Create a well named feature git branch
2) Develop code/tests
3) Maybe update the requirements.txt and environment.yml files
4) Validate pylint and pytest
5) Validate the mock election tests
6) Push code
7) Create a pull request
