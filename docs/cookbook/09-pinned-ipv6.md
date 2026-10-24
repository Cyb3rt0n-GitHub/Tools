# Check IPv6 separately from IPv4

## Who

Engineer with an authorised hostname/global IPv6 endpoint.

## What

Check IPv6 separately from IPv4. Traffic/effects: One direct IPv6 HTTPS request to the explicit address. The block creates a new private POSIX evidence directory and session log.

## Where

Linux/Kali/WSL Bash on your approved collector; use the repository root for recipes invoking repository scripts. Vantage matters: record whether you are behind VPN, proxy or TLS inspection. See the [start guide](README.md).

## When

When an asset publishes IPv6 or IPv6 coverage is incomplete.

## Why

Avoid treating an IPv4 result or AAAA record as proof of working IPv6 service.

## How

Prerequisites: Bash, curl built with IPv6, and a functioning IPv6 route. Open the specified terminal, edit sentinel inputs, then paste the complete block. Network recipes stop before probing if the target sentinel is unchanged. Inspect inputs manually; these are operator recipes, not hardened parsers for untrusted input.

```bash
(
  umask 077
  mkdir -p "$HOME/cyber-evidence" || exit 1
  EVIDENCE_DIR="$(mktemp -d "$HOME/cyber-evidence/validation-09-pinned-ipv6-XXXXXX")" || exit 1
  collect_recipe() {
    printf '%s\n' 'CHECK: Check IPv6 separately from IPv4'
    printf '%s\n' 'WHY: Avoid treating an IPv4 result or AAAA record as proof of working IPv6 service.'
    date -u '+%FT%TZ'
TARGET_HOST='REPLACE_WITH_AUTHORISED_HOST'
[[ "$TARGET_HOST" != REPLACE_WITH_AUTHORISED_HOST ]] || { echo 'Edit TARGET_HOST first.' >&2; return 2; }
TARGET_IP='REPLACE_WITH_AUTHORISED_IP'
[[ "$TARGET_IP" != REPLACE_WITH_AUTHORISED_IP ]] || { echo 'Edit TARGET_IP first.' >&2; return 2; }
TARGET_PORT=443
curl --ipv6 --noproxy '*' --silent --show-error --connect-timeout 5 --max-time 20 \
  --resolve "$TARGET_HOST:$TARGET_PORT:[$TARGET_IP]" \
  --dump-header "$EVIDENCE_DIR/ipv6.headers" --output /dev/null \
  --write-out 'HTTP: %{http_code}\nPeer: %{remote_ip}\n' \
  "https://$TARGET_HOST:$TARGET_PORT/"
printf 'curl exit: %s\n' "$?"
  }
  collect_recipe > "$EVIDENCE_DIR/session.txt" 2>&1
  recipe_status=$?
  cat "$EVIDENCE_DIR/session.txt"
  printf 'Block status: %s (inspect individual command statuses/errors)\nEvidence: %s\n' "$recipe_status" "$EVIDENCE_DIR"
)
```

## Output and interpretation

The final line identifies the evidence directory. Open session.txt and any separately saved response/certificate/scan files. Outputs vary by installed tool and environment; no canned result is presented as live evidence.

Network-unreachable can be a collector limitation. Review the actual peer, HTTP status and verification errors.

## Next decision

Confirm the local IPv6 route; repeat from an approved IPv6-capable collector if unavailable.

## Limits and recovery

Test each address independently. Equivalent DNS/provider names do not prove identical services. If a dependency, route, trust or permission check fails, keep the exact error and mark coverage incomplete. Do not treat package installation, privilege escalation, trust bypass or firewall changes as automatic recovery. No configuration rollback is needed because no remediation occurs; retain or remove only your newly generated evidence according to retention policy.

## Validation

Bash syntax checked; no live network probes were run. Use local version help and validate on a controlled authorised endpoint before operational use. [Primary references](README.md#primary-references).
