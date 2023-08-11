import dns.resolver

def fetch_spf_record(domain):
    spf_record = None
    resolvers = [dns.resolver.Resolver(), dns.resolver.Resolver(configure=False)]
    resolvers[0].nameservers = ["8.8.8.8"]  # First resolver uses Google Public DNS
    resolvers[1].nameservers = ["8.8.4.4"]  # Second resolver uses another Google Public DNS server

    try:
        for resolver in resolvers:
            try:
                txt_records = resolver.resolve(domain, "TXT")
                for record in txt_records:
                    if "v=spf1" in str(record):
                        spf_record = record
                        break
                if spf_record:
                    break
            except dns.resolver.NXDOMAIN:
                continue
            except dns.resolver.LifetimeTimeout:
                continue

    except dns.resolver.NoAnswer:
        pass

    return spf_record

def fetch_dns_and_mta_sts_records(domain):
    dns_records_info = ""
    mta_sts_info = ""

    resolvers = [dns.resolver.Resolver(), dns.resolver.Resolver(configure=False)]
    resolvers[0].nameservers = ["8.8.8.8"]  # First resolver uses Google Public DNS
    resolvers[1].nameservers = ["8.8.4.4"]  # Second resolver uses another Google Public DNS server

    try:
        # Query for DMARC record from multiple resolvers
        dmarc_record = None
        for resolver in resolvers:
            try:
                dmarc_record = resolver.resolve("_dmarc." + domain, "TXT")
                break
            except dns.resolver.NXDOMAIN:
                continue

        if dmarc_record:
            dns_records_info += f"DMARC: {str(dmarc_record.response.answer[0][0])}\n"
        else:
            dns_records_info += "DMARC: None Found\n"

        dkim_selectors = [
            "selector1",    # Microsoft (Outlook/Exchange)
            "selector2",    # Microsoft (Outlook/Exchange)
            "default",      # Default DKIM selector (you can remove this if not needed)
            "mxvault",      # Global Micro
            "mandrill",     # Mandrill
            "sendgrid",     # SendGrid
            "s1",           # SendinBlue
            "s2",           # SendinBlue
            "k1",           # Custom Provider (Example)
            "k2",           # Custom Provider (Example)
            "k3",           # Custom Provider (Example)
            "pp",           # Postmark
            "dkim",         # Hetzner
            "amazonses",    # Amazon SES
            "yahoo",        # Yahoo
            "sparkpost",    # SparkPost
            "zoho",         # Zoho
            "authsmtp",     # AuthSMTP
            "dynect",       # DynECT Email Delivery
            "socketlabs",   # SocketLabs
            "turbosmtp",    # TurboSMTP
            "vzrelay",      # Verizon
            "emarsys",      # Emarsys
            "yandex",       # Yandex.Mail
            "postmark",     # Postmark
        ]
        dkim_found = False
        for selector in dkim_selectors:
            dkim_record = None
            for resolver in resolvers:
                try:
                    dkim_record = resolver.resolve(f"{selector}._domainkey." + domain, "TXT")
                    break
                except dns.resolver.NXDOMAIN:
                    continue
                except dns.resolver.NoAnswer:
                    continue
                except dns.resolver.LifetimeTimeout:
                    continue

            if dkim_record and str(dkim_record.response.answer[0][0]) != "No DKIM record found":
                dkim_found = True
                dns_records_info += f"DKIM ({selector}): {str(dkim_record.response.answer[0][0])}\n"
        
        if not dkim_found:
            dns_records_info += "DKIM: None Found\n"

    except dns.resolver.NoNameservers:
        pass  # Handle DNS resolution error here if needed

    spf_record = fetch_spf_record(domain)
    if spf_record:
        dns_records_info += f"SPF: {str(spf_record)}\n"
    else:
        dns_records_info += "SPF: None Found\n"

    try:
        mta_sts_response = dns.resolver.resolve("_mta-sts." + domain, "TXT")
        mta_sts_records = [rdata.to_text().strip('\"') for rdata in mta_sts_response]
        if mta_sts_records:
            mta_sts_info = "\n".join(f"MTA-STS: {record}" for record in mta_sts_records)
        else:
            mta_sts_info = "MTA-STS: None Found\n"
    except dns.resolver.NXDOMAIN:
        mta_sts_info = "MTA-STS: None Found\n"
    except dns.resolver.NoNameservers:
        mta_sts_info = "MTA-STS: DNS resolution failed. None Found\n"
    except dns.resolver.Timeout:
        mta_sts_info = "MTA-STS: DNS resolution for MTA-STS timed out\n"
    except dns.resolver.NoAnswer:
        mta_sts_info = "MTA-STS: None Found\n"

    return dns_records_info, mta_sts_info

def main():
    input_file_path = "domains.txt" # Make this as a list of domains to check
    output_file_path = "domain_results.txt" 

    domains_with_dmarc = []
    domains_with_spf = []
    domains_with_dkim = []
    domains_with_mta_sts = []

    with open(input_file_path, "r") as input_file:
        total_domains = sum(1 for _ in input_file)  # Count the total number of domains
        input_file.seek(0)  # Reset the file pointer for reading

        print("Fetching DNS and MTA-STS records...")
        for index, line in enumerate(input_file, start=1):
            domain = line.strip()
            dns_info, mta_sts_info = fetch_dns_and_mta_sts_records(domain)

            if "DMARC: None Found" not in dns_info:
                domains_with_dmarc.append(domain)
            if "SPF: None Found" not in dns_info:
                domains_with_spf.append(domain)
            if "DKIM: None Found" not in dns_info:
                domains_with_dkim.append(domain)
            if "MTA-STS: None Found" not in mta_sts_info:
                domains_with_mta_sts.append(domain)

            # Display progress update
            print(f"Processed domain {index}/{total_domains}: {domain}")

    with open(output_file_path, "w") as output_file:
        print("Writing results to the output file...")
        for domain in domains_with_dmarc:
            dns_info, mta_sts_info = fetch_dns_and_mta_sts_records(domain)
            
            output_file.write(f"{domain}\n")
            output_file.write(f"{dns_info}")
            output_file.write(f"{mta_sts_info}\n\n")

        output_file.write("\nDomains with DMARC records:\n")
        output_file.write(f"Total: {len(domains_with_dmarc)}\n")
        for domain in domains_with_dmarc:
            output_file.write(f"{domain}\n")
        output_file.write("\n")

        output_file.write("Domains with SPF records:\n")
        output_file.write(f"Total: {len(domains_with_spf)}\n")
        for domain in domains_with_spf:
            output_file.write(f"{domain}\n")
        output_file.write("\n")

        output_file.write("Domains with DKIM records:\n")
        output_file.write(f"Total: {len(domains_with_dkim)}\n")
        for domain in domains_with_dkim:
            output_file.write(f"{domain}\n")
        output_file.write("\n")

        output_file.write("Domains with MTA-STS records:\n")
        output_file.write(f"Total: {len(domains_with_mta_sts)}\n")
        for domain in domains_with_mta_sts:
            output_file.write(f"{domain}\n")
        output_file.write("\n")

    print("Tool has completed. Results saved to the output file.")

if __name__ == "__main__":
    main()
