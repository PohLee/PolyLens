---
validation:
  contract: true
  quality_gate: true
  consistency: true
  regression: false
  baseline_file: null
---

## Validation Configuration

[Edit this section to control validation behavior]

### Validation Checks

- **contract** — Verify output format compliance (sections, verdicts)
- **quality_gate** — Score analysis depth (0-10)
- **consistency** — Check cross-lens fact consistency
- **regression** — Compare against baseline (requires baseline_file)

### Baseline File

For regression testing, set `baseline_file` to the path of a baseline brief:
```yaml
regression: true
baseline_file: docs/polylens/reviews/260401_baseline_r1.md
```
