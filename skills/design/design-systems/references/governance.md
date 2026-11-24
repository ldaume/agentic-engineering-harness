# Governance: Versions, Deprecation, Alignment

## Versioning

- Semantic versioning per package; a per-component changelog with a date and
  a breaking flag, because consumers decide upgrades per component
  (supported) [SRC-PROD-029].
- Release candidates on a separate channel before a breaking change
  (supported) [SRC-PROD-026].

## Deprecation

1. Mark the component or token deprecated in code and docs with the date,
   the replacement, and the planned removal version.
2. Emit a build-time or lint warning where tooling allows.
3. Provide a migration note with before and after.
4. Remove only in a major release, after the stated period.

## Design-to-code alignment

- One source of truth per decision: tokens in the token repository,
  component behavior in code, rationale in the spec.
- Mapping tools such as Figma Code Connect link design components to code;
  the mapping is an artifact that needs review, and plan seat limits apply
  (context-dependent) [SRC-PROD-027].
- Visual review in each theme and density before release.

## Agents consume the system

Coding agents now build with the system, so write it to be read by one
(supported) [SRC-TOOL-009] [SRC-PROD-035]:

- Usage rules as do and don't, each with its reason and exceptions, so an
  agent can apply the rule to a case the text did not foresee. State
  observable decisions ("destructive buttons name the action"), not
  adjectives ("buttons should be clear").
- Typed props: finite values (an enum, not a free string) and defaults, so
  invalid combinations fail at compile time.
- One canonical example per variant, kept in the repository and compiled in
  CI, because agents copy examples more reliably than prose.
- Lint rules for everything a machine can check; prose guidance only for
  judgment calls. Give each rule a stable id that docs and lint share.
- Accepted decisions live in the repository next to the code (a decision
  record or the rule file), not in chat or a design file only. Changes to
  them get evidence and human review.

## Contribution

A proposal states the recurring need with at least two real uses, the spec
draft, the accessibility contract, and who maintains it. Escape hatches are
allowed and documented, because a system that forbids every exception gets
bypassed silently.

## Platform note

Teams planning Android with Material 3 Expressive check the current Compose
Material 3 release notes first; stabilization had no date in the 2026-10
refresh (hypothesis) [SRC-PROD-030].

## Evidence gaps

The agent-consumption guidance rests on one company's account [SRC-TOOL-009]
and a 2023 practitioner post [SRC-PROD-035]; no study measures agent output
quality against documentation style.

Carbon's versioning page and Polaris' deprecation timeline could not be read
in the 2026-10 refresh.
