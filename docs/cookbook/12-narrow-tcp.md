# Narrow TCP discovery on an exact authorised IP

## Who

Engineer authorised for active port discovery.

## What

Narrow TCP discovery on an exact authorised IP. Traffic/effects: Active TCP connection attempts to one IP and explicitly listed ports; no version probes or NSE. The block creates a new private POSIX evidence directory and session log.

## Where

Linux/Kali/WSL Bash on your approved collector; use the repository root for recipes invoking repository scripts. Vantage matters: record whether you are behind VPN, proxy or TLS inspection. See the [start guide](README.md).

## When

When confirming service inventory or testing a documented service change.

## Why

Determine whether a small explicit set of TCP ports responds from this collector.

## How

Prerequisites: Bash and Nmap. Replace the IP and select approved ports. Open the specified terminal, edit sentinel inputs, then paste the complete block. Network recipes stop before probing if the target sentinel is unchanged. Inspect inputs manually; these are operator recipes, not hardened parsers for untrusted input.

```bash
(
  umask 077
  mkdir -p "$HOME/cyber-evidence" || exit 1
  EVIDENCE_DIR="$(mktemp -d "$HOME/cyber-evidence/validation-12-narrow-tcp-XXXXXX")" || exit 1
  collect_recipe() {
    printf '%s\n' 'CHECK: Narrow TCP discovery on an exact authorised IP'
    printf '%s\n' 'WHY: Determine whether a small explicit set of TCP ports responds from this collector.'
    date -u '+%FT%TZ'
TARGET_IP='REPLACE_WITH_AUTHORISED_IP'
[[ "$TARGET_IP" != REPLACE_WITH_AUTHORISED_IP ]] || { echo 'Edit TARGET_IP first.' >&2; return 2; }
TARGET_PORTS='22,80,443'
nmap -n -Pn -sT --reason -p "$TARGET_PORTS" --max-rate 10 --max-retries 1 \
  -oA "$EVIDENCE_DIR/tcp" "$TARGET_IP"
printf 'nmap exit: %s\n' "$?"
  }
  collect_recipe > "$EVIDENCE_DIR/session.txt" 2>&1
  recipe_status=$?
  cat "$EVIDENCE_DIR/session.txt"
  printf 'Block status: %s (inspect individual command statuses/errors)\nEvidence: %s\n' "$recipe_status" "$EVIDENCE_DIR"
)
```

## Output and interpretation

The final line identifies the evidence directory. Open session.txt and any separately saved response/certificate/scan files. Outputs vary by installed tool and environment; no canned result is presented as live evidence.

Open means a connection was accepted; filtered/no-response does not establish retirement. With -Pn, host-up can be an operator assumption.

## Next decision

Validate XML completion and intended port/target coverage; identify open services selectively.

## Limits and recovery

Rate choice is illustrative, not universally safe. Kernel connect traffic is not fully described by a probe-rate ceiling. Retries can miss transient responses; no UDP or exhaustive ports. If a dependency, route, trust or permission check fails, keep the exact error and mark coverage incomplete. Do not treat package installation, privilege escalation, trust bypass or firewall changes as automatic recovery. No configuration rollback is needed because no remediation occurs; retain or remove only your newly generated evidence according to retention policy.

## Validation

Bash syntax checked; no live network probes were run. Use local version help and validate on a controlled authorised endpoint before operational use. [Primary references](README.md#primary-references).
