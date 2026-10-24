# Engineering evidence tools

Python 3.10+, standard library only. Run from this directory. Covered by ../../LICENSE. No AI, telemetry, uploads, elevation or configuration changes.

## SHA-256 evidence manifests

```bash
python evidence_manifest.py snapshot /path/to/evidence /private/path/before.json
python evidence_manifest.py snapshot /path/to/evidence /private/path/after.json
python evidence_manifest.py compare /private/path/before.json /private/path/after.json
```

Windows paths work too. Reads all regular files including hidden files beneath the supplied root; skips symlinks and special files. Output must be outside the source directory and must not already exist. JSON contains relative paths, sizes, SHA-256, timestamp, skips and errors. POSIX output mode is 0600; Windows uses directory ACLs. Keep reports private.

Comparison reports added, changed and removed files. Incomplete collections suppress confirmed removals and return missing_unconfirmed. Snapshot exits 0 for no errors, 2 for errors. Compare exits 0 for complete/no changes, 1 for changes, 2 for incomplete/error.

This is an integrity aid, not signed chain of custody or an atomic filesystem snapshot. Store trusted manifests separately. Detected file mutation is reported; hostile directory races, Windows reparse points and concurrent replacement are outside its guarantees. Use quiescent trusted evidence directories. Large/cloud files can take time and trigger hydration. Skipped paths are unassessed.

## Verified TLS certificate expiry

```bash
python tls_expiry.py example.org --warn-days 30
python tls_expiry.py internal.example.org --port 8443 --ca-file internal-ca.pem
```

One TLS connection to your explicitly supplied authorised endpoint, using SNI and verified certificate/hostname checks. Supports approved internal CA bundles. No HTTP, redirects, logins or target discovery. Reports expiry, leaf SHA-256, subject/issuer, SANs, peer address and negotiated TLS/cipher. Exit 0: verified/outside warning window; 1: verified/expiring; 2: error/unknown. Invalid certificates are never bypassed.

Socket timeout does not bound system DNS resolution or total runtime. One selected endpoint and negotiated protocol do not assess all backends or supported versions. Default validation does not establish revocation status or application security. STARTTLS unsupported. Results depend on local trust store, clock and Python/OpenSSL version.

## Validation and references

Synthetic regression checks cover changes, incomplete collection, symlink skips, output protection, SNI/default-context use and certificate errors. Linux file collection was exercised locally; TLS is mocked, with no live target contact. Native Windows/macOS validation remains pending.

- [Python ssl security guidance](https://docs.python.org/3.12/library/ssl.html#security-considerations)
- [Python hashlib](https://docs.python.org/3/library/hashlib.html)

## Next candidates

Effective SSH configuration review; Windows executable signature inventory; listening-service baseline comparison; certificate inventory from explicit asset lists; vulnerability-export reconciliation. Each needs explicit scope, structured errors, reproducible evidence and interpretation limits. Remediation belongs in a separate reviewed workflow.

## Listener drift and vulnerability-export reconciliation

`compare_exports.py` compares **normalised CSV files offline**. It does not collect listeners, scan hosts, contact a scanner or download threat feeds. Python 3.10+, no dependencies. Examples use fictional assets.

From this directory:

```bash
python compare_exports.py listeners examples/listeners-before.csv examples/listeners-after.csv --scope-id lab-web --before-at 2026-10-23T09:00:00Z --after-at 2026-10-24T09:00:00Z
python compare_exports.py vulnerabilities examples/vulnerabilities-before.csv examples/vulnerabilities-after.csv --scope-id lab-web --before-at 2026-10-23T09:00:00Z --after-at 2026-10-24T09:00:00Z
```

Output goes to stdout as JSON. To retain it, redirect to a new private filename. Shell redirection can overwrite files; select a new destination. Nothing is uploaded. Exit 0: no observation changes; 1: changes; 2: invalid input/error. Scheduled jobs should distinguish changes from failures.

### Input contract

UTF-8 CSV, header required, one complete observation per row. Preserve raw scanner/collector evidence separately. Adapt vendor-specific exports into this schema explicitly; the script does not guess column meanings. Empty/header-only exports are accepted but are not proof of successful collection.

| Mode | Required identity columns | Notes |
|---|---|---|
| listeners | asset_id, protocol, address, port | protocol tcp/udp; numeric IPv4/IPv6; port 1–65535 |
| vulnerabilities | asset_id, finding_id, protocol, port | protocol tcp/udp/host; host findings use port `-` |

Use a stable inventory identifier for asset_id, not a transient address. IDs are case-sensitive. Namespace finding_id by scanner and check, e.g. `scanner-a:check-100`; a CVE alone may merge different checks. Include web path/virtual-host identity in finding_id where needed. Other columns (process, severity, CVE, status, owner) are retained and compared as metadata. Volatile fields such as timestamps and PIDs produce metadata differences; omit them from normalised input if inappropriate.

Numeric IPs and ports are canonicalised. Exact duplicate rows are counted; conflicting rows with the same identity fail closed. Do not silently merge different processes/check instances. UDP rows represent bound endpoints, not TCP LISTEN state. This first version does not parse native ss, lsof or PowerShell output.

### Interpretation and evidence

The report includes SHA-256 of each input, stated collection times/scope, unique-row and duplicate counts, newly observed rows, no-longer-observed rows and changed metadata. Input hashes identify the bytes compared; they do not establish provenance. Scope ID and timestamps are operator assertions. Independently check collector success, privileges, scanner authentication, exclusions, host coverage and export filters before drawing conclusions.

A loopback-to-wildcard binding appears as an old observation disappearing and a new one appearing. Wildcard binding does not establish external reachability: routing, firewall, namespaces and service state matter. A finding absent from the later export is not automatically fixed; verify with authenticated rescanning and closure evidence. Do not use status text alone to approve closure.

The tool deliberately avoids a synthetic risk score. Threat signals need local context: FIRST explains that EPSS predicts exploitation activity and is not a complete risk score. See [FIRST EPSS FAQ](https://www.first.org/epss/faq) before adding prioritisation fields.

Tests cover binding changes, finding severity changes, IPv6/port normalisation, duplicate conflicts, invalid rows, header-only exports and timezone validation. All comparisons run offline with synthetic data.
