# Agent Engineering Vocabulary

The terms agent builders use to judge a design, so a review names the gap the
way the field does and points at something visible in the plan, config, tool
definitions, or run traces. Authors and check scripts use it; reviews do not
load it by default. Security terms (prompt injection, lethal trifecta,
excessive agency, token passthrough, resource consumption limit) live in
`shift-left-security`; this file adds the design, context, evaluation, and MCP
terms. The field moves fast, so every source in `sources.json` is due for a
re-read in 2027-05. Check: `exact` (a pattern a script could match; none ships
here yet, so no rule ids) or `judge` (a person or model decides).

| Term | Definition | Source | Marker | Check |
|---|---|---|---|---|
| Workflow versus agent | In a workflow, code fixes the path of LLM calls; in an agent, the model picks its own steps and tools. | [SRC-AGENT-001] | A design doc that says "agent" for a fixed sequence, or a free loop where the steps are known. | judge |
| Augmented LLM | One model call given retrieval, tools, and memory it uses itself, the unit the patterns build on. | [SRC-AGENT-001] | A multi-step system proposed before a single augmented call was tried. | judge |
| Prompt chaining | A fixed sequence of calls, each taking the previous output, with programmatic gates between steps. | [SRC-AGENT-001] | A chain of calls with no check between steps. | judge |
| Routing | Classify the input, then send it to a specialized prompt, tool set, or model. | [SRC-AGENT-001] | One prompt full of per-category branches that a classifier step would separate. | judge |
| Parallelization | Independent calls run side by side (sectioning) or the same task repeated for a vote. | [SRC-AGENT-001] | Sequential calls on independent subtasks, or a single risky answer taken without a vote. | judge |
| Orchestrator-workers | A central model decides the subtasks at run time and delegates to workers. | [SRC-AGENT-001] | Fixed subtasks run through a dynamic orchestrator, or unpredictable ones hard-coded. | judge |
| Evaluator-optimizer | One call generates, another critiques, in a loop with clear criteria. | [SRC-AGENT-001] | A review loop with no stated criteria or no round cap. | judge |
| Stopping condition | A bound that ends the loop: a maximum iteration count or a human checkpoint. | [SRC-AGENT-001] | An agent loop in code with no iteration, time, or cost limit. | exact |
| Ground truth per step | Each step reads a real result (tool output, code run) to judge progress. | [SRC-AGENT-001] | A loop that continues from its own claims, not from observed results. | judge |
| Direct API first | Start with plain LLM API calls and add layers only after a simpler setup fails. | [SRC-AGENT-001] | A framework or agent runtime adopted before any plain-call baseline, hiding prompts. | judge |
| Agent-computer interface | The tool names, parameters, formats, and docs the agent sees, tuned as carefully as a prompt. | [SRC-AGENT-001] [SRC-AGENT-009] | Tool definitions with vague names, overlapping tools, or no usage notes or tests. | judge |
| Context rot | Recall of the context falls as it grows, so context is a finite attention budget. | [SRC-AGENT-009] | A prompt or transcript growing unbounded, or "use a longer window" as the fix. | judge |
| High-signal context | The smallest set of tokens that makes the desired behavior likely. | [SRC-AGENT-009] | A prompt with an edge-case laundry list instead of a few canonical examples. | judge |
| Just-in-time retrieval | The agent keeps light identifiers (paths, queries, links) and loads data through tools when needed. | [SRC-AGENT-009] | Whole corpora pasted into context up front that a tool call could fetch. | judge |
| Compaction | Summarize a near-full context and restart from the summary, keeping decisions and open bugs. | [SRC-AGENT-009] | A long run with no summary step, or a summary dropping open decisions. | judge |
| Tool result clearing | Drop old raw tool outputs from the history once used. | [SRC-AGENT-009] | Large tool outputs repeated in every later turn. | judge |
| Structured note-taking | The agent writes progress notes outside the window and reads them back later. | [SRC-AGENT-009] | A multi-hour task whose progress lives only in the transcript. | judge |
| Sub-agent context isolation | A subagent explores in a clean window and returns only a short distilled summary. | [SRC-AGENT-009] | A subagent that returns its full transcript to the lead. | judge |
| Tool execution error | A failed call returns readable `isError` text so the model can correct and retry. | [SRC-AGENT-005] | A tool that throws an opaque protocol error for bad input. | judge |
| Human in the loop for tools | A person can see and deny tool calls and sampling requests. | [SRC-AGENT-005] [SRC-AGENT-006] [SRC-AGENT-004] | A host that runs a write tool with no confirmation or visible indicator. | judge |
| MCP primitives | Servers offer tools (model acts), resources (data), prompts (templates); clients offer sampling, roots, elicitation. | [SRC-AGENT-004] | A server feature built as a tool that is only read-only data, or the reverse. | judge |
| Roots | The filesystem locations a client declares a server may work in. | [SRC-AGENT-007] | A filesystem server with no declared roots. | exact |
| Elicitation | A server asks the user for input; secrets go through URL mode, never a form. | [SRC-AGENT-008] | A form-mode request for a password, key, or token. | exact |
| Trace review | Read the actual traces, all of them at first, before building metrics. | [SRC-AGENT-002] [SRC-AGENT-003] | An eval suite with no notes taken from real traces. | judge |
| Error analysis | Open-code trace failures into notes, group them into a counted failure taxonomy. | [SRC-AGENT-003] | Eval cases not traceable to a counted failure category. | judge |
| Assertion eval | A fast, cheap deterministic check run on every change. | [SRC-AGENT-002] | Agent behavior checked only by hand or by a slow model judge. | judge |
| Binary pass/fail judge | A criterion judged pass or fail, not on a 1-5 scale. | [SRC-AGENT-003] | A rubric with 1-5 scores and no pass line. | judge |
| Judge alignment | An LLM judge is scored against human labels (true positive and negative rates) before use. | [SRC-AGENT-003] | A judge prompt used with no labeled sample and no agreement figure. | judge |
| Application-specific evaluator | A check built for this product's failure modes, not a generic score. | [SRC-AGENT-003] | A "helpfulness" or "hallucination" score as the only evaluation. | judge |

## Not admitted

- A bigger model or a longer prompt as the fix for an agent that lacks tools or
  context: context is a finite budget [SRC-AGENT-009] and tools are the
  interface [SRC-AGENT-001].
- Framework-first builds: frameworks hide prompts and invite complexity
  [SRC-AGENT-001].
- Generic 1-5 eval scores, and off-the-shelf metrics as the whole evaluation:
  use binary, application-specific checks [SRC-AGENT-003].
- An LLM judge trusted unvalidated: align it to human labels [SRC-AGENT-003].
- Trusting tool annotations or descriptions from an unvetted MCP server: the
  specification calls them untrusted [SRC-AGENT-004].
