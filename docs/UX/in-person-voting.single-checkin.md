IN PLACE VOTING - when a voter physically shows up at a voting center to vote on election day

There is only one checkin table, where the voter checks in and receives a physical ballot.

# 1) Voter shows up at the voting center

# 2) Voter selects precinct and waits in the checkin line.  Identifies themselves to the election official for that precinct.

# 3) Voter may witness election official checking off name.  VOTES prints the voter's ballot which contains a unique digest ID.  The election official gives the voter their address specific ballot.

At this point the VOTES voter-id repo (which is still private similar to the VOTES ballot repo) will indicated the voter is 'voting'.

# 4) The voter enters a private voting booth and privately fills in the ballot.  No third party witnesses or active devices are allowed except whereaccessibility is at issue, in which case one or more assistents may be present.  No active recording devices allowed regardless.

# 5) The voter leaves the voting booth a goes to the VOTES ballot scanner.  An election official is there for assistance if necessary.  The voter places the ballot face down in the scanner and the scanner scans the ballot.  If the ballot is successfully scanned, the ballot is accepted.

At this point the VOTES voter-id repo will have a status of 'voted' in addition to a new digest being present in that repo.  The VOTES ballot repo will also have a new and different digest present that will be part of the next block-chain.  Both digests are the results of a double encryption with two different and independent private keys.

Upon successful scan, the voter is free to leave or to inspect their ballot.  To support voters inspecting their ballots during election day, a special election-day inspection station needs to be set up by election official.  That station / UX experience is similar to post-election day ballot inspection except that the identification of the voter is done once when entering the voting center on election day.  However, to effectively support this UX option election officials need to adopt the double-checkin UX option.  Supporting election-day ballot inspection is not directly or easily supported by the single-checkin UX option.

If the scan is not valid, the VOTES display will display the reason for the invalid scan and physically reject the ballot.  Given that this is a single checking in-person workflow and not a double checkin in-person workflow, there may be no election official or easy UX process configured by the precinct to allow the voter to voter again.  The easist way to support voters addressing an invalid unscannable ballot is for the voting center to adopt a double checkin UX (see in-person-voting.double-checkin.md).  A single checkin voter UX workdflow does not directly and easily supports voters addressing invalid/unscannable ballots.

If the voter leaves, VOTES will end up recording the voter's status as 'voting' sans any ballot digests.
