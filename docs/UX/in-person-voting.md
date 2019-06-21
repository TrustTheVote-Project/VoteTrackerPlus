IN PLACE VOTING - when a voter physically shows up at a voting center to vote on election day

There are two checkin tables, one to checkin and receive a ballot; one to checkout and scan the completed ballot.

# 1) Voter shows up at the voting center

# 2) Voter selects precinct and waits in the checkin line.  Identifies themselves to the election official for that precinct

# 3) Voter may witness election official checking off their name.  If there are no pre-printed ballots for that precinct, VOTES prints the voter's ballot which contains an anonymous digest ID.  The election official gives the voter their address specific ballot.

# 4) Voter fills in the ballot privately.  No third party witnesses or devices are allowed except where accessibility is at issue, in which one or more assistents may be present.  Active recording devices are not allowed regardless.

# 5) Voter goes to checkout line and identifies themselves a second time.  Voter may witness election officials checking off their name again.  The ballot is placed in the scanner.  If there is a valid scan, the ballot is accepted.

Upon successful scan, the voter is free to leave or privately obtain a reference to their specific ballot's public key once enough ballots have been scanned to provide sufficient randomness/anonymity.  Obtaining a copy of the public key requires successfully checking a box on the ballot requesting such.  Once enough ballots have been scanned, the voter can receive a paper with 100 or more public keys.  The election official at the scanning station, who does not see the random-and-unique list printed for the specific VOTER, privately conveys to the voter the offset/index into the list of their public key.

If the request-the-public-key checkbox was not checked off on the ballot, neither is printed/displayed.

Note - if the minimum ballot count is 100, then the only the first 100 voters need to wait.  If at least 100 absentee or early ballots have already been counted for that voting center, then there is no wait for public digests.

If the scan is not valid, the VOTES display will display the reason for the invalid scan and the ballot is physically rejected from the scanner.  The voter is free to either leave or try again.  To try again, the election official at the scanner hits the "invalidate" button for the ballot, and another ballot is printed.  The original ballot is shredded by the election official - regardless it is no longer scannable and not stored anywhere in VOTES.  (All unscannable ballots are physically rejected by the scanner).  Though VOTES supports the ability for the voter to try again, it is up to the election officials to have configured their voter UX workflow to support additional voting attempts.

Regardless, VOTES will only ever accept one ballot per voter even if the election official prints a second ballot and then attempts to scan both of them.
