# Manifest preserved evidence using the existing tool

## Who

Engineer preparing a handover or verifying a transfer.

## What

Manifest preserved evidence using the existing tool. Traffic/effects: No network requests. The block creates a new private POSIX evidence directory and session log.

## Where

Linux/Kali/WSL Bash on your approved collector; use the repository root for recipes invoking repository scripts. Vantage matters: record whether you are behind VPN, proxy or TLS inspection. See the [start guide](README.md).

## When

Before sharing or transferring a collection directory.

## Why

Record exactly which file contents were retained and identify subsequent changes.

## How

Prerequisites: Python 3.10+; run from the repository root. Edit source/output paths; output must be outside source. Open the specified terminal, edit sentinel inputs, then paste the complete block. Network recipes stop before probing if the target sentinel is unchanged. Inspect inputs manually; these are operator recipes, not hardened parsers for untrusted input.

```bash
(
  umask 077
  mkdir -p "$HOME/cyber-evidence" || exit 1
  EVIDENCE_DIR="$(mktemp -d "$HOME/cyber-evidence/validation-19-evidence-integrity-XXXXXX")" || exit 1
  collect_recipe() {
    printf '%s\n' 'CHECK: Manifest preserved evidence using the existing tool'
    printf '%s\n' 'WHY: Record exactly which file contents were retained and identify subsequent changes.'
    date -u '+%FT%TZ'
SOURCE_DIR='REPLACE_WITH_EVIDENCE_DIRECTORY'
MANIFEST_FILE='REPLACE_WITH_NEW_MANIFEST_PATH'
[[ -d "$SOURCE_DIR" ]] || { echo 'Set SOURCE_DIR first.'; return 2; }
python3 scripts/cross-platform/security/evidence_manifest.py snapshot "$SOURCE_DIR" "$MANIFEST_FILE"
printf 'Manifest exit: %s\n' "$?"
  }
  collect_recipe > "$EVIDENCE_DIR/session.txt" 2>&1
  recipe_status=$?
  cat "$EVIDENCE_DIR/session.txt"
  printf 'Block status: %s (inspect individual command statuses/errors)\nEvidence: %s\n' "$recipe_status" "$EVIDENCE_DIR"
)
```

## Output and interpretation

The final line identifies the evidence directory. Open session.txt and any separately saved response/certificate/scan files. Outputs vary by installed tool and environment; no canned result is presented as live evidence.

Review errors/skips, not just the successful command. Hashes establish byte identity, not provenance.

## Next decision

Keep a trusted independent manifest and follow approved retention/sharing rules.

## Limits and recovery

The output directory itself is not an atomic forensic image. Do not publish raw cookies, response bodies or private identifiers. If a dependency, route, trust or permission check fails, keep the exact error and mark coverage incomplete. Do not treat package installation, privilege escalation, trust bypass or firewall changes as automatic recovery. No configuration rollback is needed because no remediation occurs; retain or remove only your newly generated evidence according to retention policy.

## Validation

Bash syntax checked; no live network probes were run. Use local version help and validate on a controlled authorised endpoint before operational use. [Primary references](README.md#primary-references).
