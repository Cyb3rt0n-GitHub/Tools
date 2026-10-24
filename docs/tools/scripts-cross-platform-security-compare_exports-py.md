# compare_exports.py

## Who

Engineer comparing equivalent listener or vulnerability collections. Do not elevate unless a documented collection prerequisite and local approval require it.

## What

Offline listener drift and vulnerability-export reconciliation. Review its output; it does not automatically remediate findings.

## Where

Any Python 3.10+ host; repository root. No scanner access or network connection required.

## When

After changes or between equivalent scheduled collections.

## Why

Expose listener-binding drift and changes between vulnerability exports without silently declaring closure.

**Decision supported:** Investigate new observations, metadata changes and items no longer observed.

## How

1. Confirm that the host, files or targets are within your authorised scope.
2. Check prerequisites: Normalised UTF-8 CSV files with the documented identity columns. Check scope, filters, collection success and timestamps independently.
3. Open the specified terminal and directory. Inspect the script before running it.
4. Run the command below. These examples do not install dependencies or bypass policy.

```bash
python scripts/cross-platform/security/compare_exports.py listeners scripts/cross-platform/security/examples/listeners-before.csv scripts/cross-platform/security/examples/listeners-after.csv --scope-id lab-web --before-at 2026-10-23T09:00:00Z --after-at 2026-10-24T09:00:00Z
python scripts/cross-platform/security/compare_exports.py vulnerabilities scripts/cross-platform/security/examples/vulnerabilities-before.csv scripts/cross-platform/security/examples/vulnerabilities-after.csv --scope-id lab-web --before-at 2026-10-23T09:00:00Z --after-at 2026-10-24T09:00:00Z
```

5. Read the output and limitations before deciding the next action. See the [detailed usage guide](../../scripts/cross-platform/security/README.md) for options, schema, collection instructions and exit behaviour.

## Output and interpretation

JSON to stdout. Examples are fictional. Exit 0 no differences, 1 changes, 2 invalid input/error.

Normalised CSV required; absent findings are not confirmed fixed and scope/collector success need independent verification.

## Next action

Investigate new observations, metadata changes and items no longer observed. Retain the original evidence privately, record collection time and scope, and confirm unexpected results with the relevant owner or an independent check. Record unknowns rather than converting them into a pass/fail claim.

## Changes and recovery

These review/collection tools do not change security configuration or remediate automatically. Network collectors create authorised traffic; file collectors can cause cloud-file hydration. Some tools write reports as documented. Preserve original evidence, use a new private output destination and follow normal retention rules. Shell redirection can overwrite existing files. No rollback of configuration is required because none is performed.

## Validation

Synthetic regression tests; Linux tested; native Windows/macOS validation pending Do not interpret synthetic tests as validation of every operating system, trust configuration or target environment.

## Worked example

**Illustrative scenario, not captured evidence:** A loopback listener disappears and a wildcard listener appears on the same host and port.

**Interpretation:** The observed bind address changed. Firewall, routing and namespaces still determine reachability.

**Next step:** Confirm whether the change was approved, identify the service owner and validate exposure within authorised scope. Missing vulnerability rows separately require closure evidence.
