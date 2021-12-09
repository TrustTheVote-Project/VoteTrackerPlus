# More Details on the VoteTracker+ Voter Receipt

## 1) Terminology

For definitions and technical terms, please refer to the [NIST Glossary](https://pages.nist.gov/ElectionGlossary/)

## 2) Background

A foundational aspect of VoteTracker+ is the basic capability to offer to the voter a personalized ballot receipt that contains no connection to their identity nor to their ballot.  To achieve this VoteTracker+ relies on both a specific UX (User eXperience, a.k.a. voter centric workflow) and technology.

From a UX point of view an overview of the voter experience is as follows:

1. After the voter marks their ballot, they submit it to the ballot scanner (not part of VoteTracker+)
1. The ballot scanner scans thier ballot and presents the voter with a human readable form of the [Cast Vote Records](https://pages.nist.gov/ElectionGlossary/#cast-vote-record).  The voter can accept or reject the ballot scanning.
1. After accepting the CVR, the scanner privately displays to the voter in a manner not observable by a third party their specific row offset on their specific voter receipt
1. The ballot scanner prints thier ballot receipt on a 8.5x11 sheet of paper
1. Prior to leaving the voting center, the voter can place their receipt on a separate scanner that will validate that the CVR's referenced on the receipt are now in fact contained in the official voter center's local VoteTracker+ repositories.  These repositories are in fact Merkle Trees that contain additional security details in addition to their history preserving aspects.

The first key step is step 3.  Even though the voter can share their receipt if they so choose, doing so does not reveal how they voted or what their identity is since the sheet contains 100 additional ballots worth of CVRs.

The second key aspect is the Merkle Tree aspect of the VoteTracker+ repositories.  By confirming to the voter that the CVR's on their ballot receipt are now part of the official Merkle Trees of the local voting center, the voter has a valid receipt for 100 CVRs including their own.

The rest of this document describes the technology in play regarding the voter receipt and the workflow described above.

## 3) Details of the Timeline for the Generation of the Voter Receipt

The following timeline assumes the following design choices.  These design decisions may change upon further research and discovery.

1. The ballot scanner is effectively a separate and individual OS/container/lambda function with its own file system, processes, and security model.  This is not a design requirement but an assumption.
1. Each voting center basically contains a Git service that hosts a voting center local git repository.  Various devices in the voting center will pull and push into this Git service.  For reference repo is referred to as the local remote repository.
1. The local remote Git repo primarily operates on the master branch.
1. The ballot scanners have the ability to print but only in one color that does not match either pencil or the ink provided by the election officials to voters to fill out the ballot.
1. Both the physical ballots and digital image scans of the ballots are considered confidential and private information never to be made publicly available.

### 3.1) On the ballot scanner after the voter has blessed the CVR of their ballot:

1. The ballot scanner will fetch the latest ballot repository from the local remote.
1. A random master branch commit is selected back in history from the previous 100 commits, different for each contest.  Since there are never any merge conflicts, the location of the branch point on master is moot.
1. A randomly generated number but one that is also a function of the CA/ICA chain is signed/digested by the voting center's private key and printed on the paper ballot.  This number is also associated with the digital scan of the ballot.
1. The contests on the current voter's CVR are selected in random order and committed in separate branches without time information (or with time information set to a specific date/time).  Blank contests are recorded as such - as a blank.
1. The JSON payload of the Git commit contains several additional fields, one being the value of the parent commit (on master) being encoded/digested by the private pem keys of the voting center as signed by RA chain for the election.  It is a security model TBD if there is also a voting center function that signs with the CA/ICA of the election as well.  See the VoteTracker+ security model for more details.
1. The first contest on the ballot also has a JSON field that contains the same generated number printed on the ballot.
1. The actual Git commit digests __are__ the digests that the voter will eventually receive.
1. The (new) voter's commits are pushed to the local remote Git repo as new branches again in random order, incrementing by N contests the number of unmerged branches on the local remote.
1. 99 random contest sets are selected (starting from the last fetch) and the 100 row ballot receipt is constructed for the voter.  The voter's specific digests for their ballot/CVR are randomly placed on some row.  That row number is displayed securely and privately to the voter while the sheet is being printed.  Once display and cleared, there is no longer any record of the which row belongs to the voters stored anywhere in software (to verify see the source code which is part of Merkle Tree and the operational provenance of the scanning device.
1.  It is a TBD how the local contest branches are handled in the local repo - it is a security model TBD.  It may be the case that they are deleted and the local Git is GC'ed and the reflog cleared.  Or it may be the case that some of this data persists for forensics in case of a compromise of the voting center.
1. The paper ballot is printed with 

### 3.2) On the local remote Git repo

1. The local remote Git repo receives the N context pushed from a ballot scanning device.
1. For each contest that is received, 
