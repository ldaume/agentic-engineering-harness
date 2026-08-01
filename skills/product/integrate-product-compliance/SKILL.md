---
name: integrate-product-compliance
description: Integrates confirmed security, trust, and compliance scope into product engineering through risk, control impact, evidence, release policy, and effectiveness review. Use when work touches ISO/IEC 27001, TISAX or VDA ISA, PCI DSS, customer security commitments, regulated or sensitive data, payment flows, compliance scope, audit evidence, control exceptions, or risk-based delivery.
---

# Integrate Product Compliance

Build compliance into the product loop without turning it into a late document
gate. Agents may trace, propose, implement, test, and collect evidence; named
humans retain interpretation, scope, risk acceptance, and assurance authority.

For ordinary security engineering without a confirmed control, contractual, or
assessment scope, use the target's security practices and relevant engineering
Skills directly.

## 1. Confirm Scope and Authority

Read the target's current ISMS or control system, policies, risk register,
Statement of Applicability or equivalent, data and system inventories,
contracts, assessment scope, prior findings, exceptions, and evidence store.

Confirm with named owners:

- applicable organization, products, locations, systems, data, suppliers, and
  contractual commitments
- exact standard, scheme, version, assessment objective, and assessment period
- control, risk, evidence, exception, release, and certification owners
- required assessor, auditor, QSA, legal, privacy, or security involvement

Do not infer applicability, certification status, TISAX objectives, PCI scope or
SAQ eligibility, control interpretation, or acceptable risk. If these are
unresolved, present options and stop the dependent branch.

Read [references/frameworks.md](./references/frameworks.md) when ISO/IEC 27001,
TISAX, or PCI DSS applies. Re-check official sources because standards,
assessment catalogs, FAQs, and effective dates change.

## 2. Classify the Product Change

Trace what changes across:

- data categories, flows, retention, residency, and deletion
- identities, roles, privileges, authentication, and administrative actions
- services, infrastructure, endpoints, payment pages, and trust boundaries
- suppliers, processors, libraries, agents, models, and external tools
- locations, teams, operating procedures, support, and incident response
- customer promises, assessment boundaries, and evidence obligations

Prefer scope reduction and simpler architecture when it preserves the intended
outcome. A compliance label is not a reason to maximize controls or artifacts.

## 3. Map Risk, Controls, and Evidence

Use the target's existing identifiers and GRC system. For each affected risk or
control record:

- requirement or obligation source and current version
- product or system behavior being protected
- implementation and control owner
- preventive, detective, and recovery mechanism
- deterministic test, policy gate, or manual review
- evidence source, provenance, retention, and access
- effectiveness signal and review trigger
- exception, expiry, compensating action, and risk owner when applicable

Do not copy copyrighted standards into the repository. Reference licensed
sources and record only the target's interpretation, implementation, and
evidence.

## 4. Integrate the Product Loop

Use **run-product-engineering** and add compliance where it changes a decision:

| State | Compliance contribution |
|---|---|
| Signal and triage | customer requirement, finding, incident, data or scope change |
| Problem and discovery | data flow, threat, control, supplier, auditability, and scope risk |
| Bet and focus | control impact, evidence cost, deadline, owner, and risk boundary |
| Build and validate | secure design, least privilege, tests, logging, configuration, and traceability |
| Release | locally defined risk class, approval, rollback, and evidence package |
| Production and outcome | control effectiveness, incidents, exceptions, customer trust, and improvement |

Use threat modeling, abuse cases, data-flow review, architecture evidence,
security testing, and assessor input only when the risk justifies them.

## 5. Generate Evidence from the System

Prefer evidence emitted by normal work:

- version control, reviews, signed or attributable changes
- CI/CD tests, policy results, provenance, and release records
- configuration, asset, access, vulnerability, and dependency state
- correlated audit events, traces, metrics, logs, and alerts
- incident, recovery, backup, restore, and continuity exercises
- supplier due diligence and contractual records
- training or manual evidence only where the control genuinely depends on it

Keep control mappings, implementation decisions, evidence references, and
review history in version control when their sensitivity and owning system
allow it. Generate audit views from those sources instead of maintaining a
second Word, wiki, or ticket narrative by hand.

Git is an evidence source, not a substitute for a required assurance format.
Use the current official TISAX/ISA, PCI ROC/AOC/SAQ, customer, assessor, or
certification-body forms when the applicable route requires them, and link or
generate them from the owned evidence where practical.

Evidence must identify scope, source, time, owner, version, and result. Protect
it according to sensitivity and retention policy. An agent may assemble an
evidence view but must not fabricate missing evidence or declare control
effectiveness from file presence.

## 6. Apply Risk-Based Release and Exceptions

Use the target's existing risk classes. If none exist, propose a minimal model
for human approval; do not silently impose a universal table.

Low-risk changes may use automated checks and ordinary review. Authentication,
authorization, sensitive data, security logging, regulated payment flows, or
assessment-scope changes usually require stronger targeted review, testing,
evidence, rollback, and explicit release authority.

Emergency response may defer nonessential ceremony to restore safety or
service. Preserve evidence, use the documented emergency authority, and
complete post-change review and remediation.

Only the named risk owner may accept an exception. Record reason, scope,
compensating controls, expiry, review trigger, and approval.

## 7. Review Effectiveness and Currentness

Feed control failures, incidents, false positives, audit findings, customer
requirements, supplier changes, standard updates, and operational evidence back
into risk, product, and harness decisions.

Agents may monitor evidence freshness, find gaps, propose remediation, prepare
reviews, and execute approved bounded changes. Humans or qualified specialists
retain:

- legal and contractual interpretation
- certification or assessment claims
- TISAX objectives and assessment scope
- PCI scoping, SAQ or ROC route, and QSA decisions
- risk acceptance and material release exceptions
- expansion from human-in-the-loop to human-on-the-loop

The integration is complete when scope and authority are explicit, affected
risks and controls map to real product behavior, evidence arises from normal
delivery, release follows the approved risk policy, effectiveness is observed,
and no agent-generated claim exceeds verified assurance.

## Related Skills

- **run-product-engineering** - operate the enclosing signal-to-outcome loop
- **product-craft** - shape trust, customer value, and viable bets
- **scaffold-harness** - assess governance and L5-L7 autonomy evidence
- **coding-discipline** and **completion-gate** - implement and verify controls
- **build-autonomous-agents** - constrain agent runtime data, tools, and effects
- **documentation-and-adrs** - record accepted consequential trade-offs
