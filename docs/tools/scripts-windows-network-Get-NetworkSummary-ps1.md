# Get-NetworkSummary.ps1

## Who

Host support/security engineer with authorised local read access; begin as a standard user. Some checks may need additional approved privileges; missing permissions mean incomplete evidence.

## What

network summary. Review its output; it does not automatically remediate findings.

## Where

On the windows host being investigated, from the repository root; not from a different management machine.

## When

When investigating DNS, connectivity, routing or unexpected local services.

## Why

Explain how the host is connected and where traffic is expected to go.

**Decision supported:** Choose the next interface, route, resolver or listener to investigate.

## How

1. Confirm that the host, files or targets are within your authorised scope.
2. Check prerequisites: Windows PowerShell 5.1+ and available platform cmdlets; follow approved execution policy.
3. Open the specified terminal and directory. Inspect the script before running it.
4. Run the command below. These examples do not install dependencies or bypass policy.

```powershell
& .\scripts\windows\network\Get-NetworkSummary.ps1
```

5. Read the output and limitations before deciding the next action. See the [detailed usage guide](../../scripts/README.md) for options, schema, collection instructions and exit behaviour.

## Output and interpretation

Human-readable local state on stdout; no report is saved automatically. Read every unavailable/failed-check message. Completion does not mean all checks succeeded.

Local configuration does not prove end-to-end reachability or external exposure; platform outputs differ.

## Next action

Choose the next interface, route, resolver or listener to investigate. Retain the original evidence privately, record collection time and scope, and confirm unexpected results with the relevant owner or an independent check. Record unknowns rather than converting them into a pass/fail claim.

## Changes and recovery

These review/collection tools do not change security configuration or remediate automatically. Network collectors create authorised traffic; file collectors can cause cloud-file hydration. Some tools write reports as documented. Preserve original evidence, use a new private output destination and follow normal retention rules. Shell redirection can overwrite existing files. No rollback of configuration is required because none is performed.

## Validation

Native Windows/PowerShell validation pending Do not interpret synthetic tests as validation of every operating system, trust configuration or target environment.
