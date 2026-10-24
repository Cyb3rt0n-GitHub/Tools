# Directory/DC and local Windows discovery

## Who

Approved directory/network administrators and security reviewers using delegated read permissions. Use RSAT on an approved administration workstation wherever possible. A DC is a high-impact identity system, not a general discovery workstation. Do not install scanners or run broad network sweeps on it as a default approach.

## What / where / when / why

Read AD structure and a scoped computer inventory, then reconcile it with DNS/DHCP, endpoint, virtualisation, cloud and network records. Use during a new estate mapping exercise, domain migration or identity/segmentation review. These documented Microsoft commands are newly assembled examples, not a claim to reproduce an earlier user's complete DC command set. The first collection targets an explicitly supplied directory server; trust/domain results do not authorise automatic traversal.

## How — directory topology

Windows PowerShell 5.1+ with ActiveDirectory RSAT module already installed; authenticated approved domain context and read access to selected objects. Set the sentinel to the approved DC/server, then run the whole block. Query scope and errors are preserved locally. No configuration, passwords, hashes or secret attributes are requested. Large query costs should be piloted with the identity team.

```powershell
$DirectoryServer = 'REPLACE_WITH_APPROVED_DIRECTORY_SERVER'
if ($DirectoryServer -eq 'REPLACE_WITH_APPROVED_DIRECTORY_SERVER') { throw 'Set DirectoryServer first.' }
Import-Module ActiveDirectory -ErrorAction Stop
$EvidencePath = Join-Path $env:USERPROFILE ('CyberEvidence\ad-map-' + [guid]::NewGuid().ToString())
New-Item -ItemType Directory -Path $EvidencePath -ErrorAction Stop | Out-Null
$CollectionStatus = @()
function Save-DirectoryQuery {
    param([string]$Name, [scriptblock]$Query)
    try {
        $Items = @(& $Query)
        ConvertTo-Json -InputObject $Items -Depth 6 | Set-Content -LiteralPath (Join-Path $EvidencePath ($Name + '.json')) -Encoding UTF8
        $script:CollectionStatus += [pscustomobject]@{query=$Name; status='collected'; count=$Items.Count; error=$null}
    } catch {
        $script:CollectionStatus += [pscustomobject]@{query=$Name; status='failed'; count=$null; error=$_.Exception.Message}
    }
}
Save-DirectoryQuery 'forest' { Get-ADForest -Server $DirectoryServer -ErrorAction Stop | Select-Object Name,RootDomain,Domains,Sites,GlobalCatalogs,ForestMode,SchemaMaster,DomainNamingMaster }
Save-DirectoryQuery 'domain' { Get-ADDomain -Server $DirectoryServer -ErrorAction Stop | Select-Object DNSRoot,NetBIOSName,DomainSID,DistinguishedName,DomainMode,PDCEmulator,RIDMaster,InfrastructureMaster }
Save-DirectoryQuery 'domain-controllers' { Get-ADDomainController -Filter * -Server $DirectoryServer -ErrorAction Stop | Select-Object HostName,Site,Domain,Forest,IPv4Address,IPv6Address,IsGlobalCatalog,IsReadOnly,OperatingSystem }
Save-DirectoryQuery 'trusts' { Get-ADTrust -Filter * -Server $DirectoryServer -ErrorAction Stop | Select-Object Name,Source,Target,Direction,TrustType,ForestTransitive,IntraForest,SelectiveAuthentication }
Save-DirectoryQuery 'sites' { Get-ADReplicationSite -Filter * -Server $DirectoryServer -ErrorAction Stop | Select-Object Name,DistinguishedName }
Save-DirectoryQuery 'replication-subnets' { Get-ADReplicationSubnet -Filter * -Server $DirectoryServer -Properties Site,Location -ErrorAction Stop | Select-Object Name,Site,Location,DistinguishedName }
Save-DirectoryQuery 'site-links' { Get-ADReplicationSiteLink -Filter * -Server $DirectoryServer -Properties SitesIncluded,Cost,ReplicationFrequencyInMinutes -ErrorAction Stop | Select-Object Name,SitesIncluded,Cost,ReplicationFrequencyInMinutes }
[ordered]@{collected_at=[DateTime]::UtcNow.ToString('o'); directory_server=$DirectoryServer; collector=$env:COMPUTERNAME; queries=$CollectionStatus} |
    ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $EvidencePath 'collection-status.json') -Encoding UTF8
Write-Output "Evidence: $EvidencePath"
$CollectionStatus | Format-Table -AutoSize
```

The script creates local files and sends authenticated directory queries; it does not prove collection across all forest domains. Select domains/scopes explicitly with their owners and repeat as authorised. A failed query is not an empty result. This block's completion/exit alone is not success: inspect collection-status.json. The output directory uses existing Windows ACLs; put sensitive directory topology in an approved private location.

### Scoped computer pilot — independent block

Start with a small approved OU. Do not silently remove the SearchBase and run an estate-wide query during peak operations. ResultPageSize is a page size, not a deliberate total cap; no ResultSetSize cap is imposed here. Review returned counts and errors.

```powershell
$DirectoryServer = 'REPLACE_WITH_APPROVED_DIRECTORY_SERVER'
$SearchBase = 'REPLACE_WITH_APPROVED_OU_DISTINGUISHED_NAME'
if ($DirectoryServer -like 'REPLACE_*' -or $SearchBase -like 'REPLACE_*') { throw 'Set server and OU first.' }
Import-Module ActiveDirectory -ErrorAction Stop
Get-ADComputer -Server $DirectoryServer -SearchBase $SearchBase -SearchScope Subtree -Filter * -ResultPageSize 200 `
    -Properties OperatingSystem,OperatingSystemVersion,LastLogonDate,whenChanged -ErrorAction Stop |
    Select-Object ObjectGUID,DistinguishedName,DNSHostName,Enabled,OperatingSystem,OperatingSystemVersion,LastLogonDate,whenChanged |
    ConvertTo-Json -Depth 4
```

Output is JSON to the console; use a new approved private destination to save it. Directory OS/version/logon fields can be stale. LastLogonDate is derived from replicated logon metadata and is not a precise liveness clock. Disabled/old objects are not automatically retired; a missing AD computer is not proof that no device exists. Join ObjectGUID with source-scoped identities and other evidence, not solely hostname/IP. This example intentionally avoids DNS-derived IPv4Address as the asset's authoritative network location.

## Optional sources to request separately

| Source | Documented starting point | What it does not prove |
|---|---|---|
| AD-authorised DHCP services | Get-DhcpServerInDC | Does not list non-Windows, unauthorised, standalone or cloud DHCP/SLAAC estate |
| DNS server zones | Get-DnsServerZone -ComputerName APPROVED_DNS_SERVER | Not every zone at a SaaS/provider; a record is not liveness/ownership |
| GPO definitions | Get-GPOReport for an approved domain/GPO scope | GPO definition/link is not endpoint resultant policy; filtering/inheritance and actual refresh matter |
| Windows firewall | Get-NetFirewallRule -PolicyStore ActiveStore with associated address/port/application/service filters | Display names alone do not give effective reachability through network/cloud controls |
| Local proxy context | netsh winhttp show proxy; supported newer systems also expose show advproxy | WinHTTP is not all browser/WinINET/PAC, environment, app-specific or agent/SWG policy |

Check local Get-Help and approved role permissions before using the optional cmdlets. Read-only retrieval can still expose sensitive topology and generate audit/load. No enable/set/reset/import commands belong in initial discovery. Do not export secrets, LAPS passwords, gMSA secret material or private keys. Privileged groups, delegation, AD CS, sync/federation and service accounts deserve separate specifically scoped identity reviews rather than indiscriminate Properties *.

## Output → mapping decisions

| Observation | Record | Validate elsewhere |
|---|---|---|
| AD subnet-to-site relationship | Directory relationship with source/time | IPAM, VLAN/VRF, routes and firewall zones; AD sites are not security zones |
| Domain trust object | Directed trust relationship and relevant properties | Effective authentication/access rights, selective auth and SID/filtering design; do not equate it with unrestricted access |
| DC/GC/FSMO data | Identity-plane roles and replication context | Service owner, effective policy, host state, backup/recovery and network paths |
| Computer object | Registered directory identity/candidate asset link | Endpoint/native inventory and current network observations |
| Replication site link/cost | AD replication configuration | Actual WAN/SD-WAN routes, capacity, outage paths and policy |

## Limits, recovery and validation

No privileged operational collection was run for this pack. PowerShell blocks are syntax-checked in CI; real AD property/role compatibility, scale and native query behaviour need a small owner-approved pilot. Missing RSAT, denied access or unreachable ADWS means incomplete coverage, not "no assets". No automatic module installation, privilege increase, authentication attack or topology change is supplied. Keep exact errors and involve the source owner. Sources: [S8,S9,S16–S19](sources.md).
