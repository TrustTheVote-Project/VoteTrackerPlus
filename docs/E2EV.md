## VoteTracker+ provides full E2EV

VTP provides E2EV, specifically the E2EV properties of __cast as intended__, __recorded as cast__, and __tallied as recorded__, without the need to encrypt the data-at-rest - without the need to encrypt the [OCR'ed](https://en.wikipedia.org/wiki/Optical_character_recognition) CVRs of the ballot.  VTP accomplishes this by privately and securely passing back to the voter their specific ballot check ID in a paperless, anonymous manner while also printing an anonymized paper based receipt.  Neither needs encryption.  The paper based receipt contains hundreds of randomized and anonymized validatable checks, only a handfull of which belong to a specific voter.

If one runs the demo included in this repo, one can witness the delivery of these three properties live:

### Cast as Intended

The [CLI](https://en.wikipedia.org/wiki/Command-line_interface) (shell) output below shows the CLI based VTP demo accepting an interactive ballot from the user, offering the user a chance to self adjudicate the OCR of their ballot _before_ it is officially submitted into the tally.  The user is prompted to accept or reject how the scanner has interpreted their paper ballot.

```
% ./vote.py --state=California --town=Alameda --address="123 Main Street"              
Running "git rev-parse --show-toplevel"
Running "git pull"
Already up to date.
Running "/opt/VoteTrackerPlus/demo.16/clients/scanner.00/VTP-root-repo/bin/cast_ballot.py -v 3 -s California -t Alameda -a 123 Main Street"
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
Please enter in rank order the numbers of your choices separated by spaces: 5 4 3
################ (2 of 7)
Contest 0001: US senate
- This is a rcv tally with 1 open position(s)/choice(s).  Regardless up to 4 selections can be rank choosen.
  [0] Larry Hogan
  [1] Greg Abbott
  [2] Pramila Jayapal
  [3] Alexandria Ocasio-Cortez
Please enter in rank order the numbers of your choices separated by spaces: 3 2
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
Contest 0000 - US president: ["5: Beta O'rourke", '4: Cory Booker', '3: Kamala Harris']
Contest 0001 - US senate: ['3: Alexandria Ocasio-Cortez', '2: Pramila Jayapal']
Contest 0002 - governor: ['1: Bernie Sanders']
Contest 0003 - County Clerk: ['1: Huckleberry Finn']
Contest 0005 - mayor: ['1: Twenty Eight']
Contest 0006 - Question 1 - school budget override: ['1: no']
Contest 0007 - Question 2 - new firehouse land purchase: ['1: no']
Is this correct?  Enter yes to accept the ballot, no to reject the ballot: yes
[...]
```

Once the user has typed 'yes' above (this is just a demo), then VTP virtually _prints_ the ballot receipt to a file and simulates privately passing the voter's ballot receipt index back to the voter by also printing it to the screen (this is just a demo):

```
[...]
############
### Receipt file: /opt/VoteTrackerPlus/demo.16/clients/scanner.00/VTP-root-repo/ElectionData/GGOs/states/California/GGOs/towns/Alameda/CVRs/receipt.csv
### Voter's row: 87
############

```

### Recorded as Cast

Once the voter has been out-processed by an election official and before leaving the voting center, they can optionally place their ballot check in a read-only VTP ballot check scanner which will validate whether or not all the digests on the ballot check are correct.

First, check that _all_ the ballot digests are valid:

```
% ./verify_ballot_receipt.py -f /opt/VoteTrackerPlus/demo.16/clients/scanner.00/VTP-root-repo/ElectionData/GGOs/states/California/GGOs/towns/Alameda/CVRs/receipt.csv -r 87
Running "git rev-parse --show-toplevel"
Running "git pull"
Already up to date.
Running "git cat-file --buffer --batch-check=%(objectname) %(objecttype)"
Contest '0000 - US president' (793fc652bfea0cc8590e2c618bdcaf8605db26e7) is vote 225 out of 348 votes
Contest '0001 - US senate' (c09d2105936fe408379fcd7332fb88020f107a53) is vote 222 out of 347 votes
Contest '0002 - governor' (dfacf455e5081208b16a5f19bfa5b62465e8558d) is vote 323 out of 347 votes
Contest '0003 - County Clerk' (c70ddbeaf2a035d6354288b54d8ac9a05f499a11) is vote 172 out of 348 votes
Contest '0005 - mayor' (5f56fd3cd03ddc88e7934f2b58a267570d889212) is vote 256 out of 347 votes
Contest '0006 - Question 1 - school budget override' (1d66b23c07c6368833527ecc5d39c158ef6f4430) is vote 192 out of 348 votes
Contest '0007 - Question 2 - new firehouse land purchase' (46b0e916db2da2acfda582cbb539beecbc3bf23d) is vote 176 out of 347 votes
############
### Ballot receipt VALID - no digest errors found
############
```

And then to inspect a specific contest, for example the voter's choice for president:

```
% ./show_contest.py -c 793fc652bfea0cc8590e2c618bdcaf8605db26e7
Running "git rev-parse --show-toplevel"
Running "git log -1 793fc652bfea0cc8590e2c618bdcaf8605db26e7"
commit 793fc652bfea0cc8590e2c618bdcaf8605db26e7 (origin/CVRs/0000/3477211a60)
Author: Foo Bar <windoverwater@users.noreply.github.com>
Date:   Sat Jan 1 12:00:00 2022 -0500

    {
        "CVR": {
            "cast_branch": "CVRs/0000/3477211a60",
            "choices": [
                {
                    "name": "Mitt Romney",
                    "party": "Circle Party"
                },
                {
                    "name": "Phil Scott",
                    "party": "Circle Party"
                },
                {
                    "name": "Ron DeSantis",
                    "party": "Circle Party"
                },
                {
                    "name": "Kamala Harris",
                    "party": "Triangle Party"
                },
                {
                    "name": "Cory Booker",
                    "party": "Triangle Party"
                },
                {
                    "name": "Beta O'rourke",
                    "party": "Triangle Party"
                }
            ],
            "ggo": "GGOs/states/California",
            "name": "US president",
            "selection": [
                "5: Beta O'rourke",
                "4: Cory Booker",
                "3: Kamala Harris"
            ],
            "tally": "rcv",
            "uid": "0000"
        }
    }
```

### Tallied as Cast

Once all the polls close and election officials have begun to upload the VTP repositories to their secure remote servers, read-only public copies of those repositories are made available to the general public.  As more results are uploaded, the general public can clone/download the read-only copies and both validate their ballot check and tally all the contests.

```
 % ./tally_contests.py -c 0000                                                  
Running "git rev-parse --show-toplevel"
Running "git pull"
Already up to date.
Running "git log --topo-order --no-merges --pretty=format:%H%B"
Scanned 348 contests for contest (US president) uid=0000, tally=rcv, max=1, win-by>0.5
RCV: round 0
Total vote count: 348
[('Mitt Romney', 74), ('Kamala Harris', 62), ('Cory Booker', 61), ('Phil Scott', 60), ("Beta O'rourke", 46), ('Ron DeSantis', 45)]
RCV: round 1
Total vote count: 348
[('Mitt Romney', 87), ('Kamala Harris', 71), ('Phil Scott', 68), ('Cory Booker', 66), ("Beta O'rourke", 56), ('Ron DeSantis', 0)]
RCV: round 2
Total vote count: 347
[('Mitt Romney', 105), ('Kamala Harris', 88), ('Cory Booker', 79), ('Phil Scott', 75), ("Beta O'rourke", 0), ('Ron DeSantis', 0)]
RCV: round 3
Total vote count: 347
[('Mitt Romney', 127), ('Cory Booker', 113), ('Kamala Harris', 107), ('Phil Scott', 0), ("Beta O'rourke", 0), ('Ron DeSantis', 0)]
RCV: round 4
Total vote count: 347
Contest US president (uid=0000):
  ('Mitt Romney', 190)
  ('Cory Booker', 157)
  ('Kamala Harris', 0)
  ('Phil Scott', 0)
  ("Beta O'rourke", 0)
  ('Ron DeSantis', 0)
```

Note that in this demo election, the contest for US president is RCV, so by default the 5 rounds of RCV required to select a winner are printed.  The total vote count by round decrements in round 2 due to one voter only selecting two or less non-winning candidates for US president, so beginning on the third round their ballot no longer contributes votes to the contest.

If the voter wishes to see how their specific choices contribute to any contest, all their specific contest digests can verbosely tracked through the tally, offering significant insight and transparency regarding teh E2EV _counted as cast_ requirement:

```
% ./tally_contests.py -v 3 -t 793fc652bfea0cc8590e2c618bdcaf8605db26e7,c09d2105936fe408379fcd7332fb88020f107a53,dfacf455e5081208b16a5f19bfa5b62465e8558d,c70ddbeaf2a035d6354288b54d8ac9a05f499a11,5f56fd3cd03ddc88e7934f2b58a267570d889212,1d66b23c07c6368833527ecc5d39c158ef6f4430,46b0e916db2da2acfda582cbb539beecbc3bf23d
Running "git rev-parse --show-toplevel"
Running "git pull"
Already up to date.
Running "git log --topo-order --no-merges --pretty=format:%H%B"
Scanned 348 contests for contest (US president) uid=0000, tally=rcv, max=1, win-by>0.5
RCV: round 0
Counted 793fc652bfea0cc8590e2c618bdcaf8605db26e7: choice=Beta O'rourke
Total vote count: 348
[('Mitt Romney', 74), ('Kamala Harris', 62), ('Cory Booker', 61), ('Phil Scott', 60), ("Beta O'rourke", 46), ('Ron DeSantis', 45)]
RCV: round 1
Total vote count: 348
[('Mitt Romney', 87), ('Kamala Harris', 71), ('Phil Scott', 68), ('Cory Booker', 66), ("Beta O'rourke", 56), ('Ron DeSantis', 0)]
RCV: round 2
RCV: 793fc652bfea0cc8590e2c618bdcaf8605db26e7 (contest=US president) last place pop and count (Beta O'rourke -> Cory Booker)
Total vote count: 347
[('Mitt Romney', 105), ('Kamala Harris', 88), ('Cory Booker', 79), ('Phil Scott', 75), ("Beta O'rourke", 0), ('Ron DeSantis', 0)]
RCV: round 3
Total vote count: 347
[('Mitt Romney', 127), ('Cory Booker', 113), ('Kamala Harris', 107), ('Phil Scott', 0), ("Beta O'rourke", 0), ('Ron DeSantis', 0)]
RCV: round 4
Total vote count: 347
Contest US president (uid=0000):
  ('Mitt Romney', 190)
  ('Cory Booker', 157)
  ('Kamala Harris', 0)
  ('Phil Scott', 0)
  ("Beta O'rourke", 0)
  ('Ron DeSantis', 0)
Scanned 347 contests for contest (US senate) uid=0001, tally=rcv, max=1, win-by>0.5
RCV: round 0
Counted c09d2105936fe408379fcd7332fb88020f107a53: choice=Alexandria Ocasio-Cortez
Total vote count: 347
[('Alexandria Ocasio-Cortez', 94), ('Larry Hogan', 90), ('Pramila Jayapal', 84), ('Greg Abbott', 79)]
RCV: round 1
Total vote count: 347
[('Alexandria Ocasio-Cortez', 120), ('Larry Hogan', 114), ('Pramila Jayapal', 113), ('Greg Abbott', 0)]
RCV: round 2
Total vote count: 347
Contest US senate (uid=0001):
  ('Alexandria Ocasio-Cortez', 180)
  ('Larry Hogan', 167)
  ('Pramila Jayapal', 0)
  ('Greg Abbott', 0)
Scanned 347 contests for contest (governor) uid=0002, tally=plurality, max=1, win-by>0.5
Plurality - one round
Counted dfacf455e5081208b16a5f19bfa5b62465e8558d: choice=Bernie Sanders
Contest governor (uid=0002):
  ('Brian Kemp', 186)
  ('Bernie Sanders', 161)
Scanned 348 contests for contest (County Clerk) uid=0003, tally=plurality, max=1, win-by>0.5
Plurality - one round
Counted c70ddbeaf2a035d6354288b54d8ac9a05f499a11: choice=Huckleberry Finn
Contest County Clerk (uid=0003):
  ('Huckleberry Finn', 128)
  ('Jean-Luc Picard', 119)
  ('Peggy Carter', 101)
Scanned 347 contests for contest (mayor) uid=0005, tally=rcv, max=1, win-by>0.5
RCV: round 0
Counted 5f56fd3cd03ddc88e7934f2b58a267570d889212: choice=Twenty Eight
Total vote count: 347
[('Twenty Eight', 94), ('John Doe', 91), ('Jane Doe', 90), ('Twenty Seven', 72)]
RCV: round 1
Total vote count: 346
[('John Doe', 121), ('Twenty Eight', 119), ('Jane Doe', 106), ('Twenty Seven', 0)]
RCV: round 2
Total vote count: 346
Contest mayor (uid=0005):
  ('John Doe', 183)
  ('Twenty Eight', 163)
  ('Jane Doe', 0)
  ('Twenty Seven', 0)
Scanned 348 contests for contest (Question 1 - school budget override) uid=0006, tally=plurality, max=1, win-by>0.5
Plurality - one round
Counted 1d66b23c07c6368833527ecc5d39c158ef6f4430: choice=no
Contest Question 1 - school budget override (uid=0006):
  ('no', 187)
  ('yes', 161)
Scanned 347 contests for contest (Question 2 - new firehouse land purchase) uid=0007, tally=plurality, max=1, win-by>2/3
Plurality - one round
Counted 46b0e916db2da2acfda582cbb539beecbc3bf23d: choice=no
Contest Question 2 - new firehouse land purchase (uid=0007):
  ('no', 193)
  ('yes', 154)
```
