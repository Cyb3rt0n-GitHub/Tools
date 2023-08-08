import dns.resolver

def query_dns_record(domain, record_type):
    try:
        result = dns.resolver.resolve(domain, record_type)
        return [str(record) for record in result]
    except dns.resolver.NXDOMAIN:
        return []
    except Exception as e:
        return [f"Error: {str(e)}"]

def main():
    # Set the path to the input and output files
    input_file_path = "domains.txt"
    output_file_path = "domain_results.txt"

    # Open the input and output files
    with open(input_file_path, "r") as input_file, open(output_file_path, "w") as output_file:
        # Loop through each line in the input file
        for line in input_file:
            # Get the domain name from the line and strip any whitespace
            domain = line.strip()

            # Query for DMARC, DKIM, and SPF records
            dmarc_records = query_dns_record("_dmarc." + domain, "TXT")
            dmarc = "\n".join(dmarc_records) if dmarc_records else "No DMARC record found"

            dkim_records = query_dns_record("default._domainkey." + domain, "TXT")
            dkim = "\n".join(dkim_records) if dkim_records else "No DKIM record found"

            spf_records = query_dns_record(domain, "TXT")
            spf = next((str(record) for record in spf_records if "v=spf1" in str(record)), "No SPF record found")

            # Write the results to the output file
            output_file.write(f"{domain}\n")
            output_file.write(f"DMARC:\n{dmarc}\n")
            output_file.write(f"DKIM:\n{dkim}\n")
            output_file.write(f"SPF:\n{spf}\n\n")

if __name__ == "__main__":
    main()
