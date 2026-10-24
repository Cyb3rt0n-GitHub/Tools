# Validate CIDRs and membership without scanning

## Who

Asset owner or engineer reconciling a supplied IP scope.

## What

Validate CIDRs and membership without scanning. Traffic/effects: No network requests. The block creates a new private POSIX evidence directory and session log.

## Where

Linux/Kali/WSL Bash on your approved collector; use the repository root for recipes invoking repository scripts. Vantage matters: record whether you are behind VPN, proxy or TLS inspection. See the [start guide](README.md).

## When

Before drafting a discovery scope or reconciling finding ownership.

## Why

Catch malformed networks and check whether a finding address is within a stated range.

## How

Prerequisites: Bash and Python 3; examples are documentation-only addresses. Open the specified terminal, edit sentinel inputs, then paste the complete block. Network recipes stop before probing if the target sentinel is unchanged. Inspect inputs manually; these are operator recipes, not hardened parsers for untrusted input.

```bash
(
  umask 077
  mkdir -p "$HOME/cyber-evidence" || exit 1
  EVIDENCE_DIR="$(mktemp -d "$HOME/cyber-evidence/validation-17-scope-calculation-XXXXXX")" || exit 1
  collect_recipe() {
    printf '%s\n' 'CHECK: Validate CIDRs and membership without scanning'
    printf '%s\n' 'WHY: Catch malformed networks and check whether a finding address is within a stated range.'
    date -u '+%FT%TZ'
python3 - <<'PYCODE'
import ipaddress
networks = [ipaddress.ip_network(x, strict=True) for x in ['192.0.2.0/24', '2001:db8::/32']]
for n in networks:
    print(n, 'first', n.network_address, 'last', n.broadcast_address, 'addresses', n.num_addresses)
for text in ['192.0.2.10', '198.51.100.10', '2001:db8::10']:
    ip = ipaddress.ip_address(text)
    print(ip, 'matches', [str(n) for n in networks if ip.version == n.version and ip in n])
PYCODE
  }
  collect_recipe > "$EVIDENCE_DIR/session.txt" 2>&1
  recipe_status=$?
  cat "$EVIDENCE_DIR/session.txt"
  printf 'Block status: %s (inspect individual command statuses/errors)\nEvidence: %s\n' "$recipe_status" "$EVIDENCE_DIR"
)
```

## Output and interpretation

The final line identifies the evidence directory. Open session.txt and any separately saved response/certificate/scan files. Outputs vary by installed tool and environment; no canned result is presented as live evidence.

Counts are address-space size, not live hosts. Range membership does not prove allocation, use or ownership.

## Next decision

Confirm written ownership/scope with the asset authority before any probing.

## Limits and recovery

No-match means investigate; cloud, SaaS and shared hosting may legitimately sit elsewhere. No targets are contacted. If a dependency, route, trust or permission check fails, keep the exact error and mark coverage incomplete. Do not treat package installation, privilege escalation, trust bypass or firewall changes as automatic recovery. No configuration rollback is needed because no remediation occurs; retain or remove only your newly generated evidence according to retention policy.

## Validation

Bash syntax checked; no live network probes were run. Use local version help and validate on a controlled authorised endpoint before operational use. [Primary references](README.md#primary-references).
