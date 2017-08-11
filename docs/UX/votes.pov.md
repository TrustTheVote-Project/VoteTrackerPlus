Election day workflow from VOTES POV - what the ballot experiences.

# 1) Pre-election day (background)

Prior to election day, election officials enter the registered voters in the VOTES voter-id repo.  This repo __only__ contains the voter's name and address.  It contains no other voter id information that a state may use to identify the voter.  However the VOTES database contains two additional fields - a status field and a digest field.

It is up the precinct to decide on a voter registration deadline.  The deadline can be prior to election day or include election day, but regardless it needs to be pre-configured in the VOTES ballot repo.

# 2) Election day voting center - in person voting

## When a voter has been identified and needs a ballot, an election official selects the voter from the VOTES voter-id repo, and VOTES will print a ballot.  The ballot contains a unique digest that neither directly identifies the voter or VOTES electronic scan of the ballot (the ballot digest is not scanned by VOTES).

VOTES only temporarily tracks the blank ballot digest against the voter while the voter is actually voting (via the VOTES private voter-id repo.  Once a ballot is printed, the blank ballot digest is entered in the VOTES voter-id repo.  Note that this repo is private.  In addition the digest not part of the ballot payload - it is only temporarily used to identify the voter while voting.  The ballot scanning process changes the voter-id status field from containing the digest of the ballot to the state of 'voted'.

Note - VOTES is 100% open source so the public can inspect and validate this behavior.  The public is also free to execute this behavior and attempt to test and compromise it.  All the UX experiences, voter and ballot, are inspectable and are contained in the ballot repo full ledger history.

## The ballot is given to the voter and the voter fills it in.

## The ballot is scanned.

Regardless of a double or single checkin, or absentee, early, or UVBM, the ballot is scanned.

### Valid Ballots

If the ballot is valid, VOTES updates the VOTES voter-id status field with a new and different digest as well as entering a new a different digest in the VOTES ballot repo.  The voter is marked as having voted.  The two new digests are double encrypted using the two independent private keys, one from the precinct/state's certificate authority and one from the VOTES SaaS certificate authority.

### Invalid Ballots

If the ballot is invalid, it is physically rejected and the reason for the rejection is displayed on the scanner's screen.  There is a shredder next to the VOTES scanner.

If the ballot is invalid, the voter can choose to leave without voting or to fill out another ballot if VOTES has been configured by the election officials to support that UX.  If so, the election official will print another ballot for the voter (address specific with a new/different blank ballot digest) and the voter can try again.

With remote voting (absentee and UVBM etc), it is up to the election officials how they wish to configure their VOTES UX for the voter.  The voter may be allowed to vote in person or not.  They may or not be notifed of an invalid scan (configurable UX workflow).

## Validating Ballots during election day

Ballots can be validated during election day but to do so election officials will have had to set up a specific ballot identification station separate from the voting station(s).  Though special security procedures, the process is similar to "Validating Ballots after all-the-polls-close ballot verification below.

## Validating Ballots after the all-the-polls-close

If the voter wishes to validate their specific ballot, they may contact an election official in person without a third person or device, electronic or otherwise, being present.  The election official validates the voter-id and requests a decoding from VOTES of the VOTES voter-id digest.  The request itself is entered into the voter-id repo (full ledger design - another commit) recording the election official and the requester of the information.  VOTES will effectively return the VOTES ballot digest for the voter to inspect.

Note that all the ballots in the ballot repo have ballot digests that are public (once all the polls close), so anyone can look up any ballot.  Voter's anonymity is based on the secret is knowing which ballot belongs to which voter.  It is simply this information which is given to the voter in person without the capacity of third party validation.  The election official may decide to show the voter her/his digest or show the voter the actual ballot contents associated with the digest.

### What happens when a voter disagrees with their electronic version of their ballot?

Upon inspection if a voter disagrees with their electronic copy of the ballot, they ask the election official to ececute a paper trail audit.  When so asked, the election official will ask the VOTES voter-id repo or their own paper copy for the ballot digest associated with the voter.  Note that the ballot digest itself is __NOT__ stored in the VOTES ballot repo when the ballot is scanned - there is nothing in the electronic medium that directly ties a voter to a ballot.

To assiocate a voter with their physical ballot requires __BOTH__ the physical ballot __AND__ the original ballot digest either as recorded by election officials in either their own database (either electronic or the physical voter id checking/checkout rolls) or has encrypted by VOTES in the voter-id repo.  If VOTES is used, VOTES will record the decoding in the VOTES voter-id repo as part of its full ledger.

Regardless of the source, the election official will procure the physical ballot in a secure, private, non 3rd-party verifiable environment for inspection by both the voter an election officials.  This is done without the election official actually observing the actual ballot unless so requested by the voter.

If the voter believes that both the physical and VOTES electronic ballot is inaccurate, the matter is transferred to either the VOTES ballot fraud department, the state's election commission, or a state's judicial system.

If the ballot is deemed to be fraudulent, it is nullified per the nullification process.

If the state permits the submitting of new ballots in such instances (VOTES can be configured either way prior to the election), a new ballot is submitted.  However, in this case the anonymity of the voter in question is only as good as the anonymity of the process involved with the correction of the inaccurate ballot.  VOTES cannot undo id disclosure outside the voting process itself.

Note - the public CANNOT get to any repo until after all the polls close.  As precincts complete scanning non IN-PERSON ballots or scanning ballots from voting centers where technical difficulties prevented live ballot uploading, the precinct repos updates are uploaded.  Eventually the precincts signoff on all ballots being entered.  At that point the precinct's repo is made public and the public can count the votes.

## Additional EULA Restriction

Also note that the VOTES EULA restricts the monetary use of a ballot digest or content - ballots cannot be sold or exchanged in any manner either via a public or private market.  If a voter does not agree to the EULA, then they are prohibited from seeing any digest with the exception of the ballot digest which is printed on the ballot.  Voters who do not sign the EULA are not able to validate their ballots in any way.

This is true both for the potential buyer or seller of ballot contents or voter-id information.  Anyone who attempts or succeeds to execute a financial transaction based on VOTES information will be liable for retribution if they have agreed to the EULA.  Agreeing to the EULA is required for ballot validation.

In addition the EULA prevents the use of the voter-id repo(s) or data contained therein for monitary uses.

In addition, once all-the-polls close, the EULA imposes export restrictions outside the country of origin as well.

## Additional checks

As ballots are scanned, the total count is available to election officials via the VOTES ballot repo.  In addtion as voters vote, the number of voters are available via the VOTES voter-id repo.  These two repos are separate and are controlled by separate entities.  Both are full ledger databases.  The sums of each must match at all times and can be publicly displayed in block-chain incremental format.

## Nullifying Ballots

If a voter-id is found to be fraudulent, the ballot can be nullified.  In this case, the precinct's RA requests a nullification of one or more voters - not ballots - from the state's RA.  The requirement of both RA insure that the transaction is recorded in the full ledger - records the who/what/when/why contained in the ballot repo.  Nothing is recorded in the VOTES voter-id repos that compromises the anonymity of the voter.

When a ballot is nullified, it is evident (recorded as such) in the ballot repo so that the tally changes.  The precinct's election official may or may not privately notify the voter that their ballot was nullified.  A nullified ballot is NOT recorded in VOTES voter-id repo. 

VOTES stores nullified ballots in a third encrypted (public) that cannot be publicly tied to either of the other two VOTES repos.  The contents of this third repo is also doubly encrypted.  Note that the  voter-id repo does NOT record nullified ballots since voter anonymity is more important then making this data publicly available.  However, election officials are encouraged to record fraudulent voters (fraudulent voter-id's) in their real voter-id databases so to prevent future VOTES voter-id repos from containing such voters.

## Digest Workflow Summary

VOTES at times will maintain up to 3 different encrypted digests:  1) a ballot digest (which covers the blank unfilled out ballot assigned to a specific voter); 2) a VOTES voter-id double encrypted digest that points to the electronic scan of the physical ballot (either valid or invalid - only ballots of the former are part of the VOTES ballot tally); and 3) a VOTES voter-id double encrypted digest that points to the physical ballot digest.

Given any of one of the three digests, it requires a double decryption using two separately controlled RA keys to reveal the association between any two digests.  In addition, each decoding translation is recorded full ledger as well so that each decoding of an association is recorded.

The fact that the VOTES voter-id repo maintains such digests will block any voter from voting trice.  However, following due process it is possible for a voter to nullify a previously invalid ballot entered in their name and to replace it with a valid ballot if VOTES has been configured to support that process by the precinct/state.

Note that all such configurations need to finalized prior to submitting of ballots to VOTES and that all such configurations will be public in a full change level ledger post all-polls-close.
