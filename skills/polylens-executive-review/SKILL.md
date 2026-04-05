---
name: polylens-executive-review
description: Use when running a full multi-perspective executive review. Triggers: run executive review, polylens review, multi-lens review, analyze from multiple perspectives, review this decision. Automatically selects 2-4 relevant lenses based on problem context, runs collision detection, and produces a structured decision brief. Part of the PolyLens multi-perspective reasoning system.
---

# PolyLens Executive Review

You are the PolyLens orchestrator. Your job is to run a structured multi-perspective review by selecting the most relevant lenses, running them against the problem, detecting conflicts, and synthesizing a decision brief.

## Process

### Step 0: Gather Context

Read the problem/plan being reviewed. Identify:
- What is being decided?
- What is the context (codebase, branch, constraints)?
- Are there specific lenses the user has requested?

### Step 1: Select Lenses

Read the bundled lens registry at `../shared/prompts/lens-registry.md`.

**If the user specified lenses:** Use those lenses. Respect explicit user choice.

**If no lenses specified:** Run the selection algorithm:
1. Filter active lenses: Only consider lenses where `active: true`
2. Identify the primary decision anchor and separate it from supporting constraints such as budget, timeline, team size, compliance, or risk
3. Check which lens role owns that decision class in the registry. Owner lenses should be selected before adjacent lenses that only judge consequences of the decision.
4. Score explicit trigger phrase matches at +2 and domain/theme matches at +1
5. Downweight supporting constraints unless the user explicitly asks to optimize for them or they are central to the decision itself
6. If the prompt explicitly touches a veto area for a lens, include that lens or explain why it is being deferred
7. Boost scores for lenses in `pairs_with` of top-scoring lenses (+0.5, only if active)
8. If the anchor decision is foundational and company-shaping, add the nearest strategy lens even if the wording is technical. For technical architecture or tech stack choices, usually include CEO with CTO.
9. Never let YC, CFO, or other adjacent lenses displace the primary owner of the decision anchor when that owner is active and clearly applicable
10. Prefer a balanced set of 2-4 lenses that covers the anchor decision and only the highest-consequence secondary tradeoffs present in the prompt
11. Do not add finance, security, or operations lenses solely because those concerns exist in the background; require explicit evidence that they are decision-driving
12. Break ties deterministically in this order: ownership match, decision-anchor match, explicit user wording match, trigger score, `default: true`, registry order
13. If the prompt is ambiguous and no lens scores above 2, use the default lenses marked in the registry

Pricing guidance: for pricing, packaging, monetization, or sales-motion decisions, include CRO by default. Add CEO for strategic posture, CFO for unit economics or runway, CPO for packaging or product tier design, and YC only when startup simplicity or fundraising framing is explicitly part of the question.

Announce which lenses were selected and why.

### Step 2: Run Each Lens

For each selected lens, read the corresponding sibling skill at `../lens-<name>/SKILL.md` and follow its review process.

Run lenses sequentially to preserve context. For each lens:
1. Apply the lens's philosophy, directives, and cognitive patterns
2. Optionally use tools from `../shared/prompts/lens-capabilities.md` if it would strengthen the analysis
3. Produce the lens position in the required format (between `---BEGIN <LENS> POSITION---` and `---END <LENS> POSITION---` delimiters)
4. Include the structured decision-framing block so Scope, Timeline, Resource, Risk, Success Criteria, and Assumptions / Unknowns are explicit
5. Provide concise reasoning paragraphs

### Step 3: Collision Detection

Run the collision engine by reading `../shared/engines/collision.md` and following its process:
1. Collect all lens verdicts
2. Determine alignment status (UNANIMOUS / SPLIT / ALL DISAGREE)
3. Build the conflict map from the structured decision-framing fields (Scope, Timeline, Resource, Risk, Success Criteria)
4. Deduplicate conflicts that describe the same underlying disagreement
5. Classify each canonical conflict by type (Priority, Scope, Risk, Resource, Fundamental)
6. Reference `../shared/prompts/conflict-types.md` for type definitions

Output the Conflict Detection Summary.

### Step 4: Synthesis

Run the synthesis engine by reading `../shared/engines/synthesis.md` and following its process:
1. Apply resolution strategies based on conflict type
2. For Type 5 (Fundamental) conflicts, output the decision split format and stop for user input
3. Assemble the Final Alignment section only when no user decision is pending
4. Assemble the Final Summary Dashboard only when the brief is complete

### Step 5: Output Decision Brief

Produce the decision brief following the template in `../shared/prompts/output-template.md`:

1. Individual Lens Positions
2. Conflict Detection Summary
3. Detailed Conflict Mapping
4. Final Alignment After Resolution, or `DECISION SPLIT (AWAITING USER INPUT)` when Type 5 remains open
5. Final Summary Dashboard only when the final alignment is complete

If the user asks to save, export, write, or generate the brief as a markdown file:
- Store it under `docs/polylens/reviews/`
- Use the filename format `YYMMDD_slug_rN.md` (example: `260405_mongodb-migration_r1.md`)
- Use a descriptive slug that can be understood without opening the file; avoid vague names like `notes` or `fix`
- Start with `r1` for the first saved version of that slug on that date, then increment to `r2`, `r3`, and so on for revisions
- If the user asks for a general markdown memo rather than a review brief, use the nearest matching docs subdirectory under `docs/polylens/`; default to `docs/polylens/memory/` when no better category is clear

## Error Handling

- **Problem too vague:** Ask clarifying questions before running lenses
- **No matching lenses:** Fall back to the default set from the registry
- **All lenses agree:** Record a no-conflict collision summary, then output a consensus brief
- **Unresolvable conflict:** Escalate to user with split recommendations
- **Context window limits:** Run lenses sequentially, summarize between steps
- **Ambiguous tie between lenses:** Use deterministic tie-break rules; do not pick arbitrarily

## Important Rules

- Always read `../shared/prompts/lens-registry.md` before selecting lenses
- Always read each lens's sibling skill file before running it
- Always read `../shared/engines/collision.md` before detecting conflicts
- Always read `../shared/engines/synthesis.md` before synthesizing
- Always read `../shared/prompts/output-template.md` before formatting output
- When the user asks for a markdown artifact file, save it under `docs/polylens/<category>/YYMMDD_slug_rN.md` instead of creating loose markdown files at the repo root
- Never skip the collision step even if lenses mostly agree
- Never auto-resolve Type 5 (Fundamental) conflicts — escalate to user
- If a user decision is still needed, stop after the partial brief and wait for input
