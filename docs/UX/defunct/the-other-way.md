IN PLACE VOTING - when a voter physically show up at a voting center

# 1) Voter POV - double checkin workflow

## Voter shows up at the voting center

## Voter selects precinct and waits in the checkin line.  Identifies themselves to the election official for that precinct

## Voter may witness election official checking off name.  Election official gives the voter their address specific ballot.  Every ballot is uniquely identified by a ballot digest.

## Voter fills in the ballot privately.  No active recording devices allowed.

## Voter goes to checkout line and identifies themselves a second time.  Election official clicks the voter in the VOTES voter-id repo indicating that the voter is about to vote.  When the ballot is scanned, if the ballot is valid (no over votes), the VOTES scanner enter the voter-id digest in the VOTES voter-id repo indicating that the voter has voted AND create/use a different digest in the VOTES ballot repo.

Given any of one of the three digests, it requires a double decryption using two separately controlled RA keys to translate between any two digests.  In addition, each decoding translation is recorded full ledger as well.

The fact that the VOTES voter-id repo now has a digest will block that voter-id from entering another ballot as it is a synchronous process step.

If the ballot is not valid, the voter can choose to leave (election official indicates that in VOTES) or fill out another ballot.  If so, the election official will print another ballot for the voter (address specific with a new/different ballot digest) and the voter can try again.

# 2) Voter POV - a single checkin workflow

## Voter shows up at the voting center

## Voter selects precinct and waits in the checking line.  Identifies themselves to the election official for that precinct

## Election official clicks the voter in the VOTES voter-id repo indicating that the voter is about to vote.  VOTES will print the ballot on demand - the ballot includes a ballot digest.

## Voter fills in the ballot privately.  No active recording devices allowed.

## Voter depots the ballot to the VOTES scanner.  If it is accepted, the voter may leave.  If it is not scan-able, the ballot is rejected and the VOTES scanner prints a page explaining the reason for the rejection.  For a voting center to support voters trying again, then either need a double checkin worklfow.

# 3) Workflow from VOTES POV

## Pre-election day

Election officials enter the voter's name and address in the VOTES voter-id repo.

## Election day voting center

A voter is identified to the VOTES voter-id repo by clicking the 'vote' button.  If the voter has not yet voted, a ballot is printed.  The ballot contains a unique digest.

It is given to the voter and it is filled in.

Regardless of a double or single checkin, the ballot is scanned.

If it is valid, VOTES updates the VOTES voter-id and ballot repos with special and different digests.  The voter is marked as having voted.

If the ballot is invalid, it is rejected but returned as all ballots must be accounted for.  A paper or a screen is used to print/display what is wrong with the ballot.  The voter may work with election officials to create a new a separate ballot and try again.

INVALID BALLOTS during physical balloting

If the ballot is rejected, the precinct can allow the voter to try again with a new ballot or not.  The new ballot will have a new digest - it must be printed on demand.  This digest may or may not be part of the block chain (TBD).  VOTES will support this with either single or double checkin balloting, but election officials may find it easier to support this with a double checkin workflow.

VALIDATING BALLOTS after the polls close

If the voter wishes to validate their specific ballot, they may contact an election official in person without a third person or device, electronic or otherwise, being present.  The election official validates the voter-id and requests a decoding from VOTES.  The request itself is entered into the voter-id repo (full ledger design - another commit) recording the election official and the requester.  VOTES generates a one-time use key that requires the latest voter-id repo.  The election official (it is tied to the precinct's CA) can then request from VOTES the actual digest.  The actual digest is given in person.  No third-party validation scenarios are allowed - the voter cannot have an active recording device nor can it be done in public.  The voter can then look up their specific ballot in the public VOTES ballot repo.  Note that all the ballots in the ballot repo have digests that are public, so anyone can look up any ballot - the secret is knowing which ballot belongs to a specific voter.

The public CANNOT get to any repo until after all the polls close.  As precincts complete scanning non IN-PLACE ballots or scanning ballots from voting centers where technical difficulties prevented live ballot uploading, the precinct repos updates are uploaded.  Eventually the precincts signoff on all ballots being entered.

ADDITIONAL EULA RESTRICTION

Also note that the VOTES EULA restricts the monetary use of a ballot digest or content - ballots cannot be sold or exchanged in any kind of public or private market.

Third-parties cannot validate ballot contents.  However, the number of ballots from a precinct/state are tested against the number of voter-id's who voted.

NULLIFYING BALLOTS

If a voter-id is found to be fraudulent, the ballot can be nullified.  In this case, the precinct's CA requests a nullification of one or more ballots from the state's CA.  If both agree, the ballots are nullified (full ledger) with a recording of the who/what/when/why contained in the ballot repo.

When a ballot is nullified, it is evident (recorded as such) in the ballot repo so that the tally changes.  The precinct's election official may or may not notify the voter that there was a problem with their ballot and their ballot nullified.  A nullified ballot is NOT recorded in VOTES voter-id repo and due to the double encryption 2x times, 


VOTES stores nullified ballots in a third encrypted (public) that cannot be publicly tied to either of the other two VOTES repos.  The contents of this third repo is also doubly encrypted.  Note that the  voter-id repo does NOT record nullified ballots since voter anonymity is more important then making this data publicly available.  However, election officials are encouraged to record fraudulent voters (fraudulent voter-id's) in their real voter-id databases so to prevent future VOTES voter-id repos from containing such voters.
