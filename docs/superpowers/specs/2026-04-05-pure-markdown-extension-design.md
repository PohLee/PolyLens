# Design Spec: PolyLens Pure Markdown Extension (Approach A)

**Date:** 2026-04-05
**Author:** System (brainstorming session)
**Status:** Draft — for comparison with Approach B and C

---

## 1. Overview

This spec extends PolyLens using only markdown — no runtime code, no Python dependencies, no execution engine. Hooks, orchestration, reasoning control, and validation are all expressed as markdown files that the LLM reads and follows as instructions. The LLM itself executes the "pipeline" by following structured prompts.

**Approach:** Pure Markdown Extension. Everything stays as markdown. Orchestrators read hook files, orchestration configs, and validation rules as part of the prompt chain. The LLM is the execution engine.

**Design principles:**
- Zero runtime dependencies — works anywhere PolyLens works today
- Markdown is both config AND execution — LLM reads and follows instructions
- Backward compatible — no changes to existing files
- Simple to understand — no Python, no YAML, no APIs

---

## 2. Architecture

```
User Problem
    ↓
[Hook: Pre-Analysis]          ← Markdown file content injected into prompt
    ↓
Orchestrator reads:           ← All config is markdown, read by LLM
  - hooks/pre-analysis/*.md
  - harness/orchestration.md
  - harness/reasoning.md
    ↓
┌─────────────────────────────────────────┐
│  LLM executes the pipeline by following │
│  the combined prompt instructions        │
│                                          │
│  1. Read hooks → apply at each stage     │
│  2. Read orchestration → chain analyses  │
│  3. Read reasoning → control depth       │
│  4. Read validation → self-check output  │
└─────────────────────────────────────────┘
    ↓
Decision Brief + Validation Report
```

**Key insight:** The LLM is the runtime. It reads all markdown files, understands the pipeline structure, and executes it step by step within a single conversation turn (or multiple turns for complex orchestration).

**New directories:**
- `hooks/` — Hook definitions (markdown files)
- `harness/` — Harness configurations (markdown files)

**Existing directories:**
- All unchanged — orchestrators are extended to read hook/harness files as part of their prompt chain

---

## 3. Hook System

### 3.1 Hook Stages

Same six stages as Approach B, defined purely in markdown:

| Stage | When it fires | Purpose |
|-------|---------------|---------|
| `pre-analysis` | Before any analysis begins | Inject context, load constraints |
| `lens-select` | During lens selection | Force lenses, override scoring |
| `review` | During individual lens reviews | Inject frameworks, custom logic |
| `collision` | During conflict detection | Adjust conflict weights |
| `synthesis` | During brief synthesis | Override output format |
| `post-analysis` | After all analysis complete | Summarize, transform output |

### 3.2 Hook File Structure

```markdown
---
hook: pre-analysis
name: inject-context
order: 1
enabled: true
---

## Purpose
Inject project-specific context before PolyLens analysis begins.

## Instructions for the LLM
When executing this hook, you MUST:

1. Read the project context below
2. Incorporate this context into ALL subsequent lens analyses
3. Reference these constraints when making recommendations

## Project Context
This is a startup decision for a SaaS company.
- Current MRR: $50K
- Team: 8 engineers, 2 designers
- Runway: 14 months
- Target market: SMB project management
```

**Key difference from Approach B:** No `type: markdown | script` field. Everything is markdown. The LLM reads the "Instructions for the LLM" section and follows it.

### 3.3 Hook Discovery

The orchestrator is updated to:

1. Check for `hooks/` directory
2. If present, read all enabled hook files
3. Inject hook content into the prompt at the appropriate stage
4. Follow hook instructions as part of execution

This is done by adding a section to the orchestrator prompt:

```markdown
## Active Hooks
The following hooks are enabled and must be applied during execution:

### Pre-Analysis Hooks
- inject-context (order: 1) — See hooks/pre-analysis/inject-context.md

### Post-Analysis Hooks
- summarize (order: 1) — See hooks/post-analysis/summarize.md

Apply these hooks at their respective stages. Do not skip any enabled hook.
```

### 3.4 Inline Hooks

Users can define hooks directly in their prompt:

```
Run polylens review on our migration plan with these hooks:

PRE-ANALYSIS: This is a startup decision for a SaaS company. Current MRR: $50K.
POST-ANALYSIS: Generate a one-paragraph executive summary.
```

---

## 4. Framework Harness

### 4.1 Orchestration Configuration

Defined in `harness/orchestration.md`:

```markdown
---
mode: sequential
---

## Orchestration Plan

Execute the following PolyLens analyses in sequence:

### Instance 1: Technical Review
- Lenses: CTO, CISO
- Depth: deep
- Constraints: Must use existing AWS infrastructure, Timeline: 6 weeks
- Apply hooks: inject-context (pre-analysis), add-framework (review)

### Instance 2: Business Impact
- Depends on: Technical Review
- Lenses: CEO, CFO, CRO
- Depth: standard
- Input: Use the technical review's risk register as primary input

### Instance 3: Security Deep-Dive (Conditional)
- Depends on: Technical Review
- Condition: If the technical review identifies any HIGH or CRITICAL security risks
- Lenses: CISO
- Depth: deep

## Execution Instructions for the LLM

1. Execute Instance 1 first. Produce a full decision brief.
2. Use Instance 1's output as input for Instance 2.
3. Evaluate the condition for Instance 3. If met, execute it.
4. Merge all outputs into a unified decision brief.
5. Apply post-analysis hooks.
6. Run validation checks.
```

### 4.2 Execution Modes

**Sequential:** LLM executes instances one after another within the conversation. Each instance's output becomes context for the next.

**Parallel:** Not natively supported. The LLM simulates parallel execution by reasoning about each instance independently, then merging results. This is less reliable than true parallelism but works within a single conversation.

**Conditional:** LLM evaluates conditions against previous output and decides whether to execute subsequent instances.

### 4.3 Output Merging

The LLM merges outputs by following instructions in the orchestration file:

```markdown
## Merge Instructions

Combine all instance outputs as follows:
1. List all verdicts from all instances
2. Identify conflicts across instances
3. Produce a unified risk register (deduplicate, keep highest severity)
4. Generate a combined executive summary
```

---

## 5. Reasoning Control

### 5.1 Configuration

Defined in `harness/reasoning.md`:

```markdown
---
reasoning:
  depth: standard
  min_lenses: 2
  max_lenses: 4
---

## Reasoning Controls

### Depth: Standard
Follow the standard PolyLens analysis process:
- Select 2-4 lenses based on relevance
- Apply default analytical frameworks
- Include web research if available

### Constraints (MUST be respected)
- Budget: under $50K
- Timeline: Q2 2026
- Team size: 3 engineers

### Output Format: Full
Include all 5 sections of the decision brief:
1. Individual Positions
2. Conflict Detection
3. Conflict Mapping
4. Final Alignment
5. Summary Dashboard
```

### 5.2 Depth Levels

| Level | Instructions to LLM |
|-------|---------------------|
| `surface` | "Perform a quick scan. Select minimum lenses. Do not research. Produce a brief response." |
| `standard` | "Follow the standard PolyLens process. Select relevant lenses. Apply default frameworks." |
| `deep` | "Perform thorough analysis. Use web research if available. Analyze git history. Apply extended frameworks. Produce a detailed response." |

### 5.3 Constraint Injection

Constraints are included in the orchestrator prompt as a dedicated section that all lenses must respect. The LLM is instructed to reference constraints in every analysis.

---

## 6. Validation Harness

### 6.1 Configuration

Defined in `harness/validation.md`:

```markdown
---
validation:
  contract: true
  quality_gate: true
  consistency: true
  regression: false
---

## Validation Instructions for the LLM

Before producing your final output, perform the following self-checks:

### Contract Check
Verify your output includes:
- [ ] All 5 decision brief sections
- [ ] GO/MODIFY/BLOCK verdicts for each lens
- [ ] Conflict detection and classification
- [ ] Final decision with risk register

### Quality Gate
Score your analysis from 1-10:
- Are claims supported by evidence?
- Are recommendations actionable?
- Are tradeoffs explicitly stated?
- If score < 7, expand your analysis.

### Consistency Check
Review your output for:
- Contradictory facts between lenses
- Mismatched assumptions
- Inconsistent timelines or budgets
- List any inconsistencies found
```

### 6.2 Validation Output

The LLM appends a self-validation report:

```markdown
VALIDATION REPORT
=================
Contract: PASS — All 5 sections present, verdicts formatted correctly
Quality Gate: 8/10 — Claims supported, recommendations actionable, tradeoffs stated
Consistency: 1 issue found
  - CEO assumes 6-month timeline, CTO assumes 12-month timeline
Regression: N/A (not configured)
```

**Key limitation:** Validation is self-reported by the LLM. There is no automated check. The LLM could miss issues or be overly generous with scores.

---

## 7. Directory Structure

```
polylens/
├── hooks/                              # NEW: Hook definitions (markdown)
│   ├── pre-analysis/
│   │   ├── inject-context.md
│   │   └── load-constraints.md
│   ├── lens-select/
│   │   ├── force-lens.md
│   │   └── custom-scoring.md
│   ├── review/
│   │   ├── add-framework.md
│   │   └── custom-lens.md
│   ├── collision/
│   │   └── weight-conflicts.md
│   ├── synthesis/
│   │   └── custom-template.md
│   └── post-analysis/
│       ├── summarize.md
│       └── webhook-notify.md
├── harness/                            # NEW: Harness configurations (markdown)
│   ├── orchestration.md
│   ├── reasoning.md
│   └── validation.md
├── skills/                             # Unchanged (orchestrators extended)
├── orchestrators/                      # Extended to read hooks/harness
├── lenses/                             # Unchanged
├── engines/                            # Unchanged
├── prompts/                            # Unchanged
├── tools/
│   └── validate_markdown_contracts.py  # Existing (unchanged)
└── docs/                               # Unchanged
```

---

## 8. Orchestrator Extensions

The existing orchestrators are extended to read hook and harness files. No new code is written — only the orchestrator markdown files are updated to include instructions for loading and applying hooks.

**Example addition to `orchestrators/polylens-executive-review.md`:**

```markdown
## Hook Execution

Before proceeding, check for the following files:

1. `hooks/pre-analysis/*.md` — If present, read and apply each enabled hook
2. `harness/orchestration.md` — If present, follow the orchestration plan
3. `harness/reasoning.md` — If present, apply reasoning controls
4. `harness/validation.md` — If present, run self-validation before output

Apply hooks in order. Do not skip any enabled hook.
```

---

## 9. Edge Cases & Limitations

| Scenario | Behavior |
|----------|----------|
| No harness config | Single PolyLens run, backward compatible |
| Hook file missing | LLM skips it, continues |
| Parallel orchestration | LLM simulates parallelism (less reliable than true parallel) |
| Conditional orchestration | LLM evaluates condition, may be inconsistent |
| Validation fails | LLM reports it, does not block delivery |
| Token limit exceeded | LLM truncates output, may lose analysis depth |
| Complex DAG | LLM may struggle with complex dependency graphs |
| Script execution | NOT SUPPORTED — no code execution |

### Key Limitations

1. **No true parallelism** — LLM simulates parallel execution sequentially
2. **No automated validation** — Validation is self-reported by the LLM
3. **No script hooks** — Cannot execute code, only follow markdown instructions
4. **Token limits** — Complex orchestration may exceed context windows
5. **Reliability** — LLM may skip steps or misinterpret instructions under load
6. **No event system** — No pub/sub, no event replay, no audit trail
7. **No plugin SDK** — Custom logic is limited to markdown instructions

---

## 10. Testing Strategy

1. **Manual testing** — Run PolyLens with various hook/harness configs, verify output
2. **Contract validation** — `python3 tools/validate_markdown_contracts.py` must still pass
3. **Prompt testing** — Test orchestrator extensions with different hook combinations
4. **Token limit testing** — Verify complex orchestration fits within context windows

**No automated test suite** — testing is manual and relies on human review of outputs.

---

## 11. Migration Path

**Phase 1: Hook system basics (1-2 days)**
- Create `hooks/` directory structure
- Add hook instructions to orchestrators
- Create example hooks

**Phase 2: Harness configurations (1-2 days)**
- Create `harness/` directory
- Add orchestration, reasoning, validation markdown files
- Update orchestrators to read harness files

**Phase 3: Documentation and examples (1-2 days)**
- Document hook system in README
- Create example configurations
- Update contributing guide

**Total: 4-6 days**

---

## 12. Effort Comparison

| Aspect | Approach A | Approach B | Approach C |
|--------|------------|------------|------------|
| **Dev time** | 4-6 days | 5-8 days | 15-20 days |
| **Architecture change** | Minimal (add markdown) | Small (add files + script) | Major (new package) |
| **Runtime dependency** | None | Small (Python script) | Full Python package |
| **Automation** | None (LLM-driven) | Partial (script-assisted) | Full (engine-driven) |
| **Validation** | Self-reported by LLM | Automated checks | Automated + extensible |
| **Parallelism** | Simulated | True (subprocess) | True (async) |
| **Script hooks** | No | Yes | Yes (full SDK) |
| **Reliability** | Low-Medium | Medium-High | High |
| **Maintenance** | Very Low | Low | Medium-High |
| **User complexity** | Very Low | Low | Medium |

---

## 13. Non-Goals

- Code execution or script hooks
- Automated validation
- True parallel execution
- Event system or pub/sub
- Plugin SDK or programmatic API
- REST API or web interface
- Anything that requires runtime code
