# Collision Engine

Detects, classifies, and structures disagreements between lens positions.

## Input

The collision engine receives:
- List of lens positions (each with Verdict, impacts, decision framing for Scope/Timeline/Resource/Risk/Success Criteria, assumptions/unknowns, concerns, endorsements, non-negotiables)
- The original problem/plan being reviewed

## Process

### Step 1: Collect Verdicts

Extract the GO/MODIFY/BLOCK verdict from each lens position.

### Step 2: Determine Alignment Status

```
If all verdicts are GO → UNANIMOUS (skip to consensus output)
If all verdicts are identical (all MODIFY or all BLOCK) → UNANIMOUS
If 2+ lenses share a verdict, others differ → SPLIT
If all verdicts differ → ALL DISAGREE
```

### Step 3: Build Conflict Map

For each dimension, extract each lens's structured position from the decision-framing block first. Use concerns, endorsements, and reasoning only to clarify the one-line entry if needed.

| Dimension | What to Extract |
|---|---|
| Scope | What each lens believes should be included/excluded |
| Timeline | What each lens believes about urgency and sequencing |
| Resource | What each lens believes about effort, time, budget |
| Risk | What each lens flags as risky and their severity rating |
| Success Criteria | What each lens considers "done" or "successful" |

### Step 4: Deduplicate Conflicts

Before counting conflicts, merge duplicates that describe the same underlying disagreement:

- If the same issue appears in multiple dimensions, keep one canonical conflict entry and list all affected dimensions.
- If two lenses restate the same objection in different words, count it once.
- If wording differs but the required user decision is the same, count it once.
- Only create separate conflicts when resolving one would not resolve the other.

### Step 5: Classify Each Conflict

For each disagreement found in the conflict map, classify it using `prompts/conflict-types.md`:

1. **Priority (Type 1):** Disagreement about order/sequence
2. **Scope (Type 2):** Disagreement about what's in/out
3. **Risk (Type 3):** Disagreement about risk severity or acceptance
4. **Resource (Type 4):** Disagreement about time/budget/effort
5. **Fundamental (Type 5):** Disagreement about core approach

### Step 6: Produce Conflict Detection Summary

Output:

```
VERDICT ALIGNMENT
=================
Alignment: [UNANIMOUS / SPLIT / ALL DISAGREE]
<Lens A>: [GO / MODIFY / BLOCK]
<Lens B>: [GO / MODIFY / BLOCK]
[<Lens C>: [GO / MODIFY / BLOCK]]
[<Lens D>: [GO / MODIFY / BLOCK]]

CONFLICT MAP
============
- Scope:
  - <Lens A>: [view]
  - <Lens B>: [view]
  - [<Lens C>: [view]]
  - [<Lens D>: [view]]
- Timeline:
  - <Lens A>: [view]
  - <Lens B>: [view]
  - [<Lens C>: [view]]
  - [<Lens D>: [view]]
- Resource:
  - <Lens A>: [view]
  - <Lens B>: [view]
  - [<Lens C>: [view]]
  - [<Lens D>: [view]]
- Risk:
  - <Lens A>: [view]
  - <Lens B>: [view]
  - [<Lens C>: [view]]
  - [<Lens D>: [view]]
- Success Criteria:
  - <Lens A>: [view]
  - <Lens B>: [view]
  - [<Lens C>: [view]]
  - [<Lens D>: [view]]

CONFLICTS DETECTED: [N]
  Type 1 (Priority):  [N]
  Type 2 (Scope):     [N]
  Type 3 (Risk):      [N]
  Type 4 (Resource):  [N]
  Type 5 (Fundamental): [N]

CANONICAL CONFLICT LIST
=======================
1. [Conflict statement]
   Type: [1 / 2 / 3 / 4 / 5]
   Lenses: [list]
   Affected dimensions: [Scope / Timeline / Resource / Risk / Success Criteria]
```

Prefer stacked markdown blocks over wide tables so the summary stays readable in chat and narrow editor panes.

## Special Cases

- **UNANIMOUS GO:** Output "All lenses agree — no conflicts detected. Proceeding to synthesis for final brief."
- **UNANIMOUS BLOCK:** Output "All lenses agree this plan should be blocked. Critical issues: [list]."
- **Single lens review:** Skip collision entirely — output "Single lens review — no collision analysis applicable."
- **Near-match wording:** If lenses differ only in phrasing but not in practical action, do not classify it as a conflict.
