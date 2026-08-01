---
name: frontend-craft
description: Guides frontend, UX, UI, responsive design, microcopy, accessibility, feedback states, and AI-assisted product surfaces with production-grade taste. Use when designing, building, reviewing, or polishing screens, React islands/components, Tailwind UI, mobile flows, loading/empty/error states, or user-facing copy.
---

# Frontend Craft

Use this for frontend and product-experience work across web apps, SaaS
interfaces, dashboards, marketing surfaces, and AI-assisted UI.

## Project Fit Check

Before designing or changing UI:

1. Scan the existing product surface, routes, components, tokens, styles,
   localization files, tests, and design docs.
2. Detect the framework and styling system before importing libraries or
   inventing primitives.
3. Follow local component, icon, copy, accessibility, motion, and responsive
   conventions. Improve them only when the task requires it.
4. If design-system docs are missing, infer patterns from the existing UI and
   state the inference when it affects the result.
5. If the repo has its own UX review checklist, merge it with this skill instead
   of replacing it.

## Core Stance

- Design flows before screens.
- Build the actual usable experience, not a decorative landing shell.
- Solve the happy path and the state path: loading, empty, error, success, and
  recovery.
- Use visual taste in service of clarity, trust, speed, and action.
- Mobile is not a small desktop. Touch, reach, network, battery, and distraction
  matter.
- UI copy is product behavior. Buttons, errors, empty states, and confirmations
  must help the user proceed or recover.

## Read First

1. Repo agent instructions (`AGENTS.md`, `CLAUDE.md`, etc.)
2. Domain glossary (`CONTEXT.md`) and current product/design docs
3. Existing components, tokens, message catalogs, routes, and tests
4. Package manifest before importing any dependency
5. Accessibility, i18n, and design-system conventions already present

Pair with `coding-discipline` for implementation and `completion-gate` before
claiming done.

## Experience Contract

Every flow needs:

1. Entry point
2. User intent and known context
3. Primary action
4. Immediate feedback
5. Outcome
6. Natural next step or exit

Use:

- hub-and-spoke for dashboards and detail views
- linear flow for onboarding, forms, checkout, and setup
- tabs only for 3 to 5 stable top-level areas
- progressive disclosure when complexity would otherwise overload the screen

## Visual Direction

Default SaaS/product surfaces should be calm, utilitarian, and high craft:

- crisp hierarchy
- restrained color
- semantic tokens
- strong contrast
- stable layout dimensions
- clear affordances
- no decoration without function

Avoid:

- generic centered hero sections when a real product surface is needed
- generic purple or blue gradients used only to signal "AI"
- nested cards
- three equal feature cards as the default layout
- stock-like visuals that hide the actual product
- text that describes how to use obvious UI controls

## Frontend Defaults

- Prefer existing framework patterns and primitives.
- Use server-rendered/static components by default; isolate client components or
  islands only where interactivity requires them.
- Check `package.json` before importing libraries.
- Use CSS variables or design tokens for colors, spacing, radius, and motion.
- Use icons from the installed icon system instead of emojis for UI controls.
- Use stable dimensions for buttons, toolbars, rows, grids, counters, and
  dynamic labels.
- Do not animate layout properties; use transform and opacity.
- Respect `prefers-reduced-motion`.

## State Discipline

Every async or data-dependent surface needs:

- **Loading**: skeletons that match the final layout; avoid generic full-page
  spinners.
- **Empty**: friendly observation, useful context, and a next action.
- **Error**: plain-language problem plus recovery; localize partial failures to
  the affected region.
- **Success**: lightweight confirmation; undo for reversible destructive
  actions.

Do not ship a polished happy path with broken silence everywhere else.

## Copy Rules

- Name the action: "Review changes", "Create workspace", "Retry import".
- Avoid generic labels like "Submit", "OK", and "Continue" when the action can
  be named.
- Use plain product language from the domain glossary.
- Do not expose raw internal errors, job names, provider stack traces, or agent
  jargon in user-facing copy.
- If the repo is localized, update all required locales in the established
  message system.
- Blame the system, not the user, when recovery is possible.

## Mobile Rules

- Minimum touch target: 44px.
- Primary actions should be reachable in normal thumb zones.
- No hover-only affordances for critical actions.
- Avoid horizontal overflow at 320-375px.
- Reserve space for async content to prevent layout jumps.
- Keep forms short; use progressive disclosure for advanced inputs.
- Safe areas matter for sticky bottom actions.

## AI Interface Rules

- Make uncertainty visible.
- Keep provenance, review, undo, or restore available for AI-generated changes
  that affect user trust.
- Do not fake AI results, citations, progress, or confidence.
- Prefer concrete progress labels over generic spinners.
- Do not let AI chrome compete with the user's primary object of work.
- Preserve user agency: suggestions should be easy to accept, reject, edit, or
  ignore.

## Review Checklist

- Does the screen answer one primary question?
- Is the primary action obvious, reachable, and accurately labeled?
- Does the flow have an exit and a recovery path?
- Are loading, empty, error, and success states present?
- Does mobile collapse cleanly without hidden actions or horizontal scroll?
- Are focus, labels, roles, contrast, keyboard access, and reduced motion
  handled?
- Does the implementation follow existing tokens and component patterns?
- Is every new dependency justified?

## Red Flags

Stop and revise when you see:

- happy-path-only UI
- hidden or generic error handling
- hover-only mobile-critical actions
- hardcoded colors where tokens exist
- icons or emojis used inconsistently
- UI copy added outside the repo's localization system
- AI surfaces with no review, provenance, or recovery
- animation that delays the user's work
