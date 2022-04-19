# VoteTracker+

A Verifiable Open Technology Election System

# 1) Overview of VoteTracker+

VoteTracker+ is a Verifiable Open Technology Election System that increases the security, accuracy, and trustworthiness of a paper ballot election by:

- giving a cryptographically anonymized and secured ballot receipt back to the voter

- allowing each voter to execute the official tally, anonymously inspect their ballot, and to inspect the public voter ID rolls

- cryptographically recording the history of the election as it occurs in real time, prior to, during, and after election day

VoteTracker+ is a fully open source [election](https://en.wikipedia.org/wiki/Election) and [voting](https://en.wikipedia.org/wiki/Voting) solution and framework.  As a framework VoteTracker+ includes the complete historical software provenance of all the software and ballot data changes pre election as well as all the [Cast Vote Records](https://pages.nist.gov/ElectionGlossary/#cast-vote-record) (CVRs).  As a direct solution VoteTracker+ is immediately usable in any public or private election.  Each pre election software change, either code or ballot data, is authenticated and tracked and automatically run through a fully automated DevSecOps CI/CD security pipeline.  During an election each CVR is added to this same provenance in a cryptographically secure and anonymous manner.

# 2) Why is VoteTracker+ non partisan and non sectarian while being accurate and trustworthy?

First, VoteTracker+ is 100% open source - it is owned and verified by the people even when operated by a small number of representatives of the people.  VoteTracker+ is about accurate and trustworthy elections and not about advancing any particular political or sectarian agenda.  It applies technology and cryptography to validate the full history of events that occur prior to, during, and after election day.  VoteTracker+ records history as it happens in an anonymous and cryptographically sound and sealed manner.  It records the change history of all the software used in the election as well as all the CVRs (the interpreted ballots) and public voter ID roll information.  Similar but very different to block chain technologies that ensure the legitimacy and accuracy of cryptocurrency transactions, VoteTracker+ supplies a greater guarantee and degree of trust due to the details of the additional cryptographic checks and balances within VoteTracker+ and the distributed nature of the inherent [Merkle tree](https://en.wikipedia.org/wiki/Merkle_tree).

As long as any partisan segment of the population believes in accuracy and transparency first, such groups will eventually be able to either publicly demonstrate the inaccuracy of the election or have an partisan independent and transparent proof that the election was trustworthy.  VoteTracker+ adds significant checks and balances above and beyond Risk Limiting Audits and paper ballot recounts.

One unique and key aspect of VoteTracker+ is that it offers to the voter a special ballot paper receipt that contains a cryptographically sealed and anonymous slice of the specific live and local ballot and election data.  This places in the hands of the voter critical evidence of the election as well as their specific ballot all in an anonymous manner.

A second unique and key aspect of VoteTracker+ is that it cryptographically ties the paper ballots with the digitally scanned [ballot images](https://pages.nist.gov/ElectionGlossary/#ballot-image) and with the CVRs such that it is practically impossible to add, change, or drop a paper ballot once it has been scanned.  The same holds true for the scanned ballot image and for paper voter receipt distributed to the voters.

A third unique and key aspect of VoteTracker+ is that with VoteTracker+ every voter can execute the same exact tally that election officials perform.  Whether a specific contest is [plurality](https://en.wikipedia.org/wiki/Plurality_voting), [Rank Choice Vote](https://pages.nist.gov/ElectionGlossary/#ranked-choice-voting), or some other [electoral system](https://en.wikipedia.org/wiki/Electoral_system#Types_of_electoral_systems), all such tallies can be executed and checked by any voter for accuracy.

A fourth unique and key aspect of VoteTracker+ is that the already public voter ID rolls are now made publicly available secured by the same underlying capabilities of a [Merkle tree](https://en.wikipedia.org/wiki/Merkle_tree).  The VoteTracker+ voter ID rolls are available in one place immediately after all the polls close, allowing every voter to validate that there are no fake names or addresses in their neighborhood.  Election officials can now perform risk limiting voter ID audits to determine if anyone is voting in multiple locations or if fake individuals have been allowed to cast a ballot.

# 3) Basic Voter In-place Experience (UX)

From the voter's point of view, VoteTracker+ is primarily a backoffice implementation that generates cryptographic metadata associated with each [Cast Vote Record](https://pages.nist.gov/ElectionGlossary/#cast-vote-record) (CVR) for storing, retrieving, inspecting, and tallying the CVRs.  As such, the voter's current in-place voting experience changes in a few subtle but significant ways.  The following describes these changes in more or less chronological order from current nominal in-place voting experiences.

The first change a voter will notice will be that the paper ballot scanning device contains a display that privately reveals to the user the CVR itself, not the digitial scan of the ballot, prior to the ballot being accepted in the election.  This offers the voter the opportunity to void their physical paper ballot and receive a new blank ballot if they believe their CVR is incorrect.  A voter is free to ignore this step and submit their ballot regardless.

The second change is that once submitted, the voter can optionally receive a printed CVR ballot receipt.  The CVR ballot receipt is cryptographically randomized and anonymized while also containing 99 additional randomized and anonymized CVRs.  Each CVR is further randomized and separated into individual micro CVR per ballot contest.  Essentially, with respect to the ballot receipt each context is separated from the other contests - as if digitally each contest is cut with scissors into its own strip.  This information is presented as 100 rows of micro CVRs.  Each column is a contest and each row is a randomized and anonymized grouping with the exception of the voter's row.

In addition to the printed CVR ballot receipt, the voter also privately views an offset into the 100 rows indicating which specific row is their specific ballot.  There is no way a third party can determine which row is the voters.  However, it is up to the voter to remember their specific row from this point on.  Though the voter's row contains the micro receipts in contest order, the other rows have been randomized on a per row basis such that no row will normally represent any single ballot.

The third change is that prior to leaving the election controlled space of the voting center, the voter can place their CVR ballot receipt on a second and independent VoteTracker+ scanner that will inspect their receipt and validate the accuracy of the receipt data against the live local VoteTracker+ ballot [Merkle tree](https://en.wikipedia.org/wiki/Merkle_tree).  This would be the initial validation to the voter that their blessed CVR as well as 99 other legitimate ballot CVRs are contained in the local copy of the VoteTracker+ repositories.  The CVR ballot receipts remain intact throughout the CVR aggregation process via the local repo Merkle Tree and do not change - they remain intact throughout the election and are contained in the final Merkle tree of the election.

The next three significant changes occur after all the polls close.  Once all the polls close, the election officials can make read-only copies of the VoteTracker+ Merkle Tree available for download and inspection via standard GitHub servers as ballots continue to be scanned and CVR data is uploaded.  Voters will be able to download the repositories as they are updated.  Note that the repositories include all the open source software via the same Merkle Trees to tally the contexts and validate individual ballot receipts, including the voter's.  Once downloaded, the voter can:

- validate their specific CVR remained in tact and is contained in the election
- validate that 99 other CVRs remain in tact and are contained in the election
- tally the contests themselves, reproducing the exact same results as the official election results

The voter can continue to do this as more results are uploaded.

In addition, once all the polls close the VoteTracker+ voter ID rolls also available by the same GitHub servers.  Voters can download that data and inspect their neighborhood or other neighborhoods for voter id irregularities as a function of name or address.  Any such irregularity can be reported to election officials.

Note that with all the data and code available to the electorate, alternate facts, illegitimate narratives, or other attempts at casting doubt on the election can eventually be publicly shown to be false.  And if either the physical ballots are compromised, or if the live VoteTracker+ data is compromised, or if individual or groups of individual collude and generate false narratives or data, the accuracy or inaccuracy of such data and narratives can be determined transparently and universally among the electorate.  With VoteTracker+ there is no single party that privately determines the accuracy of the VoteTracker+ data.

# 4) Basic Election Official Experience (UX)

VoteTracker+ brings significant election transparency to the entire election process by creating two additional CVR copies of the original paper ballots.  By simply using VoteTracker+ election officials leverage an open source validation of their ballot handling process that has come under increasing partisan attack.  The changes that election officials will witness when using a VoteTracker+ based election and voting system are chronologically summarized as follows.

# 4.1) Pre Election Day Summary

Leading up to the election, election officials can iterate over the ballot design and GGO boundaries similar to standard software development practices.  All changes are authenticated to the person making the change and all changes are run against standard automated tests.  Election officials can validate that every address receives the correct ballot via the GGO automated testing that VoteTracker+ supports.

Once a precinct finalizes a ballot, that ballot becomes available for early voting.  Early ballots can be entered into VoteTracker+ at any time, including prior, during, or after election day as configured by the VoteTracker+ configuration for that election.

## 4.2) Day of Election Summary

First, with VoteTracker+, all blank ballots can be generated on demand at the voter ID identification station.  There is no need to guess how many blank ballots to print beforehand.

Second, VoteTracker+ also independently records the voter ID, specifically only the name and address, independent from whatever the election officials are using for voter identification.  This allows each state to select the voter ID process and record keeping that they so choose.  Chossing VoteTracker+ as the voter ID framework is optionally.  Regardless, once entered VoteTracker+ will be able to flag identical names across different addresses across the entire electorate for potential auditing, not just within the local precinct.  This increased transparency increases trust in the election as it can independently defend truthful election official voter ID activities while exposing fraudulent ones.

Third, VoteTracker+ adds the capability of the voter to validate their ballots CVR before the ballot and the CVR are accepted into the election.

Fourth, VoteTracker+ will add a voter approved CVR to the Merkle Tree that is behind VoteTracker+.  A primary property of the Merkle Tree is that it keeps history intact.  It is extremely difficult to thus change history, which included the changing, inserting, or deleting a ballot.

In addition the paper ballot is printed with a cryptographic GUID that anonymously links the paper ballot to the digital scan of the ballot created by the ballot scanning manufacturer.  The importance of this step is that each paper ballot is cryptographically marked by VoteTracker+ making it extremely difficult for fraudulent ballots to be added later or for ballots to be removed or even re-ordered.  The intent is that the election officials control the paper ballots and the ballot scanning hardware manufacturer owns the digital scans, creating a check and balance.

VoteTracker+ also gives the voter a CVR receipt that anonymously and cryptographically contains some of the same information.  This creates a third copy of the data, distributed to the voters themselves.  

## 4.4) Post Election-Day Summary

Once the polls close read-only copies of the VoteTracker+ data, which contain the same Merkle Trees originally created by the election officials augmented with all the CVR submitted by the voters, can be made available.  VoteTracker+ supports incremental releases to the public of this data.

Thus, the voters themselves can download copies of the election data, validate that their ballots are correctly contained within the elections, and tally all the contests themselves.  This is a game changing capability regarding assessing the accuracy and trustworthiness of election.

# 5) Summary

In summary, VoteTracker+ is a 100% open source election and voting system, operated by election officials while being owned and verified by the people, that increases the security, accuracy, and trustworthiness of a paper ballot election.
