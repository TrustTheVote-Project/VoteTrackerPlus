# Outline
1) What is VOTES?
2) What is unique about VOTES?
3) VOTES is and leverages open source software
4) How does VOTES work?
5) What is the KickStarter campaign funding?
6) Why raise $100,000?
7) Who is behind VOTES? 

# 1) What is VOTES?

VOTES is a distributed, open-source [voting](https://en.wikipedia.org/wiki/Voting) system that enables transparent, secure, and accurate elections with full [End-to-end](https://en.wikipedia.org/wiki/End-to-end_auditable_voting_systems) (E2E) verifiable ballots.  VOTES maximizes the transparency and trust of an election throughout the election process by:

- allowing each voter to verify that their ballot is electronically cast, collected, and counted as intended
- allowing each voter to verify the tally of all the ballot questions
- allowing each voter to inspect their neighborhood for fraudulent voters and/or addresses
- allowing all election officials and voters to inspect all the voter names and addresses across the entire electorate for possible voter and ballot fraud

VOTES is an open source distributed database/repository and application that supports

- storing all the electronically interpreted scans of the paper ballots in a secure and anonymous manner
- executing the tally of all the races via 100% open source software contained within the same repositories
- creating blank ballots as a function of address
- storing the address and name of all the voters who casts a ballot without the association of any other information - the ballots are 100% anonymous

VOTES is NOT a:

- voter ID solution
- voter registration solution
- ballot scanner nor contains ballot scanning software - VOTES receives the interpreted ballot from the ballot scanner, which could be a traditional mechanical scanner, smart phone application, or manually from an election official
- replacement for paper ballots - VOTES requires the balloting process to start with a paper ballot

VOTES is implemented as a distributed set of repositories containing open-source applications that store and process the electronically interpreted scanned ballots.  These repositories are a distributed [Merkle tree](https://en.wikipedia.org/wiki/Merkle_tree) database/repository that contains a full ledger history of all the transactions that have occurred during the election process, nominally starting months prior to election day.  The Merkle tree contains a full change history of the following components that comprise a VOTES election:

- The GIS information for each geographical geopolitical overlay (GGO) boundary (the state, county, town, school district, precinct, etc boundaries).  This includes the capability to automatically print blank ballots as a function of each address.
- The applications to tally each question on any ballot, regardless of tally methodology be it plurality, ranked choice, approval, etc.
- A repository of the scanned/interpreted anonymous ballots themselves as data
- A repository of the names and addresses only of the individuals who have voted as data

# 2) What is unique about VOTES?

There are several different efforts and products that offer secure elections and E2EV, such as [Helios Voting](https://heliosvoting.org/), [Scantegrity](https://en.wikipedia.org/wiki/Scantegrity), [Pret-a-Voter](https://en.wikipedia.org/wiki/Pr%C3%AAt_%C3%A0_Voter), [STARVote](https://www.usenix.org/conference/evtwote13/workshop-program/presentation/bell), and [ElectionGuard](https://freeandfair.us/electionguard/).  And there are many DIY home voting initiatives as well.  Every effort is worth considering and helps advance the science and art of digital voting and election systems.  All the efforts are good as digital based voting is a very challenging and complicated space technically, politically, and user experience wise - it is ripe for a disruptive solution.  To help understand a fundamental aspect of any digital voting solution, digital solutions can be divided into three basic types:

- 1) those without a paper ballot which create only one source of truth stored as digital information ignoring data backups, redundancy, etc  (NOT RECOMMENDED)
- 2) those that require a paper ballot and create a single digital copy of it (ignoring backups, data redundancy etc), creating two sources of truth, one paper and one digital, that are either directly or indirectly bound or not bound at all (BETTER)
- 3) those that require a paper ballot, create a digital copy of it, and create multiple independent copies of truth (BEST)

In addition, there is the important aspect of who can be trusted in an election, with one important point of view (POV) being the voter themselves.  Other POVs are the election officials that staff/handle the physical ballots, the federal government that aggregates the ballot results, and the ballot scanning device manufacturer.  Note - VOTES is not a ballot scanning device manufacturer.

Currently only VOTES is of type 3.  With VOTES there are three separate copies of the ballot data: the first is a paper ballot controlled and secured by the election officials.  The second is a digital copy of the personally voter-approved interpreted digital scan of their ballot stored in the VOTES repository.  This copy is controlled and secured via a Merkle tree based solution and stored as 100% open source software that is also contained in the same repository as the ballot contents.  And the third is a partial copy of the ballot data handed back to the voter on a 8.5"x11" sheet.

With these three independent sources of truth, a compromise by any one can be validated by the other two.  In addition and most importantly the voter themselves can validate their own specific ballot as well as the tally of their ballot without relying on the other entities!  This is part of the power of three copies of the ballot contents with one being literally in the hands of the voters themselves.

An additional fundamental aspect of the different types of digital voting systems is whether or not the actual ballot contents are being encrypted and thus later decrypted.  It is an important design aspect of VOTES that it is not encrypting any of the ballot contents that many of the other systems encrypt.  When the ballot contents are encrypted, then one must trust both the decryption process as well as the owners of the private keys needed to perform the decryption.  Since the voter is not the owner of the private key, which is in stark contrast to the case with cryptocurrencies, https/TLS/ssh secure connections, etc., with type 2 digital voting solutions the electorate still needs to trust someone else to perform the decryption and the tally.  With type 3 digital solutions and with VOTES in particular, all the voters perform the tally as well as validate their specific ballot on their personal smart device or any other smart device, including the official copies owned/controlled by the election officials.  All the voters and all the election officials, including the federal government itself, have all the same data.
That is true E2EV from the point of view of the voter.

# 3) VOTES is and leverages open source software

Like other digital voting election systems, VOTES is 100% open source.  With funding the initial plan is understand and leverage as much existing open source code as possible, starting with [VotingWorks](https://voting.works/) open source [GitHub repositories](https://github.com/votingworks/).  All the VOTES code will also be stored back in GitHub for other projects to leverage as well.  As mentioned below, it may be the case that other voting systems adopt VOTES as a method of bringing even greater trust and transparency into elections.

# 4) How does VOTES work?

The following four scenarios describe how VOTES works from the POV of in person voting, mail-in voting (absentee, early, etc), from the POV of an election official, and from the POV of a voter performing E2EV of their ballot after all the polls close.

## 4a) Physical voting center example - what a voter will experience in person

The following is a high level walk through of what a voter would experience when casting their vote in person at a voting center employing VOTES:

- A voter enters a voting center and proceeds to location #1.  S/he supplies their registered name and address, and if the name and address is valid receives a blank ballot specific to their address.  Their name and address is recorded in the VOTES repository at this time.
 
- The voter proceeds to location #2 to privately fill out the ballot.  No active recording devices are allowed caveat local regulations to the contrary.
 
- The voter proceeds to location #3 and inserts their ballot into the ballot scanner, which is not part of VOTES.  S/he privately reviews the electronic interpretation of their ballot.  At this point the voter can accept or reject the scan.  If the voter rejects the scan, the ballot is voided and s/he obtains a new blank ballot, returning to location #2 to try again.  If the voter accepts the scan, the physical ballot is collected and the scan of the ballot is permanently stored in VOTES.
 
At a technical level there are several internal events that occur when the voter accepts the interpretation of the paper ballot.  1) Upon acceptance, the paper ballot is printed with unique cryptographic numbers, one per question.  The VOTES Merkle-chain includes these numbers as well as an additional cryptographic number that will be supplied to the voter.  The Merkle chain full history ledger is similar to a cryptographic block-chain used for many cryptocurrencies but without any private keys.  There are no private keys in VOTES.  2) Voters receive a 8.5"x11" paper sheet with 100 rows of digests pairs, one column per ballot question, and privately receives a row number via a private display.  The row number is their set of digests for their ballot.  There is no soft copy of their row number and only the voter privately receives the value.  3) Each row/column cell includes both the paper and VOTES per ballot digests, creating a third person hardcopy of the digest pairs.  The first copy is printed on the paper ballot, the second copy is recorded in the VOTES digital repositories, and the third copy is printed on paper for the voter.  Note that all 100 rows of digests are valid digests though not necessarily for any specific ballot, except for the voter's row which is guaranteed to be.

- The voting center optionally offers location #4, where a voter can place their sheet face down on a VOTES scanner which is not a ballot scanner.  Unlike location #3 that validates the scan of the ballot, location #4 validates that the ballot is correctly contained in the live VOTES Merkle database for the election.  The VOTES scanner at location #4 will display a valid or invalid indication of all the digests on the sheet. If the voter decides to optionally and privately enter their row number, the VOTES scanner will privately display their ballot as it has been recorded in the Merkle chains. This allows the voter to leave the voting center having verified that their ballot has been properly interpreted and entered into VOTES.

**A few important notes and clarifications:**

- There is no publicly available 'image scan' of the paper ballot - VOTES only makes available the interpreted ballot and the digest pairs.
- Election officials and/or the scanning machine vendor can optionally store the actual scan of the ballot itself.  Such a repository if it exists is not public.
- Once all the polls have closed and enough ballots have been scanned and the voters' names and addresses have been recorded, the VOTES repositories can be made publicly available.  The repos include the tally algorithms that are executed to tally the election, the scanned ballot data, and, independently, all the voter names and addresses. (There is 100% no connection between a voter's name and address and their ballot anywhere in VOTES or the printed ballots.)  The repo allows every voter to once again verify that their ballot is correctly recorded using their cryptographic keys as well as to execute the tally on their smart devices. It also allows neighborhoods to self-patrol for fraudulent people and fake addresses as well as state and federal investigations to scan for unauthorized or fraudulent registered voters across the entire electorate.

As the hours and days pass and additional ballots continue to be scanned and added to the VOTES Merkle based repositories, rolling public copies are continually updated for public downloads, allowing for constant E2EV as well as intermediary ballot tallies. Note that all citizens and election officials can download the latest repositories and verify and tally the election results.

## 4b) Vote by mail Example - what happens to the ballot

In vote-by-mail scenarios, the completed ballots are mailed to the election officials.  Note that in vote-by-mail scenarios trust has been placed on the electorate that no one will sell their ballot nor impersonate another voter, particularly in a verifiable manner to a third party.  Using VOTES will not eliminate such risks, but VOTES will give mail-in-voters the ability to verify that their ballot has been entered and tallied correctly.  And it makes it easier for neighbors and friends and family to spot impersonated ballots by making the voter records easily and immediately accessible once all the polls close.

In vote-by-mail scenarios election officials will scan the ballots for electorate.  Depending on the time and budget available for scanning ballots, election official can mimic the in-person workflow above or automate various steps.  For example, the human validation of the scan of the ballot can be skipped - the ballot scanning step can be executed without inspection.  Additional options include:

- VOTES prints the 100 row voter handout which is mailed back to the voter.  Their row offset could be separately returned, returned in the same envelope, transferred privately in person at some later time and location, or discarded.
- VOTES prints a URL for the 100 row handout and mails, emails, or txt's the URL back to the voter.  The voter's row can be sent separately, at the same time, transferred privately in person at some later time and location, or discarded.

Regardless of whether a vote-by-mail voter receives their ballot digest, once all the polls close the VOTES repositories are made publicly available.  Voters who know their digest can still check their ballot, and all the voters can still tally all the races and check the voter names and addresses in their neighborhood for potential inconsistencies.  This latter check offers transparency into vote-by-mail ballots as soon as the VOTES repository is available.

## 4c) How does an election official interact with VOTES?

Pre-election day, VOTES supplies the framework in which all the geographical/geopolitical overlays (the GGO's, e.g. the states, counties, municipalities, cities, towns, districts, precincts, school districts, etc.), can easily compose the ballots for their specific constituents based on address or other criteria in an iterative, collaborative, and independent manner.  VOTES natively stores the GIS information necessary to map a voter's address to all the containing GGO's and can automatically create the correct ballot for any address whenever needed.  Note that the software development framework tests the blank ballot creation and layout prior to any changes that make it into production.  The ballot scanning/scanner vendor can also participate in live, daily testing of scanning ballots.

During election day, VOTES can generate address-specific ballots (location #1), ingest scanned cast ballots and help end voters correct un-scannable ballots (location #3), and verify the voter's ballot as been properly collected (location #4).

After all the polls close, VOTES already contains the tested, verified, and open-source tally algorithms for each race across the GGO's as necessary.  The tallies can be executed by any election official or voter who has access to the VOTES repositories.  This greatly reduces the time and cost to tally an election, even if the tally is ranked choice.

## 4d) End to End Validation (E2EV)

VOTES directly supports E2EV by providing three separate copies of the voter's ballot.  The first is the physical ballot controlled by the local election officials.  The second is the digital scan of the ballot as approved by the voter and stored in the VOTES public repository.  The third copy is given to the voter on a 8.5"x11" paper containing encrypted and randomized digests of the voter's ballot.  These three different copies in addition the inherent properties of the Merkle tree database support multiple and different E2EV pathways.  The physical ballots can be independently sampled and compared to the electronic copies both in count, content, and via statistical sampling.  Each voter can validate their individual paper copy against the public repository as well.  In addition, voters in possession of their ballot's row index can inspect their specific electronic ballot.

And with an immediate and open source copy of all the names and addresses of the entire electorate, election officials as well as any voter can analyze by various methods the accuracy of those names and addresses.

# 5) What is the kickstarter campaign funding?

The primary goal of the kickstarter campaign is to raise the funds to develop VOTES into a demonstrable prototype.  With a working prototype VOTES can be demonstrated to city and state election officials.  Since VOTES is a disruptive solution, a working prototype greatly increases the ability to win an RFPs (Request For Proposals) to supply digital services for a public election.  By winning one or more such RFPs, the VOTES project will receive the funding necessary to actually be used in a public election.

Just to be clear:

**THIS KICKSTARTER CAMPAIGN IS RAISING FUNDS FOR THE RESEARCH AND DEVELOPMENT OF AN OPEN SOURCE, E2EV ELECTION SYSTEM CALLED VOTES.  IT IS NOT FUNDING THE IMMEDIATE AND DIRECT PRODUCTIZATION OF AN OPEN SOURCE E2EV ELECTION SYSTEM.  PLEDGES ARE BEING CONSIDERED AS DONATIONS/GIFTS TO FURTHER THE DEVELOPMENT OF VOTES WITH NO EXPECTATIONS OF ANY PRODUCT OR VALUE IN EXCHANGE.**

Election systems need to go through a separate and extensive RFP process in every state as well as some cities.  This campaign is an attempt to get VOTES into those RFP conversations with a working prototype.

If no RFP is signed, a secondary goal is that the kickstarter funding will allow enough technology to be created and demonstrated such that some form of public or private investing can occur, or for an existing election system vendor to independently adopt the technology.

Regardless of any financial outcome, a fundamental goal is to make elections more transparent, secure, and trustworthy.  Even if our funding goal is not reached, the kickstarter campaign can be successful if VOTES is reviewed by more voters, election scientists, and technology experts.  Being open source, such a review can be critically important for any next generation digital election solution and serve as an important open source reference.

# 6) Why raise $100,000?

The first $100,000 allows me, Sandy Currier, to work on VOTES full time for about one year depending on the degree of subcontracting.  For each $100,000 in additional funds raised, an additional full time software developer can be brought on-board.

# 7) Who is behind VOTES?

Sandy Currier started thinking about VOTES after a 2016 Thanksgiving Holiday gathering.  A lively discussion occurred concerning whether anyone was sure their vote had ever actually been counted, and if block-chain technology could be used for public elections.  He rejected block chains as a viable solution and was hoodwinked into accepting the challenge of looking into it and reporting back the following year.

Over the next few years Sandy investigated the history and current state of the science and art of voting technologies.  He sat in on numerous meetings at MIT concerning voting policy, operations, trends, security, and technology.  He discussed ideas with MIT professors, election officials, and private sector experts.  Finally he took a sabbatical from his day job this past summer in an attempt to focus on this kickstarter campaign.

Sandy graduated from MIT in 1986 and has worked in the high-tech sector for 34 years.  He's developed solutions for start-ups, Fortune 500 companies, and has run his own software company.  His bio is available at https://www.linkedin.com/in/toolsmith/Outline
