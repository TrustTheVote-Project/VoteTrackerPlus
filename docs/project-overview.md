# VOTES

A Verifiable Open Technology Election System

# 1) Overview of VOTES

VOTES is a distributed, open-source project aimed at creating public/private, transparent and trustworthy, secure, and accurate elections.  It is an [election](https://en.wikipedia.org/wiki/Election) and [voting](https://en.wikipedia.org/wiki/Voting) framework delivered as a [SaaS](https://en.wikipedia.org/wiki/Software_as_a_service) solution.

# 2) Basic Technical Overview - What is VOTES?

Technically VOTES is method to electronically and anonymously record each paper ballot as a hashed-chain of ballots.  The primary compelling reason behind VOTES is the open-source, open-data, nature of the GitHub or the equivalent git technology.  By using a currently well understood and popular enough full ledger distributed storage system (such as git), VOTES inherently provides the transparency needed for public trust for both (blank) ballot creation, ballot scanning, and electronic based software tallying.

By requiring an independent physical ballot and physical paper trail, fully air-gapped from the electronic copy, VOTES minimizes the risk that an undetectable or un-repairable ballot or election compromise occurs.

VOTES also supports a significantly customizable voter [UX](https://en.wikipedia.org/wiki/User_experience) experience depending on what the state or local election official desire to support or have the monetary resource to support.

While the ballots and tally algorithms are fully open-source with full ledger provenance, the actual implementation of an election is based on significant and currently best-available security and encryption technologies, including but not limited to full [mutual authenticated](https://en.wikipedia.org/wiki/Mutual_authentication) ssl, multi-node and independent [public key certificate](https://en.wikipedia.org/wiki/Public_key_certificate) based communication with concurrent [MFA](https://en.wikipedia.org/wiki/Multi-factor_authentication) during all workflows during the election process, including pre, day-of, and post election day.  All crucial digests are created via double encryption via two independent certificate authorities, one being the local precinct or state authority responsible for the physical ballots, and the other being the VOTES system/framework.  As such it takes a compromise of two independent certificate authorities as well as access to the original encrypted data to compromise the digests.

And even if the digests are compromised, such a compromise only attacks voter anonymity and does compromise the actual ballot contents nor the tally of the ballots.  Being a fully distributed full ledger of an election, every citizen can maintain their own full ledger copy of the election.  Compromising an election would require compromising a clear weighted majority of the distributed copies of the election.

# 3) Basic High Level Implementation

VOTES is implemented via three kinds of git repos:  a public VOTES ballot repo(s), a private VOTES voter-id repo(s), and a public VOTES voter-id repo(s).

The VOTES ballot repo holds the full ledger history of the ballot, ballot tally algorithm, voter UX workflows, and GGO (Geopolitical Geographical Overlay) configurations.  GGO's are how various groups of addresses participate or not regarding a ballot question or race.  Examples of a GGO are: state, city, borough, district, town, precinct, etc.  Each election can have different GGO's depending on many factors. On election day ballots are scanned into this repo.

The VOTES ballot repo(s) start as public.  As the GGO's work to finalize their ballots and tally algorithms and other pre-election data and configuration, the public has access to this repo.  However, once the election itself commences, updates to the VOTES ballot repo are no longer availabe.  It is fully private until after all-polls-close.  At that point the ballot repo is made public again.  As precincts privately upload their data to the VOTES SaaS implementation, those updates are made available live to the general public.

Note that with VOTES precincts are __NOT__ uploading ballot counts with percentage of ballot counted - they are uploading the actual raw VOTES scanned ballots.  The tallies are done by the GGO certificate owners as well as the public at large by downloading (cloning) the ballot repo(s) and performing the tallies.  (The tally algorithms are contained in the repo.)  With VOTES every citizen can perform the tally.

The second VOTES repo is a fully private voter-id repo.  This repo contains only two pieces of voter id data that a state may require - the voter's name and address.  The VOTES voter-id repo only maintains a copy of these two pieces of information regardless of how much data a state or precinct may actually require to positively and accurately identify a voter.  The repo is private to VOTES SaaS implementation and the precinct/state that is managing the election.

The third VOTES repo is a pruned copy of the private, stripped of all voter and ballot digests and information, VOTES voter-id repo.  It is made public along with the VOTES ballot repo once all-polls-close.

The VOTES framework maintains three important encrypted digests that are calculated live during the voting process.

The first digest identifies each unique ballot as printed and made available to a voter.  This digest is __ONLY__ tracking the blank ballot - it does not contain any information regarding how the voter may or may not have filled in the ballot.

The second digest is a double encrypted (via two separate certificate authority private keys) digest associating the VOTES voter-id with the physical ballot.  This digest is stored in the VOTES voter-id repo.  Note that neither the physical ballot nor this repo is publicly available.

The third digest is a double encrypted (via two separate certificate authority private keys) digest associating the VOTES voter-id with the electronic copy of the ballot.  This digest is stored in a private VOTES SaaS based voter-id repos.  The precinct/state VOTES voter-id repo and the SaaS VOTES voter-id repos are similar but contain separate digests.  They are private to each certificate authority.

Note that post all-polls-close, only the VOTES public ballot and voter-id repos are publicly available and that the digests are only in the privately held VOTES voter-id repos.  Every citizen can download (clone) the ballot and public version of the voter-id repo, but only the precinct/state election officials can download/clone the VOTES private voter-id repos.

This allows the public to inspect their personal as well as their precinct's limited voter id data sans digests.

Via the two independent private VOTES voter-id repos, election officials and the VOTES SaaS system can independently compare, but only by doubly decrypting via two independently private keys, one held by the precinct and one held by the VOTES SaaS implementation, the voter-id and the associaited physical or electronic ballot.  (Note - decoding a phiysical ballot is independent and a different decoding then decoding an electronic ballot.)  Importantly, each such decoding is recorded in the repos themselves such that the public and the voter have insight to when a voter-id has been decoded.

# 4) What voter UX workflows does VOTES support?

The VOTES UX workflows for the voter is customizable via configuration settings in the VOTES ballot repo.  This same repo also contains the blank ballots as a function of the various GGO's in play for a given address.

VOTES support single and double checking in-person voting, absentee voting, early voting, UVBM voting, etc.  It is configurable how a state wished to handle the details of counting/scanning ballots for each of the above workflows.

# 5) What tally algorithms does VOTES support?

VOTES supports any tally algorithm per ballot question/race desired by the election officials.  Since the tally algorithm itself is part of the full ledge history of the VOTES ballot repo, there is full transparency to the counting of the votes and as to what tally algorithm has been chosen (plurality, instant run-off, [etc](https://electology.org/library#104)).

Note that due to the full history/ledger nature of git, all the pertinent details of the election and how to count it is included in the VOTES ballot repo.

# 6) How are the actual ballots created in VOTES?

For any given election, there will be an set of GGO's that must or wish to participate in the election.  Each such GGO gets a git repo to compose their ballot questions.  VOTES takes care of the proper integration of the GGOs such that a simple and maximally comprehensible ballot is created for the voter.  Each GGO is at some point delineated by a physical boundary, and it is that boundary that drives the creation of the correct ballot for a given voter given their specific address.

# 7) Basic Business Overview - How?

Changing any existing election process is difficult.  However, the post 2016 US national election timeframe is probably the best timeframe in the US so far to undertake such a task.  There are many websites and organizations devoted to election reform.  Two arbitrary examples: [fairvote.org](http://www.fairvote.org/) is focusing on Ranked Choice Voting, and [electology.org](https://electology.org/) provides support for communities to select better election methodologies.  There are also private companies such as [BigPulse](https://www.bigpulse.com/), [SimplyVoting](https://www.simplyvoting.com/), [ClearBallot](http://www.clearballot.com/), as well as [DieBold/ESS](http://essvote.com/).  Post [HAVA](https://en.wikipedia.org/wiki/Help_America_Vote_Act), [NIST](https://en.wikipedia.org/wiki/National_Institute_of_Standards_and_Technology) is also been involved with [voting standards](https://www.nist.gov/itl/voting).  There is also academic centers of interest such as at the [University of Iowa](http://homepage.divms.uiowa.edu/~jones/voting/).

An important goal of VOTES is to be aligned with election reform so to leverage all of the above grass-roots, private, and public efforts.

High-level VOTES differentiators are:

 * Grassroots alignment with election reform
 * Each election including the ballots, counting algorithms, GGO layers etc is open sourced and distributed
 * Alignment with NIST so to leverage technical traction and maximize interplay with other vendors, agencies, and the general public at large
 * Flexible support for different voting/counting methodologies, allowing the efficient and secure interplay of differing adoption rates of different voting methodologies within a specific election
 * Best-in-class security frameworks and implementations

The current delivery model is SaaS.  As the VOTES project is still pre-garage stage, the current focus is to gain momentum and peer review from the open source community at large.  Then to build a prototype based on existing open source frameworks and toolsets.  Then as a function of feedback and available resources build a solution that will be usable in the 2020 election.

# 8) High-level Technical Requirements

(Per election)

## 8.1) High Level Requirements / In-scope

1. Open sourced - both the ballots and the counting/aggregation/validation algorithms are freely (no charge) and easily accessible.  This is key - this maximizes transparency and trust in an election.  No proprietary software, no hidden software, no hidden counting machines etc.
2. Validation by the voter of her/his specific ballot
3. Validation at any time of the vote count by any person for any ballot race/question at any GGO scope (aggregation point) of the ballot
4. Support for any combination of GGO overlays for any specific precinct/voting location (for example, support for voting in the town of Cambridge MA - see NIST reference)
5. Support for different [counting schemes](https://electology.org/library#104) (plurality, approval, IRV) potentially simultaneously across any race/question for any given ballot
6. Support for UVBM, mail-in, absentee, and electronic balloting
7. Ballot validation (rejection of non-compliant ballots) at entry point as a function of the counting scheme and election configuration
8. Best possible adherence to existing [NIST standards](http://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.1500-100.pdf) ballot payloads UML definitions
9. Distribution of control/ownership of a GGO portion of a ballot to that GGO entity as a configuration of the election
10. Tracked ballot disqualification as a configuration of the election (if an election allows the future disqualification of ballots, then the disqualification thereof is fully tracked and transparent with regards to who/what/where/where etc.)
11. An [air-gapped](https://en.wikipedia.org/wiki/Air_gap_(networking)) and physical ballot tied to the electronic copy but separate thereof
12. Distributed - no single point of failure or ballot aggregation point

## 8.2) High Level Non Requirements / Out-of-scope

1. VOTES does *NOT* provide voter identification services
2. Though VOTES supports early voting, it does not directly manage the paper based workflows of handling the early ballots - each precinct still needs to handle the early ballots and the entering of early ballots into the VOTES system.

# 9) Timeline-based Overview of Services

## 9.1) Pre Election Day Summary

Prior to election day, VOTES supports the configuration of a specific election at all the GGO levels (country, state, county, town, other) in parallel.  Each level of the election uses best-in-class authorization, authentication, and encryption to support configuration of that part of the ballot(s) to be provided any each precinct/voting center.  As election day approaches VOTES tracks all the changes (versions) to all the ballot questions as well as providing the ability for each precinct to test the election day workflows.

Once a precinct finalizes a ballot, that ballot becomes available for early voting.  Early ballots can be entered into VOTES at any time, including prior, during, or after election day as an election configuration option.

This version of the VOTES ballot repo is publicly available.  Once the actual election starts (the first ballots are scanned), no new version of the VOTES ballot repo is made available until after all polls close.

## 9.2) Day of Election Summary

VOTES directly supports the election day by scanning the paper ballot and tracking voters.  VOTES handles the aggregation of all the ballots via the ballot repo from all the precincts and the aggregation thereof as defined by the GGO's but will not reveal any such aggregated data until after all polls close.  VOTES also handles the publicly available, stripped of any private voter or ballot data, voter id repos.

## 9.3) Post Election-Day Summary

Once the polls close, the VOTES SaaS implementation immediately makes available the complete post election-day  ballot repo.  Note that as precincts make their repos available to VOTES, the VOTES SaaS public version is updated.  As the precincts update their repos in VOTES, VOTES likewise updates the public available repo(s).

The SaaS implementation also makes available the stripped version of the precinct voter id repos.

Importantly, VOTES does __NOT__ provide any actual count or tally of the ballot races/questions - that is determined of the GGO certificate authority and/or the public at large.  Though the GGO will announce the tally, every citizen is capable of executing their own tally and questioning the GGO results.  All citizens can perform the tally since the tally algorithm and the data, as well as the entire provenance of both, is contained in the VOTES ballot repo.
