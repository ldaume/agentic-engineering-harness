# Security Vocabulary

The terms application security engineers use to judge a change, so a review
names the weakness the way the field does and points at something a reader can
see in the diff, the config, or the PR. Load before judging or reviewing a
change that crosses a trust boundary. A term is admitted only with a registered
source and an observable marker. Check: `exact` (a pattern in code or config a
scanner or script can match; none ships here yet, so no rule ids), `jev` (a
typed question), `judge` (a person or model decides).

| Term | Definition | Source | Marker | Check |
|---|---|---|---|---|
| Trust boundary | A point where data or control passes between parties that trust each other differently. | [SRC-SEC-002] [SRC-SEC-038] | A diff that adds an endpoint, webhook, upload, tool, or service with no boundary named in the PR. | judge |
| Threat note | The four threat modeling questions answered for this change, with a named attacker and asset. | [SRC-SEC-002] | A boundary-crossing PR with no threat, or one that only names a category ("IDOR risk"). | judge |
| Abuse-case test | A test that plays the attacker's request and asserts it is refused, written before the control. | [SRC-SEC-002] [SRC-SEC-037] | A new control with no test that sends the hostile request; no recorded red run in the PR. | judge |
| Insecure design | A missing or wrong control that no amount of correct code fixes later. | [SRC-SEC-001] | A flow with no step where the needed check could sit (for example no owner on the record). | judge |
| Broken object level authorization | Acting on an object named by a client-supplied id without checking the caller may act on that object (IDOR). | [SRC-SEC-041] [SRC-SEC-038] | A handler loads or changes a record by a request id with no owner, tenant, or policy check in the query or before it. | judge |
| Function level authorization | Each operation checks the caller's role or permission, not only that they are logged in. | [SRC-SEC-041] [SRC-SEC-001] | An admin or mutating route reachable with any authenticated session. | judge |
| Deny by default | When no rule grants access, the answer is no. | [SRC-SEC-038] | A permission check whose fallthrough or error branch returns allow. | judge |
| Least privilege | Each user, token, and workload holds only what its task needs. | [SRC-SEC-038] [SRC-SEC-011] | A workflow without an explicit `permissions:` block; a service role or token with wildcard scope. | exact |
| Fail closed | An error in a security check denies the action and reveals nothing useful. | [SRC-SEC-001] [SRC-SEC-027] | A `catch` that continues the guarded action; a stack trace or query in a response body. | judge |
| Allowlist validation | Input is parsed at the server into a typed value with allowed shape, type, length, and range. | [SRC-SEC-003] | A denylist of bad characters; a request field used without a schema or type parse. | judge |
| Parameterized query | Query structure fixed in code, values bound by the driver. | [SRC-SEC-039] [SRC-SEC-003] | Query text built by concatenation or interpolation with a request value. | exact |
| Contextual output encoding | Untrusted data encoded for the exact context it is written into, through a safe sink. | [SRC-SEC-040] | `innerHTML`, `dangerouslySetInnerHTML`, `v-html`, a template `safe` filter, or `eval` fed with request data. | exact |
| Mass assignment | Binding a whole request body onto a model, so a client can set fields it should not. | [SRC-SEC-035] | A request body passed unfiltered to an ORM create or update call. | exact |
| Server-side request forgery | The server fetches a URL an attacker chose, reaching internal hosts or metadata. | [SRC-SEC-004] | An outbound request whose host comes from input with no target allowlist or address check. | judge |
| Resource consumption limit | A rate limit, size or page cap, timeout, and for model calls a token budget. | [SRC-SEC-036] | A new endpoint or tool call with no rate limit, unbounded page size, or no timeout. | judge |
| Security event logging | Failed logins, denials, and rejected input are logged; secrets never are. | [SRC-SEC-005] | A token, session id, password, or key in a log statement; a denial path with no log. | exact |
| Hardcoded secret | A credential committed to code, config, a fixture, or a prompt. | [SRC-SEC-006] | A secret scanner finding on the diff. | exact |
| Workload identity federation | CI or a service gets short-lived credentials from its identity (OIDC) instead of a stored key. | [SRC-SEC-007] [SRC-SEC-008] | A workflow that reads a long-lived cloud or registry key from secrets. | exact |
| Action pinning | A CI action referenced by lockfile or full commit SHA, so its code cannot change under you. | [SRC-SEC-011] | A `uses:` reference that is a tag or branch, not a 40-character SHA. | exact |
| Script injection | An untrusted event field expanded inline into a shell step. | [SRC-SEC-011] | `${{ github.event.* }}` or a head ref inside `run:` instead of an `env:` variable. | exact |
| Pwn request | A privileged trigger that checks out or runs pull request code with secrets. | [SRC-SEC-011] | `pull_request_target` with a checkout of the PR head ref. | exact |
| Dependency cooldown | A new release waits a set time before adoption, with an exception path for security fixes. | [SRC-SEC-009] [SRC-SEC-010] | An updater config with no `cooldown`, `minimumReleaseAge`, or `min-release-age`. | exact |
| Package hallucination | A dependency name a model invented, which an attacker can register (slopsquatting). | [SRC-SEC-024] [SRC-SEC-025] | A new dependency absent from the registry, or first published days ago with no usage. | exact |
| Build provenance | A signed statement of how and from what source an artifact was built. | [SRC-SEC-017] [SRC-SEC-008] | A published package or image with no provenance attestation. | exact |
| Exploitation-informed prioritization | Fix order set by KEV listing and EPSS together with severity. | [SRC-SEC-012] | A fix queue ordered by CVSS alone while a KEV-listed finding waits. | judge |
| Zero trust | Access granted per request to an authenticated identity, never for network location. | [SRC-SEC-030] [SRC-SEC-032] | A service that trusts callers by source IP, VPC, or "internal" header; plaintext service hops. | judge |
| Default-deny network policy | A namespace starts with all traffic denied and allows only named flows. | [SRC-SEC-031] | A namespace with workloads and no NetworkPolicy selecting all pods with empty ingress or egress. | exact |
| Phishing-resistant authenticator | A factor bound to the origin, such as a passkey or WebAuthn key. | [SRC-SEC-013] | MFA offered with SMS, email, or TOTP only. | judge |
| Password blocklist | New passwords checked against common and breached values instead of composition rules. | [SRC-SEC-013] | A password rule requiring symbols or digits; a maximum under 64; no breached-value check. | exact |
| Adaptive password hashing | Passwords stored with a slow, salted function: Argon2id, bcrypt, or PBKDF2. | [SRC-SEC-020] | MD5, SHA-1, or SHA-256 applied to a password, or no per-password salt. | exact |
| Session rotation | A new session id after login and every privilege change. | [SRC-SEC-033] | A login handler that keeps the pre-login session id. | judge |
| Cookie hardening | Session cookies set `Secure`, `HttpOnly`, and `SameSite`. | [SRC-SEC-033] | A session `Set-Cookie` missing one of the three attributes. | exact |
| Token validation | A JWT verified with a pinned algorithm and checked for `iss`, `aud`, and `exp`. | [SRC-SEC-034] | A decode without verify, `alg: none` accepted, or no audience check. | exact |
| Prompt injection | Instructions hidden in data a model reads, steering what it does. | [SRC-SEC-014] [SRC-SEC-025] | Fetched pages, issues, or tool output placed in a prompt next to tools that act. | judge |
| Lethal trifecta | One agent session with untrusted input, sensitive access, and an external channel. | [SRC-SEC-016] [SRC-SEC-015] | All three present with no human approval or session split. | judge |
| Excessive agency | A model given more tools, scope, or autonomy than the task needs. | [SRC-SEC-014] [SRC-SEC-023] | A tool with write or shell access where read would do; no approval on a destructive tool. | judge |
| Token passthrough | An MCP server forwarding a token it received to another API. | [SRC-SEC-029] | A server that sends the client's bearer token upstream without checking it was issued for itself. | judge |
| Shift down | The platform enforces the control so each caller does not have to remember it. | [SRC-SEC-021] [SRC-SEC-019] | A hand-written escape, auth check, or crypto where the framework provides one; a raw escape hatch without a stated reason. | judge |
| Vulnerability class fix | After a fix, the safe API, lint rule, or default that removes the whole class, plus a regression test. | [SRC-SEC-021] [SRC-SEC-018] | A security fix PR with no regression test and no proposal for the class. | judge |

## Not admitted

- Periodic forced password changes, composition rules, security questions and
  hints: retired by NIST SP 800-63B-4 [SRC-SEC-013]; judge length, blocklist,
  and rate limits instead.
- "Sanitize all input" as the injection fix: parameterize and encode
  [SRC-SEC-039] [SRC-SEC-040]; validation is an extra layer.
- Random or hidden ids as access control: unguessable ids do not replace the
  object-level check [SRC-SEC-038].
- A trusted internal network or DMZ: location grants nothing [SRC-SEC-030].
- CVSS score alone as fix order: weigh exploitation evidence [SRC-SEC-012].
- A command allowlist as the agent sandbox: argument injection escapes it
  [SRC-SEC-028].
- Abuse cases as user-story templates: OWASP archived its Abuse Case Cheat
  Sheet as rarely used; the abuse-case test above is the executable form.
