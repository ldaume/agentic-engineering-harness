---
name: ansible-automation
description: Designs, reviews, and troubleshoots Ansible inventories, playbooks, roles, variables, vault usage, idempotency, and server automation. Use when managing infrastructure with Ansible, writing playbooks, organizing roles, handling SSH inventories, templating configs, or making repeatable operations safe.
---

# Ansible Automation

Use this for repeatable server and infrastructure operations with Ansible.

## Project Fit Check

Before changing automation:

1. Read inventories, group vars, host vars, roles, collections, vault policy,
   runbooks, and CI jobs.
2. Identify target hosts, privilege escalation model, SSH user, environment, and
   whether changes are safe to run repeatedly.
3. Preserve existing variable naming, role layout, and collection versions.
4. Do not run against production without confirmation of inventory and limit.
5. Treat secrets as vault or external secret-manager material, never plain vars.

## Playbook Rules

- Make tasks idempotent; repeated runs should converge without surprise.
- Use handlers for service reloads/restarts.
- Prefer modules over shell commands.
- If shell is necessary, add `creates`, `removes`, `changed_when`, or
  `failed_when`.
- Keep templates minimal and render from explicit vars.
- Use tags for operational subsets only when they remain safe alone.

## Inventory Rules

- Keep environments explicit: staging, production, homelab, or similar.
- Use group vars for shared policy and host vars for true host differences.
- Avoid embedding secrets or personal paths in inventory.
- Document required external vars and vault files.

## Verification

```bash
ansible-playbook --syntax-check playbook.yml
ansible-playbook --check --diff playbook.yml
ansible-playbook --limit <safe-target> playbook.yml
```

Use check mode cautiously; not every module predicts changes perfectly.

## Red Flags

- raw shell task where a module exists
- production inventory selected by default
- secret in plaintext YAML
- restart on every run
- unbounded `hosts: all` for risky changes
- task depends on local machine state without documenting it
