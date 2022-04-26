# VoteTracker+

## The Pitch

VoteTracker+ is an open software paper ballot tally and tracking system that increases the security, accuracy, and trustworthiness of elections by anonymously and cryptographically tracking paper ballots.

VoteTracker+:

- directly supplies a cryptographically anonymized ballot receipt back to the voter, allowing the voter to validate that their ballot has been read, recorded, and tallied as intended

- cryptographically records and seals the entire history of the election as it occurs in real time similar to cryptocurrency transactions

- allows the public to inspect and validate the official Cast Vote Records and the tally of the election
 
## 1) Overview of VoteTracker+

VoteTracker+ is a 100% open source paper ballot tracking solution with no dark corners.  VTP includes the complete historical software provenance of all the VTP software as well as the complete runt-time provenance of the creation of all [Cast Vote Records](https://pages.nist.gov/ElectionGlossary/#cast-vote-record) (CVRs) from the paper ballots.  Depending on the level of adoption by a precinct, VTP can also provide tracking of the paper ballots themselves as well as print on demand address specific blank ballots.  It is important to note that the level of adoption is up to the election officials and is not dictated or required by VTP to track the CVRs.

VoteTracker+ 1.0 is focused on the tracking of paper ballots while minimizing the level of adoption required by election officials.  VoteTracker+ 2.0 includes the additional dramatic reduction of the cost and time of setting up, testing, securing, running, auditing, adjudicating, and certifying the end-to-end process of running a public election by more directly supplying more of the back-office software based infrastructure required to do so.  VTP 2.0 requires a deeper and more thorough adoption by election officials.  However, regardless of the level of adoption VTP will and always be 100% open source and not owned by any person or corporate entity.  There is no stove-piping or dark corners or special hardware requirements with VTP.

## 2) Why is VoteTracker+ non partisan and non sectarian while being accurate and trustworthy?

First, VoteTracker+ is 100% open source - it is owned and verified by the people and for the people 
even when operated by a small number of representatives of the people.  VTP is about accurate and trustworthy elections and not about advancing any particular political or sectarian agenda.  It applies technology and cryptography to validate the full history of events that occur prior to, during, and after election day with respect to the cast ballots.  VTP records history as it happens in an anonymous and cryptographically sound and sealed manner.  It records the change history of all the software used in the election as well as all the CVRs.  Similar but very different to block chain technologies that ensure the legitimacy and accuracy of cryptocurrency transactions, VTP supplies a greater guarantee and degree of trust due to the details of the additional cryptographic checks and balances within VTP and the distributed nature of the implemented [Merkle tree](https://en.wikipedia.org/wiki/Merkle_tree).

One unique and key aspect of VoteTracker+ is that it offers to the voter a special ballot paper receipt that contains a cryptographically sealed and anonymous slice of the specific live election data.  This places in the hands of the voter critical evidence of the election as well as their specific ballot all in an anonymous manner.

A second unique and key aspect of VoteTracker+ is that it cryptographically ties the digitally scanned [ballot images](https://pages.nist.gov/ElectionGlossary/#ballot-image) with the CVRs such that it is practically impossible to add, change, or drop digital scan image or VTP CVR once the paper ballot has been scanned.  With VoteTracker+ 2.0 and a deeper optional adoption of VTP technology, the paper ballots can be secured in a similar manner as well.

A third unique and key aspect of VoteTracker+ is that with VTP every voter can execute the same exact tally that election officials perform.  Whether a specific contest is [plurality](https://en.wikipedia.org/wiki/Plurality_voting), [Rank Choice Vote](https://pages.nist.gov/ElectionGlossary/#ranked-choice-voting), or some other [electoral system](https://en.wikipedia.org/wiki/Electoral_system#Types_of_electoral_systems), all such tallies can be executed and checked by any voter for accuracy.  In the case of RCV this includes close inspection of the multiple tally rounds that can occur with RCV.

## 3) Basic Voter In-place Experience (UX)

From the voter's point of view, VoteTracker+ is primarily a backoffice implementation that generates cryptographic metadata associated with each [Cast Vote Record](https://pages.nist.gov/ElectionGlossary/#cast-vote-record) (CVR) for storing, retrieving, inspecting, and tallying the CVRs.  As such, the voter's current in-place voting experience changes in a few subtle but significant ways.  The following describes these changes in more or less chronological order from current nominal in-place voting experiences.

The first change a voter will notice will be that the paper ballot scanning device contains a display that privately reveals to the user the CVR itself, not the digitial scan of the ballot.  Every voter is given the oppourtunity , prior to the ballot being accepted in the election to self adjudicate their ballot in the case where the ballot scanned has mis-interpreted their ballot..  This offers the voter the opportunity to void their physical paper ballot and receive a new blank ballot if they believe their CVR is incorrect.  A voter is free to ignore this step and submit their ballot regardless, in which case ballot may be adjudicated by an election official at some later time.

The second change is that once submitted, the voter can optionally receive a printed ballot receipt.  The ballot receipt is cryptographically randomized and anonymized set of unique identitifiers, one per ballot contest.  The ballot receipt also contains 99 additional randomized and anonymized contest CVRs from other ballots.  In effect each ballot receipt contains 100 separate receipts for each contest.

In addition to the printed CVR ballot receipt, the voter has the opportunity to privately view a two digit offset into the 100 rows indicating which specific row is their specific ballot.  There is no way a third party can determine which row is the voter's.  However, it is up to the voter to remember their specific row from this point on.  Though the voter's row contains the micro receipts in contest order, the other rows have been randomized on a per row basis such that no row will normally represent any single ballot.  There is no information in the VTP repositories that enables the reconstruction of a ballot from either a row of micro reseipts or from a ballot receipt.

The third change is that prior to leaving the election controlled space of the voting center, the voter can place their ballot receipt on a second and independent VoteTracker+ scanner that will inspect their receipt and validate the accuracy of the receipt data against the live local VTP ballot [Merkle tree](https://en.wikipedia.org/wiki/Merkle_tree).  This would be the initial validation to the voter that their blessed CVRs as well as 99 other legitimate ballot CVRs have been correctly scanned and recorded into the VTP repositories.  The ballot receipts remain intact throughout the CVR aggregation process via the local repo Merkle Tree and do not change - they remain intact throughout the election and are contained in the final Merkle tree of the election.

The next three significant changes occur after all the polls close.  Once all the polls close, the election officials can make read-only copies of the VoteTracker+ Merkle Tree available for download and inspection via standard GitHub servers as ballots continue to be scanned and additional CVR data is uploaded.  Voters will be able to download the repositories as they are updated.  Note that the repositories include all the open source software via the same Merkle Trees to tally the contexts and validate individual ballot receipts, including the voter's.  Once downloaded, the voter can:

- validate their specific CVR remained in tact and is contained in the election
- validate that 99 other CVRs remain in tact and are contained in the election
- tally the contests themselves, reproducing the exact same results as the official election results

The voter can continue to do this as more results are uploaded.

Note that with all the data and code available to the electorate, alternate facts, illegitimate narratives, or other attempts at casting doubt on the election can eventually be publicly shown to be false.  And if either the physical ballots are compromised, or if the live VoteTracker+ data is compromised, or if individual or groups of individual collude and generate false narratives or data, the accuracy or inaccuracy of such data and narratives can be determined transparently and universally among the electorate.  With VoteTracker+ there is no single party that privately determines the accuracy of the VoteTracker+ data.

## 4) Basic Election Official Experience (UX)

VoteTracker+ brings significant election transparency to the entire election process by creating two additional CVR copies of the original paper ballots.  By simply using VoteTracker+ election officials leverage an open source validation of their ballot handling process that has come under increasing partisan attack.  The changes that election officials will witness when using a VoteTracker+ based election and voting system are chronologically summarized as follows.

### 4.1) Pre Election Day Summary

Leading up to the election, election officials can iterate over the ballot design and GGO boundaries similar to standard software development practices.  All changes are authenticated to the person making the change and all changes are run against standard automated tests.  Election officials can validate that every address receives the correct ballot via the GGO automated testing that VoteTracker+ supports.

Once a precinct finalizes a ballot, that ballot becomes available for early voting.  Early ballots can be entered into VoteTracker+ at any time, including prior, during, or after election day as configured by the VoteTracker+ configuration for that election.

### 4.2) Day of Election Summary

1) Depending on the level of adoption of VoteTracker+, all blank ballots can be generated on demand at the voter ID identification station.  There is no need to guess how many blank ballots to print beforehand or which ballots are needed at which voting locations.

2) If fully integrated with election official workflows, VoteTracker+ can independently record the voter ID, specifically only the name and address, independent from the official voter ID record or as the official voter ID record.  This allows each precinct or state to select the voter ID process and record keeping that they so choose.  Selecting VTP as the voter ID record solution is optional but if can be a cost saving measure.  If the voter ID is recorded with VTP, VTP will be able to flag identical names across different addresses across the entire electorate for potential deeper inspection and auditing, not just within the local precinct.  This increased transparency increases trust in the election as it can independently verify truthful election official voter ID activities while exposing fraudulent ones.

3) VoteTracker+ adds the capability of the voter to validate their contest CVRs before the ballot and the CVR are accepted into the election.

4) VoteTracker+ will add a voter approved CVR to the Merkle Tree that is behind VoteTracker+.  A primary property of the Merkle Tree is that it keeps history intact.  It is extremely difficult to thus change history, which includes the changing, inserting, or deleting a ballot.

With the full adoption of VoteTracker+ 2.0, the paper ballot themselves can be cryptographically associated with the ballot digital scam images.  The importance of this step is that each paper ballot is cryptographically connected to the digital scan and with voter's receipt in a specific manner that insures anonymity and election security, preventing fraudulent ballots to be added later or for ballots to be removed or even re-ordered.  Full adoption of 2.0 results three copies of the same data distributed in a specific safe and secure manner between election officials, the ballot scanning hardware manufacturer, and the voter themselves.

### 4.3) Post Election-Day Summary

Once the polls close read-only copies of the VoteTracker+ data, which contain the same Merkle Trees originally created by the election officials augmented with all the CVR submitted by the voters, can be made available.  VTP supports incremental releases to the public of this data at a frequency chosen by election officials.

Thus, the voters themselves can download copies of the election data, validate that their ballots are correctly contained within the elections, and tally all the contests themselves.  This is a game changing capability regarding assessing the accuracy and trustworthiness of election.

## 5) Summary

In summary, VoteTracker+ is a 100% open source election and voting system, operated by election officials while being owned and verified by the people, that increases the security, accuracy, and trustworthiness of a paper ballot election.
