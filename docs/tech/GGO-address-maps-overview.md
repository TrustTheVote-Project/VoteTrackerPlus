Some thoughts on the GGO address map.

It is unclear at this time (more information is needed) if the GGO-address maps are additional and separare repos or not.  If separate repos there will also be git submodules so that they can be properly and securely tracked and managed during an election.

The copy in the repo is currently seen as either a JSON or yaml backup file dump of the GGO address maps.

Each GGO owner is responsible for their GGO-address repo.  The build will check for data consistency of pushes - builds validate data consistency across all repos.

There is a separate app that allows a GGO owner/operator to adjust its boundaries and generate the backup yaml file.  Once generated, the owner/operator can run a build (either locally or remotely - TBD) to validate that the new data is correct.

Note - GGO boundaries (say a town's school district boundary) need not align with other GGO boundaries (a state's political boundary).  But within a similar class of GGO (within the town's school district) the boundaries must align and not drop any address or include an address outside the boundary.  Note - the GGO hierarchy is important in that each outer GGO sets the configuration of the inner GGO's with regards to adherence/restrictions regarding where inner GGO boundaries can go.  This is reflected in tests that are run as part of the build and CI/CO pipeline.

Note - a GGO can have its own source of GGO-address truth and _dump_ the data to VOTES or use VOTES as the source of the truth.
