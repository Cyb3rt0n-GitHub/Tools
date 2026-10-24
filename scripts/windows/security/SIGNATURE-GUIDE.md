# Windows file-signature inventory

Why: distinguish file identity and signing observations during software-delivery review, incident triage or a change investigation. Use the SHA-256 to correlate the exact bytes with trusted vendor evidence; use signer/status to decide what needs further provenance checks or analysis. A signature is not a malware verdict.

Requires Windows PowerShell 5.1+ and its Get-FileHash/Get-AuthenticodeSignature cmdlets. Start as a normal user. Supply absolute local file paths; no recursion or execution of inspected files.

```powershell
.\Get-FileSignatureInventory.ps1 -LiteralPath 'C:\Tools\example.exe','C:\Tools\helper.dll'
```

JSON goes to stdout. Save it to a new private file with Out-File if needed; select the path carefully because redirection can overwrite. Exit 0 means collection completed, regardless of signature status. Exit 2 means at least one collection error. Read each result's error field. Investigate unexpected hashes/signers against a trusted source; do not automatically delete, allowlist or execute a file.

No elevation, configuration changes or explicit uploads. Windows trust validation can retrieve certificates/revocation data according to host policy, caches and network availability; this is not guaranteed offline. UNC/network drives and final-component reparse files are refused. Parent reparse points, races and a malicious filesystem remain outside its guarantees. File size/mtime checks detect some concurrent changes but do not create an atomic forensic snapshot. Use stable trusted copies. Valid does not mean safe; NotSigned does not mean malicious. If both embedded and catalog signatures exist, Windows may report the catalog signature.

[Microsoft cmdlet reference](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.security/get-authenticodesignature)

Windows CI exercises an unsigned synthetic PowerShell file, its SHA-256 and missing-file error handling. These checks do not establish all signing/trust-policy behaviours. Operational validation on target versions remains required.
