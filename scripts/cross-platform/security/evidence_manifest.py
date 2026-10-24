"""Snapshot SHA-256 hashes or compare two manifests; Python 3.10+, standard library only."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import stat


def snapshot(root):
    root = Path(root).resolve(strict=True)
    if not root.is_dir():
        raise ValueError('Root must be a directory')
    files, errors, skipped = {}, [], []
    def walk_error(exc):
        errors.append({'path': str(exc.filename), 'error': str(exc)})
    for directory, dirs, names in os.walk(root, followlinks=False, onerror=walk_error):
        base = Path(directory)
        for name in list(dirs):
            if (base / name).is_symlink():
                skipped.append(str((base / name).relative_to(root)))
                dirs.remove(name)
        for name in sorted(names):
            path = base / name
            rel = path.relative_to(root).as_posix()
            try:
                before = path.lstat()
                if not stat.S_ISREG(before.st_mode):
                    skipped.append(rel)
                    continue
                # O_NOFOLLOW protects final-component symlink races where supported.
                fd = os.open(path, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_BINARY', 0))
                with os.fdopen(fd, 'rb') as stream:
                    opened = os.fstat(stream.fileno())
                    if not stat.S_ISREG(opened.st_mode) or (before.st_dev, before.st_ino) != (opened.st_dev, opened.st_ino):
                        raise ValueError('File replaced during collection')
                    digest = hashlib.sha256()
                    while chunk := stream.read(1024 * 1024):
                        digest.update(chunk)
                    after = os.fstat(stream.fileno())
                if (opened.st_size, opened.st_mtime_ns, opened.st_ctime_ns) != (after.st_size, after.st_mtime_ns, after.st_ctime_ns):
                    raise ValueError('File changed during hashing')
                files[rel] = {'sha256': digest.hexdigest(), 'bytes': after.st_size}
            except (OSError, ValueError) as exc:
                errors.append({'path': rel, 'error': str(exc)})
    return {'schema': 1, 'collected_at': datetime.now(timezone.utc).isoformat(),
            'root': str(root), 'files': files, 'errors': errors, 'skipped': sorted(skipped)}


def compare(before, after):
    for manifest in (before, after):
        if manifest.get('schema') != 1 or not isinstance(manifest.get('files'), dict):
            raise ValueError('Unsupported manifest')
        for item in manifest['files'].values():
            if not isinstance(item, dict) or not isinstance(item.get('sha256'), str) or len(item['sha256']) != 64:
                raise ValueError('Invalid digest entry')
    a, b = before['files'], after['files']
    unknown = {e['path'] for m in (before, after) for e in m.get('errors', [])}
    unknown.update(p for m in (before, after) for p in m.get('skipped', []))
    # Incomplete collection must never be treated as proof of deletion.
    incomplete = bool(unknown)
    return {'added': sorted(b.keys() - a.keys()), 'removed': sorted(a.keys() - b.keys()) if not incomplete else [],
            'missing_unconfirmed': sorted(a.keys() - b.keys()) if incomplete else [],
            'changed': sorted(k for k in a.keys() & b.keys() if a[k]['sha256'] != b[k]['sha256']),
            'collection_incomplete': incomplete, 'unknown': sorted(unknown)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    snap = sub.add_parser('snapshot'); snap.add_argument('root'); snap.add_argument('output')
    diff = sub.add_parser('compare'); diff.add_argument('before'); diff.add_argument('after')
    args = parser.parse_args(argv)
    try:
        if args.command == 'snapshot':
            root = Path(args.root).resolve(strict=True)
            out = Path(args.output).resolve()
            if out == root or root in out.parents:
                raise ValueError('Save the manifest outside the collected directory')
            if out.exists():
                raise ValueError('Output already exists')
            result = snapshot(root)
            fd = os.open(out, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(fd, 'w', encoding='utf-8') as stream:
                json.dump(result, stream, indent=2); stream.write('\n')
            return 2 if result['errors'] else 0
        result = compare(json.loads(Path(args.before).read_text(encoding='utf-8')),
                         json.loads(Path(args.after).read_text(encoding='utf-8')))
        print(json.dumps(result, indent=2))
        return 2 if result['collection_incomplete'] else int(any(result[k] for k in ('added','removed','changed')))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(2, f'Error: {exc}\n')


if __name__ == '__main__':
    raise SystemExit(main())
