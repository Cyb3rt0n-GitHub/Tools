# Tool identity and prerequisites

## Who

Engineer preparing a reproducible collection.

## What

Tool identity and prerequisites. Traffic/effects: No network requests. The block creates a new private POSIX evidence directory and session log.

## Where

Linux/Kali/WSL Bash on your approved collector; use the repository root for recipes invoking repository scripts. Vantage matters: record whether you are behind VPN, proxy or TLS inspection. See the [start guide](README.md).

## When

Before using saved recipes or changing collectors.

## Why

Avoid ambiguous executables and unexplained differences between tool versions.

## How

Prerequisites: Bash and installed binaries; no installer runs. Open the specified terminal, edit sentinel inputs, then paste the complete block. Network recipes stop before probing if the target sentinel is unchanged. Inspect inputs manually; these are operator recipes, not hardened parsers for untrusted input.

```bash
(
  umask 077
  mkdir -p "$HOME/cyber-evidence" || exit 1
  EVIDENCE_DIR="$(mktemp -d "$HOME/cyber-evidence/validation-02-tool-identity-XXXXXX")" || exit 1
  collect_recipe() {
    printf '%s\n' 'CHECK: Tool identity and prerequisites'
    printf '%s\n' 'WHY: Avoid ambiguous executables and unexplained differences between tool versions.'
    date -u '+%FT%TZ'
for tool in curl openssl dig nmap sslscan httpx tlsx; do
  printf '\nTool: %s\n' "$tool"
  command -v "$tool" || echo 'Not installed or not on PATH'
done
curl --version
openssl version
nmap --version
  }
  collect_recipe > "$EVIDENCE_DIR/session.txt" 2>&1
  recipe_status=$?
  cat "$EVIDENCE_DIR/session.txt"
  printf 'Block status: %s (inspect individual command statuses/errors)\nEvidence: %s\n' "$recipe_status" "$EVIDENCE_DIR"
)
```

## Output and interpretation

The final line identifies the evidence directory. Open session.txt and any separately saved response/certificate/scan files. Outputs vary by installed tool and environment; no canned result is presented as live evidence.

Executable paths distinguish similarly named packages; missing tools leave coverage unavailable.

## Next decision

Install required tools through your approved package process and record the version actually run. Check local help before adding flags.

## Limits and recovery

This is not automatic dependency repair or supply-chain attestation. httpx may refer to a different product. If a dependency, route, trust or permission check fails, keep the exact error and mark coverage incomplete. Do not treat package installation, privilege escalation, trust bypass or firewall changes as automatic recovery. No configuration rollback is needed because no remediation occurs; retain or remove only your newly generated evidence according to retention policy.

## Validation

Bash syntax checked; no live network probes were run. Use local version help and validate on a controlled authorised endpoint before operational use. [Primary references](README.md#primary-references).
