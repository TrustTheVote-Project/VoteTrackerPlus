# 1) Design Notes/Thoughts Regarding the Ballot Repo (unreviewed)

__As an example, the following notes are assuming a 2018 US national election.__

See [project-overview.md](https://github.com/PacemTerra/votes/docs/project-overview.md) for a general overview.

There is a local copy of [NIST.SP.1500-100.pdf](https://github.com/PacemTerra/votes/docs/NIST.SP.1500-100.pdf) which contains a terminology section on page 120 as well as the precinct and ward map for Cambridge Massachusetts on pages 14 and 15.

# 2) Git Based Prototype Overview - the Ballot Repo

As a prototype, the idea is to just (sic) use a set of git/github repos to host the election data for an election.  Once a prototype is up and running and we know more of what we do not know now, the github backend implementation can be switched out.

Regarding using bitcoin as a backend - the current thought is that a bitcoin is to tied to an economic model so to be reasonably applicable to a voting situation.  The use cases are too different even though both scenarios share a similar desire to authenticate a ledger of data.  Having the ballots and the algorithms being completely stored unencrypted in a publicly accessible manner, albeit a git repo with many git submodules, achieves the verifiability goals.

Regarding Ethereum, it is still unclear whether an Ethereum solution will enable the creation of a market to sell and buy votes (by allowing individual voters to offer their ballot contents to a third party as proof of sale).

As an example and a talking point, the following overview is based on a hypothetical 2020 US presidential election.

So, the git/github prototype idea is to allocate a set of git/github repos for the 2020 US presidential election.  The (TBD) federal agency in charge of the presidential election creates the cert root authority so to be able to provide the authentication for intermediate cert authorities at the state level (or the next downward hierarchical) __Geopolitical Geographical Overlay (GGO)__  overlay for the election.  The state does the same for the next lower level GGO (counties, boroughs, towns, districts).  And so on until each actual/planned voting center/precinct has a cert to identify themselves.

Each GGO (the federal government, a state, a county, a town, a whatever) will need to clone a pre-configured 2020 VOTES repo.  The pre-configure-ing is mainly to create an ease-of-use UX for the GGO so to allow all the various repos to be aggregated.

For the git/github prototype, low-level repos will simply (sic) be a git submodule of the parent GGO, the git submodule tree mirroring in affect the cert chain hierarchy.

The federal, state, town etc git repos all are clones the same pre-configured virgin/empty VOTES repo.  An empty VOTES repo does not yet contain any election race/question details.  However it does contain the (latest) release of the VOTES framework as well as the configuration data that make it easy to create such a US federal based election.  A state only election or an election for a different country with different fundamental overlays/entities would have a different pre-configuration.  The VOTES clone specifies things such has how the different (arbitrary) GGO are aggregated within a single election.

## 2.1) What actually is a ballot?

### 2.1.1) Option A - a ballot is an empty commit

In the git prototype a ballot is simply an empty commit with a git hook validated/managed description.  The voter's choices on the ballot are scanned off the paper ballot and yaml/json/xml encoded into the commit message.  The only files contained in a repo are the VOTES framework files and the GGO's ballot sections, ballot/election configurations, etc.  As noted this includes the tally algorithm and all election related information.  Post election day when the repos are made publicly available, anyone who downloads the repos (the root repo and all the submodule repos) will be able to count the votes for all races.  They will also be able to see their individual ballot via their commit hash keys.

### 2.1.2) Option B - a ballot is just a text file in ballots subtree of the repo.

To tally a state ballot question, one needs to clone the state and its submodule repos and perform the count on their computer or phone, etc.  Note - they will also be able to tally the votes using different tally algorithms to the extent that it makes sense (since for example a plurality ballot is not tally-able with an approval tally algorithm).

To tally a national ballot question or race, one needs to clone the national repo and all its submodule repos.

## 2.2) Basic Git Repo Prototype

As a prototype implementation the VOTES framework can (in theory - TBD) be implemented as a set of git repos connected via submodules.  The parent repo is associated with the __Geopolitical Geographical Overlay (GGO)__ with the greatest geographical geopolitical extent in the election.  For the 2018 US national election, this would be the federal government as it is a national election.

Note that if only one or a few states adopt VOTES by that time, it is ok. Those states would act as the VOTES root certificate authorities for the towns and counties/boroughs that are participating.

All VOTES repos have the same layout regardless of the GGO (national, state, county, town, etc).  What is different is only the data that is contained in the folder structure within and where/how the submodule tree is stitched together.

Each repo contains the information authored by each GGO.  However, per the git subtree hierarchy children and parent repos as well as configuration data information is shared across repo.

## 2.3) Folder Layout Per Git Repo

So the root most GGO is that git repo _owned/authored_ by the VOTES root authority of the cert chain for the 2018 US election (_the election_).  In this case the agency deemed responsible for actually running the 2018 national US election would be the VOTES root authority.  The folder structure for VOTES repos is:

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

### 2.3.1) Child GGO's - Git Submodules

A child GGO is one where the VOTES Certificate Authority (CA) for this GGO creates an intermediate CA and allocates/associates sub GGO information with the ./info folder.  The git submodule tree looks like the following:

#### ./ggos/\<sub GGO class name>/\<instances name>

The \<sub GGO class name> is an arbitrary I18n name given to the specific intermediate CA's assigned by this CA.  For the US election this would be the 50 states plus any territory or other geographical geopolitical location.  (If voting is taking place electronically via the internet or other network, other or additional location coordinates will apply.)  This configuration info is also located in the ./info folder.

The following are examples.

#### ./ggos/state/Alabama, Alaska, Arizona, ...

The US national GGO will define 50 git submodules under the ggos subfolder.

#### ./ggos/town/Abbeville, Adamsville, Addison, ...

Each state entity (specifically each sub GGO who has been delegated as an intermediate certificate authority) can independently select its sub GGO class name for their state.  As an example Alabama may use the I18n string _town_ in its VOTES repo as above.

### 2.3.2) Multiple / Parallel GGOs

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

# 3) The Voter ID Repo

The voter ID ballot is a separate non-aggregated repo with a separate one nominally created for each precinct.  It contains the voter id, which nominally is the voter's name and address.  Each precinct can configure what comprises the voter id as this repo is precinct specific.

Importantly the voter id contains a specially constructed encrypted key of the voter's ballot key.  To decode a voter id repos key requires both a precinct certificate and the presiding GGO certificate so to create a decoding key - voter id digests are doubly encoded.  The presence of a single key will not result in a properly decrypted ballot digest.

In addition, the GGO decoding key is itself generated on demand and is based on the full voter id repo (ledger), and when generated, requires the voter id repo to register the creation of the _decoding_ as an additional transaction.  This decoding transaction records the who, what, when of the decoding (but not the actual generated key).  In this manner the vote-id repo records all the decodings of a voter-id entry.

So as the ballot repo records specific ballot nullifications potentially post the close of the election, the voter-id repo records when the presiding certificate authorities provide a voter-id decoding.  In this manner the voter knows both if their ballot is nullified or if their voter-id key has been decoded.

# 4) How Ballots Are Entered - an Overview

A paper or electronic ballot, generated by the VOTES framework, is custom generated for the address of the identified voter.  It is not required that the VOTES framework (the SaaS implementation) prints the voter-id paperwork.  A precinct can alternatively use their own voter-id paperwork.

Regardless, the voter fills out the ballot and submits it to a VOTES compatible ballot-capture device nominally operated by an election official at a precinct/VC.  The ballot is verified not to contain any overvotes or undervotes.  An overvote will block the submittal of a ballot.  An undervote is simply an ignorable alert to the voter that they have not entered all the ballot choices that that ballot supports.

Once validated by the VOTES framework, the ballot is submitted to the ballot repo and the commit digest (the ballot digest) is returned to the voter, the encrypted digest is returned to the election official, and the voter-id and the encrypted ballot digest is entered in the voter-id repo.

## 4.1) UVBM and Early Voting

Precincts/VC can choose whether they enter early-ballots when received or on the day of election.  The digests associated with the ballot can be made available to the early voter as the precinct sees fit, for example either by physical or electronic post.

In such UVBM or early voting situations, election officials should take care that ballots are entered by two people who are not sharing information.  One person acts as the election official and one acts as the voter.  The election official actor should never see the un-encrypted ballot digest and the voter actor should never see the encrypted digest.  The reason for this is that there should be no opportunity to unambiguously record the ballot and encrypted digest together as that would create the opportunity for a market to buy and sell votes.  As long as there is no publicly verifiable connection between any digest and it encrypted value, the public accessibility of the data contained in the ballot and voter-id repos can not easily lead to a marketplace for buying and selling votes.

As both repos are fully public, voters can validate their ballot by looking up their digest in a copy of the ballot repo or their encrypted digest in their voter-id repo.  But there is no public means to verify that the two match.

Note - that is why it is important in UVBM, early voting, or vote by mail situations that election officials need to follow the proper procedures and guidelines.

## 4.2) Election Day

Voters physically enter a precinct/VC and cast paper ballots.  For precincts/VCs that wish to support electronic balloting, ballots are entered electronically.  Early voting and absentee voting can occur on election day or prior depending on what each precinct/town decides.

# 5) What Is Accessible When

## 5.1) Pre Ballot Freeze Date

Each GGO (election overlay) starts filling in their respective information and data per the Pre Ballot Freeze Date (PBFD) workflows (there are different types of  workflows/UX experiences - PBFD, pre-election day, election day, and post election day).  The various entities/overlay owners enter the races/questions they wish to be contained on their respective ballot sections.  These can be ballot races, ballot questions, etc.

Each GGO can also select the voting algorithm if different from the default approval setting.  One reason for a default [tally algorithm](https://electology.org/library#104) to be approval is due to the shortcoming of plurality voting.  Having a GGO to take action to change the default is to plurality hopefully will increase awareness of better tally alternatives.

Note that each GGO/overlay in one sense works independently of all the others.  Each entity can only modify their repo - their own specific GGO information.  Note - various git hooks enforce the non-alteration of VOTES framework repo local files which defines how the GGO interact in a hierarchical tally sense.   Similar to software development across a distributed project spanning distributed teams, the different entities pull and push their work to the configured VOTES SaaS github servers (hosted somewhere).  There is distributed, tracked, authenticated sharing of the specific election repos during the pre-election day workflows.

Note that virgin ballot free VOTES repo contains VOTES framework files as well as files and templates for use by the various GGO.  A ballot that is given to a specific voter at a specific location will be a function of the aggregation of the ballot questions of the various overlays and the specific street address of the voter.  Each GGO composes their respective section of the ballot.

As mentioned each GGO owns a repo that is submodule of the parent GGO.

Note that during this process each entity can both test their election independently of other parent/sibling/child repos as well as test a full election.  The VOTES repo/SaaS framework comes with a test harness and test data for testing.

With this overview of VOTES in mind, once again note that VOTES (the framework and hence the repos) will be compliant as possible with [NIST](http://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.1500-100.pdf) standards - this part of the value add of a VOTES framework.

Regarding the voter-id repo, though it is recommended that election official pre-fill out the voter-id repos with the registered voters, actually doing so is optional.  Regardless, when ballots are cast part of the actual voting process is the recording of the voter-id in the voter-id repos of the VOTES framework.

So for the PBFD workflows, the various GGO work on their election ballots.  At some point all the GGO's declare done.  At some point the election set of repos is declared done.  When that occurs, early balloting can proceed.

## 5.2) Pre Election Day, Post Ballot Freeze Data

Once the ballot is frozen, the ballot is made available to all voters.  Due to the inherent design nature of the GGO's, every address in a precinct can obtain their address correct ballot via either the publicly available ballot repo or via their election officials (who obtain it via the public ballot repo).

As the precincts, towns, and state support, early voting, absentee voting, and UVBM workflows can commence.  Each precinct, town, and state can following their own procedures and guidelines regarding when the ballots are actually cast.  Note that the ballot repo is NOT available with any new updates post the __Ballot Freeze Date__ until all the polls close in all precincts.

Technical note - and patches/fixes to the ballot itself post the Ballot Freeze Date is available only as a fork of the ballot repo - a physically separate.  Once all polls close, the fork is merged into the original ballot repo on a branch so to record the changes.

As ballots are cast, via the VOTES SaaS framework and not via public copies of the repos, individual ballot digests can be inspected to make sure that the ballot is correct.  Though digests can be looked up via humans - bots are rejected - neither repo, ballot or voter-id, are publicly available.

## 5.3) Election Day

Voters visit precinct/voting centers and cast votes.  For those precincts that support electronic voting on election day, voters can vote electronically.

Note that due to inherent design nature of the voter-id anad ballot repo, it is impossible for a single voter to vote twice via any medium.  Caveat - reminder - VOTES is __NOT__ a voter id system that properly identifies voters and who and who cannot vote.  VOTES only records ballots and voter-id's however the precincts choose to identify their voters, preventing any such identified voter from voting more then once.

## 5.4) When the Last Precinct Closes

When the last precinct closes and all the UVBM, early ballots, and absentee ballots are accepted and no further ballots are acceptable, the ballot and voter-id repos are made publicly available.  Changes to the ballot itself post Ballot Freeze Date are merged in on a release branch.

At this point the general public is free to execute and inspect the tallies.

## 5.5) Post Election Day

Voters can continue to inspect their ballots but at this point the inspection can occur both via the VOTES SaaS framework or via a public copy of the ballot repo.  Voters can continue to seek redress from election officials if they so choose.

Election official can likewise decide to seek redress if they find improper voter-id information.

As both repos are publicly available, any third party can also seek redress.

### 5.5.1) Ballot Redress and Nullification

Note that both repos are a full ledger records of all transactions.  The ballot repo fully records each new record while the voter-id repo records every write as well as every encrypted digest decoding.  A ballot is nullified when a new version of the ballot is entered which nullified the original.  Nullifications can themselves be nullified.

The nullification only can occur at the owning GGO level or above, requiring not only the necessary certificate but also the pre-configured due process recorded in the ballot.

Depending on who is asking for a nullification affects the specific workflow that needs to be followed.  In the case of a third party successfully questioning a voter id via the contents of a voter-id repo, or successfully questioning the procedures or behaviors of an election official or precinct, the voter-id repo is decoded for the identified voters, the true ballot digests are obtained, and their ballots are nullified.

Nominally this process is not a public process so to protect the identity of the voter - all the public will know is that a decoding occurred (the public will not know which voter-id was decoded), and that some ballots were nullified.  When a voter-id is decoded, the record of which ballot was decoded is encrypted.  The key is available to the election officials (the owners of the first certificate), the GGO (the owners of the second certificate), and the voter themselves.

The owner of the ballots will see that their ballot was nullified when they inspect the ballot repo.  Or it might be the case that they receive notification that their voter-id data was decoded.  The ballot owner can contact their election officials and obtain the key(s) to the decodings of their voter-id so to evaluate what happened.  At that time, the voter can decide whether to pursue redress and have the nullification itself nullified.

If the voter pursues redress, that process too is not public so to protect the anonymity of the voter and their ballot.

### 5.5.2) Recounts

Post the closing of all polls/precincts/voter centers, the tallies are more or less immediately available for anyone with public access to execute.  However, post poll closing election officials, voters, and third parties will most likely inspect the data and question any irregularities found.  Irregulars can occur in either the voter-id repo or the ballot repo.  Problems with the tally algorithms can be found, with voter identification records, etc.

As such, until the election is declared officially closed, the final tally of any contest can change.  It is nominally up to the election officials of the highest GGO to declare the official closure of an election.  At that point, neither the ballot or voter-id repos can be written to or decoded.

# 6) Post Election Analysis

Once the repos are publicly available, even after the election is officially closed, the public is free to analyse the repos.  For example, the tally algorithms can be changed to determine if a different algorithm would have changed the results of a race or contest.

## 6.1) Determining Gerrymandering Coefficients

With the ballot and voter-id repos being publicly available and since the individual voter knows both their ballot and their voter-id, they can personally determine how much their vote has be gerrymandered as a function of political party or other third party interest.  (District gerrymandering can occur for reasons other then political party - any powerful enough entity can influence districting so to influence ballot outcomes.)

For example, suppose a voter voted for political party A for a state level contest.

Given the known addresses of all the voters for that race, and given the ballots for that race (which are independent of address since that information is hidden/encrypted), it is determinable the overall vote for political party A versus the actual representation of political party A in the tallies at the state level.

Thus each voter can see how their ballot is either unrepresented (a positive coefficient) or overrepresented (a negative coefficient) at the state level at a political party overlay.  Given constitutionality of one vote one person, a voter may wish to question the districting in which they live.
