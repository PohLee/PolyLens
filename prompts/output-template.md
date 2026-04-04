# Output Templates

All PolyLens reviews produce structured output following these templates.

## Section 1: Individual Lens Positions

Each lens produces this output:

```
<LENS_NAME> POSITION
============
Verdict: [GO / MODIFY / BLOCK]
Decision context impact: [LOW / MEDIUM / HIGH]
Lens domain impact: [LOW / MEDIUM / HIGH]
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

## Section 2: Conflict Detection Summary

```
VERDICT ALIGNMENT
=================
<Lens1>: [GO / MODIFY / BLOCK]
<Lens2>: [GO / MODIFY / BLOCK]
<Lens3>: [GO / MODIFY / BLOCK]
Alignment: [UNANIMOUS / 2-vs-1 / ALL DISAGREE]
```

**Alignment status definitions:**
- **UNANIMOUS:** All lenses share the same verdict
- **2-vs-1:** Two lenses agree, one dissents
- **ALL DISAGREE:** Each lens has a different verdict

## Section 3: Detailed Conflict Mapping

Matrix view across dimensions. Each cell contains the lens's position on that dimension (GO/MODIFY/BLOCK + brief reason, or a short phrase describing their stance).

```
CONFLICT MAP
============
Dimension       | <Lens1>           | <Lens2>           | <Lens3>
----------------|-------------------|-------------------|------------------
Scope           | [GO + reason]     | [MODIFY + reason] | [GO + reason]
Timeline        | [GO + reason]     | [GO + reason]     | [BLOCK + reason]
Resource        | [GO + reason]     | [MODIFY + reason] | [GO + reason]
Risk            | [GO + reason]     | [GO + reason]     | [GO + reason]
Success Criteria| [GO + reason]     | [GO + reason]     | [GO + reason]
```

## Section 4: Final Alignment After Resolution

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

RISK REGISTER
==============
RISK              | SOURCE  | SEVERITY | LIKELIHOOD | MITIGATION
------------------|---------|----------|------------|------------
[description]     | [lens]  | [severity] | [likelihood] | [plan]
[description]     | [lens]  | [severity] | [likelihood] | [plan]
```

## Section 5: Final Summary Dashboard

```
+====================================================================+
|         EXECUTIVE ALIGNMENT REVIEW - COMPLETION SUMMARY            |
+====================================================================+
| Plan               | [title]                                       |
| Review type        | [new feature / enhancement / refactor / etc.] |
| Primary lens       | [CEO / CTO / CPO / etc.]                      |
| Date               | [YYYY-MM-DD]                                  |
| Lenses involved    | [list of lenses]                              |
+--------------------------------------------------------------------+
| FINAL DECISION                                                      |
| [Clear, actionable recommendation with reasoning]                  |
|                                                                     |
| KEY TRADEOFFS                                                       |
| - [Tradeoff 1]: Chose [X] because [reason]                         |
| - [Tradeoff 2]: Chose [Y] because [reason]                         |
|                                                                     |
| RISKS ACCEPTED                                                      |
| - [Risk 1] (mitigated by [plan])                                   |
|                                                                     |
| MITIGATION PLAN                                                     |
| [Concrete steps to reduce accepted risks]                          |
|                                                                     |
| DISSENTING OPINIONS                                                 |
| - [Lens]: Recommends [alternative] because [reason]                |
|                                                                     |
| CONFIDENCE LEVEL: [High / Medium / Low]                            |
+--------------------------------------------------------------------+
| INDIVIDUAL POSITIONS                                                |
| <Lens1> verdict | [GO / MODIFY / BLOCK] + [key concern]            |
| <Lens2> verdict | [GO / MODIFY / BLOCK] + [key concern]            |
| <Lens3> verdict | [GO / MODIFY / BLOCK] + [key concern]            |
+--------------------------------------------------------------------+
| CONFLICT RESOLUTION                                                 |
| Total conflicts    | [N]                                           |
| Type 1 (Priority)  | [N] resolved                                  |
| Type 2 (Scope)     | [N] resolved                                  |
| Type 3 (Risk)      | [N] resolved                                  |
| Type 4 (Resource)  | [N] resolved                                  |
| Type 5 (Fundamental)| [N] resolved / [N] UNRESOLVED               |
<!-- Conflict types defined in prompts/conflict-types.md -->
+--------------------------------------------------------------------+
| OUTCOMES                                                            |
| Changes to plan    | [N] items                                     |
| Unanimous agreements| [N] items                                    |
| Deferred decisions | [N] items                                     |
| Risks flagged      | [N] items ([N] High severity)                 |
| Unresolved (BLOCK) | [N] items — plan cannot proceed               |
+====================================================================+
```

## Confidence Level Criteria

- **High:** All selected lenses agree (UNANIMOUS) or all conflicts are auto-resolved
- **Medium:** Some disagreement but synthesis found acceptable compromise; no unresolved Type 5 conflicts
- **Low:** Strong disagreement, unresolved Type 5 conflicts, or high-risk tradeoffs accepted
