# Reader Test Prompt

Give a fresh agent only this prompt, filled in. Add no data, context, or hints.

```text
You are <reader, for example: a manager at the client who joins the meeting
and has not followed the project>. Below is the text you will be shown. You
know nothing else. Do not guess at missing facts; say what you cannot tell.

<rendered text, exactly as the reader sees it>

1. For each number: say in one sentence what it means, and what it does NOT
   mean.
2. Answer these questions from the text alone: <the misreadings you expect,
   for example "Does this mean fewer requests reach a person?", "Are the 26
   part of the 85 or additional?">. If the text does not decide it, say so.
3. Restate the hypothesis and the next steps in your own words.
4. List every word, sentence, or relation between numbers that was unclear,
   or that you had to guess at.
```

Read the answers against the source: a number restated wrongly blocks; an
unclear item is fixed or consciously kept.
