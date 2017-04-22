# VOTES

A Verifiable Open Technology Election System

# Overview

VOTES is a distributed, open-source [voting](https://en.wikipedia.org/wiki/Voting) system that creates transparent, secure, and accurate elections with anonymous individually verifiable ballots.

**BUSINESS ADVANTAGES:**  VOTES can be adopted by existing election solution providers ([ESS/Diebold](http://www.essvote.com/about/), [ClearBallot](http://www.clearballot.com/), etc.), public or private agencies during the [RFP](https://en.wikipedia.org/wiki/Request_for_proposal) process for voting machines or UVBM ([Universal Vote By Mail](http://washingtonmonthly.com/magazine/janfeb-2016/vote-from-home-save-your-country/)) solutions, or anyone wishing to provide election systems/solutions.  VOTES is both a self-contained free open-source platform as well as a revenue generating [SaaS](https://en.wikipedia.org/wiki/Software_as_a_service) solution capable of handling national, state, town, or private elections.

**TECH ADVANTAGES:** VOTES allows the voter to anonymously validate their ballot and its accurate inclusion in an election while allowing election officials validate or invalidate ballots post casting.  It is extremely immune to hacking and compromise due to its distributed, bitcoin-like hashed full ledger design.  VOTES also increases the difficulty of creating a market for the purchasing and selling of ballots.  It fully supports UVBM and traditional elections, early and absentee balloting, as well as on-line balloting.

**END-VOTER ADVANTAGES:**  Using VOTES the voter can validate their ballot as well as the tally of any contest. VOTES is 100% transparent, insuring that no entity or person can mishandle or manipulate any ballot or contest. 

**VOTER RIGHTS/POLICY ADVANTAGES:**   VOTES is not a voter ID system, but it does by default track the voter id in an encrypted manner such that individual ballots can be surgically tracked and nullified under court supervised recounts.  With such capabilities the natural tension between extensive voter pre identification/registration and a low effective barrier to voting, particularly for the disenfranchised and disadvantaged, is mitigated in a manner that can support a low barrier of voter id while providing extensive capability of fraudulent ballot nullification that is possible regardless of the level of voter identification.  Under due process a ballot can be nullified after the fact as well as un-nullified in repeal with full automatic disclosure and full tracking.

VOTES is intended to be as compliant as possible with [NIST](https://en.wikipedia.org/wiki/National_Institute_of_Standards_and_Technology)'s [voting](https://www.nist.gov/itl/voting) efforts (see the [HAVA](https://en.wikipedia.org/wiki/Help_America_Vote_Act) Act).

# Basic Design Goal

The basic high level design goals are:

* The voter can validate the accuracy of their vote and its proper tally at any time
* After all polls close, anyone with access to the open-source public repository can count the votes
* There is both a paper and electronic trail with the necessary security attributes
* The system:
  * can support any vote counting [methodology](https://electology.org/library), including full UVBM systems
    * VOTES integrates different vote counting methodologies at any geographical/geopolitical overlay
  * is incrementally adoptable at different geographical/geopolitical overlays/levels
  * scales well, is secure, and ensures election accuracy and transparency
  * easily testable - simulations can be run at will
* Create a solution that is usable in the 2020 US election

# Status - 2017/03/20

VOTES is currently in the design phase - still working out the basics.
* Looking for volunteers to help layout basic business plans and technical designs
* See the [docs](https://github.com/PacemTerra/votes/tree/master/docs) directory for more information
* There is also a [wiki](https://github.com/PacemTerra/votes/wiki) (currently contains more or less the same information worded differently)
* There is a [votes-dev](https://groups.google.com/forum/#!forum/votes-dev) Google Group for public discussion.  Email me at windoverwater at gmail dot com for more private communication.
