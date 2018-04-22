# VOTES

A Verifiable Open Technology Election System

# Overview

VOTES is a distributed, open-source [voting](https://en.wikipedia.org/wiki/Voting) system that creates transparent, secure, and accurate elections with anonymous individually verifiable ballots.  VOTES maximizes the transparency and trust of an election thoughout the election process via:

 - 100% independent paper trail
 - All software code and data is open-sourced and stored in a full ledger, distributed blockchain / version control system
   - No hidden tally points - any citizen/voter can execute the complete tally of any contest/question and inspect all ballots after all-the-polls close
 - End-to-End-Verification (E2EV) of election results with auditing
 - A secure but anonymous on-line full copy/ledger of the physical paper ballots
 - Best in class mutual SSL digital communications with independent multi factor authentication with anti-bot interrogation points

**END-VOTER ADVANTAGES:**  Using VOTES the voter can validate their ballot as well as the tally of any contest while maintaining voter anonymity. VOTES is 100% transparent, insuring that no entity or person can mishandle or manipulate any contest, ballot, or tally.  VOTES employs multiple modern cryptographic designs and techniques to insure tamper proof electronic communications while employing open source software to insure transparent and trustworthy elections.  Multiple checks and balances are employed including a full and independent physical paper trail.

**ELECTION-OFFICIAL ADVANTAGES:** Using VOTES eliminates the overheads and expenses of integrating the information and data originating from multiple towns, districts, etc. regarding running an election.  VOTES distributes checks and balances such that state officials control what they need to while allowing other local and federal officials to efficiently enter, test, and validate the data for which they are responsible.  VOTES also exposes the execution of the ballot count in an open-source manner such that there is full transparency to the tally.  The tally is effectively instantaneous - once the polls close and the ballots are scanned, verifiable tallies are instantly available.  Trust in the ballots and the tally is maximized to levels only available in 100% open source projects - there is no hidden code or data.

**TECH ADVANTAGES:** VOTES allows the voter to anonymously validate their ballot and its accurate inclusion in an election.  VOTES is extremely immune to hacking and compromise due to its distributed, open-source, full-ledger bitcoin-like block-chain design.  The VOTES technical design insures both a central authority responsible for supervising the election as well as no single source of truth that can be compromised from within or without.  All communication channels employ full mutual ssl via dedicated certificate authorities and channel independent multi factor crowd authentication.  VOTES also increases the difficulty of creating a market for the purchasing and selling of ballots by minimizing the opportunity of 3rd-party validation of ballots.  It fully supports traditional in-person balloting as well as UVBM, early, and absentee voting, and any combination thereof.

**TRANSPARENCY, TRUST, and E2EV:**   VOTES is __not__ a voter identification system, but VOTES does record the names and addresses of the voters in the public repository.  There is no coorelation between the voter-id and the cast ballot even though both are maintained by VOTES.  However, with the full ledger copy, election end-to-end-verification can proceed more efficiently and with greater scope given the homogeneity of the VOTES implementation and the VOTES connection between the specific physical ballot and the specific electronic copy and vice versa.

Since VOTES includes the tally algorithm, trust in the complete electronic portion of the election is maximized.  This is particularly true for [Rank Choice Voting](http://www.fairvote.org/rcv#rcvbenefits) tallies.  As communities and state investigate and adopt RCV, being able to do so with VOTES maximizes the transparency and trust with these more complicated tallying algorithms.

With VOTES ballot public keys, both the physical and electronic copy can be inspected and compared with complete voter anonymity.  And with the private, only at ballot scan-time, non-third-party verifiable, identification of the public key, voters can independently verify their cast ballots.

**GERRYMANDERING ADVANTAGES:**  VOTES does not solve [gerrymandering](https://en.wikipedia.org/wiki/Gerrymandering) nor the inherent shortcomings of district based plurality voting failing to achieve [proportional representation](https://en.wikipedia.org/wiki/Proportional_representation).  However, VOTES does allow the direct inspection of their __combined__ affect.  On any geographical/geopolitical overlay (GGO), any specific ballot's over or under proportional representation by party or affiliation is calculated and displayed to the end voter.  In addition, [Monte Carlo](https://en.wikipedia.org/wiki/Monte_Carlo_method) simulations of different districting maps are executed to generate the GGO's _natural_ distribution curve of the political party percentage representation via districted seats versus votes.  By providing both numbers as a function of a specific (anonymous) ballot and/or by an end user supplied address, the voter can see the direct affect of both phenomenon on either their (anonymous) ballot or at their address.

Again, VOTES does not solve gerrymandering nor the negative affects of various [voting systems](https://en.wikipedia.org/wiki/Electoral_system), but VOTES does cast light and transparency on both.  In addition, being open source and full ledger based, VOTES allows any GGO (a state, precinct, municipality, city/town, school district, etc) to experiment with, share, and leverage different voting systems and/or [tally algorithms](https://en.wikipedia.org/wiki/Ranked_voting).

**BUSINESS ADVANTAGES:**  VOTES can be adopted by existing election solution providers ([ESS/Diebold](http://www.essvote.com/about/), [ClearBallot](http://www.clearballot.com/), etc.), public or private agencies during the [RFP](https://en.wikipedia.org/wiki/Request_for_proposal) process for voting machines or UVBM ([Universal Vote By Mail](http://washingtonmonthly.com/magazine/janfeb-2016/vote-from-home-save-your-country/)) solutions, or anyone wishing to provide election systems/solutions.  The _operational_ business model behind VOTES is a  [SaaS](https://en.wikipedia.org/wiki/Software_as_a_service) solution capable of handling national, state, town, or private elections.

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

# Status - 2018/04/19

VOTES is currently in the design phase - still working out the basics.
* Looking for volunteers to help layout basic business plans and technical designs
* Working on a kickstarter campaign
* Looking into potential seed/angel funding
* See the [docs](https://github.com/PacemTerra/votes/tree/master/docs) directory for more information
* There is also a [wiki](https://github.com/PacemTerra/votes/wiki) (currently contains more or less the same information worded differently)
* There is a [votes-dev](https://groups.google.com/forum/#!forum/votes-dev) Google Group for public discussion.

