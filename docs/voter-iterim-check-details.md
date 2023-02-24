# More Details on the VoteTracker+ Voter Anonymized Interim Ballot Check

## 1) Terminology

For definitions and technical terms, please refer to the [NIST Glossary](https://pages.nist.gov/ElectionGlossary/)

## 2) Background

See [voter-check-overview.md](./voter-check-overview.md) for background.  The voter interim check overview is based off of that document.

The interim ballot check workflow/US occurs when election officials wish to support ballot checks for the first 100 voters.  VoteTracker+ requires a minimum number of already cast ballots to adequately anonymize the voter's ballot check.  Without a special workflow/UX, the first 100 voters of every unique ballot type would not receive a ballot check.  This special workflow/UX, called the interim ballot check, supports giving ballot checks to the first 100 voters.

A summary of the interim ballot check workflow is also described in section 3.2 and 3.3 of [project-overview.md](../project-overview.md).

## 3) Details of the Interim Ballot Check

When a ballot CVR is created for one of the first 100 ballots, the current git workflows and details remain the same with the following additional modifications.

### Ballot Scanning

If a CVR digest is created on a VTP scanner and is within the 100 limit:

- after the CVR contest branch is created and pushed, the VTP scanner generates 3 digit random number and an associated GUID
- a git annotated tag is created.  The name of the tag is something like “interim-NNN-<CVR branch>” and the comment/annotation contains the GUID.  The <CVR-branch> matches the created CVR branch name.  The tag is pushed to the local remote server.
- the 3 digit random number is privately displayed to the user and the QR code of the GUID is printed on/as the provisiobal ballot check 

### After 100 ballots are cast or after all-the-polls close

The voter re-enters the voting center and properly identifies themselves to the election official.  The EO validates that the voter was one of the first 100 voters and verifies the interim ballot check.  The voter enters the semi-private VTP scanner position #3 for a second time.  The voter inserts the interim ballot check in the scanner.

When a interim ballot check is scanned:

- the interim tags are retrieved from the local remote server
- the user is prompted to enter the interim ballot index
- if the GUID matches the supplied interim index, then a real ballot chech is created and the assocuated real index is privately displayed to the user.  If there are less than 100 total ballots, the ballot check will contain that number.
- the tag is deleted

Note that the CVR digests may or may not already be merged to main as that is a different workflow independent of this one.  This workflow only concerns delivering to the first 100 voters a real after-the-fact ballot check and index.

Note that tags are never pushed upstream of the tabulation git server - they only remain local to the tabulation git server. 

## 4) Implementation Notes

During an election the git connections to the local remote server will be ssh based so that the git runtime connection is secured and access is both authenticated and encrypted.  As such the overall security surrounding the plaintext encoding of the 3 digit number and the associated GUID via a git annotated tag may/should be good enough.  More encryption may reduce the attack surface, but the limited and controlled access to the git server and workspaces should be good enough (TBD).

Note - if the remote tags can be listed with the annotation as opposed to pulling, do that to minimize the attack surface.
