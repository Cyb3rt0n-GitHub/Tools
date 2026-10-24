# Capture TLS chain with hostname verification

## Who

TLS/service engineer authorised to connect to an endpoint.

## What

Capture TLS chain with hostname verification. Traffic/effects: DNS and one TLS handshake; no application login. The block creates a new private POSIX evidence directory and session log.

## Where

Linux/Kali/WSL Bash on your approved collector; use the repository root for recipes invoking repository scripts. Vantage matters: record whether you are behind VPN, proxy or TLS inspection. See the [start guide](README.md).

## When

During certificate renewal or trust/chain failure investigation.

## Why

Keep the presented certificates, hostname verification errors and command exit together.

## How

Prerequisites: Linux/WSL Bash, OpenSSL and GNU timeout. CA trust comes from this OpenSSL installation. Open the specified terminal, edit sentinel inputs, then paste the complete block. Network recipes stop before probing if the target sentinel is unchanged. Inspect inputs manually; these are operator recipes, not hardened parsers for untrusted input.

```bash
(
  umask 077
  mkdir -p "$HOME/cyber-evidence" || exit 1
  EVIDENCE_DIR="$(mktemp -d "$HOME/cyber-evidence/validation-10-tls-chain-XXXXXX")" || exit 1
  collect_recipe() {
    printf '%s\n' 'CHECK: Capture TLS chain with hostname verification'
    printf '%s\n' 'WHY: Keep the presented certificates, hostname verification errors and command exit together.'
    date -u '+%FT%TZ'
TARGET_HOST='REPLACE_WITH_AUTHORISED_HOST'
[[ "$TARGET_HOST" != REPLACE_WITH_AUTHORISED_HOST ]] || { echo 'Edit TARGET_HOST first.' >&2; return 2; }
TARGET_PORT=443
timeout 20 openssl s_client -connect "$TARGET_HOST:$TARGET_PORT" \
  -servername "$TARGET_HOST" -verify_hostname "$TARGET_HOST" \
  -verify_return_error -showcerts </dev/null > "$EVIDENCE_DIR/tls.txt" 2>&1
status=$?
printf 'TLS command exit: %s\n' "$status"
cat "$EVIDENCE_DIR/tls.txt"
if openssl x509 -in "$EVIDENCE_DIR/tls.txt" -out "$EVIDENCE_DIR/leaf.pem"; then
  openssl x509 -in "$EVIDENCE_DIR/leaf.pem" -noout -subject -issuer -dates \
    -ext subjectAltName -fingerprint -sha256
else
  echo 'No parseable leaf; preserve the TLS failure as incomplete evidence.'
fi
  }
  collect_recipe > "$EVIDENCE_DIR/session.txt" 2>&1
  recipe_status=$?
  cat "$EVIDENCE_DIR/session.txt"
  printf 'Block status: %s (inspect individual command statuses/errors)\nEvidence: %s\n' "$recipe_status" "$EVIDENCE_DIR"
)
```

## Output and interpretation

The final line identifies the evidence directory. Open session.txt and any separately saved response/certificate/scan files. Outputs vary by installed tool and environment; no canned result is presented as live evidence.

A certificate can be parsed even when trust fails. Prioritise explicit errors, handshake state and process exit over isolated session lines.

## Next decision

Confirm SNI, collector trust store and presented intermediate chain before assigning remediation.

## Limits and recovery

Revocation is not established. A successful negotiated protocol does not show which older protocols are disabled. If a dependency, route, trust or permission check fails, keep the exact error and mark coverage incomplete. Do not treat package installation, privilege escalation, trust bypass or firewall changes as automatic recovery. No configuration rollback is needed because no remediation occurs; retain or remove only your newly generated evidence according to retention policy.

## Validation

Bash syntax checked; no live network probes were run. Use local version help and validate on a controlled authorised endpoint before operational use. [Primary references](README.md#primary-references).
