# ssl_scan_domains.sh

## Who

Engineer authorised to actively probe the listed TLS endpoints. Do not elevate unless a documented collection prerequisite and local approval require it.

## What

Domain DNS/TLS evidence collection. Review its output; it does not automatically remediate findings.

## Where

Kali/Debian or a compatible Bash environment; repository root.

## When

Before or after certificate/TLS changes, or during an authorised exposure review.

## Why

Retain repeatable raw TLS endpoint evidence and readable reports across a domain list.

**Decision supported:** Select endpoints requiring protocol/cipher investigation and compare evidence after changes.

## How

1. Confirm that the host, files or targets are within your authorised scope.
2. Check prerequisites: Bash, sslscan, aha and GNU timeout. Create domains_new.txt with authorised hostnames. Installing dependencies is a separate approved administration action.
3. Open the specified terminal and directory. Inspect the script before running it.
4. Run the command below. These examples do not install dependencies or bypass policy.

```bash
bash ssl_scan_domains.sh domains_new.txt new-tls-results
```

5. Read the output and limitations before deciding the next action. See the [detailed usage guide](../../README.md) for options, schema, collection instructions and exit behaviour.

## Output and interpretation

A new output directory containing raw scanner evidence and HTML. Nonzero exit requires inspection of failed inputs/scans.

Active TLS probes; default endpoint only; a scan is not application assurance.

## Next action

Select endpoints requiring protocol/cipher investigation and compare evidence after changes. Retain the original evidence privately, record collection time and scope, and confirm unexpected results with the relevant owner or an independent check. Record unknowns rather than converting them into a pass/fail claim.

## Changes and recovery

These review/collection tools do not change security configuration or remediate automatically. Network collectors create authorised traffic; file collectors can cause cloud-file hydration. Some tools write reports as documented. Preserve original evidence, use a new private output destination and follow normal retention rules. Shell redirection can overwrite existing files. No rollback of configuration is required because none is performed.

## Validation

Synthetic regression checks; see detailed guide for platform requirements and limitations. Do not interpret synthetic tests as validation of every operating system, trust configuration or target environment.

## Worked example

**Illustrative scenario, not captured evidence:** One hostname times out and later hostnames still produce reports.

**Interpretation:** The timed-out endpoint has incomplete evidence. Later results remain independently useful.

**Next step:** Retain partial output, check the authorised endpoint and collection path, then schedule a bounded retry. Do not classify the timeout as secure.
