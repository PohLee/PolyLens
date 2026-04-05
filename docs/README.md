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

That's it. PolyLens exposes two public entry skills: `polylens` for multi-lens work and `polylens-lens-review` for focused single-lens work.

The installable `skills/` tree is self-contained. Runtime references stay inside that tree by using sibling-relative paths such as `../shared/prompts/...`, `../shared/engines/...`, `../shared/lenses/...`, and `../shared/orchestrators/...`, so PolyLens can review another repository without extra directory permissions.

---

## Usage

### Mode 1: Standard PolyLens Review (Full Multi-Lens)

Invoke the `polylens` skill. It routes to the standard executive-review orchestrator by default, selects 2-4 relevant lenses based on your problem context, runs collision detection, and produces a structured decision brief.

**Triggers:** "run executive review", "polylens review", "multi-lens review", "analyze from multiple perspectives"

```
Run polylens review on our plan to migrate from PostgreSQL to MongoDB
```

### Mode 2: Focused Lens Review

Invoke the `polylens-lens-review` skill for one routed perspective. It automatically selects the best lens unless you name one.

```
Run lens review on our new API design
Run lens review on our authentication flow and use the CISO lens
```

### Mode 3: PolyLens Pre-Fight (Adversarial Critique)

Invoke the `polylens` skill with adversarial or pre-fight wording. The router sends the request to the internal pre-fight orchestrator, where lenses critique each other's positions, defend their own, and then either escalate the strongest disagreements or finish automatically with deterministic arbitration.

**Triggers:** "pre-fight review", "adversarial review", "critique from all angles", "stress-test this decision", "debate", "fully automatic pre-fight", "auto-resolve disagreements", "without user input"

```
Run polylens pre-fight review on our pricing strategy
Run polylens fully automatic pre-fight review on our pricing strategy
```

Normal pre-fight mode remains interactive and stops when a fundamental disagreement needs user direction. Add wording such as "fully automatic", "decide for me", or "without user input" to force automatic arbitration and a completed recommendation.

## Markdown Artifact Storage

When PolyLens is asked to generate and save a markdown file, store it under `docs/` instead of creating loose `.md` files at the repo root.

- `docs/polylens/reviews/` for executive review briefs
- `docs/polylens/pre-fight/` for pre-fight reports
- `docs/polylens/plans/` for plans and proposals
- `docs/polylens/memory/` for memory notes, working notes, and generic markdown memos when no better category is clear
- `docs/polylens/notes/` for other supporting notes

Filename convention:

- `YYMMDD_slug_rN.md`
- Example: `docs/polylens/memory/260405_selection-logic_r1.md`
- Use a clear, descriptive slug rather than a very short label; prefer names like `selection-logic-routing-fix` over `fix`
- Start at `r1`; increment the revision number when saving another version of the same dated slug

---

## Available Skills

### Public Skills (2)

| Skill | Purpose |
|---|---|
| `polylens` | Top-level multi-lens router that selects standard review or pre-fight mode |
| `polylens-lens-review` | Single-entry focused review that routes to the most relevant lens |

### Routed Lens Library

PolyLens still includes the full lens set, but they now live behind the routers instead of appearing as separate public skills.

### Internal Orchestrators

The multi-lens modes are now internal implementation files rather than user-facing skills:

| Orchestrator | Purpose |
|---|---|
| `polylens-executive-review` | Standard decision brief flow |
| `polylens-pre-fight` | Adversarial critique and arbitration flow |

### Shared Playbooks

These are reusable methods available to every lens and orchestrator. They are not separate perspective skills.

| Playbook | Purpose |
|---|---|
| `data-analysis` | Dataset exploration, statistical summaries, trend analysis, and data-quality checks |
| `financial-statement-analysis` | Ratio analysis, cash flow assessment, and financial health evaluation |
| `root-cause-analysis` | 5 Whys, fishbone thinking, and causal-chain investigation |
| `risk-assessment` | Risk identification, scoring, prioritization, and mitigation planning |
| `crisis-management` | Command structure, containment, continuity, and crisis response planning |
| `pr-crisis-recovery` | Reputation damage assessment, response posture, and trust rebuilding |

---

## Architecture

```
polylens/
├── skills/                          # Skill definitions (invocable by OpenCode)
│   ├── polylens/                    # Top-level multi-lens router
│   ├── polylens-lens-review.md      # Single-entry focused lens router
│   ├── shared/                      # Bundled runtime docs used by installed skills
│   │   ├── prompts/
│   │   ├── engines/
│   │   ├── lenses/
│   │   ├── orchestrators/
│   │   └── playbooks/
├── orchestrators/                   # Internal multi-lens review modes
│   ├── polylens-executive-review.md
│   └── polylens-pre-fight.md
├── lenses/                          # Source lens briefs
│   └── lens-*.md
├── engines/                         # Shared processing logic
│   ├── collision.md                 # Conflict detection & classification
│   └── synthesis.md                 # Resolution strategies & output assembly
├── prompts/                         # Centralized data & templates
│   ├── lens-registry.md             # Lens metadata (domains, triggers, pairs)
│   ├── conflict-types.md            # 5 conflict type definitions
│   ├── lens-capabilities.md         # Shared toolset & frameworks
│   ├── shared-playbooks.md          # Reusable analysis methods index
│   ├── playbooks/                   # Detailed shared playbooks
│   └── output-template.md           # 5-section decision brief format
└── docs/
    └── README.md                    # This file
```

The root `prompts/`, `engines/`, and `lenses/` directories remain the source docs for development. Their runtime copies live under `skills/shared/` so installed agents only need access to the symlinked `skills/` tree.

### Five-Layer Design

| Layer | Purpose | Files |
|---|---|---|
| **Skills** | Public entrypoints only | `skills/polylens*/SKILL.md` |
| **Orchestrators** | Internal multi-lens mode implementations | `orchestrators/*.md`, `skills/shared/orchestrators/*.md` |
| **Lens Library** | Internal perspective briefs selected by routing | `lenses/lens-*.md`, `skills/shared/lenses/lens-*.md` |
| **Engines** | Shared collision detection and synthesis | `engines/*.md` |
| **Prompts** | Lens registry, conflict taxonomy, playbooks, templates | `prompts/*.md`, `prompts/playbooks/*.md` |

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
3. **Check ownership** — if a lens role owns that decision category, it should usually be included before adjacent lenses that only evaluate consequences
4. **Keyword match** — scan problem against each lens's `domains`, `triggers`, and owned decision categories
5. **Downweight ambient constraints** — budget, timeline, team size, compliance, or risk details are supporting signals unless explicitly decision-driving
6. **Apply veto coverage** — if the prompt explicitly touches a veto area, include that lens or explain why it is being deferred
7. **Pairing boost** — if a top lens has `pairs_with` recommendations, boost those lenses by +0.5
8. **Add strategy complement when needed** — if the decision is foundational and company-shaping, include the nearest strategy lens even when the wording is technical
9. **Select top 2-4** — cover the anchor decision first, then only the strongest secondary tradeoffs
10. **Fallback** — if no strong matches (all scores < 2), use default trio: CEO + CTO + CPO

Example: for a question about "tech stack," CTO should be selected first and CEO should usually be included as the strategic counterpart. For a question about "product pricing," CRO should usually be selected first because pricing is a revenue-system decision; add CEO for strategic posture, CFO for margin/runway impact, CPO for packaging/tiering, and YC only when startup simplicity or fundraising framing is explicit.

User-specified lenses always override automatic selection.

---

## Lens Capabilities

Every lens has access to the same shared toolset, reusable playbooks, and analytical frameworks:

### Available Tools

- **Web research** — Market data, competitor analysis, industry trends
- **Git operations** — `git log`, `git diff`, `git blame` for codebase context
- **File system access** — Read project files, configuration, documentation
- **Code analysis** — Read source code, trace dependencies, understand architecture
- **Shell commands** — Run tests, builds, linting, metrics

### Shared Playbooks

- **Data Analysis** — Quantify trends and validate claims against real datasets
- **Financial Statement Analysis** — Assess financial health before major commitments
- **Root Cause Analysis** — Explain failures systemically instead of stopping at symptoms
- **Risk Assessment** — Score exposure explicitly and define mitigations
- **Crisis Management** — Structure command and containment during active incidents
- **PR Crisis Recovery** — Repair trust and narrative after public damage

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

PolyLens is designed for extensibility. Adding a new lens requires three changes:

### Step 1: Create the Source Lens Brief

Create `lenses/lens-<name>.md` following the existing lens template:

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

### Step 2: Bundle the Runtime Copy

Copy the same file to `skills/shared/lenses/lens-<name>.md`.

### Step 3: Register the Lens

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

That's it. No changes to orchestrators or engines are needed. The selection algorithm picks up new lenses automatically, and the validator checks that source and bundled copies stay in sync.

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
