UVBM VOTING

# 1) Pre-election day (background)

Election officials identify the registered voters by recording them in the VOTES voter-id repo.  They also configure how/when they close VOTES voter registration - it can occur eithr prior to or on election day.  They also configure whether they allow in-person voting or not, and whether in-person voting is restricted to the UVBM distributed ballots or if the voter can create a new ballot in person.

# 2) How the ballots are physically mailed is TBD (decisions need to be made regarding potential APIs and/or native VOTES capabilities).  Regardless VOTES is used to physically print the specific voter ballot with the associated ballot digest.  VOTES can also be used to electronically create the specific voter ballots as well - configurable.

The ballots are mailed out to the registered voters.  Note that similar to in-person voting the precinct pre election day has entered into the VOTES voter-id repo the names and addresses only of the registered voters.

# 3) The voters receive the ballots and fill them out.  If received electronically the voter prints the ballot and voter-id paper (whatever the precinct and pre-configured that to be).  The voter returns the ballot and voter-id form.

# 4) At times chosen by the election officials, ballots are scanned similar to absentee voting.  And similarly election officials have several options to choose from regarding the details regarding how they handle invalid ballots.

When scanning UVBM ballots. election officials have the option of scanning the voter-id paperwork at the same time.  If so, VOTES can take care of all the transactions thus enabling mass input of the ballots.  Or similar to absentee ballots, the ballots can be manually entered one at a time by election officials.

If the latter, the UVBM workflow is similar to absentee workflows.  The ballots are manually entered by election officials.

If mass scanning, both the voter-id paperwork is scanned as well as the ballot.  If VOTES is doing the scanning of both documents, the VOTES ballot repo has been configured with the printed format layout of the voter-id paperwork so that it can be directly scanned by VOTES.  If a 3rdparty is scanning the voter-id, the 3rdparty software scans the voter-id, calls into the VOTES API regarding voter-id, and then passes the scan of the ballot to VOTES.

TBD - work is needed here to determine the viability of whether or not there can be a 3rdparty approach to this or if VOTES itself needs to include the ability of mass scanning and what that means security model wise - TBD.

It is configurable how invalid ballots are handled during mass scanning.  Election officials may want to physically inspect the physical invalid ballots, they may want to allow the voter to try again, etc.  The security model and security requirements depend on whether the mass scanners are provided by VOTES or provided by a 3rdparty.

