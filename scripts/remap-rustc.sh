#!/usr/bin/env bash
set -euo pipefail
project_root="$(cd "$(dirname "$0")/.." && pwd)"
exec "$@" "--remap-path-prefix=$project_root=/avm-vesting-streams"
