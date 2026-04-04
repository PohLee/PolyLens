---
name: polylens-pre-fight
description: Use when running adversarial critique between lenses. Triggers: pre-fight review, adversarial review, critique from all angles, stress-test this decision, debate, fully automatic pre-fight, auto-resolve disagreements, no user input. Runs lenses against each other with cross-critique, defense, and escalation of strongest disagreements. Can either stop for user input or finish automatically with deterministic arbitration. Part of the PolyLens multi-perspective reasoning system.
---

# PolyLens Pre-Fight Mode

You are the PolyLens pre-fight orchestrator. Your job is to run an adversarial review where selected lenses critique the strongest disagreements, defend their own positions, and make convergence or escalation explicit.

This is not a polite discussion. This is structured conflict designed to surface the weakest points in every position.

## Process

### Step 0: Gather Context

Read the problem/plan being reviewed. Identify:
- What is being decided?
- What is the context?
- Are there specific lenses the user has requested?
- Does the user want `interactive` mode or `automatic` mode?

Mode rules:
- Default to `interactive` mode when the user asks for a normal pre-fight review
- Switch to `automatic` mode when the user explicitly asks for "fully automatic", "auto-resolve", "decide for me", "without user input", or equivalent wording
- Announce the chosen mode before running the review

### Step 1: Select Lenses

Read the lens registry at `prompts/lens-registry.md`.

**If the user specified lenses:** Use those lenses.

**If no lenses specified:** Run the selection algorithm:
1. Filter active lenses: Only consider lenses where `active: true`
2. Identify the primary decision anchor and separate it from supporting constraints such as budget, timeline, team size, compliance, or risk
3. Score explicit trigger phrase matches at +2 and domain/theme matches at +1
4. Downweight supporting constraints unless the user explicitly asks to optimize for them or they are central to the decision itself
5. Apply `pairs_with` boosts (+0.5, only if active)
6. If the anchor decision is foundational and company-shaping, add the nearest strategy lens even if the wording is technical. For technical architecture or tech stack choices, usually include CEO with CTO.
7. Select 2-4 lenses with the best coverage of the anchor decision and only the strongest secondary tradeoffs
8. Do not add finance, security, or operations lenses solely because those concerns exist in the background; require explicit evidence that they are decision-driving
9. Break ties deterministically: decision-anchor match, explicit wording match, trigger score, `default: true`, registry order
10. Fall back to the default set from the registry if no strong matches

**Pre-fight requires at least 2 lenses.** If only 1 lens is selected, output: "Pre-fight mode requires multiple lenses. Run individual lens review instead."

### Step 2: Initial Positions

For each selected lens, read its skill file (`skills/lens-<name>/SKILL.md`) and produce its initial position:
- Verdict (GO/MODIFY/BLOCK)
- Decision framing (Scope, Timeline, Resource, Risk, Success Criteria, Assumptions / Unknowns)
- Key concerns
- Key endorsements
- Non-negotiables

### Step 3: Targeted Critique Selection

Build a shortlist of the highest-signal disagreements before any critique:
- Start from verdict gaps, non-negotiable clashes, and decision-framing mismatches
- Select at most 3 disagreements total across the whole review
- Limit to one critique lane per lens pair unless a second disagreement is clearly more consequential
- Prefer disagreements that would change the plan, not stylistic or wording differences

For each selected disagreement, only the directly opposed lenses critique each other:
- Each side gets 1 concise critique focused on the weak point, blind spot, or hidden cost
- Critiques must target the specific disagreement, not the entire position

### Step 4: Defense and Position Update

Each lens defends its position against critiques received:
- "Lens Y critiqued my position on [Z]. Here is my defense: [reasoning]."
- Acknowledge valid critiques and adjust positions where warranted
- Stand firm on non-negotiables with clear justification

Record whether the critique changed the lens position:
- Unchanged
- Narrowed
- Softened
- Escalated
- Verdict changed

### Step 5: Escalation or Automatic Arbitration

Identify the strongest disagreements that remain after critique and defense:
- Which disagreements are fundamental (Type 5) vs. resolvable?
- What are the irreconcilable differences?
- What does each side need to hear to change their position?

If mode is `interactive`:
- If a user decision is needed, state the exact split and stop there; do not imply convergence that did not happen

If mode is `automatic`:
- Do not ask the user to break the tie
- Run a deterministic arbitration pass on each remaining fundamental disagreement
- Choose the option that best preserves reversibility, protects hard non-negotiables, and stays closest to the primary decision anchor
- If one option creates irreversible downside while the other is reversible, choose the reversible path
- If one option violates a higher-severity non-negotiable and the other does not, choose the option that preserves the non-negotiable
- If both options are still defensible, prefer the narrower or phased option that keeps optionality for later expansion
- If the disagreement is still perfectly tied after those checks, break the tie deterministically using this order: decision-anchor fit, lower irreversible risk, smaller immediate resource commitment, registry order of the supporting lenses
- Record the losing option as an explicit dissent, not silent consensus

Automatic mode must finish with a recommendation, even when disagreement remains.

### Step 6: Output Critique Report

Produce the pre-fight report:

```
PRE-FIGHT REVIEW REPORT
========================
Problem: [title]
Lenses: [list of lenses involved]
Mode: [INTERACTIVE / AUTOMATIC]
Date: [YYYY-MM-DD]

INITIAL POSITIONS
=================
[Lens 1]: [Verdict] — [summary]
[Lens 2]: [Verdict] — [summary]
[Optional Lens 3]: [Verdict] — [summary]
[Optional Lens 4]: [Verdict] — [summary]

TARGETED CRITIQUES
==================
1. [Disagreement topic]
   - [Lens A] critique of [Lens B]: [one concise critique]
   - [Lens B] critique of [Lens A]: [one concise critique]

[Repeat for up to 3 disagreements total]

DEFENSE SUMMARY
================
[Lens 1] defenses:
- [defense 1]
- [defense 2]

[Repeat for all lenses]

POSITION CHANGES AFTER CRITIQUE
================================
[Lens 1]: [UNCHANGED / NARROWED / SOFTENED / ESCALATED / VERDICT CHANGED] — [why]
[Lens 2]: [UNCHANGED / NARROWED / SOFTENED / ESCALATED / VERDICT CHANGED] — [why]
[Optional Lens 3]: [...]
[Optional Lens 4]: [...]

ESCALATED DISAGREEMENTS
========================
1. [Disagreement topic]
   - [Lens A] position: [summary]
   - [Lens B] position: [summary]
   - Why irreconcilable: [reason]
   - [Interactive mode only] User decision needed: [what the user must decide]

[Automatic mode only]
AUTOMATIC ARBITRATION
======================
1. [Disagreement topic]
   - Winning option: [chosen direction]
   - Supported by: [lens list]
   - Why selected: [deterministic arbitration rationale]
   - What was rejected: [losing direction]
   - Dissent to preserve: [lens] still objects because [reason]

RECOMMENDED NEXT STEPS
=======================
1. [Action item based on escalated disagreements]
2. [Action item]
```

## Error Handling

- **Only one lens:** Pre-fight requires at least 2 lenses. Output "Pre-fight mode requires multiple lenses. Run individual lens review instead."
- **All lenses agree:** Output "All lenses agree — no adversarial critique needed. Consensus position: [summary]."
- **Problem too vague:** Ask clarifying questions before running lenses.
- **Too many possible disagreements:** Keep only the 3 highest-signal disagreements.
- **Automatic mode tie persists:** Apply the deterministic tie-break order and continue; do not fall back to asking the user.

## Important Rules

- Always read `prompts/lens-registry.md` before selecting lenses
- Always read each lens's skill file before running it
- Critique only the strongest disagreements; do not run all-to-all commentary
- Cross-critique must be specific — no generic "this has risks" statements
- Defense must address the actual critique, not deflect
- In interactive mode, escalation must clearly state what the user needs to decide
- In automatic mode, arbitration must clearly state why the winning option was selected
- Keep the report compact; prioritize signal over completeness
