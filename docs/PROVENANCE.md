# Tool and source provenance

- Vendored `avm-contract-sdk`: unchanged source from `gosh-sh/avm-sdk` commit
  `72ee42dbf923f081bf29b4a1a1b6ea012b6af54f`. `vendor/SHA256SUMS` records every
  vendored file and the upstream licence. No external Rust registry dependencies.
- Published AVM tool release: `avm-dev-335a0f09fdbc-sdk-0cbca40fad9a`.
  Runtime source: `335a0f09fdbc98eb7a1056c0f6b84cd4f39d889e`; packaged SDK source:
  `0cbca40fad9a8f11863197cbcbaf6208651752b9`.
  Linux x86-64 archive SHA-256:
  `2171ee865bc9fc2e1a1274dfdd0f4330dc362b1f49d38c0a35c4de41aa61d6f3`.
- Rust 1.93.0, `wasm32-unknown-unknown`; release optimization `s`, LTO enabled,
  one codegen unit, panic abort, symbol stripping. `RUSTC_WRAPPER` remaps the
  project path to `/avm-vesting-streams` while preserving the official builder's
  encoded VM flags. The official builder verifies two clean compilations.
- Binaryen `version_133`; Linux archive SHA-256:
  `2dc9c7813f5375db93d96ead4b78222fcc3e2677bbb832297af4797782a37489`.
  The optimizer runs twice and compares bytes; flags and before/after hashes are
  recorded in `evidence/optimization.json`. Compiler artifacts are retained as
  `contract.compiler.wasm`; deployed artifacts are `contract.wasm`.

The vendored SDK is newer than the packaged tool's SDK source. It remains an
explicit path dependency and was tested against the published runtime's canonical
ABI. The current SDK was not substituted into the runtime binary. Actual execution
evidence is `evidence/avm-e2e.json.gz` (gzip-compressed JSON); hashes and exports are `evidence/artifacts.json`.
Install scripts verify archive hashes before extraction.
