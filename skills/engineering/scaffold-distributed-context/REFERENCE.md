# Distributed Context Reference

## Core Model

Use Domain-Driven Design terms precisely:

- **Bounded context:** a boundary within which a domain model and language are
  consistent.
- **Ubiquitous language:** shared terms used by domain experts, engineers,
  code, tests, and documentation within that context.
- **Context map:** relationships between bounded contexts, including direction,
  ownership, and integration style.
- **Contract:** an executable public boundary such as a schema, API
  specification, event definition, package interface, or compatibility test.
- **Seam:** a boundary where behavior can be exercised or replaced without
  requiring the whole system.

Repositories, teams, deployables, and bounded contexts may align, but none
implies another. Record the real relationship.

For multi-team systems, treat the context map as a federation of explicit
authority. Each context and contract names its team or role owner, provider and
consumer responsibilities, semantic and risk decision rights, compatibility
check, shared-policy version, and escalation path. A central catalog improves
discovery; it does not become domain authority.

## Ownership Layers

| Concern | Owner | Verification |
|---|---|---|
| Domain term or invariant | Canonical context owned with domain experts | Review plus examples or executable invariant |
| Context relationship | Coordinating context map | Owner confirmation and representative navigation |
| API, event, package, or UI integration boundary | Producing repository's public contract | Consumer or compatibility test |
| Local implementation and commands | Target repository | Local Fast Check and Full Gates |
| Cross-repository projection | Coordinator or consumer, with source revision | Drift check against source |
| Code or relationship index | Retrieval system | Rebuild plus validated query set |
| Mandatory organizational rule | Named policy owner | Deterministic enforcement and audit |

Do not copy a shared statement into several `AGENTS.md` files. Route each
consumer to the owner or a checked projection.

## Minimum Shapes

Use existing names when present. A small coordinating repository may need only:

```text
AGENTS.md
CONTEXT-MAP.md
LEARNINGS.md
```

Add these only when evidence requires them:

```text
contexts/
  <bounded-context>/
    CONTEXT.md
contracts/
  README.md
projections/
  README.md
evals/
  cross-repository-queries.md
```

Canonical context may live in a target repository instead of `contexts/`.
`CONTEXT-MAP.md` should link to it rather than create a second copy.

A useful context-map entry names:

- bounded context
- canonical source
- owning team or role
- repositories and deployables
- providers and consumers
- public contracts
- compatibility checks
- sensitivity or access boundary
- last verified revision or re-check trigger

## Progressive Scale

Stop at the first layer that handles representative work:

1. **Git and Markdown** - explicit owners, context map, glossary, ADRs.
2. **Executable contracts** - schemas and compatibility checks at boundaries.
3. **Checked projections** - revisioned consumer views when direct reads are
   impractical.
4. **Native or indexed code search** - faster discovery across code.
5. **Derived relationship graph** - multi-hop dependency and impact queries.
6. **Software catalog** - organization-scale ownership and component metadata.
7. **Policy engine** - deterministic enforcement of explicit organizational
   policy.

Layers complement rather than replace the sources below them.

## Retrieval and Governance Choices

| Candidate | Use when | Do not use as |
|---|---|---|
| Native Git and repository search | Scope is small and relationships are easy to verify | A substitute for missing ownership or contracts |
| Zoekt | Fast text and regular-expression search across many repositories is the demonstrated need | A semantic domain model |
| Graphify | Local-first code relationship traversal or multi-hop impact discovery repeatedly improves representative tasks | Canonical domain truth, policy enforcement, or automatic architecture authority |
| Sourcegraph | Many repositories or code hosts need centralized indexed search and cross-repository navigation | Proof of product semantics or ownership by itself |
| Backstage Software Catalog | Organization-scale component and ownership metadata needs a maintained catalog | Code-level dependency truth or an initial small-team requirement |
| Open Policy Agent | Explicit policy must be evaluated deterministically across systems or pipelines | A place to discover or negotiate policy |

Do not choose from a feature checklist. Run the smallest representative
evaluation and retain the candidate only when it changes task quality, latency,
or risk enough to justify its operation.

## Graphify Adoption Gate

Before adopting Graphify, require:

- repeated questions that need relationships beyond ordinary text or symbol
  search
- a named user and decision improved by the graph
- repository and context aliases stable enough for repeatable queries
- reproducible generation from authorized source revisions
- a small known-answer query set covering dependency and impact cases
- freshness, failure, and stale-index behavior
- access zones that prevent cross-boundary disclosure
- a removal path that leaves canonical context and checks intact

Store only configuration, evaluation cases, and operational instructions that
the target owns. Install and update Graphify from its upstream source instead
of vendoring its implementation here.

## Representative Evaluation

Use five to ten known-answer questions from real work, such as:

- Which bounded context owns this term?
- Which repositories provide and consume this contract?
- What must change when this event or package interface changes?
- Where is the shell-to-microfrontend integration seam verified?
- Which local instruction hierarchy applies to this file?
- Which result is canonical, and which is a generated projection?

For each candidate record:

- expected answer and authoritative source
- result quality and omissions
- time to useful evidence
- source revision and freshness
- false relationships or access violations
- verification and recovery path

Keep a simpler layer when it passes.

## Failure Modes

- treating one repository as one bounded context without evidence
- centralizing local facts that targets should own
- copying contracts without a source revision or drift check
- using retrieval relevance as truth confidence
- adding a graph before validating ordinary navigation and search
- encoding policy before its owner and exceptions are agreed
- giving a coordinator permission to override target-local instructions
- measuring successful indexing rather than successful engineering decisions

## Current Primary Sources

Verify volatile behavior before adoption:

- [Graphify repository](https://github.com/Graphify-Labs/graphify)
- [Graphify concepts](https://graphify.com/concepts)
- [Zoekt repository](https://github.com/sourcegraph/zoekt)
- [Sourcegraph Code Search capabilities](https://sourcegraph.com/docs/code-search/features)
- [Sourcegraph Code Navigation](https://sourcegraph.com/docs/code-navigation)
- [Backstage Software Catalog](https://backstage.io/docs/features/software-catalog/)
- [Open Policy Agent documentation](https://www.openpolicyagent.org/docs)
- [mattpocock/skills `domain-modeling`](https://github.com/mattpocock/skills/tree/main/skills/engineering/domain-modeling)
- [mattpocock/skills `tdd`](https://github.com/mattpocock/skills/tree/main/skills/engineering/tdd)

These links are discovery entrypoints, not approval. Record the checked date,
version, access model, and re-check trigger in the adopting system.
