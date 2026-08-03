# ADR 0001: One Canonical Cross-Repository Discovery Map

- Status: Accepted
- Date: 2026-08-03
- Owner: Repository maintainers

## Context

An agent may start in any member repository and still need to find the
coordinator, related repositories, source owners, contracts, and integration
checks. Humans need the same route to remain understandable without learning an
agent-specific control plane.

The relationship model is relatively stable, Git-owned configuration. It must
work from sibling checkouts, from isolated repository checkouts, and when a
local coordinator is temporarily unavailable.

## Decision

The coordinator's `CONTEXT-MAP.md` is the single canonical map for repository
membership, discovery, relationships, source authority, and checks.

- A member keeps a thin pointer to coordinator `SYNC.md`.
- `SYNC.md` routes to the canonical context map through a local path first and
  a stable remote fallback second.
- Repository entries use explicit owners, paths, and full canonical HTTPS
  discovery URLs. Filesystem proximity and credentialed Git remotes do not
  establish membership or hosting authority.
- Member repositories remain authoritative for their local product, domain,
  code, permissions, and checks.

## Why This Is the Golden Path

`CONTEXT-MAP.md` already routes context and source authority. Repository
relationships are part of that job. A second relationship map would repeat the
same members, owners, and locations, creating two files that must agree before
an agent can trust either one.

The local route keeps normal workspace navigation fast and available offline.
The remote fallback lets a session discover the system from an isolated member
checkout. The fixed member-to-sync-to-map path is small enough to verify
mechanically.

## Consequences

- Humans and agents have one relationship source to inspect and maintain.
- A session can enter through any member without assuming that repositories are
  siblings or hosted on the same forge.
- Cross-repository work depends on the coordinator map being current and
  reachable locally or remotely. If neither route works, only reversible
  member-local work may continue.
- The coordinator gains discovery authority, not authority over member-local
  truth.
- Membership changes must update the map, member pointer, and relevant
  verification together.

## Alternatives Considered

### Separate `HARNESS-MAP.md`

Not selected. It overlaps with `CONTEXT-MAP.md` on members, relationships,
owners, locations, and checks. The extra name does not create a separate source
of authority, but it does create another drift path.

### Member-to-Member Pointer Mesh

Not selected. Each member would need to know which other members matter, so
membership changes create repeated edits and partial views. Thin member
pointers to one coordinator scale with the number of members instead of their
pairwise relationships.

### Infer Membership from Sibling Directories or Git Remotes

Not selected as authority. Nearby repositories may be unrelated, and a Git
remote may use a credentialed alias or mirror that does not identify the
canonical discovery host. Automatic discovery may propose candidates, but an
explicit owner-controlled map admits them.

### External Registry or Graph Service

Not selected for the default harness. It adds availability, permissions,
schema, and operational ownership to a problem that Git-tracked Markdown and a
deterministic check currently solve. Reconsider it when repository membership
is highly dynamic, map updates become a measured bottleneck, or consumers need
queries and availability guarantees that the file cannot provide.

### No Coordinator

Preferred when no durable relationship, shared state, contract, or integration
check spans repositories. The golden path does not add coordination machinery
to a single repository or a merely convenient workspace.

## Revisit When

Revisit this decision when the canonical map causes measured merge contention
or discovery latency, membership changes faster than the Git review cycle can
support, access boundaries prevent members from reading the coordinator, or a
governed registry becomes the actual source of repository membership.
