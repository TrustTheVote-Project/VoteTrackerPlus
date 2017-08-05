IN PLACE VOTING - when a voter physically shows up at a voting center to vote on election day

There is only one checkin table, where the voter checks in and receives a physical ballot.

# 1) Voter shows up at the voting center

# 2) Voter selects precinct and waits in the checkin line.  Identifies themselves to the election official for that precinct.

# 3) Voter may witness election official checking off name.  VOTES prints the voter's ballot which contains a unique digest ID.  The election official gives the voter their address specific ballot.

At this point the VOTES voter-id repo (which is still private similar to the VOTES ballot repo) will indicated the voter is 'voting'.

# 4) The voter enters a private voting booth and privately fills in the ballot.  No third party witnesses or active devices are allowed except whereaccessibility is at issue, in which case one or more assistents may be present.  No active recording devices allowed regardless.

# 5) The voter leaves the voting booth a goes to the VOTES ballot scanner.  An election official is there for assistance if necessary.  The voter places the ballot face down in the scanner and the scanner scans the ballot.  If the ballot is successfully scanned, the ballot is accepted.

At this point the VOTES voter-id repo will have a status of 'voted' in addition to a new digest being present in that repo.  The VOTES ballot repo will also have a new and different digest present that will be part of the next block-chain.  Both digests are the results of a double encryption with two different and independent private keys.

Upon successful scan, the voter is free to view an optional visual-only receipt of their ballot scan (similar to a receipt at a POS (point of sale) cash register.  The visual receipt simply contains two identifiers, a random and short, unique word identifying the voter's block-chain and an offset into that block-chain.  The POS display is physically set up so that only the voter can see the display.

At the next station a VOTES ballot machine will indicate when the next block chain is available.  The voter is then free to print the block chain receipt.  By matching their offset they can find their ballot digest.  Note that multiple block-chains are built in parallel and multiple (short string) identifiers are used.

This procedure is necessary so to make it difficult for a third person to associate a voter and a ballot or a voter with a specific block-chain.  Regardless, when all the polls close, the voter can look up their ballot via the VOTES ballot repo given a digest.

If the scan is not valid, the VOTES display will display the reason for the invalid scan and physically reject the ballot.  Given that this is a single checking in-person workflow and not a double checkin in-person workflow, there may be no election official or easy UX process configured by the precinct to allow the voter to voter again.  The easist way to support voters addressing an invalid unscannable ballot is for the voting center to adopt a double checkin UX (see in-person-voting.double-checkin.md).  A single checkin voter UX workdflow does not directly and easily support voters addressing invalid/unscannable ballots.

If the voter leaves, VOTES will end up recording the voter's status as 'voting' sans any ballot digests.
