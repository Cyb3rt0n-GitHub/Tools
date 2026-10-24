# Verified HTTPS response evidence

## Who

Engineer authorised to request the service root.

## What

Verified HTTPS response evidence. Traffic/effects: DNS and one verified HTTPS GET. Curl may use configured proxies; record that vantage. The block creates a new private POSIX evidence directory and session log.

## Where

Linux/Kali/WSL Bash on your approved collector; use the repository root for recipes invoking repository scripts. Vantage matters: record whether you are behind VPN, proxy or TLS inspection. See the [start guide](README.md).

## When

During service identification, certificate changes or supplier assurance.

## Why

Retain headers, body, peer address and errors without confusing transfer success with application health.

## How

Prerequisites: Bash and curl. Open the specified terminal, edit sentinel inputs, then paste the complete block. Network recipes stop before probing if the target sentinel is unchanged. Inspect inputs manually; these are operator recipes, not hardened parsers for untrusted input.

```bash
(
  umask 077
  mkdir -p "$HOME/cyber-evidence" || exit 1
  EVIDENCE_DIR="$(mktemp -d "$HOME/cyber-evidence/validation-07-verified-http-XXXXXX")" || exit 1
  collect_recipe() {
    printf '%s\n' 'CHECK: Verified HTTPS response evidence'
    printf '%s\n' 'WHY: Retain headers, body, peer address and errors without confusing transfer success with application health.'
    date -u '+%FT%TZ'
TARGET_HOST='REPLACE_WITH_AUTHORISED_HOST'
[[ "$TARGET_HOST" != REPLACE_WITH_AUTHORISED_HOST ]] || { echo 'Edit TARGET_HOST first.' >&2; return 2; }
curl --silent --show-error --connect-timeout 5 --max-time 20 \
  --max-filesize 5242880 \
  --dump-header "$EVIDENCE_DIR/response.headers" --output "$EVIDENCE_DIR/response.body" \
  --write-out 'HTTP: %{http_code}\nPeer: %{remote_ip}\nURL: %{url_effective}\n' \
  "https://$TARGET_HOST/"
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

HTTP 403 with curl exit 0 means a response was transferred, not that the application is healthy. TLS verification remains enabled.

## Next decision

Review status, Location and headers, then decide whether an approved next URL or owner query is needed.

## Limits and recovery

No redirects, credentials, forms or page JavaScript. A GET can still create server logs or side effects. Size limits can leave partial bodies; inspect exit/error. If a dependency, route, trust or permission check fails, keep the exact error and mark coverage incomplete. Do not treat package installation, privilege escalation, trust bypass or firewall changes as automatic recovery. No configuration rollback is needed because no remediation occurs; retain or remove only your newly generated evidence according to retention policy.

## Validation

Bash syntax checked; no live network probes were run. Use local version help and validate on a controlled authorised endpoint before operational use. [Primary references](README.md#primary-references).
