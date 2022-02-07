[VC](https://pages.nist.gov/ElectionGlossary/#vote-center) python executables

## 1) accept_ballot.py
- runs on a VTP scanner
- will run the necessary git commands to commit all contests to contest unique and specific branches and push them to the VC VTP remote
- input: a ballot.cvr file
- output: N contest specific git branches pushed to the VC VTP remote
- output: the voter's ballot receipt (a file during testing)
- output: the voter's ballot receipt row (either STDOUT or a file or as part of the voter receipt during testing)

## 2) generate_blank_ballot.py
- runs anywhere
- will parse all the config.yaml files in the election git tree and generate a blank ballot.
- initial version will just render a CVR compatible blank ballot.json file suitable for automated voting/casting of ballots for tests.  A later version can produce a ballot.pdf (from the sphinx/rst files).
- input: all config.yaml files
- input: all ballot.rst files
- input: an address
- output: a blank ballot.json file
- output: a blank ballot.pdf file

## 3) cast_a_ballot.py
- runs anywhere
- for testing only
- note - the caller will/can randomly or otherwise select the contest selections
- input:  a blank ballot.json file
- output: a valid ballot.cvr file containing 0 or more 'voter' selected contests

## 4) add_a_ballot.py
- runs on the VC VTP git server
- per nominal configuration settings, will do the following:
  - test for sufficient conditions to add a ballot
  - will randomly select one contest.cvr per all contests, merge in the CVR, and delete the branch in a meaningfully atomic manner

## 5) add_the_backlog.py
- runs on the VC VTP git server
- will add the backlog of unadded pushed ballots to the ledger

## 6) verify_ballot_receipt.py
- runs anywhere
- input: a ballot receipt (file)
- output: Pass/Fail if all the contest digests are legitimate
- output: if there is a failure, and indication of the failing rows and columns / digests

## 7) cast_n_ballots.py
- runs on a VTP scanner
- for testing only
- will cast N ballots according to the parameters provided (exact, probability, whatever)
- will call cast_a_ballot.py N times

The next set is a TBD list of tally functions

## 8) tally_contest.py
- runs anywhere
- will tally a specific contest by looking at the history of the configured/relevant contest.cvr files
- input: all the config.yaml files
- input: all the election repositories (should be obvious but might as well clearly state it)
- output: the json/yaml output of the tally of the contest.  Various details are printed per optional switches.

## 9) tally_all_contests.py
- runs anywhere
- will tally all the contests per supplied arguments by calling tally_contest.py with the appropriate switches
- input: all the config.yaml files
- input: all the election repositories (should be obvious but might as well clearly state it)
- output: the json/yaml output of the tally of all the contests.  Various details are printed per optional switches.

Some initial audit support utilities

## 10) tally_specific_contest_file.py
- run anywhere
- for VC VTP audit purposes - this is NOT necessarily a tally of a contest as that will depend on the config.yaml files
- will tally a specific contest by looking at the history of a specific contest contest.cvr file
- input: the history of a specific contest.cvr file
- output: the json/yaml summary and details, caveat switches, of all the contests entered via that specific contest.cvr file

## 11) verify_configs.py
- run anywhere
- will slurp all the config.yaml files and verify various aspects of each file as well as the aggregate data
- input: all the config.yaml files
- input: all the election repositories (should be obvious but might as well clearly state it)
- output: pass/fail assessment of the config files

## 11) audit_election.py
- run anywhere
- for VTP audit purposes
- will slurp all the config.yaml as well as the CVR's and run various validations to the accuracy of the election
- initial list of conditions to check for (TBD)
  - mis-cast contests
  - missing contests and other missing data
  - invalid commits via either invalid metadata or file content
  - un-enforced operational standards (commits with PGP keys, evidence of history re-writes)
