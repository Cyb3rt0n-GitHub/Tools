#!/usr/bin/env bash
# Scan one hostname per line; retain raw output, including failed scans.
set -uo pipefail
input=${1:-domains_new.txt}
output_dir=${2:-sslscan-output-$(date -u +%Y%m%dT%H%M%SZ)}
for tool in sslscan aha timeout; do
    command -v "$tool" >/dev/null || { printf 'Missing dependency: %s\n' "$tool" >&2; exit 1; }
done
[[ -r "$input" ]] || { printf 'Cannot read input: %s\n' "$input" >&2; exit 1; }
umask 077
mkdir -- "$output_dir" || exit 1
output="$output_dir/sslscan_results.txt"
: > "$output"
failed=0
count=0
while IFS= read -r domain || [[ -n "$domain" ]]; do
    domain=${domain%%#*}
    domain=${domain//$'\r'/}
    domain="${domain#"${domain%%[![:space:]]*}"}"
    domain="${domain%"${domain##*[![:space:]]}"}"
    [[ -z "$domain" ]] && continue
    if [[ ! "$domain" =~ ^[a-zA-Z0-9]([a-zA-Z0-9.-]*[a-zA-Z0-9])?$ ]]; then
        printf 'Invalid hostname: %s\n' "$domain" >&2
        failed=1
        continue
    fi
    count=$((count + 1))
    printf '\n=== %s ===\n' "$domain" >> "$output"
    printf 'Scanning %s\n' "$domain"
    timeout 120 sslscan --no-colour "$domain" >> "$output" 2>&1
    status=$?
    if (( status != 0 )); then
        printf '\nSCAN FAILED (exit %s)\n' "$status" >> "$output"
        failed=1
    fi
done < "$input"
if (( count == 0 )); then
    printf 'No valid domains supplied\n' >&2
    exit 1
fi
aha -f "$output" > "$output_dir/sslscan_results.html" || exit 1
printf 'Reports saved in %s\n' "$output_dir"
exit "$failed"
