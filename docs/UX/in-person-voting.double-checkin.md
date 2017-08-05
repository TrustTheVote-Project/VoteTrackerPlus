IN PLACE VOTING - when a voter physically shows up at a voting center to vote on election day

There are two checkin tables, one to checkin and receive a ballot; one to checkout and cast a ballot.

# 1) Voter shows up at the voting center

# 2) Voter selects precinct and waits in the checkin line.  Identifies themselves to the election official for that precinct

# 3) Voter may witness election official checking off name.  VOTES prints the voter's ballot which contains a unique digest ID.  The election official gives the voter their address specific ballot.

At this point the VOTES voter-id repo (which is still private) will indicate the voter is 'voting'.

# 4) Voter fills in the ballot privately.  No third party witnesses allowed except where accessibility is at issue, in which one or more assistents may be present.  No active recording devices allowed regardless.

# 5) Voter goes to checkout line and identifies themselves a second time.  Voter may witness election officials checking off their name.  The ballot is placed in the scanner.  If there is a valid scan, the ballot is accepted.

At this point the VOTES voter-id repo will have a status of 'voted' in addition to a new digest being present.  The VOTES ballot repo will also have a new and different digest present.  Both digests are the results of a double encryption with two different and independent private keys.

Upon successful scan, the voter is free to view an optional visual-only receipt of their ballot scan (similar to a receipt at a POS (point of sale) cash register.  The visual receipt simply contains two identifiers, a random and short, unique word identifying the voter's unique block-chain and an offset into that block-chain.  The POS display is physically set up so that only the voter can see the display.

At the next station a VOTES ballot machine will indicate when the next block chain is available.  The voter is then free to print the block chain receipt.  By matching their offset they can find their ballot digest.  Note that multiple block-chains are built in parallel and multiple (short string) identifiers are used.

This procedure is necessary so to make it difficult for a third person to associate a voter and a ballot or a voter with a specific block-chain.  Regardless, when all the polls close, the voter can look up their ballot via the VOTES ballot repo given a digest.

If the scan is not valid, the VOTES display will display the reason for the invalid scan and the ballot is physically rejected from the scanner.  The voter is free to either leave or try again.  To try again, the election official at the scanner hits the "invalidate" button for the ballot, and another ballot with a new digest will be printed.  The original ballot is shredded by the election official - regardless it is no longer scannable and not stored anywhere in VOTES.  (All unscannable ballots are physically rejected by the scanner).  Though VOTES supports the ability for the voter to try again, it is up to the election officials to have configured their voter UX workflow to support additional attempts.  The voter may or may not try again.

If the voter leaves, the election official hits the 'no-vote' button and voter is marked as having not voted.  If the election official forgets that step, the voter is simply left as the status 'voting' (as in the case of the in-person-voting.single-checkin.md workflow).
