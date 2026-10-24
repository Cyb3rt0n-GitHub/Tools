# DNS records and resolver status

## Who

Domain owner or authorised DNS reviewer.

## What

DNS records and resolver status. Traffic/effects: Queries the configured resolver; it may use remote upstream services. The block creates a new private POSIX evidence directory and session log.

## Where

Linux/Kali/WSL Bash on your approved collector; use the repository root for recipes invoking repository scripts. Vantage matters: record whether you are behind VPN, proxy or TLS inspection. See the [start guide](README.md).

## When

During asset onboarding, DNS changes or ownership investigation.

## Why

Separate NXDOMAIN, empty answers and failed queries while collecting useful record context.

## How

Prerequisites: Bash and dig. Open the specified terminal, edit sentinel inputs, then paste the complete block. Network recipes stop before probing if the target sentinel is unchanged. Inspect inputs manually; these are operator recipes, not hardened parsers for untrusted input.

```bash
(
  umask 077
  mkdir -p "$HOME/cyber-evidence" || exit 1
  EVIDENCE_DIR="$(mktemp -d "$HOME/cyber-evidence/validation-03-dns-records-XXXXXX")" || exit 1
  collect_recipe() {
    printf '%s\n' 'CHECK: DNS records and resolver status'
    printf '%s\n' 'WHY: Separate NXDOMAIN, empty answers and failed queries while collecting useful record context.'
    date -u '+%FT%TZ'
TARGET_HOST='REPLACE_WITH_AUTHORISED_HOST'
[[ "$TARGET_HOST" != REPLACE_WITH_AUTHORISED_HOST ]] || { echo 'Edit TARGET_HOST first.' >&2; return 2; }
for rr in A AAAA CNAME MX NS TXT CAA; do
  printf '\n=== %s %s ===\n' "$TARGET_HOST" "$rr"
  dig +time=3 +tries=1 "$TARGET_HOST" "$rr"
  printf 'dig exit: %s\n' "$?"
done
  }
  collect_recipe > "$EVIDENCE_DIR/session.txt" 2>&1
  recipe_status=$?
  cat "$EVIDENCE_DIR/session.txt"
  printf 'Block status: %s (inspect individual command statuses/errors)\nEvidence: %s\n' "$recipe_status" "$EVIDENCE_DIR"
)
```

## Output and interpretation

The final line identifies the evidence directory. Open session.txt and any separately saved response/certificate/scan files. Outputs vary by installed tool and environment; no canned result is presented as live evidence.

Read the DNS status and answer section. NOERROR without an answer differs from NXDOMAIN; resolver failure is unknown.

## Next decision

Confirm authoritative records and responsible owners before modifying inventory or controls.

## Limits and recovery

DNS associations and shared provider names do not prove ownership, application use or vulnerability. If a dependency, route, trust or permission check fails, keep the exact error and mark coverage incomplete. Do not treat package installation, privilege escalation, trust bypass or firewall changes as automatic recovery. No configuration rollback is needed because no remediation occurs; retain or remove only your newly generated evidence according to retention policy.

## Validation

Bash syntax checked; no live network probes were run. Use local version help and validate on a controlled authorised endpoint before operational use. [Primary references](README.md#primary-references).
