# Zones, boundaries, firewalls and proxies

## Who, where, when and why

Network/security architects, platform owners and service owners use this model during estate mapping, segmentation review and change assessment. Work from configuration/telemetry exports on an approved analysis host. The decision is whether a service's access paths are understood and enforced as intended, not whether a diagram looks segmented.

## Keep four classifications separate

| Field | Meaning | Examples |
|---|---|---|
| zone_id / zone_role | Intended security grouping and use | Public edge, workload, user, management, identity, recovery, guest, supplier, OT |
| local_colour | Organisation-specific diagram legend | Red/amber/green, with text labels; optional |
| plane / privilege_scope | What compromise/control can affect | Control, management, workload; specific privilege scope |
| assessment_status | Dated assessment against a named criterion | Red, amber, green, unknown, not_applicable |

**Illustrative colour convention, not a standard:** red = untrusted/external or guest; amber = controlled ingress/egress and interchange; green = internal restricted workloads. Identity/control, management, backup/recovery and OT must still be distinct named zones where design requires; do not collapse them into a flat green LAN. A device may have interfaces in several zones; record membership per interface/network context. VLAN boundaries alone are not proof of security enforcement. Zero-trust access is still required inside a zone [S4,S7].

**Suggested assessment criteria:** red = evidenced unacceptable exposure/control failure against the agreed criterion; amber = partial evidence, incomplete implementation or action required; green = current sufficient evidence meets that specific criterion; unknown = no adequate evidence; not_applicable = reviewed with rationale. Acceptance of risk does not automatically turn a red condition green. Record severity, confidence, owner, exception and review date separately. Do not translate these colours into a CAF achieved/not-achieved outcome automatically.

## Boundary inventory — what to record

| Component | Configuration evidence | Relationships and questions |
|---|---|---|
| Firewall/virtual appliance | Running rulebase, order, expanded objects/groups, interfaces/zones, VRFs/contexts, NAT, routes, VPNs, HA/sync, logging, policy versions | Which ingress/egress interfaces and translated identities apply? Is the selected rule really effective? What is the default action? |
| Cloud controls | NIC/subnet NSGs or security groups, NACLs, firewall policy, routes, peering/transit, endpoints and org-level controls | Are controls stateful/stateless? Are rules inherited? Are return routes valid? Is there an alternate permitted path? |
| Proxy/SWG/SSE | Explicit/transparent/agent mode, PAC/WPAD, bypass, auth, category/URL rules, TLS inspection, connector/tunnel, service-account path | Which clients/services use it? What bypasses it? Does DNS resolve at client or proxy? Who handles certificates? |
| Reverse proxy/WAF/LB | Listener/VIP, SNI/Host/path routing, TLS termination/re-encryption, backend pool/health, auth, WAF rules | Does public exposure reach a different origin? Can origin access bypass the edge? |
| VPN/ZTNA/remote supplier access | Identity/device policy, route advertisements, split/full tunnel, connector placement, session logs, privilege controls | What access is effective after authentication? Which suppliers or remote users can administer what? |
| Switch/router/SD-WAN | Ports, VLAN/trunks, SVI, ARP/ND, MAC tables, LLDP, VRF, routes and ACLs | Is a link physical or logical? Does routing bypass an expected firewall? Is IPv6 similarly controlled? |

Full exports may contain secrets, keys, internal addressing and personal data. Collect only authorised fields into the register; retain raw source privately. Never place a configuration backup or PAC containing internal details in the public cookbook.

## Flow register: one direction and context per record

Minimum: flow_id, service_id, source selector and zone, destination selector and zone, initiator, transport/port/application, hostname/SNI/path where applicable, address family, address/network context, pre/post-NAT values, ordered enforcement points, rule/policy references, auth/service identity, data classification, purpose, owner, approval/change record, expected decision, observed decision/window, test result, evidence IDs and freshness.

Record return-state behaviour and asymmetric routing; do not mechanically add a reverse "allow all" row. Use multiple hop/segment records for a proxy or TLS-terminating reverse proxy: client-to-proxy and proxy-to-origin are not one socket. Dynamic FQDN/service-tag selectors need a dated resolved set or vendor reference, not a permanent IP assumption. TLS identity and application authorisation are additional checks beyond port reachability.

### Example matrix — no rule changes implied

| Source | Destination | Intended purpose | Example decision | Evidence needed |
|---|---|---|---|---|
| External user | Public WAF listener | Approved public HTTPS service | Allow TCP 443 under edge policy | DNS/VIP/WAF policy, access logs, exact-host test |
| WAF/backend connector | Application listener | Forward approved request | Allow only approved source/path | Backend routing, policy, TLS identity and app logs |
| Application identity | Data service | Approved business transaction | Permit selected service identity/action | DB/API auth, transport rule, audit and transaction evidence |
| User endpoint | Internet | Managed web browsing | Via approved SWG/proxy | PAC/agent/bypass, identity policy, proxy logs |
| User endpoint | Identity admin interface | Unapproved administration | Deny under local design | Boundary/host policy plus approved negative test |
| Privileged admin workstation | PAM/jump path | Approved administration | Allow under strong identity/session policy | Device/identity, elevation/session logs and downstream scope |
| Backup plane | Workload and recovery target | Backup and restore | Explicit approved protocol/direction | Separate job and restore dependencies, isolation and recovery evidence |

AD requires more than one port and can include dynamic RPC and name/time dependencies. Obtain the supported platform/application port requirements; do not turn this illustrative matrix into production firewall rules.

## Validate the path, not one appliance

Compare intended policy, collected effective policy, routes/NAT, observed logs and a narrow test from the actual source zone/user context. Preserve collector, time, source identity/address, destination/port/hostname, rule versions, NAT translation and result. Test IPv4/IPv6 separately where applicable. A permitted rule with no route is not working connectivity; a successful session may have used another route. Logs establish only their captured window/visibility. Negative tests need exact approval; no lateral-movement, authentication attack or automatic firewall change is part of this method.

Primary foundations: NCSC network security, NHS segmentation, Microsoft access planes and cloud diagnostics [S3,S6,S7,S12]. Proposed fields/legend are local design choices. See [sources](sources.md).
