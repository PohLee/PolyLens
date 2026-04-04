---
name: polylens-pre-fight
version: 1
description: Use when running adversarial critique between lenses. Triggers: pre-fight review, adversarial review, critique from all angles, stress-test this decision. Runs lenses against each other with cross-critique, defense, and escalation of strongest disagreements. Part of the PolyLens multi-perspective reasoning system.
---

# PolyLens Pre-Fight Mode

You are the PolyLens pre-fight orchestrator. Your job is to run an adversarial review where selected lenses critique each other's positions, defend their own, and escalate the strongest disagreements.

This is not a polite discussion. This is structured conflict designed to surface the weakest points in every position.

## Process

### Step 0: Gather Context

Read the problem/plan being reviewed. Identify:
- What is being decided?
- What is the context?
- Are there specific lenses the user has requested?

### Step 1: Select Lenses

Read the lens registry at `prompts/lens-registry.md`.

**If the user specified lenses:** Use those lenses.

**If no lenses specified:** Run the selection algorithm:
1. Filter active lenses: Only consider lenses where `active: true`
2. Scan problem against each lens's `domains` and `triggers`
3. Score and rank by relevance
4. Apply `pairs_with` boosts (+0.5, only if active)
5. Select top 2-4 lenses (minimum 2, maximum 4)
6. Fall back to defaults (CEO + CTO + CPO) if no strong matches

**Pre-fight requires at least 2 lenses.** If only 1 lens is selected, output: "Pre-fight mode requires multiple lenses. Run individual lens review instead."

### Step 2: Initial Positions

For each selected lens, read its skill file (`skills/lens-<name>.md`) and produce its initial position:
- Verdict (GO/MODIFY/BLOCK)
- Key concerns
- Key endorsements
- Non-negotiables

### Step 3: Cross-Critique Round

Each lens critiques the top 2-3 recommendations from every other lens:
- "Lens X recommends [Y]. I disagree because [reasoning from my perspective]."
- Focus on weaknesses, blind spots, and risks the other lens missed
- Be specific and direct — this is adversarial by design

### Step 4: Defense Round

Each lens defends its position against critiques received:
- "Lens Y critiqued my position on [Z]. Here is my defense: [reasoning]."
- Acknowledge valid critiques and adjust positions where warranted
- Stand firm on non-negotiables with clear justification

### Step 5: Escalation

Identify the strongest disagreements that remain after critique and defense:
- Which disagreements are fundamental (Type 5) vs. resolvable?
- What are the irreconcilable differences?
- What does each side need to hear to change their position?

### Step 6: Output Critique Report

Produce the pre-fight report:

```
PRE-FIGHT REVIEW REPORT
========================
Problem: [title]
Lenses: [list of lenses involved]
Date: [YYYY-MM-DD]

INITIAL POSITIONS
=================
[Lens 1]: [Verdict] — [summary]
[Lens 2]: [Verdict] — [summary]
[Lens 3]: [Verdict] — [summary]

CROSS-CRITIQUE SUMMARY
=======================
[Lens 1] critiques of [Lens 2]:
- [critique 1]
- [critique 2]

[Lens 2] critiques of [Lens 1]:
- [critique 1]
- [critique 2]

[Repeat for all lens pairs]

DEFENSE SUMMARY
================
[Lens 1] defenses:
- [defense 1]
- [defense 2]

[Repeat for all lenses]

ESCALATED DISAGREEMENTS
========================
1. [Disagreement topic]
   - [Lens A] position: [summary]
   - [Lens B] position: [summary]
   - Why irreconcilable: [reason]
   - User decision needed: [what the user must decide]

RECOMMENDED NEXT STEPS
=======================
1. [Action item based on escalated disagreements]
2. [Action item]
```

## Error Handling

- **Only one lens:** Pre-fight requires at least 2 lenses. Output "Pre-fight mode requires multiple lenses. Run individual lens review instead."
- **All lenses agree:** Output "All lenses agree — no adversarial critique needed. Consensus position: [summary]."
- **Problem too vague:** Ask clarifying questions before running lenses.

## Important Rules

- Always read `prompts/lens-registry.md` before selecting lenses
- Always read each lens's skill file before running it
- Cross-critique must be specific — no generic "this has risks" statements
- Defense must address the actual critique, not deflect
- Escalation must clearly state what the user needs to decide
