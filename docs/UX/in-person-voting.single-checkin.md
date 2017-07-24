IN PLACE VOTING - when a voter physically shows up at a voting center to vote on election day

There is only one checkin table, one to checkin and receive a ballot

# Voter shows up at the voting center

# Voter selects precinct and waits in the checkin line.  Identifies themselves to the election official for that precinct

# Voter may witness election official checking off name.  VOTES prints the voter's ballot which contains a unique digest ID.  The election official gives the voter their address specific ballot.

At this point the VOTES voter-id repo (which is still private) will indicated the voter is 'voting'.

# Voter fills in the ballot privately.  No third party witnesses allowed except where accessibility is at issue, in which one or more assistents may be present.  No active recording devices allowed regardless.

# The voter goes to the scanner and places the ballot in the scanner.  If there is a valid scan, the ballot is accepted.

At this point the VOTES voter-id repo will have a status of 'voted' in addition to a new digest being present.  The VOTES ballot repo will also have a new and different digest present.  None of the three digests match.

# If the scan is not valid, the VOTES display will the reason for the invalid scan.  The voter is free to either leave or try again.  To try again, the election official at the scanner will hit the "invalidate" button for the ballot, and another ballot with a new digest will be printed.  The original ballot is shredded by the election official - regardless it is no longer scannable.  The voter tries again.

If the voter leaves, the election official hits the 'no-vote' button and the ballot is permanently rejected.  The election official shreds the ballot.
