$ErrorActionPreference = 'Stop'
$collector = Join-Path $PSScriptRoot '../scripts/windows/security/Get-FileSignatureInventory.ps1'
$tempFile = Join-Path $env:TEMP ([guid]::NewGuid().ToString() + '.txt')
try {
    [IO.File]::WriteAllText($tempFile, 'synthetic unsigned test data')
    $json = & powershell -NoProfile -File $collector -LiteralPath $tempFile
    if ($LASTEXITCODE -ne 0) { throw 'Collection failed' }
    $report = ($json -join "`n") | ConvertFrom-Json
    if ($report.results.Count -ne 1) { throw 'Wrong result count' }
    if ($report.results[0].sha256 -ne (Get-FileHash -LiteralPath $tempFile -Algorithm SHA256).Hash.ToLowerInvariant()) { throw 'Hash mismatch' }
    if ($report.results[0].signature_status -ne 'NotSigned') { throw 'Expected unsigned synthetic file' }
    $json = & powershell -NoProfile -File $collector -LiteralPath ($tempFile + '.missing')
    if ($LASTEXITCODE -ne 2) { throw 'Missing input did not return collection error' }
    $report = ($json -join "`n") | ConvertFrom-Json
    if (-not $report.results[0].error) { throw 'Missing error evidence' }
} finally { Remove-Item -LiteralPath $tempFile -Force -ErrorAction SilentlyContinue }
