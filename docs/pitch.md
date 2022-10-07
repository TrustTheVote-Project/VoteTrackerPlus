VoteTracker+ is an open software ballot tracking system that increases the security, accuracy, and trustworthiness of a paper ballot election by cryptographically tracking the [Cast Vote Records](https://pages.nist.gov/ElectionGlossary/#cast-vote-record) associated with paper ballots.

VoteTracker+ provides three core capabilities:

1. Directly supplies a cryptographically anonymized ballot check back to the voter, allowing the voter to validate that their specific ballot has been interpreted, recorded, and tallied as intended

2. Cryptographically records and seals the entire history of the election as it occurs in near real time

3. Allows the public to inspect and validate the official Cast Vote Records and tally as well as (ideally) the aggregate voter ID rolls across the entire electorate

VTP provides [E2EV](https://en.wikipedia.org/wiki/End-to-end_auditable_voting_systems), specifically the E2EV properties of  __cast as intended__, __recorded as cast__, and __tallied as recorded__, without the need to encrypt the CVRs of the voter's ballot.  That is, VTP provides this without the need to encrypt the data at rest.
