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
