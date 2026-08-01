---
name: meilisearch
description: Designs, configures, and debugs Meilisearch indexing, search settings, filters, ranking rules, synonyms, typo tolerance, multi-tenant indexes, and reindex/backfill flows. Use when adding Meilisearch, changing search relevance, debugging missing results, tuning facets, or operating search indexes.
---

# Meilisearch

Use this for search-backed product features and operational search workflows.

## Project Fit Check

Before changing search:

1. Read existing index definitions, sync/backfill jobs, search clients, auth
   rules, settings, and tests.
2. Identify whether indexes are global, tenant-scoped, user-scoped, or mixed.
3. Confirm which fields are searchable, filterable, sortable, displayed, and
   safe to expose.
4. Preserve existing relevance policy unless the task is to tune it.
5. Plan reindexing and rollback before changing settings or document shape.

## Index Rules

- Keep document IDs stable.
- Store only fields needed for search and display.
- Avoid indexing secrets, private prompts, tokens, or raw sensitive content.
- Make tenant/user ownership enforceable before query results reach the user.
- Treat settings changes as migrations: apply consistently and verify.

## Relevance Rules

- Tune searchable attributes before adding complex ranking hacks.
- Use filters/facets for structured constraints.
- Add synonyms only when they reflect real domain language.
- Test typo tolerance against real queries, not only ideal examples.
- Record meaningful relevance changes in docs or changelog.

## Sync And Backfill

- Prefer idempotent indexing jobs.
- Track source record id, index name, version, and last indexed timestamp when
  operations need observability.
- Handle deletes and permission changes, not only creates/updates.
- Batch conservatively and retry safely.

## Verification

- fixture search tests for relevance-critical queries
- permission tests for tenant/user boundaries
- backfill smoke test on a small sample
- manual query check for changed facets or ranking rules

## Red Flags

- search results bypass authorization
- private fields indexed for convenience
- settings changed without reindex plan
- relevance tuned from one anecdotal query
- delete path missing from sync
