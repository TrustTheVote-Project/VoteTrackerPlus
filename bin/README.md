# VoteTracker+ Development and Usage Details

This is significantly incomplete and needs more thought and work.

## Terminology

For basic terminology see the [NIST](https://pages.nist.gov/ElectionGlossary/) glossary page.

The acronym for VoteTracker+ is VTP.

Maybe also see ../docs/project-overview.md file in this git repo if you are unfamiliar with VoteTracker+.  That page contains a diagram of how a VoteTracker+ election is organized directory structure wise.

What is a VTP election (a.k.a. a VTP election tree)?

A VTP election is basically this repo plus zero or more additional git submodules organized in a specific manner.  See the directory structure described in ../docs/project-overview.md.

This repo contains all the python executables and libraries (in this bin directory) required to run an election with respect to anything that directly reads or writes into these repos.  When a specific election is configured, the ./config.yaml and address_map.yaml files in this repos are modified which as a by-product effectively define an Directed Acyclic Graph (DAG) of election configuration yaml data.  This DAG is based on the election defining various Geographical/Geopolitical Overlays (GGOs) that will be in play for this specific election.  The GGOs have a child parent relationship with this repo while also potentially having sibling relationships amongst themselves.

This DAG election data can somewhat arbitrarily span git submodules.  The git submodule splitting occurs when any physical location in which VTP will be processing ballots __and__ needs to be disconnected internet wise from other VTP locations.   A git submodule will allow a voting center to operate without network connectivity with other VTP instances.  The election configuration DAG and the git submodule tree do not need to be the same tree/graph.

So, to create a VTP election configuration is to create these yaml files either from scratch or to import/merge them from a previous election (and potentially update them).  Once imported/merged, VTP mock election tests can be run to validate the configuration.  Running VTP mock election tests may require upstream git repos depending on the degree of the testing.  Mock election testing may also include actual GitHub test repositories.

## Background and Caveats

The VoteTracker+ project with respect to executable programs currently consists of a handfull of python scripts and libraries all in this directory.  To run these scripts the CWD (current working directory) for the programs can either be the git workspace root or this bin directory.  Other CWD's may not work as they are not currently part of the test matrix.

It is important that the end-voter usage model be as simple as possible and as immune as possible to false narratives and conspiracy theories.  A primary goal of VoteTracker+ is election and ballot trustworthiness.  As such a design goal of VoteTracker+ is that this git repo along with the various git submodules will comprise a specific election, statically, both in terms of code __and__ election configuration data __and__ [Cast Vote Records (CVRs)](https://pages.nist.gov/ElectionGlossary/#cast-vote-record).  By avoiding a python installation step the end-user (the end-voter) usage model is simplified while also minimizing the potential attack surface in the end-user's environment.  The intent is that the end-voter can clone this repo and with no further installation run the commands placed here as is, with as little mystery as possible from the point of view of someone with no software coding experience.  An entire VTP election tree is relocatable and reclone-able.  Only the python environment itself needs to be installed.

Therefor, there is no setup.py file for this project as there is no __pip install votetracker+__ installation step.  As there is no python installation step, tests are run directly via pytest and not via tox.  It is important that an end-voter can also run the pytest tests.

## Development Process Target Goal

It is a goal to create a development process that eventually includes the following:

- Every commit needs to be signed with a PGP key
- Standard GitHub pull-request development models are in play
- All pull-requests and un-squashed commits pass pylint with at least a 9.9 score
- All pull-requests and un-squashed commits pass pytest
- A TBD coverage level of unit, functional, and system level testing
- A TBD level of test coverage

The project is not there yet.

## Current Development Process

### 1) Clone this repo

### 2) One time python environment setup

Note - I am currently using (mini) conda.  Regardless there is requirements.txt and environment.yml in the root of the git workspace.

### 3) One time mock election configuration setup

### 4) Development cycle

At this point new development can use a feature branch directly in this repo:

1) Create a well named feature git branch
2) Develop code/tests
3) Maybe update the requirements.txt and environment.yml files
4) Validate pylint and pytest
5) Push code
6) Create a pull request
