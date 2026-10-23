---
{
  "mode": "sequential",
  "instances": []
}
---

## Orchestration Plan

Empty instances means a single normal review, not two example reviews. Harness is opt-in.
Configuration uses JSON between the `---` delimiters; nested YAML is rejected, not flattened.
The Python CLI generates a plan. The host agent executes it within existing tool permissions.

Modes: `sequential` (listed order), `parallel` (ready independent instances),
`conditional` (host evaluates conditions before each dependent instance).
Names must be unique; dependencies must exist and form an acyclic graph.
Conditions are plain-language instructions, never Python or shell expressions to evaluate.
If a condition is unknown, report it and do not execute that instance without clarification.

### Example: Technical → Business Review

Replace the frontmatter object with:

```json
{
  "mode": "sequential",
  "instances": [
    {"name": "technical-review", "lenses": ["CTO", "CISO"], "reasoning": {"depth": "deep"}},
    {"name": "business-impact", "depends_on": "technical-review", "lenses": ["CEO", "CFO", "CRO"]}
  ]
}
```

Each instance can additionally specify `condition`, `hooks` (stage → list of hook names),
and `reasoning` with the same fields as the shared reasoning configuration.
