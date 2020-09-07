# VOTES

A Verifiable Open Technology Election System

# Overview

VOTES is a distributed, open-source [voting](https://en.wikipedia.org/wiki/Voting) system that enables transparent, secure, and accurate elections with full [End-to-end](https://en.wikipedia.org/wiki/End-to-end_auditable_voting_systems) (E2E) verifiable ballots.  VOTES maximizes the transparency and trust of an election throughout the election process by:

- allowing each voter to verify that their ballot is electrontically cast, collected, and counted as intended
- allowing each voter to verify the tally of all the ballot questions
- allowing each voter to inspect their neighborhood for fraudulent voters and/or addresses

VOTES is an open source distributed database/repository and application that supports

- storing all the electronically interpreted scans of the paper ballots in a secure and anonymous manner
- executing the tally of all the races via software contained within the same repositories
- creating blank ballots as a function of address
- storing the address and name of all the voters who casts a ballot without the association of any other information - the ballots are 100% anonymous

VOTES is NOT a:

- voter ID solution
- voter registration solution
- ballot scanner nor contains ballot scanning software - VOTES receives the interpreted ballot from the ballot scanner, which could be a traditional mechanical scanner, smart phone application, or manually from an election official
- replacement for paper ballots - VOTES requires the balloting process to start with a paper ballot

VOTES is implemented as a distributed set of repositories and containing several open-source applications that store and process the electrically interpreted scanned ballots.  These repositories are a distributed [Merkle tree](https://en.wikipedia.org/wiki/Merkle_tree) that contains a full ledger history of all the transactions that have occurred during the election process, nominally starting months prior to election day.  The Merkle tree contains a full change history of the following components that comprise a VOTES election:

- The GIS information for each geographical/geopolitical boundary (the state, county, town, school district, precinct, etc boundaries).  This includes the capability to automatically print blank ballots as a function of each address.
- The applications to tally each question on any ballot, regardless of tally methodology be it plurality, ranked choice, approval, etc.
- A repository of the cast anonymous ballot themselves as data
- A repository of the names and addresses only of the individuals who have voted as data

# How Does VOTES Work?

## A Physical Voting Center Example - what a voter will experience in person

The following is a high level walk through of what a voter would experience when casting their vote in person at a voting center:

1) A voter enters a voting center and proceeds to location #1.  S/he supplies their registered name and address, and if valid receives a blank ballot specific to their address.  Their name and address is recorded in the VOTES repository.

2) The voter proceeds to location #2 to privately fill out the ballot.  No active recording devices are allowed/requested, caveat local regulations.

3) The voter proceeds to location #3 and inserts their ballot into the ballot scanner.  S/he privately reviews the electronic interpretation of the ballot.  The voter can accept or reject the scan.  If the voter rejects the scan, the first ballot is voided and s/he obtains a new blank ballot, returning to location #2 to try again.

At a VOTES technical level, there are several internal program events that occur when the voter accepts the interpretation of the paper ballot:

Upon acceptance, the paper ballot is printed with a unique random digest number for each ballot question on the ballot.  Each such paper ballot per question digest is included in the VOTES per question ballot Merkle chain wise while a second votes per question digest is also recorded.  Finally, an aggregate transaction digest is included once more on the paper ballot Merkle chain wise.  The Merkle chain full history ledger is similar to cryptographic block-chain implementations used for many cryptocurrencies.

4) After N initial ballots (where N may equal 100 TBD), voters receive a 8.5x11 sheet with 100 rows of digests pairs, one column per ballot question, and privately receives a row number.  The row number is their set of digests for their ballot questions.  There is no soft copy of their row number and only the voter privately receives the value.

Each row/column cell includes both the VOTES and the paper per ballot digests, creating a third person hardcopy of the digest pairs owned by the voter.  The first copy is printed on the paper ballot, the second copy is recorded in the VOTES repositories as a soft copy, and the third copy is printed on paper for the voter.  Note that all 100 rows of digests are valid digests though not necessarily for any specific ballot, except for the voter's row which is guaranteed to be.

6) The voting center optionally offers location #4, where a voter can place their sheet face down on a VOTES scanner (not a ballot scanner).  Unlike location #3 that validates the scan of the ballot, location #4 validates that the ballot is correctly contained in the live VOTES Merkle chains for the election.  The VOTES scanner at location #4  will display a valid or invalid indication of all the digests on the sheet.  If the voter decides to optionally and privately enter their row number, the VOTES scanner will privately display their ballot as it has been recorded in the Merkle chains.  This allows the voter to leave the voting center having verified that their ballot has been properly interpreted and entered into VOTES.

### Some important notes and clarifications:

Note - there is no publicly available 'scan' of the paper ballot - VOTES only makes available the interpreted ballot and the digest pairs.

Note - election officials and/or the scanning machine vendor can optionally store the actual scan of the ballot itself.  Such a repository if it exists is also not public.

Once all the polls have closed and enough ballots have been scanned and all the voter's names and addresses have been entered, the VOTES repositories are made publicly available.  The repos includes the tally algorithms that is executed to tally the election as well as all the voter names and addresses.  This allows every voter to once again verify that their ballot is correctly recorded and to execute the tally on their smart devices.  It also allows neighborhoods to self police for fraudulent people and fake addresses as well as state and federal investigations to scan for unauthorized or fraudulent registered voters.

As the hours and days pass, latent ballots continue to be scanned and the publicly available VOTES repo is updated with more and more ballots.  Note - to cloak the last N voters, the publicly available repository is always behind the live version by at least 100 ballots so that at a minimum the last 100 ballots can be cloaked.

## Vote by Mail Example

In vote-by-mail scenarios, the completed ballots are mailed to the election officials.  Note that in vote-by-mail scenarios both election officials and the electorate have placed trust in all the voters that they will not sell their mail-in ballot for compensation.  Using VOTES will not validate that voters have not done this nor will validate if someone has impersonated a voter.  However VOTES makes it easier for neighbors and friends to spot impersonated ballots but making the voter records easily and immediately accessible once all the polls close.

In vote-by-mail scenarios election officials have multiple options for configuring VOTES regarding handling vote-by-mail scenarios to suit their needs and budgets.  Election officials could for example configure VOTES such that:

- VOTES prints the 100 row voter handout which can be mailed back to the voter.  Their row offset could be returned separately, in the same envelope, transferred privately in person at some later time and location, or discarded.
- VOTES prints a URL for the 100 row handout and mails, emails, or txt's the URL back to the voter.  The voter's row can be sent separately, at the same time, transferred privately in person at some later time and location, or discarded.

Regardless of whether a vote-by-mail voter receives their ballot digest, once all the polls close the VOTES repositories are made publicly available.  Vote-by-mail voters who know their digest can check their ballot.  Regardless, all the voters can still tally all the races and check the voter names and addresses in their neighborhood for potential inconsistencies.  This latter check offers transparency into vote-by-mail ballots as soon as the VOTES repository is available.

# Additional Details

VOTES is intended to be as compliant as possible with [NIST](https://en.wikipedia.org/wiki/National_Institute_of_Standards_and_Technology)'s [voting](https://www.nist.gov/itl/voting) efforts (see the [HAVA](https://en.wikipedia.org/wiki/Help_America_Vote_Act) Act).

For more information contact Sandy Currier at:  windoverwater at gmail dot com

# Status - 2020/02/14

VOTES is currently in the design phase - still working out the basics.
* Looking for volunteers to help in any way
* Working on a kickstarter campaign
* Looking into potential funding
