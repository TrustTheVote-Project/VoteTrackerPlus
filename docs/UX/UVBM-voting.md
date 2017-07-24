UVBM VOTING

# 1) Pre-election day (background)

Election officials identify the registered voters by recording them in the VOTES voter-id repo.  They also configure how/when they close VOTES voter registration - it can occur eithr prior to or on election day.  They also configure whether they allow in-person voting or not, and whether in-person voting is restricted to the UVBM distributed ballots or if the voter can create a new ballot in person.

# 1) The ballots are mailed out per the registered (detailed) voter database maintained by the state/precinct.  Note that similar to in-person voting the precinct pre election day has entered into the VOTES voter-id repo the names and addresses only of the registered voters.

# 2) The ballots are returned.

# 3) At times chosen by the election officials, ballots are scanned similar to absentee voting.  And similarly election officials have several options to choose from regarding the details of whether or they desire to automatcally return digests to the user.

# 4) The ballots are scanned with legitimate ballots being entered and un-readable or invalid ballots being rejected.

When scanning UVBM ballots. election officials have the option of scanning the voter-id's at the same time.  If so, VOTES can take care of both the uploading of the voter-id and the ballot itself to the two respective repos.  Or the election officials can mimic the in-person workflows.
