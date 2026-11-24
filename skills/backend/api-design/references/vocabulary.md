# API Design Vocabulary

The terms API designers use to judge a contract, so a review names the gap the
way the field does and points at something a reader can see in the OpenAPI or
GraphQL schema, the handler, or a recorded request and response. Authors and
check scripts use it; reviews do not load it by default. A term is admitted
only with a registered source and an observable marker; evidence and access
dates are in `sources.json`. Check: `exact` (a pattern in the schema or a
response a script can match; none ships here yet, so no rule ids), `jev` (a
typed question), `judge` (a person or model decides).

| Term | Definition | Source | Marker | Check |
|---|---|---|---|---|
| API first | The contract is written and reviewed before the implementation. | [SRC-API-010] | An OpenAPI file generated after the fact, or no review by a consumer before merge. | judge |
| Resource-oriented design | Many nouns, few verbs: standard methods on resources, custom methods only when none fits. | [SRC-API-003] | Verb paths such as `/getUser` or `/doUpdateOrder` beside resources that could carry them. | exact |
| Standard methods | Get, List, Create, Update, and Delete with one consistent resource shape. | [SRC-API-003] | A resource returned in different shapes by Get, List, and Create. | judge |
| Resource name | A path of plural collection nouns and ids that identifies one resource. | [SRC-API-004] | Singular or mixed collection names, or the same collection twice in one path. | exact |
| Safe method | A method with no intended side effect on the server. | [SRC-API-002] | A GET that creates, deletes, or changes state. | judge |
| Idempotent method | Repeating the request has the same intended effect as sending it once. | [SRC-API-002] | A PUT or DELETE whose repeat creates a duplicate or fails differently. | judge |
| Request identification | An optional client-sent id that makes a create or other unsafe request safe to retry. | [SRC-API-006] [SRC-BACK-009] | A POST that charges, sends, or creates with no idempotency key or request id. | exact |
| Partial update | PATCH with an explicit field mask, so absent fields stay unchanged. | [SRC-API-005] | A PUT-only update, or PATCH that clears fields the client did not send. | judge |
| Conditional request | A write that names the version it read (ETag with If-Match) and fails when it changed. | [SRC-API-002] [SRC-API-009] | Concurrent editors on a resource with no ETag or version check on update. | exact |
| Problem details | Errors as `application/problem+json` with type, title, status, detail, and instance. | [SRC-API-001] [SRC-API-010] | Error bodies in several ad hoc shapes, or a type that is not a stable URI. | exact |
| Problem type | A stable URI naming one kind of error that clients branch on, never the message text. | [SRC-API-001] | Clients that parse `detail` or `message` text to decide what to do. | judge |
| Status code fidelity | The HTTP status says what happened: 4xx for the client's request, 5xx for the server. | [SRC-API-002] [SRC-API-010] | A 200 response whose body reports an error. | exact |
| 422 Unprocessable Content | Well-formed content the server cannot act on because of its meaning. | [SRC-API-002] | Validation failures answered with 500, or with 400 for content that parsed fine. | judge |
| Multi-status | Per-item results for a batch, answered with 207 when items differ. | [SRC-API-010] | A batch that answers 200 while some items failed. | exact |
| No stack traces | Error responses carry no implementation detail. | [SRC-API-010] | A stack trace, SQL text, or provider error in a response body. | exact |
| Cursor pagination | An opaque page token and a next token, with a bounded, documented page size. | [SRC-API-007] [SRC-API-010] | A list endpoint with no limit, or offset paging over data that changes. | exact |
| Opaque cursor | A page token clients cannot read or build. | [SRC-API-007] [SRC-API-010] | A cursor that is a raw id, timestamp, or base64 of a visible query. | judge |
| Backward compatibility | A change that keeps every existing client working. | [SRC-API-008] [SRC-API-010] | A field, value, or endpoint removed or renamed in the same major version. | exact |
| Compatible extension | Adding optional fields, values, or endpoints instead of versioning. | [SRC-API-010] | A new major version for a change an optional field would have carried. | judge |
| Tolerant reader | A client that ignores unknown fields and handles new enum values and status codes. | [SRC-API-010] | A client with strict deserialization that fails on an extra field. | exact |
| Expand and contract | Add the replacement, serve both, remove the old a release later. | [SRC-API-008] | A rename that removes the old field in the change that adds the new one. | judge |
| operationId | A unique, case-sensitive identifier for each operation in an OpenAPI document. | [SRC-API-011] | Missing or duplicate `operationId` values. | exact |
| JSON Schema 2020-12 | The schema dialect of OpenAPI 3.1; 3.0-only keywords no longer apply. | [SRC-API-011] | A 3.1 document using `nullable: true` instead of a type list with `null`. | exact |

## Not admitted

- PUT for every change: full replacement breaks clients when fields are added;
  use PATCH with a field mask [SRC-API-005].
- HTTP 200 with an error body: it hides failure from clients, caches, and
  monitoring [SRC-API-002] [SRC-API-010].
- A new version per change: prefer compatible extensions [SRC-API-010].
- Clients matching on error message text: branch on the problem type
  [SRC-API-001].
- Offset pagination as the default for growing or changing data
  [SRC-API-010].
- Retrying any failed request: only idempotent ones, or with a request id
  [SRC-API-002] [SRC-API-006].
