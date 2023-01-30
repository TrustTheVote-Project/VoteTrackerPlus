# VoteTracker+ Layperson Overview

A Summary of VoteTracker+ from the point of view of a typical voter

## 1) Background - Understanding Two Things First

To understand VoteTracker+ the voter needs to understand two (only two) fundamental aspects of election systems, namely [Cast Vote Records][Cast Vote Record] and End-to-End-Verification.

### 1.1) Cast Vote Records (CVRs)

A Cast Vote Record is an electronic record of a voter's ballot selections. It is typically generated when the voter places their ballot in the ballot scanner and can be thought of as the automatic/optical interpretation of the voter's choices for each contest on the ballot. If the ballot contains 10 contests, then depending on the scanner manufacturer there could be one CVR per ballot with each CVR containing 10 contest selections. The primary purpose of the CVR is to provide a record of voter selections that can be counted in an efficient manner to produce election results. An important and additional use of the CVRs is to provide an audit check on the paper ballots and vice versa.

All modern and approved paper based ballot scanners basically perform this function - they optically scan the voter's paper ballot creating a CVR for each contest which can then be automatically tallied. This step is at the heart of current paper based voting systems and to understand VoteTracker+, one needs to understand this.

### 1.2) End-to-End-Verification (E2EV)

The second concept is E2EV - this is the capability of the election system to provide back to the voter themselves the following three proofs or properties:

- __Cast as Intended__: Allow voters to confirm the voting system correctly interpreted their ballot selections while in the polling place via a receipt and provide evidence such that if there is an error or flaw in the interpretation of the voters’ selections.
- __Recorded as Cast__: Allow voters to verify that their cast ballots were accurately recorded by the voting system and in the case of VoteTracker+ included in the public CVR database.
- __Tallied as Recorded__: Provide a publicly verifiable tabulation process from the public records of encoded ballots.

The conflict between the fact that the CVR content needs to remain anonymous while also needing to be correctly identified back to the specific voter has made supplying E2EV historically challenging. There have only been a few solutions so far, all requiring the CVR contents to be encrypted.

Up until VoteTracker+ that is ...

VoteTracker+ supplies E2EV back to the voter without encrypting the contents of the CVR data - this is the one-line take-away of the importance of VoteTracker+ and the difference between VoteTracker+ and all other election systems available today.

## 2) Without VoteTracker+

Without VoteTracker+, current ballot scanning and tallying solutions require trust in all the moving parts, some of which are proprietary and blackbox, as well as the manufacturing and operational provenance of the electronic and software technological solutions. The voter needs to trust the software that scans their ballot and creates the CVRs and then counts their CVRs. This is true for each and every voter for each and every ballot across the entire election.

Note that each ballot scanner in each polling location is a separate machine with a separate copy of the electronics and software. Not only does the trust need to include all the individual machines, but it also needs to include the human based procedures to aggregate the tallies across all the individual machines. Though this human aggregation can be transparent, the size of the task and number of individuals and moving parts results in an overall system that is easy prey for misinformation attacks as well as subject to human error.

And as already mentioned, without VoteTracker+ there is no transparent, non-encrypted E2EV solution available.

## 3) With VoteTracker+

With VoteTracker+, the CVRs are anonymously stored in a cryptographically secure 100% open source public repository that does not require the CVRs to be encrypted. This results in transparent CVR data that is available to be validated by the voter. In addition, the same cryptographically secure repository contains all the software used to manage the CVR data in it, including tallying the contests.

With this open source, transparent, cryptographically secure repository that the voter can download and inspect, once all the polls close -- the voter can do exactly that. Each and every voter can download the same, exact, down to the last bit, repository containing all the CVR data and VoteTracker+ software. With the repository the voter can tally the contests on their own smart devices in the privacy of their homes or via shared resources in the cloud. A major point here is that since the repository is cryptographically secure but unencrypted by design, it is obvious and blatant when all the data and software is correct and un-compromised and when it is not.

This allows each voter to individually verify that their vote has been Cast as Intended, Recorded as Cast, and Tallied as Recorded.

[Cast Vote Record]: https://pages.nist.gov/ElectionGlossary/#cast-vote-record
[E2EV]: https://www.eac.gov/voting-equipment/end-end-e2e-protocol-evaluation-process
[E2EV.md]: ./E2EV.md
