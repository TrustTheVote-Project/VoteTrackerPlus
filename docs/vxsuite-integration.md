# Integrating VoteTracker+ with VxSuite: Initial Findings and Open Questions

Status: early draft for discussion. Nothing has been implemented yet.

## Goal

Make ballots cast on [VxSuite](https://github.com/OpenVotingTechnologyGroup/vxsuite) (our verbatim fork of the VotingWorks paper-ballot system) trackable by the voter using VoteTracker+ (VTP). When a voter casts a ballot on VxSuite equipment, VTP records the vote and hands the voter a ticket. The voter can use the ticket later to confirm their vote was cast and counted as intended.

## Findings

### VTP side

The core step is `AcceptBallotOperation` in [src/vtp/ops/accept_ballot_operation.py](../src/vtp/ops/accept_ballot_operation.py):

- It takes a cast ballot as JSON in VTP's own format, validated against the VTP ElectionData.
- Each contest on the ballot is committed as its own git commit on its own branch. The commit's SHA is the voter's digest for that contest, so **a ballot with N contests yields N SHAs**.
- It builds the voter's receipt: a table with one column per contest and `BALLOT_RECEIPT_ROWS` (100) rows of digests. One randomly chosen row holds the voter's own SHAs; the other 99 rows are other voters' not-yet-merged CVR digests, so the receipt alone does not reveal which row is the voter's.
- Optionally (`version_receipts`) the receipt is itself committed, and a QR code is generated that points to that receipt commit (`show-commit.html?digest=<receipt SHA>`).
- It returns the receipt (2-D list), the voter's row number, the QR code (base64 SVG), and the receipt digest.

[VTP-web-api](https://github.com/OpenVotingTechnologyGroup/VTP-web-api) already exposes this over HTTP, including `POST /web-api/cast_ballot`, `GET /web-api/verify_ballot_receipt/...`, `GET /web-api/verify_ballot_row/...` and `GET /web-api/tally_contests/...`.

### VxSuite side

- Our fork currently has zero commits on top of upstream VotingWorks `main`.
- The natural integration point is **VxScan**, the precinct scanner the voter feeds their paper ballot into. When a sheet is accepted, the `accepted` state of the scanner state machine calls `recordScannedSheet()` in [`apps/scan/backend/src/scanner.ts`](https://github.com/OpenVotingTechnologyGroup/vxsuite/blob/main/apps/scan/backend/src/scanner.ts). That stores the interpreted sheet and queues its cast vote record (CVR) for export.
- VxSuite includes a thermal printer library (`libs/fujitsu-thermal-printer`), so a ticket could be printed at the scanner.
- VxSuite is TypeScript/Node; VTP is Python.

## Proposed approach

1. **Run VTP as a local sidecar service.** The scanner backend calls VTP-web-api over HTTP rather than embedding Python in VxSuite.
2. **Translate the election definition.** Before an election, generate the VTP ElectionData (config/address map YAML, contests, blank ballots) from the VxSuite election definition.
3. **Hook VxScan's accept step.** After `recordScannedSheet()`, convert the interpreted votes into VTP cast-ballot JSON, call VTP accept-ballot, and receive the SHAs, receipt, row number and QR code.
4. **Give the voter a ticket.** Print (or display) the voter's SHAs and/or the QR code.
5. **Verification stays on the VTP side.** The existing VTP-web-client and web API already handle receipt verification and tallies.

## Open questions

1. **No receipt for early voters.** VTP skips the receipt until each contest has at least 100 other unmerged CVRs. The first voters at a location would get no ticket. How should that be handled?
2. **Ballot privacy.** VxSuite deliberately avoids revealing the order in which ballots were cast (for example, sheet IDs are kept out of logs). Do VTP's per-contest git commits, branch names and receipts preserve that property when driven from a scanner?
3. **SHA-1.** Digests are git commit hashes. The mock election repos use git's default object format, SHA-1 (`git rev-parse --show-object-format` returns `sha1`), which is considered weak. Should election repos be created with `--object-format=sha256`?
4. **One SHA per contest or per voter?** The current design gives one SHA per contest. Is that the intended ticket, or should a voter get a single digest per ballot?
5. **What goes on the ticket?** Options: the voter's SHAs (possibly shortened), the QR code, the row number, or the full 100-row receipt. The full table is too large for a thermal printer and would need to be viewed online.
6. **Ballot data coverage.** Can VTP's cast-ballot JSON represent everything VxSuite's interpreter produces, including write-ins, overvotes/undervotes and ranked-choice contests?
7. **Latency.** accept-ballot performs several git commits and pushes per ballot. Should this run in the background, or block the "ballot accepted" screen until the ticket is ready?
8. **Scope.** VxScan only, or also VxMark/VxMarkScan (ballot-marking devices) and VxCentralScan (mail-in/absentee batches, where there is no voter present to hand a ticket to)?
9. **Licensing.** VxSuite is GPL-3.0-only; VTP is GPL-2.0-or-later. These are compatible if the combined work is distributed under GPL v3. Is that acceptable?

## Next steps

- Agree on answers to the open questions above.
- Map the VxSuite election definition to VTP ElectionData for one mock election.
- Prototype the VxScan → VTP-web-api call against a mock election, without printing.
