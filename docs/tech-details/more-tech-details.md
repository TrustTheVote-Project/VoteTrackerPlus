# 1) Design Notes/Thoughts Regarding the Ballot Repo (unreviewed)

The VoteTracker+ product road map is divided into a short/mid term project, 1.0, and a long term project called 2.0.  1.0 is focused on ballot tracking and supplying an anonymous ballot receipt to the voter.  VoteTracker+ 2.0 allows election officials to optionally integrate greater election security and transparency checks.  It is all the same product - it is just that some of the 2.0 features will not be immediately available.

See [project-overview.md](../project-overview.md) for a general project overview.

See security-overview.md for a general overview of the security aspects of running an election via a VoteTracker+ SaaS implementation.

This document give a general technology overview of the open-source components of the project.  For reference there is a local copy in this directory of [NIST.SP.1500-100.pdf](../NIST.SP.1500-100.pdf) which contains a terminology section on page 120 as well as the precinct and ward map for Cambridge Massachusetts on pages 14 and 15.

# 2) Git Based Prototype Overview

As a prototype, the idea is use a set of git/github repos to host the election data for an election.  Once a prototype is up and running and we know more of what we do not know, either git or the GitHub backend implementations can be switched out for some other implementation.

Regarding using bitcoin as a backend - the current thought is that a bitcoin is to tied to an economic model so to be reasonably applicable to a voting situation.  The use cases are too different even though both scenarios share a similar desire to authenticate a ledger of data.  Having the ballots and the algorithms being completely stored unencrypted in a publicly accessible manner, albeit a git repo with many git submodules, achieves the verifiability goals and allows for a greater degree of trustworthiness from the voters.  It is important that the voters trust the election system in use.

Regarding Ethereum, it is still unclear whether an Ethereum solution will enable the creation of a market to sell and buy votes (by allowing individual voters to offer their ballot contents to a third party as proof of sale).

As an example and a talking point, the following overview is based on a hypothetical 2020 US presidential election.

## 2.1) Certificate Authorities

The git/GitHub prototype idea is to allocate a set of git/GitHub repos for the 2020 US presidential election.  The election commission of each state opting in to the VoteTracker+ SaaS solution would appoint/select the certificate authority for that state.  The VTP SaaS entity itself would also create a certificate authority independent of the states.  It is a TBD whether that certificate authorities would be owned by the private contractor responsible for the 2020 election or if it owned by the [EAC](https://www.eac.gov/) or some other branch of the federal government.  Given the open-source nature of VTP it could be either and be different for different elections.  Regardless the VTP framework would be shared between all the participating states while the certificate authorities would not be.

Each such state entity would in turn create intermediate cert authorities for each child GGO (Geopolitical Geographical Overlay - NIST calls this a [geopolitical unit](https://pages.nist.gov/ElectionGlossary/#geopolitical-unit)) down from the state level that will be managing a git repo that will be contrinuting to the election.  For example, if there will be county, borough, town, district or other GGO based ballot questions or races, those entities will need their own repo so to create the ballot question and races.

In addition, each state will need to create a intermediate authority for each voting center that wishes to collect and process/scan ballots.  Voting centers can be grouped into sets by sharing certificates but in theory each voting center will want to have in independent certificate.

Each GGO (the federal government, a state, a county, a town, a whatever) will need to clone a pre-configured 2020 VoteTracker+ repo.  The pre-configure-ing is mainly to create an ease-of-use UX for the GGO so to allow all the various repos to be aggregated.

For this 2020 git/GitHub prototype each state will be a submodule under the parent VoteTracker+ git repo.  In addition each GGO will also be a git submodule.  All the submodules are arranged in a directory tree structure that mirrors the certificate authority chain which in fact is exactly the GGO chain as well.

The federal, state, town etc git repos all are clones the same pre-configured virgin/empty VoteTracker+ repo.  An empty VTP repo does not yet contain any election race/question details.  However it does contain the (latest) release of the VTP framework as well as the configuration data that make it easy to create such a US federal based election.  A state only election or an election for a different country with different fundamental overlays/entities would have a different pre-configuration.  The VTP clone specifies things such has how the different (arbitrary) GGO are aggregated within a single election.

## 3.1) What actually is a ballot?

### 3.1.1) Option A - a ballot is an empty commit

In the git prototype a ballot is simply an empty commit with a git hook validated/managed description.  The voter's choices on the ballot are scanned off the paper ballot and yaml/json/xml encoded into the commit message.  The only actual files contained in a repo are the VoteTracker+ framework files and the GGO's ballot sections, ballot/election configurations, etc.  As noted this includes the tally algorithm and all election related information.  Post election day when the repos are made publicly available, anyone who downloads the repos (the root VTP repo and all the state and GGO submodule repos) will be able to count the votes for all races.  They will also be able to inspect all the ballots as well as their own specific ballot.

### 3.1.2) Option B - a ballot is just a text file in ballots subtree of the repo

In this option the ballot contents are stored as separate yaml/json/xml text files.  Similar to Option A the individual repos also contain the various other files such as the ballot questions/races, tally algorithms, etc. 

To tally a state ballot question, one needs to clone the state and its submodule repos and perform the tally on their computer or phone, etc.  Side note - they will also be able to tally the votes using different tally algorithms to the extent that it makes sense (since for example a plurality ballot is not tally-able with an approval tally algorithm).

To tally a national ballot question or race that is _above_ the state level, such as a presidential race, the root VoteTracker+ repo will contain an software implementation of the electoral college.  However, this would just be a simulation, an estimate, as the real electoral college is independent of the VTP implementation.

## 3.2) Basic Git Repo Prototype

As a prototype implementation the VoteTracker+ framework is implemented as a set of git repos connected via submodules.  The parent repo is associated with VTP SaaS framework itself and can be owned and operated by either a private or public entity per election.

Note that any number of states can opt into the VTP framework.  Currently the only point where state exchange ballot data is at the electoral college level, which for VTP is just a simulation (as VTP does __NOT__ replace the electoral college).

If only certain GGO's within a state participate in the VTP framework, that too is ok as per NIST and other standards the VTP ballot data is easily, quickly, and trivially translatable/migratable to other electronic formats.  Or more directly the tallies of the questions/races being handled by VTP can be passed into those other election systems.

All VTP repos have the same layout regardless of the GGO (national, state, county, town, etc).  What is different is only the data that is contained in the folder structure within and where/how the submodule tree is stitched together.

Each repo contains the information authored by each GGO.  However, per the git subtree hierarchy children and parent repos as well as configuration data information is shared across repo.

## 3.3) Folder Layout Per Git Repo

So the root most GGO is that git repo _owned/authored_ by the VoteTracker+ root authority of the cert chain for the 2020 US election (_the election_).  In this case the agency deemed responsible for actually running the 2020 national US election would be the VTP root authority.  The folder structure for VTP repos is:

#### ./config

Contains configuration data for this GGO in yaml form (unless it really needs to be xml or something else).  Yaml is more human readable and more (git) merge-able.  If so necessary it can be translated into xml when needed.

#### ./bin

Contains executables directly associated with the VTP repos are located in this folder.  Includes the executables necessary to tally the various contests and leverages configuration data.  For example the tally scheme for a GGO or a contest within the GGO can be configured in ./config while the actual algorithms and tally code is implemented in ./bin.

For a US presidential election, due to the electorial college the states tally function will mirror/implement the states electorial tally function, which is basically a summation.  However different states do it differently, and in the case of the electoral college the electors actually must vote, so the tally function non binding and perfunctory only.

This folder does not contain phone or desktop apps for either the voter or election officials.  Those are downloaded separately.

#### ./ballot

Contains the ballot information for this GGO if there is ballot information.  For the national GGO for the 2018 election which does not contain a presidential contest, this would probably be empty except perhaps for a welcome message for the voter.

Each GGO contributes to the ballot that is presented to the voter at the precinct/Voting Center (VC).

#### ./CVRs

Votes are _collected_ in the CVRs (Cast Vote Records) folder.  The default configuration is that only GGO repos that have a precinct/VC will be collecting votes.  However it is configurable for a precinct/VC to commit votes to a parent GGO repo.  So, the root GGO repo in most cases would not directly contain any votes since it would not have a precinct/VC associated with it.

### 3.3.1) Child GGO's - Git Submodules

A child GGO is one where the VoteTracker+ Certificate Authority (CA) for this GGO creates an intermediate CA and allocates/associates sub GGO information with the ./config folder.  The git submodule tree looks like the following:

#### ./ggos/\<sub GGO class name>/\<instances name>

The \<sub GGO class name> is an arbitrary I18n name given to the specific intermediate CA's assigned by this CA.  For the US election this would be the 50 states plus any territory or other geographical geopolitical location.  (If voting is taking place electronically via the internet or other network, other or additional location coordinates will apply.)  This configuration info is also located in the ./config folder.

The following are examples relative from the current GGO:

#### A US national election root level example

The US national GGO will define 50 git submodules under the ggos subfolder.

./ggos/states/Alabama, Alaska, Arizona, ...

#### A US national election at the state level

Each state entity (specifically each sub GGO who has been delegated as an intermediate certificate authority) can independently select its sub GGO class name for their state.  As an example Alabama may use the I18n string _town_ in its VTP repo as above.

./ggos/towns/Abbeville, Adamsville, Addison, ...

### 3.3.2) Multiple / Parallel GGOs

It is possible to have multiple and different classes of sub GGOs. For a state with both towns, counties, boroughs, congressional districts, school districts etc that can overlap in effectively arbitrary ways.  In the VoteTracker+ framework this is implemented as multiple/sibling \<sub GGO class names>:

#### ./ggos/counties/Alameda, Alpine, Amador, ...
#### ./ggos/towns/Adelanto, Agoura Hills, Alameda, ...

The above may be how California decides to handle its counties and towns.

The sibling and multiple inheritance of the GGO's is flexible and configurable.  That is, it it possible for a state to have some towns in counties and some town not in any county.  And some towns may share school boards in the case of regional school systems.

Regardless of the number of different sub GGO class names, the __config.yaml__ file will determine how the sub GGO's are handled.  In addition, though a state, county, or town repo can be cloned in isolation, doing so will not result in a valid VoteTracker+ clone.  A valid VTP clone of the election will include the repo hierarchy from the root repo, including all sibling GGO's in the hierarchy that take part in any of the sub GGOs.  Again this is configured in the config.yaml file.  In this manner a California precinct/VC repo will also contain the town and county submodule/subtree repo trees and information.  One of several reasons for this is so that the correct blank ballots can be generated and marked by voters.

In the California case, each town will in fact get a copy of those counties to which it has an overlay with.  A specific town may reside within multiple counties and a county will usually contain multiple towns.  It is configurable via the __config.yaml__ file whether in this case California defines how the two GGO's overlay (which towns are in which county and vice versa) or if the counties or towns decide that.  Technical note - California actually owns the authority to decide but can pass the authority to either the county or town to define that information.

In a similar fashion each GGO also has an __address_map.yaml__ file which lists the addresses valid for the GGO.  Thus both the __config.yaml__ and __address_map.yaml__ files are [RBAC](https://en.wikipedia.org/wiki/Role-based_access_control) controlled by the owning GGO.  Note the the __address_map.yaml__ supports references to child GGOs.  For example, the state of California can simply state that any legel address in the town of Alameda (as controlled by the town) will receive/contribute to the California GGO contests.

Regardless of delegation of the definition, each town and county clone only the relevant upstream and sibling repos.  At some level in this hierarchical tree, a GGO will want to actually collect votes on election day.  Actual votes are collected in the CVRs folder but require the repo to be configured as such, again via data in the config and address_map files.

In addition to the CVRs folder there is also a blank-ballots folder which contains all the possible valid blank ballots for the CVRs that will be processed at that location.  The number of different blank ballots is a function of the number of different intersections of all the GGOs for that location.

Four implementation notes:
1) <ggo-GUID> is just a uniquely serialized string of GGOs contained in the specific blank ballot.
2) There is a blank-ballots folder for each CVR folder.
3) Even though the blank ballots are generated uniquely for each VTP election config, they are still committed to the repository so to minimize data in motion post a 'git clone' operation.
4) The blank ballots are generated in each language (UTF-8) that is desired by the election officials.

As an example, the following section assumes the town of Cambridge Massachusetts.  When the city of Cambridge clones the VTP repo for the 2018 election, assuming that all the parent GGO are indeed participating in a VTP framework, the directory tree will look someting like:

```
US-2024-National-Election/.git
                          .gitmodules
                          LICENSE
                          README.md
                          VTP-core/
                          address_map.yaml
                          config.yaml
                          GGOs/Massachusetts/.git
                                             config.yaml
                                             address_map.yaml
                                             GGOs/Cambridge/.git
                                                            config.yaml
                                                            address_map.yaml
                                                            ballot.rst
                                                            blank-ballots/json/<ggo-GUID>.json
                                                                          <language>/<ggo-GUID>.pdf
                                                            CVRs/
                                                            GGOs/5th Congressional District/.git
                                                                                            config.yaml
                                                                                            address_map.yaml
                                                                                            ballot.rst
                                                                                            blank-ballots/json/<ggo-GUID>.json
                                                                                                          <language>/<ggo-GUID>.pdf
                                                                                            CVRs/
                                                                 7th Congressional District/.git
                                                                                            config.yaml
                                                                                            address_map.yaml
                                                                                            ballot.rst
                                                                                            blank-ballots/json/<ggo-GUID>.json
                                                                                                          <language>/<ggo-GUID>.pdf
                                                                                            CVRs/
                                                                 ward 1-1/{config,ballot}
                                                                 ward 1-2/{config,ballot}
                                                                 ...
                                                                 ward 11-2/{config,ballot}
                                                                 ward 11-3/{config,ballot}
```
Each Congressional District and Ward could either each have a git repo where there respective ballot contests can be entered or they can be share git repos.  When the voter gets a ballot from the VC (either an absentee, early, or on election day ballot), the VoteTracker+ framework can generate the correct ballot for the address.

Implementation note: it is possible for precincts/VC to share the same repo or leverage a parent repo to cast votes into - it is configurable into which repo a precinct/VC submits votes to.

GGOs that are not configured to scan actual ballots are not a separate git repo - they simply are a folder with the necessary config and ballot files necessary to specify the information necessary to add contests to the ballot for the governing GGO.

# 4) The Voter ID Repo - VoteTracker+ 2.0

With VoteTracker+ 2.0, in addition to the VTP ballot repositories there are also similar but separate voter-id repositories.  These repositories contain the voter's name and address as entered by election officials.  The voter-id repository is organized in a similar manner to VTP ballot repos via the git submodule hierarchy described above.  Like the ballot repo this repo is only publicly available once all the polls close.  However, it is available to election officials who decide to incorporate it in their election workflows.  When leveraged, it provides a transparent way of tracking voter-id across the entire electorate without stove-piping or dark space.

[Note - to be clear there is no data stored anywhere in VTP that can be used to associate any data in the voter-id repositories with any the data in the VTP ballot repositories.  Both are publicly available after all-the-polls close and are full ledger repositories.]

# 5) How Ballots Are Entered - an Overview

A paper or electronic ballot, generated by the VoteTracker+ framework, is custom generated for the address of the identified voter.  It is not required that the VTP framework (the SaaS implementation) prints the voter-id paperwork.  A precinct can alternatively use their own voter-id paperwork.  But regardless the VTP voter-id repository is populated with the registered voters casting ballots.

Regardless, the voter fills out the ballot and submits it to a VTP compatible ballot scanning device operated by an election official.  The ballot is verified not to contain any overvotes or undervotes.  An overvote will block the submittal of a ballot as being invalid.  Each precinct/state can configure VTP as to how undervotes are handled.  They can simply be ignored or be configured to allow an election official to ask/allow the voter to fill out a new ballot.

Once validated by the VTP framework, the ballot is submitted to the VTP system and the various repos are updated accordingly.

There are several workflows checks that are not configurable and are part of the nature of VTP.  For example once a voter (a specific voter-id) has submitted a ballot, they no longer can submit any other ballot, be it absentee, early, late, whatever.  However, as described how a precinct handles undervotes is configurable.

## 5.1) In Person Voting

See the UX documentation describing in person voting.  This also includes in-person early voting.

## 5.2) Absentee Voting

See the UX documentation describe [absentee voting](UX/absentee-voting.md)

## 5.3) UVBM - Universal Vote By Mail

See the UX documentation describe [UVBM voting](UX/UVBM-voting.md)

# 6) What Is Accessible When and General UX

Note - there are different classes/sets of VoteTracker+ supported workflows/UX experiences.  One set is voter centric - how the voter experiences the act of casting a ballot.  This includes in-person voting at a voting center, both for early voting or election day voting.  The voter UX also includes non in-person voter workflows such as absentee and UVBM.

Separate from voter UX is the GGO pre-election day workflows.  These include how the various GGO's construct their ballots and configure VTP to handle customizable aspects of the voter experience.  Section 6 pertains to the GGO centric UX.

## 6.1) Pre Blank Ballot Freeze Date

Each GGO (Geopolitical Geographical Overlay) starts filling in their respective information and data per the Ballot Freeze Date (BFD) workflows.  The various entities/overlay owners enter the races/questions they wish to be contained on their respective ballot sections.  These can be ballot races, ballot questions, etc.

Each GGO can also select the [tally algorithm](https://electology.org/library#104) per contest.

Note that each GGO/overlay can work independently of all the others or in conjunction with other GGOs.  Each entity can only modify their repo - their own specific GGO information.  Note - various git hooks and other aspects of the VTP framework enforce the non-alteration of VTP framework repo local files which defines how the GGO interact in a hierarchical tally sense.   Similar to software development across a distributed project spanning distributed teams, the different entities pull and push their work to the configured VTP SaaS github servers.  There is distributed, tracked, authenticated sharing of the specific election repos during the pre-election day workflows.

Note that during this process each entity can both test their election independently of other parent/sibling/child repos as well as test a full election.  The VTP repo/SaaS framework comes with a test harness and test data for testing.

With this overview of VTP in mind, once again note that VTP (the framework and hence the repos) will be compliant as possible with [NIST](http://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.1500-100.pdf) standards - this part of the value add of a VTP framework.

Regarding the voter-id repo, though it is highly recommended that election official pre-fill out the voter-id repos with the registered voters, actually doing so is optional.  Voters can be added to the voter-id repo directly at the voting center if so configured by the election officials.

## 6.2) Pre Election Day, Post Ballot Freeze Data

Once all the GGO's complete their portions of the blank ballot, the blank ballot is said to be done and is made available to all voters.  Due to the inherent design nature of the GGO's, every address in a precinct can obtain their address correct ballot via either the publicly available VTP repos or via their election officials - who obtain it via the public ballot repo as well.

As the precincts/state support it, early voting, absentee voting, and UVBM workflows can commence.  Each precinct/state follow their own workflows regarding when the ballots are actually cast and scanned.  Note that the ballot repo is __not__ publicly updated once ballots are allowed to be entered into VoteTracker+.

## 6.3) Election Day

Voters visit precinct/voting centers and cast votes in-person.  See the voter IX documentation regarding the various kinds of in-person voting experiences/workflows.

## 6.4) When the Last Precinct Closes

When the last precinct closes and all the UVBM, early ballots, and absentee ballots are accepted and no further un-cast ballots are acceptable, the ballot and voter-id repos are made publicly available.

Note that some precincts may still be scanning ballots after all the polls close.  This could be by choice or due to computer glitch, power failure, etc.  Regardless as precincts update their repos, in a manner similar to native distributed software development, they post their latest versions of their repos when they are ready.

At this point the general public is free to execute and inspect the tallies as precincts post their results.

## 6.5) Election Validation - E2EV

Once all the polls close, the ballot and voter-id repos are made fully public, this to provide transparency and allow direct inspection of the election, ballot, and the public copy of the voter-id data.  All elections regardless of their auditability, actually need to be audited.  Thus for N days (configurable per election) past all-polls-closed, the election is in an _under audit_ state.  Risk-limiting audits are performed including E2EV (End To End Validation) where selected precinct's physical ballots are compared with the electronic copies in VTP.  Note that the each physical ballot contains a blank-ballot unique digest - this can be compared to the blank-ballot digests stored in VTP for additional inspection.

In addition to content based E2EV (described above), count based E2EV, where the physical ballots are simply counted and compared against the ballot counts in VTP, is also randomly performed.

In addition, voter-id alignment audits are performed.  This is where the precinct's voter registration rolls are compared to the VTP voter-id.  This is a E2EV from the starting point of the state's voter-id through to the VTP public copy (which is derived from the VTP private copy).

While the election official and independent 3rd-party entities are carrying out the internal auditing process, the public is encouraged to look for signs of voter-id or ballot tampering on the public side.  This includes voter's checking their individual electronic copy as well as their physical ballot.

## 6.6) Close-of-Election

After N days post all-polls-close, both the public at large and election officials should have a good sense of the accurateness of the election.  If the auditing process needs to be continued perhaps because of a close race and the degree of error are concerning, it can be.

If the VoteTracker+ copy is found to be unfixable due to extensive fraudulent/illicit ballots or tampering, either the ballots can be entered from scratch again in a separate VTP SaaS instance, or the ballots are physically counted.  Note - this can also be done on a precinct by precinct basis in the case a precinct localized compromise.

As such, until the election is declared officially closed, the final tally of any contest may indeed change as all citizens and officials looks for irregularities.  It is nominally up to the election officials of the root GGO's (the states) to declare the official closure of an election within their GGO.  At that point, neither the ballot or voter-id repos can be changed.

Once the election is officially closed, there is a N day cooling off period so to handle any additional potential or real issues.  After the N day cooling off period, for security the private keys for the certificates are destroyed to insure the anonymity of the voters.

# 7) Post Election Analysis

Once the repos are publicly available, even after the election is officially closed, the public is free to analyse the repos.  For example, the tally algorithms can be changed to determine if a different algorithm would have changed the results of a race or contest.  Since the repos are public and free via an EULA that restricts certain anti-constitutional anti-democratic uses such as trying to sell or selling votes, citizens can clone the repo and, for example, change the tally algorithms and such.

However, the VoteTracker+ EULA prohibits the use of VTP data for monetary or military means.  There are also export restrictions such that VTP data cannot be exported outside the country of origin.

## 7.1) Exposing Gerrymandering

The legality and morality of [gerrymandering](https://en.wikipedia.org/wiki/Gerrymandering) is an important democratic question to be asked and answered by the electorate.  But the legal/moral question is a different question as to whether or not gerrymandering is happening and if so to what degree.  All citizens should be able to observe the effects of gerrymandering on the votes in their community.  The open source nature of VoteTracker+ allows for the inclusion of [Markov chain Monte Carlo](https://en.wikipedia.org/wiki/Markov_chain_Monte_Carlo) as a way of nonpartisan evaluation of the presence of gerrymandering so that every citizen can see the effects of district maps per GGO per election.
