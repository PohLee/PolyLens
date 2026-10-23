---
{
  "validation": {
    "contract": false,
    "quality_gate": false,
    "consistency": false,
    "regression": false,
    "baseline_file": null
  }
}
---

## Validation Configuration

Checks are opt-in during reviews. `harness.py validate brief.md` explicitly enables the
standard brief contract check even when these defaults are disabled.

- `contract`: deterministic full/partial brief structure and lens verdict checks.
- `quality_gate`: legacy name for format hints only, not a measure of reasoning quality.
- `consistency`: deterministic verdict-alignment checks, not factual verification.
- `regression`: fail when section/verdict structure or whitespace-normalized content differs from a baseline. Drift is a review signal, not proof that the new recommendation is worse.
- `baseline_file`: path relative to this configuration file. Missing baselines fail.

Example: enable `contract` and `regression`, then set `baseline_file` to
`../docs/polylens/reviews/260401_baseline_r1.md` when this file is in the project harness directory.
Human/model behavior evaluation is separate from these deterministic checks.
