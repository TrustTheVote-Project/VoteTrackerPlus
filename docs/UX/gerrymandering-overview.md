GERRYMANDERING UX

The gerrymandering UX is basically via the end voter web portal in the VOTES SaaS implementation for the election.  Note - each VOTES election is a separate URL.  The voter portal is public and though only available via https, there are no user logins or passwords - there is no webportal private user data stored.

Note - the web portal is immunized against bots and web crawlers.  The web portal also carries a EULA prohibiting the use of the site for the purchase and sale of either ballot or voter-id data.  It also prohibits the export of either data (of either repo) out of the country of origin (similar to the VOTES voter EULA).

The voter portal is basically a lightweight wrapper around the already publicly available VOTES ballot and voter-id repo, basically allowing a user to enter either an address or a ballot digest.  Entering an (arbitrary) ballot digest takes the end user to that ballot.

After entering an (arbitrary) address, the user is taken to a gerrymandering page that describes various aspects of how potential ballot selections have been affected by the various GGO boundaries that have the potential for being affected by Gerrymandering.  For example, for a federal or state races, a specific address can be up-valued or down-valued depending on how the districting has been laid out - these values are presented to the user.

In addition, the gerrymandering page can display different potential boundaries for the GGO and display the associated up/down valuations and resulting party-level representation at that GGO.
