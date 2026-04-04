# Synthesis Engine

Resolves conflicts between lens positions and produces the final aligned decision brief.

## Input

- Original problem/plan
- All lens positions (from individual lens reviews)
- Conflict detection summary (from `engines/collision.md`)

## Happy Path: No Conflicts

If the collision engine reports UNANIMOUS (no conflicts detected):
- Proceed directly to Output Assembly with the original plan unchanged
- Set CONFLICTS RESOLVED: 0 of 0
- Set Confidence Level: High

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
2. If both positions are defensible and gap > 2x → split the difference with milestones

### Type 5 (Fundamental) → Escalate to User

1. Present both positions clearly with reasoning
2. Show tradeoffs and consequences of each choice
3. Ask user to decide
4. Record user's decision in the brief
5. If user doesn't decide → mark as UNRESOLVED (CRITICAL)

## Output Assembly

After resolving all conflicts, assemble the final brief:

### Section 4: Final Alignment After Resolution

```
ALIGNED PLAN
============
Original plan: [title]
Review date: [date]
Branch: [branch, if applicable — optional]

VERDICT ALIGNMENT (after resolution):
  <Lens1>: [GO / MODIFY / BLOCK]
  <Lens2>: [GO / MODIFY / BLOCK]
  <Lens3>: [GO / MODIFY / BLOCK]

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

RISK REGISTER
==============
[List risks with source, severity, likelihood, mitigation]
```

### Section 5: Final Summary Dashboard

Assemble the completion summary table following the template in `prompts/output-template.md`. Fill all 6 fields:

1. **FINAL DECISION** — Clear, actionable recommendation with reasoning
2. **KEY TRADEOFFS** — Explicit tradeoffs with dimension scores
3. **RISKS ACCEPTED** — Risks with their mitigation plans
4. **MITIGATION PLAN** — Concrete steps to reduce accepted risks
5. **DISSENTING OPINIONS** — Which lenses disagreed and why
6. **CONFIDENCE LEVEL** — High / Medium / Low (see Confidence Level Assignment below)

## Confidence Level Assignment

- **High:** All lenses agree (UNANIMOUS) or all conflicts are auto-resolved
- **Medium:** Some disagreement but synthesis found acceptable compromise; no unresolved Type 5 conflicts
- **Low:** Strong disagreement, unresolved Type 5 conflicts, or high-risk tradeoffs accepted
