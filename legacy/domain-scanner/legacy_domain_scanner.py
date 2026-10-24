"""Legacy domain scanner: DNS/TLS evidence."""
import argparse
from datetime import datetime, timezone
from html import escape
import json
from pathlib import Path
import re
import shutil
import subprocess
import dns.exception
import dns.resolver


def read_domains(path):
    domains = []
    for number, line in enumerate(Path(path).read_text(encoding="utf-8-sig").splitlines(), 1):
        domain = line.split("#", 1)[0].strip().rstrip(".").lower()
        if not domain:
            continue
        domain = domain.encode("idna").decode("ascii")
        if len(domain) > 253 or not all(re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?", s) for s in domain.split(".")):
            raise ValueError(f"Invalid hostname on line {number}")
        if domain not in domains:
            domains.append(domain)
    if not domains:
        raise ValueError("No domains supplied")
    return domains


def perform_ssl_scan(domain):
    try:
        result = subprocess.run(["sslscan", "--no-colour", domain], capture_output=True,
                                text=True, errors="replace", timeout=120, check=False)
        return {"output": result.stdout + result.stderr,
                "error": f"sslscan exited {result.returncode}" if result.returncode else None}
    except subprocess.TimeoutExpired as exc:
        output = exc.stdout or b""
        if isinstance(output, bytes):
            output = output.decode("utf-8", errors="replace")
        return {"output": output, "error": "sslscan timed out after 120 seconds"}
    except OSError as exc:
        return {"output": "", "error": f"Could not start sslscan ({type(exc).__name__})"}


def fetch_dns_and_mta_sts_records(domain):
    resolver = dns.resolver.Resolver()
    results = {}
    for label, name, prefix in (("DMARC", "_dmarc." + domain, "v=DMARC1"),
                                ("SPF", domain, "v=spf1"),
                                ("DKIM (default selector only)", "default._domainkey." + domain, None),
                                ("MTA-STS advertisement", "_mta-sts." + domain, "v=STSv1")):
        try:
            values = [b"".join(r.strings).decode("utf-8", errors="replace")
                      for r in resolver.resolve(name, "TXT", lifetime=5)]
            if prefix:
                values = [v for v in values if v.split(";", 1)[0].split(" ", 1)[0] == prefix]
            else:
                values = [v for v in values if any(p.strip().startswith("p=") for p in v.split(";"))]
            results[label] = {"records": values, "error": None}
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
            results[label] = {"records": [], "error": None}
        except dns.exception.DNSException as exc:
            results[label] = {"records": [], "error": f"{type(exc).__name__}: presence unknown"}
    return results


def write_reports(output, results):
    (output / "results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    text = "\n\n".join(f"{r['domain']}\n{json.dumps(r, indent=2, ensure_ascii=False)}" for r in results)
    (output / "domain_results.txt").write_text(text + "\n", encoding="utf-8")
    (output / "sslscan_results.txt").write_text("\n\n".join(
        f"{r['domain']}\n{r['tls']['output']}\n{r['tls']['error'] or ''}" for r in results), encoding="utf-8")
    sections = []
    for r in results:
        sections.append(f"<h2>{escape(r['domain'])}</h2><pre>{escape(json.dumps(r, indent=2, ensure_ascii=False))}</pre>")
    note = "Record presence is not policy validation. Only the default DKIM selector is checked. MTA-STS HTTPS policy is not fetched."
    (output / "domain_results.html").write_text(
        '<!doctype html><html lang="en"><meta charset="utf-8"><title>Legacy domain scanner evidence</title>'
        '<body><h1>Legacy domain scanner</h1><p>' + note + '</p>' + ''.join(sections) + '</body></html>', encoding="utf-8")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", default="domains.txt")
    parser.add_argument("--output-dir", help="New directory; existing paths are refused")
    args = parser.parse_args(argv)
    if not shutil.which("sslscan"):
        parser.error("Install sslscan and ensure it is on PATH")
    try:
        domains = read_domains(args.input)
        output = Path(args.output_dir or datetime.now(timezone.utc).strftime("scan-%Y%m%dT%H%M%S%fZ"))
        output.mkdir(mode=0o700, parents=True, exist_ok=False)
    except (OSError, ValueError, UnicodeError) as exc:
        parser.error(str(exc))
    results = []
    for domain in domains:
        print(f"Collecting evidence: {domain}")
        result = {"domain": domain, "collected_at": datetime.now(timezone.utc).isoformat(),
                  "tls": perform_ssl_scan(domain), "dns": fetch_dns_and_mta_sts_records(domain)}
        results.append(result)
        write_reports(output, results)
    print(f"Reports: {output}")
    return int(any(r["tls"]["error"] or any(v["error"] for v in r["dns"].values()) for r in results))


if __name__ == "__main__":
    raise SystemExit(main())
