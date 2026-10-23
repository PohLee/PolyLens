---
name: polylens
description: Use as the main PolyLens entrypoint for multi-lens analysis. Triggers: polylens review, executive review, multi-lens review, analyze from multiple perspectives, pre-fight review, adversarial review, stress-test this decision, critique from all angles, fully automatic pre-fight, auto-resolve disagreements. Routes to the standard executive review flow or the pre-fight flow based on user intent.
---

# PolyLens Router

You are the top-level PolyLens router. Your job is to choose the correct multi-lens review mode and then hand off to the matching internal orchestrator.

## Routing Rules

### Step 1: Classify The Request

Read the user's request and decide whether it is asking for:

- **Standard review mode** — normal multi-lens analysis, decision brief, synthesis, executive review, or general PolyLens review
- **Pre-fight mode** — adversarial review, critique, debate, stress-test, strongest disagreements, or fully automatic conflict arbitration

Default to **standard review mode** unless the user clearly asks for adversarial or pre-fight behavior.

### Step 2: Route To The Internal Orchestrator

- For **standard review mode**, read and follow `../shared/orchestrators/polylens-executive-review.md`
- For **pre-fight mode**, read and follow `../shared/orchestrators/polylens-pre-fight.md`

Announce which mode was selected and why.

### Step 2.5: Check for Harness Configuration

Harness is optional and applies to **standard review mode** only. Pre-fight keeps its own
embedded execution flow; do not switch modes to apply Harness. If a user requests an
incompatible multi-instance Harness flow in pre-fight, explain that limitation explicitly.

For standard mode, activate Harness when the user requests deep/surface analysis, validation,
inline hooks, multi-instance orchestration, or reusable non-default configuration:

1. Check if `../shared/harness/orchestration.md` exists and has instances configured
2. Check if `../shared/harness/reasoning.md` exists with non-default settings
3. Check if `../shared/harness/validation.md` exists with any validation check enabled
4. Check if `../shared/hooks/` directory has any enabled hooks

If active and Python is available, invoke `../shared/tools/harness.py run` with the problem as
one safely passed argument and `--json` to obtain the plan. Resolve tool/config paths from this
skill's base directory, not the target project's working directory. Translate explicit user
depth requests to `--depth`; apply inline hooks/constraints as per-request overrides without
changing installed files. The CLI generates configuration, not a model invocation.

If Python is unavailable, follow the same JSON configuration and Markdown hooks directly,
report that deterministic CLI validation was not run, and continue the core Markdown review.
Shipped configurations and example hooks are inactive by default. Their presence alone does
not activate Harness. User tool restrictions remain in force; script hooks require explicit
authorization and are never executed by the Python plan generator.

If NONE are active, proceed to Step 3 with the standard flow.

### Step 3: Execute The Chosen Flow

Run the selected internal orchestrator exactly as written.

## Important Rules

- Always decide the mode before doing any lens selection.
- Do not improvise a hybrid between standard review and pre-fight.
- If the user wants a single focused perspective rather than a multi-lens review, recommend `polylens-lens-review` instead.
- Preserve all save/export behavior defined by the chosen internal orchestrator.
- When harness is active, follow the harness execution flow from the orchestrator.
