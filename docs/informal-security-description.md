# An Informal Description of the Security Model of VOTES

## 1) Terminology

For definitions and technical terms, please refer to [NIST Glossary](https://pages.nist.gov/ElectionGlossary/)

## 2) What does this page cover?

This page describes a high-level summary of the security model presented by VOTES.  For ease of understanding, the VOTES [Attack Surface](https://en.wikipedia.org/wiki/Attack_surface) is divided into five security domains:

- Data-at-Rest security
- Data-at-Remote-Update security
- Data-in-Remote-Motion security
- Data-in-Local-Motion security
- Data-at-Local-Update security

These domains are overlapping, which is not considered a bad thing as whitespace in a security model, the opposite of overlaps, is a bad thing.  For example, to update the VOTES repositories hosted by a service somewhere, both data-at-update and data-in-remote-motion security concerns and attack surfaces are involved.

## 3) What does this page not cover?

Lots.  This page is a selective slice of the VOTES workflows from a cryptographic point of view, covering the general high level security model and [Attack Surface](https://en.wikipedia.org/wiki/Attack_surface).  Other pages describe the various technologies, high / low level descriptions, User eXperiences, and workflows that comprise VOTES.

## 4) VOTES is not introducing a new cryptographic protocol

VOTES is not introducing a new cryptographic protocol, such as say homomorphic encryption as with election systems such as [ElectionGuard](https://www.electionguard.vote/), that needs to be designed, vetted, and built.  VOTES leverages already in-play and existing security protocols for all three security domains - data-at-rest, data-at-update, and data-in-movement.  VOTES does add at the VOTES application level, which is on top of third-party applications that are built on already vetted [PKI](https://en.wikipedia.org/wiki/Public_key_infrastructure) and [PGP](https://en.wikipedia.org/wiki/Pretty_Good_Privacy) security models, additional security features, such as [2FA](https://en.wikipedia.org/wiki/Multi-factor_authentication), as a way to increase tamper-resistance and prevent accidental corruption and adversarial attacks.

## 5) The VOTES Attack Surface - a Decomposition into Five Domains

### 5a) Data-at-Rest

VOTES leverages [Git](https://git-scm.com/) as the [Merkle Tree](https://en.wikipedia.org/wiki/Merkle_tree) engine in which to store both the VOTES software applications, blank ballot information, as well as the [cast vote records](https://pages.nist.gov/ElectionGlossary/#cast-vote-record).  VOTES does this by storing the individual precinct data in precinct *owned* repos that are configured as [git submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules) into the parent git repo that is effectively *running the election*.  All the repos Git are configured to only use [SHA-265 commit digests](https://github.com/git/git/blob/master/Documentation/technical/hash-function-transition.txt).  In addition the Git hosting service is configured to require all commits to have valid  [GPG](https://docs.github.com/en/github/authenticating-to-github/managing-commit-signature-verification/about-commit-signature-verification) keys.

At rest, the git repositories are protected from tampering both via the nature of the SHA-256 Merkle Tree as well as the git hosting service protecting the git repositories at rest.  Since the repositories are publicly available, each voter can have their own complete copy as well and independently secure their clone as well.  Note that VOTES repositories contain both the VOTES programs, such as those used to tally the votes for the specific associated election as well as the cast vote records for that election.  All VOTES programs are written in python as source code and include all testing and CI/CD pipeline infrastructure code as well such that every voter can inspect, test, and comment on all aspects of the VOTES programs.

### 5b) Data-at-Update

Data-at-Update refers to that part of the attack surface in play when someone is either legitimately trying to update a remote VOTES repo or when VOTES is being independently attacked.

#### Prior to ballots being scanned

Regarding the git hosting service and using GitHub as an example, though any sufficiently robust git hosting service can be used, the election is initially setup via a GitHub organization representing the actual real organization that is running the overall election.  The parent VOTES repo for the election is forked from the latest official release of the VOTES open source project.  The organization is set up with the industry/military best practices regarding security.  For purposes of this description, will assume this is for the 2024 US election and that the election is being run by .

The parent VOTES repo is configured for the next level of the Geopolitical Geographical Overlay (GGO) that comprise the first GGO overlay of the physical geographical geopolitical locations on the planet over which the election is being held.  The parent VOTES organizations works with official representatives of each of the GGO's to create and verify GitHub users with the proper security settings (GPG keys etc) and proper forks of the release VOTES repo configured as git submodules.

Again using the 2024 US election as an example, if there is no such parent organization running the election at a federal level, then each state acts as an independent parent organization.  It is possible that some states will decide to share a single parent, facilitating the overall election process, while other state will opt out while other state will not even be employing a VOTES solution.

Regardless, the root election owning organization establishes the GPG chain-of-trust with downstream repo owners.  From a [SDLC](https://en.wikipedia.org/wiki/Systems_development_life_cycle) point of view, prior to the start of the election proper when the first ballot is cast, the various GGO's follow standard Git/GitHub best software agile development methods to update all the GGO VOTES repos with the correct ballot races and questions.  There is a natural CI pipeline that is followed prior to [pull requests](https://en.wikipedia.org/wiki/Distributed_version_control) being merged into the root VOTES repo master branch.  Note that all submodules master branch updates need to adhere to this policy.

#### During Ballot Scanning and Cast Vote Record Creation

Once the election enters the phase of scanning cast ballots and creating vote records, in theory no more changes are allowing by the controlling organization to any aspect of the VOTES repo other than the cast vote records themselves.  If any change is made, at least every voter will see it.

During this phase, the live VOTES repos are not publicly available as they are being updated.  The security of the previous section still applies.  However, in addition, all pull requests have an additional non internet based 2FA between the root organization and individual on-the-ground election official(s) for each distributed local VOTES repo.  Nominally there is one local VOTES repo per voting center such that any single or set of voting centers can go offline and still process local ballots.  When the centers come back on line and push cast vote records, the 2FA is executed at that time.

After all the polls close, any un-pushed cast vote records are pushed and other ballots such as mail-in, absentee, etc., are also scanned and pushed.

#### Post Ballot Scanning and Cast Vote Record Creation

After all the polls close, the VOTES repos for the election can be made publicly available.  Voters can continually update their clones as the queues of un-scanned, un-pushed cast vote records are pushed.  Each voter and each election official can tally the votes on their devices as well as inspecting the voter id repos.  The voter id repos are separate repos that solely contain the voter names and addresses and no other data.  This allows all voters to search for local and non local fraudulent voter names or addresses.

Since the voter id registration process can be attacked, which is completely separate from VOTES itself, it is quite possible that legal cases will be filed to through out certain ballots or sets of ballots.  Technically this can be done by selecting the physically ballots to be revoked and revoking the specific SHA-256 commits for the associated cast vote records.

If fraudulent cast vote records are found, they can be revoked in a similar manner.

Note that since every cast vote records nominally has a voter behind it, a voter will know when their cast vote record is revoked.  This will allow a counter legal challenge to be brought if the voter so chooses.

### 5c) Data-in-Remote-Motion

This section primarily covers security of when there is data in motion from one spot on the planet / internet to another.

At the https layer, all election official connections will employ [mutual authentication](https://en.wikipedia.org/wiki/Mutual_authentication) leveraging a root certificate authority chain created and managed by the root level parent GGO running the election.  Note - the CI pipeline testing of this operational part of VOTES will include cert revocation - all end points in the operational footprint of a VOTES election must be able to adequately and properly handle cert revocation and new/renew cert allocation.

On top of this military/industrial grade https/ssl layer will reside the GitHub app level security model at the highest grade implementation.  For example, all commits will be GPG signed.

On top of this layer, when merging pull requests that contain cast vote records, a out-of-band non-internet based 2FA human interaction is required to bless a merge.  This to add yet more robustness to updating of cast vote records.

Regarding reading/cloning repositories from the VOTES Git service, there will be a mirror of the actual live repos to several different git services.  This will allow the voters at large as well as election officials who only need to read/clone the VOTES repos to access services built to handle the traffic as well as the adversarial assaults on large capacity servers.  The real VOTES upstream servers will be hardened in a manner consistent with limited read/write access.

### 5d) Data-in-Local-Motion

Data in local motion refers to the security models and attack surfaces in play within a specific LAN where either cast vote records are being created/processed or prior to the start of an election when the various GGO's are configuring VOTES and the blank ballots as well as testing VOTES in various test scenarios.

Prior to when the first ballots are scanned, the various VOTES repos are under going normal [SDLC](https://en.wikipedia.org/wiki/Systems_development_life_cycle) agile development methodologies.  As Git is a well understood [distributed version control](https://en.wikipedia.org/wiki/Distributed_version_control) system, standard agile development practices will apply.  Basically, within a LAN, each developer is interacting with the live remote repos - there is no special LAN specific cryptographic protocols in play beyond the well understood military/industrial best practices.

Once a LAN at a voting center starts scanning / processing cast vote records, the LAN needs to be protected against run-time adversarial attacks at disrupting active voters.  This is no different then other non-VOTES implementations.  Best practices should be used - wired connections if possible, etc.

Note that the local voting center can go offline at ballot scanning time without issues.  This is because each local VOTES repo is self contained regarding the creation and management of cast vote records.  In a worse case scenario, the cast ballots can be rescanned into VOTES from scratch in bulk at a later time.  In this scenario depending on the local election budget, the voter sheets can be redistributed to the voters by having voters revisit an election secure voting center and having VOTES print another voter sheet with the old digests mapped to the new digests.  In this workflow the voter DOES NOT reveal their private offset nor does the private offset change - VOTES will look up the old digests with a map to the new digests of the new cast vote records.  In this case the first compromised VOTES repos is never made public.

### 5e) Data-at-Local-Update

Data-at-Local-Update refers to the security and attack surfaces in play when at a local voting center ballots are being scanned into VOTES.  This is the time and place where new [GUIDs](https://en.wikipedia.org/wiki/Universally_unique_identifier) and SHA-256 Git digests are being generated.  The generation of both are completely local as the salt's for the GUIDs include the various private and public keys already shared between the local VOTES submodule repo and the root parent VOTES repo and git service.

At a high level, each ballot is separated into each race/question.  The voter's ballot will receive a different git commit for each race/question.  The main purpose of this is to minimize the revelation of perhaps nefarious patterns to the multiple choices on a ballot.  There is no way in VOTES to re-assemble the individual ballot questions into a single ballot with the sole exception being the private information returned to the voter - their specific row offset in their specific voter sheet.

Once the voter has personally and privately blessed the cast vote record or decided to pass on that verification step entirely, the physical ballot is printed with a GUID that is both random and based on a unique and local election private key as well as the pubic election key of the parent root VOTES repo.  The GUID is also added to the digital scan of the ballot by the ballot scanning device.  This simply associates the physical ballot with the actual digital scan, both of which are not made public.  This association aids audits and recounts by limiting the ability to alter either the physical or digital scans individually.

Next a per question GUID is generated and printed on the physical ballot and added to the JSON payload of the git commit for each question.  The git commits are generated with an altered date and time such that all dates and times are the same.  Each commit is in a different workspace and are not sequential in relationship.

The last approximately 200 (TBD - this number may be smaller or larger post more analysis) ballots are also still in their respective individual workspaces.  Thus there are 200 x the number of ballot questions workspace-only commits that have yet to be pushed to the locally based remote VOTES repo.

Next the voter's votes sheet is printed.  A random row is selected to be the voters specific ballot, and that row is filled with the voter's true git commits.  The other 99 rows are randomly selected from 200 un-pushed workspaces and printed to fill the sheet.  The sheet is printed and the voter's row is privately revealed on a screen to the voter.

Then a random set of per question commits across a random set of the un-pushed workspaces are pushed via a merge to the local repo, returning the number of un-pushed workspaces so-to-speak to 200.  In this manner as ballots are scanned and cast vote records are created, they are sequentially pushed the local remote randomly both in actual ballot order and by question order.

After all the polls close, the last remaining 200 un-pushed cast voter records are pushed again in a random order.

