# Native Windows verified HTTPS evidence

## Who

Windows engineer or service owner authorised to request the selected endpoint. Begin with a standard user account; no administrator rights or execution-policy changes are part of this recipe.

## What

One HTTPS root GET with certificate verification, the configured Windows curl network/proxy behaviour, no redirect following and no authentication. Saves headers, a bounded body, curl metadata, stderr and exit status.

## Where

A standard Windows PowerShell 5.1+ terminal on your approved Windows collector. Use curl.exe explicitly, because curl can be an alias in Windows PowerShell. WSL and native Windows have different network/trust behaviour.

## When

When Windows is your available collector or WSL's route/trust behaviour needs an independent comparison.

## Why

Obtain evidence without first installing a Linux environment, and distinguish HTTP response, certificate validation and network errors. Decide whether the next step is service-owner investigation, route/proxy troubleshooting or certificate review.

## How

Edit the hostname sentinel. This requires Windows curl.exe with the documented flags. It uses a new directory under your profile; it does not set a custom NTFS ACL. Choose an approved private destination if your profile is synchronised/shared.

```powershell
$TargetHost = 'REPLACE_WITH_AUTHORISED_HOST'
if ($TargetHost -eq 'REPLACE_WITH_AUTHORISED_HOST') { throw 'Edit TargetHost first.' }
$CurlPath = Join-Path $env:SystemRoot 'System32\curl.exe'
if (-not (Test-Path -LiteralPath $CurlPath)) { throw 'Windows curl.exe is unavailable.' }
$EvidencePath = Join-Path $env:USERPROFILE ('CyberEvidence\https-' + [guid]::NewGuid().ToString())
New-Item -ItemType Directory -Path $EvidencePath -ErrorAction Stop | Out-Null
(Get-Date).ToUniversalTime().ToString('o') | Set-Content -LiteralPath (Join-Path $EvidencePath 'collected-at.txt')
& $CurlPath --version | Set-Content -LiteralPath (Join-Path $EvidencePath 'curl-version.txt')
& $CurlPath --silent --show-error --connect-timeout 5 --max-time 20 --max-filesize 5242880 `
    --dump-header (Join-Path $EvidencePath 'response.headers') `
    --output (Join-Path $EvidencePath 'response.body') `
    --write-out 'HTTP: %{http_code}\nPeer: %{remote_ip}\nURL: %{url_effective}\n' `
    "https://$TargetHost/" 1> (Join-Path $EvidencePath 'transfer.txt') 2> (Join-Path $EvidencePath 'curl.stderr.txt')
$CurlStatus = $LASTEXITCODE
$CurlStatus | Set-Content -LiteralPath (Join-Path $EvidencePath 'curl-exit.txt')
Write-Output "curl exit: $CurlStatus"
Write-Output "Evidence: $EvidencePath"
```

## Output and interpretation

Inspect transfer.txt, curl.stderr.txt, curl-exit.txt and response files together. Exit zero with HTTP 403 is a completed response, not a healthy application. A certificate error is a failed verified request; do not add --insecure to turn it into a pass. Size/time limits can leave partial files.

**Illustrative example:** curl exit 60 with no valid response means trust/identity validation failed under the collector's conditions. Preserve the error and compare trust, clock, hostname and authorised network vantage. Do not claim the origin is faulty until intermediary behaviour is understood.

## Next decision

Confirm the expected endpoint and owner. Record Location without automatically following it; authorise any destination separately. Ask for actual runtime/package evidence where component status matters. A returned HTML page or missing version header cannot establish patch completion.

## Limits and recovery

GET can generate logs or application effects. Responses can contain cookies, secrets or personal data. Network proxies, trust caches and certificate policy affect the result. The body is saved but never rendered or executed by this command. If a prerequisite or connection fails, retain the exact failure and use an approved collector; do not weaken policy, route or trust settings. Keep or remove only the new evidence folder according to retention rules.

## Validation

Adapted public recipe; Windows syntax validation is included in CI. No live endpoint was contacted to validate this recipe. Historical private runs are not evidence for this rewritten example. [curl reference](https://curl.se/docs/manpage.html).
