# More Details on the VoteTracker+ Voter Anonymized Provisional Ballot Check

## 1) Terminology

For definitions and technical terms, please refer to the [NIST Glossary](https://pages.nist.gov/ElectionGlossary/)

## 2) Background

See [voter-check-overview.md](./voter-check-overview.md) for background.  The voter provisional check overview is based off of that document.

The provisional ballot check workflow/US occurs when election officials wish to support ballot checks for the first 100 voters.  VoteTracker+ requires a minimum number of already cast ballots to adequately anonymize the voter's CVRs.  Without a special workflow/UX, the first 100 voters of every unique ballot type would not receive a ballot check.  This special workflow, called the provisional ballot check, supports giving ballot checks to the first 100 voters..

A summary of the provisional ballot check workflow is described in section 3.2 and 3.3 of [project-overview.md](../project-overview.md).

## 3) Details of the Provisional Ballot Check

When a ballot CVR is created for one of the first 100 ballots, the current git workflows and details remain the same with the following additional workflows/details.

### Ballot Scanning

If a CVR digest is created on a VTP scanner and is within the 100 limit:

- after the CVR contest branch is created and pushed, the VTP scanner generates 3 digit random number and an associated GUID
- a git annotated tag is created.  The name of the tag is something like “provisional-NNN-<CVR branch>” and the comment contains the GUID.  The <CVR-branch> matches the created CVR branch name.  The tag is pushed.
- the 3 digit random number is peivately displayed to the user and the QR code of the GUID is printed on/as the provisiobal ballot check 

### After 100 ballots are cast or after all-the-polls close

The voter re-enters the voting center and properly identifies themselves to the election official.  The EO validates that the voter was one of the first 100 voters and verifies the provisional ballot check.  The voter enters the semi-private VTP scanner position.  THe voter inserts the provisional ballot check in the scanner.

When a provisional ballot check is scanned:

- the provisional tags are retrieved from the local remote server
- the user is prompted to enter the provisional ballot index
- if the GUID matches the supplied provisional index, then a real ballot chech is created and the assocuated real index is privately displayed to the user.  If there are less than 100 total ballots, the ballot check will contain that number.
- the tag is deleted

Note that the CVR digests may or may not already be merged to master as that is a different workflow independent of this one.  This workflow only concerns delivering to the first 100 voters a real after-the-fact ballot check and index.

## 4) Implementation Notes

In the wild the git connections to the local remote server will be ssh based so that the git runtime connection is secured.  Access is both authenticated and encrypted.

Note - if the remote tags can be listed with the annotation, do that to minimize the attack surface instead of pulling them.

As such the plaintext encoding of the 3 digit number and the associated GUID may/should be good enough.  More encryption may reduce the attack surface in time and space, but this may be good enough. TBD
