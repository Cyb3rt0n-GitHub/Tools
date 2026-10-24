<#
.SYNOPSIS
Read-only local diagnostics for Windows. No changes, elevation or remote probes.
.DESCRIPTION
Run from a trusted checkout in PowerShell 5.1+ on Windows. Missing modules or
access restrictions are reported per check; partial output is not assurance.
Native Windows validation is pending for this initial public-library draft.
#>
[CmdletBinding()]
param()
if ($env:OS -ne 'Windows_NT') { throw 'This script requires Windows.' }
function Invoke-Check {
    param([string]$Title, [scriptblock]$Action)
    Write-Output "`n=== $Title ==="
    try { & $Action } catch { Write-Output ("CHECK UNAVAILABLE: " + $_.Exception.Message) }
}
Write-Output ('UTC: ' + [DateTime]::UtcNow.ToString('o'))
Invoke-Check 'Interfaces and DNS settings' {
    Get-NetIPConfiguration -ErrorAction Stop | Format-List
}
Invoke-Check 'IPv4 routes' {
    Get-NetRoute -AddressFamily IPv4 -ErrorAction Stop |
        Select-Object DestinationPrefix, NextHop, InterfaceAlias, RouteMetric | Format-Table -AutoSize
}
Invoke-Check 'Listening TCP ports' {
    Get-NetTCPConnection -State Listen -ErrorAction Stop |
        Select-Object LocalAddress, LocalPort, OwningProcess | Sort-Object LocalPort | Format-Table -AutoSize
}
Write-Output 'Collection complete. Unavailable checks are not security findings. Review before sharing.'
