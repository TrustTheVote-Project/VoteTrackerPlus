# An Informal Description of the Security Model of VOTES

## 1) Terminology

For definitions and technical terms, please refer to [NIST Glossary](https://pages.nist.gov/ElectionGlossary/)

## 2) What does this page cover?

This page describes a high-level summary of the security model presented by VOTES.  For ease of understanding, the VOTES [Attack Surface](https://en.wikipedia.org/wiki/Attack_surface) is divided into three security domains:

- Data-at-Rest security
- Data-at-Update security
- Data-in-Movement security

## 3) What does this page not cover?

Lots.  This page is a selective slice of the VOTES workflows from a cryptographic point of view, covering the general high level security model and [Attack Surface](https://en.wikipedia.org/wiki/Attack_surface).  Other pages describe the various technologies, high / low level descriptions, User eXperiences, and workflows that comprise VOTES.

## 4) VOTES is not introducing a new cryptographic protocol

VOTES is not introducing a new cryptographic protocol, such as say homomorphic encryption as with election systems such as [ElectionGuard](https://www.electionguard.vote/), that needs to be designed, vetted, and built.  VOTES leverages already in-play and existing security protocols for all three security domains - data-at-rest, data-at-update, and data-in-movement.  VOTES does add at the VOTES application level, which is on top of third-party applications that are built on already vetted [PKI](https://en.wikipedia.org/wiki/Public_key_infrastructure) and [PGP](https://en.wikipedia.org/wiki/Pretty_Good_Privacy) security models, additional security features, such as [2FA](https://en.wikipedia.org/wiki/Multi-factor_authentication), as a way to increase tamper-resistance and prevent accidental corruption and adversarial attacks.

## 5) The VOTES Attack Surface - a Three-way Decomposition

### 5a) Data-at-Rest

VOTES leverages [Git](https://git-scm.com/) as the [Merkle Tree](https://en.wikipedia.org/wiki/Merkle_tree) engine in which to store both the VOTES software applications, blank ballot information, as well as the [cast vote records](https://pages.nist.gov/ElectionGlossary/#cast-vote-record).  VOTES does this by storing the individual precinct data in precinct *owned* repos that are configured as [git submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules) into the parent git repo that is effectively *running the election*.  All the repos Git are configured to only use [SHA-265 commit digests](https://github.com/git/git/blob/master/Documentation/technical/hash-function-transition.txt).  In addition the Git hosting service is configured to require all commits to have valid  [GPG](https://docs.github.com/en/github/authenticating-to-github/managing-commit-signature-verification/about-commit-signature-verification) keys.

At rest, the git repositories are protected from tampering both via the nature of the SHA-256 Merkle Tree as well as the git hosting service protecting the git repositories at rest.  Since the repositories are publicly available, each voter can have their own complete copy as well.  Note that VOTES repositories contain both the VOTES programs, such as those used to tally the votes for the specific election associated with the specific set of VOTES repositories, as well as the cast vote records.  All VOTES programs are written in python as source code and include all CI/CD pipeline code such that every voter can inspect and comment on all aspects of the VOTES programs.

### 6a) Data-at-Update


