# Output Templates

All PolyLens reviews produce structured output following these templates.

## Presentation Rules

- Prefer plain markdown headings, bold labels, and short bullet lists.
- Do not use ASCII box borders for the final brief.
- Prefer stacked comparison blocks over wide markdown tables so output stays readable in chat, terminals, and narrow editor panes.

### Compact Example

```markdown
VERDICT ALIGNMENT
=================
Alignment: SPLIT
CTO: MODIFY
CPO: GO
CEO: MODIFY

CONFLICT MAP
============
- Scope:
  - CTO: Narrow to API and schema changes first
  - CPO: Include the full onboarding flow now
  - CEO: Ship the smallest differentiated wedge
- Timeline:
  - CTO: Phase rollout over 2 releases
  - CPO: Validate with a pilot this sprint
  - CEO: Launch as soon as the core story is credible

EXECUTIVE ALIGNMENT REVIEW - COMPLETION SUMMARY
===============================================
Plan: Guided onboarding revamp
Review type: enhancement
Primary lens: CPO
Date: 2026-04-05
Lenses involved: CTO, CPO, CEO

FINAL DECISION
--------------
Ship a pilot onboarding flow now, but defer deeper platform changes to a second phase.

KEY TRADEOFFS
-------------
- Scope vs speed: Cut non-essential setup paths to reduce implementation risk.
- UX ambition vs delivery safety: Validate the core flow before reworking shared infrastructure.
```

## Section 1: Individual Lens Positions

Each lens produces this output:

```
<LENS_NAME> POSITION
============
Verdict: [GO / MODIFY / BLOCK]
Decision context impact: [LOW / MEDIUM / HIGH]
Lens domain impact: [LOW / MEDIUM / HIGH]
Decision framing:
- Scope: [EXPAND / HOLD / NARROW / REFRAME] — [what must be in or out]
- Timeline: [NOW / PHASED / DEFER / BLOCKED] — [timing, sequencing, or trigger]
- Resource: [LIGHT / MODERATE / HEAVY / UNKNOWN] — [team, budget, or effort implication]
- Risk: [LOW / MEDIUM / HIGH / CRITICAL] — [primary failure mode]
- Success Criteria: [what must be true to call this successful]
- Assumptions / Unknowns: [critical assumption, missing input, or "None material"]
Key concerns:
- [concern 1]
- [concern 2]
- [concern 3]
Key endorsements:
- [endorsement 1]
- [endorsement 2]
Non-negotiables: [what must not change — security, stability, etc.]
```

**Definitions:**
- **Decision context impact:** Impact on the specific problem being reviewed
- **Lens domain impact:** Impact on the lens's area of expertise (e.g., for CTO: technical impact on the system)
- **Decision framing:** Compact, structured inputs the collision and synthesis engines can compare directly across lenses

## Section 2: Conflict Detection Summary

```
VERDICT ALIGNMENT
=================
Alignment: [UNANIMOUS / SPLIT / ALL DISAGREE]
<Lens A>: [GO / MODIFY / BLOCK]
<Lens B>: [GO / MODIFY / BLOCK]
[<Lens C>: [GO / MODIFY / BLOCK]]
[<Lens D>: [GO / MODIFY / BLOCK]]
```

**Alignment status definitions:**
- **UNANIMOUS:** All lenses share the same verdict
- **SPLIT:** One or more lenses dissent, but there is at least one shared verdict
- **ALL DISAGREE:** Each lens has a different verdict

## Section 3: Detailed Conflict Mapping

Stacked view across dimensions. Each dimension lists the lens's position on that dimension (GO/MODIFY/BLOCK + brief reason, or a short phrase describing their stance).

```
CONFLICT MAP
============
- Scope:
  - <Lens A>: [stance + reason]
  - <Lens B>: [stance + reason]
  - [<Lens C>: [stance + reason]]
  - [<Lens D>: [stance + reason]]
- Timeline:
  - <Lens A>: [stance + reason]
  - <Lens B>: [stance + reason]
  - [<Lens C>: [stance + reason]]
  - [<Lens D>: [stance + reason]]
- Resource:
  - <Lens A>: [stance + reason]
  - <Lens B>: [stance + reason]
  - [<Lens C>: [stance + reason]]
  - [<Lens D>: [stance + reason]]
- Risk:
  - <Lens A>: [stance + reason]
  - <Lens B>: [stance + reason]
  - [<Lens C>: [stance + reason]]
  - [<Lens D>: [stance + reason]]
- Success Criteria:
  - <Lens A>: [stance + reason]
  - <Lens B>: [stance + reason]
  - [<Lens C>: [stance + reason]]
  - [<Lens D>: [stance + reason]]
```

Use only the columns needed for the selected 2-4 lenses if you must render a table. Prefer the stacked layout below over wide markdown tables.

## Section 4: Final Alignment After Resolution

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
1. [What was in the plan] → [What it is now]
   Driven by: [Lens name] lens
   Reason: [one-line rationale]
   Tradeoff: [what we gave up]

UNANIMOUS AGREEMENTS
=====================
1. [Element] — all lenses endorse this because [reason]

DEFERRED DECISIONS
===================
1. [Decision] — deferred because [reason]. Revisit: [when/trigger].

ASSUMPTIONS / UNKNOWNS
======================
1. [Open assumption or missing information] — owner: [lens or user], impact: [LOW / MEDIUM / HIGH], next step: [how to resolve]

RISK REGISTER
==============
1. [Risk description]
  Source: [lens]
  Severity: [LOW / MEDIUM / HIGH / CRITICAL]
  Likelihood: [LOW / MEDIUM / HIGH]
  Mitigation: [plan]
2. [Risk description]
  Source: [lens]
  Severity: [LOW / MEDIUM / HIGH / CRITICAL]
  Likelihood: [LOW / MEDIUM / HIGH]
  Mitigation: [plan]
```

When a Type 5 conflict needs a user decision, do not output this section as if it were complete. Output the partial-brief split below and stop for user input:

```
DECISION SPLIT (AWAITING USER INPUT)
====================================
Decision needed: [the irreducible choice]
Why escalation happened: [why the lenses could not auto-resolve it]

OPTION A
--------
Supported by: [lens list]
What changes: [plan shape under this option]
Upside: [benefits]
Downside: [costs / risks]

OPTION B
--------
Supported by: [lens list]
What changes: [plan shape under this option]
Upside: [benefits]
Downside: [costs / risks]

What the user should answer: [specific decision prompt]
What remains blocked until then: [critical unresolved item]
```

## Section 5: Final Summary Dashboard

Use this section only when the brief is complete and no user decision is still pending.
Use short labeled lines and bullets; do not use ASCII box borders.

```
EXECUTIVE ALIGNMENT REVIEW - COMPLETION SUMMARY
===============================================
Plan: [title]
Review type: [new feature / enhancement / refactor / etc.]
Primary lens: [CEO / CTO / CPO / etc.]
Date: [YYYY-MM-DD]
Lenses involved: [list of lenses]

FINAL DECISION
--------------
[Clear recommendation with reasoning]

KEY TRADEOFFS
-------------
- [Tradeoff 1]: Chose [X] because [reason]
- [Tradeoff 2]: Chose [Y] because [reason]

RISKS ACCEPTED
--------------
- [Risk 1] (mitigated by [plan])

MITIGATION PLAN
---------------
- [Concrete step 1]
- [Concrete step 2]

DISSENTING OPINIONS
-------------------
- [Lens]: Recommends [alternative] because [reason]

CONFIDENCE LEVEL
----------------
[High / Medium / Low]

INDIVIDUAL POSITIONS
--------------------
- <Lens A>: [GO / MODIFY / BLOCK] + [key concern]
- <Lens B>: [GO / MODIFY / BLOCK] + [key concern]
- [<Lens C>: [GO / MODIFY / BLOCK] + [key concern]]
- [<Lens D>: [GO / MODIFY / BLOCK] + [key concern]]

CONFLICT RESOLUTION
-------------------
- Total conflicts: [N]
- Type 1 (Priority): [N] resolved
- Type 2 (Scope): [N] resolved
- Type 3 (Risk): [N] resolved
- Type 4 (Resource): [N] resolved
- Type 5 (Fundamental): [N] resolved / [N] awaiting input
<!-- Conflict types defined in prompts/conflict-types.md -->

OUTCOMES
--------
- Changes to plan: [N] items
- Unanimous agreements: [N] items
- Deferred decisions: [N] items
- Assumptions open: [N] items
- Risks flagged: [N] items ([N] High severity)
- Unresolved (BLOCK): [N] items — plan cannot proceed
```

## Confidence Level Criteria

- **High:** No unresolved Type 5 conflict, no material assumptions left open, no accepted high-severity risk without mitigation, and no deferred decision that blocks execution
- **Medium:** Some disagreement or deferred decisions remain, but the execution path is still clear and all critical risks or assumptions have owners and mitigation
- **Low:** User decision still required, material assumptions remain unresolved, accepted high-severity risks lack sufficient mitigation, or key execution decisions are deferred
