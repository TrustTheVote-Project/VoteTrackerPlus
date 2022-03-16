ABSENTEE VOTING

# 1) The election officials received a request for an absentee ballot.

# 2) They identify the voter.

# 3) The election official enters the absentee request into the VOTES voter-id repo indicating the request.  Note the VOTES voter-id is soley the voter's name and address.  It is up to the state how to handle absentee and in-person voting - VOTES by default allows only one vote (submitted ballot) per voter-id.  But also by default VOTES will allow a person to change their ballot type (in-person, absentee, early, etc) up until a ballot is cast.

# 4) The election official gives/sends an absentee ballot to the voter.  The identification requirements is an additional and separate paper, printed by VOTES, configured by the precinct/state.

# 5) The voter receives the ballot, fills it in, and signs the ballot in accordance to the precincts identification requirements.  The ballot is sent back by the voter to the election officials.

# 6) Upon receipt of the ballot, election officials validate the voter as they will, either then or later.  The voter's ballot can be entered either prior to, on, or after election day.

# 7) When the ballot is processed, an election official inspects the VOTES voter-id repo to independently validate the state of the voter-id (similar to in-person voting).

If the voter identification process is valid, the ballot is scanned.  The ballot processing is per ballot and mirrors the in-place voting procedures caveat that there is no voter present (see in-person voting).  The election official will hit the 'voting' button for the voter who has been properly identified.  If the voter has not voted and the ballot is not invalid, it is submitted.  As with in-person voting the VOTES voter-id and ballot repos are updated.

If invalid, similar to in-person the reason is displayed and the ballot as scanned is stored in a different section in the VOTES ballot repo.  It is up to the election officials to choose a specific workflow (the workflow is configurable) - they could notify the user and allow them to try again.  Or they may block the voter from trying again.

Note the workflow configuration is contained in the VOTES ballot repo and is fully open source.

Note that the voter can record their ballot digest and/or the election official may record the voter's ballot digest.  Note that that this digest is __not__ recorded in either VOTES repo and as such does not really mean much to the voter at that time.  After the polls have closed, the voter can contact the election officials and validate either their physical ballot with that digest or their VOTES scanned copy with the electronic ballot digest obtained by in-person, non third-party verifiable, inspection with an election official.

Regardless the public has direct access to all the public electronic VOTES voter-id and ballot digests but not the physical ballots.

Storage, management, and access to the physical ballots is outside of VOTES technologies.  A precinct may optionally record the procedures in VOTES if they so desire only as a way to publicly describe it.
