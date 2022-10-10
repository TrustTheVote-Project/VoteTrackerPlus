## The Pitch

VoteTracker+ is an open software ballot tracking system that increases the security, accuracy, and trustworthiness of a paper ballot election by cryptographically tracking the [Cast Vote Records](https://pages.nist.gov/ElectionGlossary/#cast-vote-record) associated with paper ballots.

### VoteTracker+ provides three core capabilities:

1. Directly supplies a cryptographically anonymized ballot check back to the voter, allowing the voter to validate that their specific ballot has been interpreted, recorded, and tallied as intended - a.k.a. End-to-End Verification ([E2EV](https://en.wikipedia.org/wiki/End-to-end_auditable_voting_systems))

2. Cryptographically records and seals the entire history of the election as it occurs in near real time

3. Allows the public to inspect and validate the official Cast Vote Records and tally as well as (ideally) the aggregate voter ID rolls across the entire electorate

### VoteTracker+ provides complete E2EV

VTP provides E2EV, specifically the E2EV properties of  __cast as intended__, __recorded as cast__, and __tallied as recorded__, without the need to encrypt the data-at-rest - without the need to encrypt the [OCR'ed](https://en.wikipedia.org/wiki/Optical_character_recognition) CVRs of the ballot.  VTP accomplishes this by privately and securely passing back to the voter their specific ballot check ID in a paperless, anonymous manner while also printing an anonymized paper based receipt.  Neither needs encryption.  The paper based receipt contains hundreds of randomized and anonymized checks, only a handfull belonging to the voter.

If one runs the demo included in this repo, one can witness the delivery of these three properties live:

#### Cast as Intended

The [CLI](https://en.wikipedia.org/wiki/Command-line_interface) (shell) output below shows the CLI based VTP demo accepting an interactive ballot from the user, offering the user a chance to self adjudicate the OCR of their ballot before it is officially submitted into the tally.  The user is prompted to accept or reject how the scanner has interpreted their paper ballot.

```bash
% ./vote.py --state=California --town=Alameda --address="123 Main Street"
Running "git rev-parse --show-toplevel"
Running "git pull"
Already up to date.
Running "/opt/VoteTrackerPlus/demo.15/clients/scanner.00/VTP-root-repo/bin/cast_ballot.py -v 3 -s California -t Alameda -a 123 Main Street"
Running "git rev-parse --show-toplevel"
################ (1 of 7)
Contest 0000: US president
- This is a rcv tally with 1 open position(s)/choice(s).  Regardless up to 6 selections can be rank choosen.
  [0] Mitt Romney
  [1] Phil Scott
  [2] Ron DeSantis
  [3] Kamala Harris
  [4] Cory Booker
  [5] Beta O'rourke
Please enter in rank order the numbers of your choices separated by spaces: 3 4 5
################ (2 of 7)
Contest 0001: US senate
- This is a rcv tally with 1 open position(s)/choice(s).  Regardless up to 4 selections can be rank choosen.
  [0] Larry Hogan
  [1] Greg Abbott
  [2] Pramila Jayapal
  [3] Alexandria Ocasio-Cortez
Please enter in rank order the numbers of your choices separated by spaces: 1
################ (3 of 7)
Contest 0002: governor
- This is a plurality tally
- The voting is for 1 open position(s)/choice(s) - only that number of selections can be choosen.
  [0] Brian Kemp
  [1] Bernie Sanders
Please enter the number for your choice: 1
################ (4 of 7)
Contest 0003: County Clerk
- This is a plurality tally
- The voting is for 1 open position(s)/choice(s) - only that number of selections can be choosen.
  [0] Jean-Luc Picard
  [1] Huckleberry Finn
  [2] Peggy Carter
Please enter the number for your choice: 1
################ (5 of 7)
Contest 0005: mayor
- This is a rcv tally with 1 open position(s)/choice(s).  Regardless up to 4 selections can be rank choosen.
  [0] Twenty Seven
  [1] Twenty Eight
  [2] Jane Doe
  [3] John Doe
Please enter in rank order the numbers of your choices separated by spaces: 1
################ (6 of 7)
Contest 0006: Question 1 - school budget override
- This is a plurality tally
- The voting is for 1 open position(s)/choice(s) - only that number of selections can be choosen.
  [0] yes
  [1] no
Please enter the number for your choice: 1
################ (7 of 7)
Contest 0007: Question 2 - new firehouse land purchase
- This is a plurality tally
- The voting is for 1 open position(s)/choice(s) - only that number of selections can be choosen.
  [0] yes
  [1] no
Please enter the number for your choice: 1
Contest 0000 - US president: ['3: Kamala Harris', '4: Cory Booker', "5: Beta O'rourke"]
Contest 0001 - US senate: ['1: Greg Abbott']
Contest 0002 - governor: ['1: Bernie Sanders']
Contest 0003 - County Clerk: ['1: Huckleberry Finn']
Contest 0005 - mayor: ['1: Twenty Eight']
Contest 0006 - Question 1 - school budget override: ['1: no']
Contest 0007 - Question 2 - new firehouse land purchase: ['1: no']
Is this correct?  Enter yes to accept the ballot, no to reject the ballot: yes
[...]
```

Once the user has typed 'yes' above (this is just a demo), then VTP virtually prints the ballot receipt to a file (this is just a demo) and prints the voter's ballot index to the screen (this is just a demo):

```bash
[...]
############
### Receipt file: /opt/VoteTrackerPlus/demo.15/clients/scanner.00/VTP-root-repo/ElectionData/GGOs/states/California/GGOs/towns/Alameda/CVRs/receipt.csv
### Voter's row: 36
############

```

#### Recorded as Cast

Once the voter has been out-processed by an election official and before leaving the voting center, they can optionally place their ballot check in a read-only VTP ballot check scanner which will validate whether or not all the digests on the ballot check are correct.

```bash
% ./verify_ballot_receipt.py -f ../../receipts.51.csv -r 51
Running "git rev-parse --show-toplevel"
Running "git pull"
Already up to date.
Running "git cat-file --buffer --batch-check=%(objectname) %(objecttype)"
Contest '0000 - US president' (14d1c99f8a103bb3c3a44e2e63a401e4d16b9951) is vote 474 out of 487 votes
Contest '0001 - US senate' (12b284558b353e3d07ae6d4da0fb0c7a2dc95af7) is vote 218 out of 488 votes
Contest '0002 - governor' (acd523562bdb07d70f10ed6d9558b73c90dad5f5) is vote 228 out of 489 votes
Contest '0003 - County Clerk' (5d1d66a1743eeab5b7c3374872e45fd1de576b14) is vote 278 out of 489 votes
Contest '0005 - mayor' (4ab59d49787ff9377439ad6142544435bfcde1e3) is vote 229 out of 489 votes
Contest '0006 - Question 1 - school budget override' (89858304146236e3959b4942dfd0adc0194750fc) is vote 195 out of 489 votes
Contest '0007 - Question 2 - new firehouse land purchase' (f68885250d8ec2f31e3346c6098bd8ae470676e0) is vote 314 out of 488 votes
############
### Ballot receipt VALID - no digest errors found
############
```

#### Tallied as Cast

Once all the polls close and election officials have begun to upload the VTP repositories to their secure remote servers, read-only public copies of those repositories are made available to the general public.  As more results are uploaded, the general public can clone/download the read-only copies and both validate their ballot check and tally all the contests.


