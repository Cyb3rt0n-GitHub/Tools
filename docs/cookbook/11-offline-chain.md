# Diagnose a missing intermediate offline

## Who

TLS engineer with saved certificate evidence.

## What

Diagnose a missing intermediate offline. Traffic/effects: No network requests. The block creates a new private POSIX evidence directory and session log.

## Where

Linux/Kali/WSL Bash on your approved collector; use the repository root for recipes invoking repository scripts. Vantage matters: record whether you are behind VPN, proxy or TLS inspection. See the [start guide](README.md).

## When

When the original verified connection fails with an issuer/chain error.

## Why

Distinguish missing intermediate delivery from trust-store or hostname errors without adding a trusted root.

## How

Prerequisites: Bash and OpenSSL; saved leaf, independently obtained authentic intermediate and existing trusted root bundle. Edit all paths. Open the specified terminal, edit sentinel inputs, then paste the complete block. Network recipes stop before probing if the target sentinel is unchanged. Inspect inputs manually; these are operator recipes, not hardened parsers for untrusted input.

```bash
(
  umask 077
  mkdir -p "$HOME/cyber-evidence" || exit 1
  EVIDENCE_DIR="$(mktemp -d "$HOME/cyber-evidence/validation-11-offline-chain-XXXXXX")" || exit 1
  collect_recipe() {
    printf '%s\n' 'CHECK: Diagnose a missing intermediate offline'
    printf '%s\n' 'WHY: Distinguish missing intermediate delivery from trust-store or hostname errors without adding a trusted root.'
    date -u '+%FT%TZ'
TARGET_HOST='REPLACE_WITH_CERTIFICATE_HOST'
LEAF_FILE='REPLACE_WITH_LEAF_PEM'
INTERMEDIATE_FILE='REPLACE_WITH_INTERMEDIATE_PEM'
ROOTS_FILE='REPLACE_WITH_EXISTING_ROOT_BUNDLE'
for file in "$LEAF_FILE" "$INTERMEDIATE_FILE" "$ROOTS_FILE"; do
  [[ -f "$file" ]] || { echo "Missing input: $file"; return 2; }
done
openssl verify -CAfile "$ROOTS_FILE" -purpose sslserver -verify_hostname "$TARGET_HOST" "$LEAF_FILE"
printf 'Without supplied intermediate exit: %s\n' "$?"
openssl verify -CAfile "$ROOTS_FILE" -untrusted "$INTERMEDIATE_FILE" \
  -purpose sslserver -verify_hostname "$TARGET_HOST" "$LEAF_FILE"
printf 'With supplied intermediate exit: %s\n' "$?"
  }
  collect_recipe > "$EVIDENCE_DIR/session.txt" 2>&1
  recipe_status=$?
  cat "$EVIDENCE_DIR/session.txt"
  printf 'Block status: %s (inspect individual command statuses/errors)\nEvidence: %s\n' "$recipe_status" "$EVIDENCE_DIR"
)
```

## Output and interpretation

The final line identifies the evidence directory. Open session.txt and any separately saved response/certificate/scan files. Outputs vary by installed tool and environment; no canned result is presented as live evidence.

If only the second verification succeeds, the supplied intermediate completes a path for that saved leaf and trust store.

## Next decision

Correlate the leaf fingerprint with the original handshake and fix server chain delivery through change control; rerun original verification afterwards.

## Limits and recovery

The intermediate is untrusted chain material, not a new root. Confirm authenticity through validation to existing roots. Missing transmitted roots is normal; this is not a revocation check. If a dependency, route, trust or permission check fails, keep the exact error and mark coverage incomplete. Do not treat package installation, privilege escalation, trust bypass or firewall changes as automatic recovery. No configuration rollback is needed because no remediation occurs; retain or remove only your newly generated evidence according to retention policy.

## Validation

Bash syntax checked; no live network probes were run. Use local version help and validate on a controlled authorised endpoint before operational use. [Primary references](README.md#primary-references).
