# 1) Design Notes/Thoughts Regarding the Ballot Repo (unreviewed)

__As an example, the following notes are assuming a 2020 US national election.__

See [project-overview.md](https://github.com/PacemTerra/votes/docs/project-overview.md) for a general project overview.

See security-overview.md for a general overview of the security aspects of running an election via a VOTES SaaS implementation.

This document give a general technology overview of the open-source components of the project.  For reference there is a local copy in this directory of [NIST.SP.1500-100.pdf](https://github.com/PacemTerra/votes/docs/NIST.SP.1500-100.pdf) which contains a terminology section on page 120 as well as the precinct and ward map for Cambridge Massachusetts on pages 14 and 15.

# 2) Git Based Prototype Overview

As a prototype, the idea is use a set of git/github repos to host the election data for an election.  Once a prototype is up and running and we know more of what we do not know, either git or the GitHub backend implementations can be switched out for some other implementation.

Regarding using bitcoin as a backend - the current thought is that a bitcoin is to tied to an economic model so to be reasonably applicable to a voting situation.  The use cases are too different even though both scenarios share a similar desire to authenticate a ledger of data.  Having the ballots and the algorithms being completely stored unencrypted in a publicly accessible manner, albeit a git repo with many git submodules, achieves the verifiability goals and allows for a greater degree of trustworthiness from the voters.  It is important that the voters trust the election system in use.

Regarding Ethereum, it is still unclear whether an Ethereum solution will enable the creation of a market to sell and buy votes (by allowing individual voters to offer their ballot contents to a third party as proof of sale).

As an example and a talking point, the following overview is based on a hypothetical 2020 US presidential election.

## 2.1) Certificate Authorities

The git/GitHub prototype idea is to allocate a set of git/GitHub repos for the 2020 US presidential election.  The election commission of each state opting in to the VOTES SaaS solution would appoint/select the certificate authority for that state.  The VOTES SaaS entity itself would also create a certificate authority independent of the states.  It is a TBD whether that certificate authorities would be owned by the private contractor responsible for the 2020 election or if it owned by the [EAC](https://www.eac.gov/) or some other branch of the federal government.  Given the open-source nature of VOTES it could be either and be different for different elections.  Regardless the VOTES framework would be shared between all the participating states while the certificate authorities would not be.

Each such state entity would in turn create intermediate cert authorities for each child GGO (Geopolitical Geographical Overlay) down from the state level that will be managing a git repo that will be contrinuting to the election.  For example, if there will be county, borough, town, district or other GGO based ballot questions or races, those entities will need their own repo so to create the ballot question and races.

In addition, each state will need to create a intermediate authority for each voting center that wishes to collect and process/scan ballots.  Voting centers can be grouped into sets by sharing certificates but in theory each voting center will want to have in independent certificate.

Each GGO (the federal government, a state, a county, a town, a whatever) will need to clone a pre-configured 2020 VOTES repo.  The pre-configure-ing is mainly to create an ease-of-use UX for the GGO so to allow all the various repos to be aggregated.

For this 2020 git/GitHub prototype each state will be a submodule under the parent VOTES git repo.  In addition each GGO will also be a git submodule.  All the submodules are arranged in a directory tree structure that mirrors the certificate authority chain which in fact is exactly the GGO chain as well.

The federal, state, town etc git repos all are clones the same pre-configured virgin/empty VOTES repo.  An empty VOTES repo does not yet contain any election race/question details.  However it does contain the (latest) release of the VOTES framework as well as the configuration data that make it easy to create such a US federal based election.  A state only election or an election for a different country with different fundamental overlays/entities would have a different pre-configuration.  The VOTES clone specifies things such has how the different (arbitrary) GGO are aggregated within a single election.

## 3.1) What actually is a ballot?

### 3.1.1) Option A - a ballot is an empty commit

In the git prototype a ballot is simply an empty commit with a git hook validated/managed description.  The voter's choices on the ballot are scanned off the paper ballot and yaml/json/xml encoded into the commit message.  The only actual files contained in a repo are the VOTES framework files and the GGO's ballot sections, ballot/election configurations, etc.  As noted this includes the tally algorithm and all election related information.  Post election day when the repos are made publicly available, anyone who downloads the repos (the root VOTES repo and all the state and GGO submodule repos) will be able to count the votes for all races.  They will also be able to inspect all the ballots as well as their own specific ballot.

### 3.1.2) Option B - a ballot is just a text file in ballots subtree of the repo

In this option the ballot contents are stored as separate yaml/json/xml text files.  Similar to Option A the individual repos also contain the various other files such as the ballot questions/races, tally algorithms, etc. 

To tally a state ballot question, one needs to clone the state and its submodule repos and perform the tally on their computer or phone, etc.  Side note - they will also be able to tally the votes using different tally algorithms to the extent that it makes sense (since for example a plurality ballot is not tally-able with an approval tally algorithm).

To tally a national ballot question or race that is _above_ the state level, such as a presidential race, the root VOTES repo will contain an software implementation of the electoral college.  However, this would just be a simulation, an estimate, as the real electoral college is independent of the VOTES implementation.

## 3.2) Basic Git Repo Prototype

As a prototype implementation the VOTES framework is implemented as a set of git repos connected via submodules.  The parent repo is associated with VOTES SaaS framework itself and can be owned and operated by either a private or public entity per election.

Note that any number of states can opt into the VOTES framework.  Currently the only point where state exchange ballot data is at the electoral college level, which for VOTES is just a simulation (as VOTES does __NOT__ replace the electoral college).

If only certain GGO's within a state participate in the VOTES framework, that too is ok as per NIST and other standards the VOTES ballot data is easily, quickly, and trivially translatable/migratable to other electronic formats.  Or more directly the tallies of the questions/races being handled by VOTES can be passed into those other election systems.

All VOTES repos have the same layout regardless of the GGO (national, state, county, town, etc).  What is different is only the data that is contained in the folder structure within and where/how the submodule tree is stitched together.

Each repo contains the information authored by each GGO.  However, per the git subtree hierarchy children and parent repos as well as configuration data information is shared across repo.

## 3.3) Folder Layout Per Git Repo

So the root most GGO is that git repo _owned/authored_ by the VOTES root authority of the cert chain for the 2020 US election (_the election_).  In this case the agency deemed responsible for actually running the 2020 national US election would be the VOTES root authority.  The folder structure for VOTES repos is:

#### ./info

Contains configuration data for this GGO in yaml form (unless it really needs to be xml or something else).  Yaml is more human readable and more (git) merge-able.  If so necessary it can be translated into xml when needed.

#### ./bin

Contains executables directly associated with the VOTES repos are located in this folder.  Includes the executables necessary to tally the various contests and leverages configuration data.  For example the tally scheme for a GGO or a contest within the GGO can be configured in ./info while the actual algorithms and tally code is implemented in ./bin.

For a US presidential election, due to the electorial college the states tally function will mirror/implement the states electorial tally function, which is basically a summation.  However different states do it differently, and in the case of the electoral college the electors actually must vote, so the tally function non binding and perfunctory only.

This folder does not contain phone or desktop apps for either the voter or election officials.  Those are downloaded separately.

#### ./ballot

Contains the ballot information for this GGO if there is ballot information.  For the national GGO for the 2018 election which does not contain a presidential contest, this would probably be empty except perhaps for a welcome message for the voter.

Each GGO contributes to the ballot that is presented to the voter at the precinct/Voting Center (VC).

#### ./votes

Votes are _collected_ in the votes folder.  The default configuration is that only GGO repos that have a precinct/VC will be collecting votes.  However it is configurable for a precinct/VC to commit votes to a parent GGO repo.  So, the root GGO repo in most cases would not directly contain any votes since it would not have a precinct/VC associated with it.

### 3.3.1) Child GGO's - Git Submodules

A child GGO is one where the VOTES Certificate Authority (CA) for this GGO creates an intermediate CA and allocates/associates sub GGO information with the ./info folder.  The git submodule tree looks like the following:

#### ./ggos/\<sub GGO class name>/\<instances name>

The \<sub GGO class name> is an arbitrary I18n name given to the specific intermediate CA's assigned by this CA.  For the US election this would be the 50 states plus any territory or other geographical geopolitical location.  (If voting is taking place electronically via the internet or other network, other or additional location coordinates will apply.)  This configuration info is also located in the ./info folder.

The following are examples.

#### ./ggos/state/Alabama, Alaska, Arizona, ...

The US national GGO will define 50 git submodules under the ggos subfolder.

#### ./ggos/town/Abbeville, Adamsville, Addison, ...

Each state entity (specifically each sub GGO who has been delegated as an intermediate certificate authority) can independently select its sub GGO class name for their state.  As an example Alabama may use the I18n string _town_ in its VOTES repo as above.

### 3.3.2) Multiple / Parallel GGOs

It is possible to have multiple and different classes of sub GGOs. For a state with both towns, counties, boroughs, congressional districts, school districts etc that can overlap in effectively arbitrary ways.  In the VOTES framework this is implemented as multiple/sibling \<sub GGO class names>:

#### ./ggos/county/Alameda, Alpine, Amador, ...
#### ./ggos/town/Adelanto, Agoura Hills, Alameda, ...

The above may be how California decides to handle its counties and towns.

Regardless of the number of different sub GGO class names, the __info__ section will determine how the sub GGO's are handled.  In addition, though a state, county, or town repo can be cloned in isolation, doing so will not result in a valid VOTES clone.  A valid VOTES clone of the election will include the repo hierarchy from the root repo, including all sibling GGO's in the hierarchy.  In this manner a California precinct/VC repo will also contain the town and county submodule/subtree repo trees and information.

In the California case, each town will in fact get a copy of those counties to which it has an overlay with.  A specific town may reside within multiple counties and a county will usually contain multiple towns.  It is configurable via the __info__ folder whether in this case California defines how the two GGO's overlay (which towns are in which county and vice versa) or if the counties or towns decide that.  Technical note - California actually owns the authority to decide but can pass the authority to either the county or town to define that information.

Regardless of delegation of the definition, each town and county clone only the relevant upstream and sibling repos.  At some level in this hierarchical tree, a GGO will want to actually collect votes on election day.  Actual votes are collected in the votes folder but require the repo to be configured as such, again via data in the ./info section.

As an example, the following section assumes the town of Cambridge Massachusetts.  When the city of Cambridge clones the VOTES repo for the 2018 election, assuming that all the parent GGO are indeed participating in a VOTES framework, the directory tree will look someting like:

```
US-2018-National-Election/.git
                          info
                          ballot
                          bin
                          votes
                          ggos/Massachusetts/.git
                                             info
                                             ballot
                                             bin
                                             votes
                                             ggos/Cambridge/.git
                                                            info
                                                            ballot
                                                            bin
                                                            votes
                                                            ggos/5th Congressional District
                                                                 7th Congressional District
                                                                 ward 1-1
                                                                 ward 1-2
                                                                 ...
                                                                 ward 11-2
                                                                 ward 11-3
```
Each Congressional District and Ward would have a git repo where there respective ballot contests can be entered.  When the voter gets a ballot from the VC (either an absentee, early, or on election day ballot), the VOTES framework will generate the correct ballot for the address.

Implementation note: it is possible for precincts/VC to share the same repo or leverage a parent repo to cast votes into - it is configurable into which repo a precinct/VC submits votes to.

# 4) The Voter ID Repo(s)

There three versions of the voter-id repo.  The first variant is private (a.k.a. The Private copy) to the voting center's election officials, nominally controlled by the state certificate authority entity.  It is not publicly shared even though it stored in the VOTES framework.  It should not be confused with whatever database and/or application and/or process that the state, town, or precinct election officials are using to correctly and accurately identify voters.

The private version of the VOTES voter-id repo only contains the voter's name, address, and two additional fields to store VOTES information.  One field is the VOTES voter status which concerns the state of the voter's ballot within the VOTES supported ballot workflows.  The other is a VOTES generated digest.

The private VOTES voter-id repos is never aggregated and is never publicly shared.

The second variant of the VOTES voter-id repo is public (a.k.a. The Public Copy) and only contains the voter's name and address as entered in the state/town private repo.  The public variant repos are organized in a similar manner to VOTES ballot repos via the git submodule hierarchy described above.  However, unlike the ballot repo this repo is only publicly available once all the poles close.  VOTES maintains this repo as an internally updated copy of the private version.

The third version of the VOTES voter-id repo is similar to the private variant except that it is VOTES internal only (a.k.a. The Internal Copy).  It also contains two additional fields beyond the voter's name and address, a status field and a VOTES generated digest.

VOTES keeps the 2nd and 3rd versions in sync with the first version as the state enters and modifies their private copy.  The 2nd and 3rd versions are only updated with new/changed/removed voter id's when the private version is updated by the state/town.

Regarding the state/town private copy, depending on the state of the ballot (see the UX documentation for more details on ballot/voter workflows) the digest field may be blank, it may contain the digest of the blank (!) ballot that the voter has received but not filled in, or it may contain the double encrypted digest of the voter's _physical_ ballot digest as it was scanned into VOTES.  Specifically this digest when so doubly encoded __ONLY__ points to the scanned physical ballot, not the ballot contents that were scanned into the VOTES SaaS implementation.  The VOTES electronically scanned ballot has a completely different digest associated with it.

The 3rd version of the VOTES voter-id repo, The Internal version, is somewhat similar to The Private version except that The Internal version __only__ contains the double encrypted digest of the electronically scanned ballot.  The Internal version has no pathway to the physical ballot and The Private version has no pathway to the electronic copy of the ballot.  But with the valid double decryption of either, The Private version allows election officials following due process to associate a voter with their specific ballot while The Internal version allows VOTES to associate the voter with their specific electronic copy of the ballot.

In no case can either ballot (physical or electronic) be associated with a voter given The Public version of the voter-id repo since that version does not contain any digest or ballot information, encrypted or not.

# 5) How Ballots Are Entered - an Overview

A paper or electronic ballot, generated by the VOTES framework, is custom generated for the address of the identified voter.  It is not required that the VOTES framework (the SaaS implementation) prints the voter-id paperwork.  A precinct can alternatively use their own voter-id paperwork.

Regardless, the voter fills out the ballot and submits it to a VOTES compatible ballot scanning device operated by an election official.  The ballot is verified not to contain any overvotes or undervotes.  An overvote will block the submittal of a ballot as being invalid.  An undervote may or may not block a ballot scan.  Each precinct/state can configure VOTES as to how undervotes are handled.  They can simply be ignored or be configured to allow an election official to ask/allow the voter to fill out a new ballot.

Once validated by the VOTES framework, the ballot is submitted to the VOTES system and the various repos are updated accordingly.

There are several workflows checks that are not configurable and are part of the nature of VOTES.  For example once a voter (a specific voter-id) has submitted a ballot, they no longer can submit any other ballot, be it absentee, early, late, whatever.  However, as described how a precinct handles undervotes is configurable.

## 5.1) In Person Voting

See the UX documentation describing in person voting.  This also includes in-person early voting.

## 5.2) Absentee Voting

See the UX documentation describe [absentee voting](UX/absentee-voting.md)

## 5.3) UVBM - Universal Vote By Mail

See the UX documentation describe [UVBM voting](UX/UVBM-voting.md)

# 6) What Is Accessible When and General UX

Note - there are different classes/sets of VOTES supported workflows/UX experiences.  One set is voter centric - how the voter experiences the act of casting a ballot.  This includes in-person voting at a voting center, both for early voting or election day voting.  The voter UX also includes non in-person voter workflows such as absentee and UVBM.

Separate from voter UX is the GGO pre-election day workflows.  These include how the various GGO's construct their ballots and configure VOTES to handle customizable aspects of the voter experience.  Section 6 pertains to the GGO centric UX.

## 6.1) Pre Ballot Freeze Date

Each GGO (Geopolitical Geographical Overlay) starts filling in their respective information and data per the Ballot Freeze Date (BFD) workflows.  The various entities/overlay owners enter the races/questions they wish to be contained on their respective ballot sections.  These can be ballot races, ballot questions, etc.

Each GGO can also select the voting algorithm if different from the default tally settings.  One reason for a default [tally algorithm](https://electology.org/library#104) to be approval is due to the shortcoming of plurality voting.  Having a GGO to take action to change the default is to plurality hopefully will increase awareness of better tally alternatives.

Note that each GGO/overlay in one sense works independently of all the others.  Each entity can only modify their repo - their own specific GGO information.  Note - various git hooks and other aspects of the VOTES framework enforce the non-alteration of VOTES framework repo local files which defines how the GGO interact in a hierarchical tally sense.   Similar to software development across a distributed project spanning distributed teams, the different entities pull and push their work to the configured VOTES SaaS github servers.  There is distributed, tracked, authenticated sharing of the specific election repos during the pre-election day workflows.

Note that virgin ballot free VOTES repo contains VOTES framework files as well as files and templates for use by the various GGO.  A ballot that is given to a specific voter at a specific location will be a function of the aggregation of the ballot questions of the various overlays and the specific street address of the voter.  Each GGO composes their respective section of the ballot.

As mentioned each GGO owns a repo that is submodule of the parent GGO.

Note that during this process each entity can both test their election independently of other parent/sibling/child repos as well as test a full election.  The VOTES repo/SaaS framework comes with a test harness and test data for testing.

With this overview of VOTES in mind, once again note that VOTES (the framework and hence the repos) will be compliant as possible with [NIST](http://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.1500-100.pdf) standards - this part of the value add of a VOTES framework.

Regarding the voter-id repo, though it is highly recommended that election official pre-fill out the voter-id repos with the registered voters, actually doing so is optional.  Voters can be added to the voter-id repo directly at the voting center if so configured by the election officials.

Once a GGO achieves their BFD, their portion of ballot is ready.

## 6.2) Pre Election Day, Post Ballot Freeze Data

Once all the GGO's complete their portions of the ballot, the ballot is said to be done and is made available to all voters.  Due to the inherent design nature of the GGO's, every address in a precinct can obtain their address correct ballot via either the publicly available ballot repo or via their election officials - who obtain it via the public ballot repo as well.

As the precincts/state support it, early voting, absentee voting, and UVBM workflows can commence.  Each precinct/state follow their own workflows regarding when the ballots are actually cast and scanned.  Note that the ballot repo is __not__ publicly updated once ballots are allowed to be entered into VOTES.  Any patches/fixes to the ballot itself post the Ballot Freeze Date is available only as a fork of the ballot repo - a physically separate repo.  Once all polls close, the fork is merged into the original ballot repo on a branch so to record the changes.

## 6.3) Election Day

Voters visit precinct/voting centers and cast votes in-person.  See the voter IX documentation regarding the various kinds of in-person voting experiences/workflows.

## 6.4) When the Last Precinct Closes

When the last precinct closes and all the UVBM, early ballots, and absentee ballots are accepted and no further un-cast ballots are acceptable, the ballot and voter-id repos are made publicly available.

Note that some precincts may still be scanning ballots after all the polls close.  This could be by choice or due to computer glitch, power failure, etc.  Regardless as precincts update their repos, in a manner similar to native distributed software development, they post their latest versions of their repos when they are ready.

At this point the general public is free to execute and inspect the tallies as precincts post their results.

## 6.5) Post Election Day

Voters can inspect either their personal physical ballot or its electronic copy by visting in-person an election office.

Citizens at large can inspect The Public version of the voter-id repo(s) and the ballot repo(s).  All citizens can look for voter-id issues, ballot issues, election fraud issues, etc.

Note that there is nothing in VOTES that produces a single official version of the tally since an official tally is available to all citizens to compute themselves.  The VOTES ballot repo(s) are completely open source.

### 6.5.1) Ballot Redress and Nullification

Note that all VOTES repos are a full ledger records of all transactions as both are based on git.

Regarding nullifying fraudulent ballots, a specific ballot can be nullified as an additional change to the underlying git repos.  Whenever a ballot is nullified, the specific state/precinct ballot repo will receive a change that nullifies the specific ballot of interest.  In addition The Private and The Internal voter-id repos fully record each nullification, recording the who, what, when, why etc of the nullification.  This information is absent from The Public version of the voter-id repo.

The nullification only can occur at the owning GGO level or above, requiring the necessary double certificate authorities to create such a change.  Workflow details concerning the due process necessary for nullifying ballots is contained in the configuration section of the ballot repo for each GGO.  In this manner different states can decide how to handle ballot nullification workflows as they desire.

Depending on who is asking for a nullification affects the specific workflow that needs to be followed.  In the case of a third party successfully questioning a voter id via the contents of a voter-id repo, or successfully questioning the procedures or behaviors of an election official or precinct, the voter-id repo is decoded for the identified voters, the true ballot digests are obtained, and their ballots are nullified.

Election officials can also call for the nullification of ballots.

Even with the safeguards and double encryption, the potential for abuse of this feature is high.  As such VOTES requires a minimum number of ballots to be nullified before executing any nullification transaction, somewhat similar to a block-chain model.  It is also possible to disable this feature by precinct by configuration, disabling the nullification capability.

Nominally nullification is not a public process so to protect the identity of the voter - all the public will know is that a decoding occurred (The Public version of the voter-id repo will not know which voter-id was decoded), and that some ballots were nullified (since the ballot repo does indeed change).  When a voter-id is decoded, the record of which ballot was decoded is encrypted.  And in addition that info is limited to The Private and The Internal version of the voter-id repo.

The owner of the ballots will see that their ballot was nullified when they inspect their ballot either via a meeting with an election official (so to see their electronic copy of their physical ballot), or if they already have securely obtained their electronic ballot digest, by direct inspection of that ballot.  Or it might be the case that they receive notification that their voter-id data was decoded if their election officials are sending out that information.

In either case the voter can decide whether or not to pursue redress and have the nullification itself nullified.  If the voter pursues redress, that process too is not public so to protect the anonymity of the voter and their ballot.  If they win their case, the original nullification of their ballot is nullified, re-instating their ballot in the tally.

### 6.5.2) Recounts

Post the closing of all polls/precincts/voter centers, the tallies are more or less immediately available for anyone with public access to execute.  However, post poll closing election officials, voters, and third parties will most likely inspect the data and question any irregularities found.  Irregulars can stem from many different effects and may or may not result in fraudulent ballots.  Ideally, any such fraudulent ballots will be delineated and nullified.

As such, until the election is declared officially closed, the final tally of any contest may indeed change as all citizens and officials looks for irregularities.  It is nominally up to the election officials of the root GGO's (the states) to declare the official closure of an election within their GGO.  At that point, neither the ballot or voter-id repos can be changed.

# 7) Post Election Analysis

Once the repos are publicly available, even after the election is officially closed, the public is free to analyse the repos.  For example, the tally algorithms can be changed to determine if a different algorithm would have changed the results of a race or contest.  Since the repos are public and free via an EULA that restricts certain anti-constitutional anti-democratic uses such as trying to sell or selling votes, citizens can clone the repo and, for example, change the tally algorithms and such.

## 7.1) Determining Gerrymandering Coefficients

Regardless of the legality of [gerrymandering](https://en.wikipedia.org/wiki/Gerrymandering), given the constitutional guarantee of 'one person one vote', one interpretation of this guarantee is that nothing should diminish or augment 'one person one vote'.  That is, in effect one voter's ballot should not count more or less then another's ballot.  However, whether gerrymandering is or is not illegal is a separate and different question as to whether or not gerrymandering is happening and to what degree it is happening.  All citizens should be able to observe the effects of gerrymandering on the votes in their community.

With the ballot and voter-id repos being publicly available, it is possible to determine at the various GGO levels the degree of gerrymandering that is present.  For example, if a state has a heavily gerrymandered federal, state, or city districting, then the representation of a political party or individual at that GGO level can vary significantly from the 'popular vote' (given no districting) or given alternative district boundaries.

With VOTES, any voter or 3rd party can look at any specific ballot in VOTES, enter an arbitrary address, be it their own specific ballot or not, and VOTES can display the gerrymandering coefficients as a function of the various ways the state or town is currently __and can be__ districted.  The gerrymandering coefficient for each such scenario, be current or hypothetical, can be generated and shown to be positive (this ballot is effectively augmented in representative voting power) or negative (this specific ballot is effectively diminished in representative voting power) and by how much.

Alternatively, a voter can also go to The Public voter-id repo and see the gerrymandering coefficients for the various questions/races on the ballot for that address.  In this latter method the voter enters nothing but needs to remember how they voted on each question/race to see how augmented or diminished their potential votes are for either candidate.
