# Tools

py3dns.py

Add DNS record querying functionality for domain analysis

- Implemented a Python script to query DMARC, DKIM, and SPF records for a list of domains.
- Utilized the `dns.resolver` module for performing DNS queries.
- Handled exceptions to gracefully handle cases where records are not found.
- Generated an output file with the results of the DNS queries.

This commit introduces a Python script that enables the analysis of DNS records for a list of domains. The script utilizes the `dns.resolver` module, providing a convenient way to perform DNS queries within Python.

The script reads a list of domains from the "domains_new.txt" input file and extracts each domain name. It then queries for the corresponding DMARC, DKIM, and SPF records using the `dns.resolver.query()` method.

For DMARC records, the script queries for the "_dmarc." prefix concatenated with the domain name. If a record is found, it is stored in the `dmarc` variable as a string. In cases where no DMARC record is found, the variable is set to "No DMARC record found".

Similarly, the script queries for DKIM records by appending "default._domainkey." to the domain name. The record is stored in the `dkim` variable if found, or set to "No DKIM record found" if not.

For SPF records, the script queries the domain itself. It iterates through the response to find a record containing "v=spf1". If such a record is found, it is stored in the `spf` variable. If no SPF record with the desired content is found, the variable is set to "No SPF record found".

Finally, the script generates an output file named "domain_results.txt" and writes the domain name, along with the corresponding DMARC, DKIM, and SPF records (or appropriate "Not found" messages) for each domain. Each set of records is separated by newlines for readability.

This functionality can be valuable for domain analysis, security assessments, and monitoring DNS configurations.

Please review the script and provide feedback on its implementation and usage.


