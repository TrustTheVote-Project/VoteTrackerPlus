# VoteTrackerPlus

A Verifiable Open Technology Election System.  Also known as VoteTracker+ or VTP as an acronym.

# Overview

VoteTrackerPlus is a distributed, open-source [voting](https://en.wikipedia.org/wiki/Voting) system that enables transparent, secure, and accurate elections with full voter based [End-to-end](https://en.wikipedia.org/wiki/End-to-end_auditable_voting_systems) verifiable (E2EV) ballots.  VoteTrackerPlus maximizes the transparency and trust of an election throughout the election process by:

* allowing each voter to verify that their ballot is electronically cast, collected, and counted as intended
* allowing each voter and all election officials to verify the tally of all the ballot questions
* allowing each voter to inspect their neighborhood for fraudulent voters and/or addresses
* allowing each voter and all election officials to inspect all the voter names and addresses across the entire electorate for possible voter and ballot fraud
* cryptographically associating the anonymous paper ballots with the anonymous VoteTrackerPlus digital copies, insuring that neither set is tampered or fraudulently altered as well as supplying a third copy directly to the voter themselves, thus creating 3 separate copies of the anonymous but cryptographically signed ballot data

VoteTrackerPlus is an open source distributed database/repository and application that supports

* full End-to-End validation (E2EV) of the paper and digital ballots
* storing all the electronically interpreted scans of the paper ballots in a secure and anonymous manner
* executing the tally of all the races via 100% open source software contained within the same repositories as the ballot data
* creating blank ballots as a function of address
* storing the address and name of all the voters who cast a ballot without the association of any other information - the ballots are 100% anonymous
    * if there is a previous election, VoteTrackerPlus can track the voter's name and address across elections allowing greater insight and transparency into potential voter and election fraud


VoteTrackerPlus is NOT a:

* voter ID solution
* voter registration solution
* ballot scanner nor contains ballot scanning software - VoteTrackerPlus receives the interpreted ballot from the ballot scanner, which could be a traditional mechanical scanner, smart phone application, or manually from an election official
* replacement for paper ballots - VoteTrackerPlus requires the balloting process to start and end with a paper ballot

# Additional Details

For a more detailed overview, see the file [./docs/project-overview.md](./docs/project-overview.md) in this git repo.  The docs folder also contains the current [pitch](./docs/pitch.md) as well as an [informal security description](./docs/informal-security-description.md).

VoteTrackerPlus is intended to be compliant to the extent that it makes sense with [NIST](https://en.wikipedia.org/wiki/National_Institute_of_Standards_and_Technology)'s [voting](https://www.nist.gov/itl/voting) efforts (see the [HAVA](https://en.wikipedia.org/wiki/Help_America_Vote_Act) Act).

VoteTrackerPlus will attempt to leverage as much code and prior art from such projects as [VotingWorks](https://voting.works/).  It may be the case that VoteTrackerPlus will first be intergrated with VotingWorks as a proof-of-concept.

The following is a short and incomplete list of other and past voting projects:
* [Helios Voting](https://heliosvoting.org/) 
* [Scantegrity](https://en.wikipedia.org/wiki/Scantegrity) 
* [Pret-a-Voter](https://en.wikipedia.org/wiki/Pr%C3%AAt_%C3%A0_Voter) 
* [STARVote](https://www.usenix.org/conference/evtwote13/workshop-program/presentation/bell) 
* [ElectionGuard](https://freeandfair.us/electionguard/) 
* [VotingWorks](https://www.voting.works/) (and [VotingWorks Suite](https://docs.voting.works/vxsuite/))

For more information contact Sandy Currier at:  windoverwater at gmail dot com

# Development

See the [bin/README.md](bin/README.md) for notes regarding running and writing code.

# Status - 2021/02/21

VoteTrackerPlus is currently in the design phase - still working out the basics and trying to obtain credible peer reviews.  The current priorities are:
* Looking for technical, legal, and UX design peer reviews; positive, negative or neutral
* Looking for volunteers to help in any way
* Working on a kickstarter/gofundme campaign
* Looking into potential funding

The kiskstarter project is nearly complete and ready to launch.  The project video is available at [https://www.youtube.com/watch?v=V0EuZHNHZ6A](https://www.youtube.com/watch?v=V0EuZHNHZ6A).  However, the launch is being delayed until adequate peer reviews have been given so to independently establish the efficacy and viability of a VoteTrackerPlus approach to an election.  Donating money and time to a doomed project is not a good thing.  So, if you watch the above videa and/or read any of the summaries and can offer strong feedback, it would be greatly appreciated.  It is possible that many people would appreciate it.
