# Cyber Security Cookbook

Reusable methods adapted from a private validation toolbox. Organisation-specific names, addresses, collector IDs, paths, finding counts, historical logs and case conclusions are omitted. All recipes below are rewritten public examples; previous case-specific validation does **not** transfer to them.

## Start here

1. Choose the question you need to answer from the menu. Read Who, What, Where, When, How and Why before running it.
2. Use a trusted Linux/Kali/WSL Bash terminal unless a recipe explicitly says otherwise. macOS needs compatible tools (notably GNU timeout); native macOS validation is pending. No automatic installation or elevation is performed.
3. For network recipes, replace the sentinel target with an explicitly authorised hostname/IP and review the port, scope, proxy/vantage and traffic described. Documentation addresses are not live targets. A hostname can resolve to several/shared addresses: use exact IP pinning where required.
4. Paste one complete block. Each starts a subshell, sets private POSIX output permissions and creates a fresh evidence directory with mktemp. Variables do not survive the closing parenthesis. Commands and their separate statuses are recorded in session.txt; the recipe's last command is not an overall success indicator.
5. Read stderr, statuses, raw evidence and coverage limits. Keep originals private. No recipe performs automatic remediation, submits credentials or bypasses TLS verification.

**Evidence effects:** local files/directories are created under ~/cyber-evidence; active checks generate traffic and logs. Bodies, headers and host configuration can contain secrets/personal data. POSIX umask does not guarantee Windows-mounted-filesystem ACLs. Use an approved evidence location and retention policy. These Bash examples are syntax-checked and dependency commands reviewed; no network targets were contacted during validation. Existing-tool regression tests are separate.

## Recipe menu

- [Local collector and network context](01-local-context.md)
- [Tool identity and prerequisites](02-tool-identity.md)
- [DNS records and resolver status](03-dns-records.md)
- [Compare configured and public DNS](04-resolver-comparison.md)
- [Mail DNS advertisements and known DKIM selectors](05-mail-dns.md)
- [Retrieve an MTA-STS policy body](06-mta-sts-policy.md)
- [Verified HTTPS response evidence](07-verified-http.md)
- [Pin an HTTPS request to an explicit IPv4 address](08-pinned-ipv4.md)
- [Check IPv6 separately from IPv4](09-pinned-ipv6.md)
- [Capture TLS chain with hostname verification](10-tls-chain.md)
- [Diagnose a missing intermediate offline](11-offline-chain.md)
- [Narrow TCP discovery on an exact authorised IP](12-narrow-tcp.md)
- [Light service identification on one known-open port](13-light-service.md)
- [Enumerate TLS protocols and ciphers selectively](14-tls-ciphers.md)
- [Validate an SMTP STARTTLS handshake](15-mail-starttls.md)
- [SSH banner, algorithms and host-key evidence](16-ssh-algorithms.md)
- [Validate CIDRs and membership without scanning](17-scope-calculation.md)
- [Inspect saved web evidence for component indicators](18-local-component-evidence.md)
- [Manifest preserved evidence using the existing tool](19-evidence-integrity.md)

- [Native Windows verified HTTPS evidence](20-windows-verified-https.md)

- [Check saved Nmap TCP coverage](21-nmap-coverage.md)

## Further methods: explicit review required

The original also contains crawling/screenshots, ProjectDiscovery fingerprinting, FTP/FTPS/POP3/IMAP variants, RPC/SNMP, broad/batched discovery, template scanning, package repair and native Windows evidence collection. Their useful concepts are retained in [advanced-methods.md](advanced-methods.md), with scope and validation requirements. Historical shell history, temporary workarounds, incomplete runs and case-specific results are not public recipes.

## Primary references

- [curl manual](https://curl.se/docs/manpage.html): resolve, noproxy, output, timeouts and verification.
- [OpenSSL s_client](https://docs.openssl.org/3.5/man1/openssl-s_client/): SNI, verification, chain display and STARTTLS.
- [OpenSSL verification options](https://docs.openssl.org/3.5/man1/openssl-verification-options/): purpose, hostname, trusted roots and untrusted intermediates.
- [Nmap output](https://nmap.org/book/man-output.html): XML and saved evidence formats.

## Read the result, not a green exit alone

HTTP success is not application assurance; collection is not ownership; a banner is not patch proof; absence is not remediation. Retain timestamp, source vantage, tools, explicit scope, hostname/SNI, selected address/port, errors and incomplete coverage. Keep originals separate from summaries. The public [tool guide](../../TOOL-GUIDE.md) links complementary scripts.
