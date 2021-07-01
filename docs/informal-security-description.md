# An Informal Description of the Security Model of VOTES

## 1) Terminology

For definitions and technical terms, please refer to the [NIST Glossary](https://pages.nist.gov/ElectionGlossary/)

## 2) What does this page cover?

This page describes a high-level summary of the security model, [cryptographic protocols](https://en.wikipedia.org/wiki/Cryptographic_protocol), and [attack surfaces](https://en.wikipedia.org/wiki/Attack_surface) presented by VOTES.  For ease of understanding, this information is divided five domains:

- Data-at-Rest domain
- Data-at-Remote-Update domain
- Data-in-Remote-Motion domain
- Data-in-Local-Motion domain
- Data-at-Local-Update domain

These domains are overlapping, which is not considered a bad thing since failing to consider a security aspect is worse then considering it multiple times from different points of view.  For example, to update the VOTES repositories hosted by a VOTES service somewhere, both data-at-remote-update and data-in-remote-motion security concerns and attack surfaces need to be considered.

## 3) What does this page not cover?

Lots.  This page is a selective slice of the VOTES workflows from a security and cryptographic point of view, covering the general high level security models, cryptographic protocols, and attack surfaces.  Other pages describe the various technologies, workflow descriptions, and User eXperiences that comprise VOTES.

## 4) VOTES is not introducing a new cryptographic protocol

VOTES is not introducing a new cryptographic protocol, such as for example when  [ElectionGuard](https://www.electionguard.vote/) introduces homomorphic encryption.  New cryptographic protocols need to designed, vetted, and built.  VOTES leverages already in-play and existing cryptographic protocols for all five security domains.  On the other hand VOTES does add at the VOTES application level, which is on top of third-party applications that are built on already vetted cryptographic protocols such as [PKI](https://en.wikipedia.org/wiki/Public_key_infrastructure) and [PGP](https://en.wikipedia.org/wiki/Pretty_Good_Privacy), additional security features such as [2FA](https://en.wikipedia.org/wiki/Multi-factor_authentication) as a way to increase tamper-resistance and to add greater resistance to accidental corruption and adversarial attacks.

## 5) The VOTES Attack Surface - a Decomposition into Five Domains

### 5a) Data-at-Rest

VOTES leverages [Git](https://git-scm.com/) as the [Merkle Tree](https://en.wikipedia.org/wiki/Merkle_tree) engine in which to store both the VOTES software applications, blank ballot information, as well as the [cast vote records](https://pages.nist.gov/ElectionGlossary/#cast-vote-record).  VOTES does this by storing the individual precinct data in precinct *owned* repos that are configured as [git submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules) via the parent git repo that is effectively *running the election*.  In all repos Git is configured to only use [SHA-265 commit digests](https://github.com/git/git/blob/master/Documentation/technical/hash-function-transition.txt).  In addition the Git hosting service is configured to require all commits to have valid  [GPG](https://docs.github.com/en/github/authenticating-to-github/managing-commit-signature-verification/about-commit-signature-verification) signatures, etc.

At rest, the git repositories are protected from tampering both via the nature of the SHA-256 Merkle Tree as well as the git hosting service protecting the git repositories at rest.  Since the repositories are publicly available, each voter can have their own complete copy as well and independently secure their clone as desired.  Note that VOTES repositories contain both the VOTES programs, such as those used to tally the votes for the specific associated election as well as the cast vote records for that election.  All VOTES programs are written in python as source code and include all testing and CI/CD pipeline infrastructure code as well such that every voter can inspect, test, and comment on all aspects of the VOTES programs.

### 5b) Data-at-Update

Data-at-Update refers to that part of the attack surface in play when someone is either legitimately trying to update a remote VOTES repo or when VOTES is being independently attacked.

#### Prior to ballots being scanned

Regarding the git hosting service and using GitHub as an example (any sufficiently robust git hosting service can be used), the election is initially setup via a GitHub organization representing the actual real organization that is running the overall election.  The parent VOTES repo for the election is forked from the latest official release of the VOTES open source project.  The organization is set up with the industry/military best practices regarding security.  For purposes of this description, will assume this is for the 2024 US election and that the election is being run by some thin federal agency.

The parent VOTES repo is configured for the next level of the Geopolitical Geographical Overlay (GGO) that comprise the first GGO overlay of the physical geographical geopolitical locations on the territory over which the election is being held.  The parent VOTES organizations works with official representatives of each of the GGO's to create and verify election officials as GitHub users with the proper security settings (GPG keys etc) and proper forks of the release VOTES repos.

Again using the 2024 US election as an example, if there is no such parent organization running the election at a federal level, then each state acts as an independent parent organization.  It is possible that some states will decide to share a single parent, facilitating the overall election process, while other state will opt out while other state will not even be employing a VOTES solution.

Regardless, the root election owning organization establishes the chain-of-trust with downstream repo owners.  From a [SDLC](https://en.wikipedia.org/wiki/Systems_development_life_cycle) point of view, prior to the start of ballot scanning, the various GGO's follow standard Git/GitHub best software agile development methods to update all the GGO VOTES repos with the correct ballot races and questions as well as the GIS information.  The GIS information allows VOTES to print address correct ballots.

There is a natural CI pipeline that is followed prior to [pull requests](https://en.wikipedia.org/wiki/Distributed_version_control) being merged into the root VOTES repo master branch, helping to validate changes even at this stage of the election.  Note that all submodules master branch updates should also adhere to such a policy.

#### During Ballot Scanning and Cast Vote Record Creation

Once the election enters the phase of scanning ballots and creating cast vote records, in theory no additional non cast vote records changes are allowing by the controlling organization.  This would nominally be enforced at pull request time if not earlier in the [SDLC](https://en.wikipedia.org/wiki/Systems_development_life_cycle) process.

Regardless if any such changes are made, every change, included the authenticated author, will be seen by every voter when the VOTES repos are downloaded.

During this phase of cast vote record creation, the live VOTES repos are not publicly available.  Note that operationally the **real** VOTES repos are highly armored with only limited and official access.  These repos are technically never publicly available.  What is publicly available are direct downstream mirrors of these.  Once scanning of the ballots begins, the mirrors are **NOT** updated until all the polls close.

However, the security of the previous section still applies.  In addition, all pull requests have an additional non internet based 2FA between the root organization and individual on-the-ground election official(s) for each distributed local VOTES repo.  Nominally there is one local VOTES repo per voting center such that any single or set of voting centers can go offline and still process local ballots.  When the centers come back on line and push cast vote records, the 2FA is executed at that time.

After all the polls close, any un-pushed cast vote records are continued to be pushed and other ballots such as mail-in, absentee, etc., are also continued to be scanned and pushed.

Independent of the continued scanning of yet-to-be scanned ballots, once all the polls close and the election is considered *closed* for any additional unqueued ballots, the mirrors of the real VOTES repos can be updated so that the electorate can see how the election is unfolding in real time.

Note that in this manner, every member of the electorate is on equal footing with election officials as to the tallying of the votes.


#### Post Ballot Scanning and Cast Vote Record Creation

After all the polls close, the VOTES repos for the election can be made publicly available.  Voters can continually update their clones as the queues of un-scanned, un-pushed cast vote records are pushed.  Each voter and each election official can tally the votes on their devices as well as inspecting the voter id repos.  The voter id repos are separate repos that solely contain the voter names and addresses and no other data.  This allows all voters to search for local and non local fraudulent voter names or addresses.

Note - it is not covered here, but when subsequent elections are held via a VOTES technology solution, depending on the state configuration of VOTES it is possible for VOTES to track a specific voter across addresses, greatly reducing the ability of an individual to vote in multiple times via different addresses.  Similar to risk limiting audits of the ballot counting/scanning process, risk limiting audits can be executed against voters with the same name but with different addresses within a single election but also across multiple elections.

Since the voter id registration process itself can be either erroneous or attacked, which is completely separate from VOTES itself, it is quite possible that legal cases will be filed to throw out certain ballots or sets of ballots, perhaps at specific voting center.  Technically this can be done by selecting the physically ballots to be revoked and revoking the specific SHA-256 commits for the associated cast vote records.

If fraudulent cast vote records are found, they can be revoked in a similar manner.

Note that since every cast vote records nominally has a voter behind it, a voter will know when their cast vote record is revoked.  This will allow a counter legal challenge to be brought if the voter so chooses.

### 5c) Data-in-Remote-Motion

This section primarily covers security of when there is data in motion from one spot on the planet / internet to another, for example when a local voting center with its local VOTES repo goes to push there repo to the election root VOTES server.

At the https layer, all election official connections will employ [mutual authentication](https://en.wikipedia.org/wiki/Mutual_authentication) ssl leveraging a root certificate authority chain created and managed by the root level parent GGO running the election.  Note - the CI pipeline testing of this operational part of VOTES will include cert revocation - all end points in the operational footprint of a VOTES election must be able to adequately and properly handle cert revocation and new/renew cert allocation.  The CI test plan includes this type of adversarial attack.

On top of this military/industrial grade https/ssl layer will reside the GitHub app level security model at the highest grade configuration and implementation.  For example, all commits will be GPG signed and during the cast vote record creation phase, all pull requests require out-of-band 2FA.

Regarding reading/cloning repositories from the VOTES Git service, there will be a mirror of the actual live repos to several different git service end-points.  This will allow the voters at large as well as election officials who only need to read/clone the VOTES repos to access services built to handle the traffic (perhaps many millions of connections per second) as well as the adversarial assaults on large capacity servers without effecting the uploading of commits to the real root servers.  The real VOTES upstream servers will be hardened in a manner consistent with limited read/write access and hidden to extent possible from the internet at large.

### 5d) Data-in-Local-Motion

Data in local motion refers to the security models and attack surfaces in play within a specific LAN where either cast vote records are being created/processed or prior to the start of an election when the various GGO's are configuring VOTES and the blank ballots as well as testing VOTES in various test scenarios.

Prior to when the first ballots are scanned, the various VOTES repos are undergoing normal [SDLC](https://en.wikipedia.org/wiki/Systems_development_life_cycle) agile development methodologies.  As Git is a well understood [distributed version control](https://en.wikipedia.org/wiki/Distributed_version_control) system, standard Git based agile development practices will apply.  Basically, within a LAN, each developer is interacting with the live remote repos - there is no special LAN specific cryptographic protocols in play beyond the well understood military/industrial best practices.

Once a LAN at a voting center starts scanning / processing cast vote records, the LAN needs to be protected against run-time adversarial attacks at disrupting active voters.  This is no different then other non-VOTES implementations.  Best practices should be used - wired connections if possible, WiFi encryption, etc.

Note that the local voting center can go offline at ballot scanning time without issues.  This is because each local VOTES repo is self contained regarding the creation and management of cast vote records.  In a worse case scenario, the cast ballots can be rescanned into VOTES from scratch in bulk at a later time.  In this scenario depending on the local election budget, the voter sheets can be redistributed to the voters by having voters revisit an election secure voting center and having VOTES print another voter sheet with the old digests mapped to the new digests.  In this workflow the voter DOES NOT reveal their private offset nor does the private offset change - VOTES will look up the old digests with a map to the new digests of the new cast vote records.  In this case the first compromised VOTES repos is never made public.

### 5e) Data-at-Local-Update

Data-at-Local-Update refers to the security and attack surfaces in play when at a local voting center ballots are being scanned into VOTES.  This is the time and place where new [GUIDs](https://en.wikipedia.org/wiki/Universally_unique_identifier) and SHA-256 Git digests are being generated.  The generation of both are completely local as the salt's for the GUIDs include the various private and public keys already shared between the local VOTES submodule repo and the root parent VOTES repo and git service.

At a high level, each ballot is separated into each race/question.  The voter's ballot will receive a different git commit for each race/question.  The main purpose of this is to minimize the revelation of perhaps nefarious patterns to the multiple races and choices on a ballot.  There is no way in VOTES to re-assemble the individual ballot questions into a single ballot with the sole exception being the private information returned to the voter - their specific row offset in their specific voter sheet.

Once the voter has personally and privately blessed the cast vote record or decided to pass on that verification step entirely, the physical ballot is printed with a GUID that is both random and based on a unique local election repo private key as well as a root private key passed from the root repo to the local via a private key exchange.  An adversary will not be able to generate a valid GUID against the public election keys without the private key of both the local repo and the passed in private key.

This ballot GUID is also added to the digital scan of the ballot by the ballot scanning device.  This simply associates the physical ballot with the actual digital scan, both of which are never made public.  This association aids audits and recounts by limiting the ability to alter either the physical or digital scans individually.  Election officials control the physical ballot while the contractual agreement between the election officials and the ballot scanning hardware supplies determines the ownership of the actual ballot scans.

Next a per question GUID is generated and printed on the physical ballot and added to the JSON payload of the git commit for each question.  The git commits are generated with an altered/zero'ed out date and time such that all dates and times are the same.  Each commit is in a different workspace and are not sequential in relationship.  The JSON payload does not contain the ballot GUID but only the specific race GUID.

The last approximately 200 (TBD - this number may be smaller or larger post more analysis) ballots are also still in their respective individual workspaces having not yet been pushed locally.  Thus there are 200 x the number of ballot questions workspace-only commits that have yet to be pushed to the locally based remote VOTES repo.

Next, the voter's VOTES sheet is printed.  A random row is selected to be the voters specific ballot, and that row is filled with the voter's true git commits.  The other 99 rows are randomly selected from 200 un-pushed workspaces and printed to fill the sheet.  Each ballot question is randomly selected so that there is no association of ballot questions back to a single specific ballot.  Finally the sheet is printed and the voter's row is privately revealed on a screen to the voter.  The passing back of the voter's row on the sheet is done in private many limiting the ability of the voter to prove to a third party that they voted in a specific manner.

Then a random set of per question commits across a random set of the un-pushed workspaces are pushed via a merge to the local repo, returning the number of un-pushed workspaces so-to-speak to 200.  In this manner as ballots are scanned and cast vote records are created, they are sequentially pushed the local remote randomly both in actual ballot order and in question order.

After all the polls close, the last remaining 200 un-pushed cast voter records are pushed again in a random order.

