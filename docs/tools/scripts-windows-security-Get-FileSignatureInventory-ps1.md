# Get-FileSignatureInventory.ps1

## Who

Windows engineer reviewing software provenance or investigating file changes. Do not elevate unless a documented collection prerequisite and local approval require it.

## What

Domain DNS/TLS evidence collection. Review its output; it does not automatically remediate findings.

## Where

Windows PowerShell 5.1+; repository root. Inspect explicit files on local drives.

## When

When checking software deliveries, suspected tampering or post-change binaries.

## Why

Record file identity and publisher-signature observations without running the files.

**Decision supported:** Select files needing provenance checks, sandbox analysis or vendor confirmation.

## How

1. Confirm that the host, files or targets are within your authorised scope.
2. Check prerequisites: Read access to stable local files; Get-FileHash and Get-AuthenticodeSignature. Follow approved execution policy. No bypass or automatic elevation.
3. Open the specified terminal and directory. Inspect the script before running it.
4. Run the command below. These examples do not install dependencies or bypass policy.

```powershell
& .\scripts\windows\security\Get-FileSignatureInventory.ps1 -LiteralPath "C:\Tools\example.exe","C:\Tools\helper.dll"
```

5. Read the output and limitations before deciding the next action. See the [detailed usage guide](../../scripts/windows/security/SIGNATURE-GUIDE.md) for options, schema, collection instructions and exit behaviour.

## Output and interpretation

JSON to stdout, including hashes, signer/status and individual errors. Exit 0 collection completed, 2 at least one error. Windows trust checks may use the network.

Valid is not safe; unsigned is not malicious; host trust and network/cache behaviour affect validation.

## Next action

Select files needing provenance checks, sandbox analysis or vendor confirmation. Retain the original evidence privately, record collection time and scope, and confirm unexpected results with the relevant owner or an independent check. Record unknowns rather than converting them into a pass/fail claim.

## Changes and recovery

These review/collection tools do not change security configuration or remediate automatically. Network collectors create authorised traffic; file collectors can cause cloud-file hydration. Some tools write reports as documented. Preserve original evidence, use a new private output destination and follow normal retention rules. Shell redirection can overwrite existing files. No rollback of configuration is required because none is performed.

## Validation

Windows synthetic-file CI added; broader operational validation pending Do not interpret synthetic tests as validation of every operating system, trust configuration or target environment.
