# review_sshd.py

## Who

SSH service administrator or reviewer working with authorised configuration evidence. Do not elevate unless a documented collection prerequisite and local approval require it.

## What

Domain DNS/TLS evidence collection. Review its output; it does not automatically remediate findings.

## Where

Any Python 3.10+ analysis host; repository root. Capture sshd -T separately on the authorised Linux/macOS SSH server.

## When

When reviewing saved sshd -T output for a specific default or simulated connection context.

## Why

Turn effective SSH settings into review prompts while retaining authentication and access context.

**Decision supported:** Select settings needing design/owner review before proposing changes.

## How

1. Confirm that the host, files or targets are within your authorised scope.
2. Check prerequisites: Saved successful sshd -T output, not raw sshd_config. Record whether default or a specific -C connection context was used; see the detailed guide for collection and privileges.
3. Open the specified terminal and directory. Inspect the script before running it.
4. Run the command below. These examples do not install dependencies or bypass policy.

```bash
python scripts/cross-platform/security/review_sshd.py saved-sshd-effective.txt --context-label "default, no -C context"
```

5. Read the output and limitations before deciding the next action. See the [detailed usage guide](../../scripts/cross-platform/security/README.md) for options, schema, collection instructions and exit behaviour.

## Output and interpretation

JSON review prompts and full effective values. Exit 0 means parsed, not secure; exit 2 means read/format error.

Not a compliance baseline; does not prove the running daemon uses these settings or that MFA/reachability works.

## Next action

Select settings needing design/owner review before proposing changes. Retain the original evidence privately, record collection time and scope, and confirm unexpected results with the relevant owner or an independent check. Record unknowns rather than converting them into a pass/fail claim.

## Changes and recovery

These review/collection tools do not change security configuration or remediate automatically. Network collectors create authorised traffic; file collectors can cause cloud-file hydration. Some tools write reports as documented. Preserve original evidence, use a new private output destination and follow normal retention rules. Shell redirection can overwrite existing files. No rollback of configuration is required because none is performed.

## Validation

Synthetic parser regression tests; native Linux/macOS sshd collection validation pending Do not interpret synthetic tests as validation of every operating system, trust configuration or target environment.
