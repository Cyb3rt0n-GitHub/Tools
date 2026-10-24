# Mail DNS advertisements and known DKIM selectors

## Who

Email-security engineer or domain owner.

## What

Mail DNS advertisements and known DKIM selectors. Traffic/effects: Queries configured DNS only. The block creates a new private POSIX evidence directory and session log.

## Where

Linux/Kali/WSL Bash on your approved collector; use the repository root for recipes invoking repository scripts. Vantage matters: record whether you are behind VPN, proxy or TLS inspection. See the [start guide](README.md).

## When

During email onboarding, spoofing investigation or policy review.

## Why

Collect policy advertisements before diagnosing mail authentication.

## How

Prerequisites: Bash and dig. Edit the domain and known selector. Open the specified terminal, edit sentinel inputs, then paste the complete block. Network recipes stop before probing if the target sentinel is unchanged. Inspect inputs manually; these are operator recipes, not hardened parsers for untrusted input.

```bash
(
  umask 077
  mkdir -p "$HOME/cyber-evidence" || exit 1
  EVIDENCE_DIR="$(mktemp -d "$HOME/cyber-evidence/validation-05-mail-dns-XXXXXX")" || exit 1
  collect_recipe() {
    printf '%s\n' 'CHECK: Mail DNS advertisements and known DKIM selectors'
    printf '%s\n' 'WHY: Collect policy advertisements before diagnosing mail authentication.'
    date -u '+%FT%TZ'
TARGET_HOST='REPLACE_WITH_AUTHORISED_HOST'
[[ "$TARGET_HOST" != REPLACE_WITH_AUTHORISED_HOST ]] || { echo 'Edit TARGET_HOST first.' >&2; return 2; }
DKIM_SELECTOR='default'
for spec in "$TARGET_HOST MX" "$TARGET_HOST TXT" "_dmarc.$TARGET_HOST TXT" \
            "_mta-sts.$TARGET_HOST TXT" "_smtp._tls.$TARGET_HOST TXT" \
            "$DKIM_SELECTOR._domainkey.$TARGET_HOST TXT"; do
  read -r name rr <<< "$spec"
  printf '\n=== %s %s ===\n' "$name" "$rr"
  dig +time=3 +tries=1 "$name" "$rr"
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

TXT presence is evidence, not complete SPF/DMARC/DKIM/MTA-STS validation. Selectors must come from the mail deployment.

## Next decision

Review syntax, policy scope, actual mail flow and service ownership with the email administrator.

## Limits and recovery

Absent exact-domain DMARC can require policy-discovery evaluation. No full DMARC tree walk or SPF lookup-budget evaluation is implemented. If a dependency, route, trust or permission check fails, keep the exact error and mark coverage incomplete. Do not treat package installation, privilege escalation, trust bypass or firewall changes as automatic recovery. No configuration rollback is needed because no remediation occurs; retain or remove only your newly generated evidence according to retention policy.

## Validation

Bash syntax checked; no live network probes were run. Use local version help and validate on a controlled authorised endpoint before operational use. [Primary references](README.md#primary-references).
