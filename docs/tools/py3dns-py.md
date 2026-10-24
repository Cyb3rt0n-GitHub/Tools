# py3dns.py

## Who

Domain owner or engineer reviewing email DNS controls. Do not elevate unless a documented collection prerequisite and local approval require it.

## What

Domain DNS/TLS evidence collection. Review its output; it does not automatically remediate findings.

## Where

Linux/macOS terminal or Windows Python environment; repository root.

## When

During domain onboarding, ownership review or email-security troubleshooting.

## Why

Find gaps or unexpected changes in advertised email DNS controls across an authorised domain list.

**Decision supported:** Identify records needing owner confirmation and deeper policy validation.

## How

1. Confirm that the host, files or targets are within your authorised scope.
2. Check prerequisites: Python 3.10+ and dnspython; install requirements in an approved virtual environment. Create domains.txt containing authorised domain names.
3. Open the specified terminal and directory. Inspect the script before running it.
4. Run the command below. These examples do not install dependencies or bypass policy.

```bash
python py3dns.py domains.txt --output domain_results.txt
```

5. Read the output and limitations before deciding the next action. See the [detailed usage guide](../../README.md) for options, schema, collection instructions and exit behaviour.

## Output and interpretation

Text report at the specified output path. Check per-domain errors before interpreting record counts.

Record presence is not effective protection; unknown selectors and DNS failures prevent absence conclusions.

## Next action

Identify records needing owner confirmation and deeper policy validation. Retain the original evidence privately, record collection time and scope, and confirm unexpected results with the relevant owner or an independent check. Record unknowns rather than converting them into a pass/fail claim.

## Changes and recovery

These review/collection tools do not change security configuration or remediate automatically. Network collectors create authorised traffic; file collectors can cause cloud-file hydration. Some tools write reports as documented. Preserve original evidence, use a new private output destination and follow normal retention rules. Shell redirection can overwrite existing files. No rollback of configuration is required because none is performed.

## Validation

Synthetic regression checks; see detailed guide for platform requirements and limitations. Do not interpret synthetic tests as validation of every operating system, trust configuration or target environment.

## Worked example

**Illustrative scenario, not captured evidence:** A domain returns no DMARC TXT answer while another lookup times out.

**Interpretation:** No answer and a failed lookup are different observations; a timeout leaves presence unknown.

**Next step:** Confirm authoritative DNS and ownership; validate the actual policy before recommending a change.
