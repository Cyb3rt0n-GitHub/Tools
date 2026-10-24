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
Invoke-Check 'Microsoft Defender status (if available)' {
    Get-MpComputerStatus -ErrorAction Stop |
        Select-Object AMServiceEnabled, AntivirusEnabled, RealTimeProtectionEnabled,
            AntivirusSignatureLastUpdated | Format-List
}
Invoke-Check 'Windows Firewall profiles' {
    Get-NetFirewallProfile -ErrorAction Stop |
        Select-Object Name, Enabled, DefaultInboundAction, DefaultOutboundAction | Format-Table -AutoSize
}
Invoke-Check 'BitLocker status (may require elevation)' {
    Get-BitLockerVolume -ErrorAction Stop |
        Select-Object MountPoint, VolumeStatus, ProtectionStatus, EncryptionPercentage | Format-Table -AutoSize
}
Write-Output 'Collection complete. Unavailable checks are not security findings. Review before sharing.'
