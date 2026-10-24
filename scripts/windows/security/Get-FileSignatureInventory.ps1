<#
.SYNOPSIS
Collect SHA-256 and Authenticode observations for explicitly selected local files.
.DESCRIPTION
Does not run the files, recurse, elevate or change configuration. Trust validation may
use Windows certificate caches, policy and network retrieval. Output is JSON on stdout.
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)]
    [ValidateNotNullOrEmpty()]
    [string[]]$LiteralPath
)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
if ($env:OS -ne 'Windows_NT') { throw 'This collector requires Windows.' }
$results = @()
$failed = $false
foreach ($candidate in $LiteralPath) {
    $record = [ordered]@{
        input_path = $candidate; path = $null; bytes = $null; sha256 = $null
        signature_status = 'Unknown'; status_message = $null
        signer_subject = $null; signer_thumbprint = $null
        timestamp_subject = $null; collected_at = [DateTime]::UtcNow.ToString('o')
        error = $null
    }
    try {
        # Only local drive paths: avoid accidental UNC/network-share traversal.
        if ($candidate -notmatch '^[A-Za-z]:[\\/]') { throw 'Use an absolute local drive path.' }
        $item = Get-Item -LiteralPath $candidate -Force
        if ($item.PSProvider.Name -ne 'FileSystem' -or $item.PSIsContainer) { throw 'Expected a filesystem file.' }
        if (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) { throw 'Reparse-point files are not collected.' }
        $root = [IO.Path]::GetPathRoot($item.FullName)
        if (([IO.DriveInfo]::new($root)).DriveType -eq [IO.DriveType]::Network) { throw 'Network drives are not collected.' }
        $record.path = $item.FullName
        $lengthBefore = $item.Length
        $modifiedBefore = $item.LastWriteTimeUtc
        $hash = Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256
        $signature = Get-AuthenticodeSignature -LiteralPath $item.FullName
        $after = Get-Item -LiteralPath $item.FullName -Force
        if ($after.Length -ne $lengthBefore -or $after.LastWriteTimeUtc -ne $modifiedBefore) { throw 'File changed during collection; retry on a stable copy.' }
        $record.bytes = $lengthBefore
        $record.sha256 = $hash.Hash.ToLowerInvariant()
        $record.signature_status = $signature.Status.ToString()
        $record.status_message = $signature.StatusMessage
        if ($null -ne $signature.SignerCertificate) {
            $record.signer_subject = $signature.SignerCertificate.Subject
            $record.signer_thumbprint = $signature.SignerCertificate.Thumbprint
        }
        if ($null -ne $signature.TimeStamperCertificate) { $record.timestamp_subject = $signature.TimeStamperCertificate.Subject }
    } catch {
        $record.error = $_.Exception.Message
        $failed = $true
    }
    $results += [pscustomobject]$record
}
[ordered]@{
    schema = 1
    interpretation = 'Signature observations are not a malware verdict. Valid does not mean safe; NotSigned does not mean malicious. Validation depends on host trust, policy, clock, caches and network availability.'
    results = @($results)
} | ConvertTo-Json -Depth 6
if ($failed) { exit 2 }
