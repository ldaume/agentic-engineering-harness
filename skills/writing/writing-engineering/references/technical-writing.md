# Technical Writing

## Rules

- Name the audience and its prerequisites at the top.
- One purpose per section; one idea per paragraph; the key point first.
- Active voice with a clear actor: "The worker retries the job" beats "The job
  is retried".
- Specific verbs: "returns", "rejects", "writes", not "handles", "manages".
- Consistent terminology: one term per concept for the whole document; define
  it on first use.
- Second person and imperative in procedures: "Run ...", "Check that ...".
- Numbered steps only when order matters; each step one action plus its
  observable result.
- Every procedure ends with verification ("You should see ...") and a
  failure or recovery path.
- Code, commands, paths, and identifiers in code formatting; copy-pasteable.
- Descriptive link text and descriptive headings.
- State versions and dates for anything that changes.

## Architecture

Purpose, prerequisites, concept or model, procedure, verification, failure
and recovery, related decisions.

## Anti-patterns

- Narrating history before the current truth.
- "Simply", "just", "obviously": they hide steps and blame the reader.
- Undefined acronyms and internal nicknames.
- Claims of performance or safety without a measurement or reference.
