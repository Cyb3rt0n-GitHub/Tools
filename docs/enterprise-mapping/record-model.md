# Linked register and evidence model

Proposed engineering schema, not a mandated industry standard. Use it in an existing controlled CMDB/graph/data store or a small private initial register; the public JSON files are empty/fictional examples only. Do not create competing authoritative inventories without agreeing system ownership.

## Core collections

| Collection | Minimum useful fields and joins | Why |
|---|---|---|
| scopes | scope_id, entity, authorised systems/sites/accounts, exclusions, collection/test permissions, approver, expiry | Separate what is known from what can be collected/tested |
| services | service_id, purpose, business/technical/data owner, criticality, users, data classes, RTO/RPO, supplier refs, lifecycle | Connect technical findings to business impact |
| assets | asset_id, source-native IDs, type, names/aliases, platform/location/account, lifecycle, owner refs, evidence refs | One logical entity with auditable cross-source identities |
| interfaces | interface_id, asset_id, network_context_id, network_id, MAC/IP assignments with valid_from/to, zone refs | Multihoming, IPv6, NAT and address reuse cannot be one hostname/IP cell |
| networks | network_id, prefix, address family, VRF/tenant/account context, VLAN/VNet/VPC, site, route refs | Prevent merging overlapping private address spaces |
| zones | zone_id, role, local colour/legend, owner, criteria, network/interface membership refs | Record intended segmentation without implying trust |
| boundaries | boundary_id, device/service refs, zones/interfaces, enforcement type, HA/context, policy/version refs | Identify where and how a path is controlled |
| identities | identity_id, provider/native ID, type (human/group/device/workload), owner, privilege/plane, federation refs | Model authentication and admin authority separately from packets |
| flows | flow_id, source/destination selectors, initiator/protocol/ports/app, NAT/hops, identity, intent/config/observation/test evidence, owner | Preserve multi-level traffic evidence and exceptions |
| relationships | relation_id, from_id, to_id, relation_type, scope, direction, valid time, evidence and confidence | hosted_on, depends_on, authenticates_via, administers, backs_up, routes_via etc. |
| suppliers | supplier_id, service/contract refs, responsibility split, access/data scope, incident/exit/support arrangements | An external service dependency needs accountable boundaries |
| collections | collection_id, source/scope, permissions/query/version, time/window, pages/counts, status/errors, evidence refs | Explain discovery coverage rather than assuming it |
| evidence | evidence_id, private location, hash, source/collector, observation/collection time, method, scope, sensitivity/retention | Keep a conclusion traceable without publishing raw evidence |
| assessments | assessment_id, subject/criterion, RAG, confidence, reason, evidence, owner, action/exception, reviewed/expiry | Separate risk/control evaluation from topology colouring |
| issues | issue_id, type, conflicting claim refs, impact, owner, next action, due/status | Drive unresolved identity, ownership, scope and freshness gaps |

## Record claims explicitly

For attributes that matter, retain the statement and its evidence: subject, attribute, value, source_id, observed_at, collected_at, valid_from/to if known, method, scope and confidence. Do not let a normalised "current" view erase contradicting source observations. Owner-approved intent and observed state can differ legitimately and need separate fields.

Proposed knowledge states: unknown, reported, observed, corroborated, owner_confirmed, validated_for_context, stale, conflicting. These are not numeric probabilities and are separate from red/amber/green assessment. A validated network connection still does not establish every business/control claim about that service.

## Joins that avoid false maps

- Prefer native IDs scoped to their provider/directory/management domain: AD ObjectGUID plus forest context; cloud resource ID plus tenant/account; hypervisor UUID plus manager; device/agent ID with source. Preserve creation/deletion/recreation history.
- Serial, MAC and hostname are useful correlation clues, but can be missing, virtual, reused, renamed or duplicated. Auto-join only when identity rules are strong; queue ambiguous candidates for review.
- IP identity requires address family, network context and assignment time. Keep NAT public/private tuples and load-balancer/backend relationships separately. One public IP may serve many owners/applications.
- Service ownership is an explicit relationship approved by a responsible party; do not infer ownership solely from DNS suffix, naming convention, certificate SAN or a cloud tag.
- Record domains, trusts and federation as directed relationships with scope and properties. They do not prove blanket access. Admin/control relationships can span networks without a simple persistent data-flow edge.

## Freshness and RAG examples

An old AD object can remain valid identity evidence but weak liveness evidence. A firewall export is configured-state evidence for its collected version, not necessarily today's running configuration. A backup job may be green for job execution yet unknown for restore readiness. Expire evidence per source/claim and service criticality, not by applying one global scan date.

For an ownership assessment, green might require a named accepted accountable owner and in-date review. For a boundary assessment, green requires the specific policy/route/log/test evidence agreed by that control owner. A colour without criterion, evidence and review time is not an assessment.

## Diagrams generated from records

Maintain a high-level service/context view; site and WAN/hybrid view; zone/boundary view; per-service user/data flow; identity/privileged administration view; recovery dependency view. Give every diagram scope, version/as-of time, owner, legend and unresolved assumptions. Link each node/edge to register IDs. Do not publish internal topology merely because the generic templates are public.

## Validation and review

The empty template names the collections. The fictional example demonstrates joins and different evidence levels; it is not an authoritative production schema or any organisation's estate. Local structural checks confirm IDs/references in the example; service owners must validate a populated model. Initial acceptance: one critical service with accountable ownership, explicit dependencies, boundary paths, collection gaps and recovery assumptions. Then expand the scope systematically.
