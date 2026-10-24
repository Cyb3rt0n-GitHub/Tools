# Check saved Nmap TCP scope and coverage accounting

## Who

Security engineers reviewing their own authorised discovery evidence or a supplied scan handover. No administrator rights or Nmap installation are required for this offline check.

## What

Compare saved TCP Nmap XML with an independently supplied exact IP allowlist and intended port set. Check successful runstats, host summary, per-host timeout/status, explicit ports plus extraports counts, missing/unexpected hosts and duplicate observations across batches. Print JSON with input hashes and reasons to investigate. No scan is run and no targets are contacted.

## Where

From the repository root, in a terminal with Python 3.10+. Standard library only, no extra packages. Use trusted saved XML; keep both raw scan outputs and approved scope evidence separately. Native Windows/macOS validation remains pending.

## When

Before reporting a scan as covering the intended estate, after a timeout, or when reconciling batch results and unexpected gaps.

## Why

An exit-zero scan can still leave intended hosts or ports unaccounted for. This check helps decide whether results are usable for the stated scope or whether recollection/investigation is needed. It does not convert a scan into an assurance verdict.

## How

First try the synthetic example. It reads local documentation data only:

```bash
python3 scripts/cross-platform/security/check_nmap_coverage.py \
  --targets scripts/cross-platform/security/examples/nmap-targets.txt \
  --ports 22,80,443 \
  scripts/cross-platform/security/examples/nmap-synthetic.xml
```

For real evidence, prepare a text file containing one explicit approved IPv4/IPv6 address per line. Comments after # and blanks are allowed. Hostnames, CIDRs, scoped IPv6 and duplicates are rejected. Supply the **intended** TCP ports/ranges, not a port list copied blindly from the output being checked. Supply each intended XML batch once. Review the file list before running; shell glob behaviour differs between operating systems.

```bash
python3 scripts/cross-platform/security/check_nmap_coverage.py \
  --targets /private/scope/approved-ips.txt --ports 22,80,443,8000-8002 \
  /private/evidence/batch-001.xml /private/evidence/batch-002.xml
```

Replace paths and ports with your approved scope. Output is JSON on stdout. Save to a **new** private destination if needed; shell redirection can overwrite files. Exit 0 means the supported accounting checks are consistent; 1 means incomplete/inconsistent evidence; 2 means invalid input or a read/parse failure. Any nonzero exit needs investigation before reporting coverage.

## Output and interpretation

The synthetic example reports status consistent, one expected address and three ports. Its explicit port 443 is open and two other ports are represented by a closed extraports count. The host-up reason is user-set, deliberately demonstrating that -Pn is not evidence of a response. These are fictional observations, not live findings.

The report includes the expected scope, missing/unexpected/duplicate targets, XML hashes, Nmap version/start time, per-file issues and per-host state counts. explicit_open_ports lists only individually enumerated open ports; an aggregate open extraports group has no specific port identities and is not expanded by guesswork.

**Illustrative failure:** one expected IP is absent and a host has timedout=true. The report is incomplete_or_inconsistent. Keep the partial results, establish the collection problem, and recollect within the approved scope rather than calling the host retired or secure.

## Next decision

If inconsistent, inspect the specific file/host issues and original stderr/session. Check exclusions, permissions, command scope, time budget and collector vantage. Rescan only under the approved procedure. If consistent, continue with service identification and evidence interpretation; independently confirm scope provenance and whether the scan method actually answers your question.

## Limits and recovery

- Supports one TCP scaninfo per document and requires every intended host to have accounted-for port observations. Mixed TCP/UDP, host-discovery-only, down hosts and repeated-target scans are flagged or unsupported. Separate legitimate repeat scans before comparison; do not merge them silently.
- Aggregate extraports provide counts, not an independently verified list of identities or packet evidence. Matching totals plus declared scope is an accounting check, not proof that all packets were delivered. A crafted/incorrect XML can still describe consistent results.
- XML hashes identify compared bytes, not authenticity, authorisation or ownership. Successful runstats do not establish accurate detection. Missing XML files are detectable only through the supplied scope/observations; no external batch-status log is consumed.
- Does not assess NSE completion, service/version coverage, scripts' side effects, vulnerability coverage, UDP, revocation, application health or remediation. Filtered/no-response does not establish retirement.
- 20 MiB per XML file. UTF-8/ASCII XML only; entities and external/nonstandard DTDs are rejected. The ordinary `<!DOCTYPE nmaprun>` is allowed. Read only trusted evidence; do not treat this as a general hostile-XML processing service.
- This tool reads local files and prints a report; there are no configuration changes to roll back. Keep originals. For malformed or unsupported evidence, preserve the exact error and use a supported/manual review route rather than editing evidence to manufacture a pass.

## Validation

Synthetic tests exercise successful aggregate accounting, timeouts, failed runs, incorrect scope, duplicate batches, wrong protocols/ports, missing states, invalid summaries, malformed XML and entity/DTD rejection. No live scans were performed. See the [Nmap XML reference](https://nmap.org/book/output-formats-xml-output.html) and [advanced completion guidance](advanced-methods.md#batched-discovery-completion-is-a-separate-check).
