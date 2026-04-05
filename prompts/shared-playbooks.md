# Shared Playbooks

Reusable analysis methods available to all PolyLens lenses and orchestrators.

These are shared capabilities, not separate perspective lenses. Use them when they materially improve judgment, evidence quality, or decision structure.

## Available Playbooks

| Playbook | When to Apply | Detail File |
|---|---|---|
| **Data Analysis** | Explore datasets, summarize patterns, validate data quality, quantify trends | `prompts/playbooks/data-analysis.md` |
| **Financial Statement Analysis** | Evaluate company financial health, compare periods, analyze ratios and cash flow | `prompts/playbooks/financial-statement-analysis.md` |
| **Root Cause Analysis** | Investigate incidents, failures, recurring issues, and systemic causes | `prompts/playbooks/root-cause-analysis.md` |
| **Risk Assessment** | Identify, score, prioritize, and mitigate strategic, operational, financial, or technical risks | `prompts/playbooks/risk-assessment.md` |
| **Crisis Management** | Structure immediate response, command, containment, and recovery during active crises | `prompts/playbooks/crisis-management.md` |
| **PR Crisis Recovery** | Assess reputation damage, shape response posture, and rebuild stakeholder trust | `prompts/playbooks/pr-crisis-recovery.md` |

## Usage Pattern

When a lens or orchestrator applies a playbook:

1. State which playbook is being applied and why.
2. Read the detailed playbook file if the task needs structured guidance.
3. Use only the sections relevant to the decision.
4. Fold findings back into the lens position or final synthesis.

Playbooks are optional accelerators. They should sharpen the analysis, not replace the lens's core perspective.