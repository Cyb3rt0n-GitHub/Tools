import dns.resolver

# Set the path to the input and output files
input_file_path = "domains_new.txt"
output_file_path = "domain_results.txt"

# Open the input and output files
with open(input_file_path, "r") as input_file, open(output_file_path, "w") as output_file:
    # Loop through each line in the input file
    for line in input_file:
        # Get the domain name from the line and strip any whitespace
        domain = line.strip()

        # Query for DMARC, DKIM, and SPF records
        try:
            dmarc_record = dns.resolver.query("_dmarc." + domain, "TXT")
            dmarc = str(dmarc_record[0])
        except:
            dmarc = "No DMARC record found"

        try:
            dkim_record = dns.resolver.query("default._domainkey." + domain, "TXT")
            dkim = str(dkim_record[0])
        except:
            dkim = "No DKIM record found"

        try:
            spf_record = dns.resolver.query(domain, "TXT")
            for record in spf_record:
                if "v=spf1" in str(record):
                    spf = str(record)
                    break
            else:
                spf = "No SPF record found"
        except:
            spf = "No SPF record found"

        # Write the results to the output file
        output_file.write(f"{domain}\n")
        output_file.write(f"DMARC: {dmarc}\n")
        output_file.write(f"DKIM: {dkim}\n")
        output_file.write(f"SPF: {spf}\n\n")
