# 1) Low Level Git Centric Design Details Regarding Voter Receipt Workflows

This document describes the git commands necessary execute the scan of the voter's ballot and the creation of the CVR for each of the [contests](https://pages.nist.gov/ElectionGlossary/#contest) on their ballot.  See the ../voter-receipt-overview.md document for more general context of this document.

# 2) Background

Per the overview of the VTP git directory and submodule layout as described in ../tech-overview.md, any phyiscal location that will be scanning and entering ballots will have a local git repo.  It is possible for two distinct physical locations to share one git repo, but it is is up to the election officials to trade off the risks, costs, and benefits of sharing one a repo in physically separate locations.  (Note - VTP may not want to support this.)

Per the git submodule layout, the git repo ultimately  associated with CVRs will have a CVRs subdirectory.  In the CVRs directory there is a single file called 'contest.cvr'.  The contest.cvr file will contain a JSON rendering of a specific contest on the voter's ballot.  Each contest will be checked into a separate git branch albeit the same file.  The git branching naming convention is something like the following:

```bash
$ git checkout -b <contest>/<short GUID> <random master branch commit>

Where:

<contest> is the VTP contest identifier
<short GUID> is a short and random and non repeating number for this repo
<random master branch commit> is a random master branch commit
```

Where <scanner id> is the alphanumeric VTP identification of the physical scanner and <contest> is the unique contest name for this [Voting Center](https://pages.nist.gov/ElectionGlossary/#vote-center).  The JSON payload looks something like the following:

```json
{"CVR": {
 "tree": "GGOs/states/California/GGOs/towns/Alameda/CVRs",
 "vote center": "Emeryville Senior Center",
 "contest": "states.US_senate",
 "election id digest": "b5dfbc103a8d28d9ae6609b42da822dc7f89ea09441537972299cf695fc408ec",
 "size": "290",
 "values": [
   "Five Six"
   ]
 }
}
```
```
Where:

"tree"                is tied to the GGO layout for this specific election
"vote center"         is the unique identification of the physical vote center where ballots are being scanned
"contest"             is the unique contest name
"election id digest"  is a cryptographic fixed length key generated from the CA chain for the current election
"size"                is the file size in bytes of the CVR record being committed
"values"              contains the values of the contest
```

Note that the actual data structure of "values" depends on the contest details, such as the tally mechanism (rank choice vote, plurality, instent runoff, etc.) as well as number of positions being filled.

Because a Voting Center can receive multiple precincts where the turnout might be lite, the single git repo's CVRs directory can receive any configured contest aggregated across any of the legal GGO sets configured for that location.  In other words, the value of "tree", "vote center", and "contest" guarantee that the CVR is unique across the entire election and that the values will be correctly tallied in the correct GGO.  And note that this configuration data is always PGP signed and pushed, tested, reviewed, and merged into the Merkle trees for the election.

As it is also possible to batch scan ballots from different 'precincts' in one location (via one set of VTP scanners), the values of tree, vote center, and contest support this scenario as well as by how the VTP scanners are configured.

Note that not every GGO needs to have a dedicated git repo - git repos are allocated via scanning locations (as in, physical VTP ballot scanners).  GGO's that do not have a dedicated git repo will still have a config.yaml and blank-ballot file that specifies the GGO contests and other info.

# 3) Git Command Sequence (Voting Center)

There are more or less four different sequences of git commands for the [Voting Center](https://pages.nist.gov/ElectionGlossary/#vote-center) VTP ballot scanner and git server:

1) Initialization of the Voting Center's git server
2) Initialization of a VTP ballot scanner
3) Scanner sequence - receiving a ballot scan, nominally from a voter standing in front of a VTP scanner
4) Server sequence - receiving and merging VTP scanner git push's

For simplicity, this description ignores the first 100 ballots cast as those voters will not receive a ballot receipt due to the need to build up the backlog of CVRs so to properly randomize and anonymize the ballot receipts.

## 3.1) Initialization of the VC git server

Note - this does not describe the pre-election configuration of a specific election or a VTP deployment.  This part is only the low level git commands that would nominally be executed and does not include self tests, verifications, authorizations, and authentications, etc.

TBD - at the moment there is nothing that needs to be initialized on the server.  A boot from the distributed firmware and software brings up the VTP Voting Center git server into a ready-to-use mode.  At the moment the following step is seen as part of the configuration prior to deployment:

Initialize the contest.cvr file with the following contents and commit message on the master branch (with the git DATE's similarly set):

```json
{"CVR": {
  "tree": "GGOs/states/California/GGOs/towns/Alameda/CVRs",
  "vote center": "Emeryville Senior Center",
  "initial file version": true
  }
}
```
## 3.2) Initialization of a VTP scanner

1) ENV setup:

Three git EV's need to be set for the processes calling the git commands:

```bash
export GIT_AUTHOR_DATE=2022-01-01T12:00:00
export GIT_COMMITTER_DATE=2022-01-01T12:00:00
GIT_EDITOR=true git merge
```

## 3.3) Scanner Sequence:  per contest example

Once the voter blesses their interpretation of their ballot into CVRs, the following is the basic git sequence to create the voter's specific ballot per contest public git commit digests (a.k.a. VTP public keys).  Note - the below is executed for each contest on the ballot regardless if the voter left the contest unmarked.


```bash
# pre-condition: scanner places JSON payload in CVRs/ballot.cvr post voter's approval step
# VTP python code validates ballot.cvr, initiates ballot casting, and loops over each contest:
$ git checkout -b <contest>/<short branch GUID> <random master branch commit>
$ git add CVRs/contest.cvr
$ git commit -F CVRs/contest.cvr
$ git push origin <contest>/<short branch GUID>
$ # Note - if there is a collision, pick another random number and try again
# VTP python code completes ballot casting by marking paper and digital image with an <election ballot GUID>

Where:

<contest>                     is the VTP contest identifier
<short branch GUID>           is a short, random, and non repeating GUID for this repo
<random master branch commit> is a random master branch commit
<election ballot GUID>        is a election (CA chain) specific and random, anonymous GUID
```

Note that each VTP scanner has an ID which is included with the VTP ballot fingerprint recorded/associated with both the digital image of the ballot and the physical ballot itself.

To generate the actual voter receipt, assuming that at least 100 ballots have been submitted to the local VTP git server, for each contest on the voter's ballot:


```bash
$ # select a random and anonymized set of 99 digests (for each of the contests)
$ # select a random number N between 1 and 100
$ # print 100 rows of contest digests, each contest being a column, with row N being the voter's
$ # privately display N to the voter
```

## 3.4) Server side sequence: per contest example

This is always on the master branch.

```bash
$ git pull
$ git merge --no-ff --no-commit <contest>/<short GUID>
$ openssl rand -base64 48 > CVRs/contest.cvr
$ GIT_EDITOR=true git commit
$ git branch -d <contest>/<short GUID>
$ git push origin master
$ git push origin :<contest>/<short GUID>
```

## 3.5) To see the results as so far pushed to the VTP git server:

```bash
$ git pull origin master
$ git log --topo-order --no-merges contest.cvr
```
