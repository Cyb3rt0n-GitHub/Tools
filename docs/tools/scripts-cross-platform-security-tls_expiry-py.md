# tls_expiry.py

## Who

Service owner or engineer authorised to connect to the endpoint. Do not elevate unless a documented collection prerequisite and local approval require it.

## What

Verified TLS endpoint certificate expiry. Review its output; it does not automatically remediate findings.

## Where

Any Python 3.10+ host with network access to the explicitly authorised endpoint; repository root.

## When

Before renewals, during service onboarding or after certificate deployment.

## Why

Spot impending certificate expiry or certificate/identity validation failures.

**Decision supported:** Prioritise renewal or investigate trust, hostname and connectivity errors.

## How

1. Confirm that the host, files or targets are within your authorised scope.
2. Check prerequisites: Python standard library only, correct clock and trust store. Substitute an authorised hostname. Internal PKI may require --ca-file.
3. Open the specified terminal and directory. Inspect the script before running it.
4. Run the command below. These examples do not install dependencies or bypass policy.

```bash
python scripts/cross-platform/security/tls_expiry.py example.org --warn-days 30
```

5. Read the output and limitations before deciding the next action. See the [detailed usage guide](../../scripts/cross-platform/security/README.md) for options, schema, collection instructions and exit behaviour.

## Output and interpretation

JSON to stdout. Exit 0 verified/outside warning window, 1 verified/expiring, 2 error/unknown. It makes a TLS connection.

One verified endpoint is not complete TLS coverage; trust depends on local clock/store and revocation is not established.

## Next action

Prioritise renewal or investigate trust, hostname and connectivity errors. Retain the original evidence privately, record collection time and scope, and confirm unexpected results with the relevant owner or an independent check. Record unknowns rather than converting them into a pass/fail claim.

## Changes and recovery

These review/collection tools do not change security configuration or remediate automatically. Network collectors create authorised traffic; file collectors can cause cloud-file hydration. Some tools write reports as documented. Preserve original evidence, use a new private output destination and follow normal retention rules. Shell redirection can overwrite existing files. No rollback of configuration is required because none is performed.

## Validation

Synthetic regression tests; Linux tested; native Windows/macOS validation pending Do not interpret synthetic tests as validation of every operating system, trust configuration or target environment.

## Worked example

**Illustrative scenario, not captured evidence:** JSON reports status expiring with days_remaining 12 and the process exits 1.

**Interpretation:** Certificate validation succeeded for the selected endpoint, but expiry falls within the configured warning window.

**Next step:** Confirm service ownership and renewal arrangements, deploy through change control, then repeat the same hostname/port check.
