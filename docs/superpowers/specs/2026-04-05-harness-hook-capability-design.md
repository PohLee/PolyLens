# Design Spec: PolyLens Harness Engineering & Hook Capability

**Date:** 2026-04-05
**Author:** System (brainstorming session)
**Status:** Draft — pending user review

---

## 1. Overview

This spec adds two major capability sets to PolyLens:

1. **Hook System** — Pipeline stage hooks and custom plugin hooks that let users inject logic at any point in the PolyLens analysis pipeline
2. **Harness System** — Framework harness for multi-instance orchestration and reasoning control for managing analysis depth, constraints, and output format

**Approach:** Hybrid Markdown + Lightweight Runtime (Approach B). Markdown files serve as both human-readable documentation and machine-readable configuration. A small Python runtime (`tools/harness.py`) handles execution: chaining, conditions, validation, and hook lifecycle management.

**Design principles:**
- Backward compatible — existing PolyLens runs unchanged without harness config
- Markdown-first — hooks, configs, validation rules are `.md` files
- Extends existing patterns — builds on `validate_markdown_contracts.py` infrastructure
- Dual audience — simple markdown hooks for end users, script hooks for developers

---

## 2. Architecture

```
User Problem
    ↓
[Hook: Pre-Analysis]          ← Custom logic before analysis starts
    ↓
Harness Router                ← Decides single vs multi-instance, chaining mode
    ↓
┌─────────────────────────────────────────┐
│  PolyLens Instance A                     │
│    ↓                                    │
│  Lens Selection → [Hook: Lens Select]   │
│    ↓                                    │
│  Individual Reviews → [Hook: Review]    │
│    ↓                                    │
│  Collision → [Hook: Collision]          │
│    ↓                                    │
│  Synthesis → [Hook: Synthesis]          │
│    ↓                                    │
│  Decision Brief                         │
└─────────────────────────────────────────┘
    ↓
[Harness Orchestrator]                    ← Conditional routing, parallel merge
    ↓
┌─────────────────────────────────────────┐
│  PolyLens Instance B (if needed)        │
│  (same hook pipeline)                   │
└─────────────────────────────────────────┘
    ↓
[Hook: Post-Analysis]         ← Custom logic after all analysis complete
    ↓
[Validation Harness]          ← Contract check, quality gate, consistency
    ↓
Final Output
```

**New directories:**
- `hooks/` — Hook definitions (markdown files, dual-purpose: docs + config)
- `harness/` — Harness configurations (orchestration patterns, reasoning controls)
- `tools/harness.py` — Python execution engine

**Existing directories unchanged:**
- `skills/`, `orchestrators/`, `lenses/`, `engines/`, `prompts/` — no structural changes

---

## 3. Hook System

### 3.1 Hook Stages

Six hook points in the PolyLens pipeline:

| Stage | When it fires | Purpose |
|-------|---------------|---------|
| `pre-analysis` | Before any analysis begins | Inject context, load constraints, modify input |
| `lens-select` | During lens selection | Force lenses, override scoring, add custom selection logic |
| `review` | During individual lens reviews | Inject frameworks, add custom lens logic, modify review prompts |
| `collision` | During conflict detection | Adjust conflict weights, add custom conflict rules |
| `synthesis` | During brief synthesis | Override output format, add custom sections |
| `post-analysis` | After all analysis complete | Summarize, notify external systems, transform output |

### 3.2 Hook File Structure

Hooks live under `hooks/<stage>/<name>.md` with YAML frontmatter:

```markdown
---
hook: pre-analysis
name: inject-context
order: 1
enabled: true
type: markdown
---

## Purpose
Inject project-specific context before PolyLens analysis begins.

## Hook Content
[Markdown content injected into the orchestrator prompt at this stage]
```

**Frontmatter fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `hook` | string | Yes | Stage name (pre-analysis, lens-select, review, collision, synthesis, post-analysis) |
| `name` | string | Yes | Unique hook identifier |
| `order` | int | Yes | Execution order within stage (lower = earlier) |
| `enabled` | bool | Yes | Whether hook is active |
| `type` | string | Yes | `markdown` or `script` |
| `script` | string | Conditional | Path to script (required when type=script) |

### 3.3 Markdown Hooks

Content is injected into the orchestrator's prompt chain at the appropriate stage. The orchestrator reads the hook file and appends its content to the prompt before executing that stage.

**Example — pre-analysis hook:**
```markdown
---
hook: pre-analysis
name: inject-context
order: 1
enabled: true
type: markdown
---

## Project Context
This is a startup decision for a SaaS company.
- Current MRR: $50K
- Team: 8 engineers, 2 designers
- Runway: 14 months
- Target market: SMB project management

Apply this context to all lens analyses.
```

### 3.4 Script Hooks

For developers who need executable logic. The Python runtime executes the script, passing relevant context as stdin and capturing stdout.

**Example — post-analysis hook:**
```markdown
---
hook: post-analysis
name: webhook-notify
order: 1
enabled: false
type: script
script: scripts/webhook_notify.py
---

## Purpose
Send analysis results to external webhook.

## Script Interface
- Input: JSON of full decision brief via stdin
- Output: None (side effect: HTTP POST)
```

**Script hook interface:**
- **stdin:** JSON object containing the current pipeline state (input problem, lens selections, decision brief, validation results)
- **stdout:** JSON object with modifications to pipeline state (for hooks that transform output)
- **exit code:** 0 = success, non-zero = hook failure (logged, does not block pipeline)

### 3.5 Inline Hooks

Users can define hooks directly in `.polylensrc` or in their prompt:

```yaml
hooks:
  pre-analysis: |
    This is a startup decision for a SaaS company...
  post-analysis:
    script: ./my-custom-handler.py
```

Inline hooks override file-based hooks of the same stage when both exist.

### 3.6 Hook Registry

The Python runtime builds a hook registry at startup:

1. Scan `hooks/` directory for `.md` files
2. Parse frontmatter from each file
3. Group by stage, sort by order
4. Filter by `enabled: true`
5. Merge with inline hooks (inline takes precedence)
6. Execute in order at each stage

---

## 4. Framework Harness

### 4.1 Orchestration Configuration

Defined in `harness/orchestration.md`:

```markdown
---
mode: sequential
instances:
  - name: technical-review
    lenses: [CTO, CISO]
    reasoning:
      depth: deep
      constraints:
        - "Must use existing AWS infrastructure"
        - "Timeline: 6 weeks"
    hooks:
      pre-analysis: [inject-context]
      review: [add-framework]
  - name: business-impact
    depends_on: technical-review
    lenses: [CEO, CFO, CRO]
    reasoning:
      depth: standard
    input_transform: |
      Use the technical review's risk register as primary input
  - name: security-deep-dive
    depends_on: technical-review
    condition: "risk_register.severity >= HIGH"
    lenses: [CISO]
    reasoning:
      depth: deep
---

## Orchestration Plan
[Human-readable description of the orchestration strategy]
```

### 4.2 Execution Modes

**Sequential mode:**
- Run instances in order
- Each instance can depend on previous instance output
- `input_transform` field defines how to transform previous output into next input
- Final output = last instance's brief

**Parallel mode:**
- Run all instances without `depends_on` simultaneously (via subprocess)
- Instances with `depends_on` run after their dependencies complete
- Merge all briefs into unified decision dashboard
- Merge strategy: combine verdicts, deduplicate conflicts, unified risk register

**Conditional mode:**
- Evaluate `condition` field against previous instance output
- Condition syntax: dot-notation path comparison (e.g., `risk_register.severity >= HIGH`)
- Skipped instances are noted in final output but do not block execution

### 4.3 Harness Router

The harness router is the entry point that decides execution path:

1. Check for `harness/orchestration.md`
2. If absent → single PolyLens run (backward compatible)
3. If present → parse orchestration config
4. Execute instances per mode
5. Merge results
6. Run post-analysis hooks
7. Run validation harness
8. Return final output

### 4.4 Output Merging

| Mode | Strategy |
|------|----------|
| Sequential | Last instance brief becomes final output |
| Parallel | Merge all briefs: combine verdicts, deduplicate conflicts, unified risk register, combined dashboard |
| Conditional | Include only executed instances in final output |

---

## 5. Reasoning Control

### 5.1 Configuration

Defined in `harness/reasoning.md` or inline:

```markdown
---
reasoning:
  depth: standard
  min_lenses: 2
  max_lenses: 4
  constraints:
    - "Budget: under $50K"
    - "Timeline: Q2 2026"
    - "Team size: 3 engineers"
  output:
    format: full
    include_sections: [all]
    custom_template: null
---
```

### 5.2 Depth Levels

| Level | Behavior |
|-------|----------|
| `surface` | Fast scan, minimum lenses, no web research, no git analysis |
| `standard` | Current PolyLens behavior (default) |
| `deep` | Extended research, web searches, git log/diff analysis, deeper analytical frameworks, extended playbooks |

### 5.3 Constraint Injection

Constraints are prepended to the orchestrator prompt so all lenses must respect them. Format:

```
## Constraints (must be respected in all analyses)
- Budget: under $50K
- Timeline: Q2 2026
- Team size: 3 engineers
```

### 5.4 Output Format Control

| Setting | Values | Description |
|---------|--------|-------------|
| `format` | `full`, `concise`, `dashboard-only` | Output verbosity |
| `include_sections` | `[all]` or list of section names | Which brief sections to include |
| `custom_template` | `null` or path to template file | Override output template |

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
  baseline_file: null
---
```

### 6.2 Validation Checks

| Check | What it validates | Action on failure |
|-------|-------------------|-------------------|
| **Contract** | Required sections present, verdict format (GO/MODIFY/BLOCK), 5-section structure | Flag in output, suggest fixes |
| **Quality gate** | Minimum analysis depth, supported claims, reasoning completeness | Score 0-10, warn if below threshold |
| **Consistency** | Contradictory facts between lenses, mismatched assumptions | List contradictions for user review |
| **Regression** | Output drift vs. baseline (section count, verdict changes, risk count delta) | Report delta, no blocking |

### 6.3 Validation Output

Appended to the decision brief as a "Validation Report" section:

```markdown
VALIDATION REPORT
=================
Contract: PASS
Quality Gate: 8/10
Consistency: 1 issue found
  - CEO assumes 6-month timeline, CTO assumes 12-month timeline
Regression: N/A (no baseline configured)
```

Validation is **always advisory** — never blocks delivery.

---

## 7. Directory Structure

```
polylens/
├── hooks/                              # NEW: Hook definitions
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
├── harness/                            # NEW: Harness configurations
│   ├── orchestration.md
│   ├── reasoning.md
│   └── validation.md
├── tools/
│   ├── validate_markdown_contracts.py  # Existing
│   └── harness.py                      # NEW: Execution engine
├── skills/                             # Unchanged
├── orchestrators/                      # Unchanged
├── lenses/                             # Unchanged
├── engines/                            # Unchanged
├── prompts/                            # Unchanged
└── docs/                               # Unchanged
```

---

## 8. Python Runtime: `tools/harness.py`

### 8.1 Responsibilities

1. **Hook registry management** — Scan, parse, merge, and execute hooks
2. **Orchestration execution** — Run sequential/parallel/conditional PolyLens instances
3. **Reasoning control** — Apply depth, constraints, output format settings
4. **Validation** — Run contract, quality, consistency, and regression checks
5. **Backward compatibility** — No-op when no harness config exists

### 8.2 Command Interface

```bash
# Run with harness (auto-detects config)
python3 tools/harness.py run "Your problem here"

# Run with specific orchestration
python3 tools/harness.py run --orchestration harness/orchestration.md "Your problem"

# Run validation only on existing brief
python3 tools/harness.py validate docs/polylens/reviews/260405_migration_r1.md

# List available hooks
python3 tools/harness.py hooks list

# Enable/disable a hook
python3 tools/harness.py hooks enable pre-analysis/inject-context
python3 tools/harness.py hooks disable pre-analysis/inject-context
```

### 8.3 Integration with Existing Skills

The harness runtime does NOT replace existing skills. Instead:

1. Hooks are injected into the orchestrator prompt chain before the LLM processes it
2. The existing `polylens` skill remains the entry point
3. When harness config exists, the skill delegates to `harness.py` for execution
4. When no harness config exists, the skill runs as before

---

## 9. Edge Cases & Error Handling

| Scenario | Behavior |
|----------|----------|
| No harness config | Single PolyLens run, backward compatible |
| Hook file missing | Log warning, skip hook, continue |
| Script hook fails | Log error, skip hook, continue (does not block pipeline) |
| Circular dependency in orchestration | Detect and error before execution |
| Condition evaluation fails | Log warning, skip conditional instance, continue |
| Validation fails | Report in output, do not block delivery |
| Parallel instance fails | Log error, continue with remaining instances, note in output |
| Depth=deep but no web access | Fall back to standard depth, log warning |

---

## 10. Testing Strategy

1. **Unit tests** — Hook parsing, registry building, condition evaluation, config validation
2. **Integration tests** — Full pipeline run with hooks, orchestration modes, validation checks
3. **Contract tests** — Ensure hook frontmatter schema is valid, orchestration config is well-formed
4. **Regression tests** — Compare output format against baseline briefs
5. **Existing validation** — `python3 tools/validate_markdown_contracts.py` must still pass

---

## 11. Migration Path

**Phase 1:** Hook system + Python runtime basics
- Hook registry, markdown hooks, script hook execution
- `tools/harness.py` with `run`, `hooks list`, `hooks enable/disable`

**Phase 2:** Framework harness
- Orchestration config parsing
- Sequential execution mode
- Reasoning control (depth, constraints)

**Phase 3:** Advanced orchestration + validation
- Parallel and conditional modes
- Validation harness (contract, quality, consistency)
- Regression testing support

**Phase 4:** Polish
- Inline hooks support
- Output format control
- Documentation and examples

---

## 12. Non-Goals

- Replacing existing PolyLens skills or orchestrators
- Real-time streaming or interactive hook debugging
- GUI for hook management
- Hook versioning or rollback
- Multi-language script support (Python only for v1)
