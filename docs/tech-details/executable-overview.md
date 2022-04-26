# Basic [VC](https://pages.nist.gov/ElectionGlossary/#vote-center) python executables

Some initial/basic python executables geared to supporting a VTP demo

## 1) create_blank_ballot.py
- runs anywhere
- will parse all the config.yaml files in the election git tree and generate a blank ballot.
- initial version will just render a CVR compatible blank ballot.json file suitable for automated voting/casting of ballots for tests.  A later version can produce a ballot.pdf (from the sphinx/rst files).
- input: all config.yaml files
- input: all ballot.rst files
- input: an address
- output: a blank ballot.json file
- output: a blank ballot.pdf file

## 2) generate_all_blank__ballots.py
- runs anywhere
- will generate all the blank ballots acros the election nominally per VTP configuration placing them in the town's blank ballot directory
- input: all config.yaml files
- input: all ballot.rst files
- output: blank ballot.json files
- output: blank ballot.pdf files

## 3) cast_ballot.py
- runs on a VTP scanner
- for testing only
- note - the caller can randomly or otherwise select the contest selections
- input:  a blank ballot.json file
- output: a valid ballot.cvr file containing 0 or more 'voter' selected contests

## 4) accept_ballot.py
- runs on a VTP scanner
- will run the necessary git commands to commit all contests to contest unique and specific branches and push them to the VC VTP remote
- input: a ballot.cvr file
- output: N contest specific git branches pushed to the VC VTP remote
- output: the voter's ballot receipt (a file during testing)
- output: the voter's ballot receipt row (either STDOUT or a file or as part of the voter receipt during testing)

## 5) merge_contests.py
- runs on the VC VTP git server
- per nominal configuration settings, will do the following:
  - test for sufficient conditions to add a ballot
  - will randomly select one contest.cvr per all contests, merge in the CVR, and delete the branch in a meaningfully atomic manner

## 6) verify_receipt.py
- runs anywhere
- input: a ballot receipt (file)
- output: Pass/Fail if all the contest digests are legitimate
- output: if there is a failure, and indication of the failing rows and columns / digests

## 9) tally_contests.py
- runs anywhere
- will tally all or a specific contest by looking at the history of the configured/relevant contest.cvr files
- input: all the config.yaml files
- input: all the election repositories (should be obvious but might as well clearly state it)
- output: the json/yaml output of the tally of the contest.  Various details are printed per optional switches.

# Audit Executables

These are supporting auditing of the VTP and VTP data.  This is different than paper ballot audits or digital scan audits.

## 10) verify_configs.py
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

# Tests Executables

The above audit utilities are not DevSecOps CI/CD tests.  As part of the DevSecOps pipeline all the executables will have unit tests, feature tests, system tests, etc.  For example, there will be CI/CD tests that include validating the various tally algorithms, such as RCV, plurality, etc.

There will be system tests which include mock elections that contains both fixed and random ballot-content balloting.

There will also be configuration consistency testing which basically validates that the correct blank ballots are generated for specific addresses.

There will also be operational non-compliance/error insertion testing which includes attack/failure scenarios to validate that VTP correctly reports the error at insertion time and handles it as designed.
