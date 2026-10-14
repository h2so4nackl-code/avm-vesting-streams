#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
sdk="${1:-$root/.runtime/avm-sdk-linux-x86_64}"
optimizer="${2:-$root/.runtime/binaryen-version_133/bin/wasm-opt}"
sdk="$(cd "$sdk" && pwd)"
cd "$root"
mkdir -p evidence
rustc --version
python3 scripts/runtime_info.py --sdk "$sdk"
rustfmt --edition 2021 --check core/src/lib.rs contracts/vesting/src/lib.rs contracts/receiver/src/lib.rs tests/src/lib.rs tests/tests/regressions.rs
python3 scripts/oracle.py --check
python3 scripts/verify_vendor.py
cargo clippy --workspace --all-targets --locked --offline -- -D warnings 2>&1 | tee evidence/clippy-native.txt
cargo test --workspace --locked --offline 2>&1 | tee evidence/native-tests.txt
bash scripts/build.sh "$sdk" "$optimizer"
for contract in vesting receiver; do
  cargo clippy -p "avm-stream-$contract" --target wasm32-unknown-unknown --locked --offline -- -D warnings 2>&1 | tee "evidence/clippy-wasm-$contract.txt"
done
python3 scripts/e2e.py --sdk "$sdk"
python3 scripts/verify_artifacts.py
python3 scripts/summarize.py
echo "All vesting stream checks passed."
