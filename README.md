# VOTES

A Verifiable Open Technology Election System

# Overview

VOTES is a distributed, open-source [voting](https://en.wikipedia.org/wiki/Voting) system that creates transparent, secure, and accurate elections with anonymous individually verifiable ballots.

**END-VOTER ADVANTAGES:**  Using VOTES the voter can validate their ballot as well as the tally of any contest while maintaining voter anonymity. VOTES is 100% transparent, insuring that no entity or person can mishandle or manipulate any ballot or contest.  VOTES employs multiple modern cryptographic designs and techniques to insure tamper proof transparent elections.

**ELECTION-OFFICIAL ADVANTAGES:** Using VOTES eliminates the overheads and expenses of integrating the information and data coming from individual towns, districts, etc. regarding running an election.  VOTES distributes checks and balances such that state officials control what they need to while allowing other local and federal officials to efficiently enter, test, and validate the data for which they are responsible.  VOTES also exposes the execution of the ballot count in an open-source manner such that there is full transparency to the tally.  The tally is also instantenious - once the polls close and the ballots are scanned, verifiable tallies are instantly available.  Trust in the ballots and the tally is maximized to levels only available in 100% open source projects - there is no hidden code or data.

**TECH ADVANTAGES:** VOTES allows the voter to anonymously validate their ballot and its accurate inclusion in an election.  VOTES is extremely immune to hacking and compromise due to its distributed, open-source, full-ledger bitcoin-like design.  There is no single source of truth that can be compromised from within or without.  All communication channels employ full mutual ssl via dedicated certificate authorities and channel independent multi factor authentication.  VOTES also increases the difficulty of creating a market for the purchasing and selling of ballots.  It fully supports traditional in-person balloting as well as UVBM, early, and absentee voting, and any combination thereof.

**VOTER RIGHTS/POLICY ADVANTAGES:**   VOTES is __not__ a voter identification system, but it does track in an private and double encrypted manner the voter identities per election.  Via this encrypted non-public data individual ballots can be surgically nullified or un-nullified under court supervised recounts.  With such capabilities the natural tension between extensive high-bar pre registration identification and a low effective barrier pre registration identification, particularly for disenfranchised and disadvantaged voters, is mitigated in a manner not available with current election systems.  With VOTES a state has more leeway to implement a lower barrier of voter registration while simultaneously providing a higher degree of ballot authenticity!  Regardless of illecit election official or voter activity, specific fraudulent ballots can be discovered and nullified quickly after the fact and new tallies instantly recalculated by any citizen.

**GERRYMANDERING ADVANTAGES:**  VOTES does not solve gerrymandering, but it does expose gerrymandering directly to the end voter.  While VOTES tracks ballots in an anonymous manner, the ballot is still tracked on a per precinct basis.  On any geographical/geopolitical overlay basis the ballot's gerrymandering coefficient, the degree to which the voter's ballot is either over or under represented due to gerrymandering, can be displayed.  It is also possible to project potentially different outcomes as a function of the amount of gerrymandering present per type of potential districting.  By more directly exposing gerrymandering to the end voter, VOTES indirectly helps to eliminate it.

**BUSINESS ADVANTAGES:**  VOTES can be adopted by existing election solution providers ([ESS/Diebold](http://www.essvote.com/about/), [ClearBallot](http://www.clearballot.com/), etc.), public or private agencies during the [RFP](https://en.wikipedia.org/wiki/Request_for_proposal) process for voting machines or UVBM ([Universal Vote By Mail](http://washingtonmonthly.com/magazine/janfeb-2016/vote-from-home-save-your-country/)) solutions, or anyone wishing to provide election systems/solutions.  The business model behind VOTES is a  [SaaS](https://en.wikipedia.org/wiki/Software_as_a_service) solution capable of handling national, state, town, or private elections.

VOTES is intended to be as compliant as possible with [NIST](https://en.wikipedia.org/wiki/National_Institute_of_Standards_and_Technology)'s [voting](https://www.nist.gov/itl/voting) efforts (see the [HAVA](https://en.wikipedia.org/wiki/Help_America_Vote_Act) Act).

For more information contact Sandy Currier at:  windoverwater at gmail dot com

# Basic Design Goal

The basic high level design goals are:

* The voter can validate the accuracy of their vote and its proper tally at any time
* After all polls close, anyone with access to the open-source public repository can count the votes
* There are independent paper and electronic trails with the necessary security attributes
* The system:
  * can support any vote counting [methodology](https://electology.org/library), including full UVBM systems
    * VOTES integrates different vote counting methodologies at any geographical/geopolitical overlay
  * is incrementally adoptable at different geographical/geopolitical overlays/levels
  * scales well, is secure, and ensures election accuracy and transparency
  * easily testable - simulations can be run at will
* Create a solution that is usable in the 2020 US election

# Status - 2017/07/30

VOTES is currently in the design phase - still working out the basics.
* Looking for volunteers to help layout basic business plans and technical designs
* See the [docs](https://github.com/PacemTerra/votes/tree/master/docs) directory for more information
* There is also a [wiki](https://github.com/PacemTerra/votes/wiki) (currently contains more or less the same information worded differently)
* There is a [votes-dev](https://groups.google.com/forum/#!forum/votes-dev) Google Group for public discussion.
