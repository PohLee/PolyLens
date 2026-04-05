# Lens Capabilities

Shared toolset and analytical frameworks available to all PolyLens lenses.

Any lens can use any tool when it would strengthen their analysis. Tools are not assigned per-lens — the full set is available to every lens.

## 1. Available Tools

All lenses have access to:

- **Web research (browser)** — Search for market data, competitor analysis, industry trends, best practices, user research
- **Git operations** — `git log`, `git diff`, `git blame`, `git show` to understand codebase history, recent changes, authorship patterns
- **File system access** — Read project files, configuration, documentation, test files, architecture docs
- **Code analysis** — Read source code, trace dependencies, understand architecture patterns
- **Shell commands** — Run project-specific commands (tests, builds, linting, metrics)
- **Strategic frameworks** — SWOT analysis, Porter's Five Forces, Jobs-to-be-Done, RICE prioritization, Kano model

## 2. Shared Playbooks

All lenses may also apply these reusable methods when they materially improve the analysis:

- **Data analysis** — Explore datasets, validate quality, quantify trends, and summarize evidence
- **Financial statement analysis** — Assess profitability, liquidity, solvency, efficiency, and cash generation
- **Root cause analysis** — Trace incidents and recurring problems to their underlying systemic causes
- **Risk assessment** — Identify, score, prioritize, and mitigate meaningful risks before commitment
- **Crisis management** — Structure command, containment, continuity, and recovery during active crises
- **PR crisis recovery** — Assess reputational damage, choose response posture, and rebuild trust

Detailed playbooks live under `prompts/playbooks/` and are indexed in `prompts/shared-playbooks.md`.

## 3. When to Use Tools

| Situation | What to Do |
|---|---|
| **Before forming a position** | Research market data, check codebase state, review recent changes |
| **When validating assumptions** | Verify claims with data (e.g., "this framework is popular" → check GitHub stars/npm downloads) |
| **When assessing impact** | Read actual code to understand blast radius, not just the plan description |
| **When benchmarking** | Compare against industry standards or competitor approaches |
| **When data is missing** | Don't guess — research, measure, or read the code |

## 4. Analytical Frameworks Reference

Each lens can apply these frameworks when relevant:

| Framework | When to Use | Output |
|---|---|---|
| SWOT Analysis | Strategic decisions, market positioning | Strengths, Weaknesses, Opportunities, Threats table |
| Porter's Five Forces | Competitive analysis, market entry | Competitive forces assessment |
| Jobs-to-be-Done | Product/feature decisions | User job statements with success criteria |
| RICE Prioritization | Feature prioritization, roadmap decisions | Reach × Impact × Confidence ÷ Effort scores |
| Kano Model | Feature classification | Basic/Performance/Excitement classification |
| Cost of Delay | Timeline/priority decisions | Weekly cost of not shipping |
| Technical Debt Quadrant | Architecture decisions | Deliberate/Inadvertent × Reckless/Prudent classification |
| DORA Metrics | Engineering velocity assessment | Deployment frequency, lead time, MTTR, change failure rate |

## 5. Tool Usage Pattern

When a lens needs to use a tool, it should:

1. **State what it's researching and why**
2. **Use the tool** (browser, git, file read, shell command)
3. **Incorporate findings into its position**
4. **Cite sources** when making claims based on research

### Example

> Before forming my position, I'll check the recent commit history to understand the team's current velocity and any related refactoring work...
