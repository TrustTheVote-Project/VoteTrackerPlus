# Outline
1) What is VOTES?
2) What is unique about VOTES?
3) VOTES is and leverages open source software
4) How does VOTES work?
5) End-to-End Voter Validation (E2EV)
6) High Level Tech Summary of Scanning a Ballot
7) Security
8) What is the KickStarter campaign funding?
9) Why raise $100,000?
10) Who is behind VOTES? 

# 1) What is VOTES?

VOTES is a distributed, open-source [voting](https://en.wikipedia.org/wiki/Voting) system that enables transparent, secure, and accurate elections with full voter based [End-to-end](https://en.wikipedia.org/wiki/End-to-end_auditable_voting_systems) verifiable (E2EV) ballots.  VOTES maximizes the transparency and trust of an election throughout the election process by:

- allowing each voter to verify that their ballot is electronically cast, collected, and counted as intended
- allowing each voter to verify the tally of all the ballot questions
- allowing each voter to inspect their neighborhood for fraudulent voters and/or addresses
- allowing election officials to inspect all the voter names and addresses across the entire electorate for possible voter and ballot fraud
- cryptographically associating the anonymous paper ballots with the anonymous VOTES digital copies, insuring that neither set is tampered or fraudulently altered as well as supplying a third copy directly to the voter themselves, thus creating 3 separate copies of the anonymous but cryptographically signed ballot data

VOTES is an open source distributed database/repository and application that supports

- full End-to-End validation (E2EV) of the paper and digital ballots
- storing all the [cast vote records](https://pages.nist.gov/ElectionGlossary/#cast-vote-record) (CVR) in a secure and anonymous manner
- executing the tally of all the races via 100% open source software contained within the same repositories as the ballot data
- creating blank ballots as a function of address
- storing the address and name of all the voters who cast a ballot without the association of any other information - the ballots are 100% anonymous

VOTES is NOT a:

- voter ID solution
- voter registration solution
- ballot scanner nor contains ballot scanning software - VOTES receives the interpreted ballot from the ballot scanner, which could be a traditional mechanical scanner, smart phone application, or manually from an election official
- replacement for paper ballots - VOTES requires the balloting process to start with a paper ballot

VOTES is implemented as a distributed set of repositories containing open-source applications that store and process the [cast vote records](https://pages.nist.gov/ElectionGlossary/#cast-vote-record).  These repositories are managed as a distributed [Merkle tree](https://en.wikipedia.org/wiki/Merkle_tree) database that contains a full ledger history of all the transactions that have occurred during the election process, nominally starting months prior to election day.  The Merkle tree contains a full change history of the following components that comprise a VOTES based election:

- The GIS information for each geographical geopolitical overlay (GGO) boundary (the state, county, town, school district, precinct, etc boundaries).  This includes the capability to automatically print blank ballots as a function of address.
- All the software applications relavent to the election, including for example the application to tally each ballot question, regardless of tally methodology be it plurality, ranked choice, approval, etc.
- A repository of the  anonymous cast vote records as election data
- A repository of the names and addresses only of the individuals who have voted as election data

In summary, the VOTES distributed repositories store both the open source software and the data that comprise the entire election process, from months prior election day, the election day itself, and post election day as additional ballots may be counted or recounted.  VOTES also handles election data being legally challenged and redacted, again recording such actions transparently in the same Merkle tree databases.

# 2) What is unique about VOTES?

There are several different efforts and products that offer secure elections and E2EV (though not necessarily end-voter based E2EV), such as [Helios Voting](https://heliosvoting.org/), [Scantegrity](https://en.wikipedia.org/wiki/Scantegrity), [Pret-a-Voter](https://en.wikipedia.org/wiki/Pr%C3%AAt_%C3%A0_Voter), [STARVote](https://www.usenix.org/conference/evtwote13/workshop-program/presentation/bell), and [ElectionGuard](https://freeandfair.us/electionguard/).  And there are many DIY home voting initiatives as well.  Every effort is worth considering and helps advance the science and trustworthiness of digital voting and election systems.  All such efforts are worthwhile as digital based voting is a challenging and complicated space technically, politically, and user experience wise - it is ripe for a disruptive solution.  To help understand a fundamental aspect of any digital voting solution, digital solutions can be divided into four basic types:

- Type 1 - those without a paper ballot which create only one source of truth stored as digital information (ignoring data backups, redundancy, etc).  THIS IS NOT RECOMMENDED
- Type 2 - those that require a paper ballot and create a single digital copy of it (ignoring backups, data redundancy etc), creating two sources of truth, one paper and one digital, that are either directly or indirectly associated or not, with the both data and software not being open source.  BETTER, BUT NOT GOOD ENOUGH.
- Type 3 - similar to number 2, but includes encryptions and private keys to allow some type of inspection by some type of third party.  MAYBE BETTER, BUT ADDS COMPLEXITY AND VULNERABILITIES, INCREASING THE ATTACK SURFACE, AND DECREASING EASE OF UNDERSTANDING AND PERHAPS TRANSPARENCY
- Type 4 - those that require a paper ballot and create a digital copy of it with multiple independent copies of the truth, owned by different entities, distributed back to the voters themselves, without private key based encryption.  BEST

In addition, there is the important aspect of who can be trusted in an election, with one important constituite being the voter themselves.  Other important constituites are the election officials that staff/handle the physical ballots, the federal government that approves the election results, and the ballot scanning device manufacturer.  Note - VOTES is not a ballot scanning device manufacturer.

Currently only VOTES is a type 4 election system.  With VOTES there are three separate copies of the ballot data:

- The first is a paper ballot controlled and secured by the election officials.
- The second is a digital copy of the personally voter-approved cast vote record of their ballot stored in the VOTES repository.   The data-at-rest aspects of this digital copy is controlled and secured via a Merkle tree based solution and stored as 100% open source software that is also contained in the same repository as the ballot contents.  The data-in-movememt aspects of this data is secured operationally throughout the entire election process (typically many months).
- The third copy is a partial copy of the ballot data handed back to the voter on a 8.5"x11" sheet secured by the cryptographic GUIDs (Global Unique Identifiers) and digests generated by VOTES.

With these three independent sources of truth, a compromise by any one can be validated by the other two.  In addition and most importantly the voter themselves can validate their own specific ballot as well as the tally of their ballot without relying on the other entities!  This is part of the power of three copies of the ballot contents with one being literally in the hands of the voters themselves.

An additional fundamental aspect of the different types of digital voting systems is whether or not the actual ballot contents are being encrypted and thus later decrypted.  It is an important design aspect of VOTES that it is not encrypting any of the ballot contents that many of the other systems encrypt.  When the ballot contents are encrypted, then one must trust both the decryption process as well as the owners of the private keys needed to perform the decryption.  With type 3 digital voting solutions the electorate still needs to trust someone else to perform the decryption and the tally.  With type 4 digital solutions and with VOTES in particular, all the voters vsn perform the tally as well as validate their specific ballot on their personal smart device, including the official copies of the VOTES data owned/controlled by the election officials.  All the voters and all the election officials, including the federal government itself, have all the same data.

This is true E2E verification from the point of view of the voter.

# 3) VOTES is and leverages open source software

Like other digital voting election systems, VOTES is 100% open source.  With funding the initial plan is understand and leverage as much existing open source code as possible, starting with [VotingWorks](https://voting.works/) open source [GitHub repositories](https://github.com/votingworks/).  All the VOTES code will also be stored back in GitHub for other projects to leverage as well.  As mentioned below, it may be the case that other voting systems adopt VOTES as a method of bringing even greater trust and transparency into elections.

# 4) How does VOTES work?

The following three scenarios describe how VOTES works a) from the POV of in person voting, b) from the POV of mail-in voting (absentee, early, etc), and c0 from the POV of an election official.  Section 5 describes E2E end-user verification in more detail while section 6 goes into even greater technical detail of an initial VOTES prototype leveraging the Git open source project.

## 4a) Physical voting center example - what a voter will experience in person

The following is a high level walk through of what a voter would experience when casting their vote in person at a voting center employing VOTES:

- A voter enters a voting center and proceeds to location #1.  S/he supplies their registered name and address (and whatever additional identification is required).  Upon successful identification of the voter and their name and address, the voter receives their address specific ballot.  Their name and address is recorded in the VOTES repository at this time.
 
- The voter proceeds to location #2 to privately fill out the ballot.  No active recording devices are allowed caveat local regulations to the contrary.
 
- The voter proceeds to location #3 and inserts their ballot into the ballot scanner, which is not part of VOTES.  S/he privately reviews the electronic interpretation of their ballot.  At this point the voter can accept or reject the digital scan of their paper ballot.  If the voter rejects the interpretation of the scan, the ballot is voided and s/he obtains a new blank ballot, returning to location #2 to try again.  If the voter accepts the interpretation of the scan, the physical ballot is accepted and the scan of the ballot is permanently stored in VOTES.  The scanner will then print a sheet of paper with 100 rows of ballot data on it.  The scanner will also privately display to the voter the offset in the sheet of their specific ballot.  Technical details of this step is described in section 5 below.
 
- The voting center optionally offers location #4, where a voter can place their sheet face down on a VOTES scanner which is not a ballot scanner.  Unlike location #3 that validates the interpretation of the scan of the ballot and updates the VOTES database with the new ballot, location #4 solely validates that the voter's handout which includes their ballot as well as 99 other ballots.  Specifically all 100 rows of ballot data is validated against the live VOTES Merkle database for the election.  The VOTES scanner at location #4 will display an invalid indication if any of the ballot data on the voter's handout is not currently correct in the live VOTES databases.

**Three important clarifications:**

- There is no publicly available 'image scan' of the paper ballot - VOTES only makes available the interpreted ballot and the digest pairs.  The actual image scan is controlled by the ballot scanner manufacturer and the election officials
- Once all the polls have closed and enough ballots have been cast and the voters' names and addresses have been recorded, the VOTES repositories can be made publicly available.  The repos include the tally algorithms that are executed to tally the election, the cast vote records, and, independently, all the voter names and addresses. (There is 100% no connection between a voter's name and address and their ballot anywhere in VOTES or on the printed ballots.)  The repo allows every voter to once again verify that their ballot is correctly recorded using their public digests as well as to execute the tally on their smart devices. It also allows neighborhoods to self-patrol for fraudulent people or addresses as well as state and federal investigations to search for unauthorized or fraudulent registered voters across the entire electorate.
- As the hours and days pass and additional ballots continue to be scanned and added to the VOTES Merkle based repositories, rolling public updates continue, allowing for constant E2EV as well as intermediary ballot tallies.  Note that all citizens and election officials can download the latest repositories and verify and tally the election results.

## 4b) Vote by mail Example - what happens to the ballot

In vote-by-mail scenarios, the completed ballots are mailed to the election officials.  Note that in vote-by-mail scenarios trust has already been placed on the electorate such that no one will sell their ballot nor impersonate another voter, particularly in a verifiable manner to a third party.  Using VOTES will not eliminate those risks, but VOTES will give mail-in-voters the ability to verify that their ballot has been entered and tallied correctly.  And it makes it easier for neighbors and friends and family to spot impersonated ballots by making the voter records easily and immediately accessible once all the polls close.

In vote-by-mail scenarios election officials will scan the ballots for electorate.  Depending on the time and budget available for handling vote-by-mail ballots, election official can mimic the in-person workflow above, automate various steps, or skip various steps.  For example, the human validation of the scan of the ballot can be skipped.  Or, the voter handout can still be printed and mailed back to the voter.  Their row offset could be separately returned, returned in the same envelope, transferred privately in person at some later date, or discarded.

Regardless of whether a vote-by-mail voter receives their ballot digest, once all the polls close the VOTES repositories are made publicly available.  Voters who know their digest can still check their ballot, and all the voters can still tally all the races and check the voter names and addresses in their neighborhood for potential inconsistencies.  This latter check offers transparency into vote-by-mail ballots as soon as the VOTES repository is available.

## 4c) How does an election official interact with VOTES?

Pre-election day, VOTES supplies the framework in which all the geographical/geopolitical overlays (the GGO's, e.g. the states, counties, municipalities, cities, towns, districts, precincts, school districts, etc.), can easily compose the ballots for their specific constituents based on address or other criteria in an iterative, collaborative, and independent manner.  VOTES natively stores the GIS information necessary to map a voter's address to all the containing GGO's and can automatically create the correct ballot for any address whenever needed.  Note that the software development framework tests the blank ballot creation and layout prior to any changes that make it into production.  The ballot scanning/scanner vendor can also participate in live, daily testing of scanning ballots.

During election day, VOTES can generate address-specific ballots (location #1), ingest scanned cast ballots and help end voters correct un-scannable ballots (location #3), and verify the voter's ballot as been properly collected (location #4).

After all the polls close, VOTES already contains the tested, verified, and open-source tally algorithms for each race across the GGO's as necessary.  The tallies can be executed by any election official or voter who has access to the VOTES repositories.  This greatly reduces the time and cost to tally an election, even if the tally is ranked choice.

# 5) End-to-End Voter Validation (E2EV)

VOTES directly supports E2EV by providing three separate copies of the voter's ballot.  The first is the physical ballot controlled by the local election officials.  The second is the cast vote record as approved by the voter and stored in the VOTES public repository.  The third copy is a partial copy of the VOTES data given to the voter on a 8.5"x11" paper containing encrypted and randomized digests of the voter's ballot.  These three different copies in addition the inherent properties of the Merkle tree database support multiple and different E2EV pathways.  The physical ballots can be independently sampled and compared to the electronic copies both in count, content, and via statistical sampling.  Each voter can validate their individual paper copy against the public repository as well.  In addition, voters in possession of their ballot's row index can inspect their specific digital ballot.

And with the open source copy of the names and addresses of the entire electorate, election officials as well as any voter can analyze by various methods the accuracy of those names and addresses.

# 6) High Level Tech Summary of Scanning a Ballot

This section is a technical summary of how a ballot is added to the VOTES database and how the voter's handout sheet is generated.  This section is based on a VOTES prototype leveraging the open source Git project so to be more universally explainable.  Different potential future tooling frameworks may result in different implementations.

At location #3, the scan station, after the voter accepts the digital scan of the ballot, several separate but related technical workflow will occur.  Given a VOTES prototype based on Git, each ballot question gets a Git submit commit with the voter's selection recorded as a block of cleartext JSON within the comment section (there is no file being committed).  The Git commit time is set to null on all the commits and each commit for each question is on a separate Git branch.  Nominally there are a 200 (N) ballots times X questions committed on unique branches but not merged at any given time.  Pushing the commits upstream is an election based operational TBD, decided later depending on data redundancy and resilience concerns.  Several separate workflows happen at this time:

A) The seal-the-ballot-and-commit workflow

This workflow will cryptographically seal the new ballot, adding it to a physical ballot Merkle tree.

- 1) The physical ballot is printed with a unique and random (but seeded specifically for this election) GUID digest for each question.  The GUIDs are also a function of the previous ballot-wide GUID generated by step 4 for the previously scanned ballot
- 2) The per question GUID is included in the Git commit comment as clear text (JSON) for each question on the incoming ballot, even if the voter's selection is blank.
- 3) Each Git commit digest is then printed on the physical ballot as well, below the per question GUID.
- 4) The physical ballot is also printed with a ballot unique GUID which is a function of all the GUIDs and commit digests.  This ballot GUID is used for the next ballot in a Merkel DAG manner.

Thus there is a Git based Merkle tree per question in the VOTES repository containing the same GUID as printed on the ballot as well as a physical ballot Merkle tree.

B) The print-the-voter-sheet workflow

This workflow creates the voter's physical handout.

The previous 200 ballots times X question commits are randomly selected/divided into 99 rows along with the voter's incoming ballot, totaling 100 rows.  Note - half of the Git unmerged questions are randomly ignored.  The voter sheet is printed and the voter's row number is privately revealed to the voter only via a digital screen.  The rows have both the Git commit digest AND the physical ballot question GUIDs.

Note that in mail-in-ballot scenarios, 1) the voter sheet printing can be disabled completely (save paper, cloak more); 2) the row number only can be disabled and not displayed; or 3) an encrypted version of the row number can be printed on the sheet when there are multiple private keys, at least one being held by the local election officials and at least being held by the voter themselves.  Note - it is a TBD how to manage the voter's public key in this scenario.  It is also a TBD if such a capability can be supported for mail-in ballots.  If such a future capability is possible to support, there are several constraints that would need to be enforced based on the dual private key nature of the encryption and the requirement that the voter be properly identified and the act of decryption be properly recorded with adequate transparency.

C) The merge-the-commit workflow

This workflow adds the voter's ballot to the VOTES repositories.

Lastly, a random set of X questions are selected and merged into the local voting center Git branch.  This will randomize the native Git based branch DAGs.  Having the unmerged pool be greater than what is printed on the voter sheet increases the difficulty of reverse data mining if multiple voter sheets are combined.  This will return the unmerged pool back to 200 from 201 ballots.

Note that during these workflows, the Git repo can be pushed upstream to a remote server if so configured.  Or the file system itself can be backed up, however data redundancy and data resilience have been designed.  (This is another operational design decision to be decided during election planning.)

# 7) Security

The security of an election system is paramount.  The election system must supply a tamper proof and accurate election in both reality and appearance.

In addition, the security model must also be easily understood and trustable by the casual voter at a high level while its efficacy be completely verifiable and provable by cryptographic experts at all levels.

And both these domains are not static - they are continually evolving and being re-evaluated in a transparent open-book manner, available to all voters and election officials.  That is how and why VOTES technically looks like it does.  In summary:

- VOTES is 100% open source
- the VOTES repositories include all the code to tally the vote and all the data that comprises an election
- VOTES requires a paper ballot that is tracked with the digital electronic interpretation of the ballot
- all the ballot data at rest is un-encrypted and anonymous - no private keys are required to decrypt anything
- the base Merkle Tree is protected by SHA-256 encryption combined with additional security protocols 
- all data in movement is done so under standard and well understood and fully hardened [PKI](https://en.wikipedia.org/wiki/Public_key_infrastructure) (public-private key), [PGP](https://en.wikipedia.org/wiki/Pretty_Good_Privacy) (Pretty Good Privacy), and the latest [TSL](https://en.wikipedia.org/wiki/Transport_Layer_Security) protocols with additional app-level 2FA

In short, VOTES is **NOT** proposing, creating, or adding a new encryption protocol or scheme - it is more simply leveraging existing military and industrial best practices.

For a more security information, see the file [./docs/informal-security-description.md](./docs/informal-security-description.md) in this git repo.

# 8) What is the kickstarter campaign funding?

The primary goal of the kickstarter campaign is to raise the funds to develop VOTES into a demonstrable prototype.  With a working prototype VOTES can be demonstrated to city and state election officials and the public at large.  It will maximize that a VOTES or similar are derivitive solution be developed as soon as possible.  Clear and free and transparent peer review by the general public is key.  Since VOTES is a disruptive solution, a working prototype greatly increases the ability to win an RFPs (Request For Proposals) to create a VOTES solution for an upcoming election.  By winning one or more such RFPs, the VOTES project will receive the funding necessary to actually be used in a public election.

Fundraiser Disclaimer:

**THIS FUNDRAISING CAMPAIGN IS RAISING FUNDS FOR THE RESEARCH AND DEVELOPMENT OF AN OPEN SOURCE, E2EV ELECTION SYSTEM CALLED VOTES.  IT IS NOT FUNDING THE IMMEDIATE AND DIRECT PRODUCTIZATION OF ANY SUCH ELECTION SYSTEM.  PLEDGES ARE CONSIDERED AN DONATION/GIFT TO FURTHER THE DEVELOPMENT OF VOTES WITH NO EXPECTATIONS OF ANY SPECIFIC PRODUCT TIMELINE, DELIVERY, OR EVEN EVENTUAL DELIVERABILITY.  A DONATION TO THIS PROJECT IS AN EXTREMELY RISKY INVESTMENT IN A NON-PARTISAN, OPEN SOURCE, ELECTION AND VOTING SYSTEM !**

Election systems need to go through a separate and extensive RFP process in every voting juridiction, which for the United States numbers more than 8,000.  This campaign is an attempt to get VOTES into an initial set of RFP conversations and then into a working prototype.

If no RFP is signed, a secondary goal is that the kickstarter funding will allow enough technology to be created and demonstrated such that some form of public or private investing can occur, or for an existing election system vendor to independently adopt the technology.

Regardless of any financial outcome, a fundamental goal is to make elections more transparent, secure, and trustworthy.  Even if our funding goal is not reached, the kickstarter campaign can be considered successful if VOTES is reviewed by more voters, election scientists, and technology experts.  Being open source, such a review is critically important for any next generation digital election solution and can serve as an important open source reference.

# 9) Why raise $100,000?

The first $100,000 allows me, Sandy Currier, to hire software developers to create an initial prototype of VOTES.  It will also allow me to work on VOTES for about one year in a mostly unpaid role.  For each additional $25,000 raised, additional software development subcontracting can be added for developing the VOTES prototype.  The more resources that are raised, the more work can be done in a shorter time frame.

# 10) Who is behind VOTES?

Sandy Currier started working on VOTES after a 2016 Thanksgiving Holiday gathering.  A lively discussion occurred concerning whether anyone was sure their vote had ever actually been counted, and if block-chain technology could be used verify that.  He rejected block chains as a viable solution and was eventually hoodwinked into accepting the challenge of looking into open source, transparent, E2EV election systems, and reporting back the following year.

Over the next few years Sandy investigated the history and current state of the science and art of voting technologies.  He sat in on numerous meetings at MIT concerning voting policies and election systems.  He discussed ideas with MIT professors, election officials, and private sector experts.  He is now trying to work on VOTES full time.

Sandy graduated from MIT in 1986 and has worked in the high-tech sector for 35 years.  He's developed solutions for start-ups, Fortune 500 companies, and has run his own software company.  His bio is available at https://www.linkedin.com/in/toolsmith/Outline
