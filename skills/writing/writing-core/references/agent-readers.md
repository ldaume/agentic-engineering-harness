# Writing for agents

AGENTS.md files, Skill descriptions, subagent briefs and prompts are a genre of
their own. The reader is a model: it reads every line literally, acts on it,
and pays for each token in cost and attention. Write for that reader; for a
Skill's own structure, frontmatter and activation tests, `write-a-skill` owns
the rules.

## Rules

1. Put the most important rules first. Accuracy falls as the number of
   instructions grows, and earlier instructions are followed more reliably
   than later ones (supported) [SRC-WRITE-063].
2. State the goal, the constraint and why. A reason lets the agent decide an
   unlisted case; Anthropic reports that motivation behind an instruction helps
   Claude deliver more targeted responses (verified) [SRC-WRITE-049].
3. Say what to do, not only what to avoid: Anthropic's guidance is to tell
   Claude what to do instead of what not to do (verified) [SRC-WRITE-049].
4. No CRITICAL or MUST shouting. Current models follow the system prompt
   closely, so emphasis written for older models now over-applies; use the
   plain "Use this tool when ..." (verified) [SRC-WRITE-049]. OpenAI reports the
   same for an emphatic "Be THOROUGH" prompt that made GPT-5 over-use tools
   (supported) [SRC-WRITE-052].
5. Remove contradictions. When two instructions contradict each other,
   Claude Code's documentation says Claude may pick one arbitrarily
   (verified) [SRC-WRITE-061], and a model spends effort reconciling them;
   removing them improved results in OpenAI's example (supported)
   [SRC-WRITE-052]. Read the file once as a ledger of rules and
   check each pair (`verification.md`).
6. Include only what the agent cannot find in the repository. The smallest set
   of high-signal tokens wins, and minimal need not mean short
   (supported) [SRC-WRITE-050]. A repository overview the agent can read from the
   tree is cost without gain.
7. A few diverse, canonical examples beat a list of edge cases (supported)
   [SRC-WRITE-050]. Pick examples that show the expected behavior from
   different sides and say what makes each canonical.
8. Keep rules and examples in sync: an example that breaks the rule above it
   teaches the example.
9. Keep a context file short: Claude Code's documentation targets under 200
   lines per CLAUDE.md, because longer files cost context and reduce
   adherence (verified) [SRC-WRITE-061]. Codex concatenates AGENTS.md files
   from the root to the working directory and stops adding them past 32 KiB
   combined (verified) [SRC-WRITE-062], so a long root file can hide the
   nested one.
10. A rule that must hold every time goes into a hook or a check, not into
    prose: instruction files are context, not enforced configuration, and a
    hook runs whatever the agent decides (verified) [SRC-WRITE-061].
11. In a brief, say when to delegate and set the scope of the work. On
    Opus 5-class models, drop blanket lines such as "verify everything at the
    end" or "use a subagent to verify": they cause over-verification. Keep
    the deterministic gates (tests, linters, named checks) (supported)
    [SRC-WRITE-049].
12. Wrap pasted or fetched text in a tagged block (`<document>`,
    `<email>`) and say it is data to work on, not instructions to follow.
13. Maintainer notes for humans go into block HTML comments in CLAUDE.md:
    Claude Code strips them before injection, so they cost no context
    (verified) [SRC-WRITE-061]. Other hosts may not strip them.

## Evidence on context files

A study of repository-level context files for coding agents (ETH Zurich,
arXiv 2602.11988 v3, revised 2026-09-29) found that they did not generally
raise task success and raised inference cost by over 20 percent on average;
LLM-generated files gave no gain, and developer-written files gained 2.4
percent, which was not significant (verified for the abstract) [SRC-WRITE-051]. Agents followed the instructions in the files, and the
authors see them as useful for non-standard practices. So write a context file
for what the agent cannot discover (a non-obvious command, a house rule, a trap),
keep it short, and test a change to it instead of assuming it helps. The study
covers coding benchmarks; it does not measure briefs or prompts for other work.

## Check

- Could the agent act on each line without asking? If not, state the goal or the
  missing fact.
- Which line would the agent find by reading the repository anyway? Cut it.
- Which two lines disagree? Fix one.
