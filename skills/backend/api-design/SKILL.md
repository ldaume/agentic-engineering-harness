---
name: api-design
description: Designs and reviews REST, GraphQL, and internal APIs with explicit contracts, validation, errors, pagination, versioning, documentation, auth, and compatibility. Use when creating endpoints, changing API contracts, writing OpenAPI docs, reviewing GraphQL schemas, or refactoring service boundaries.
---

# API Design

Use this for API contracts that other code, users, or services depend on.

## Project Fit Check

Before changing an API:

1. Read existing routes, schemas, OpenAPI/GraphQL docs, clients, tests, and auth
   rules.
2. Identify consumers: UI, external users, workers, webhooks, integrations, or
   internal packages.
3. Preserve existing naming, error shape, pagination style, and versioning
   policy unless the task is to change them.
4. Treat compatibility as a product constraint.
5. If documentation is missing, add the smallest useful contract near the
   existing source of truth.

## Contract Rules

- Validate input at the boundary.
- Make response shape stable and documented.
- Use machine-readable error codes plus human-readable messages.
- Keep auth and ownership checks at the strongest available boundary.
- Make pagination, filtering, sorting, and limits explicit.
- Keep idempotency clear for create/update/retry paths.
- Avoid leaking provider errors or internal stack details.

## REST Rules

- Use resources and actions consistently.
- Choose status codes deliberately.
- Keep destructive operations explicit.
- Support partial failure only when the client can act on it.
- Use versioning when breaking changes cannot be coordinated.

## GraphQL Rules

- Design schema around consumer needs, not database tables.
- Keep nullability meaningful.
- Avoid resolver waterfalls; batch where needed.
- Make authorization explicit per object or field where sensitivity differs.
- Deprecate before removing fields.

## Verification

- schema/typecheck for contracts
- unit tests for validation and errors
- integration tests for auth, pagination, and persistence
- client or e2e tests for user-visible flows

## Red Flags

- silent response shape change
- unbounded list endpoint
- inconsistent error format
- auth only in the frontend
- endpoint mirrors database internals
- breaking change without migration or version plan
