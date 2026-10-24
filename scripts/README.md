# Personal admin, network and security scripts

A starter collection for Cyb3rt0n-GitHub's personal/public account. Standalone scripts are grouped by platform and purpose. Workplace and enterprise projects are excluded.

| Platform | Admin | Network | Security |
|---|---|---|---|
| Windows | OS, uptime, disk and memory | Interfaces, DNS settings, IPv4 routes, TCP listeners | Defender, firewall profiles, BitLocker |
| macOS | OS, uptime, disk and memory | Interfaces, default route, DNS and proxies | FileVault, Gatekeeper, SIP and application firewall |
| Linux | OS, uptime, disk and memory | Interfaces, routes, resolver configuration and listeners | Firewall status, SSH service state and filesystem types |

## Status

Initial drafts. Linux scripts have been smoke-tested in a Linux container; all Bash scripts have passed syntax checks. Windows and macOS scripts still need native platform validation. These are diagnostics, not a hardening or compliance assessment. A Linux container is not representative of a full desktop/server installation.

## Run

Download or clone the source, inspect it, then run only the file for your platform. No remote `curl | bash` installer and no execution-policy bypass is required or supplied.

Linux:

```bash
bash linux/admin/system-summary.sh
bash linux/network/network-summary.sh
bash linux/security/security-summary.sh
```

macOS (built-in Bash is supported):

```bash
bash macos/admin/system-summary.sh
bash macos/network/network-summary.sh
bash macos/security/security-summary.sh
```

Windows, from a PowerShell prompt in the collection's root:

```powershell
.\windows\admin\Get-SystemSummary.ps1
.\windows\network\Get-NetworkSummary.ps1
.\windows\security\Get-SecuritySummary.ps1
```

If organisational policy prevents script execution, follow the organisation's approved process. Do not weaken it to run these scripts.

## Requirements and interpretation

Windows: Windows PowerShell 5.1+; CIM, NetTCPIP, Defender, NetSecurity and BitLocker cmdlets where installed. macOS: built-in commands listed in each script. Linux: Bash and the optional tools shown in each script (`ip`, `ss`, `free`, `ufw`, `firewall-cmd`, `systemctl`, `lsblk`). A missing optional command is reported, never installed automatically.

These scripts read local state only. They do not elevate, install packages, modify settings, ping hosts, scan targets, upload results or contact AI services. Some checks need privileges or host services that may be unavailable; they then show incomplete/unknown output. Alternative firewall and SSH services need not all be installed or active. A detected listener does not prove internet exposure. Filesystem type is not conclusive proof of encryption.

Standard-user execution is the starting point. Each collector continues after an unavailable check, so a successful process exit does not mean every check succeeded or that the device is secure. Exit 2 from Bash indicates the wrong operating system.

To capture Bash output locally, append `> report.txt 2>&1`. In PowerShell, pipe to `Out-File -Encoding utf8 report.txt`. Use a private destination and review results before sharing: local addresses, DNS servers, routes, software versions and host configuration may be sensitive. No reports are saved automatically.

## Future additions

Use the same platform/category structure for backups, log collection, file integrity, certificate checks and troubleshooting. Any script that changes state should document changes, privileges, preview/dry-run behaviour and recovery separately. Add proven existing personal scripts only after removing duplicates, checking provenance and inspecting for secrets.

The newly authored starter scripts are supplied under the MIT licence in LICENSE. Recovered third-party or pre-existing lab material is not covered by this licence; see lab/README.md for the separate review queue.

## Lab environments

Topology-dependent or state-changing material belongs under `lab/`, with separate setup, preview, recovery and validation instructions. See [lab/README.md](lab/README.md).

## Cross-platform engineering tools

See [evidence manifests and TLS expiry](cross-platform/security/README.md) for SHA-256 collection/change comparison and verified certificate checks. Python 3.10+, no extra packages.

Compare saved [listener and vulnerability exports](cross-platform/security/README.md#listener-drift-and-vulnerability-export-reconciliation) to identify observation changes without automatically declaring remediation.

See the [tool selection guide](../TOOL-GUIDE.md) for the reason to use each tool, the decision it supports and its limits.
