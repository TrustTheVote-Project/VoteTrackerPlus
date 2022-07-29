# VoteTracker+

## The Pitch

VoteTracker+ is an open software ballot tracking system that increases the security, accuracy, and trustworthiness of a paper ballot election by cryptographically tracking the [Cast Vote Records](https://pages.nist.gov/ElectionGlossary/#cast-vote-record) associated with paper ballots.

VoteTracker+ provides three core capabilities:

1. Directly supplies a cryptographically anonymized ballot check back to the voter, allowing the voter to validate that their specific ballot has been interpreted, recorded, and tallied as intended

2. Cryptographically records and seals the entire history of the election as it occurs in near real time

3. Allows the public to inspect and validate the official Cast Vote Records and tally as well as (ideally) the aggregate voter ID rolls across the entire electorate
 
## 1) Overview of VoteTracker+

VoteTracker+ is a 100% open source paper ballot tracking solution with no dark corners.  VTP includes the complete historical software provenance of all the VTP software as well as the complete runt-time provenance of the creation of all [Cast Vote Records](https://pages.nist.gov/ElectionGlossary/#cast-vote-record) (CVRs) from the paper ballots.  Depending on the level of adoption by a precinct, VTP can also provide tracking of the paper ballots themselves as well as print on demand address specific blank ballots.  It is important to note that the level of adoption is up to the election officials and is not dictated or required by VTP to track the CVRs.

VoteTracker+ 1.0 is focused on the tracking of paper ballots while minimizing the level of adoption required by election officials.  VoteTracker+ 2.0 includes the additional dramatic reduction of the cost and time of setting up, testing, securing, running, auditing, adjudicating, and certifying the end-to-end process of running a public election by more directly supplying more of the back-office software based infrastructure required to do so.  VTP 2.0 requires a deeper and more thorough adoption by election officials.  However, regardless of the level of adoption VTP will and always be 100% open source and not owned by any person or corporate entity.  There is no stove-piping or dark corners or special hardware requirements with VTP.

## 2) Why is VoteTracker+ non partisan and non sectarian while being accurate and trustworthy?

First, VoteTracker+ is 100% open source - it is owned and verified by the people and for the people 
even when operated by a small number of representatives of the people.  VTP is about accurate and trustworthy elections and not about advancing any particular political or sectarian agenda.  It applies technology and cryptography to validate the full history of events that occur prior to, during, and after election day with respect to the cast ballots.  VTP records history as it happens in an anonymous and cryptographically sound and sealed manner.  It records the change history of all the software used in the election as well as all the CVRs.  Similar but very different to block chain technologies that ensure the legitimacy and accuracy of cryptocurrency transactions, VTP supplies a greater guarantee and degree of trust due to the details of the additional cryptographic checks and balances within VTP and the distributed nature of the implemented [Merkle tree](https://en.wikipedia.org/wiki/Merkle_tree).

One unique and key aspect of VoteTracker+ is that it offers to the voter a special ballot anonymized paper check that contains a cryptographically sealed and anonymous slice of the specific live election data.  This places in the hands of the voter critical evidence of the election as well as their specific ballot all in an anonymous manner.

A second unique and key aspect of VoteTracker+ is that it cryptographically ties the digitally scanned [ballot images](https://pages.nist.gov/ElectionGlossary/#ballot-image) with the CVRs such that it is practically impossible to add, change, or drop digital scan image or VTP CVR once the paper ballot has been scanned.  With VoteTracker+ 2.0 and a deeper optional adoption of VTP technology, the paper ballots can be secured in a similar manner as well.

A third unique and key aspect of VoteTracker+ is that with VTP every voter can execute the same exact tally that election officials perform.  Whether a specific contest is [plurality](https://en.wikipedia.org/wiki/Plurality_voting), [Rank Choice Vote](https://pages.nist.gov/ElectionGlossary/#ranked-choice-voting), or some other [electoral system](https://en.wikipedia.org/wiki/Electoral_system#Types_of_electoral_systems), all such tallies can be executed and checked by any voter for accuracy.  In the case of RCV this includes close inspection of the multiple tally rounds that can occur with RCV.

## 3) Basic Voter In-place Experience (UX)

### 3.1) After the first 100 ballots have been cast

This is in the nominal case of there already having been cast 100 ballots of the same type.  VoteTracker+ requires a cache of 100 pre-existing CVRs so to insure the anonymity of the ballot tracking system.  Handling the case of either the first 100 ballots or the case of there being less than 100 ballots cast in the election are covered after this section.

From the voter's point of view, VoteTracker+ is primarily a backoffice implementation that generates cryptographic metadata associated with each [Cast Vote Record](https://pages.nist.gov/ElectionGlossary/#cast-vote-record) (CVR) for storing, retrieving, inspecting, and tallying the CVRs.  As such, the voter's current in-place voting experience changes in a few subtle but significant ways.  The following describes these changes in more or less chronological order from current nominal in-place voting experiences.

The first change a voter will notice will be that the paper ballot scanning device contains a display that privately reveals to the user the CVR itself, not the digitial scan of the ballot.  Every voter is given the oppourtunity , prior to the ballot being accepted in the election to self adjudicate their ballot in the case where the ballot scanned has mis-interpreted their ballot..  This offers the voter the opportunity to void their physical paper ballot and receive a new blank ballot if they believe their CVR is incorrect.  A voter is free to ignore this step and submit their ballot regardless, in which case ballot may be adjudicated by an election official at some later time.

The second change is that once submitted, the voter can optionally receive a printed anonymized ballot check.  The ballot check is cryptographically randomized and anonymized set of unique identitifiers, one per ballot contest.  The ballot check also contains 99 additional randomized and anonymized contest CVRs from other ballots.  In effect each ballot check contains 100 separate checks for each contest.

In addition to the printed CVR ballot check, the voter has the opportunity to privately view a two digit offset into the 100 rows indicating which specific row is their specific ballot.  There is no way a third party can determine which row is the voter's.  However, it is up to the voter to remember their specific row from this point on.  Though the voter's row contains the micro checks in contest order, the other rows have been randomized on a per row basis such that no row will normally represent any single ballot.  There is no information in the VTP repositories that enables the reconstruction of a ballot from either a row of micro checks or from a ballot check.

The third change is that prior to leaving the election controlled space of the voting center, the voter can place their ballot check on a second and independent VoteTracker+ scanner that will inspect their check and validate the accuracy of the check data against the live local VTP ballot [Merkle tree](https://en.wikipedia.org/wiki/Merkle_tree).  This would be the initial validation to the voter that their blessed CVRs as well as 99 other legitimate ballot CVRs have been correctly scanned and recorded into the VTP repositories.  The ballot checks remain intact throughout the CVR aggregation process via the local repo Merkle Tree and do not change - they remain intact throughout the election and are contained in the final Merkle tree of the election.

The next three significant changes occur after all the polls close.  Once all the polls close, the election officials can make read-only copies of the VoteTracker+ Merkle Tree available for download and inspection via standard GitHub servers as ballots continue to be scanned and additional CVR data is uploaded.  Voters will be able to download the repositories as they are updated.  Note that the repositories include all the open source software via the same Merkle Trees to tally the contexts and validate individual ballot checks, including the voter's.  Once downloaded, the voter can:

- validate their specific CVR remained in tact and is contained in the election
- validate that 99 other CVRs remain in tact and are contained in the election
- tally the contests themselves, reproducing the exact same results as the official election results

The voter can continue to do this as more results are uploaded.

Note that with all the data and code available to the electorate, alternate facts, illegitimate narratives, or other attempts at casting doubt on the election can eventually be publicly shown to be false.  And if either the physical ballots are compromised, or if the live VoteTracker+ data is compromised, or if individual or groups of individual collude and generate false narratives or data, the accuracy or inaccuracy of such data and narratives can be determined transparently and universally among the electorate.  With VoteTracker+ there is no single party that privately determines the accuracy of the VoteTracker+ data.

### 3.2) Handling the first 100 ballots

VoteTracker+ can be configured to supply ballot checks and offsets to the first 100 voters casting ballots via a special workflow/UX involving an interim ballot check.  After the voter self adjudicates their ballot, VTP will generate a random 3 digit number and associated one-way GUID, privately displaying the 3 digit interim offset to the voter while printing the GUID as an interum ballot check.  The interim ballot check contains no CVR digests.

The voter shows the interim ballot check to the out-processing EO who then records in the out-processing voter id roll that the voter has an interim ballot check.

Either after 100 ballots have been submitted or after all the polls close assuming the polling center stays open to allow for processing interim ballot checks, the voter once again enters the polling center and identifies themselves as an interim ballot check voter.  The EO confirm this is the case and visually inspects the interim ballot check.

The voter proceeds to a VTP scanner and inserts their interim ballot check into the scanner.  The voter must correctly remember their interim ballot check index and enter that on the keypad next to the private display.  Upon successful entering of both, the real ballot index is privately displayed to the voter and the real ballot check is printed.

### 3.3) When there are less than 100 ballots cast

The case of a precinct with less than 100 voters or ballots that have been cast is similar to immediately preceeding section 3.2 above - "Handling the first 100 ballot".  In the case of less than 100 voters, all the voters have received an interim ballot check.  once all the polls close, the voters still can exchange their interim ballot checks for real ballot checks by following the same workflow as in 3.2 above.  However, in this case instead of 100 rows of CVR digests only the total number of rows, which are the total number of ballots, will be printed.

Note that since the contest tallies per precinct are public information regardless of the number of voters, having a ballot check with the same less-then-100 rows will in itself reveal no additional information.

## 4) Basic Vote-by-Mail Voter Experience (UX)

VoteTracker+ can enhance the voter vote-by-mail experience depending on the level of adoption by both election officials and the voter.  If configured by election officials, the voter can receive their anonymized ballot check by mail.  In this scenario an election official performs the following nominal steps:

Nominal mail-ballot workflow/UX:

- receives/opens mail-in ballot package
- verifies the voter id
- places the ballot in the OEM+VTP mail-in scanner
- the scanner will display on the screen if ballot passes OEM and VTP checks
- if not, election official follows election guidelines
- if yes, the following are steps are completed
- if the voter supplied an optional ballot check (BC) public key, the election official scans the public key and the scanner stores the encrypted ballot index in the private ballot index ledger
- if the voter supplied a self addressed envelope for the ballot check, the VTP mail-in scanner prints ballot check and the EO places the ballot check in the self addressed envelope.

Note that the public key is not associated in any way with the paper ballot, the scanner image, or the ballot check.  The [public private key pair](https://en.wikipedia.org/wiki/Public-key_cryptography) generated by the voter is not tied to anything in particular so cannot really be used for voter identification.

After all the polls close and election officials have setup the required restricted access to the private ballot check index ledger, voters can visit election officials in person, nominally at their town hall or other officially designated location.  After the voter has properly identified themselves nominally in a manner similar to casting a ballot in person, an election official can privately and securely reveal to the voter their specific encrypted ballot index offset.  The voter can then enter the encrypted offset into the VTP mobile app to decrypt the index and reveal their true check index.  With that index they can validate that their specific mail-in ballot has been cast, recorded, and tallied as intended via the public VoteTracker+ election repos.

## 4b) Supporting the first 100 mail-in ballots

Though it is possible to support interim ballot checks to the first 100 mail-in voters, a less cumbersome workflow can be supported since at the time of opening the mail-in ballot the election official is in control of both the ballot and the voter identification.  Specifically:

First 100 mail-ballot workflow/UX:

- receives/opens mail-in ballot package
- verifies the voter id
- places the ballot in the OEM+VTP mail-in scanner
- the scanner will display on the screen if ballot passes OEM and VTP checks
- if not, election official follows election guidelines
- if yes, the following are steps are completed
- election official receives the mail-in interim ballot check which contains both the interim index and the associated GUID
- election official places the voter package together with the interim ballot check in the first 100 mail-in ballot box/pile
- this process is repeated until there are 100 interim ballot packages.  Note that VTP will automatically initiate the nominal mail-in ballot workflow when the 100 ballot cache has been achieved.
- an election official then processes the first 100 mail-in ballot box by re-submitting the interim ballot check in the VTP scanner
- if the voter supplied an optional ballot check (BC) public key, the election official scans the public key and the scanner stores the encrypted ballot index in the private ballot index ledger
- if the voter supplied a self addressed envelope for the ballot check, the VTP mail-in scanner prints ballot check and the EO places the ballot check in the self addressed envelope.

## 5) Basic Election Official Experience (UX)

VoteTracker+ brings significant election transparency to the entire election process by creating two additional CVR copies of the original paper ballots.  By simply using VoteTracker+ election officials leverage an open source validation of their ballot handling process that has come under increasing partisan attack.  The changes that election officials will witness when using a VoteTracker+ based election and voting system are chronologically summarized as follows.

### 5.1) Pre Election Day Summary

Leading up to the election, election officials can iterate over the ballot design and GGO boundaries similar to standard software development practices.  All changes are authenticated to the person making the change and all changes are run against standard automated tests.  Election officials can validate that every address receives the correct ballot via the GGO automated testing that VoteTracker+ supports.

Once a precinct finalizes a ballot, that ballot becomes available for early voting.  Early ballots can be entered into VoteTracker+ at any time, including prior, during, or after election day as configured by the VoteTracker+ configuration for that election.

### 5.2) Day of Election Summary

1) Depending on the level of adoption of VoteTracker+, all blank ballots can be generated on demand at the voter ID identification station.  There is no need to guess how many blank ballots to print beforehand or which ballots are needed at which voting locations.

2) If fully integrated with election official workflows, VoteTracker+ can independently record the voter ID, specifically only the name and address, independent from the official voter ID record or as the official voter ID record.  This allows each precinct or state to select the voter ID process and record keeping that they so choose.  Selecting VTP as the voter ID record solution is optional but if can be a cost saving measure.  If the voter ID is recorded with VTP, VTP will be able to flag identical names across different addresses across the entire electorate for potential deeper inspection and auditing, not just within the local precinct.  This increased transparency increases trust in the election as it can independently verify truthful election official voter ID activities while exposing fraudulent ones.

3) VoteTracker+ adds the capability of the voter to validate their contest CVRs before the ballot and the CVR are accepted into the election.

4) VoteTracker+ will add a voter approved CVR to the Merkle Tree that is behind VoteTracker+.  A primary property of the Merkle Tree is that it keeps history intact.  It is extremely difficult to thus change history, which includes the changing, inserting, or deleting a ballot.

With the full adoption of VoteTracker+ 2.0, the paper ballot themselves can be cryptographically associated with the ballot digital scam images.  The importance of this step is that each paper ballot is cryptographically connected to the digital scan and with voter's check in a specific manner that insures anonymity and election security, preventing fraudulent ballots to be added later or for ballots to be removed or even re-ordered.  Full adoption of 2.0 results three copies of the same data distributed in a specific safe and secure manner between election officials, the ballot scanning hardware manufacturer, and the voter themselves.

### 5.3) Post Election-Day Summary

Once the polls close read-only copies of the VoteTracker+ data, which contain the same Merkle Trees originally created by the election officials augmented with all the CVR submitted by the voters, can be made available.  VTP supports incremental releases to the public of this data at a frequency chosen by election officials.

Thus, the voters themselves can download copies of the election data, validate that their ballots are correctly contained within the elections, and tally all the contests themselves.  This is a game changing capability regarding assessing the accuracy and trustworthiness of election.

## 6) Franking - a VoteTracker+ 2.0 Consideration

[Franking](https://en.wikipedia.org/wiki/Franking) is the process of marking the paper ballot once it has been scanned to create the CVRs for the contests on the ballot.  This step can only really be attempted with 100% open software as it is all too easy to embed within the frank mark an indication of voter id.  As VoteTracker+ is 100% opensource, franking is a VoteTracker+ 2.0 consideration.

The general idea is to mark the paper ballot post the self adjudication thereof with contest digests generated by VTP.  In addition a run-time election private key generated GUID is also franked.  The digests and the GUID would also be associated with the digital image of the ballot.  However the GUID is not recorded in any of the VTP public ledgers.  Neither the paper ballots nor the actual digital images are public.

This allows an exact one-to-one mapping between the paper ballot and the digital scans thereof.  Both frank marks limit the ability of ballots to be inserted and removed from one of the two sources of this data, either the paper ballots themselves or the digital scans of the paper ballots.  The GUID also limits the ability fraudulent VTP ledgers to be added into the election's real VTP aggregated ledgers.

This also allows specific ballots or large numbers of ballots to be rejected post acceptance into the tally while allowing the voters who cast the ballots to know that their specific ballot has been rejected.  This allows the opportunity for election officials to nullify ballots after the fact while both having the original VTP tally remain accurate and having the voter able raise an anonymous claim that their ballot was incorrectly rejected.

Regardless of franking or not, if a voting center CVR records are rejected and the paper ballots are not, re-scanning the paper ballots a second time would render the voter's original ballot checks invalid and useless.  In fact any type of rescanning of the paper ballots nullify pre-existing ballot checks for those ballots.

## 7) Summary

In summary, VoteTracker+ is a 100% open source election and voting system, operated by election officials while being owned and verified by the people, that increases the security, accuracy, and trustworthiness of a paper ballot election.
