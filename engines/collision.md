# Collision Engine

Detects, classifies, and structures disagreements between lens positions.

## Input

The collision engine receives:
- List of lens positions (each with Verdict, concerns, endorsements, non-negotiables)
- The original problem/plan being reviewed

## Process

### Step 1: Collect Verdicts

Extract the GO/MODIFY/BLOCK verdict from each lens position.

### Step 2: Determine Alignment Status

```
If all verdicts are GO → UNANIMOUS (skip to consensus output)
If all verdicts are identical (all MODIFY or all BLOCK) → UNANIMOUS
If 2+ lenses share a verdict, others differ → 2-vs-1 (or N-vs-M)
If all verdicts differ → ALL DISAGREE
```

### Step 3: Build Conflict Map

For each dimension, extract each lens's position:

| Dimension | What to Extract |
|---|---|
| Scope | What each lens believes should be included/excluded |
| Timeline | What each lens believes about urgency and sequencing |
| Resource | What each lens believes about effort, time, budget |
| Risk | What each lens flags as risky and their severity rating |
| Success Criteria | What each lens considers "done" or "successful" |

### Step 4: Classify Each Conflict

For each disagreement found in the conflict map, classify it using `prompts/conflict-types.md`:

1. **Priority (Type 1):** Disagreement about order/sequence
2. **Scope (Type 2):** Disagreement about what's in/out
3. **Risk (Type 3):** Disagreement about risk severity or acceptance
4. **Resource (Type 4):** Disagreement about time/budget/effort
5. **Fundamental (Type 5):** Disagreement about core approach

### Step 5: Produce Conflict Detection Summary

Output:

```
VERDICT ALIGNMENT
=================
<Lens1>: [GO / MODIFY / BLOCK]
<Lens2>: [GO / MODIFY / BLOCK]
<Lens3>: [GO / MODIFY / BLOCK]
Alignment: [UNANIMOUS / 2-vs-1 / ALL DISAGREE]

CONFLICT MAP
============
Dimension       | <Lens1> | <Lens2> | <Lens3>
----------------|---------|---------|--------
Scope           | [view]  | [view]  | [view]
Timeline        | [view]  | [view]  | [view]
Resource        | [view]  | [view]  | [view]
Risk            | [view]  | [view]  | [view]
Success Criteria| [view]  | [view]  | [view]

CONFLICTS DETECTED: [N]
  Type 1 (Priority):  [N]
  Type 2 (Scope):     [N]
  Type 3 (Risk):      [N]
  Type 4 (Resource):  [N]
  Type 5 (Fundamental): [N]
```

## Special Cases

- **UNANIMOUS GO:** Output "All lenses agree — no conflicts detected. Proceeding to synthesis for final brief."
- **UNANIMOUS BLOCK:** Output "All lenses agree this plan should be blocked. Critical issues: [list]."
- **Single lens review:** Skip collision entirely — output "Single lens review — no collision analysis applicable."
