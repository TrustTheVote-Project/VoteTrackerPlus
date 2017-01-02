# VOTES

A Verifiable Open Technology Election System

# Overview

VOTES is a distributed, open-source project aimed at creating public/private, transparent, secure, and accurate elections.  It is an [election](https://en.wikipedia.org/wiki/Election) and [voting](https://en.wikipedia.org/wiki/Voting) framework delivered as a [SaaS](https://en.wikipedia.org/wiki/Software_as_a_service) solution.

The basic idea is to design a open technology system for elections that can either be adopted by existing election system providers (ESS/Diebold), by public or private agencies during the [RFP](https://en.wikipedia.org/wiki/Request_for_proposal) process, or by anyone wishing to provide election systems (a public agency, an individual, or a high tech start-up).

VOTES is intended to be as compliant as possible with [NIST](https://en.wikipedia.org/wiki/National_Institute_of_Standards_and_Technology)'s [voting](https://www.nist.gov/itl/voting) efforts (see the [HAVA](https://en.wikipedia.org/wiki/Help_America_Vote_Act) Act).

# Basic Design Goal

The basic high level design goals are:

* The voter can validate the accuracy of their vote and its proper tally at any time
  * Anyone with access to the election repository can count the votes
  * The election repository is not available until after the polls close
* There is both a paper and electronic trail with the necessary security attributes
* The system:
  * can support any vote counting [methodology](https://electology.org/library)
  * is incrementally adoptable at different geographical/hierarchical levels
  * scales well - is distributed
  * easily testable - simulations can be run at will
* Create a solution that is usable in the 2020 US election

# Status - 2017/01/01

Happy New Year - VOTES is currently in the design phase - still working out the basics etc.  See the docs directory for more info.
