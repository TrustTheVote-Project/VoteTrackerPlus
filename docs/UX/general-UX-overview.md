# An Overview of the workflows / user experience (UX) of various roles regarding the use of VoteTracker+

## 1) How does an end voter interact with VoteTacker+?

## 1.1) Overview of an in-person voter physically casting a ballot

1) The voter identifies themself to an election official
2) The election official verifies their identity and registration status
3) The election official gives the voter an address correct blank ballot
4) The voter proceeds to a private location to complete as much of the ballot as desired
5) The voter proceeds to a second semi private location generally observable by an election official
    1) The voter privately inserts their ballot into a VTP scanner
    2) The scanner displays the Cast Vote Record for all the contests on the ballot.  Blank contests are indicated as such.  Improperly marked contests are indicated as such and block the ballot from being accepted.
    3) Before the election started accepting ballots, elections officials have configured the options that the voter has when a contest has been improperly marked via the CVR stage.  Options include receiving a new blank ballot, correcting the current ballot, marking the contest as no vote and proceeding, etc.  For this workflow description, the voter corrects their current ballot and successfully attains an accurate and complete CVR set.
    4) The CVR are accepted by the VTP scanner
    5) The VTP privately displays a screen only observable by the voter their row offset for their ballot receipt
    6) The ballot receipt is printed for the voter to take
6) Optional step - the voter proceeds to a second checkout voter ID location to re-identify themselves to another election official

## 1.2) Absentee ballot and Vote-by-mail ballot identification

1) The voter successfully receives the absentee or vote-by-mail ballot from their election officials
2) The voter fills in the ballot as much as desired
3) If supported by how the election was configured by the election officials, the voter may be able to indicate the following options on their ballot:
    - receive their ballot receipt in the mail or by some other delivery mechanism
    - by notified (and by how and when and with what limitations) if their ballot receives an invalid CVR contest scan with or without the ballot being accepted
4) The voter mails or delivers the absentee/vote-by-mail ballot to their election officials
5) Depending on what is supported, the voter may receipt their ballot receipt

## 1.3) Accessibility Notes

For those voters who have accessibility issues, an election official or personal helper can accompany the voter through the in-person or remote voting experience.

An additional option is that election officials have the option of providing an independent ballot marking station where instead of the voter physically marking a ballot, the voter privately marks a touch screen and prints an accurately marked ballot.  In this case the voter does not receive a physical blank ballot when first identifying themselves to election officials.

## 1.4) The voter can inspect their ballot receipt prior to leaving the voting center

After leaving the primary ballot casting area and before leaving the voting center, election officials can optionally make available and additional stand along, readonly VTP ballot verifier that can scan a ballot receipt and validate the inclusion of all the individual contest receipts as printed on the ballot receipt.  This informs the voter that their contests have been properly recorded in the VTP ledger.

## 1.5) Once all the polls close, the voter can inspect their specific electronic ballot

Once all the polls close, readonly clones of the official VTP election repositories are made publicly available.  Voters with a voter receipt and either manualy enter contest public keys or scan the entire receipt.  Either way, they can verify all 100 sets of contest receipts against the official repos.  As election officials push updates to their official election repos, the readonly clones are updated as the pull requests are validated and merged in.  As such, some voters will have to wait until their ballot CVRs are successfully pushed.

Alternatively, the voter can download copies of the readonly repositories and perform the same queries offline.

It is important to note that the public keys are NEVER made available to voters in a manner that allows the any third party to identify a specific ballot with a specific voter even when a third party is given the public key.

If the voter remembers their specific offset into their ballot receipt, then can inspect their actual CVRs.

## 1.6) Once all the polls close, voters can inspect the VTP voter_ID repositories

Once all the polls close, voters can also download/clone copies of the readonly voter_ID repositories.  These are separate git repositories that record the VTP voter IDs, which are solely voter name and address.

However, regardless of WITSEC (see below) programs or not, the voter id rolls are already publicly available.  However, most voters do not have easy access to them, which is both a postive and a negative.  However, with regards to the trustworthiness of an election, supporting easy access to the VTP filtered voter id data allows voter in real time to inspect the voter id information for their neighborhood as well as neighborhoods where they may suspect voter id fraud.  By make the data available, false narratives and mis information can be more quickly and more believably be corrected.

### 1.6.1) WIP/WITSEC Notes

VTP does not directly impact [WPP/WITSEC](https://en.wikipedia.org/wiki/United_States_Federal_Witness_Protection_Program) programs in the at the federal level, the voter's name has already been changed.  State level WITSEC programs will work as well as they do given however the state identifies individuals at the voting center in their WITSEC program.

## 1.7) Once all the polls close, the voter can perform all the ballot tallies

Since the VTP repositories, a.k.a. the election public ledgers, also contain the tally algorithm for all contests for all ballots, the voter can perform their own tally on their own device.  Since the ledger is cryptographically sealed, all legitimate copies of the ledger are known to be the same.

## 1.8) The voter can tell if their ballot is removed from the tally

If election officials decide to remove a ballot or a set of ballots from the election, for example under a court order or some other direction, the election officials will scan the physical ballots in a special VTP scanner that will match the VTP physical ballot ID with that of the associated contest CVRs, and remove them from the appropriate VTP repositories.  As with voter ballot scanning, these individual commits must be git PGP signed, pushed, reviewed, and merged.  The full history of the removal of ballots will be transparent to the electorate, supporting the possibility of reverse litigation.

## 1.9) Voters can inspect their voter registration status as entered into VTP

For precincts that adopt the VTP registration data as a valid source of truth regarding who is registered to vote, voters in those precincts will be able to validate their registration status.  As more precincts adopt VTP as a valid source of truth, pre-voting registration audits can more effectively be performed to validate the legitimacy of registered voters across the entire electorate.

## 2) How does an election official interact with VOTES?

The election official interactions with VTP elections will be different depending on the phase of the election, whether it is pre, during/active, or post election.  Here pre-election workflows refer to all the election official workflows and activities prior to the first scan/entry/count of the first ballot anywhere or by any means.  The pre-election phase ends when the first ballot somewhere is scanned/entered/counted.  The 'during' or 'active' election phase is when ballots are being scanned/entered/counted.  NIST implies this phase starts when the first [voting session](https://pages.nist.gov/ElectionGlossary/#voting-session) regardless if the ballot is cast as in person, absentee, early voting, or vote-by-mail.  The active election phase ends when _all the polls close_.  _All the polls close_ is when it is no longer possible to cast a new ballot anywhere again regardless of the type of voting session (in-person, early, absentee, by mail, etc).  This excludes ballots that have already been _accepted_ and not yet scanned/entered/counted.  Note that the specific and detailed definition of _accepted_ can vary from state to state.

## 2.1) Pre-election workflows

When an election is initiated, the root election GGO will fork the VTP product repositories.  If there was a previous VTP election, the git changes of that prior election can be merged into the new fork, perhaps significantly reducing the costs of configuring the new election.

The election officials across the GGOs of the election will work both independently on their own configuration as well as with the other GGOs.  All the changes will git push into the VTP election repos for this specific election and be pulled back down by the GGOs.  As per the "../tech/github-devsecops-overview.md" overview there is an always on CI/CD pipeline vetting all pushed changes before a change can be merged into the VTP root level repositories and pulled by other GGOs.  Note - similar to any software development project using git, GGOs can freely share changes directly between themselves if they so choose.  But regardless of that level a sharing, all changes need to pass the CI/CD pipeline before merging into the root repositories.

A primary design point of VTP is the efficacy of the CI/CD pipeline that are an integral part of VTP.  Changes can be vetted in minimal time and thus with minimal cost, including changes to the GGO's specific ballot sections.  The CI/CD pipeline includes tests to make sure the correct addresses are receiving the correct contests.

At some point the complete blank ballot is declared both accurate and complete.  Note that all changes to the ballot have authors and all changes are included in the full public ledger.  Note that VTP can print address specific ballots on demand as well as making available soft copies that any voter can view beforehand.

At this time any GGO that will be accepting and scanning ballots, nominally at the precinct level, will enter voter id into VTP if they are using another system to track voter registration.  The automatic import of voter id information will be supported for various data formats.  And with all things VTP, these voter registration commits will also need to be PGP signed and pushed to the VTP root repositories.

## 2.2) Vote-by-Mail and other pre-election workflows

Vote-by-mail, absentee, and early voting workflows can commence once the ballot is finalized.  Scanning/entering/counting ballots will transition the VTP election phase from pre-election to active-election.

In vote-by-mail and absentee, depending on how the precinct is handling vote-by-mail and absentee, the ballots may be created in soft form and emailed/digitally delivered or printed as hardcopy and physically posted.

If the precinct is supporting early voting in person, then an election day workflow is supported in a physical voting center.  As with election day in-person voting, a ballot receipt will not be available until a sufficient number of people have voted so to be able to sufficiently randomize the public keys.

## 2.3) Election day workflows

On election day in a voting center, the election official workflows match the in-person voter workflow described in section 1.1 above.  Specifically:

1) An election official asks the voter to identity themselves
2) An election official verifies their identity and registration status
3) An election official gives the voter an address specific blank ballot
4) An election official directs/assists the voter to a private location to fill in their ballot
5) An election official directs/assists the voter to a semi private VTP scanner.  The election observes from a distance:
    1) Observes the voter privately inserting their ballot into a VTP scanner
    2) Observer the voter accept/reject the ballot.  Note that the election cannot tell at this whether the ballot was accepted or rejected.
    3) Depending on the VTP configuration for this voting center, the election official may:
       1) Assist the voter in destroying their current ballot and obtaining a new ballot if they rejected their current ballot
       2) Assist the voter in returning to a private location to correct their ballot
       3) Assist the voter to checking out from the voting center if their ballot was accepted by the VTP scanner.  The voter may or may not have decided to receive a ballot receipt.
6) Optional step - the voter proceeds to a second checkout voter ID location to re-identify themselves to another election official
7) Optional step - an election official may direct/assist the voter to a VTP ballot verifier scanner outside the primary voting area.  This is where the voter can verify prior to leaving the voting center that their ballot has been entered into the tally and is now part of the VTP ledger.

## 2.4) Post-election day workflows

Once all the polls close, election officials proceed with their post election day activities.  With a VTP election, this will include various audits as well as verifying that all the ballots have been pushed from all the VTP scanners to the VTP git server handling the voter center.  Ultimately the VTP git server changes will need to be pushed to the VTP election remote servers, a pull request created following the various authentication, authorization, and security protocols.  Once the pull request has been merged, it will be available from the VTP root servers.

Note - the public never accesses the VTP root servers - the public only can access the readonly clones of the secured VTP election servers.

Note - the update the VTP election servers by the voting center election officials can occur by several different means, either electronically or manually by actual delivery of the VTP server or a copy of the VTP data.

## 3) End-to-End Validation (E2EV) Audits

E2EV audits can occur almost at any time, but primarily and should occur after all the polls close so to not interrupt election officials and not require audits of the auditors (since in that case they would then be part of the election and subject to auditing as well).  Note that nominally and for reasons of transparency and trust, VTP only audits occur on the public readonly copies of the data as that is the data that the public will also be scrutinizing.  Because of the low latency of the VTP solution, VTP based audits, whether they concern the ballots or the recorded voter IDs, can be performed by anyone.

The VTP only audits are different than paper audits that can/should also occur.  The paper based audits can be done either by election officials or by qualified 3rd party independent teams.  Note that the VTP scanner will securely mark the paper ballot and associate it with its digital scan.  The mark is created in an anonymous and cryptographic manner such that given a paper ballot, one can identify the associated contest CVRs.  Thus if a specific ballot or a set of ballots are deemed to be illegitimate, they can be removed by an election official by adding an additional git commit to the associated VTP repository.  As with all git commits, the commit must be PGP signed, pushed, pull requested, approved, and merged.

An important aspect regarding this step is that the voter whose ballot has been rejected needs to be able to know this and be given the opportunity to challenge its removal if they so choose.  Note that the ballot receipts have been cryptographically created in such a way that one needs direct access to a set of operational private keys specifically generated for the specific election.  These keys, associated with but in addition to the [CA](https://en.wikipedia.org/wiki/Certificate_authority) chain created for this election, are distributed in a certain way to competing and separate parties such that voters and other 3rd parties cannot create legitimate ballot receipts.

Given the anonymous nature of a VTP election, E2EV procedures will not be able to decode or identify ballot owners without a collusion between a super majority of the voters, election officials, and auditors.  That is, if most everyone is colluding to hold an illegitimate election, then an illegitimate election can occur.

