"""Restore losslessly packaged source CSVs and verify their original SHA-256."""
from pathlib import Path
import gzip
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def main():
    records = json.loads((ROOT / 'large_sources.json').read_text(encoding='utf-8'))
    for record in records:
        target = ROOT / record['original_path']
        archive = ROOT / record['archive_path']
        if target.exists():
            if digest(target) != record['original_sha256']:
                raise RuntimeError(f'Refusing to overwrite modified source: {target}')
        else:
            if digest(archive) != record['archive_sha256']:
                raise RuntimeError(f'Archive checksum mismatch: {archive}')
            temporary = target.with_suffix(target.suffix + '.restoring')
            with gzip.open(archive, 'rb') as src, temporary.open('wb') as dst:
                shutil.copyfileobj(src, dst)
            if digest(temporary) != record['original_sha256']:
                raise RuntimeError(f'Restored checksum mismatch: {temporary}')
            temporary.replace(target)
        print(f"Verified {record['original_path']}")

if __name__ == '__main__':
    main()
