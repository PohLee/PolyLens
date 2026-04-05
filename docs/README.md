# PolyLens

**Multi-perspective reasoning for high-stakes decisions**

PolyLens is an agentic decision system that simulates executive-level thinking to analyze problems, surface disagreements, and resolve them into clear, actionable decisions. It is implemented as a collection of OpenCode-compatible skills — no code dependencies, pure markdown.

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/your-org/polylens.git
cd polylens

# Symlink skills into your OpenCode skills directory
ln -s "$(pwd)/skills" ~/.config/opencode/skills/polylens
```

That's it. Every lens and orchestrator is now available as a skill.

The installable `skills/` tree is self-contained. Runtime references stay inside that tree by using sibling-relative paths such as `../shared/prompts/...` and `../shared/engines/...`, so PolyLens can review another repository without extra directory permissions.

---

## Usage

### Mode 1: Executive Review (Full Multi-Lens)

Invoke the `polylens-executive-review` skill. The orchestrator automatically selects 2-4 relevant lenses based on your problem context, runs collision detection, and produces a structured decision brief.

**Triggers:** "run executive review", "polylens review", "multi-lens review", "analyze from multiple perspectives"

```
Run executive review on our plan to migrate from PostgreSQL to MongoDB
```

### Mode 2: Individual Lens Review

Invoke any lens skill directly for a focused, single-perspective analysis.

**Available lenses:**

| Skill | Focus | Triggers |
|---|---|---|
| `lens-ceo` | Business & Strategy | pricing strategy, go-to-market, roadmap, growth metrics |
| `lens-cto` | Technical & Infrastructure | tech stack, API design, scalability, technical debt |
| `lens-cpo` | Product & User Experience | user experience, feature prioritization, retention, usability |
| `lens-yc` | Startup & Fundability | pitch deck, fundraising, MVP scope, unit economics |
| `lens-cio` | Information & Operations | workflow automation, internal tools, process redesign |
| `lens-cdo` | Data & Analytics | data pipeline, analytics dashboard, ML model, metrics |
| `lens-ciso` | Security & Compliance | authentication, GDPR, SOC2, vulnerability assessment |
| `lens-cxo` | Customer Experience | customer journey, NPS, support flow, churn reduction |
| `lens-cco` | Communication & Culture | team alignment, documentation, developer experience |

```
Run CTO review on our new API design
```

### Mode 3: Pre-Fight (Adversarial Critique)

Invoke the `polylens-pre-fight` skill for structured conflict between lenses. Lenses critique each other's positions, defend their own, and then either escalate the strongest disagreements or finish automatically with deterministic arbitration.

**Triggers:** "pre-fight review", "adversarial review", "critique from all angles", "stress-test this decision", "debate", "fully automatic pre-fight", "auto-resolve disagreements", "without user input"

```
Run pre-fight review on our pricing strategy
Run fully automatic pre-fight review on our pricing strategy
```

Normal pre-fight mode remains interactive and stops when a fundamental disagreement needs user direction. Add wording such as "fully automatic", "decide for me", or "without user input" to force automatic arbitration and a completed recommendation.

---

## Available Skills

### Orchestrators (2)

| Skill | Purpose |
|---|---|
| `polylens-executive-review` | Full multi-lens review with automatic lens selection, collision detection, and synthesis |
| `polylens-pre-fight` | Adversarial critique mode — lenses attack and defend positions |

### Lenses (9 Active)

| Skill | Focus | Default | Key Triggers |
|---|---|---|---|
| `lens-ceo` | Speed, growth, market direction | Yes | pricing strategy, go-to-market, roadmap |
| `lens-cto` | Scalability, risk, system integrity | Yes | tech stack, API design, scalability |
| `lens-cpo` | User value, UX, retention | Yes | user experience, feature prioritization |
| `lens-yc` | Clarity, fundability, simplicity | No | pitch deck, fundraising, MVP scope |
| `lens-cio` | Operational efficiency, internal systems | No | workflow automation, internal tools |
| `lens-cdo` | Data strategy, analytics, metrics | No | data pipeline, analytics, ML model |
| `lens-ciso` | Security posture, compliance, risk | No | authentication, GDPR, security audit |
| `lens-cxo` | Customer satisfaction, journey | No | customer journey, NPS, churn reduction |
| `lens-cco` | Team alignment, documentation | No | team alignment, developer experience |

### Planned (Not Yet Active)

| Lens | Focus |
|---|---|
| COO | Operational scaling, supply chain, process optimization |
| CFO | Financial sustainability, budget, profitability |

---

## Architecture

```
polylens/
├── skills/                          # Skill definitions (invocable by OpenCode)
│   ├── polylens-executive-review.md # Orchestrator: full review pipeline
│   ├── polylens-pre-fight.md        # Orchestrator: adversarial critique
│   ├── shared/                      # Bundled runtime docs used by installed skills
│   │   ├── prompts/
│   │   └── engines/
│   ├── lens-ceo.md                  # Business & Strategy
│   ├── lens-cto.md                  # Technical & Infrastructure
│   ├── lens-cpo.md                  # Product & User Experience
│   ├── lens-yc.md                   # Startup & Fundability
│   ├── lens-cio.md                  # Information & Operations
│   ├── lens-cdo.md                  # Data & Analytics
│   ├── lens-ciso.md                 # Security & Compliance
│   ├── lens-cxo.md                  # Customer Experience
│   └── lens-cco.md                  # Communication & Culture
├── engines/                         # Shared processing logic
│   ├── collision.md                 # Conflict detection & classification
│   └── synthesis.md                 # Resolution strategies & output assembly
├── prompts/                         # Centralized data & templates
│   ├── lens-registry.md             # Lens metadata (domains, triggers, pairs)
│   ├── conflict-types.md            # 5 conflict type definitions
│   ├── lens-capabilities.md         # Shared toolset & frameworks
│   └── output-template.md           # 5-section decision brief format
└── docs/
    └── README.md                    # This file
```

The root `prompts/` and `engines/` directories remain the source docs for development. Their runtime copies live under `skills/shared/` so installed agents only need access to the symlinked `skills/` tree.

### Three-Layer Design

| Layer | Purpose | Files |
|---|---|---|
| **Skills** | Individual lens prompts + orchestrators | `skills/*.md` |
| **Engines** | Shared collision detection and synthesis | `engines/*.md` |
| **Prompts** | Lens registry, conflict taxonomy, templates | `prompts/*.md` |

---

## How It Works

```
Input Problem
    ↓
Smart Lens Selection (2-4 lenses from registry)
    ↓
Individual Lens Reviews (sequential, with optional tool use)
    ↓
Collision Engine (detect & classify conflicts)
    ↓
Synthesis Engine (resolve tradeoffs, assemble brief)
    ↓
Decision Brief (5-section structured output)
```

### Smart Lens Selection

The orchestrator does not run all lenses. It selects the 2-4 most relevant lenses using this algorithm:

1. **Filter active lenses** — only lenses with `active: true` are considered
2. **Find the decision anchor** — identify the primary decision being asked, separate from supporting constraints
3. **Keyword match** — scan problem against each lens's `domains` and `triggers`
4. **Downweight ambient constraints** — budget, timeline, team size, compliance, or risk details are supporting signals unless explicitly decision-driving
5. **Score & rank** — count matches, but prefer lenses that match the anchor decision over lenses that only match surrounding constraints
6. **Pairing boost** — if a top lens has `pairs_with` recommendations, boost those lenses by +0.5
7. **Add strategy complement when needed** — if the decision is foundational and company-shaping, include the nearest strategy lens even when the wording is technical
8. **Select top 2-4** — cover the anchor decision first, then only the strongest secondary tradeoffs
9. **Fallback** — if no strong matches (all scores < 2), use default trio: CEO + CTO + CPO

Example: for a question about "tech stack," CTO should be selected first and CEO should usually be included as the strategic counterpart. Add CISO only when security/compliance is itself part of the decision. Add CFO only when spend, runway, or ROI is being explicitly optimized.

User-specified lenses always override automatic selection.

---

## Lens Capabilities

Every lens has access to the same shared toolset and analytical frameworks:

### Available Tools

- **Web research** — Market data, competitor analysis, industry trends
- **Git operations** — `git log`, `git diff`, `git blame` for codebase context
- **File system access** — Read project files, configuration, documentation
- **Code analysis** — Read source code, trace dependencies, understand architecture
- **Shell commands** — Run tests, builds, linting, metrics

### Analytical Frameworks

| Framework | Use Case |
|---|---|
| SWOT Analysis | Strategic decisions, market positioning |
| Porter's Five Forces | Competitive analysis, market entry |
| Jobs-to-be-Done | Product/feature decisions |
| RICE Prioritization | Feature prioritization, roadmap |
| Kano Model | Feature classification |
| Cost of Delay | Timeline/priority decisions |
| Technical Debt Quadrant | Architecture decisions |
| DORA Metrics | Engineering velocity assessment |

---

## Adding New Lenses

PolyLens is designed for extensibility. Adding a new lens requires only two changes:

### Step 1: Create the Lens Skill

Create `skills/lens-<name>.md` following the existing lens template:

```markdown
---
name: lens-<name>
version: 1
description: Use when... Triggers: ...
---

# <Role> Lens

**Role:** <One-line description>

## Philosophy
<Your lens's core philosophy>

## Prime Directives
1. ...
2. ...

## Cognitive Patterns
- ...

## Priority Hierarchy Under Pressure
1. ...
2. ...

## Review Process
### Step 1: Understand the Decision
### Step 1.5: Research (Optional)
### Step 2: Apply <Role> Lens
### Step 3: Produce Position
### Step 4: Provide Reasoning

## Verdict Guidance
- **GO:** ...
- **MODIFY:** ...
- **BLOCK:** ...
```

### Step 2: Register the Lens

Add an entry to `prompts/lens-registry.md`:

```markdown
### <NAME> — <Short Description>

- **focus:** One-line description
- **domains:** comma, separated, areas
- **triggers:** keyword, phrases, that, activate
- **pairs_with:** ComplementaryLens, OtherLens
- **default:** false
- **active:** true
- **bias:** priority > alternative
- **verdict_style:** GO if ..., MODIFY if ..., BLOCK if ...
```

That's it. No changes to orchestrators or engines are needed. The selection algorithm picks up new lenses automatically.

---

## Output Format

Every executive review produces a 5-section decision brief:

1. **Individual Lens Positions** — GO/MODIFY/BLOCK verdicts with concerns, endorsements, and non-negotiables
2. **Conflict Detection Summary** — Verdict alignment and conflict classification across 5 dimensions
3. **Detailed Conflict Mapping** — Stacked comparison of each lens's position per dimension
4. **Final Alignment After Resolution** — Changes to plan, unanimous agreements, deferred decisions, assumptions, and risk register
5. **Final Summary Dashboard** — Compact executive summary with decision, tradeoffs, risks, mitigations, and confidence level

Presentation rule: keep the final brief narrow and readable. Prefer headings, labeled lines, and bullets instead of ASCII borders or wide markdown tables.

Conflicts are classified into 5 types: Priority, Scope, Risk, Resource, and Fundamental. Types 1-4 are auto-resolved; Type 5 is escalated to the user.

---

## Contributing

Contributions are welcome in these areas:

- **New lenses** — Add perspectives we haven't covered (COO, CFO, and more)
- **Improved frameworks** — Better analytical frameworks for lenses to use
- **Conflict resolution models** — New strategies for resolving disagreements
- **Engine improvements** — Better collision detection or synthesis logic
- **Documentation** — Clearer examples, better explanations

To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test by invoking the skill in OpenCode
5. Submit a pull request

---

## License

MIT License

Copyright (c) 2026 PolyLens Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
