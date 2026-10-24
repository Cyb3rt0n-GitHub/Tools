# Validate an SMTP STARTTLS handshake

## Who

Mail/TLS engineer authorised to probe the named service.

## What

Validate an SMTP STARTTLS handshake. Traffic/effects: One SMTP protocol/TLS negotiation; no authentication or message submission. The block creates a new private POSIX evidence directory and session log.

## Where

Linux/Kali/WSL Bash on your approved collector; use the repository root for recipes invoking repository scripts. Vantage matters: record whether you are behind VPN, proxy or TLS inspection. See the [start guide](README.md).

## When

When mail TLS evidence is missing or after a mail certificate change.

## Why

Assess certificate/hostname verification on an explicit SMTP STARTTLS endpoint.

## How

Prerequisites: Bash, OpenSSL with SMTP STARTTLS support and GNU timeout. Open the specified terminal, edit sentinel inputs, then paste the complete block. Network recipes stop before probing if the target sentinel is unchanged. Inspect inputs manually; these are operator recipes, not hardened parsers for untrusted input.

```bash
(
  umask 077
  mkdir -p "$HOME/cyber-evidence" || exit 1
  EVIDENCE_DIR="$(mktemp -d "$HOME/cyber-evidence/validation-15-mail-starttls-XXXXXX")" || exit 1
  collect_recipe() {
    printf '%s\n' 'CHECK: Validate an SMTP STARTTLS handshake'
    printf '%s\n' 'WHY: Assess certificate/hostname verification on an explicit SMTP STARTTLS endpoint.'
    date -u '+%FT%TZ'
TARGET_HOST='REPLACE_WITH_AUTHORISED_HOST'
[[ "$TARGET_HOST" != REPLACE_WITH_AUTHORISED_HOST ]] || { echo 'Edit TARGET_HOST first.' >&2; return 2; }
TARGET_PORT=25
timeout 25 openssl s_client -starttls smtp -connect "$TARGET_HOST:$TARGET_PORT" \
  -servername "$TARGET_HOST" -verify_hostname "$TARGET_HOST" \
  -verify_return_error -showcerts </dev/null > "$EVIDENCE_DIR/smtp-tls.txt" 2>&1
printf 'SMTP STARTTLS exit: %s\n' "$?"
cat "$EVIDENCE_DIR/smtp-tls.txt"
  }
  collect_recipe > "$EVIDENCE_DIR/session.txt" 2>&1
  recipe_status=$?
  cat "$EVIDENCE_DIR/session.txt"
  printf 'Block status: %s (inspect individual command statuses/errors)\nEvidence: %s\n' "$recipe_status" "$EVIDENCE_DIR"
)
```

## Output and interpretation

The final line identifies the evidence directory. Open session.txt and any separately saved response/certificate/scan files. Outputs vary by installed tool and environment; no canned result is presented as live evidence.

This checks one SMTP handshake and the supplied hostname, not real sender-to-recipient delivery or MTA-STS enforcement.

## Next decision

Confirm the actual MX/service identity and sending-MTA trust expectations before calling a name mismatch a policy failure.

## Limits and recovery

Protocol negotiation may issue greeting/EHLO/STARTTLS; no AUTH or mail message. Opportunistic SMTP policy differs from HTTPS. If a dependency, route, trust or permission check fails, keep the exact error and mark coverage incomplete. Do not treat package installation, privilege escalation, trust bypass or firewall changes as automatic recovery. No configuration rollback is needed because no remediation occurs; retain or remove only your newly generated evidence according to retention policy.

## Validation

Bash syntax checked; no live network probes were run. Use local version help and validate on a controlled authorised endpoint before operational use. [Primary references](README.md#primary-references).
