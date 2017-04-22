# VOTES

A Verifiable Open Technology Election System

# 1) Overview of VOTES

VOTES is a distributed, open-source project aimed at creating public/private, transparent, secure, and accurate elections.  It is an [election](https://en.wikipedia.org/wiki/Election) and [voting](https://en.wikipedia.org/wiki/Voting) framework delivered as a [SaaS](https://en.wikipedia.org/wiki/Software_as_a_service) solution.

# 2) Basic Technical Overview - What is VOTES?

Technically VOTES is method to electronically record each paper ballot as a hashed-chain of ballots.  Specifically, each voter receives a [cryptographic hash](https://en.wikipedia.org/wiki/Cryptographic_hash_function) and associated barcode/[QR code](https://en.wikipedia.org/wiki/QR_code) for their ballot.  There is only one ballot repo per election.

In addition each precinct/voting center also has a voter-id repo that is local for that precinct only.  The voter-id repo contains the names and address of each voter and a special cryptographic key that requires two keys to decode.  One such key is owned by the election officials of the precinct and the other key is owned by the VOTES framework.  In the presence of both keys, a specific targeted voter id entry can be decoded to reveal the ballot digest.  Note that the keys are effectively use once keys, so new keys are required for each decoding.  In addition each decoding is recorded in the voter id repo.

On election day or whenever a voter casts her/his vote, the voter privately receives the ballot digest only.  Election officials may choose to privately receive the encrypted voter-id record of the ballot just cast as a means of recording in an air-gapped manner the voter-id encrypted digest.  Note that though both repos are public and hence distributed in an open source sense (once the polls close), the algorithms and cryptography being employed prevents the public or any third party from associating a voter id digest with a ballot digest.

When mail-in ballots are counted, either via UVBM, early, or absentee scenarios, election officials need to follow proper guidelines so to not inadvertantly provide an opportunity to develop a method to secure the purchase of ballots.  This is primarily accomblished by having two separate individuals submit mail-in ballots of any kind - one election official acts as the voter and only sees the ballot digest, and the other election official only potentially sees the encrypted voter-id digest if the precinct is indeed manually recording voted -id data.

When a person votes in person with a physical ballot, they can receive either a physical or electronic copy the ballot digest only.  Election official can choose how they wish to process ballots, with a few options being:

* the physical ballot can be stamped with the ballot digest and stored in an air-gapped secure manner
* the physical ballot can be destroyed leaving no air-gapped record
* the VOTES voter-id repo can be the sole record of the voter id encrypted ballot digest or the precinct can record the encrypted digest in their own air-gapped vote-id records, in which case it is important to __NOT__ record or make available any connection between the encrypted and non encrypted ballot digest.

This allows local election officials to choose between fully electronic, partially electronic, or fully physical ballot record keeping.  As the election officials may need to recount votes or provide evidence of voter id, election officials can choose how they wish to comply with such requirements and concerns.  However, regardless of their choice VOTES will manage both the ballot and voter-id repos for the public at large.

The cryptographic hash of both repos are chained - the hashing function includes the previous hash for the previous ballot for that precinct (for that ballot database repository).  The precinct's VOTES servers/SaaS randomize the ballot sequence such that _physical_ sequential ballots at any specific voting location are not sequential in the hashing function, minimizing the probability that the previous hash matches the previous voter in any given precinct.  This is true for both the voter-id and ballot repos.

Individual ballots are immediately and publicly accessable once cast (post the randomizing blocking function) and remain so on the VOTES servers until the power is turned off.  Prior to when the polls close ballot digest lookup is only available via the VOTES SaaS implementation via a human interaction (bots are rejected).  Since the election database/repository is freely copied by anyone, private copies may exist for quite some time even after the election is closed and potentially later mothballed.  Any individual can lookup their specific ballot via their hash at any time.

Once the polls close, the complete hashed chain of ballots becomes available for any person to download.  This allows any individual or agency, government or private, to perform the counting function of any race in the election.  In particular this ability is available with any copy of the election database/repository.

Regarding ballot counting, the algorithms, including how the ballots are defined, parsed, counted, and validated/invalidated are included in the hashing function as they are also contained in the same database/repository as the ballots themselves.  Any individual can both inspect their ballot as well as its compliance/status at any time once (block) cast by querying the VOTES SaaS implementation.  Once the polls close, since only then is the entire repo accessible to all, any individual can then also count the votes for any question/race on their ballot or for any race/question in the election.  All that is required to count the votes at any __Geopolitical Geographical Overlay (GGO)__ level of the election is a copy iof the election database/repositories.

Each actual election is a different instance of the VOTES SaaS solution and runs on a different set of VOTES servers, nominally in either a public or private cloud.

Regarding GGO overlays per election, an _election_ is created when an identified owner (say for example the federal US government) creates one.  Creating an election implies creating two things (a highly scientific term):

* A root election database/repository.  A root election database/repository aggregates intermediate database/repositories that are created at lower GGO overlays.
* A [Certificate Authority](https://en.wikipedia.org/wiki/Certificate_authority) which in turn allows [Intermediate Certificate Authorities](https://en.wikipedia.org/wiki/Intermediate_certificate_authority) to be created at lower GGO overlays.

Per the reality of GGO overlays (for example state, county, town, precincts - see [NIST standards](http://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.1500-100.pdf)), the overlays may or may not overlap or share physical boundaries.  Regardless each state or county or town or voting center (precinct) can participate in the election by providing races/questions at their respective GGO level.  Each GGO overlay also can optionally create their separate ballot repository, controlled/managed by them.  Thus the actual election database is distributed in nature, locally managed, but aggregated in a shared manner.

The aggregation does not change the voter's original hash and no repository is available in its entirety until after all polls close, even though voters can individually validate their specific ballot at any time.

Regarding ballot validation, there is a natural ballot entry validation that occurs when the physical ballot is scanned or the electronic ballot is entered - if the ballot does not meet the validation requirements for each of the GGO overlays the ballot is rejected and no hash is generated.  (Note - different vote counting methodologies will have different validation algorithms even via a single ballot.)

Post entry into VOTES, the various authorities at the GGO overlays can invalidate a specific ballot by issuing a negation ballot.  A negation ballot voids a previous ballot and becomes part of the chain of votes at the time of the invalidation.  Negation ballots require full disclosure of the who/what/when/why such that all observers (anyone with access to a copy of the election repository) can inspect the invalidation, including the voter.  Negation ballots themselves can be negated, such as when the negation of the ballot is overruled.  However, the entire timeline of ballots, the potential negation thereof, and the potential reversal of the negation are all part of the permanent cryptographic hash chain of the election.

Technical note - the overall GGO security model is not limited to root and intermediate CA's - there are additional out-of-band security controls in play to minimize and mitigate [attack surfaces](https://en.wikipedia.org/wiki/Attack_surface).

# 3) Basic Business Overview - How?

Changing any existing election process is difficult.  However, the post 2016 US national election timeframe is probably the best timeframe in the US so far to undertake such a task.  There are many websites and organizations devoted to election reform.  Two arbitrary examples: [fairvote.org](http://www.fairvote.org/) is focusing on Ranked Choice Voting, and [electology.org](https://electology.org/) provides support for communities to select better election methodologies.  There are also private companies such as [BigPulse](https://www.bigpulse.com/), [SimplyVoting](https://www.simplyvoting.com/), [ClearBallot](http://www.clearballot.com/), as well as [DieBold/ESS](http://essvote.com/).  Post [HAVA](https://en.wikipedia.org/wiki/Help_America_Vote_Act), [NIST](https://en.wikipedia.org/wiki/National_Institute_of_Standards_and_Technology) is also been involved with [voting standards](https://www.nist.gov/itl/voting).  There is also academic centers of interest such as at the [University of Iowa](http://homepage.divms.uiowa.edu/~jones/voting/).

An important goal of VOTES is to be aligned with election reform so to leverage all of the above grass-roots, private, and public efforts.

High-level VOTES differentiators are:

 * Grassroots alignment with election reform
 * Each election including the ballots, counting algorithms, GGO layers etc is open sourced and distributed
 * Alignment with NIST so to leverage technical traction and maximize interplay with other vendors, agencies, and the general public at large
 * Flexible support for different voting/counting methodologies, allowing the efficient and secure interplay of differing adoption rates of different voting methodologies within a specific election
 * Best-in-class security frameworks and implementations

The current delivery model is SaaS.  As the VOTES project is still pre-garage stage, the current focus is to gain momentum and peer review from the open source community at large.  Then to build a prototype based on existing open source frameworks and toolsets.  Then as a function of feedback and available resources build a solution that will be usable in the 2020 election.

# 4) High-level Technical Requirements

(Per election)

## 4.1) High Level Requirements / In-scope

1. Validation at any time of a ballot post submittal by the voter
2. Validation at any time of the vote count by any person for any ballot race/question at any GGO scope (aggregation point) of the ballot
3. Support for any combination of GGO overlays for any specific precinct/voting location (for example, support for voting in the town of Cambridge MA - see NIST reference)
4. Support for different [counting schemes](https://electology.org/library#104) (plurality, approval, IRV) potentially simultaneously across any race/question for any given ballot
5. Support for UVBM, mail-in, absentee, and electronic balloting
6. Ballot validation (rejection of non-compliant ballots) at entry point as a function of the counting scheme and election configuration
7. Best possible adherence to existing [NIST standards](http://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.1500-100.pdf) ballot payloads UML definitions
8. Distribution of control/ownership of a GGO portion of a ballot to that GGO entity as a configuration of the election
9. Tracked ballot disqualification as a configuration of the election (if an election allows the future disqualification of ballots, then the disqualification thereof is fully tracked and transparent with regards to who/what/where/where etc.)
10. An [air-gapped](https://en.wikipedia.org/wiki/Air_gap_(networking)) and physical ballot tied to the electronic copy but separate thereof
11. Distributed - no single point of failure or ballot aggregation point
12. Open sourced - both the ballots and the counting/aggregation/validation algorithms are freely (no charge) and easily accessible

## 4.2) High Level Non Requirements / Out-of-scope

1. VOTES does *NOT* provide voter identification services
2. Though VOTES supports early voting, it does not directly manage the paper based workflows of handling the early ballots - each precinct still needs to handle the early ballots and the entering of early ballots into the VOTES system.

# 5) Timeline-based Overview of Services

## 5.1) Pre Election Day Summary

Prior to election day, VOTES supports the configuration of a specific election at all the GGO levels (country, state, county, town, other) in parallel.  Each level of the election uses best-in-class authorization, authentication, and encryption to support configuration of that part of the ballot(s) to be provided any each precinct/voting center.  As election day approaches VOTES tracks all the changes (versions) to all the ballot questions as well as providing the ability for each precinct to test the election day workflows.

Once a precinct finalizes a ballot, that ballot becomes available for early voting.  Early ballots can be entered into VOTES at any time, including prior, during, or after election day as an election configuration option.

## 5.2) Day of Election Summary

VOTES directly supports the election day by scanning the paper ballot and privately providing the necessary digests to the voter and election officials.  VOTES handles the aggregation of all the ballots via the ballot repo from all the precincts and the aggregation thereof as defined by the GGO's but will not reveal any such aggregated data until after all polls close.  VOTES also handles the individual precinct voter id repos.

## 5.3) Post Election-Day Summary

Once the polls close, the VOTES SaaS implementation immediately makes available the entire cryptographically hashed aggregated election results contained in the ballot repo.  The SaaS implementation also makes available the various voter id repos.  VOTES actually does not provide official counting of the ballot races/questions - that is determined of the owner(s) of the election as well as any observer of the election.  Since the counting and validation algorithms as well as the code implementations thereof for each ballot race/question is also contained in the same database as the ballots themselves and abides by the same open source framework provided by VOTES (see NIST documents for more ballot payload details), every voter and can access the same election data and count the votes.
