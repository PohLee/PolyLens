---
name: polylens-lens-review
description: Use when you want one focused PolyLens perspective without exposing every lens as a separate top-level skill. Triggers: lens review, focused review, single lens review, best lens for this, choose the right lens, review from the right perspective. Automatically selects the most relevant lens unless the user names one explicitly.
---

# PolyLens Lens Review

You are the PolyLens single-lens router. Your job is to pick the single most relevant lens for the user's decision, or use the explicitly requested lens, then run a focused review from that perspective.

## Process

### Step 0: Gather Context

Read the problem or plan being reviewed. Identify:
- What is being decided?
- What is the context and constraint set?
- Did the user explicitly name a lens?
- Is the user asking for a single focused perspective rather than a multi-lens debate?

Before lens selection, read and follow `../shared/prompts/project-context.md` to load an attributed snapshot from the target project's indexed memory.

For PR crisis response or reputation recovery, read and apply `../shared/playbooks/pr-crisis-recovery.md` before forming the lens position. Its gates are mandatory even when research is disabled. Include its evidence ledger and response checks in the focused review.

### Step 1: Select One Lens

Read the bundled lens registry at `../shared/prompts/lens-registry.md`.

**If the user specified a lens:** Use it.

**If no lens was specified:** Apply the authoritative selection contract:

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

Announce the selected lens and why it was chosen.

### Step 2: Run The Lens

Read the selected lens brief from `../shared/lenses/lens-<name>.md`.

When useful, also apply:
- tools from `../shared/prompts/lens-capabilities.md`
- reusable methods from `../shared/prompts/shared-playbooks.md`

Produce the lens position using the lens brief's required output contract.

### Step 3: Output Focused Review

Return a compact single-lens review with:
1. Selected lens and why
2. Lens position block
3. Optional recommended next step if more lenses should be involved

If the user asks to save, export, write, or generate the review as a markdown file:
- Store it under `docs/polylens/reviews/`
- Use the filename format `YYMMDD_slug_rN.md`
- Use a descriptive slug

## Error Handling

- **Problem too vague:** Ask clarifying questions before selecting a lens.
- **Explicit but unknown lens:** Explain that the lens is not in the registry and fall back to automatic selection.
- **Two equally strong lenses:** Use the deterministic tie-break order; do not ask the user unless they explicitly want options.

## Important Rules

- Always read `../shared/prompts/lens-registry.md` before selecting a lens.
- Always read the selected brief under `../shared/lenses/` before producing the review.
- Do not run collision or synthesis for a single-lens review.
- If the user really needs multiple competing perspectives, recommend `polylens` instead of improvising a multi-lens output.
