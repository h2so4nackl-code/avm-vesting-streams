# AVM Vesting Streams

A Rust AVM reference application for scheduled grants, contributor payments, and
token vesting. One funded contract manages up to eight independent streams with
immutable recipients, cliffs, linear or stepped accrual, and optional cancellation.
Designed as an SDK example and regression-suite candidate.

## Behavior

- The owner funds the exact aggregate grant amount once, before the earliest start.
- Each beneficiary signs to claim their newly accrued entitlement. Principal goes
  to the fixed payout address; callers cannot redirect it.
- A cliff gates the entire grant until its timestamp, then catches up from the
  start. Stepped schedules release complete intervals and the remainder at the end.
- Optional owner cancellation freezes earned rights. Beneficiaries keep the earned
  part; the owner can return only the unearned part to the fixed refund address.
- Every stream has separate beneficiary and refund lanes. One pending lane does
  not block other streams or the opposite lane.
- Successful native callbacks settle principal once. Failed delivery must return
  the exact principal before that lane can retry. Receipts bind source, method,
  causal logical time, and, on success, the exact nonce and payment body.
- Arithmetic supports the full `u128` range without multiplying amount by time
  in `u128`. State stays bounded across repeated claims and retries.

## Verified local journey

The actual AVM journey deploys one vesting account and six bound receiver accounts.
It funds three grants, checks unauthorized and premature claims, rejects and retries
a beneficiary payment, cancels two streams, rejects and retries a refund, and finishes
an irrevocable stream. Final receiver totals are:

| Stream | Funded | Beneficiary received | Refund received |
| --- | ---: | ---: | ---: |
| Linear, cancelled | 1,000 | 400 | 600 |
| Stepped, cancelled | 600 | 400 | 200 |
| Irrevocable | 300 | 300 | 0 |
| Total | 1,900 | 1,100 | 800 |

No principal remains held or pending. The queue is empty and journal replay matches
account and registry roots, accepted-input count, and cumulative fees. These are
local main-value units, not a live NACKL payment or bounty award.

## Validation and reproduction

Requirements: Linux x86-64 (Windows: WSL2), Bash, Python 3, curl, and rustup.
Dependencies are vendored; Rust checks and builds run offline after tool installation.

```bash
rustup toolchain install 1.93.0 --profile minimal --component rustfmt --component clippy
rustup target add wasm32-unknown-unknown --toolchain 1.93.0
bash scripts/install_runtime.sh
bash scripts/install_binaryen.sh
bash scripts/check.sh
```

`check.sh` verifies formatting, source hashes, the seeded independent Python oracle,
native and WASM Clippy, 60 application regressions and 12 SDK tests, official
reproducible builds, canonical identifiers, two matching optimizer outputs, WASM
exports without host imports, and the actual local stand journey. One regression
checks 1,200 bigint oracle cases; another exercises 14,400 generated state transitions.
Sixteen simultaneous pending lanes and reverse settlement are native regressions;
the actual stand journey automatically drains its delivery queue.

Included local results are in [`evidence/`](evidence/). The full local journal is
compressed as `avm-e2e.json.gz`; `avm-e2e-summary.json` provides the final accounting.
The workflow generates a fresh uncompressed journal and uploads all results as an
Actions artifact. Check [GitHub Actions](https://github.com/h2so4nackl-code/avm-vesting-streams/actions)
for the current hosted CI result.

## Scope

Recipients must be distinct accounts in the same DApp. The receiver is a bound
testing fixture that retains payments; it is not a general wallet or withdrawal
adapter. Missing callbacks keep the affected lane pending, because unlocking it
without an authentic outcome could permit double payment. Receipt checks rely on
AVM-native callback authenticity and queue replay protection, not on resistance
to arbitrary forged VM headers. SHELL operating funds are separate from principal.

See [the protocol specification](docs/SPEC.md), [provenance](docs/PROVENANCE.md),
and [SDK integration notes](docs/SDK-INTEGRATION.md). Project code is MIT licensed;
the unchanged vendored SDK retains its upstream licence.
