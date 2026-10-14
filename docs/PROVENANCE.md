# Tool and source provenance

Current validation uses the published **AVM SDK 0.2.0 / guest SDK 0.1.1** bundle.
Vendored guest source and the unchanged release verifier come from the immutable
SDK commit `0748f4f0767a26da8bc363bcb6b5585539d6970e`; `vendor/SHA256SUMS` checks all
vendored bytes. The guest SDK licence is retained.

The runtime source is `06e96ef71006cca020575cbf35e6b82cc82a324e`. Its exact
release, archive hash, profile and binary hashes are in `PROVENANCE.json`,
`evidence/runtime-build-manifest.json` and `evidence/runtime-v020.json`.
The host builder reports 0.1.0; that is distinct from the bundle version 0.2.0.

Rust/Cargo 1.93.0 and rust-lld are enforced by the official builder, which
compares two clean builds per guest using the reviewed Cargo.lock. SDK 0.2.0
rejects RUSTC_WRAPPER, so no remapping wrapper is used. Per-build compiler/lock
provenance is recorded in `evidence/build-provenance-*.txt`.

Binaryen `version_133` is pinned by archive SHA-256
`2dc9c7813f5375db93d96ead4b78222fcc3e2677bbb832297af4797782a37489`.
It runs twice and compares outputs. Flags and before/after hashes are in
`evidence/optimization.json`; original compiler WASM is retained.

Actual execution evidence is the complete compressed `evidence/avm-e2e.json.gz`.
`avm-e2e-summary.json` and `VALIDATION.json` summarize fresh local accounting and
replay; `artifacts.json` records exports and SHA-256 values. See
[SDK 0.2.0 migration](SDK-020.md) for requirements, state reset scope and limits.

Historical SDK 0.1.0 package rehearsal results are retained under
`evidence/historical-pre020/`; they are not evidence for the current SDK.
