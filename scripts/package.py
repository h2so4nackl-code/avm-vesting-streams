#!/usr/bin/env python3
"""Package reviewable sources, verified artifacts, and evidence; no caches."""
from pathlib import Path
import argparse
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parents[1]
def included(path):
    parts = path.relative_to(ROOT).parts
    if '__pycache__' in parts or '.runtime' in parts or '.git' in parts:
        return False
    if parts[0] == 'target':
        return False
    if 'target' in parts:
        return len(parts) == 5 and parts[0] == 'contracts' and parts[2:4] == ('target','avm') and parts[-1] in {
            'contract.wasm','contract.compiler.wasm','contract.acab','contract.descriptor'}
    return path.name != 'SHA256SUMS' or parts[0] == 'vendor'
def run(output):
    journey = json.loads((ROOT/'evidence/avm-e2e.json').read_text())
    assert journey['status'] == 'PASS'
    assert 'All vesting stream checks passed.' in (ROOT/'evidence/full-check.txt').read_text()
    files = sorted(p for p in ROOT.rglob('*') if p.is_file() and included(p))
    manifest = ''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(ROOT).as_posix()+'\n' for p in files)
    (ROOT/'SHA256SUMS').write_text(manifest)
    files.append(ROOT/'SHA256SUMS')
    with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for path in files:
            z.write(path, ROOT.name+'/'+path.relative_to(ROOT).as_posix())
    with zipfile.ZipFile(output) as z:
        assert z.testzip() is None
        for line in manifest.splitlines():
            expected, name = line.split('  ',1)
            assert hashlib.sha256(z.read(ROOT.name+'/'+name)).hexdigest() == expected
    print(json.dumps({'file':str(output),'files':len(files),'bytes':output.stat().st_size,'sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'zip_and_checksums':'PASS'},indent=2))
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=ROOT.parent/'avm-vesting-streams-v1.zip')
    args = parser.parse_args()
    run(args.output.resolve())
