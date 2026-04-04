---
name: polylens-executive-review
version: 1
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

Read the lens registry at `prompts/lens-registry.md`.

**If the user specified lenses:** Use those lenses. Respect explicit user choice.

**If no lenses specified:** Run the selection algorithm:
1. Filter active lenses: Only consider lenses where `active: true`
2. Scan the problem description against each lens's `domains` and `triggers` from the registry
3. Score lenses by match count
4. Boost scores for lenses in `pairs_with` of top-scoring lenses (+0.5, only if active)
5. Select top 2-4 lenses (minimum 2, maximum 4)
6. If no strong matches (all scores < 2), use default lenses (CEO + CTO + CPO)

Announce which lenses were selected and why.

### Step 2: Run Each Lens

For each selected lens, read the corresponding `skills/lens-<name>.md` file and follow its review process.

Run lenses sequentially to preserve context. For each lens:
1. Apply the lens's philosophy, directives, and cognitive patterns
2. Optionally use tools from `prompts/lens-capabilities.md` if it would strengthen the analysis
3. Produce the lens position in the required format (between `---BEGIN <LENS> POSITION---` and `---END <LENS> POSITION---` delimiters)
4. Provide reasoning paragraphs

### Step 3: Collision Detection

Run the collision engine by reading `engines/collision.md` and following its process:
1. Collect all lens verdicts
2. Determine alignment status (UNANIMOUS / 2-vs-1 / ALL DISAGREE)
3. Build conflict map across dimensions (Scope, Timeline, Resource, Risk, Success Criteria)
4. Classify each conflict by type (Priority, Scope, Risk, Resource, Fundamental)
5. Reference `prompts/conflict-types.md` for type definitions

Output the Conflict Detection Summary.

### Step 4: Synthesis

Run the synthesis engine by reading `engines/synthesis.md` and following its process:
1. Apply resolution strategies based on conflict type
2. For Type 5 (Fundamental) conflicts, escalate to user for decision
3. Assemble the Final Alignment section
4. Assemble the Final Summary Dashboard

### Step 5: Output Decision Brief

Produce the complete 5-section decision brief following the template in `prompts/output-template.md`:

1. Individual Lens Positions
2. Conflict Detection Summary
3. Detailed Conflict Mapping
4. Final Alignment After Resolution
5. Final Summary Dashboard

## Error Handling

- **Problem too vague:** Ask clarifying questions before running lenses
- **No matching lenses:** Fall back to default trio (CEO + CTO + CPO)
- **All lenses agree:** Skip collision engine, output consensus brief
- **Unresolvable conflict:** Escalate to user with split recommendations
- **Context window limits:** Run lenses sequentially, summarize between steps

## Important Rules

- Always read `prompts/lens-registry.md` before selecting lenses
- Always read each lens's skill file before running it
- Always read `engines/collision.md` before detecting conflicts
- Always read `engines/synthesis.md` before synthesizing
- Always read `prompts/output-template.md` before formatting output
- Never skip the collision step even if lenses mostly agree
- Never auto-resolve Type 5 (Fundamental) conflicts — escalate to user
