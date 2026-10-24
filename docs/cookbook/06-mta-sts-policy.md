# Retrieve an MTA-STS policy body

## Who

Mail-security reviewer authorised to request the domain policy.

## What

Retrieve an MTA-STS policy body. Traffic/effects: DNS and one HTTPS GET to the specified domain’s MTA-STS policy host. The block creates a new private POSIX evidence directory and session log.

## Where

Linux/Kali/WSL Bash on your approved collector; use the repository root for recipes invoking repository scripts. Vantage matters: record whether you are behind VPN, proxy or TLS inspection. See the [start guide](README.md).

## When

After collecting _mta-sts TXT evidence.

## Why

Distinguish the DNS advertisement from the HTTPS policy actually served.

## How

Prerequisites: Bash and curl. Open the specified terminal, edit sentinel inputs, then paste the complete block. Network recipes stop before probing if the target sentinel is unchanged. Inspect inputs manually; these are operator recipes, not hardened parsers for untrusted input.

```bash
(
  umask 077
  mkdir -p "$HOME/cyber-evidence" || exit 1
  EVIDENCE_DIR="$(mktemp -d "$HOME/cyber-evidence/validation-06-mta-sts-policy-XXXXXX")" || exit 1
  collect_recipe() {
    printf '%s\n' 'CHECK: Retrieve an MTA-STS policy body'
    printf '%s\n' 'WHY: Distinguish the DNS advertisement from the HTTPS policy actually served.'
    date -u '+%FT%TZ'
TARGET_HOST='REPLACE_WITH_AUTHORISED_HOST'
[[ "$TARGET_HOST" != REPLACE_WITH_AUTHORISED_HOST ]] || { echo 'Edit TARGET_HOST first.' >&2; return 2; }
curl --silent --show-error --connect-timeout 5 --max-time 20 \
  --dump-header "$EVIDENCE_DIR/policy.headers" --output "$EVIDENCE_DIR/policy.txt" \
  --write-out 'HTTP: %{http_code}\nPeer: %{remote_ip}\n' \
  "https://mta-sts.$TARGET_HOST/.well-known/mta-sts.txt"
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

Review certificate/transfer success, HTTP status, version, mode, mx patterns and max_age in the saved body.

## Next decision

Check policy MX coverage against the actual inbound mail architecture before proposing enforcement.

## Limits and recovery

No redirects are followed; retrieval does not prove sending MTAs enforce the policy or mail delivery works. If a dependency, route, trust or permission check fails, keep the exact error and mark coverage incomplete. Do not treat package installation, privilege escalation, trust bypass or firewall changes as automatic recovery. No configuration rollback is needed because no remediation occurs; retain or remove only your newly generated evidence according to retention policy.

## Validation

Bash syntax checked; no live network probes were run. Use local version help and validate on a controlled authorised endpoint before operational use. [Primary references](README.md#primary-references).
