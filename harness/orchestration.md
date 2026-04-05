---
mode: sequential
instances:
  - name: primary-review
    lenses: []
    reasoning:
      depth: standard
    hooks:
      pre-analysis: []
      review: []
  - name: follow-up-review
    depends_on: primary-review
    lenses: []
    reasoning:
      depth: standard
    condition: null
---

## Orchestration Plan

[Edit this section to define your multi-instance orchestration strategy]

### Execution Modes

- **sequential** — Run instances in order, feed output to next
- **parallel** — Run independent instances concurrently, merge results
- **conditional** — Evaluate conditions, selectively run instances

### Instance Configuration

Each instance specifies:
- `name`: Unique identifier
- `lenses`: Specific lenses to use (empty = auto-select)
- `depends_on`: Name of instance this depends on (null = no dependency)
- `condition`: Condition to evaluate before running (null = always run)
- `reasoning.depth`: analysis depth (surface | standard | deep)
- `hooks`: Hooks to apply for this instance

### Example: Technical → Business Review

```yaml
mode: sequential
instances:
  - name: technical-review
    lenses: [CTO, CISO]
    reasoning:
      depth: deep
  - name: business-impact
    depends_on: technical-review
    lenses: [CEO, CFO, CRO]
    reasoning:
      depth: standard
```
