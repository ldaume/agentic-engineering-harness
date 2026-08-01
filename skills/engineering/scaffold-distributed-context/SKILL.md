---
name: scaffold-distributed-context
description: Establishes the smallest reliable domain-context system across repositories without confusing repositories, bounded contexts, generated graphs, or agent instructions with canonical truth. Use when agents must reason across services, applications, shells, microfrontends, or code hosts; when creating a cross-repository context map, domain glossary, contracts, or projections; or when evaluating Graphify, Zoekt, Sourcegraph, Backstage, or policy tooling for context discovery and governance.
---

# Scaffold Distributed Context

Build from canonical domain language and executable boundaries. Add retrieval
or catalog tooling only when observed work cannot find or verify the needed
relationships reliably.

## 1. Ground Scope and Authority

Read the coordinating repository's instructions, then each affected target's
local instructions and canonical sources.

Identify:

- the task and repositories actually in scope
- candidate bounded contexts and their owners
- public providers, consumers, and contracts
- existing glossaries, context maps, ADRs, tests, schemas, and catalogs
- access boundaries and who may accept domain, architecture, security, or
  product decisions
- team or role ownership, cross-team decision rights, and escalation for each
  affected context and public contract

A repository is a deployment or ownership boundary, not automatically a
bounded context. Do not invent domain semantics from directory names or code
similarity.

Stop when one repository and one clear context already answer the task; use its
local harness instead of building a coordination layer.

## 2. Separate Truth from Discovery

Classify every relevant source:

1. **Canonical truth** - owned domain language, invariants, decisions, and
   public contracts.
2. **Executable evidence** - schemas, compatibility tests, builds, and runtime
   checks.
3. **Projection** - a copied or generated view tied to a source revision.
4. **Retrieval index** - searchable code, graph, embeddings, or catalog
   metadata that can be rebuilt.

Generated graphs and search results help discovery. They never become domain
authority merely because agents can query them.

## 3. Establish the Minimum Layers

Reuse existing owners. Add only missing layers:

- one cross-repository `CONTEXT-MAP.md` in a coordinating repository
- one canonical glossary or `CONTEXT.md` per bounded context
- executable public contracts at context boundaries
- thin target-local agent instructions that route to local truth
- revisioned projections only where a consumer cannot read the source directly
- deterministic drift or compatibility checks for copied contracts and
  projections

Use [REFERENCE.md](./REFERENCE.md) for ownership, starter shapes, and the
scaling decision matrix.

Keep domain modeling evolutionary:

```text
shared language and behavior hypothesis
-> concrete example or experiment
-> thin implementation and executable boundary
-> production or user feedback
-> refine language, invariants, contracts, and context relationships
```

Do not freeze a comprehensive domain model before implementation. When evidence
changes meaning, update the owned language, examples, contracts, and code in the
same loop.

If domain language is unresolved and the upstream Skill is installed, use
[mattpocock/skills `domain-modeling`](https://github.com/mattpocock/skills/tree/main/skills/engineering/domain-modeling)
with the domain owners. Do not outsource semantic authority to the Skill or
copy its implementation into this repository.

## 4. Prove the Boundary

Choose one representative cross-repository change and verify that an agent can:

1. find the owning context and repository
2. distinguish canonical facts from derived views
3. locate provider, consumer, owner, and public contract
4. make the narrow local change under target instructions
5. run local Fast Checks and cross-boundary compatibility checks
6. report uncertainty without promoting an inference to shared truth

Use an installed upstream `tdd` Skill for behavior changes when it fits the
target's test strategy.

## 5. Add Retrieval Only on Evidence

Start with Git, Markdown, native repository search, and executable contracts.
Add a retrieval layer only after representative tasks show repeated discovery
failure or unacceptable latency.

Evaluate candidates by utility, access model, freshness, reproducibility,
verification, operating cost, cognitive load, and removal cost.

Use Graphify only when local graph traversal or multi-hop impact discovery is
the demonstrated gap. Treat its output as derived and replaceable:

- follow current upstream installation and operating instructions
- define stable repository and context aliases
- make graph generation reproducible
- validate a small query set against known relationships
- separate access zones
- keep canonical facts and enforcement outside the graph

Read the source registry in [REFERENCE.md](./REFERENCE.md) and
`../scaffold-harness/CURRENTNESS.md` before choosing a volatile tool or feature.

## 6. Govern Expansion

Keep a human in the loop for unresolved domain semantics, ownership, access,
security, consequential architecture, or product decisions. Present options
with evidence, trade-offs, reversibility, and a recommendation before changing
the dependent branch.

Automate deterministic checks only after the invariant and owner are explicit.
Add catalog or policy platforms only when the scale and enforcement need
justify their operation.

## Completion

Complete when:

- each shared fact has one canonical owner
- repository and bounded-context boundaries are explicit
- public contracts and compatibility checks cover the exercised seam
- projections name source and revision
- retrieval layers are derived, reproducible, access-scoped, and removable
- local instructions still outrank coordinating guidance
- unresolved authority and next evidence triggers are visible
