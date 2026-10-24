# Personal security tools

Small public utilities by Cyb3rt0n. These collect evidence; they do not certify a domain as secure. Use TLS scans only within your authorised scope.

## Email DNS evidence — `py3dns.py`

Requires Python 3.10+ and dnspython (a third-party package).

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python py3dns.py domains.txt --output domain_results.txt
```

Create `domains.txt` with one hostname per line, for example `example.org`. Blank lines and `#` comments are ignored; duplicate domains are checked once. Supply hostnames, not URLs. The system DNS resolver is used, with a five-second query limit.

DMARC, SPF and MTA-STS TXT records are collected, along with DKIM records at `selector1`, `selector2`, `default`, `s1` and `s2`. To check known selectors instead:

```bash
python py3dns.py domains.txt --selector myselector --selector another
```

Every input domain is included, even without DMARC. Summary counts represent matching record presence, not policy validity. DNS failures are reported as unknown, not absent. TXT chunks are joined before interpretation. DKIM selectors cannot be exhaustively discovered this way; an empty result does not establish that DKIM is disabled. MTA-STS HTTPS policy and enforcement are not checked.

## TLS scans — `ssl_scan_domains.sh`

Requires Bash, `sslscan`, `aha` and GNU `timeout`. On Kali/Debian:

```bash
sudo apt install sslscan aha coreutils
bash ssl_scan_domains.sh domains_new.txt
# Or specify a new output directory:
bash ssl_scan_domains.sh domains_new.txt my-scan-results
```

Input is one ASCII hostname per line, with optional blank lines and `#` comments. Reports go into a new directory; an existing directory is refused to avoid mixing runs. Raw output is retained alongside HTML. Each scan has a 120-second deadline. A failed scan is recorded, later hosts still run, and the script exits nonzero if any input or scan fails. These results describe the supplied hostname's default TLS endpoint; other ports and mail TLS are not assessed.

Generated evidence can contain sensitive details: inspect it before sharing. Neither utility calls an AI service.

## Local checks

```bash
python -m unittest discover -s tests -v
bash -n ssl_scan_domains.sh
```

## Platform script collection

See [scripts/README.md](scripts/README.md) for nine read-only Windows, macOS and Linux admin, network and security collectors, their requirements and validation status. Lab tools have a separate review section. The MIT licence in scripts/LICENSE applies only to that newly authored collection.

## Legacy scanner

The standalone [domain scanner](legacy/domain-scanner/README.md) has moved here from the retired GPT-Tools repository. It collects DNS and TLS evidence without AI integration.
