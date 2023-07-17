#!/bin/bash

# Read domains from file
DOMAINS=$(cat domains_new.txt)

# Output files
OUTPUT_FILE="sslscan_results.txt"
HTML_OUTPUT_FILE="sslscan_results.html"

# Loop through each domain and perform SSL scan
for DOMAIN in $DOMAINS
do
    echo -e "\033[1mScanning $DOMAIN...\033[0m"
    sslscan -color "$DOMAIN" >> "$OUTPUT_FILE"
done

# Convert the results to HTML
aha -f "$OUTPUT_FILE" > "$HTML_OUTPUT_FILE"

# Clean up the intermediate text file
rm "$OUTPUT_FILE"

