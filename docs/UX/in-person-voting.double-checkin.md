IN PLACE VOTING - when a voter physically shows up at a voting center to vote on election day

There are two checkin tables, one to checkin and receive a ballot; one to checkout and cast a ballot.

# 1) Voter shows up at the voting center

# 2) Voter selects precinct and waits in the checkin line.  Identifies themselves to the election official for that precinct

# 3) Voter may witness election official checking off name.  VOTES prints the voter's ballot which contains a unique digest ID.  The election official gives the voter their address specific ballot.

At this point the VOTES voter-id repo (which is still private) will indicate the voter is 'voting'.

# 4) Voter fills in the ballot privately.  No third party witnesses allowed except where accessibility is at issue, in which one or more assistents may be present.  No active recording devices allowed regardless.

# 5) Voter goes to checkout line and identifies themselves a second time.  Voter may witness election officials checking off their name.  The ballot is placed in the scanner.  If there is a valid scan, the ballot is accepted.

At this point the VOTES voter-id repo will have a status of 'voted' in addition to a new digest being present.  The VOTES ballot repo will also have a new and different digest present.  Both digests are the results of a double encryption with two different and independent private keys.

Upon successful scan, the voter is free to leave or to inspect their ballot.  To support voters inspecting their ballots during election day, a special election-day inspection station needs to be set up by election officials.  That station / UX experience is similar to post-election day ballot inspection except that the identification of the voter is done once when entering the voting center.

If the scan is not valid, the VOTES display will display the reason for the invalid scan and the ballot is physically rejected from the scanner.  The voter is free to either leave or try again.  To try again, the election official at the scanner hits the "invalidate" button for the ballot, and another ballot with a new digest will be printed.  The original ballot is shredded by the election official - regardless it is no longer scannable and not stored anywhere in VOTES.  (All unscannable ballots are physically rejected by the scanner).  Though VOTES supports the ability for the voter to try again, it is up to the election officials to have configured their voter UX workflow to support additional attempts.  The voter may or may not try again.

If the voter leaves, the election official hits the 'no-vote' button and voter is marked as having not voted.  If the election official forgets that step, the voter is simply left as the status 'voting' (as in the case of the in-person-voting.single-checkin.md workflow).
