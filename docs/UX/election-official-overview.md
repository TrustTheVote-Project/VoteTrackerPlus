AN OVERVIEW OF THE WORKFLOWS / USER EXPERIENCE OF VARIOUS ROLES REGARDING THE USE OF VOTES

# 1) How does an end voter interact with VOTES?

# 1.1) For the voter who physically casts a ballot at a voting center, the experience is mostly the same but with a few minor tweaks.

After the voter successfully identifies themselves to the election official, the election official supplies a numbered but anonymous VOTES printed blank ballot.  The ballot contains a checkbox allowing the voter to receive the public key for their ballot.  After completing as much of the ballot as desired in private, the voter transitions to the VOTES ballot casting station.  With optional assistance from an election official, the ballot is scanned and either rejected or accepted.  A rejected ballot is one where some portion of the ballot is either un-readable or non compliant/invalid.  The rejected portion of the ballot and the reason thereof is privately shown to the voter.  A rejected ballot is not accepted by the VOTES ballot casting equipment and is ultimately shredded.

When accepted and if the voter asked for a public key, a receipt is printed containing ~100 public keys.  The voter is then privately shown the index (which public key in the list is theirs).  Note - if the precinct is small or if there are not at least ~100 cast ballots with the same set of GGO's, then the public key is not available.

If rejected, the voter can receive a new blank ballot (again numbered but anonymous) printed at the VOTES ballot casting station.  Or with the help of an election official and after the voter acknowledges that those portions of their ballot that cannot be scanned will in fact not be counted, the ballot can be forced scanned where only the scan-able portions of the ballot are entered - the unscannable races are not counted.

# 1.2) Once all the polls close, the voter can inspect their specific electronic ballot

Once all the polls close, the voter can inspect their electronic ballot in two ways.  They can download the ballot public ledger (the repository) and lookup their ballot via their public key.  The ledger contains all the cast ballots via their public keys, so every voter can validate their electronic copy of their ballot.

It is important to note that the public keys are NEVER made available to voters in a manner that allows the any third party to identify a specif  ballot with a specific voter even when a third party is given the public key.  For example:

When the voter is physically casting their ballot at a voting center, they are visually (or verbally) given the public key privately as an index into a sufficiently large list of valid public keys.  The list of public keys itself cannot identify the voter's specific ballot.

When voting by mail, absentee ballot, or other by mail systems, the voter is only allowed to receive their public key in a manner by which a third party cannot verify its owner - the public key is delivered is a privately secure manner.  Note that such a capability implies that election officials will handle information that ties a specific ballot to a specific voter.  It is up to the election officials to decide if and how they wish to support optionally giving voters their public keys and if voters wish to have elections officials perform this function.

# 1.3) Once all the polls close, the voter can perform the election tallies

Since the public ledger also contains the tally algorithm for all races and contests for all ballots, the voter can perform their own instance of the tally.  Since the ledger is cryptographically sealed, all copies of the ledger are known to be the same.

Note that the private keys are never publicly available and in fact are double encrypted requiring two independent certificate authorities to decode while also requiring the full ledger record whenever a key or keys are decoded. 

# 1.4) Once all the polls close, the voter can validate their physical ballot

Though VOTES generates and maintains in a secure manner an electronic copy of the ballot, it is the responsibility of the local election officials to maintain the security surrounding the physical ballots.  Depending on the procedures and resources available at the precinct level, the precinct may support the voter validing their physical ballot.  Regardless, the possibility of this procedure is important in maintaining public trust in the election since both the physical and electronic copies of the ballot are independently identifiable in a secure private manner.  With two copies, one copy can be checked against the other.

If a voter believes that the electronic copy of their ballot is not correct, they can initiate an inspection of their physical ballot if such inspection is supported.

When physical ballot validation is supported, the voter can physically visit the election official and after properly identifying her/himself and their public key, which may require (TBD) photo based identification beyond that what is required at the voting center, the election official can initiate the validation of the physical ballot.  VOTES maintains data that matches the electronic copy with the physical copy.  Given the voter's public key, the election official can track down the specific matching physical ballot and validate that the entered selections match the electronic copy.  If the voter is still not satisfied, the election official can show the voter the physical ballot in a private manner without the presense of electronic or other recording devices such that no third party can see the physical ballot.  This is because the voter can mark ballots in such a way as to uniquely identify them to themselves or others.  And though 'personalizing' a physical ballot is in general a good thing, is something that necessitates any physical ballot inspection to be done completely isolated from any third party observation.  This includes durinfg any E2EV.

The ability to have voters return to the election officials and inspect their specific physical ballot increases the level of trust in the election.

# 1.5) Absentee ballot and Vote-by-mail ballot identification

When voting by mail or by absentee ballot, the voter's specific public key can only be made available in a private manner similar to section 1.4 above.  By keeping the identity of the public key private, the public key cannot be used to identity the ballot owner (the voter), only the ballot.

The governing GGO can choose its own specific method of revealing a voter's specific public key.  As one example for absentee ballots and vote-by-mail scenarios, the voter might be required to physically visit an election official and after proper identification, the official can then give the voter their specific public key in a private manner similar to the non vote-by-mail scenario above.

# 2) How does an election official interact with VOTES?

The election official interaction depends on whether the phase of the election is pre-election day, election day, or post-election day.

# 2.1) Pre-election workflows

At the state level (in the US this would be the _outer_ GGO level), in an interative agile software development manner the state election officials would start to fill in their portion of the ballot.  The VOTES public repo comes with a test framework that allows the state election officials to test their portion of the ballot with the portions of the ballot thus far published by the other GGOs.  This is true both for ballot questions whether they be races or questions.

Similarly, each GGO can independently iterate on their portions of the ballot.

Note that each GGO maintains a definition of what is required to have that portion of the ballot be present (to be presented) to a specific voter.  Each voter is associated with some address or some other identifying characteristic.  Nominally it is their address.  For a state, the voter must be a resident of the state (the voter's address must be within the state).  The same is true for a precinct, town, county, school district, etc.  Each GGO has more or less a GPS/location based identification.  When a specific voter is to recieve their ballot, by any means, their ballot is custom printed for that address.

At some point the ballot in total is declared done.  Note that all changes to the ballot have authors and all changes are included in the full public ledger.  (Implentation note - since the prototype is using git as the repository technology, distributed git workflows generally apply.)

The VOTES system handles the printing of the ballots whether the ballots are created via hard or soft copy.

In addition to the ballot repository, the precinct also updates the VOTES voter-id repository with the registers voters, entering the name and the address.

# 2.2) Vote-by-Mail and other pre-election day ballot casting workflows

Vote-by-mail, absentee, and early voting workflows can commence once the ballot is finalized.  In vote-by-mail, each voter's specific ballot is printed and mailed.  Depending on how the precinct is handling absentee and early voting, the ballots may be printed in soft form and emailed or printed as hardcopy and posted.

If the precinct is supporting early voting in person, then the election day workflow is supported.  However, when early voting the public key will not be available until a sufficient number of people have voted so to be able to sufficiently randomize the public keys.  In some cases, the public key will not be available until after all the poles close.  In some cases it will never be available if the minimum number of cast ballots necessary to insure a minimal level of voter anonimity is not attained.

# 2.3) Election day workflows

On election day in a voting center, the election official workflows match that of section 1.1 above.  Election officials first identity the voter.  Once identified, a ballot specific to their address is supplied, either being printed on demand or from a pre-printed supply.  An election official leads the voter to a private voting location where the ballot can be filled out privately.  The voter then proceeds to the VOTES ballot casting location where the ballot is scanned and is either accepted or rejected.  See section 1.1.

As ballots are cast, the ballots are processed by the VOTES system both locally at the voting center and via the SaaS implementation.  At certain intervals the local data is securely pushed to the SaaS implementation.  Both sets of data are independently monitored by both local and remote officials.  The security monitoring is continuous.

Once all the poles close, the synchronization intervals continue until all the data has been synchronized.  Once all the precincts have synchronized their data with the SaaS implementation and the security monitoring has addressed all the real and potential issues that have occurred, both independent CA authorities can declare the election sealed.  Once declared sealed by both authorities, the final public key(s) in the public VOTES repository are made available as well as the full ledger repository itself.  Note - the same is done for the non-public VOTES repository key(s) except that the repository itself remains private.

# 2.4) Post-election day workflows

Once made available, the public repository can be downloaded (cloned) and can be used to independently tally all races and contests.  In addition voters who know their public key can validate their electronic copy of their ballot.

# 3) End-to-End Validation (E2EV) Audits

As a quick background, the first voter end-point for E2EV occurs when the voter casts her/his ballot, regardless of how that happens (physically at a voting center, by mail, by absentee, etc).  A second voter end point is the VOTES public repository that contains the blank and cast ballots, the tally algorithms, and other public information.  A third voter end point is the secured physical ballots.

E2EV procedures occur without decoding/identifying the ballot owners as with current non-VOTES managed elections and can occur against any of the three above end points.

TBD: see E2EV auditing references

Without decoding the ballot owners, election officials can compare the physical ballots not just in a tally manner as with today's non-VOTES elections, but can also compare the physical ballots against the individual electronic copies maintained in VOTES.  Audit teams will be able to leverage database queries to actually match physical ballots with their specific electronic copies and detect anomalies.
