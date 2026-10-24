# legacy_domain_scanner.py

## Who

Engineer explicitly authorised to probe the supplied domains. Do not elevate unless a documented collection prerequisite and local approval require it.

## What

DNS and TLS evidence collection. Review its output; it does not automatically remediate findings.

## Where

Linux/Kali terminal or another validated sslscan-capable host; first change into the legacy scanner directory.

## When

Only when that legacy report format is specifically required.

## Why

Preserve the earlier combined DNS/TLS evidence workflow for users who need its report format.

**Decision supported:** Review per-domain DNS/TLS evidence and collection errors.

## How

1. Confirm that the host, files or targets are within your authorised scope.
2. Check prerequisites: Python 3.10+ and the local requirements.txt, sslscan on PATH, and domains.txt with authorised hostnames.
3. Open the specified terminal and directory. Inspect the script before running it.
4. Run the command below. These examples do not install dependencies or bypass policy.

```bash
cd legacy/domain-scanner
python legacy_domain_scanner.py domains.txt --output-dir new-results
```

5. Read the output and limitations before deciding the next action. See the [detailed usage guide](../../legacy/domain-scanner/README.md) for options, schema, collection instructions and exit behaviour.

## Output and interpretation

A new report directory, raw TLS evidence, DNS text and escaped HTML plus results.json. Inspect collection errors before drawing conclusions.

Overlaps newer tools; no AI; limited DKIM/MTA-STS coverage; no assurance verdict.

## Next action

Review per-domain DNS/TLS evidence and collection errors. Retain the original evidence privately, record collection time and scope, and confirm unexpected results with the relevant owner or an independent check. Record unknowns rather than converting them into a pass/fail claim.

## Changes and recovery

These review/collection tools do not change security configuration or remediate automatically. Network collectors create authorised traffic; file collectors can cause cloud-file hydration. Some tools write reports as documented. Preserve original evidence, use a new private output destination and follow normal retention rules. Shell redirection can overwrite existing files. No rollback of configuration is required because none is performed.

## Validation

Synthetic regression checks; see detailed guide for platform requirements and limitations. Do not interpret synthetic tests as validation of every operating system, trust configuration or target environment.
