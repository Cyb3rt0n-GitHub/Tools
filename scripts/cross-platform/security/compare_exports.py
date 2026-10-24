"""Compare normalised listener or vulnerability CSV exports offline (Python 3.10+)."""
import argparse
import csv
from datetime import datetime, timezone
import hashlib
import ipaddress
import json
from pathlib import Path


def read_export(path, kind):
    data = Path(path).read_bytes()
    text = data.decode('utf-8-sig')
    fields = ['asset_id', 'protocol', 'address', 'port'] if kind == 'listeners' else ['asset_id', 'finding_id', 'protocol', 'port']
    rows, duplicates = {}, 0
    import io
    reader = csv.DictReader(io.StringIO(text, newline=''), strict=True)
    if not reader.fieldnames or len(set(reader.fieldnames)) != len(reader.fieldnames):
        raise ValueError('Missing or duplicate CSV headers')
    if not set(fields).issubset(reader.fieldnames):
        raise ValueError('Required columns: ' + ', '.join(fields))
    for number, row in enumerate(reader, 2):
        if None in row or any(v is None for v in row.values()):
            raise ValueError(f'Malformed CSV row {number}')
        row = {k: v.strip() for k, v in row.items()}
        for field in fields:
            if not row[field]:
                raise ValueError(f'Row {number}: empty {field}')
        if row['protocol'].lower() not in ('tcp', 'udp', 'host'):
            raise ValueError(f'Row {number}: protocol must be tcp, udp or host')
        row['protocol'] = row['protocol'].lower()
        if kind == 'listeners' and row['protocol'] == 'host':
            raise ValueError(f'Row {number}: listeners require tcp or udp')
        if row['protocol'] == 'host':
            if row['port'] != '-':
                raise ValueError(f'Row {number}: host findings require port -')
        else:
            try: port = int(row['port'])
            except ValueError: raise ValueError(f'Row {number}: invalid port') from None
            if not 1 <= port <= 65535:
                raise ValueError(f'Row {number}: port out of range')
            row['port'] = str(port)
        if kind == 'listeners':
            try: row['address'] = str(ipaddress.ip_address(row['address']))
            except ValueError: raise ValueError(f'Row {number}: address must be a numeric IP (use 0.0.0.0 or :: for wildcard)') from None
        key = tuple(row[f] for f in fields)
        if key in rows:
            if rows[key] != row:
                raise ValueError(f'Row {number}: conflicting duplicate identity; add the missing distinguishing information to your IDs')
            duplicates += 1
        rows[key] = row
    return rows, {'sha256': hashlib.sha256(data).hexdigest(), 'rows': len(rows), 'exact_duplicates': duplicates}


def compare(before, after):
    common = before.keys() & after.keys()
    changed = []
    for key in sorted(common):
        fields = {name: {'before': before[key].get(name), 'after': after[key].get(name)}
                  for name in sorted(before[key].keys() | after[key].keys())
                  if before[key].get(name) != after[key].get(name)}
        if fields:
            changed.append({'identity': list(key), 'fields': fields})
    return {'newly_observed': [after[k] for k in sorted(after.keys() - before.keys())],
            'no_longer_observed': [before[k] for k in sorted(before.keys() - after.keys())],
            'changed_metadata': changed, 'unchanged_count': len(common) - len(changed)}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('kind', choices=['listeners','vulnerabilities'])
    p.add_argument('before'); p.add_argument('after')
    p.add_argument('--scope-id', required=True, help='Operator assertion that both exports cover the same defined scope')
    p.add_argument('--before-at', required=True, help='ISO 8601 collection time including timezone')
    p.add_argument('--after-at', required=True)
    a = p.parse_args(argv)
    try:
        times = [datetime.fromisoformat(v.replace('Z','+00:00')) for v in (a.before_at,a.after_at)]
        if any(t.tzinfo is None for t in times) or times[1] <= times[0] or not a.scope_id.strip():
            raise ValueError('Use timezone-aware increasing collection times and a nonempty scope ID')
        before, bm = read_export(a.before,a.kind); after, am = read_export(a.after,a.kind)
        report = compare(before,after)
        report.update({'schema':1, 'kind':a.kind, 'scope_id':a.scope_id,
                       'generated_at':datetime.now(timezone.utc).isoformat(),
                       'before':dict(bm,collected_at=times[0].isoformat()),
                       'after':dict(am,collected_at=times[1].isoformat()),
                       'interpretation':'Observation differences only. Absence does not prove remediation, service removal or lack of exposure. Verify scope, collection success and independent evidence.'})
        print(json.dumps(report,indent=2,ensure_ascii=False))
        return int(any(report[k] for k in ('newly_observed','no_longer_observed','changed_metadata')))
    except (OSError,ValueError,csv.Error) as exc:
        p.exit(2,f'Error: {exc}\n')


if __name__ == '__main__':
    raise SystemExit(main())
