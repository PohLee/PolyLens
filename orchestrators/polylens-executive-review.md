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

Before lens selection, read and follow `../shared/prompts/project-context.md` to load an attributed snapshot from the target project's indexed memory.

For PR crisis response or reputation recovery, read and apply `../shared/playbooks/pr-crisis-recovery.md` before forming lens positions. Its gates are mandatory even when research is disabled. Carry its evidence ledger and response checks through the existing brief sections.

### Step 0.5: Harness Execution (if active)

If the harness is active (detected in Step 2.5 of the router), follow these instructions:

**Load Hook Content:**
For each enabled hook in the registry, read the hook file from `../shared/hooks/<stage>/<name>.md`.
Inject the hook's content (everything after the frontmatter) into the prompt at the appropriate stage.

**Apply Reasoning Controls:**
Use the emitted plan and explicit current-request overrides as the authoritative configuration.
If running without Python, read the JSON frontmatter directly. If reasoning controls are active:
- Set analysis depth per the config (surface/standard/deep)
- Inject constraints into the prompt before lens selection
- Apply output format settings

**Execute Orchestration:**
If `../shared/harness/orchestration.md` has multiple instances:
- Run instances in the specified order (sequential mode)
- In parallel/conditional mode, execute only instances whose dependencies completed; honor host concurrency limits
- For each instance, apply its specific lenses, hooks, and reasoning settings
- Use previous instance output as context for dependent instances
- Evaluate conditions before running conditional instances
- Conditions are plain language, not code to eval; if a condition cannot be determined, report and stop that branch

**Run Validation:**
After producing the decision brief, if `../shared/harness/validation.md` has validation enabled:
- Run the contract check only for full standard briefs (complete or partial); concise/custom output needs a separate format contract
- Treat the legacy quality_gate setting as advisory format hints, never a reasoning-quality score
- Run deterministic consistency checks for verdict alignment; factual verification requires evidence review
- Append validation report to the brief

For deterministic checks, save to a user-authorized artifact or temporary file and invoke the
bundled `../shared/tools/harness.py validate <absolute-brief-path>` with the selected validation
configuration. A nonzero exit is a failed check, not a completed validation. Do not run contract
checks on the validation report itself. Manual evidence review remains separate.

**Hook Injection Format:**
When injecting a hook's content, prefix it with:
```
## Active Hook: <name> (<stage>)
<hook content>
```

This ensures the LLM knows which hook is being applied and at what stage.

### Step 1: Select Lenses

Read the bundled lens registry at `../shared/prompts/lens-registry.md`.

**If the user specified lenses:** Use those lenses. Respect explicit user choice.

**If no lenses specified:** Apply the authoritative selection contract:

<!-- BEGIN GENERATED SELECTION -->
1. **Filter active lenses:** Only consider lenses where `active: true`
2. **Identify the decision anchor:** Separate the primary decision being asked from supporting constraints. The primary decision should drive the first lens selection.
3. **Promote decision owners first:** If the anchor matches a lens's `owns_decisions`, that lens should usually be selected before adjacent lenses that only evaluate consequences of the decision.
4. **Score explicit wording:** Exact or near-exact matches against `triggers` score +2; domain/theme matches score +1
5. **Downweight ambient constraints:** Budget, timeline, team size, compliance, or risk details count as supporting signals unless the user explicitly asks to optimize for them or they are central to the decision itself
6. **Apply veto coverage:** If the prompt explicitly touches a lens's `veto_on` area, include that lens or state why it is being deferred.
7. **Rank by relevance:** Sum the scores and keep a note of which user constraints each lens covers, but never let an adjacent lens displace the primary owner of the decision anchor.
8. **Apply pairing rules:** If a top lens has `pairs_with` recommendations, boost those lenses' scores by 0.5 (only if they are also active)
9. **Promote strategic complement when needed:** If the anchor decision is foundational and company-shaping, add the nearest strategy lens even if the wording is technical. For technical architecture or tech stack choices, this usually means pairing CTO with CEO.
10. **Prefer coverage without drift:** For a multi-lens review, select 2-4 lenses covering the main decision and its highest-consequence tradeoffs. For a focused review, Select exactly one lens: apply the same ranking, treat veto coverage as eligibility, and recommend a multi-lens review if one lens cannot cover the decision. Pairing and strategic complements do not add lenses in focused mode.
11. **Cap secondary lenses:** After the anchor lens, its owner, and any necessary strategy complement, add supporting lenses only when they introduce a distinct decision axis with explicit evidence. Do not add finance, security, or operations lenses solely because those concerns exist in the background.
12. **Break ties deterministically:** Use this order: stronger ownership match, stronger decision-anchor match, more direct user wording match, stronger trigger match, `default: true`, registry order
13. **Fallback:** Only if all scores < 2, use active lenses marked `default: true`; exactly 2 is a strong match. In focused mode choose the highest-ranked default lens only.
<!-- END GENERATED SELECTION -->

Pricing guidance: for pricing, packaging, monetization, or sales-motion decisions, include CRO by default. Add CEO for strategic posture, CFO for unit economics or runway, CPO for packaging or product tier design, and YC only when startup simplicity or fundraising framing is explicitly part of the question.

Announce which lenses were selected and why.

### Step 2: Run Each Lens

For each selected lens, read the corresponding shared lens brief at `../shared/lenses/lens-<name>.md` and follow its review process.

Run lenses sequentially to preserve context. For each lens:
1. Apply the lens's philosophy, directives, and cognitive patterns
2. Optionally use tools from `../shared/prompts/lens-capabilities.md` and reusable methods from `../shared/prompts/shared-playbooks.md` if they would strengthen the analysis
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
2. For Type 5 (Fundamental) conflicts or any escalation threshold in the conflict taxonomy (including Type 4 resource gaps > 2x with defensible estimates), output the decision split format and stop for user input
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
- **All lenses agree:** Complete framing comparison; matching verdicts alone do not establish zero conflicts or high confidence
- **Unresolvable conflict:** Escalate to user with split recommendations
- **Context window limits:** Run lenses sequentially, summarize between steps
- **Ambiguous tie between lenses:** Use deterministic tie-break rules; do not pick arbitrarily

## Important Rules

- Always read `../shared/prompts/lens-registry.md` before selecting lenses
- Always read each selected lens brief under `../shared/lenses/` before running it
- When a deeper reusable method is needed, read the relevant file under `../shared/playbooks/`
- Always read `../shared/engines/collision.md` before detecting conflicts
- Always read `../shared/engines/synthesis.md` before synthesizing
- Always read `../shared/prompts/output-template.md` before formatting output
- When the user asks for a markdown artifact file, save it under `docs/polylens/<category>/YYMMDD_slug_rN.md` instead of creating loose markdown files at the repo root
- Never skip the collision step even if lenses mostly agree
- Never auto-resolve Type 5 (Fundamental) conflicts — escalate to user
- If a user decision is still needed, stop after the partial brief and wait for input
