# VoteTrackerPlus&trade;

[![CodeQL](https://github.com/OpenVotingTechnologyGroup/VoteTrackerPlus/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/OpenVotingTechnologyGroup/VoteTrackerPlus/actions/workflows/codeql-analysis.yml)

VoteTrackerPlus&trade; (a.k.a. VTP or VoteTracker+&trade;) is a 100% open source project that offers a verifiable guarantee directly to the voter that their ballot is correctly cast and tallied.  This guarantee directly increases the security, accuracy, and trustworthiness of elections regardless how they are held.

All types of elections are supported: traditional in-person paper based, mail-in, absentee, internet voting (iVoting) with or without paper, etc.  Currently four [tally algorithms](docs/tally-comparison.md) are supported in both single and multi-seat contests: plurality, sequential Rank Choice Vote, proportional RCV (STV), and pairwise Condorcet.

VTP cryptographically and anonymously tracks the per contest votes, supplying real [E2EV][E2EV.md] for voters and election officials.  VTP is a software only product comprised of backoffice plugins with voter and election official frontend facing components.  VTP can leverage existing election hardware infrastructure to the extent that the OEM manufacturers allow and support the installation of the VTP plugins.

Read the [pitch](docs/pitch.md), an [executive summary](https://docs.google.com/document/d/1vNaitQpqWkAESnY_DFsIbUO_yz1K_QZ53JBhXiGsi3E), ask for a live demo, or download the repos and run your own live demo.  The demo consists of separate python uvicorn web and tabulator servers running on Linux or MacOS, the web server providing a iVoting experience for any LAN/WAN connected devices.  End voters can vote a demo ballot containing 4 plurality and one RCV contest.  As it is a demo, with the tabulation server running in demo mode voters can tally the election at any time and verify that their ballot has been cast and tallied as intended, all within a single demo experience.

The VoteTrackerPlus project is comprised of a four or more git repositories:

| Git Repository | Contents | Development Notes |
| --- | --- | --- |
| an ElectionData git repository tree | Contains the ElectionData - the definition of the election (address, contest, and tally information etc); all blank ballots; all Cast Vote Records (contest CVR's) and ballot receipts | See [VTP-mock-election.US.17](https://github.com/OpenVotingTechnologyGroup/VTP-mock-election.US.17) or [VTP-mock-election.sRCV.1](https://github.com/OpenVotingTechnologyGroup/VTP-mock-election.sRCV.1) as examples |
| [VTP-web-api](https://github.com/OpenVotingTechnologyGroup/VTP-web-api) | Contains the python FastAPI & uvicorn based web API | main branch has linear history with signed commits |
| [VTP-web-client](https://github.com/OpenVotingTechnologyGroup/VTP-web-client) | Contains the html/css/javascript client front end | main branch has linear history with signed commits |
| [VoteTrackerPlus](https://github.com/OpenVotingTechnologyGroup/VoteTrackerPlus) | Contains the python based backend | main branch has linear history with signed commits |

See the [src/vtp/README.md](src/vtp/README.md) file in this repo for more software/technical details.

See the [VTP-dev-env git repo](https://github.com/OpenVotingTechnologyGroup/VTP-dev-env) for overall project level information.  That repo also includes a Makefile with the necessary commands to clone everything and run a mock VTP election.  The demo includes the ability for participants to cast ballots in parallel via a simulated in-person voting center with VTP ballot scanners and one tabulator.

## 1) Overview

VoteTracker+ is a distributed, open-source vote and [Cast Vote Record][Cast Vote Record] (CVR) integrity and tracking system to support public [elections](https://en.wikipedia.org/wiki/Election).  It enables verifiable, accurate, secure and transparent elections with a complete [End-to-End Verifiable](https://en.wikipedia.org/wiki/End-to-end_auditable_voting_systems) (E2EV) solution - see [docs/E2EV.md][E2EV.md].  VoteTracker+ maximizes the transparency and trust of an election throughout the election process by:

* allowing each voter to verify that their ballot is electronically cast, collected, and counted as intended
* allowing each voter and all election officials to verify the tally of all the ballot questions
* allowing each voter to inspect their neighborhood for fraudulent voters and/or addresses
* allowing each voter and all election officials to inspect all the voter names and addresses across the entire electorate for possible voter and ballot fraud
* cryptographically associating the anonymous paper ballots with the anonymous VoteTracker+ digital copies, insuring that neither set is tampered or fraudulently altered as well as supplying a third copy directly to the voter themselves, thus creating 3 separate copies of the anonymous but cryptographically signed ballot data

VoteTracker+ is an open source distributed database/repository and application that supports:

* full End-to-End validation (E2EV) of the paper and digital ballots - see [docs/E2EV.md][E2EV.md] for more details
* storing all the digitally interpreted scans of the paper ballots in a secure and anonymous manner
* executing the tally of all the races via 100% open source software contained within the same repositories as the ballot data
* creating blank ballots as a function of address
* (Aspirationally) storing the address and name of all the voters who cast a ballot without the association of any other information - the ballots are 100% anonymous
    * Ideally, if there is a previous election, VoteTracker+ would track the voter's name and address across elections allowing greater insight and transparency into potential voter and election fraud


VoteTracker+ is NOT a:

* voter ID solution
* voter registration solution
* ballot scanner nor contains ballot scanning software - VoteTracker+ receives the interpreted ballot from the ballot scanner, or in the case of iVoting, from the VTP web interface itself
* replacement for paper ballots - VoteTracker+ requires the balloting process to start and end with a paper ballot

An open source ledger based voter ID and registration solution is covered by the [RegistrationTrackerPlus](https://github.com/OpenVotingTechnologyGroup/RegistrationTrackerPlus) project.

## 2) 10,000 Foot Overview

The VTP root repo (this repo) is meant to be directly integrated via a git submodule with a VTP ElectionData directory tree which is comprised of one or more git submodules (though as of this writing and stage of agile software development, an OS level symbolic-link is typically used instead).  An VTP ElectionData tree is a directory tree that _componentizes_ the backend election configuration data into separate GGOs (Geopolitical Geographical Overlays - NIST calls this a [geopolitical unit](https://pages.nist.gov/ElectionGlossary/#geopolitical-unit)).  Each GGO can have is its own [RBAC](https://en.wikipedia.org/wiki/Role-based_access_control) authority or share another GGO's RBAC.  Independent of the GGO components the ElectionData tree supports arbitrary git submodule componentization which ultimately allows a [Voting Center](https://pages.nist.gov/ElectionGlossary/#vote-center) to operate completely disconnected from an external computer network.

A sample mock ElectionData repo can be found at [VTP-mock-election.US.10](https://github.com/OpenVotingTechnologyGroup/VTP-mock-election.US.10).

A diagram representing the high level in-person voter experience is located [here](https://drive.google.com/file/d/1-vKSE89R6DGvIs2JduyOt1AojmEXongL/view?usp=sharing) (Google Drive).

A diagram representing the high level mail-in ballot workflow is located [here](https://drive.google.com/file/d/107M8GcjGfCZ7Vu1j__OT7xYtE-D-xiia/view?usp=sharing) (Google Drive).

## 3) Demos

There are two demos available for play.  The first demo is command line based and self contained in the VoteTrackerPlus repo.  The Makefile there has more details.  The demo does require a VTP ElectionData tree for storing the election configuration and election data.

The second demo is more involved and requires wiring the three VTP code repos together with a VTP ElectionData tree.  This demo allows participants to cast votes on their own personal smart devices as well as validate their ballot receipts and tally contests.  Depending on the network configuration, this can be a live test over the internet or a local only live test disconnectedd from the internet using an isolated router.

## 4) Additional Details

For a more detailed overview, see the file [./docs/project-overview.md](./docs/project-overview.md) in this git repo.  The docs folder also contains the current [pitch](./docs/pitch.md) as well as an [informal security description](./docs/informal-security-description.md).  There is a high level scurity threat model located at [VoteTracker+ Threat Model Mind Map](https://mm.tt/1939443508?t=DuNY3bTVbg).  See [docs/E2EV.md](docs/E2EV.md) for more examples of the current basic command line interface.

VoteTracker+ is intended to be compliant to the sensible extent possible [NIST](https://en.wikipedia.org/wiki/National_Institute_of_Standards_and_Technology)'s [voting](https://www.nist.gov/itl/voting) efforts.  With funding the intent is to be compiant with NIST's [Special Publication 1500-100](https://pages.nist.gov/ElectionResultsReporting/), Election Results Reporting Common Data Format Specification Revision 2.

VoteTracker+ will attempt to leverage as much code and prior art as possible. There are several possible alternatives for standing up a pilot; if you have suggestions please get in touch.

## <a name="ElectionGuardb"></a>5) Other Voting Solutions

The following is a short and incomplete list of other voting projects that are of relevance:

* [ElectionGuard](https://freeandfair.us/electionguard/) 
* [Helios Voting](https://heliosvoting.org/) 
* [Pret-a-Voter](https://en.wikipedia.org/wiki/Pr%C3%AAt_%C3%A0_Voter) 
* [Scantegrity](https://en.wikipedia.org/wiki/Scantegrity) 
* [STARVote](https://www.usenix.org/conference/evtwote13/workshop-program/presentation/bell) 
* [VotingWorks](https://www.voting.works/) (and [VotingWorks Suite](https://docs.voting.works/vxsuite/))

The differences between VoteTracker+ and blockchain and other encrypt-the-data-at-rest solutions such as ElectionGuard are particularly and important to note.

Regarding blockchain solutions, blockchains have as a fundemental design goal the existance of private keys that conver private ownership.  This is the opposite of a basic principle of public voting - the absense of ownership of the ballot.  The ballots of public elections need to remain anonymous.  In addition that are ownership questions of who actually owns the blockchain and what can happen to the blockchain when there is collusion of a majority of the minors - when a major of the minors do not like the outcome of an election.

Regarding ElectionGuard, ElectionGuard is based on the paper [Simple Verifiable Elections](https://www.usenix.net/legacy/events/evt06/tech/full_papers/benaloh/benaloh.pdf).  Such solutions are based on independently encrypting the individual CVR's of the ballot (encrypting the ballot data at rest) and with the necessary inclusion of a [Device Challenge](https://github.com/phayes/benaloh-challenge) implementation to add a layer of trust for the voting machines that perform the encrypting.  VTP is less complex in that the CVR's are never encrypted and as such no Benaloh Challenge is required.  Voters get direct access to the real and final per contest CVR digests as the CVRs need not be encrypted since the voter's CVR's are effectively anonymized amongst 99 other sets of contest CVRs.  No encryption / decryption is required for the VTP data-at-rest portion even while significant encryption occurs in the VTP data-in-movement portion much like today's commercial/military grade encrypted network connections.

In addition ElectionGuard is not based on a Merkle Tree.  VTP adds a significant layer of security and trustworthiness via a Merkle Tree implementation in that the entire change history is stored in the public Merkle Tree ledger.  However, unlike cryptocurrencies which are also Merkle Tree based but which are also based on [blockchain](https://en.wikipedia.org/wiki/Blockchain) technology, VTP is not based on blockchain technology and contains no blockchain [implementation/code](https://github.com/dragonchain/dragonchain).  This again results in VTP being less complex than blockchain solutions while also not subject to the significant issues that blockchains implementations have with voter and ballot anonymity.

Finally, unlike the ElectionGuard and blockchain voting implementations, VTP is anonymized in time both in an absolute sense as the ballot data contains no date-time information and via the Merkle Tree chain itself as the CVRs are randomized in linkage order.

For more information contact Sandy Currier at: sandy at osetinstitute dot org

## 6) Development

See the [src/vtp/README.md](src/vtp/README.md) for notes regarding running and writing code.

## 7) Status - 2022/07/19

VoteTracker+ is currently in the early design phase with a downloadable CLI demo. The current priorities are:
* Technical peer reviews
* Recruiting contributing developers and UX designers, specifically a javascript engineer to provide a GUI demo support
* Funding

Crowdfunding is also possible - a preliminary project video is available at [https://www.youtube.com/watch?v=V0EuZHNHZ6A](https://www.youtube.com/watch?v=V0EuZHNHZ6A)

VoteTracker+ is currently using GitHub's [project planning for developers](https://github.com/features/issues) for the [VoteTracker+ Project Plan](https://github.com/orgs/OpenVotingTechnologyGroup/projects/1/views/1).  The project pages are currently private - get involved or join the team to gain access to it.  :-)

[Cast Vote Record]: https://pages.nist.gov/ElectionGlossary/#cast-vote-record
[E2EV.md]: docs/E2EV.md
