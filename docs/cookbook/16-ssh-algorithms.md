# SSH banner, algorithms and host-key evidence

## Who

Engineer authorised for SSH service identification.

## What

SSH banner, algorithms and host-key evidence. Traffic/effects: SSH protocol probes to one IP/port; no supplied credentials. The block creates a new private POSIX evidence directory and session log.

## Where

Linux/Kali/WSL Bash on your approved collector; use the repository root for recipes invoking repository scripts. Vantage matters: record whether you are behind VPN, proxy or TLS inspection. See the [start guide](README.md).

## When

During inventory, SSH hardening review or a host-key change investigation.

## Why

Review SSH exposure and cryptographic offerings without a password/login attempt.

## How

Prerequisites: Bash and Nmap with the named scripts. Open the specified terminal, edit sentinel inputs, then paste the complete block. Network recipes stop before probing if the target sentinel is unchanged. Inspect inputs manually; these are operator recipes, not hardened parsers for untrusted input.

```bash
(
  umask 077
  mkdir -p "$HOME/cyber-evidence" || exit 1
  EVIDENCE_DIR="$(mktemp -d "$HOME/cyber-evidence/validation-16-ssh-algorithms-XXXXXX")" || exit 1
  collect_recipe() {
    printf '%s\n' 'CHECK: SSH banner, algorithms and host-key evidence'
    printf '%s\n' 'WHY: Review SSH exposure and cryptographic offerings without a password/login attempt.'
    date -u '+%FT%TZ'
TARGET_IP='REPLACE_WITH_AUTHORISED_IP'
[[ "$TARGET_IP" != REPLACE_WITH_AUTHORISED_IP ]] || { echo 'Edit TARGET_IP first.' >&2; return 2; }
TARGET_PORT=22
nmap -n -Pn -sT -p "$TARGET_PORT" --script ssh2-enum-algos,ssh-hostkey \
  -oA "$EVIDENCE_DIR/ssh" "$TARGET_IP"
printf 'nmap exit: %s\n' "$?"
  }
  collect_recipe > "$EVIDENCE_DIR/session.txt" 2>&1
  recipe_status=$?
  cat "$EVIDENCE_DIR/session.txt"
  printf 'Block status: %s (inspect individual command statuses/errors)\nEvidence: %s\n' "$recipe_status" "$EVIDENCE_DIR"
)
```

## Output and interpretation

The final line identifies the evidence directory. Open session.txt and any separately saved response/certificate/scan files. Outputs vary by installed tool and environment; no canned result is presented as live evidence.

Algorithms and host keys describe the observed service. They do not prove authentication policy or a particular CVE.

## Next decision

Verify expected host keys through an independent trusted source; review effective SSH configuration with the service owner.

## Limits and recovery

No password authentication is attempted. Service handshakes are logged and can trigger monitoring. Backports mean a banner alone is not patch evidence. If a dependency, route, trust or permission check fails, keep the exact error and mark coverage incomplete. Do not treat package installation, privilege escalation, trust bypass or firewall changes as automatic recovery. No configuration rollback is needed because no remediation occurs; retain or remove only your newly generated evidence according to retention policy.

## Validation

Bash syntax checked; no live network probes were run. Use local version help and validate on a controlled authorised endpoint before operational use. [Primary references](README.md#primary-references).
