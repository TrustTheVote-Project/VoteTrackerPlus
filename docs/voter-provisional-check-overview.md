# More Details on the VoteTracker+ Voter Anonymized Provisional Ballot Check

## 1) Terminology

For definitions and technical terms, please refer to the [NIST Glossary](https://pages.nist.gov/ElectionGlossary/)

## 2) Background

See [voter-check-overview.md](./voter-check-overview.md) for background.  The voter provisional check overview is based off of that document.

The provisional ballot check workflow/US occurs when election officials wish to support ballot checks for the first 100 voters.  VoteTracker+ requires a a minimum number of already cast ballots to adequately anonymize the voter's CVRs.  Without a special workflow/UX, the first 100 voters of every unique ballot type would not receive a ballot check.  This special workflow, called the provisional ballot check, supports this.

A summary of the provisional ballot check workflow is described in section 3.2 and 3.3 of [project-overview.md](../project-overview.md).

## 3) Details of the Provisional Ballot Check

When a ballot CVR is created for one of the first 100 ballots, the current git workflows and details remain with the following additional details.

### Pre Ballot Scanning

When the VTP scanners are configured for a voting center (wherever ballots will be scanned)
- a public/private key pair is generated for that location on the local remote git server
- 100 times the number of VTP scanners random 3 digit numbers are generated and 100 each are distributed to the VTP scanners.  If there are more than 10 VTP scanners, alphanumerics or words (TBD) are used
- the public key is also passed to the VTP scanners

### Ballot Scanning

If a CVR digest is created on a VTP scanner and is within the 100 limit
- a random number is pulled from the queue
- it is encrypted with the public key
- a git tag is created for each CVR branch and also pushed with the branch.  The tag name is the 3 digit random number and the contest UID.  There will be N contest tags for each provisional ballot check
- the 3 digit random is displayed to the voter instead of the real ballot index
- the encrypted version of the random number is printed on (as) the provisional ballot check for the voter

### After 100 ballots are cast or after all-the-polls close

When a provisional ballot check is scanned and validated (the encrypted index must be successfully decrypted and match a live provisional ballot index), the voter is prompted the un-encrypted provisional index.

If the correct un-encrypted provisional index is entered, using either the 100 or less provisional ballot tags (which reference the correct and real CVR digests), a real ballot check is printed.  The real ballot index is also privately displayed to the voter.  The provisional ballot index is deleted so that it cannot be used again.

Note that the CVR digests may or may not already be merged to master as that is a different workflow independent of this one.  This workflow only concerns delivering to the voter a real after-the-fact ballot check and index.
