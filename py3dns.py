"""Collect DNS evidence without treating lookup errors as missing controls."""
import argparse
from pathlib import Path
import re
import dns.exception
import dns.resolver

SELECTORS = ("selector1", "selector2", "default", "s1", "s2")


def read_domains(path):
    domains = []
    for number, line in enumerate(Path(path).read_text(encoding="utf-8-sig").splitlines(), 1):
        domain = line.split("#", 1)[0].strip().rstrip(".").lower()
        if not domain:
            continue
        domain = domain.encode("idna").decode("ascii")
        if len(domain) > 253 or not all(re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?", label) for label in domain.split(".")):
            raise ValueError(f"Invalid hostname on line {number}: {domain}")
        if domain not in domains:
            domains.append(domain)
    if not domains:
        raise ValueError("Input contains no domains")
    return domains


def lookup_txt(name, resolver=None):
    resolver = resolver or dns.resolver.Resolver()
    try:
        answer = resolver.resolve(name, "TXT", lifetime=5)
        return [b"".join(record.strings).decode("utf-8", errors="replace") for record in answer], None
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
        return [], None
    except dns.exception.DNSException as exc:
        return [], f"Lookup failed ({type(exc).__name__}); presence unknown"


def collect_records(domain, selectors=SELECTORS, resolver=None):
    records = {}
    for label, name, prefix in (("DMARC", "_dmarc." + domain, "v=DMARC1"),
                                ("SPF", domain, "v=spf1"),
                                ("MTA-STS", "_mta-sts." + domain, "v=STSv1")):
        values, error = lookup_txt(name, resolver)
        records[label] = ([v for v in values if v.split(";", 1)[0].split(" ", 1)[0] == prefix], error)
    for selector in selectors:
        values, error = lookup_txt(f"{selector}._domainkey.{domain}", resolver)
        records[f"DKIM ({selector})"] = ([v for v in values if any(part.strip().startswith("p=") for part in v.split(";"))], error)
    return records


def format_records(records):
    return "".join(f"{label}: {error or (' | '.join(values) if values else 'No matching TXT record at queried name')}\n"
                   for label, (values, error) in records.items())


def fetch_spf_record(domain):
    return next(iter(collect_records(domain, selectors=())["SPF"][0]), None)


def fetch_dns_and_mta_sts_records(domain):
    records = collect_records(domain)
    mta = {"MTA-STS": records.pop("MTA-STS")}
    return format_records(records), format_records(mta)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", default="domains.txt")
    parser.add_argument("--output", default="domain_results.txt")
    parser.add_argument("--selector", action="append", help="DKIM selector; repeat to check multiple (overrides defaults)")
    args = parser.parse_args(argv)
    selectors = args.selector if args.selector is not None else SELECTORS
    if any(not re.fullmatch(r"[A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)*", s) for s in selectors):
        parser.error("Invalid DKIM selector")
    try:
        domains = read_domains(args.input)
        if Path(args.input).resolve() == Path(args.output).resolve():
            raise ValueError("Output must differ from input")
    except (OSError, ValueError, UnicodeError) as exc:
        parser.error(str(exc))
    results = [(domain, collect_records(domain, selectors)) for domain in domains]
    with open(args.output, "w", encoding="utf-8") as output:
        for domain, records in results:
            output.write(f"{domain}\n{format_records(records)}\n")
        output.write("Summary: domains with matching TXT records (presence only, not validation)\n")
        for label in ("DMARC", "SPF", "MTA-STS"):
            present = [domain for domain, records in results if records[label][0]]
            output.write(f"{label}: {len(present)}/{len(results)} — {', '.join(present)}\n")
        output.write("DKIM: only the selected names were checked; absence does not establish that DKIM is disabled.\n")
        output.write("MTA-STS: DNS advertisement only; HTTPS policy and enforcement were not checked.\n")
    print(f"Processed {len(results)} domains. Results: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
