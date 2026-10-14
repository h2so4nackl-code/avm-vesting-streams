# SDK integration candidate

The project is intended to become an `examples/vesting-streams` directory in
`gosh-sh/avm-sdk`. For a future integration, retain this nested workspace and
replace the vendored SDK path dependencies: from `core`, use
`../../../crates/avm-contract-sdk`; from `contracts/vesting` and
`contracts/receiver`, use `../../../../crates/avm-contract-sdk`. Do not copy or modify the
upstream SDK implementation. Adjust workspace inheritance and the licence path,
then rerun the complete native, WASM, packaged build, and actual stand gate.

Useful regressions introduced here include full-range time-based accrual, cliff
catch-up, stepped terminal remainder, cancellation while payout is pending,
independent beneficiary and refund callbacks, exact failed-payment principal
return, nonce/time replay checks, and native sixteen-lane concurrency.

The actual stand uses explicit deterministic timestamps. Its first publication
initializes receiver authority as `developer`, whereas vesting initialization
in this journey uses `package-owner`. The test reads actual receiver owner state
and configures the vesting owner separately; publisher and account-owner identities
must not be assumed interchangeable.

Canonical method and event identifiers come from the official ACAB output,
not hand-chosen numbers. `scripts/sync_ids.py --check` verifies them. When metadata
is intentionally changed, first build metadata, regenerate identifiers using
`python3 scripts/sync_ids.py`, and rebuild before running the full gate.

This archive is a standalone candidate. It does not claim an upstream PR,
maintainer review or bounty acceptance for this third project.

## SDK 0.2.0

See [the standalone compatibility result](SDK-020.md). In-tree integration must
use the current SDK path dependency and reviewed lock, without RUSTC_WRAPPER.
The existing upstream integration PR is #11. Its approval and validation
are separate from these standalone checks.
