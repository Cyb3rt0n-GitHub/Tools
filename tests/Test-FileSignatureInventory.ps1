$ErrorActionPreference = 'Stop'
$collector = Join-Path $PSScriptRoot '../scripts/windows/security/Get-FileSignatureInventory.ps1'
$tempFile = Join-Path $env:TEMP ([guid]::NewGuid().ToString() + '.ps1')
try {
    [IO.File]::WriteAllText($tempFile, '# Synthetic unsigned script; never executed by this test.')
    $json = & powershell -NoProfile -File $collector -LiteralPath $tempFile
    if ($LASTEXITCODE -ne 0) { throw 'Collection failed' }
    $report = ($json -join "`n") | ConvertFrom-Json
    if ($report.results.Count -ne 1) { throw 'Wrong result count' }
    if ($report.results[0].sha256 -ne (Get-FileHash -LiteralPath $tempFile -Algorithm SHA256).Hash.ToLowerInvariant()) { throw 'Hash mismatch' }
    if ($report.results[0].signature_status -ne 'NotSigned') { throw ('Expected NotSigned for synthetic .ps1; got ' + $report.results[0].signature_status + ': ' + $report.results[0].status_message) }
    $json = & powershell -NoProfile -File $collector -LiteralPath ($tempFile + '.missing')
    if ($LASTEXITCODE -ne 2) { throw 'Missing input did not return collection error' }
    $report = ($json -join "`n") | ConvertFrom-Json
    if (-not $report.results[0].error) { throw 'Missing error evidence' }
} finally { Remove-Item -LiteralPath $tempFile -Force -ErrorAction SilentlyContinue }
# The missing-file case intentionally leaves LASTEXITCODE=2. Do not let the
# workflow wrapper mistake that expected child status for this test's result.
exit 0
