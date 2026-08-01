---
name: secure-linux-web-hosting
description: Guides secure setup and review of Linux web servers for self-hosted apps, static sites, reverse proxies, SSH, firewalls, TLS, backups, updates, logs, and basic hardening. Use when provisioning a VPS, hardening a server, configuring Nginx/Caddy/Traefik, deploying web apps, or reviewing self-hosting security.
---

# Secure Linux Web Hosting

Use this for pragmatic server hardening and web hosting operations.

## Project Fit Check

Before changing a server:

1. Identify provider, OS, access path, services, firewall, reverse proxy,
   backup policy, and deployment process.
2. Read existing runbooks, compose files, systemd units, proxy configs, and DNS
   records.
3. Confirm whether the server is production, staging, or experimental.
4. Prefer reversible changes and snapshot/backup before risky operations.
5. Do not lock down SSH or firewall rules until a second access path is known.

## Baseline

- Key-based SSH; disable password login when operationally safe.
- Dedicated deploy/user accounts; avoid routine root login.
- Firewall allows only required ports.
- Automatic security updates or a documented patch cadence.
- TLS via the chosen proxy or certificate automation.
- Backups for stateful data, tested restore path, and retention policy.
- Logs available for auth, proxy, app, and system failures.

## Reverse Proxy Rules

- Keep hostnames, upstreams, TLS, redirects, and security headers explicit.
- Do not expose admin dashboards publicly without auth and rate limiting.
- Set request/body limits according to app needs.
- Preserve WebSocket/SSE headers for realtime apps.
- Document whether the proxy terminates TLS or forwards to another layer.

## Deployment Rules

- Keep secrets outside git and out of shell history.
- Use systemd, Docker Compose, or orchestrator units consistently.
- Prefer health checks and rollback notes for app deployments.
- Monitor disk, memory, certificates, and failed services.

## Red Flags

- public SSH password login
- firewall disabled because "the app works"
- untested backups
- admin UI exposed on the public internet
- wildcard proxy routes with no auth boundary
- manual server changes that bypass the documented deployment path
