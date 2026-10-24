# Inspect saved web evidence for component indicators

## Who

Engineer analysing already collected response files.

## What

Inspect saved web evidence for component indicators. Traffic/effects: No network requests. The block creates a new private POSIX evidence directory and session log.

## Where

Linux/Kali/WSL Bash on your approved collector; use the repository root for recipes invoking repository scripts. Vantage matters: record whether you are behind VPN, proxy or TLS inspection. See the [start guide](README.md).

## When

After an approved response capture or during offline triage.

## Why

Find clues for technology/supplier questions without making additional web requests.

## How

Prerequisites: Bash and grep; a trusted saved text response. Edit the path. Open the specified terminal, edit sentinel inputs, then paste the complete block. Network recipes stop before probing if the target sentinel is unchanged. Inspect inputs manually; these are operator recipes, not hardened parsers for untrusted input.

```bash
(
  umask 077
  mkdir -p "$HOME/cyber-evidence" || exit 1
  EVIDENCE_DIR="$(mktemp -d "$HOME/cyber-evidence/validation-18-local-component-evidence-XXXXXX")" || exit 1
  collect_recipe() {
    printf '%s\n' 'CHECK: Inspect saved web evidence for component indicators'
    printf '%s\n' 'WHY: Find clues for technology/supplier questions without making additional web requests.'
    date -u '+%FT%TZ'
SAVED_BODY='REPLACE_WITH_SAVED_TEXT_RESPONSE'
[[ -f "$SAVED_BODY" ]] || { echo 'Set SAVED_BODY to an existing evidence file.'; return 2; }
grep -nEi 'wp-content/|wp-includes/|bootstrap|jquery|lodash|datatables' "$SAVED_BODY"
printf 'grep exit: %s (1 means no match; 2 means error)\n' "$?"
  }
  collect_recipe > "$EVIDENCE_DIR/session.txt" 2>&1
  recipe_status=$?
  cat "$EVIDENCE_DIR/session.txt"
  printf 'Block status: %s (inspect individual command statuses/errors)\nEvidence: %s\n' "$recipe_status" "$EVIDENCE_DIR"
)
```

## Output and interpretation

The final line identifies the evidence directory. Open session.txt and any separately saved response/certificate/scan files. Outputs vary by installed tool and environment; no canned result is presented as live evidence.

A filename, string or advertised version is an indicator, not proof of an executing vulnerable component.

## Next decision

Request runtime/package, deployment and relevant vendor advisory/backport evidence from the supplier.

## Limits and recovery

Cached or bundled content can mislead. Do not infer PHP version from WordPress version, or a CVE from a library filename. If a dependency, route, trust or permission check fails, keep the exact error and mark coverage incomplete. Do not treat package installation, privilege escalation, trust bypass or firewall changes as automatic recovery. No configuration rollback is needed because no remediation occurs; retain or remove only your newly generated evidence according to retention policy.

## Validation

Bash syntax checked; no live network probes were run. Use local version help and validate on a controlled authorised endpoint before operational use. [Primary references](README.md#primary-references).
