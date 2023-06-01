# VoteTracker+ Layperson Overview

A Summary of VoteTracker+ from the point of view of a typical voter

## 1) Background - Understanding Three Things First

To understand VoteTracker+ the voter needs to understand only three fundamental aspects of election systems at a high level, namely [Cast Vote Records][Cast Vote Record] (CVRs), End-to-End-Verifiable ([E2EV][E2EV]) Elections, and zero trust technology security models ([ZTAs][ZTA] - Zero Trust Architectures).

### 1.1) Cast Vote Records (CVRs)

A Cast Vote Record is an electronic record of a voter's ballot selections. It is typically generated when the voter places their ballot in an electronic ballot scanner which optically interprets the voter's choices for each contest on the ballot. The digital interpretation itself is called a CVR. The primary purpose of the CVR is to provide a record of voter selections that can be digitally counted in an efficient manner to produce election results. Importantly the CVRs can be compared to the paper ballots during auditing.
All modern and approved paper based ballot scanners basically perform this function - they optically scan the voter's paper ballot creating a CVR which can then be automatically tallied. This step is at the heart of current paper based voting systems and to understand any modern voting system, one needs to understand this.

### 1.2) End-to-End-Verifiable (E2EV) Elections

The second concept is E2EV - this is the capability of the election to provide back to the voter themselves and not solely to just the election officials the following three proofs or properties:
- __Cast as Intended__: Allow voters to confirm the voting system correctly interpreted their ballot selections while casting their ballot
- __Recorded as Cast__: Allow voters to verify that their cast ballots were accurately recorded by the voting system
- __Tallied as Recorded__: Provide a publicly verifiable tabulation process from the public records of encoded ballots
The conflict between the CVR content remaining anonymous while also needing to be accurately identified back to the specific voter has made supplying E2EV historically challenging.  Call this the Secret Ballot Requirement (SBR) - the requirement that no voter can demonstrate how s/he voted to any third party.  See wikipedia for more on E2EV history.

### 1.3) Zero Trust Technology Security Models (ZTAs)

ZTAs with respect to elections and election systems are analogous to ZTAs for computer networks.  With elections, ZTAs need to include all the paper ballots, all the software, all the CVR data, and all the people involved within the blast radius of both - election officials as well as the voters themselves.  Regarding the software, ZTA effectively requires all the software that touches the CVRs to be open source as well as the CVR data itself.  !  ZTA also effectively requires no private encryption keys to be directly associated with the data-at-rest nature of the software or the CVR data as that requires trust in the key holder.  Technically, private keys are absolutely necessary when moving digital data, but this does not break the ZTA requirement for election systems if the data-at-rest is in an unencrypted state.

The basic tenets and implications of the above can be seen when comparing VoteTracker+ with ElectionGuard (EG).  EG is based on homomorphically encrypting the CVR data-at-rest so that the voter can execute a non-interactive-zero-knowledge proof both to indirectly validate their ballot has been cast as intended and counted as cast (plurality only - rank choice voting is currently not supported).  It is indirect since the voter can’t actually see their CVR - they can only see the contents if they spoil it in which case they have to enter a new and different ballot.  To accomplish this EG requires trust in the EG Guardians while introducing significant amounts of encryption software.  Yes the software is open source and with respect to that meets ZTA goals, but the quantity and necessary quality increases the attack surface compared to other solutions.  It also perturbs the electorate’s voting UX (User eXperience).  Regardless, though EG is a great improvement towards supplying E2EV and SBR, trust remains necessary when EG is employed.

In contrast, VoteTracker+ goes further and effectively achieves a more complete ZTA election solution precisely due to the lack of private keys associated with the data-at-rest in addition to its other cryptographic properties.  Specifically, VoteTracker+ employs a standard open source based Merkle Tree Data Model that includes both the software and CVR data.  The Merkle Tree self validates the data-at-rest and employs the self contained software to run the election.  During voting, the voter is given a paper copy of 100 randomly selected Merkle Tree entries, one of which is their personal ballot.  This effectively creates three copies of truth: the physical paper ballots, the Merkle Tree as managed by the election officials, and a slice of that data physically owned by the voter.  SBR is achieved because the voter’s specific and random index into the 100 entries is privately transferred to the voter and not contained anywhere else.  As such there is no ability to prove the value to any third party or election official.

## 2) Without VoteTracker+

Without VoteTracker+, current ballot scanning and tallying solutions require trust in all the moving parts, some of which are proprietary and blackbox, as well as the manufacturing and operational provenance of the electronic and software technological solutions. The voter needs to trust the software that scans their ballot and creates the CVRs and then counts their CVRs.

Not only does the trust need to include all the machines, but it also needs to include the human based procedures that aggregate the tallies across all the machines. Though this human aggregation can be transparent, the size of the task and number of individuals and moving parts results in an overall system that is easy prey for misinformation attacks as well as subject to human error.

## 3) With VoteTracker+

With VoteTracker+, the CVRs are anonymously stored in a secure 100% open source public repository that does not require the CVRs to be encrypted. This results in transparent CVR data that is available to be validated by the voter and election officials. In addition, the same cryptographically secure repository contains all the software used to manage the CVR data in it, including tallying the contests.

With this open source, transparent, cryptographically secure repository that the voter can download and inspect once all the polls close -- the voter can do exactly that. Each and every voter can download the same, exact, down to the last bit, repository containing all the CVR data and VoteTracker+ software. With the repository the voter can tally the contests on their own smart devices in the privacy of their homes or via shared resources in the cloud. A major point here is that since the repository is cryptographically secure but unencrypted by design, it is obvious and blatant when all the data and software is correct and un-compromised and when it is not.
This allows each voter to individually verify that their vote has been Cast as Intended, Recorded as Cast, and Tallied as Recorded.


[Cast Vote Record]: https://pages.nist.gov/ElectionGlossary/#cast-vote-record
[E2EV]: https://www.eac.gov/voting-equipment/end-end-e2e-protocol-evaluation-process
[E2EV.md]: ./E2EV.md
[ZTA]: https://en.wikipedia.org/wiki/Zero_trust_security_model
