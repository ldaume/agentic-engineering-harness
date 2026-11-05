# Research Refresh

The knowledge base is part of the product. A rule whose source changed, moved,
or was superseded keeps steering agents until someone re-checks it.

## When to refresh

- A source's `revisit` trigger fires (a WCAG 3 Candidate Recommendation, a
  new DTCG or Style Dictionary major, a design system's breaking release).
- A tool in the registry ships a major version.
- A rule produced a wrong result in review or testing.
- Twelve months have passed since a source's `accessed` date.

## Procedure

1. List stale entries: `accessed` older than twelve months, or a fired
   `revisit` trigger.
2. Open each source again. Never update an entry from memory; if it cannot be
   opened, record that in `limits` and lower the evidence level.
3. Update `findings`, `published`, `accessed`, `evidence_level`. Keep the id.
4. Find every rule that cites the id (`grep -rn SRC-XXX-NNN skills/design`)
   and re-judge it. Mark a rule that no longer holds as deprecated in place,
   with the date and the reason, before removing it in a later release.
5. Add new sources with the next free id in their domain prefix.
6. Keep contradictions visible: when two credible sources disagree, record
   both and the reason the rule chose one.
7. Run `python3 scripts/check-knowledge.py skills/design` and the skill tests.
8. Bump each changed skill's version (minor for a changed rule, patch for a
   citation fix) and note the refresh date in the release notes.

## Registry fields

`id`, `title`, `url`, `publisher`, `published` (date or `unknown`),
`accessed` (date actually opened), `type`, `domains`, `findings` (one
checkable statement each), `limits`, `evidence_level`, `revisit`.

## Research cut

Registry cut: 2026-10-21. Gaps recorded during that refresh live in each
skill's "Evidence gaps" section; start the next refresh there.
