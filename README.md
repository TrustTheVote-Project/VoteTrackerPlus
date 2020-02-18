# VOTES

A Verifiable Open Technology Election System

# Overview

VOTES is a distributed, open-source [voting](https://en.wikipedia.org/wiki/Voting) system that enables transparent, secure, and accurate elections with full End-to-End (E2E) verifiable ballots.  VOTES maximizes the transparency and trust of an election throughout the election process by:

- allowing each voter to verify that their ballot is electrontically cast and collected as intended
- allowing each voter to verify that their ballot has been correctly counted

VOTES is an open source distributed database/repository and application that supports

- storing all the electronically interpreted scans of the paper ballots in a secure and anonymous manner
- executing the tally of all the races via software code contained within repository
- creating blank ballots as a function of address
- storing the address and name of every person who casts a ballot without the association of any other information - the ballots are 100% anonymous

VOTES is NOT a:

- voter ID solution
- voter registration solution
- ballot scanner nor contains ballot scanning software - VOTES receives the interpreted ballot from the ballot scanner, which could be a traditional mechanical scanner or a smart phone application
- replacement for paper ballots - VOTES supports a full E2E verified election in addition to a completely independent paper trail of the paper ballots

VOTES is implemented as a distributed set of repositories and several embedded applications contained within the repositories that store and process the electrically scanned and interpreted ballots.  These repositories are a distributed [Merkle tree](https://en.wikipedia.org/wiki/Merkle_tree) that contains a full ledger of all the transactions that have occurred during the election process, nominally starting months prior to election day.  This includes the GIS information for each geographical/geopolitical boundary (the state, county, town, school district, precinct, etc boundaries), the (automatic) layout of the blank ballots for each address, and the (potentially different) tallies for each race.  These same repositories then also record the (completely anonymous) cast ballots as well as the names and addresses of those voting.

# How Does VOTES Work?

## A Physical Voting Center Example

When a voter casts their ballot in a physical voting, the ballot is scanned and interpreted (parsed) at the ballot scanner.  A private screen (for example, a cell phone connected to the scanner and not connected to the internet) displays the interpreted results.  If the results are incorrect, the voter cancels the ballot, the ballot is destroyed, and the voter tries again.

Once a scan of the ballot has been approved by the voter, the interpreted results are added to the VOTES repository.  Via the same private screen, the voter is shown an index number between 1 and 100.  In addition a ballot printer prints a page with 100 valid and specially selected ballot digests indexed between 1 and of 100.  The privately displayed index indicates which digest belongs to the voter.  The transfer of this number from VOTES to the voter and the selection of the 100 public digests are done so that the voter's digest cannot be validated by a third party - there is no soft or hard copy retention of the index once it is displayed.

Once all the polls close, the VOTES repositories that contain all the ballots and election software are made publicly available.  The voters with a digest can look up their digest in the VOTES repositories to confirm that their ballot has been properly collected.

In addition to and separate of the ballot validation, each voter or election officials who has downloaded the VOTES repository can execute the election tallies directly on their computer devices.  There is no reliance on a single trusted source for the tally.

In addition to the ballot and tally validations, each voter and election official can inspect their local neighborhood or any other neighborhood for suspicious names and addresses.  This level of transparency will combat conspiracy theories proposed by disgruntled candidates as well as third parties.  It will allow election officials to quickly investigate suspicious voting claims.

All of the above increase the trust and transparency of an election.

## Vote by Mail Example

In vote-by-mail scenarios, the completed ballots are mailed to the election officials.  Note that in vote-by-mail scenarios both election officials and the electorate have placed trust in all the voters that they will not sell their mail-in ballot for compensation.  Using VOTES will not directly validate that any specific voter has done this.

In vote-by-mail scenarios election officials have multiple options for configuring VOTES regarding handling vote-by-mail scenarios to suit their needs and budgets.  For example, election officials could configure VOTES such that:

- VOTES prints the 100 digests per ballot which can be mailed back to the voter
- VOTES prints a URL for the 100 digests and mails, emails, or txt's the URL back to the voter

In both cases, the voter's secret index number can either simply be discarded, be returned to the voter by mail or some other method of delivery, or be secretly revealed in person later (similarly to in-person voting) via an election official at a town center.  In this latter scenario election officials must be able to accurately identify the voter and record the fact that a secret index was given out (the index is secretly shown to the voter).

Regardless of whether a vote-by-mail voter receives their ballot digest, once all the polls close the VOTES repositories are made publicly available.  Vote-by-mail voters who know their digest can check their ballot.  Regardless, all the voters can still tally all the races and check the voter names and addresses in their neighborhood for potential inconsistencies.  This latter check offers transparency into vote-by-mail ballots as soon as the VOTES repository is available.

# Additional Details

VOTES is intended to be as compliant as possible with [NIST](https://en.wikipedia.org/wiki/National_Institute_of_Standards_and_Technology)'s [voting](https://www.nist.gov/itl/voting) efforts (see the [HAVA](https://en.wikipedia.org/wiki/Help_America_Vote_Act) Act).

For more information contact Sandy Currier at:  windoverwater at gmail dot com

# Status - 2020/02/14

VOTES is currently in the design phase - still working out the basics.
* Looking for volunteers to help in any way
* Working on a kickstarter campaign
* Looking into potential funding
