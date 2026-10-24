# evidence_manifest.py

## Who

Engineer preserving evidence or checking file integrity. Do not elevate unless a documented collection prerequisite and local approval require it.

## What

SHA-256 evidence snapshots and comparison. Review its output; it does not automatically remediate findings.

## Where

Any Python 3.10+ host; repository root. Source evidence must be in a trusted, stable directory.

## When

Before and after evidence transfer, analysis or controlled maintenance.

## Why

Detect file-content changes and identify the exact evidence bytes preserved.

**Decision supported:** Decide which files need investigation or recollection.

## How

1. Confirm that the host, files or targets are within your authorised scope.
2. Check prerequisites: Python standard library only. Replace placeholders with real paths; output must be outside the evidence directory and must not already exist.
3. Open the specified terminal and directory. Inspect the script before running it.
4. Run the command below. These examples do not install dependencies or bypass policy.

```bash
python scripts/cross-platform/security/evidence_manifest.py snapshot /path/to/evidence /private/path/before.json
python scripts/cross-platform/security/evidence_manifest.py snapshot /path/to/evidence /private/path/after.json
python scripts/cross-platform/security/evidence_manifest.py compare /private/path/before.json /private/path/after.json
```

5. Read the output and limitations before deciding the next action. See the [detailed usage guide](../../scripts/cross-platform/security/README.md) for options, schema, collection instructions and exit behaviour.

## Output and interpretation

JSON snapshots plus comparison output. Snapshot exit 2 indicates collection errors; comparison 1 means differences, 2 means incomplete/error.

Hashes do not prove provenance; collection is not atomic and skipped/error paths remain unassessed.

## Next action

Decide which files need investigation or recollection. Retain the original evidence privately, record collection time and scope, and confirm unexpected results with the relevant owner or an independent check. Record unknowns rather than converting them into a pass/fail claim.

## Changes and recovery

These review/collection tools do not change security configuration or remediate automatically. Network collectors create authorised traffic; file collectors can cause cloud-file hydration. Some tools write reports as documented. Preserve original evidence, use a new private output destination and follow normal retention rules. Shell redirection can overwrite existing files. No rollback of configuration is required because none is performed.

## Validation

Synthetic regression tests; Linux tested; native Windows/macOS validation pending Do not interpret synthetic tests as validation of every operating system, trust configuration or target environment.

## Worked example

**Illustrative scenario, not captured evidence:** Comparison lists report.json as changed and another path as missing_unconfirmed.

**Interpretation:** The first file has different content hashes; incomplete collection prevents confirming the missing file was deleted.

**Next step:** Check expected edits, preserve both manifests and recollect inaccessible evidence before approving integrity or transfer completion.
