Some thoughts on the GGO address map.

The GGO-address map repo is text backup yaml file dump of the mapping of addresses to a specific GGO.  It is unclear if this repo is publicly available or not.  It is also unclear if the voter_id repo is publicly available or not.  Only the ballot repo is known to be publicly available as of this writing.

Similar to the ballot repo, the GGO-address map repo is stitched together via a similar mechanism.  Per GGO, each address within the geographical boundary is listed as being present.  The _boundary_ of different GGO classes need not align, but alignment will be one of the live checks when inspecting/loading/reviewing GGO address boundaries.

Each GGO owner is responsible for their GGO-address repo.  The build will check for data consistency of pushes - builds validate data consistency across all repos.

There is a separate app/service (if service, the SaaS provider will supply the service) that allows a GGO owner/operator to adjust its boundaries and generate the backup yaml file.  Once generated, the owner/operator can run a build (either locally or remotely - TBD) to validate that the new data is correct.  Once validated, the election owner (SaaS entity - TBD) can accept the fork, updating the master (or whatever) branch.

Thus a class of GGO boundaries (say a town's school district boundary) need not align with other GGO boundaries (a state's political boundary).  But within the class (within the town's school district) the boundaries must align and not drop any address or include an address outside the boundary.  Note - the GGO hierarchy is important in that each outer GGO sets the configuration of the inner GGO's with regards to adherence/restrictions regarding where inner GGO boundaries can go (which is reflected in tests that are run as part of the build).

A GGO can have its own source of GGO-address truth and _dump_ the data to VOTES or use VOTES as the source of the truth.

Tech note - the above may all be moot - it might be the case that the GGO-address repo is just data without any validation - it might just be GGO contained addresses.  The build may just construct the ballot and determine using open maps (or something)  characteristics based on all the ballots (some graph/geometry theory here).  Such as flag when there are holes or non contiguous ballots.

