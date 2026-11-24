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

## Page type

Route each page to one of four types before drafting, and keep one type per
page: a tutorial (learning by doing, guided), a how-to guide (a competent
reader's goal), reference (accurate, neutral facts that mirror the thing
described), or explanation (why, context). Blurring the types is a common
source of weak documentation; link to the other type instead of mixing it in
(Diataxis, opened 2026-11-24; `SRC-WRITE-046`).

## Architecture

Purpose, prerequisites, concept or model, procedure, verification, failure
and recovery, related decisions.

## ADR prose

Follow the MADR 4 sections (MADR 4.0.0, 2024-09-17): title (problem and
solution in a short phrase), context and problem statement, decision drivers
(optional), considered options, decision outcome with consequences and
confirmation (both optional), pros and cons of the options (optional), more
information (optional) (`SRC-WRITE-047`). This reference covers the prose
only; whether a change needs an ADR and what the decision is belong to
`documentation-and-adrs`.

## Docs that AI reads

Agents and search retrieve fragments, not whole pages. So each section stands
alone: name the subject in its first sentence, and write no "as above" or "the
previous step". A reference page carries no narrative; put the story in an
explanation page (Diataxis) [SRC-WRITE-046]. Do not mandate an `llms.txt`
file: a log study of 137,210 domains found that 97 percent of such files got no
requests in May 2026 (supported) [SRC-WRITE-059], and Google's John Mueller said
no AI system uses the file (supported, second-hand) [SRC-WRITE-060].

## Anti-patterns

- Narrating history before the current truth.
- "Simply", "just", "obviously": they hide steps and blame the reader.
- Undefined acronyms and internal nicknames.
- Claims of performance or safety without a measurement or reference.
