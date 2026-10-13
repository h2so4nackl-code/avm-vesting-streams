#!/usr/bin/env python3
"""Check unchanged upstream SDK bytes against the recorded source manifest."""
import hashlib
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
for line in (ROOT/'vendor/SHA256SUMS').read_text().splitlines():
    expected, name = line.split('  ', 1)
    assert hashlib.sha256((ROOT/'vendor'/name).read_bytes()).hexdigest() == expected, name
print('Vendored SDK source hashes: PASS')
