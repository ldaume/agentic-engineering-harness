# Writing for agents

AGENTS.md files, Skill descriptions, subagent briefs and prompts are a genre of
their own. The reader is a model: it reads every line literally, acts on it,
and pays for each token in cost and attention. Write for that reader; for a
Skill's own structure, frontmatter and activation tests, `write-a-skill` owns
the rules.

## Rules

1. State the goal, the constraint and why. A reason lets the agent decide an
   unlisted case; Anthropic reports that motivation behind an instruction helps
   Claude deliver more targeted responses (verified) [SRC-WRITE-049].
2. Say what to do, not only what to avoid: Anthropic's guidance is to tell
   Claude what to do instead of what not to do (verified) [SRC-WRITE-049].
3. No CRITICAL or MUST shouting. Current models follow the system prompt
   closely, so emphasis written for older models now over-applies; use the
   plain "Use this tool when ..." (verified) [SRC-WRITE-049]. OpenAI reports the
   same for an emphatic "Be THOROUGH" prompt that made GPT-5 over-use tools
   (supported) [SRC-WRITE-052].
4. Remove contradictions. A model spends effort reconciling two rules that
   cannot both hold, and removing them improved results in OpenAI's example
   (supported) [SRC-WRITE-052]. Read the file once as a ledger of rules and
   check each pair (`verification.md`).
5. Include only what the agent cannot find in the repository. The smallest set
   of high-signal tokens wins, and minimal need not mean short
   (supported) [SRC-WRITE-050]. A repository overview the agent can read from the
   tree is cost without gain.
6. One canonical example beats a list of edge cases (supported)
   [SRC-WRITE-050]. Pick the example that shows the expected behavior and say
   what makes it canonical.
7. Keep rules and examples in sync: an example that breaks the rule above it
   teaches the example.

## Evidence on context files

A study of repository-level context files for coding agents found that they did
not generally raise task success and raised inference cost by over 20 percent on
average, for LLM-generated and developer-committed files alike (verified for the
abstract) [SRC-WRITE-051]. Agents followed the instructions in the files, and the
authors see them as useful for non-standard practices. So write a context file
for what the agent cannot discover (a non-obvious command, a house rule, a trap),
keep it short, and test a change to it instead of assuming it helps. The study
covers coding benchmarks; it does not measure briefs or prompts for other work.

## Check

- Could the agent act on each line without asking? If not, state the goal or the
  missing fact.
- Which line would the agent find by reading the repository anyway? Cut it.
- Which two lines disagree? Fix one.
