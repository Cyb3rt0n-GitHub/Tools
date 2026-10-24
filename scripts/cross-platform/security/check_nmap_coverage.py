"""Check saved TCP Nmap XML against an exact IP/port scope. Offline, Python 3.10+."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import ipaddress
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET


def ports(spec):
    result = set()
    for item in spec.split(','):
        if not re.fullmatch(r'\d+(?:-\d+)?', item):
            raise ValueError('Ports must be comma-separated integers/ranges')
        bounds = item.split('-'); low, high = int(bounds[0]), int(bounds[-1])
        if not 1 <= low <= high <= 65535:
            raise ValueError('Port outside 1–65535 or reversed range')
        result.update(range(low,high+1))
    return result


def targets(path):
    result = []
    for line in Path(path).read_text(encoding='utf-8-sig').splitlines():
        line = line.split('#',1)[0].strip()
        if not line: continue
        if '%' in line: raise ValueError('Scoped IPv6 addresses are unsupported')
        result.append(str(ipaddress.ip_address(line)))
    if not result or len(result) != len(set(result)):
        raise ValueError('Target file must contain unique explicit IPs, one per line')
    return set(result)


def inspect(path, expected_ports):
    path = Path(path)
    if path.stat().st_size > 20 * 1024 * 1024:
        raise ValueError('XML exceeds 20 MiB per-file limit')
    data = path.read_bytes()
    if len(data) > 20 * 1024 * 1024:
        raise ValueError('XML exceeds 20 MiB per-file limit')
    # Limit supported input to UTF-8/ASCII so declaration checks cannot be bypassed by UTF-16.
    data.decode('utf-8-sig')
    if b'\x00' in data: raise ValueError('NUL/UTF-16 XML is unsupported')
    # Accept normal Nmap's simple DOCTYPE, never entity declarations or external DTDs.
    if b'<!ENTITY' in data.upper() or re.search(br'<!DOCTYPE(?!\s+nmaprun\s*>)[^>]*',data,re.I):
        raise ValueError('XML entities and nonstandard/external DTDs are unsupported')
    doc = ET.fromstring(data)
    if doc.tag != 'nmaprun' or doc.get('scanner') != 'nmap':
        raise ValueError('Expected an Nmap XML document')
    issues = []
    finished = doc.find('runstats/finished')
    if finished is None or finished.get('exit') != 'success':
        issues.append('Missing successful runstats/finished')
    infos = doc.findall('scaninfo')
    if len(infos) != 1 or infos[0].get('protocol') != 'tcp':
        issues.append('Requires exactly one TCP scaninfo; mixed protocols unsupported')
    else:
        declared = ports(infos[0].get('services',''))
        if declared != expected_ports:
            issues.append('Declared port set differs from intended ports')
        if int(infos[0].get('numservices','-1')) != len(declared):
            issues.append('scaninfo numservices differs from declared port count')
    observations = []
    for host in doc.findall('host'):
        problems = []
        addresses = [str(ipaddress.ip_address(a.get('addr',''))) for a in host.findall('address')
                     if a.get('addrtype') in ('ipv4','ipv6')]
        if len(addresses) != 1:
            raise ValueError('Expected one IP address per host element')
        address = addresses[0]
        status = host.find('status')
        if status is None or status.get('state') != 'up':
            problems.append('Host not reported up; intended TCP coverage unconfirmed')
        if host.get('timedout','false').lower() not in ('false','0'):
            problems.append('Host timed out or has an unknown timeout flag')
        explicit = set(); counts = Counter(); open_ports = []
        port_section = host.find('ports')
        if port_section is None:
            problems.append('Missing ports section')
        else:
            for item in port_section.findall('port'):
                number = int(item.get('portid','-1'))
                if item.get('protocol') != 'tcp' or number not in expected_ports:
                    problems.append('Unexpected protocol or explicit port')
                if number in explicit: problems.append('Duplicate explicit port')
                explicit.add(number)
                state = item.find('state')
                value = state.get('state') if state is not None else None
                if value not in ('open','closed','filtered','unfiltered','open|filtered','closed|filtered'):
                    problems.append('Missing/unsupported port state')
                counts[value or 'unknown'] += 1
                if value == 'open': open_ports.append(number)
            extra_count = 0
            for extra in port_section.findall('extraports'):
                count = int(extra.get('count','-1'))
                if count < 0:
                    raise ValueError('Negative or absent extraports count')
                state = extra.get('state','unknown')
                if state not in ('open','closed','filtered','unfiltered','open|filtered','closed|filtered'):
                    problems.append('Missing/unsupported extraports state')
                counts[state] += count; extra_count += count
            if len(explicit) + extra_count != len(expected_ports):
                problems.append('Explicit plus extraports counts do not equal intended port count')
        observations.append({'address':address,'issues':problems,'explicit_open_ports':sorted(open_ports),
                             'state_counts':dict(counts),'host_up_reason':status.get('reason') if status is not None else None})
    summary = doc.find('runstats/hosts')
    if summary is None:
        issues.append('Missing runstats hosts summary')
    else:
        total, up, down = [int(summary.get(k,'-1')) for k in ('total','up','down')]
        if min(total,up,down) < 0 or total != up + down or total != len(observations) or down:
            issues.append('Host summary inconsistent or includes down/unrepresented targets')
    return {'file':str(path),'sha256':hashlib.sha256(data).hexdigest(),
            'nmap_version':doc.get('version'),'scan_start_epoch':doc.get('start'),
            'issues':issues,'hosts':observations}


def check(scope, expected_ports, paths):
    reports = [inspect(p,expected_ports) for p in paths]
    seen = Counter(h['address'] for r in reports for h in r['hosts'])
    missing, unexpected = sorted(scope - seen.keys()), sorted(seen.keys() - scope)
    duplicates = sorted(k for k,v in seen.items() if v > 1)
    consistent = not (missing or unexpected or duplicates or any(r['issues'] or any(h['issues'] for h in r['hosts']) for r in reports))
    return {'schema':1,'generated_at':datetime.now(timezone.utc).isoformat(),
            'status':'consistent' if consistent else 'incomplete_or_inconsistent',
            'expected_targets':sorted(scope),'expected_ports':sorted(expected_ports),
            'missing_targets':missing,'unexpected_targets':unexpected,'duplicate_targets':duplicates,
            'reports':reports,
            'interpretation':'XML accounting consistency only, not proof of wire-level coverage, ownership, service health, complete vulnerability assessment or remediation. Filtered/no-response is not retirement; user-set host-up is not a response.'}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--targets',required=True,help='File of exact approved IPv4/IPv6 literals')
    p.add_argument('--ports',required=True,help='Explicit intended TCP ports/ranges, e.g. 22,80,443')
    p.add_argument('xml',nargs='+',help='Saved Nmap XML files; no wildcard expansion inside the program')
    a = p.parse_args(argv)
    try:
        report = check(targets(a.targets),ports(a.ports),a.xml)
        print(json.dumps(report,indent=2))
        return int(report['status'] != 'consistent')
    except (OSError,ValueError,ET.ParseError) as exc:
        p.exit(2,f'Error: {exc}\n')


if __name__ == '__main__': raise SystemExit(main())
