# security-summary.sh

## Who

Host support/security engineer with authorised local read access; begin as a standard user. Some checks may need additional approved privileges; missing permissions mean incomplete evidence.

## What

security summary. Review its output; it does not automatically remediate findings.

## Where

On the linux host being investigated, from the repository root; not from a different management machine.

## When

During initial host review or after approved security configuration work.

## Why

Collect a quick view of locally available security-control status.

**Decision supported:** Identify unavailable or unexpected controls that need a targeted check.

## How

1. Confirm that the host, files or targets are within your authorised scope.
2. Check prerequisites: Bash and the optional native commands named in the script. Missing tools are reported, not installed.
3. Open the specified terminal and directory. Inspect the script before running it.
4. Run the command below. These examples do not install dependencies or bypass policy.

```bash
bash scripts/linux/security/security-summary.sh
```

5. Read the output and limitations before deciding the next action. See the [detailed usage guide](../../scripts/README.md) for options, schema, collection instructions and exit behaviour.

## Output and interpretation

Human-readable local state on stdout; no report is saved automatically. Read every unavailable/failed-check message. Completion does not mean all checks succeeded.

Missing privileges/tools make results incomplete; this is not a hardening score or compliance verdict.

## Next action

Identify unavailable or unexpected controls that need a targeted check. Retain the original evidence privately, record collection time and scope, and confirm unexpected results with the relevant owner or an independent check. Record unknowns rather than converting them into a pass/fail claim.

## Changes and recovery

These review/collection tools do not change security configuration or remediate automatically. Network collectors create authorised traffic; file collectors can cause cloud-file hydration. Some tools write reports as documented. Preserve original evidence, use a new private output destination and follow normal retention rules. Shell redirection can overwrite existing files. No rollback of configuration is required because none is performed.

## Validation

Linux local smoke check Do not interpret synthetic tests as validation of every operating system, trust configuration or target environment.
