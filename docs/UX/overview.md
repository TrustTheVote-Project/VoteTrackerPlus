AN OVERFIEW OF THE WORKFLOWS AND USER EXPERIENCE OF VARIOUS ROLES REGARDING THE USE OF VOTES

# 1) How does an end voter interact with VOTES?

# 1.1) For the voter who physically casts a ballot at a voting center, the experience is mostly the same but with a few minor tweaks.

After the voter successfully identifies themselves to the election official, the election official will supply a numbered but anonymous VOTES printed blank ballot.  The ballot contains a checkbox allowing the voter to receive the public key for their ballot.  After completing as much of the ballot as desired in private, the voter transitions to the VOTES ballot casting station.  With optional assistance from an election official, the ballot is scanned and either rejected or accepted.  A rejected ballot is one where some portion of the ballot is either un-readable or non compliant/invalid.  If accepted and if the voter asked for a public key, a receipt is printed containing ~100 public keys and via a private display, the voter is shown which public key is theirs.

# 1,2) Once all the polls close, the voter can inspect their specific electronic ballot

Once all the polls close, the voter can inspect their electronic ballot in two ways.  They can download the ballot public ledger (the repository) and lookup their ballot via their public key.  The ledger contains all the cast ballots via their public keys.  So every voter can validate their electronic copy of their ballot.

It is important to note that the public keys are NEVER made available to voters in a manner that allows the any third party to identify a ballot with a specific voter even when a third party is given the public key.  For example:

When the voter is physically casting their ballot at a voting center, they are visually (or verbally) given the public key privately as an index into a sufficiently large list of valid public keys.  The list of public keys  itself cannot identify the voter's specific ballot.

# 1.3) Once all the polls close, the voter can perform the election tallies

Since the public ledger also contains the tally algorithm for all races and contests for all ballots, the voter can perform their own instance of the tally.  Since the ledger is cryptographically sealed, all copies of the ledger are known to be the same.

Note that the private keys are never publicly available and in fact are double encrypted requiring two independent certificate authorities to decode while also requiring the full ledger record of the double decoding. 

# 1.4) Once all the polls close, the voter can inspect their physical ballot

Though VOTES generates and maintains in a secure way an electronic copy of the ballot, it is the responsibility of the local election officials to maintain the security surrounding the physical ballots.  Depending on the procedures and resources available at the precinct  level, the precinct may support the voter inspecting the their physical ballot, or may not.  Regardless, the possibility of this procedure is important in maintaining public trust in the election since both the physical and electronic copies of the ballot are independently identifiable in a secure manner.

When physical ballot identification is supported, the voter can physically visit the election official and after properly identifying her/himself, the election official can initiate the identification of the physical ballot.  Similar to privately identifying the electronic ballot to a voter, a physical ballot identification requires both the state (the governing geographical/geopolitical overlay - the governing GGO) and the operators of the VOTES SaaS election to independently decode a private VOTES repository with their independent private keys so to identify a physical ballot.  Doing so requires the creation of a full record of the decoding of such an identification within the private full ledger itself.  This supports full transparency tracking of every ballot identity decoding, limiting the abuse of such a feature.

Once this physical ballot identification is made privately available to the local election official, the official can initiate a physical lookup of the physical ballot.  Note - both steps are not automatic and require human interaction and as such neither step is instantaneous.  Both steps require some amount of time to execute - it may require several days depending on the local available resources and the physical security surrounding the physical ballots.

# 1.5) Absentee ballot and Vote-by-mail ballot identification

When voting by mail or by absentee ballot, the voter's specific public key can only be made available in a private manner similar.  By keeping the identity of the public key private, the public key cannot be used to identity the ballot owner (the voter), only the ballot.

The governing GGO can choose its own specific method of revealing a voter's specific public key.  As one example for absentee ballots and vote-by-mail scenarios, the voter might be required to physically visit an election official and after proper identification, the official can then give the voter their specific public key in a private manner similar to the non vote-by-mail scenario above.  The act of identifying an electronic ballot after the polls close requires a double and independent decryption of the ballot identity which is also recorded in the same full ledger private repository.

# 2) How does an election official interact with VOTES?

The election official interaction depends on whether the phase of the election is pre-election day, election day, or post-election day.

# 2.1) Pre-election workflows

# 2.2) Election day workflows

# 2.3) Post-election day workflows

# 3) End-to-End Validation (E2EV) Audits

As a quick background, the first end-point for E2EV occurs when the voter casts her/his ballot, regardless of how that happens (physically at a voting center, by mail, by absentee, etc).  A second end point is the VOTES public repository that contains the blank and cast ballots, the tally algorithms, and other public information.  A third end point is the secured physical ballots.

E2EV procedures occur without decoding/identifying the ballot owners as with current non-VOTES managed elections and can occur against any of the three above end points.

ZZZ: see E2EV auditing references

Without decoding the ballot owners, election officials can compare the physical ballots not just in a tally manner as with today's non-VOTES elections, but can also compare the physical ballots against the individual electronic copies maintained in VOTES.  Audit teams will be able to leverage database queries to actually match physical ballots with their specific electronic copies and detect anomalies.
