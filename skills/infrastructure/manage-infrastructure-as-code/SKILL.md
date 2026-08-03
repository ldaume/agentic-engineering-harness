---
name: manage-infrastructure-as-code
description: Manages infrastructure through reviewable desired state, GitOps or GitOps-near reconciliation, plans, protected state, policy checks, controlled apply, drift detection, and recovery. Use for infrastructure as code, IaC, Terraform, OpenTofu, Pulumi, CloudFormation, Bicep, declarative infrastructure, GitOps, GitOps-near workflows, plan/apply, state backends, existing-resource imports, infrastructure drift, or infrastructure policy gates.
---

# Manage Infrastructure as Code

Make infrastructure changes through the target's owned desired state and
checks. Use the repository's existing tool and stack profile for syntax; this
Skill owns the lifecycle around those tools.

Do not activate only because a repository has CI, a Dockerfile, or a deploy
script. Use it when infrastructure desired state, provisioning, configuration,
or reconciliation is part of the change.

## 1. Establish Authority and Boundaries

Read the target's instructions, architecture, inventory, infrastructure source,
state configuration, runbooks, checks, deployment controls, and recent change
history. Identify:

- desired-state, infrastructure, service, state, security, and release owners
- affected accounts, environments, regions, hosts, networks, services, data,
  and trust boundaries
- who may plan, approve, apply, import, unlock, destroy, or accept drift
- provider and module versions, state backend, locking, encryption, backup,
  and recovery path
- credentials, runner identity, network reachability, maintenance window,
  observability, and rollback or forward-recovery limits

Keep production and destructive work human-in-the-loop unless the target has a
narrower evidence-backed policy. Stop on unresolved ownership, missing state,
unknown existing resources, unavailable recovery, secret exposure, or a plan
outside the declared boundary.

## 2. Choose the Reconciliation Model

Name the actual operating model instead of treating every Git-backed deploy as
GitOps:

- **GitOps** - desired state is declarative, versioned, immutable, and retains
  complete history; an agent pulls it and continuously reconciles the runtime
- **GitOps-near** - Git owns desired state and checks, while CI or an operator
  triggers controlled apply and drift reconciliation is scheduled or explicit
- **IaC plan/apply** - declarations and plans are reviewable, but reconciliation
  remains a bounded change workflow

Use the smallest model that gives the target reliable review, recovery, and
feedback. Do not add a controller only to earn the GitOps label. For a
GitOps-near system, make the missing pull or continuous-reconciliation property,
the compensating drift check, and the trigger for revisiting the model explicit.

## 3. Reconcile Actual and Desired State

Trace the complete path from source declarations through plan, policy checks,
apply, runtime state, and observed outcome. Inventory resources already present
before creating replacements.

Choose one explicit treatment for every existing resource in scope:

- already managed - preserve its address and lifecycle
- adopt - import it using a reviewed, repeatable procedure
- replace - show downtime, data, dependency, and recovery impact
- external - document the owner and exclude it from this state boundary
- remove - require explicit destructive authority and retained recovery evidence

Do not hide placement or resource creation in workflow shell when the owned
declarative model can express it. Keep unavoidable bootstrap steps small,
idempotent, and linked to the declaration they enable.

## 4. Encode the Desired State

- Keep non-secret desired state, dependency constraints, and policy tests in
  version control.
- Use secret references or runtime injection; treat plans and state as
  sensitive even when values are marked sensitive.
- Pin providers, modules, images, and actions to the level required by the
  target's reproducibility and supply-chain policy.
- Split state or modules only at real ownership, lifecycle, trust, or blast-
  radius boundaries.
- Prefer idempotent declarations and native lifecycle controls over custom
  orchestration.
- Keep state remote when collaboration or sensitivity requires it. Use a
  backend with access control, encryption, locking where supported, audit
  evidence, tested backup, and a documented recovery path.

Do not commit state, plan files, credentials, generated private keys, or other
sensitive runtime artifacts.

## 5. Validate and Plan

Run the smallest tool-native checks that can reject a bad change before it has
credentials to mutate infrastructure:

1. format and parse the changed declarations
2. validate configuration, dependency constraints, and references
3. run focused module or component tests when the tool supports them
4. evaluate the target's security, cost, reliability, and compliance policy
   checks against source and plan data
5. produce a plan for the exact revision, variables, workspace, backend, and
   target environment that would be applied
6. classify create, update, replace, destroy, data migration, privilege,
   exposure, and unknown-value effects

Fail closed when a required policy input or check is unavailable. Keep plan
output and logs within the target's evidence and sensitivity policy.

The reviewer must be able to connect every material plan effect to the intended
change. A syntactically valid plan is not approval.

## 6. Apply Through the Controlled Path

Apply the reviewed revision or saved plan through the target's normal runner,
identity, locking, approval, timeout, and cancellation controls. Use least
privilege and prevent concurrent writers to the same state or target.

Verify preconditions immediately before apply. Stop if the source, variables,
state lineage, plan, policy result, approval, or actual environment changed.

After failure or cancellation, preserve recovery state, inspect both recorded
state and actual resources, and produce a fresh reviewed plan before retrying.
Never reuse a stale plan blindly. If a backend write fails and the tool emits
local recovery state, protect and reconcile that artifact through the backend's
documented recovery path before another writer proceeds.

Do not describe `git revert` as sufficient rollback when an apply moved or
destroyed runtime state. Name the actual recovery: forward reconciliation,
resource restore, data restore, failover, import, or a tested reverse change.

Emergency or diagnostic console changes may restore safety under the target's
incident authority. Capture what changed and reconcile it into desired state or
explicitly reverse it before the incident closes.

## 7. Detect and Resolve Drift

Use a scheduled or event-triggered read-only plan, refresh, or platform check
when the value and cost justify it. Route drift to a named owner with the
source revision, target, time, plan summary, and evidence location.

Classify drift before acting:

- legitimate emergency or external-owner change - adopt it explicitly or
  restore the declared state after owner review
- unauthorized or unsafe change - contain, investigate, and reconcile through
  the incident path
- provider normalization or volatile field - model or ignore only the exact
  non-semantic difference
- stale declaration - update the source and pass the normal gates

Never auto-apply unknown drift merely to make the check green.

## 8. Verify Outcome and Retain Evidence

Verify the real system, not only the apply exit code: health, reachability,
security boundaries, data durability, observability, cost guardrails, and the
behavior the infrastructure exists to support. Exercise the smallest credible
recovery check when the change alters state, backup, or rollback assumptions.

Retain the source revision, reviewed plan summary, policy results, approval,
apply identity and result, runtime verification, and exception or recovery
evidence in the target's existing systems.

Complete only when desired and actual state agree within declared tolerances,
material effects were reviewed, state and secrets stayed protected, runtime
verification passed, drift has an owner, and recovery is credible.

## Related Skills and Sources

- **integrate-product-compliance** - map confirmed control scope to executable
  policy, evidence, release, and human assurance authority
- **ansible-automation** - implement Ansible-specific configuration convergence
- **gitea-actions** - implement Gitea CI and controlled apply workflows
- **secure-linux-web-hosting** - handle host exposure and security boundaries
- [OpenGitOps principles](https://opengitops.dev/)
- [OpenTofu state storage and locking](https://opentofu.org/docs/language/state/backends/)
- [OpenTofu state and plan encryption](https://opentofu.org/docs/language/state/encryption/)
- [OPA in CI/CD](https://www.openpolicyagent.org/docs/cicd)
