# Working scenario: a large distributed enterprise

A generic enterprise scenario, not findings about any named organisation. Use it to map a business that may have inherited multiple services, suppliers and technical estates through growth, acquisitions or migrations. Confirm the facts with accountable owners; public history and naming conventions are not evidence of today's architecture.

## Who / where / when / why

The mapping lead works with heads of service, business continuity, information asset owners, ICT/platform/network/identity teams, procurement/contracts, security operations, property/facilities and commissioned-service owners. Start with a service-scoping workshop and existing registers before issuing technical queries. The decision is what must be protected and recoverable for essential service delivery, with the dependencies and ownership gaps visible.

NIST CSF asset-management outcomes cover inventories, suppliers and authorised data flows [S1]. NCSC asset-management guidance includes critical dependencies and supporting infrastructure [S2]. This is the practical reason to connect network discovery to service ownership, not simply count live hosts. A colour-coded map does not by itself establish assurance or framework conformity.

## Candidate service groups — validate scope and criticality

| Group | Questions for service/technical owners |
|---|---|
| Customer operations and support | Which CRM/case systems, identity, partner transfers, remote access and out-of-hours arrangements support delivery? Who controls supplier recovery? |
| Finance, billing and payments | Which customer/payment channels, back-office systems, file/API integrations, scheduled jobs and banking/provider dependencies exist? |
| Product delivery and outsourced operations | What is enterprise-controlled, partner-operated or separately hosted? Who owns customer data, support access and incident response? |
| Engineering, analytics and document services | Which portals, document stores, data pipelines, integrations and supplier backends support the service? |
| Logistics, manufacturing and field operations | Which dispatch, mobile, telemetry/OT, contractor and connectivity dependencies exist? What is the safe discovery method? |
| Corporate services | Which identity, collaboration/SaaS, HR/payroll, telephony/contact centre, procurement and collaboration dependencies support other services? |
| Branches, training and partner access | Which sites/services are operated internally, outsourced or independently controlled? Keep guest Wi-Fi, partner networks and restricted corporate access distinct. |
| Business continuity and public communications | Which publication, communications, remote access and continuity mechanisms are needed during a major incident? |

These are scoping candidates, not a pre-approved critical-service list or a statement that all are delivered by the same business unit/team. The BIA and responsible service owners determine consequence and recovery requirements.

## Inherited-estate questions

1. Which current legal/service entity is accountable for each system? Retain predecessor organisation as provenance, not as the default current owner.
2. Which legacy names, domains, tenants, forests and contracts remain active, are redirectors, are pending migration or are retired with evidence?
3. Are similarly named systems actually different installations, environments, customer tenants or provider instances? Do not merge on name alone.
4. Which inherited CIDRs/VLANs/sites and overlaps are confirmed in present IPAM, routing and device configuration? A historical allocation is not current scan authority.
5. Do old and new identity systems coexist or synchronise? What are the explicit trusts/federations, privilege paths and migration dependencies?
6. Which suppliers manage infrastructure, applications, patching, PKI/DNS/mail, logging, backup and recovery? Separate enterprise accountability from each provider's contracted responsibility.
7. Which decommission/migration decisions have testable closure evidence: deleted resources, revoked access, removed routes/DNS/publication and retained data/records handled appropriately?
8. Where are ownership and operational knowledge held by individuals? Record responsible teams, escalation/support and recovery documentation rather than exposing personal contact details in public material.

## First pilot: one important public-to-back-office service

Select the service with the owner, using consequence and achievable evidence access. Suggested path to **investigate**, not an assumed implementation:

Customer channel → DNS/certificate → WAF/reverse proxy/LB → application or SaaS → integration/API/file exchange → back-office data → identity/proxy/management → backup/recovery.

For each link record the owner and responsibility split, network context/zone, identity, intended flow, effective control, recent observation and validation status. Include batch/out-of-hours and supplier support paths. Check whether sensitive data is copied into logs, integration staging, exports and backups; data-flow visibility extends beyond the live database.

Parallel views: staff/remote-user access; privileged/supplier administration; identity and synchronisation; dependency failure and service recovery. A working customer web page does not show that the back office, scheduled integrations, MFA or recovery work.

## Initial workshop and evidence requests

- Service owner/BIA: function, impact, data, users, owner, RTO/RPO, dependencies and known changes.
- Network team: approved source inventory, IPAM/VRFs/VLANs/sites, topology, running firewall/NAT/routes, VPN/SD-WAN and proxy paths, telemetry availability and safe pilot scope.
- Identity team: approved directory/tenant scope, topology and trusts, privileged administration, synchronisation/federation, PKI and source permissions; use the [directory guide](directory-discovery.md).
- Platform/cloud/endpoint: management scopes, native ID inventories, resource and software exports, coverage/permissions and exclusions.
- Supplier/procurement: service/contract/tenant ownership, access and data-sharing, responsibilities, incident notification, change, assurance and exit/recovery evidence.
- SOC/resilience: retained logs/flow windows, monitored coverage, backup dependencies and demonstrated restore arrangements.

## Deliverable and review

Produce one owner-reviewed service map and its linked asset/identity/zone/flow records, source collection ledger and prioritised unknowns. RAG must state the assessed criterion; not knowing who owns a critical dependency remains an explicit gap. Then extend by service/site/tenant and reconcile shared dependencies. This scenario uses no organisational exports or real topology; populated records must remain private.
