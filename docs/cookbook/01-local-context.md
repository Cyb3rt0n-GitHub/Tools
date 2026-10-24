# Local collector and network context

## Who

Host support or security engineer with local read access.

## What

Local collector and network context. Traffic/effects: No network requests. The block creates a new private POSIX evidence directory and session log.

## Where

Linux/Kali/WSL Bash on your approved collector; use the repository root for recipes invoking repository scripts. Vantage matters: record whether you are behind VPN, proxy or TLS inspection. See the [start guide](README.md).

## When

Before collecting or comparing evidence from different networks.

## Why

Explain which machine, resolver and route produced an observation.

## How

Prerequisites: Linux/WSL Bash; ip, ss, uname, date; optional resolvectl. Open the specified terminal, edit sentinel inputs, then paste the complete block. Network recipes stop before probing if the target sentinel is unchanged. Inspect inputs manually; these are operator recipes, not hardened parsers for untrusted input.

```bash
(
  umask 077
  mkdir -p "$HOME/cyber-evidence" || exit 1
  EVIDENCE_DIR="$(mktemp -d "$HOME/cyber-evidence/validation-01-local-context-XXXXXX")" || exit 1
  collect_recipe() {
    printf '%s\n' 'CHECK: Local collector and network context'
    printf '%s\n' 'WHY: Explain which machine, resolver and route produced an observation.'
    date -u '+%FT%TZ'
date -u '+%FT%TZ'
hostname
uname -a
cat /etc/os-release
ip -br address
ip route
ip -6 route
cat /etc/resolv.conf
ss -tulpen
  }
  collect_recipe > "$EVIDENCE_DIR/session.txt" 2>&1
  recipe_status=$?
  cat "$EVIDENCE_DIR/session.txt"
  printf 'Block status: %s (inspect individual command statuses/errors)\nEvidence: %s\n' "$recipe_status" "$EVIDENCE_DIR"
)
```

## Output and interpretation

The final line identifies the evidence directory. Open session.txt and any separately saved response/certificate/scan files. Outputs vary by installed tool and environment; no canned result is presented as live evidence.

Addresses, routes and listeners describe the collector, not the remote estate. Permission restrictions can hide process details.

## Next decision

Record VPN/proxy context; investigate missing routes before classifying a remote service failure.

## Limits and recovery

Read each command error. A local listener does not establish external exposure. If a dependency, route, trust or permission check fails, keep the exact error and mark coverage incomplete. Do not treat package installation, privilege escalation, trust bypass or firewall changes as automatic recovery. No configuration rollback is needed because no remediation occurs; retain or remove only your newly generated evidence according to retention policy.

## Validation

Bash syntax checked; no live network probes were run. Use local version help and validate on a controlled authorised endpoint before operational use. [Primary references](README.md#primary-references).
