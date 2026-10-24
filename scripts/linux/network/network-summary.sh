#!/usr/bin/env bash
# Read-only local diagnostics. No elevation, configuration changes or remote probes.
# Run with bash; optional capture: bash SCRIPT > report.txt 2>&1
set -u
if [[ "$(uname -s)" != "Linux" ]]; then printf "This script requires linux.\n" >&2; exit 2; fi
check() {
    title=$1; shift
    printf '\n=== %s ===\n' "$title"
    if ! command -v "$1" >/dev/null 2>&1; then
        printf 'UNAVAILABLE: command is not installed: %s\n' "$1"
        return 0
    fi
    "$@"
    status=$?
    if (( status != 0 )); then
        printf 'CHECK INCOMPLETE or service inactive (exit %s); inspect the output above. Do not infer a secure/insecure state.\n' "$status"
    fi
    return 0
}
printf 'Personal diagnostics: linux — network\nUTC: '; date -u '+%Y-%m-%dT%H:%M:%SZ'
check Interfaces ip -brief address
check Routes ip route show
check 'Resolver configuration' cat /etc/resolv.conf
check 'Listening TCP/UDP ports' ss -lntu
printf '\nCollection complete. Unavailable checks are not security findings. Review before sharing.\n'
