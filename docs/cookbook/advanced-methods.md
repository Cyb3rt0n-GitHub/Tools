# Advanced methods: retain the useful reasoning

These are engineering design/review notes, not tested turnkey collectors. Use the core recipes first. Each topic below needs its own explicit scope, native-version validation and full runbook before becoming an executable public script. No historical customer targets, observations, scan counts or incident conclusions are retained.

## Who, where and when

Senior engineers working with the relevant asset/service owners, on approved collectors. Use these when basic evidence leaves a specific question unanswered. Required permissions and traffic differ by method; ownership of a hostname does not authorise probing a provider's entire shared address range.

## Why these methods matter

| Method | Question and decision supported | How to approach it | Important limits |
|---|---|---|---|
| Reverse DNS and registration | Who should confirm allocation or service ownership? | Compare supplied inventory, DNS, registration and provider/owner records. | Registration, ASN and PTR are clues, not business ownership or remediation authority. |
| Iterative DNS trace | Where does a delegation/resolution problem occur? | Trace the specific authorised name, retain delegation and DNS statuses. | Contacts multiple authoritative services; network filtering and DNSSEC need separate interpretation. |
| Wildcard DNS comparison | Is a discovered name distinct or a wildcard response? | Compare candidate answers with a small approved random-name sample. | Wildcard DNS does not prove identical application routing or make arbitrary names valid assets. |
| Delegated mail and DMARC discovery | Which domain/policy applies to the actual mail flow? | Use actual sender/delegated-domain context, authoritative records and the current policy-discovery standard. | Absence at one exact node is not sufficient; a few parent lookups are not a full standards implementation. |
| Redirect review | Which next application does an endpoint point toward? | First save one response without following; approve each destination before continuing. | Automatic following can leave scope. A redirector can still execute vulnerable server-side code. |
| HTTP security-header review | Which observed response needs application-owner review? | Retain the full response and compare headers against application behaviour and policy. | One response is not every path; missing CSP/HSTS etc. must be assessed in context, not converted to a universal score. |
| CDN/front-door attribution | Is the observed response from the intended service? | Preserve hostname, selected IP/port, SNI, Host header, DNS and response details. | Shared IPs, default pages and intermediary certificates do not automatically belong to the application owner. |
| ProjectDiscovery httpx/tlsx | How can explicit endpoints be identified consistently? | Verify executable identity, installed versions and local flags; use explicit input and separate TLS trust validation. | Fingerprinting/certificate collection can succeed without trusted TLS. Tool flags and versions change. |
| Browser screenshots | What rendered interface was visible? | Use a controlled browser, explicit scope and resource/navigation controls; retain final URL and visually inspect images. | JavaScript, redirects and third-party resources create additional traffic. A saved PNG path is not usable evidence; login fields do not prove absent MFA. |
| Scoped crawling/link checks | Which approved links or paths need investigation? | Fix hostname/path scope, rate and depth; review external-link behaviour and crawl outputs. | Crawlers can load external links or state-changing GET endpoints. Root-only checks do not bound later crawls. |
| FTP/FTPS | Is the named file-transfer listener cleartext, explicit TLS or implicit TLS? | Identify only the approved port, then select the appropriate protocol negotiation with correct identity/trust handling. | Ports 21 and 990 are different workflows. FEAT is not authentication; no credential submission is implied. |
| POP3/IMAP TLS | Does the actual mail-access listener negotiate verified TLS? | Separate implicit TLS from STARTTLS; retain the exact hostname/port and errors. | A successful SMTP test does not validate POP3/IMAP; a handshake is not a mailbox login or delivery test. |
| RPC/SNMP | Is an unexpected management service reachable? | Begin with an authorised narrow port/protocol check and obtain owner context before deeper enumeration. | UDP silence is ambiguous. Community/credential attempts require separate scope; no default-credential probing is included. |
| TLS interception comparison | Is trust failure at the destination or a network intermediary? | Compare fingerprint-matched evidence from independent approved vantage points, keeping SNI and endpoint consistent. | An unexpected issuer alone does not prove destination fault or malicious interception. Do not bypass controls to obtain a preferred result. |
| Native Windows IPv6/HTTPS | Is WSL missing a network capability available on its host? | Use native curl.exe explicitly with correct hostname/SNI and an approved explicit address. | Windows and WSL have different routes/trust/proxy behaviour. A WSL routing error is not remote service failure. |
| Component/runtime supplier assurance | Does the running service actually contain an affected version? | Request package/image build, vendor backport, applicable advisory, deployment time and process-restart evidence. | Banners and cached library names are not confirmed CVEs. Supplier fleet claims are not per-asset closure proof. |
| Dependency installation/repair | Is the collector environment fit to run the chosen check? | Diagnose paths/versions first; use the approved package process and retain before/after evidence. | Package repair changes the host. Do not mix privileged repair, trust-store changes or arbitrary installers into a collection recipe. |

## Batched discovery: completion is a separate check

**Who/when:** an engineer authorised for a defined multi-host discovery exercise, after a small pilot. **Why:** avoid claiming an estate is clear when scans ran out of time or covered the wrong targets/ports.

Before running:

1. Validate an exact supplied allowlist, exclusions, address families and explicit port set offline. Record provenance and a hash. Do not infer permission from DNS/CDN/provider membership.
2. Estimate at least initial IP/port checks divided by the planned probe rate. Allow for retries, adaptive timing and batch overhead. A host timeout can invalidate coverage; removing it trades completeness against runtime and requires an approved operational stop plan.
3. Pilot on a small approved group, including known-open controls. A sample rate is not a universally safe threshold.
4. Keep sequential batches, exact inputs, tool versions, normal/XML outputs, stderr, session and individual exit statuses. Stop failed batches and label partial coverage; do not hide failures behind tee's exit code.

After running, **independently validate**:

- Successful XML runstats and every expected batch/status record.
- Exact intended host coverage: no unexpected hosts, missing hosts, duplicate observations or timed-out hosts.
- Intended port set for each host, including extraports summaries as well as explicit port entries.
- Known controls and whether collection vantage/filtering changed.

Nmap exit zero alone is insufficient. With -Pn, an up/user-set label is not evidence of a host response. Filtered/no-response is not retirement. Rate limits for discovery are not a universal cap on later version/NSE or kernel-generated traffic. Keep service identification and application attribution as separate stages. See [Nmap output](https://nmap.org/book/man-output.html) and [timing guidance](https://nmap.org/book/man-performance.html).

## Template scanning: review before execution

**Why:** technology identification and broad automatic vulnerability testing are different activities. Signed templates establish origin/integrity, not absence of side effects. Excluding selected tags is not proof that the remainder is non-destructive.

Before any public recipe is added, document exact reviewed templates/version, intended request behaviour, target expansion, redirects, authentication, OAST callbacks, headless/code execution, exclusions, rate/concurrency and stop conditions. An automatic technology-to-template mapping is not a guarantee of coverage for a new advisory. Completion, reproducibility and validation of matches need evidence; a template count or progress percentage is not confirmed coverage. No executable automatic scan or exploit template is imported here.

## Evidence handover

Use user-owned approved private destinations, preserve originals, hash both sides of a transfer and verify archive contents. Do not generalise an old workstation's hardcoded public-folder path or change broad filesystem permissions to make a transfer work. Windows ACLs differ from POSIX modes. Review response bodies, cookies, internal DNS, certificate details, usernames and screenshots before sharing.

## Validation status

These are reviewed design notes adapted from a private cookbook. No historical observed result is claimed for a public example. Native collectors and advanced tools require controlled validation before operational release. The [core recipes](README.md) provide the initial executable examples.
