# VOTES

A Verifiable Open Technology Election System

# 1) Overview of VOTES

VOTES is a distributed, open-source project aimed at increasing the security, accuracy, and trustworthiness of paper ballot elections by:
- giving cryptographically anonymized ballot receipts back to the voter
- providing each voter full access to all the anonymous ballot data and election software
- allowing each voter to individually execute the tally and inspect voter rolls

It is a fully open source [election](https://en.wikipedia.org/wiki/Election) and [voting](https://en.wikipedia.org/wiki/Voting) solution and framework.  As a framework VOTES includes the complete historical software provenance of all the software and ballot data changes pre election as well as all the recording of the CVR of the election itself.  As a direct solution VOTES is immediately usable in any public or private election.  Each pre election software change, either code or ballot data, is authenticated and tracked and automatically run through a fully automated DevSecOps CI/CD pipeline prior.  Each election recording of either the voter ID or their anonymous CVR is also authenticated and tracked.

VOTES is also 100% non-partisan.  It is based on accuracy and transparency.  As long as any sectarian/partisian segment of the population believes in accuracy and transparency, any such segment will be able to accept a valid VOTES backed election or be able to demonstrate publicly and transparently its inaccuracy.

One key unique and key aspect of VOTES is that it offers to the voter a special ballot receipt that contains an anonymous piece of the live local CVR data cryptographically tied to the specific election being supported by VOTES.  This offers a third voter controlled copy of the election data.

# 2) Basic Voter In-place Experience (UX)

From the voter's point of view, VOTES is primarily a backoffice implementation that generates cryptographic metadata associated with each [Cast Vote Record](https://pages.nist.gov/ElectionGlossary/#cast-vote-record) (CVR) for storing, retrieving, inspecting, and tallying the CVRs.  As such, the voter's current in-place voting experience changes in a few subtle but significant ways.  The following describes these changes in more or less chronological order from current in-place voting experiences.

The first change a voter will notice will be that the paper ballot scanning device contains a display that privately reveals to the user the CVR itself, not the digitial scan of the ballot, prior to the ballot being accepted in the election.  This offers the voter the opportunity to void their physical paper ballot and receive a new blank ballot if they believe their CVR is incorrect.  A voter is free to ignore this step and submit their ballot regardless.

The second change is that once submitted, the voter can optionally receive a printed CVR ballot receipt.  The CVR ballot receipt is cryptographically randomized and anonymized while also containing 99 additional randomized and anonymized CVRs.  Each CVR is further randomized and separated into individual micro CVR per ballot contest.  Essentially, with respect to the ballot receipt each context is separated from the other contests - as if digitally each contest is cut with scissors into its own strip.  This information is presented as 100 rows of micro CVRs.  Each column is a contest and each row is a randomized and anonymized grouping with the exception of the voter's row.

In addition to the printed CVR ballot receipt, the voter also privately views an offset into the 100 rows indicating which specific row is their specific ballot.  There is no way a third party can determine which row is the voters.  However, it is up to the voter to remember their specific row from this point on.  Though the voter's row contains the micro receipts in contest order, the other rows have been randomized on a per row basis such that no row will normally represent any single ballot.

The third change is that prior to leaving the election controlled space of the voting center, the voter can place their CVR ballot receipt on a second and independent VOTES scanner that will inspect their receipt and validate the accuracy of the receipt data against the live local VOTES ballot [Merkle tree](https://en.wikipedia.org/wiki/Merkle_tree).  This would be the initial validation to the voter that their blessed CVR as well as 99 other legitimate ballot CVRs are contained in the local copy of the VOTES repositories.  The CVR ballot receipts remain intact throughout the CVR aggregation process via the local repo Merkle Tree and do not change - they remain intact throughout the election and are contained in the final Merkle tree of the election.

The next three significant changes occur after all the polls close.  Once all the polls close, the election officials can make read-only copies of the VOTES Merkle Tree available for download and inspection via standard GitHub servers as ballots continue to be scanned and CVR data is uploaded.  Voters will be able to download the repositories as they are updated.  Note that the repositories include all the open source software via the same Merkle Trees to tally the contexts and validate individual ballot receipts, including the voter's.  Once downloaded, the voter can:

- validate their specific CVR remained in tact and is contained in the election
- validate that 99 other CVRs remain in tact and are contained in the election
- tally the contests themselves, reproducing the exact same results as the official election results

The voter can continue to do this as more results are uploaded.

In addition, once all the polls close the VOTES voter ID rolls also available by the same GitHub servers.  Voters can download that data and inspect their neighborhood or other neighborhoods for voter id irregularities as a function of name or address.  Any such irregularity can be reported to election officials.

Note that with all the data and code available to the electorate, alternate facts, illegitimate narratives, or other attempts at casting doubt on the election can eventually be publicly shown to be false.  And if either the physical ballots are compromised, or if the live VOTES data is compromised, or if individual or groups of individual collude and generate false narratives or data, the accuracy or inaccuracy of such data and narratives can be determined transparently and universally among the electorate.  With VOTES there is no single party that privately determines the accuracy of the VOTES data.

# 3) Basic Election Official Experience (UX)

VOTES brings significant election transparency to the entire election process by creating two additional CVR copies of the original paper ballots.  By simply using VOTES election officials leverage an open source validation of their ballot handling process that has come under increasing partisan attack.  The changes that election officials will witness when using a VOTES based election and voting system are chronologically summarized as follows.

# 3.1) Pre Election Day Summary

Leading up to the election, election officials can iterate over the ballot design and GGO boundaries similar to standard software development practices.  All changes are authenticated to the person making the change and all changes are run against standard automated tests.  Election officials can validate that every address receives the correct ballot via the GGO automated testing that VOTES supports.

Once a precinct finalizes a ballot, that ballot becomes available for early voting.  Early ballots can be entered into VOTES at any time, including prior, during, or after election day as configured by the VOTES configuration for that election.

## 3.2) Day of Election Summary

First, with VOTES, all blank ballots can be generated on demand at the voter ID identification station.  There is no need to guess how many blank ballots to print beforehand.

Second, VOTES also independently records the voter ID, specifically only the name and address, independent from whatever the election officials are using for voter identification.  This allows each state to select the voter ID process and record keeping that they so choose.  Chossing VOTES as the voter ID framework is optionally.  Regardless, once entered VOTES will be able to flag identical names across different addresses across the entire electorate for potential auditing, not just within the local precinct.  This increased transparency increases trust in the election as it can independently defend truthful election official voter ID activities while exposing fraudulent ones.

Third, VOTES adds the capability of the voter to validate their ballots CVR before the ballot and the CVR are accepted into the election.

Fourth, VOTES will add a voter approved CVR to the Merkle Tree that is behind VOTES.  A primary property of the Merkle Tree is that it keeps history intact.  It is extremely difficult to thus change history, which included the changing, inserting, or deleting a ballot.

In addition the paper ballot is printed with a cryptographic GUID that anonymously links the paper ballot to the digital scan of the ballot created by the ballot scanning manufacturer.  The importance of this step is that each paper ballot is cryptographically marked by VOTES making it extremely difficult for fraudulent ballots to be added later or for ballots to be removed or even re-ordered.  The intent is that the election officials control the paper ballots and the ballot scanning hardware manufacturer owns the digital scans, creating a check and balance.

VOTES also gives the voter a CVR receipt that anonymously and cryptographically contains some of the same information.  This creates a third copy of the data, distributed to the voters themselves.  

## 3.4) Post Election-Day Summary

Once the polls close read-only copies of the VOTES data, which contain the same Merkle Trees originally created by the election officials augmented with all the CVR submitted by the voters, can be made available.  VOTES supports incremental releases to the public of this data.

Thus, the voters themselves can download copies of the election data, validate that their ballots are correctly contained within the elections, and tally all the contests themselves.  This is a game changing capability regarding assessing the accuracy and trustworthiness of election.

# 4) Partisan and Sectarian Responses to VOTES

VOTES is inherently both 100% open source for full transparency and 100% non partisan.  VOTES is about accurate and trustworthy elections and not about advancing any particular political party or other sectarian based agendas.  It does advance partisian voting rights issues.  Thegoal of the Merkle Tree inherent in the design of VOTES is to secure the history of the election as it occurs in real time with enough anonymity and trustworthiness and to distribute the data across all the stake holders.  This distribution of the data as a set of Merkel Trees and in the manner described above maximizes the trustworthiness and accuracy of an election, and is a significant increase in such from current election technologies.

In summay, the 100% open source nature of VOTES in both design and implementation allows any political party that holds accurate and trustworthy elections as a primary goal and requirement of democracy to use, inspect, question, enhance, and trust VOTES.
