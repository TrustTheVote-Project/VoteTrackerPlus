Election day workflow from VOTES POV - what the ballot experiences.

# 1) Pre-election day (background)

Prior to election day, election officials enter the registered voters in the VOTES voter-id repo.  This repo __only__ contains the voter's name and address.  It contains no other voter id information that a state may use to identify the voter.

It is up the precinct to decide on a voter registration deadline.  The deadline can be prior to election day or include election day, but regardless it needs to be pre-configured in the VOTES ballot repo.

# 2) Election day voting center - in person voting

## When a voter has been identified and needs a ballot, an election official selects the voter from the VOTES voter-id repo, and VOTES will print a ballot.  The ballot contains a unique digest that neither identifies the voter nor the VOTES electronic scan of the ballot.  Importantly the ballot digest is not capabable of being scanned by VOTES.

Note - VOTES is 100% open source so the public can inspect and validate this behavior.  The public is also free to execute this behavior and attempt to test and compromise it.  All the UX experiences, voter and ballot, are inspectable and are contained in the ballot repo full ledger history.

## The ballot is given to the voter and the voter fills it in.

## The ballot is scanned.

Regardless of whether in-person voting, or absentee, early, or UVBM voting, the ballot is scanned.

### Valid Ballots

If the ballot is valid, VOTES updates the ballot repository with the new information caveat the randomization of ballot casting.

### Invalid Ballots

If the ballot is invalid, it is physically rejected and the reason for the rejection is displayed on the scanner's screen.  There is a shredder next to the VOTES scanner.

If the ballot is invalid, the voter can choose to leave without voting or to fill out another ballot.  If casting again, the voter needs obtain a new ballot and once again privately fill it out.  The first ballot is shredded while the election official at the ballot scanning station prints a new ballot.

It is also possible, depending on the configuation of VOTES by the election officials, that a ballot can be forced scanned.  When done so, the unscannable part of the ballot are skipped.

With remote voting (absentee and UVBM etc), it is up to the election officials how they wish to configure their VOTES UX for the voter.  The voter may be allowed to vote in person or not.  They may or not be notifed of an invalid scan (configurable UX workflow).

## Additional EULA Restriction

Also note that the VOTES EULA restricts the monetary use of a ballot public key or content - ballots cannot be sold or exchanged in any manner either via a public or private market.  If a voter does not agree to the EULA, then they are prohibited from seeing their public key or from using any public key.  Voters who do not agree to the EULA are not able to validate their ballots in any way.

This is true both for the potential buyer or seller of ballot contents or voter-id information.  Anyone who attempts or succeeds to execute a financial transaction based on VOTES information will be liable for retribution if they have agreed to the EULA.  Agreeing to the EULA is required for voter centric ballot inspection and/or validation.

In addition the EULA prevents the use of the voter-id repo(s) or data contained therein for monitary purposes.

In addition, once all-the-polls close, the EULA may impose export restrictions outside the country of origin depending on the configuration.

## Additional checks

As ballots are scanned, the total count is available to election officials.  In addition as voters vote, the number of voters and their voter-id (name and address only) are available via the VOTES voter-id repo.  These two repos are separate and are controlled by separate entities.  Both are full ledger databases.  The sums of each must match at all times and can be publicly displayed in block-chain incremental format.

## Digest Workflow Summary

VOTES at times will maintain various encrypted digests:  1) a VOTES public ballot id key identifies a specific electronic cast ballot; and 2) a VOTES voter-id public key that identifies a specific voter.  Note that there is no data stored in VOTES or elsewhere that can associate a cast ballot with a voter even though that association exists during the actual casting of a ballot.  The only coorelation that is stored is the association of a specific physical ballot with its electronic copy and vice versa.

Note that the fact that the VOTES voter-id repo maintains such digests will block any voter from voting trice.  In addition voting centers can also configure alerts when the same name is used across voting across voting centers.

