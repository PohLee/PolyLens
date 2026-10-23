# Synthesis Engine

Resolves conflicts between lens positions and produces the final aligned decision brief.

## Input

- Original problem/plan
- All lens positions (from individual lens reviews)
- Conflict detection summary (from `engines/collision.md`)

Use the structured decision-framing fields as the primary synthesis input. Use reasoning paragraphs to explain tradeoffs, not to reconstruct the basic stance.

## Happy Path: No Conflicts

Only take this path when the canonical conflict count is zero, not merely when alignment is UNANIMOUS:
- Retain compatible required modifications even when every verdict is MODIFY
- A unanimous BLOCK still blocks execution; report the reasons and remediation, not permission to proceed
- Proceed to Output Assembly after recording execution blockers, required modifications, material assumptions, and pending user decisions separately
- Set CONFLICTS RESOLVED: 0 of 0
- Assign confidence using Confidence Level Assignment below; consensus is not evidence

## Resolution Strategies by Conflict Type

### Type 1 (Priority) → Time-Horizon Split

Phase the work:
1. Identify what each lens wants done first
2. Create Phase 1 (immediate) and Phase 2 (deferred)
3. Phase 1 addresses the most time-sensitive concern
4. Phase 2 addresses the other concern with a specific trigger/date for revisiting

### Type 2 (Scope) → Constraint Resolution

1. List each lens's non-negotiables
2. Find the smallest scope that includes all non-negotiables
3. Everything else becomes a deferred decision with a revisit trigger
4. If non-negotiables are mutually exclusive → escalate to user (Type 5)

### Type 3 (Risk) → Weighted Tradeoff Matrix

Score each disputed risk:
1. Impact: 1-5 (1=minor, 5=catastrophic)
2. Likelihood: 1-5 (1=rare, 5=almost certain)
3. Reversibility: reversible / irreversible
4. Cost to mitigate: low / medium / high

Decision rule:
- If irreversible AND impact >= 4 → non-negotiable, must mitigate
- If reversible AND impact * likelihood <= 6 → accept with monitoring
- Otherwise → mitigate with proportional effort

### Type 4 (Resource) → Reversible vs Irreversible Framework

1. Is the resource commitment reversible? (Can we reassign people/budget later?)
   - Yes → go with the smaller estimate, can adjust later
   - No → go with the larger estimate, under-commitment is more costly
2. If both positions are defensible and gap > 2x → escalate to user using the decision split format; this overrides the reversible/irreversible shortcut above
3. Keep it classified as Type 4, but treat the unresolved escalation exactly like any pending user decision: partial brief only, then stop

### Type 5 (Fundamental) → Escalate to User

1. Present the irreducible choice clearly with reasoning from each side
2. Show tradeoffs and consequences of each option
3. Output a partial brief with a `DECISION SPLIT (AWAITING USER INPUT)` section
4. Stop and wait for user input instead of pretending the final aligned brief is complete
5. After the user decides, resume synthesis and record that decision in the final brief
6. If the user does not decide, leave the issue as unresolved and confidence as Low

## Output Assembly

After resolving conflicts, assemble the final brief only when no user decision is pending. A Type 4 escalation also requires a partial brief and a stop.

### Section 4: Final Alignment After Resolution

```
ALIGNED PLAN
============
Original plan: [title]
Review date: [date]
Branch: [branch, if applicable — optional]
Lenses involved: [2-4 lenses]

VERDICT ALIGNMENT (after resolution):
  <Lens A>: [GO / MODIFY / BLOCK]
  <Lens B>: [GO / MODIFY / BLOCK]
  [<Lens C>: [GO / MODIFY / BLOCK]]
  [<Lens D>: [GO / MODIFY / BLOCK]]

CONFLICTS RESOLVED: [N] of [N]
  Auto-resolved: [N]
  User-decided: [N]
  Deferred: [N]
  Unresolved (CRITICAL): [N]

CHANGES TO ORIGINAL PLAN
=========================
[List each change with: what changed, driven by which lens, reason, tradeoff]

UNANIMOUS AGREEMENTS
=====================
[List elements all lenses endorse]

DEFERRED DECISIONS
===================
[List deferred decisions with revisit triggers]

ASSUMPTIONS / UNKNOWNS
======================
[List unresolved assumptions, their impact, and who owns resolution]

RISK REGISTER
==============
1. [Risk description]
  Source: [lens]
  Severity: [LOW / MEDIUM / HIGH / CRITICAL]
  Likelihood: [LOW / MEDIUM / HIGH]
  Mitigation: [plan]
```

If user input is still required for any conflict type, replace Section 4 with the `DECISION SPLIT (AWAITING USER INPUT)` format from `prompts/output-template.md`, keep Sections 1-3, and stop before producing a completed Section 5 dashboard.

### Section 5: Final Summary Dashboard

Assemble the completion summary block following the template in `prompts/output-template.md`. Use short labeled lines and bullet lists instead of box-drawing or wide tables. Fill the 6 primary dashboard fields and the supporting summary sections:

1. **FINAL DECISION** — Clear, actionable recommendation with reasoning
2. **KEY TRADEOFFS** — Explicit tradeoffs with dimension scores
3. **RISKS ACCEPTED** — Risks with their mitigation plans
4. **MITIGATION PLAN** — Concrete steps to reduce accepted risks
5. **DISSENTING OPINIONS** — Which lenses disagreed and why
6. **CONFIDENCE LEVEL** — High / Medium / Low (see Confidence Level Assignment below)

For 2-4 lenses, include one row per selected lens only.

## Confidence Level Assignment

- **High:** Execution path is clear, no execution blocker or user decision is pending, no material assumptions remain unresolved, and no accepted high-severity risk lacks mitigation
- **Medium:** Some disagreement, deferred decisions, or moderate assumptions remain, but the plan can proceed with clear owners and guardrails
- **Low:** A user decision is still pending, high-severity risk is accepted with weak mitigation, or major assumptions materially affect execution
