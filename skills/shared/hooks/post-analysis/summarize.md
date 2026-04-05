---
hook: post-analysis
name: summarize
order: 1
enabled: true
type: markdown
---

## Purpose
Generate a concise executive summary after the full analysis.

## Instructions for the LLM
When executing this hook, you MUST:

1. Read the complete decision brief
2. Produce a 3-5 sentence executive summary covering:
   - The decision and verdict
   - Key tradeoffs
   - Top risks
3. Append the summary after the validation report

## Summary Format
**Decision:** [one sentence]
**Tradeoffs:** [one sentence]
**Top Risk:** [one sentence]
**Confidence:** [High/Medium/Low]
