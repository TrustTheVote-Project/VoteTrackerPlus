Election day workflow from VOTES POV

# 1) Pre-election day (background)

Prior to election day, election officials enter the registered voters in the VOTES voter-id repo.  This repo __only__ contains the voter's name and address.  It contains two additional fields - a status field and a digest field.

It is up the precinct to decide on a registration deadline.  The deadline can be prior to election day or include election day, but regardless it needs to be pre-configured in the VOTES ballot repo.

# 2) Election day voting center - in person voting

## When a voter has been identified and needs a ballot, an election official selects the voter from the VOTES voter-id repo, and VOTES will print a ballot.  The ballot contains a unique digest.

VOTES temporarily tracks the ballot digest against the voter.  This information is discarded when the ballot is scanned.  Note - VOTES is 100% open source so the public can inspect and validate this behavior.

## The ballot is given to the voter and the voter fills it in.

## The ballot is scanned.

Regardless of a double or single checkin, or absentee, early, or UVBM, the ballot is scanned.

### Valid Ballots

If it is valid, VOTES updates the VOTES voter-id and ballot repos with special and different digests.  The voter is marked as having voted.

### Invalid Ballots

If the ballot is invalid, it is rejected and the reason for the rejection is displayed.  The ballot is recorded in a different section of the VOTES ballot repo that is not included in the tally.  Similar to a valid ballot both the voter-id and ballot repos contain different digests doubly encrypted so that the invalid repo can be tracked if necessary.

If the invalid scanning occurs during in-person voting, VOTES supports the voter being able to try again.  If so configured by the precinct the election official at the VOTES scanning device will hit 'try again' button before the ballot is submitted, thus rejecting the ballot.

Note - to assure anonimity the invalid ballot section is primed with 100 fake invalid ballots such that if there is only invalid ballot per precinct, that voter's anonymity is not compromised.

With in-person voting the voter may work with election officials to create a new a separate ballot and try again as the VOTES voter-id repo has been marked with an 'invalid ballot' indication.  Note that VOTES repos are full ledger - even if the voter obtains a new ballot and successfully scans it, all is recorded.

## Validating Ballots after the polls close

If the voter wishes to validate their specific ballot, they may contact an election official in person without a third person or device, electronic or otherwise, being present.  The election official validates the voter-id and requests a decoding from VOTES.  The request itself is entered into the voter-id repo (full ledger design - another commit) recording the election official and the requester.  VOTES will effectively return the VOTES ballot digest for the voter to inspect.

Note that all the ballots in the ballot repo have digests that are public, so anyone can look up any ballot - the secret is knowing which ballot belongs to which voter.

The public CANNOT get to any repo until after all the polls close.  As precincts complete scanning non IN-PERSON ballots or scanning ballots from voting centers where technical difficulties prevented live ballot uploading, the precinct repos updates are uploaded.  Eventually the precincts signoff on all ballots being entered.  At that point the precinct's repo is made public and the public can count the votes.

## Additional EULA Restriction

Also note that the VOTES EULA restricts the monetary use of a ballot digest or content - ballots cannot be sold or exchanged in any kind of public or private market.

## Additional checks

As ballots are scanned, the total count is available to election officials via the VOTES ballot repo.  In addtion as voters voter, the number of voters are available via the VOTES voter-id repo.  These two repos are separate and are controlled by separate entities.  Both are full ledger databases.

## Nullifying Ballots

If a voter-id is found to be fraudulent, the ballot can be nullified.  In this case, the precinct's RA requests a nullification of one or more voters (!) - not ballots - from the state's RA.  The requirement of both RA insure that the transaction is recorded in the full ledger - records the who/what/when/why contained in the ballot repo.  Nothing is recorded in the VOTES voter-id repos so to keep the anonimity of the voter intact.

When a ballot is nullified, it is evident (recorded as such) in the ballot repo so that the tally changes.  The precinct's election official may or may not privately notify the voter that their ballot was nullified.  A nullified ballot is NOT recorded in VOTES voter-id repo and due to the double encryption 2x times, 


VOTES stores nullified ballots in a third encrypted (public) that cannot be publicly tied to either of the other two VOTES repos.  The contents of this third repo is also doubly encrypted.  Note that the  voter-id repo does NOT record nullified ballots since voter anonymity is more important then making this data publicly available.  However, election officials are encouraged to record fraudulent voters (fraudulent voter-id's) in their real voter-id databases so to prevent future VOTES voter-id repos from containing such voters.





Given any of one of the three digests, it requires a double decryption using two separately controlled RA keys to translate between any two digests.  In addition, each decoding translation is recorded full ledger as well.

The fact that the VOTES voter-id repo now has a digest will block that voter-id from entering another ballot as it is a synchronous process step.

If the ballot is not valid, the voter can choose to leave (election official indicates that in VOTES) or fill out another ballot.  If so, the election official will print another ballot for the voter (address specific with a new/different ballot digest) and the voter can try again.
