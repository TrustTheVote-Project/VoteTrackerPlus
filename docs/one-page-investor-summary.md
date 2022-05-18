## VoteTracker+ (VTP) is a 100%  open software ballot tracking system that increases the security, accuracy, and trustworthiness of a paper ballot election by cryptographically tracking the [Cast Vote Records](https://pages.nist.gov/ElectionGlossary/#cast-vote-record) associated with paper ballots.

VoteTracker+ provides three core capabilities:

1. Directly supplies a cryptographically anonymized paper ballot receipt back to the voter, allowing the voter to __independently__ validate that their specific ballot has been correctly interpreted, recorded, and tallied as intended.

2. Cryptographically records and seals the entire history of the election as it occurs.

3. Allows the public to inspect and validate the official Cast Vote Records and tally as well as (ideally) the aggregate voter ID rolls across the entire electorate.

There are two levels of adoption of VoteTracker+ referred to as VTP 1.0 and VTP 2.0.  It is all the same technology but the realities of current election hardware infrastructure, election official training, and end-voter voting experiences suggest that for many parts of the electorate an incremental adoption needs to be fully supported option.  At a 1.0 adoption level the [Cast Vote Records](https://pages.nist.gov/ElectionGlossary/#cast-vote-record) are digitally signed and entered into a public ledger similar to today's cryptocurrencies.  However, as the voter's ballot needs to remain anonymous, VoteTracker+ implements this __without__ the privates keys associated with cryptocurrencies.  Once there are no private keys, the need for the ledger to be publicly distributed for the purpose of validating the transaction _at the time of transaction_ is removed __IF__ the public ledger can be valadated after the fact, after the close of the election.  This is the case with VoteTracker+ as the public ledger is publicly available _after_ all the polls have closed and no more ballots can be cast.

## How does VTP compare with cryptocurrencies and blockchain technology?  What is similar, what is different, and why does VoteTracker+ __rock__ as a ballot tracking solution while cryptocurrency blockchains do not?

Cryptocurrency blockchain is an ideal solution for a managing a public ledger of transactions without the need of a third-party to record and adjudicate transactions at a future time.  The public ledger aspect of cryptocurrencies secures the entire history of all transactions forever.

The same is true for the VoteTracker+ public ledger - it secures the CVR's of all the ballots.  However, where cryptocurrency blockchains need to secure the ownership of a transaction, in public elections securing the ownership of a ballot is anti-goal - ballots need to anonymous from start to finish.  With VTP the private keys of transaction are removed.

Cryptocurrencies also require a distributed ledger so that no one entity needs to be trusted with securing the ledger.  In the case of a public election, the requirement can more precisely be defined that the ledger only needs to be validated as correct without loss of security, accuracy, or trustworthiness.  With VTP the physical ballot receipt that each voter receives contains 100 public keys for 100 ballots, one of which is the voter's.  Even though in the case of VTP the ledger is not distributed and in fact is effectively _owned_ by the single entity running the election, the fact that the voter has 100 transactions that each insures the history of all previous transaction allows each voter to independently validate the single-sourced public ledger.

This __rocks__.

And without private keys and the need to mutually validate transactions across a set of independent _miners_ as with cryptocurrency blockchains, the need for proof-of-work or proof-of-stake is removed.  Saving _a lot_ of complexity and electricity.

This also __rocks__.

And so far we are talking primarily just about VoteTracker+ 1.0.

VoteTracker+ 2.0 adds a 100% open source public ledger of voter ID records.  These records are solely the names and addresses of the voters in the election and contain no other information, excluding any additional information that election officials may use to identify a voter.  This data is across the entire electorate and can be accessed in real time.  This offers election officials the ability to more securely implement same-day registration if they so choose.  Regardless, it allows every voter to audit the election after all the polls close for suspicious identical voters at different addresses or suspicious multiple voters at the same address, or for suspicious voters or addresses, either in their own neighborhood or somewhere else.

Yes, this also __rocks__.

As a final note, VoteTracker+ has many other key aspects regarding running elections.  One is that out of the box it supports Rank Choice Voting ([RCV](https://en.wikipedia.org/wiki/Ranked_voting)) allowing every voter to run the tally of a RCV contest and see the results of each round.  All the tally software is included the same ledger that includes the Cast Vote Records allowing voters to understand and independently validate a RCV tally.  As [Danielle Allen](https://scholar.harvard.edu/danielleallen/home) of the [Democratic Knowledge Project](https://www.democraticknowledgeproject.org/) espouses as with many others, Rank Choice Voting is a numnber one priority to securing a democratic polity.

## Why should investors invest in VoteTracker+

Investors should invest in VoteTracker+ for all of the above reasons.  It is the best available technology for tracking paper based ballot elections while being aligned with the most important aspects of securing, stabilizing, and defending our democratic polity.
