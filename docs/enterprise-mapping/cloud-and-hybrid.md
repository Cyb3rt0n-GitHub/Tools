# On-premises, hybrid, cloud and SaaS mapping

## Who / what / where / when / why

Cloud/platform and identity administrators provide approved read/query exports to the mapping lead. Start at account/tenant ownership, then networks, resources, IAM, services and dependencies. Do this when discovering an estate, reviewing a landing zone or tracing cross-premises service access. The decision is whether the full service/control path and its uncollected scopes are understood. A cloud icon on a diagram is not sufficient.

## On-premises baseline

Map sites/racks, physical and virtual hosts, hypervisors/clusters, storage, vSwitches/port groups/VLANs, network uplinks, VM NICs, containers, backup/management and out-of-band interfaces. Use native IDs scoped to the management system. A hypervisor export misses standalone hosts and a VM name is not a unique enterprise ID. Keep power, cooling, carrier and key-person dependencies where critical to the service [S2].

## Hybrid: record each connection and identity bridge

- VPN/ExpressRoute/Direct Connect/interconnect/SD-WAN endpoint and provider, route/BGP advertisement, VRF and overlapping prefixes, NAT, failover and return path.
- AD–Entra/other IdP sync or provisioning, federation, service principals/workload federation, private service connectors, App Proxy/ZTNA connectors and privileged administration. Network peering is not an identity trust; directory trust is not a network route.
- DNS public/private zones, conditional forwarders/resolvers, split-horizon responses, private endpoint zones, time, PKI/KMS/HSM and certificate validation dependencies.
- Outbound proxy/SWG, inspection, egress/NAT identity, direct exceptions, SaaS endpoints, management/update/telemetry and software supply-chain access.
- Recovery paths that still work if production AD, network control or the cloud tenant is impaired. Configuration inventory does not prove restore capability.

Microsoft documents hub/spoke as one pattern, including shared connectivity and services. Peering and routing must be checked, not inferred; do not impose that architecture on an estate without evidence [S15].

## Cloud collection matrix

| Platform | Start with | Then obtain | Coverage limits |
|---|---|---|---|
| Azure | Approved tenant/subscription registry and role visibility; Resource Graph resource/parent IDs | VNet/subnet/NIC/public IP, peerings/routes, NSGs/admin rules/firewalls, VPN/ExpressRoute, private endpoints/DNS, WAF/LB, IAM/managed identities, policy, diagnostics and PaaS | Resource Graph sees authorised scope and can return partial visibility; handle pagination and unsupported/stale properties [S10] |
| AWS | Approved organisation/accounts/regions, enabled Config recorder coverage and aggregator scopes | VPC/subnet/ENI/route, SG/NACL, NAT/IGW/transit/peering/VPN/DX, LB/WAF/endpoints, IAM/roles/resource policies, services and logs | Aggregation only covers included/recorded accounts, regions and resource types; no universal completeness claim [S11] |
| Google Cloud | Approved organisation/folders/projects and Asset Inventory access | Networks/subnets/routes/peering/VPN/interconnect, firewall policies, interfaces/LB/Cloud NAT, IAM/service accounts and service/data dependencies | Asset freshness and supported types vary; relationships have entitlement/support restrictions. It is not designed as a real-time enforcement view [S13] |
| SaaS | Provider/tenant, accountable owner, contract and IdP/admin inventory | Federation/OAuth/API integrations, service accounts, privileged support, data classification/location, logs/retention, backup/export/exit and incident responsibility | Cloud infrastructure APIs do not inventory SaaS in general; SSO inventory misses non-federated services |

## Azure discovery query — explicit pilot, not a complete exporter

Run in Azure Resource Graph Explorer with the approved subscriptions selected and read access. This KQL query does not deploy or change resources:

```kusto
Resources
| project id, name, type, subscriptionId, resourceGroup, location, tags
| order by id asc
```

Use returned native resource IDs as joins. Export all pages through a supported API/CLI process and retain scope, returned total/truncation/token state and errors. A portal preview or top/first page is not the whole estate. Compare subscriptions with an independently approved subscription register; a successful authorised query may omit scopes you cannot read without declaring them [S10]. Treat tags as assertions until owner-confirmed. Detailed properties, IAM, network effective rules and Entra/Microsoft 365 are separate evidence, not implied by this list.

## Configuration analysis versus actual traffic

Azure Network Watcher provides routing/filtering/connection diagnostics [S12]. Some diagnostics are configuration analyses; others create probe traffic or diagnostic resources and have permissions/operational/cost implications. Do not run all features as if they were passive exports. AWS Reachability Analyzer models configuration rather than sending data-plane packets and has documented scope/protocol limits [S20]. Neither establishes a successful application transaction or universal end-to-end coverage.

Use existing flow telemetry to corroborate configured paths. For new Azure logging designs, use the current VNet flow-log guidance: Microsoft states that new NSG flow-log creation is no longer supported and existing NSG flow logs retire on 30 September 2027 [S21]. Enabling/migrating logging is a separate change, not a discovery prerequisite performed silently. Preserve sampling, retention, missing intervals, NAT and source/destination identity context.

## Output → next decision

Trace one service across user access, workload/data, administration/control and recovery. A public hostname can resolve to an edge while the origin is private; one SaaS app can depend on on-premises federation or DNS; a cloud VM can be administered by an on-premises RMM platform. Record each independently evidenced relationship, responsible party and policy boundary. Reconcile absent resources with scope/access/recording gaps before declaring deletion.

## Limits and validation

This is a researched collection plan, not a tested multi-cloud exporter. No cloud account was queried and no agents, log resources, roles or diagnostic analyses were deployed. Actual deployment patterns and service-specific limits require owner review and current vendor documentation. See [sources](sources.md).
