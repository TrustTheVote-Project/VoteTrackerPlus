## VoteTracker+ (VTP) is a 100% open software ballot tracking system that increases the security, accuracy, and trustworthiness of a paper ballot election by cryptographically tracking the [Cast Vote Records](https://pages.nist.gov/ElectionGlossary/#cast-vote-record) associated with paper ballots.

VoteTracker+ provides three core capabilities:

1. Directly supplies a cryptographically anonymized paper ballot receipt back to the voter, allowing the voter to __independently__ validate that their specific ballot has been correctly interpreted, recorded, and tallied as intended.

2. Cryptographically records and seals the entire history of the election as it occurs in a public ledger.

3. Allows the public to inspect and validate the official Cast Vote Records, official tally, and ideally the aggregate voter ID rolls across the entire electorate.

There are two levels of adoption of VoteTracker+ referred to as VTP 1.0 and VTP 2.0.  It is all the same technology but the realities of current election hardware infrastructure, election official training, and end-voter voting experiences suggest that for many parts of the electorate an incremental adoption is needed.  In VTP 1.0 the [Cast Vote Records](https://pages.nist.gov/ElectionGlossary/#cast-vote-record) are digitally signed and entered into a public ledger similar to today's cryptocurrencies.  However, as the voter's ballot needs to remain anonymous, VTP implements this _without_ the private keys associated with cryptocurrencies.  VTP 2.0 integrates the currently public voter ID rolls into a separate public ledger with separate capabilities.  As the initial and primary value proposition concerns VTP 1.0 and not VTP 2.0, the rest of this article focuses on VTP 1.0.

## How does VTP compare with cryptocurrencies and blockchain technology? What is similar, what is different, and why does VTP _ rock_  as a ballot tracking solution while cryptocurrency blockchains do not?

Cryptocurrency blockchain is an ideal solution for managing a public ledger of transactions without the need of a third-party to record and adjudicate the transactions.  The public ledger aspect of cryptocurrencies secures the entire history of all transactions forever.

That __rocks__.

The same is true for the VTP public ledger - it secures the CVR's of all the ballots.  However, where cryptocurrency blockchains need to secure the ownership of a transaction with private keys, in public elections securing the ownership of a ballot is anti-goal - ballots need to anonymous from start to finish.  With VTP the private keys of transaction are completely absent while the public keys and the public ledger remain.

This __rocks__.

Cryptocurrencies also require a distributed ledger so that no one entity needs to be trusted with securing the ledger.  In the case of a public election, a single entity can manage the ledger as long as the ledger can be independently validated _after_ all the polls close as correct without loss of security, accuracy, or trustworthiness.  With VTP the physical ballot receipt that each voter receives contains 100 public keys for 100 ballots, one of which is the voter's.  Even though in the case of VTP the ledger is not distributed and in fact is effectively _owned_ by the single entity running the election, the fact that the voter has 100 transactions that each insures the history of all previous transactions allows each voter to independently validate the single-sourced public ledger.

This is __rocking__.

So, without private keys and the need to mutually validate transactions across a set of independent _coin miners_ as with cryptocurrency blockchains, the need for proof-of-work or proof-of-stake is removed, saving _a lot_ of complexity and electricity.

Additionally, VoteTracker+ has additional code-causes-change aspects regarding running elections.  One out-of-the-box supported feature is Rank Choice Voting ([RCV](https://en.wikipedia.org/wiki/Ranked_voting)).  VTP allows every voter to run the tally of a RCV contest on their private smart device and see and inspect the results of each incremental round.  All the tally software is included in the same ledger that includes the Cast Vote Records allowing voters to understand and independently validate a RCV tally.  As [Danielle Allen](https://scholar.harvard.edu/danielleallen/home) recently [tweeted](https://twitter.com/dsallentess/status/1314373590620536832), Rank Choice Voting is a number one priority to securing a democratic polity.

Yes, this also __rocks__.

So far we have been talking primarily about VTP 1.0.  VTP 2.0 adds a 100% open source public ledger of voter ID records.  These records are solely the names and addresses of the voters in the election and contain no other information, excluding any additional information that election officials may use to identify a voter.  This data is across the entire electorate and can be accessed in real time.  This offers election officials the ability to more securely implement same-day registration if they so choose.  Regardless, it allows every voter to audit the election after all-the-polls close for suspicious identical voters at different addresses, suspicious multiple voters at the same address, or for suspicious voters or addresses either in their own neighborhood or somewhere else.

## Why invest in VoteTracker+

It is the best available technology for tracking paper based ballot elections while being aligned with the most important aspects of securing, stabilizing, and defending our democratic polity.  Period.
