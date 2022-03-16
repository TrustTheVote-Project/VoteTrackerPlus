# VoteTracker+ Development and Usage

This is significantly incomplete and needs more thought and work but it is a start.

## Terminology

For basic terminology see the [NIST](https://pages.nist.gov/ElectionGlossary/) glossary page.

The acronym for VoteTracker+ is VTP.

See [../docs/project-overview.md](../docs/project-overview.md) file in this git repo if you are unfamiliar with the VoteTracker+ directory structure.  That page contains a diagram of how a VoteTracker+ election is organized directory structure wise.

What is a VTP election tree (a.k.a. a VTP election directory tree)?

A VTP election tree is the directory structure that represents a specific election.  It is rooted with a clone of this repository and has zero or more additional git submodules organized in a specific manner.

This root repo contains all the python executables and libraries in this bin subdirectory that are necessary to run an election with respect to anything that directly reads or writes into these repos.  When a specific election is configured, the ./config.yaml and ./address_map.yaml files in this root repository are modified.  This initial modification will recursively define Geographical Geopolitical Overlays (GGOs - NIST calls this a [geopolitical units](https://pages.nist.gov/ElectionGlossary/#geopolitical-unit)).  More specifically, this root repo via the config.yaml and address-map.yaml files define the direct child GGOs (there can be multiple children), and those children config and address-map files define their potentially multiple children.  This effectively define an Directed Acyclic Graph (DAG) of election configuration yaml data.

This GGO based DAG election data can more or less arbitrarily span git submodules.  The git submodule splitting occurs when election official define a specific physical location in which VTP will be processing ballots __and__ when that location needs to scan the ballots or be able to scan the ballots disconnected network wise from other VTP locations.   A git submodule allows a voting center to operate without network connectivity with other VTP locations.  The election configuration DAG and the git submodule tree, which is also a DAG, need not be the same tree/graph.

Also, though disconnected network wise, each VTP location processes ballots with a full and complete distributed copy of all the VTP repos that comprise the election.

So, to create a VTP election configuration is to create these yaml files and git submodules either from scratch or to import/merge them from a previous or similar election.  Once imported/merged they can be updated and modified.  And once imported, the unit, functional, and mock election tests can be run locally as they are always executed as part of the VTP development process as part of the GitHub devsecops infrastructure.

## Background and Caveats

The VoteTracker+ project with respect to executable programs currently consists of a handfull of python scripts and libraries all in this directory.  To run these scripts the CWD (current working directory) for the programs can either be the git workspace root or this bin directory.  Other CWD's may not work as they are not currently part of the test matrix.

It is important that the end-voter usage model be as simple as possible and as immune as possible to false narratives and conspiracy theories.  A primary goal of VoteTracker+ is election and ballot trustworthiness.  As such a design goal of VoteTracker+ is that this git repo along with the various git submodules will comprise a specific election, statically, both in terms of code __and__ election configuration data __and__ [Cast Vote Records (CVRs)](https://pages.nist.gov/ElectionGlossary/#cast-vote-record).  By avoiding a python installation step the end-user (the end-voter) usage model is simplified while also minimizing the potential attack surface in the end-user's environment.  The intent is that the end-voter can clone this repo and with no further installation run the commands placed here as is, with as little mystery as possible from the point of view of someone with no software coding experience.  An entire VTP election tree is relocatable, reclone-able tree of files.  Only the python environment itself needs to be installed.

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

ZZZ - more work here

### 1) Clone this repo and an ElectionData repo

Note - currently using a symlink instead of a git submodule:

```bash
# clone both repos
$ git clone git@github.com:TrustTheVote-Project/VTP-root-repo.git
$ git clone git@github.com:TrustTheVote-Project/VTP-mock-election.US.01.git
$ cd VTP-root-repo
$ ln -s ../VTP-mock-election.US.01 ElectionData
```

See [VTP-mock-election.US.01](https://github.com/TrustTheVote-Project/VTP-mock-election.US.01) as an example

### 2) One time python environment setup

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

### 3) One time mock election configuration setup

TBD.  Maybe the better thing is to prefab mock elections as other separate repos, some with git submodules and some without, and have the mock election tests framework stuff this repo as-is into that directory tree and run the mock election tests there.  Some of the mock tests might be limited to local repo only testing while some of the mock tests may involve simulating GitHub pushes and other pre and post election day mock testing.

### 4) Development cycle

New development should use a feature branch directly in this repo as well as in the mock election repos:

1) Create a well named feature git branch
2) Develop code/tests
3) Maybe update the requirements.txt and environment.yml files
4) Validate pylint and pytest
5) Validate the mock election tests
6) Push code
7) Create a pull request
