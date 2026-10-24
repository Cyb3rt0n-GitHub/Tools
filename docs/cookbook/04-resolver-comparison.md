# Compare configured and public DNS

## Who

DNS/network engineer with approval to query an external resolver.

## What

Compare configured and public DNS. Traffic/effects: Queries configured DNS and Google DNS-over-HTTPS; no discovered host is probed. The block creates a new private POSIX evidence directory and session log.

## Where

Linux/Kali/WSL Bash on your approved collector; use the repository root for recipes invoking repository scripts. Vantage matters: record whether you are behind VPN, proxy or TLS inspection. See the [start guide](README.md).

## When

When internal and external asset observations disagree.

## Why

Identify split DNS or differences caused by vantage, caching and resolver policy.

## How

Prerequisites: Bash, dig and curl. External resolver use must follow policy. Open the specified terminal, edit sentinel inputs, then paste the complete block. Network recipes stop before probing if the target sentinel is unchanged. Inspect inputs manually; these are operator recipes, not hardened parsers for untrusted input.

```bash
(
  umask 077
  mkdir -p "$HOME/cyber-evidence" || exit 1
  EVIDENCE_DIR="$(mktemp -d "$HOME/cyber-evidence/validation-04-resolver-comparison-XXXXXX")" || exit 1
  collect_recipe() {
    printf '%s\n' 'CHECK: Compare configured and public DNS'
    printf '%s\n' 'WHY: Identify split DNS or differences caused by vantage, caching and resolver policy.'
    date -u '+%FT%TZ'
TARGET_HOST='REPLACE_WITH_AUTHORISED_HOST'
[[ "$TARGET_HOST" != REPLACE_WITH_AUTHORISED_HOST ]] || { echo 'Edit TARGET_HOST first.' >&2; return 2; }
dig +time=3 +tries=1 "$TARGET_HOST" A
printf 'configured DNS exit: %s\n' "$?"
curl --silent --show-error --fail --connect-timeout 5 --max-time 15 \
  --get --data-urlencode "name=$TARGET_HOST" --data-urlencode 'type=A' \
  'https://dns.google/resolve'
printf '\nDoH transfer exit: %s\n' "$?"
  }
  collect_recipe > "$EVIDENCE_DIR/session.txt" 2>&1
  recipe_status=$?
  cat "$EVIDENCE_DIR/session.txt"
  printf 'Block status: %s (inspect individual command statuses/errors)\nEvidence: %s\n' "$recipe_status" "$EVIDENCE_DIR"
)
```

## Output and interpretation

The final line identifies the evidence directory. Open session.txt and any separately saved response/certificate/scan files. Outputs vary by installed tool and environment; no canned result is presented as live evidence.

A successful HTTPS transfer is not necessarily a successful DNS answer; inspect the JSON Status and Answer fields.

## Next decision

Retain both answers and compare from an approved independent collector if needed.

## Limits and recovery

Public resolver queries disclose the queried name. A difference is not by itself a defect. If a dependency, route, trust or permission check fails, keep the exact error and mark coverage incomplete. Do not treat package installation, privilege escalation, trust bypass or firewall changes as automatic recovery. No configuration rollback is needed because no remediation occurs; retain or remove only your newly generated evidence according to retention policy.

## Validation

Bash syntax checked; no live network probes were run. Use local version help and validate on a controlled authorised endpoint before operational use. [Primary references](README.md#primary-references).
