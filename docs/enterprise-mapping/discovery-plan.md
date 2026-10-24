# Source-by-source discovery and reconciliation

## Who / what / where / when / why

An inventory lead coordinates service, network, identity, platform, cloud, endpoint, data and supplier owners. Start from approved exports/APIs and available telemetry, then validate defined gaps. The goal is a defensible evidence model and ownership queue across the agreed estate, not a scan from one privileged server.

## How: collection plan

| Area | Read/query sources | Facts to extract | Gaps to retain |
|---|---|---|---|
| Services and business | Service catalogue, BIA, architecture, contracts, finance/procurement, owner interviews | Service/owner, criticality, RTO/RPO, data, users/suppliers, recovery dependencies | Interview assertions need source/approval; an invoice does not prove current deployment |
| Sites and facilities | DCIM, rack/circuit inventory, building/facilities records | Physical locations, devices, carrier links, power/cooling, access/support dependencies | Network scans do not identify power or key-person dependencies [S2] |
| Network | IPAM, DHCP, DNS, switches/routers/WLC/SD-WAN, NAC, passive sensors | Prefixes by VRF, VLAN/interfaces, routes, ARP/ND/MAC/LLDP, reservations/leases and associations | Tables age; routed scans miss switch paths; IPv6/SLAAC and static devices need other sources |
| Identity | AD, Entra/other IdP, IAM/PAM, PKI, RADIUS, GPO and federation | Domains/trusts, directories, service/device identities, sync, privilege and policy paths | Registered object does not establish liveness or control; privileges/role scope constrain completeness |
| Servers/virtualisation | vCenter/Hyper-V/KVM/platform APIs, host management and configuration tooling | Hosts/clusters/VM IDs, NICs, networks, datastore/storage, resource owner and lifecycle | Templates, snapshots, powered-off VMs and unmanaged hypervisors need explicit handling |
| Endpoints/software | EDR, MDM/Intune, software inventory, NAC and local evidence | Native device IDs, serial/hardware, OS/software, adapters, last observation and management state | Agents see enrolled/supported devices and their telemetry window, not every enterprise asset [S14] |
| Ingress/egress | Firewalls/NAT, WAF/LB, proxies/SWG, VPN/ZTNA and DNS filters | Address translations, listeners/pools, routes, auth, policies and observed decisions | A port allow is not app access; user and service proxy paths differ |
| Cloud | Organisation/tenant/account registry, resource/config inventory, IAM and network APIs | Native resource IDs, networks, peerings, endpoints, identities, policy, region and tags | Missing permission/scope/pagination/recording coverage can look like an empty estate [S10,S11,S13] |
| SaaS and suppliers | IdP enterprise apps, OAuth grants, finance/contracts, SaaS/admin audit, supplier architecture | Tenant/instance, owner, federation, integrations/data transfer, support/access, exit/backup arrangements | SSO catalogues miss non-federated/shadow SaaS; supplied infrastructure is not automatically scan scope |
| Apps/data/containers | App catalogue, Kubernetes/cloud APIs, CI/CD/IaC, DB/storage/secret-manager metadata | Service/API/deployment IDs, ingress, service identity, storage/data and dependency references | Never collect secret values by default; short-lived objects need snapshot time and parent workload |
| Resilience/management | Backup, monitoring, vulnerability tools, remote management, update repositories, PKI/KMS | Protected assets, admin authority, vault/cert dependencies, logging and tested recovery paths | Product enrollment/job success does not prove restore success; management may span all zones |
| OT/IoT/voice/print/guest | OT owners, passive inventory, vendor records, controllers and NAC | Device role/firmware, physical process, network context, supplier remote maintenance | Default active scans can disrupt fragile equipment; use owner/vendor-approved methods |
| External perimeter | Registrars/DNS, certificate inventory, EASM, approved provider records, existing cookbook checks | Public names/IPs, service identity, provider/owner links, exposure and certificate evidence | Certificate/DNS association does not confer ownership or scanning authority |

## One collection ledger row per scoped source run

Record source/system ID, collector identity and tool version, read permissions/roles, expected scope IDs, requested and returned counts, page/token completion, query/filter, time/window/timezone, success/error status, exclusions, raw evidence location/hash, normalisation version and data owner. Denied or unattempted scopes must remain visible. A successful API request is not proof that all pages, accounts or asset types were available.

## Reconciliation examples

- AD computer exists, EDR absent, DHCP observation recent: investigate agent/enrollment or object matching; do not automatically label it an unmanaged live server.
- EDR device seen, AD absent: it may be cloud joined, workgroup, Linux/macOS, a stale join or a source-access gap. Check native IDs and enrollment.
- IPAM entry with no current traffic: could be a quiet service, disconnected asset or stale reservation. Obtain owner/lifecycle evidence before retirement.
- Cloud resource without a CMDB entry: record as a candidate with native ID, tenant/account and evidence; confirm ownership/criticality instead of inventing it from a tag.
- Firewall rule with no hits in the reviewed window: may support recovery, monthly jobs or a log-disabled path. Review owner intent and the full operational cycle.
- Same address in two networks: retain separate VRF/VPC/tenant context and assignment times. Never merge by private IP alone.
- Different source counts: compare scope, object type, stale records, sampling and time before publishing a coverage percentage.

## Tools and organisation

Prefer existing owned platforms and exported evidence before purchasing another inventory product. A CMDB/service catalogue records accountable service relationships; IPAM/DCIM records intended network/physical structure; discovery and endpoint/cloud tools supply observations; graph/diagram tooling presents relationships; ticketing owns unresolved questions. A platform can play several roles, but name the authoritative source per attribute and preserve conflicting observations. We have not evaluated product licensing or recommended a vendor in this research.

## Active validation comes last

Build exact authorised host/service lists from confirmed scope, exclude fragile environments and specify traffic/accounts/windows. Use the cookbook's narrow HTTP/TLS/SSH/TCP recipes and Nmap accounting checker where they answer the question. Broad scans, credentialed collection and protocol-specific enumeration each need an explicit operational plan. Do not extend scope from a discovered trust, route, CIDR or cloud relationship automatically.

## Completion and maintenance

A useful initial milestone is one critical service with owner-reviewed identity, user/admin/data/recovery paths and resolved evidence gaps. Expand by zone/site/account/service. Keep current counts for scopes attempted, permission/page completion, ownership, unresolved identity conflicts, unknown zone membership, critical dependencies without evidence and stale collections. Agree refresh windows by criticality and source churn; there is no universal "scan monthly and done" schedule.

Reference the linked [primary sources](sources.md) and record proposed local thresholds separately from framework outcomes.
