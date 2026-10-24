"""Check one authorised TLS endpoint with certificate verification enabled; Python 3.10+."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import socket
import ssl


def collect(host, port=443, timeout=10, cafile=None, warn_days=30):
    context = ssl.create_default_context(cafile=cafile)
    with socket.create_connection((host, port), timeout=timeout) as raw:
        with context.wrap_socket(raw, server_hostname=host) as conn:
            cert = conn.getpeercert()
            expiry = ssl.cert_time_to_seconds(cert['notAfter'])
            remaining = (expiry - datetime.now(timezone.utc).timestamp()) / 86400
            return {'host': host, 'port': port, 'collected_at': datetime.now(timezone.utc).isoformat(),
                    'status': 'expiring' if remaining <= warn_days else 'ok',
                    'days_remaining': math.floor(remaining),
                    'expires_at': datetime.fromtimestamp(expiry, timezone.utc).isoformat(),
                    'leaf_sha256': hashlib.sha256(conn.getpeercert(binary_form=True)).hexdigest(),
                    'subject': cert.get('subject'), 'issuer': cert.get('issuer'),
                    'subject_alt_names': cert.get('subjectAltName'), 'tls_version': conn.version(),
                    'cipher': conn.cipher(), 'peer': conn.getpeername()}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('host'); p.add_argument('--port', type=int, default=443)
    p.add_argument('--timeout', type=float, default=10)
    p.add_argument('--warn-days', type=int, default=30)
    p.add_argument('--ca-file', help='Optional trusted PEM CA bundle for internal PKI')
    a = p.parse_args(argv)
    if not 1 <= a.port <= 65535 or not math.isfinite(a.timeout) or not 0 < a.timeout <= 120 or a.warn_days < 0:
        p.error('Invalid port, timeout (0–120 seconds) or warning threshold')
    if not a.host or any(c.isspace() for c in a.host) or any(c in a.host for c in '/\\@'):
        p.error('Provide a hostname or IP address, not a URL')
    try:
        result = collect(a.host, a.port, a.timeout, a.ca_file, a.warn_days)
    except (OSError, ValueError) as exc:
        print(json.dumps({'host': a.host, 'port': a.port, 'status': 'unknown',
                          'error_type': type(exc).__name__, 'error': str(exc)}))
        return 2
    print(json.dumps(result, indent=2))
    return int(result['status'] != 'ok')


if __name__ == '__main__':
    raise SystemExit(main())
