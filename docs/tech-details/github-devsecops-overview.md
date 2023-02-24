# 1) General GitHub and DevSecOps Overview

The VTP product repositories can be forked at any time from the main branch, after first product ship, to set up an election.  For the purpose of the election, it is the forked copies which are considered to the source of truth regarding the git repositories.  These repositories are never merged back into the VTP product repositories, though it highly likely that patches will flow back both ways as bugs and CVE's are discovered and addressed.

Once forked, the election is configured with the various GGOs (Geopolitical geographical Overlay - NIST calls this a [geopolitical unit](https://pages.nist.gov/ElectionGlossary/#geopolitical-unit)), contests, and blank ballot details.  VTP supports other types of configurations such as the type of tally being used for the contest as well as various VTP internal configurations.

In addition to the configuration data the address maps for each GGO is also added to election VTP repositories.  

The source VTP repositories hosted nominally on GitHub include a complete DevSecOps [CI](https://en.wikipedia.org/wiki/Continuous_integration)/[CD](https://en.wikipedia.org/wiki/Continuous_delivery) pipeline.  It is a TBD whether the native [GitHub Python Pipeline](https://docs.github.com/actions/automating-builds-and-tests/building-and-testing-nodejs-or-python?langId=py) or some other pipeline vendor is used.  Regardless the VTP repositories include [tox](https://tox.wiki/en/latest/) based testing as well as [Sphinx](https://www.sphinx-doc.org/en/master/) based documentation.

The pipeline will nominally test both the VTP internal software as well as the voter facing applications such as contest tallies.  There will also be election configuration and GGO address map testing.

# 2) General Election Pull Request Model

Elections will contain a starting root repo which contains the tally applications and other software.  Depending on the election itself, GGOs that ultimately will be directly collecting, scanning, and counting ballots will have their own git submodule.  One reason for this is the ability to operate in a completely disconnected mode from the internet.  GGOs that are simply contributing contests to a ballot somewhere may or may not have their own git submodule.

Regardless, all the git submodules will be forked in a similar manner to the root repository.  The owning GGOs may or may not set up their own pipelines to test changes before they are pushed.  Regardless, when they create a pull request back into the upstream, the pipelines must pass the change before the pull request can be accepted.  Though not a requirement, it is expected that each change also pass an in depth review process.

Note that all changes need to be PGP signed and that election officials can configure VTP to require various type of [2FA](https://en.wikipedia.org/wiki/Multi-factor_authentication), which can be out-of-band - such as actually talking to the author of the change and/or the GGO owner, potentially through encrypted channels etc.

# 3) A Note on Security

For a general security overview please see the "informal-security-overview.md" document in the docs folder of this repo.  That documents includes an overview of the certificate authority chain that will be set up for a specific election.  All TSL connections will require mutual SSL.

#4) Notes

One major intent and capability of a VTP based election is the DevSecOps model and pipeline that comes with VTP.  The CI/CD pipeline will be in operation from the beginning of an election cycle and includes all the software, configuration, and data entry leading up to the point of verifying the blank ballots.  VTP covers the pre and post election phases as well as the election day.  The pipeline continues to operate to handle bugs, CVEs, and attacks on the election through all phases, including the recording of when a ballot or set of ballorts are removed from the election post their scanning and tally.  This is important so that a voter knows if, when, by whom their ballot is removed from the election.  Note - when a ballot or ballots are removed, not only with the git commit include a PGP signed author of the removal commit, the election official and/or judge or court order is also recorded in the commit.

This transparency is important so to be able to trust an election.

