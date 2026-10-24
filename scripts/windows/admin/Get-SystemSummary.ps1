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
Invoke-Check 'Operating system' {
    Get-CimInstance Win32_OperatingSystem -ErrorAction Stop |
        Select-Object Caption, Version, OSArchitecture, LastBootUpTime | Format-List
}
Invoke-Check 'Disk capacity' {
    Get-CimInstance Win32_LogicalDisk -Filter "DriveType=3" -ErrorAction Stop |
        Select-Object DeviceID, @{Name='SizeGB';Expression={[math]::Round($_.Size/1GB,1)}},
            @{Name='FreeGB';Expression={[math]::Round($_.FreeSpace/1GB,1)}} | Format-Table -AutoSize
}
Invoke-Check 'Memory capacity' {
    Get-CimInstance Win32_ComputerSystem -ErrorAction Stop |
        Select-Object @{Name='MemoryGB';Expression={[math]::Round($_.TotalPhysicalMemory/1GB,1)}} | Format-List
}
Write-Output 'Collection complete. Unavailable checks are not security findings. Review before sharing.'
