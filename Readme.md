# PolyLens

> **An AI boardroom in your terminal.** Multi-perspective reasoning for high-stakes decisions.

PolyLens simulates executive-level thinking — CEO, CTO, CPO, and more — to analyze problems, surface disagreements, and resolve them into clear, actionable decisions. Implemented as pure markdown skills with no runtime code or install scripts. Works with any AI coding agent that supports skills.

---

## ✨ Why PolyLens?

Most decisions fail not because of lack of intelligence, but because:

- **Perspectives are missing** — you're thinking like an engineer when you should think like a CEO
- **Tradeoffs are invisible** — speed vs. quality, short-term vs. long-term
- **Disagreements go unresolved** — tension is buried, not structured

PolyLens fixes this by applying multiple **lenses**, forcing structured **collision**, and running a **synthesis engine** to produce a decision brief.

---

## 📦 Installation

Clone or download this repository, then link the `skills/` directory into your agent's skills folder.

```bash
git clone <repository-url> polylens
cd polylens
```

### Platform-Specific Setup

| Agent | macOS / Linux | Windows (PowerShell) |
|---|---|---|
| **OpenCode** | `ln -s "$(pwd)/skills" ~/.config/opencode/skills/polylens` | `New-Item -ItemType Junction -Path "$env:USERPROFILE\.config\opencode\skills\polylens" -Target "$(Get-Location)\skills"` |
| **Claude Code** | `ln -s "$(pwd)/skills" ~/.claude/skills/polylens` | `New-Item -ItemType Junction -Path "$env:USERPROFILE\.claude\skills\polylens" -Target "$(Get-Location)\skills"` |
| **Codex** | `ln -s "$(pwd)/skills" ~/.codex/skills/polylens` | `New-Item -ItemType Junction -Path "$env:USERPROFILE\.codex\skills\polylens" -Target "$(Get-Location)\skills"` |
| **RooCode** | `ln -s "$(pwd)/skills" ~/.roo/skills/polylens` | `New-Item -ItemType Junction -Path "$env:USERPROFILE\.roo\skills\polylens" -Target "$(Get-Location)\skills"` |
| **Copilot** | Follow your Copilot skill/custom-instruction path conventions and point them at this repo's `skills/` directory | Same via VS Code Settings UI |

> **Tip:** After installation, verify skills are detected by asking your agent: *"What skills do you have available?"*

The installable `skills/` tree is self-contained. Runtime references stay inside that tree by using sibling-relative paths such as `../shared/prompts/...` and `../shared/engines/...`, so PolyLens can review another repository without extra directory permissions.

---

## 🚀 Usage

### Mode 1: Executive Review

Full multi-lens analysis. The orchestrator auto-selects 2-4 relevant lenses, detects conflicts, and produces a structured decision brief.

```
Run executive review on our plan to migrate from PostgreSQL to MongoDB
```

**Triggers:** *"run executive review"*, *"polylens review"*, *"multi-lens review"*, *"analyze from multiple perspectives"*

### Mode 2: Individual Lens

Single-perspective analysis for focused reviews.

```
Run CTO review on our new API design
Run CISO review on our authentication flow
```

### Mode 3: Pre-Fight

Adversarial critique. Lenses attack each other's positions, defend their own, and then either escalate the strongest disagreements for user choice or finish automatically with deterministic arbitration.

```
Run pre-fight review on our pricing strategy
Run fully automatic pre-fight review on our pricing strategy
```

**Triggers:** *"pre-fight review"*, *"adversarial review"*, *"critique from all angles"*, *"stress-test this decision"*, *"debate"*, *"fully automatic pre-fight"*, *"auto-resolve disagreements"*, *"without user input"*

Standard pre-fight stays interactive and stops when a fundamental split needs a user decision. Add language like *"fully automatic"*, *"decide for me"*, or *"without user input"* to force automatic arbitration and a completed recommendation.

Pre-fight is self-contained at runtime: it uses the embedded registry and lens briefs inside the pre-fight skill instead of reading other PolyLens files after activation.

### Markdown Artifact Storage

When a user asks PolyLens to generate and save a markdown file, store it under `docs/` instead of creating loose `.md` files at the repo root.

- Use `docs/polylens/reviews/` for executive review briefs
- Use `docs/polylens/pre-fight/` for pre-fight reports
- Use `docs/polylens/plans/` for plans and proposals
- Use `docs/polylens/memory/` for memory notes, working notes, and generic markdown memos when no better category is clear
- Use `docs/polylens/notes/` for other supporting notes

Filename convention:

- `YYMMDD_slug_rN.md`
- Example: `docs/polylens/memory/260405_selection-logic_r1.md`
- Use a clear, descriptive slug rather than a very short label; prefer names like `selection-logic-routing-fix` over `fix`
- Start at `r1`; increment the revision number when saving another version of the same dated slug

---

## 👥 The Lenses

| Lens | Full Name | Focus | Default | When It Fires |
|------|-----------|-------|:-------:|---------------|
| 🎯 **CEO** | Chief Executive Officer | Speed, growth, market direction | Yes | Pricing, go-to-market, roadmap |
| ⚙️ **CTO** | Chief Technology Officer | Scalability, risk, system integrity | Yes | Tech stack, architecture, scalability |
| 🧩 **CPO** | Chief Product Officer | User value, UX, retention | Yes | Feature design, usability, product-market fit |
| 💰 **CFO** | Chief Financial Officer | Financial sustainability, capital strategy | No | Budget, profitability, unit economics, fundraising |
| 🔗 **COO** | Chief Operating Officer | Operations, supply chain, process optimization | No | Supply chain, vendor management, capacity planning |
| 📣 **CMO** | Chief Marketing Officer | Marketing, brand, growth acquisition | No | Marketing campaigns, brand strategy, customer acquisition |
| 🤝 **CBDO** | Chief Business Development Officer | Partnerships, revenue channels, strategic alliances | No | Partnerships, joint ventures, channel strategy |
| 💼 **CRO** | Chief Revenue Officer | Revenue strategy, sales execution, GTM alignment | No | Revenue targets, pipeline, pricing optimization, sales velocity |
| 🚀 **YC** | Y Combinator | Clarity, fundability, simplicity | No | Fundraising, MVP scope, investor readiness |
| 📊 **CIO** | Chief Information Officer | Operational efficiency, internal systems | No | Workflow automation, internal tools |
| 📈 **CDO** | Chief Data Officer | Data strategy, analytics, metrics | No | Data pipelines, ML, business intelligence |
| 🔒 **CISO** | Chief Information Security Officer | Security posture, compliance, risk | No | Auth, GDPR, SOC2, vulnerability |
| 👤 **CXO** | Chief Experience Officer | Customer experience, UI/UX design, journey | No | NPS, churn, support, UI design, accessibility |
| 🧑‍🤝‍🧑 **CCO** | Chief Customer Officer | Customer journey, retention, satisfaction, advocacy | No | Customer retention, churn reduction, NPS, customer success |
| 🤖 **CAIO** | Chief AI Officer | AI strategy, ethics, governance, AI ROI | No | AI/ML deployment, AI ethics, LLM integration, AI compliance |
| 🔄 **CAgO** | Chief Agile Officer | Organizational agility, delivery enablement, team health | No | Agile transformation, sprint planning, ways of working |
| 👥 **CHRO** | Chief Human Resources Officer | Talent strategy, culture, employee experience | No | Hiring, retention, compensation, leadership development |
| ⚖️ **CLO** | Chief Legal Officer | Legal risk, regulatory compliance, governance, IP | No | Contract review, regulatory compliance, IP protection |

**Default lenses** (CEO + CTO + CPO) activate when no strong keyword match is found.

---

## 🧠 How It Works

```
Your Problem
    ↓
Smart Lens Selection  ← 2-4 lenses chosen by context
    ↓
Individual Reviews    ← Each lens researches, analyzes, takes a position
    ↓
Collision Engine      ← Detects & classifies disagreements
    ↓
Synthesis Engine      ← Resolves tradeoffs, assembles brief
    ↓
Decision Brief        ← 5-section structured output
```

### Smart Lens Selection

The orchestrator doesn't run all lenses. It selects the most relevant ones:

1. **Filter** — only active lenses considered
2. **Anchor** — identify the primary decision being asked, separate from supporting constraints
3. **Check ownership** — if a lens role owns that decision category, it should usually be included before adjacent lenses that only evaluate consequences
4. **Match** — scan problem against each lens's domains, triggers, and owned decision categories
5. **Downweight ambient constraints** — budget, timeline, team size, compliance, or risk details are supporting signals unless explicitly decision-driving
6. **Apply veto coverage** — if the prompt explicitly touches a veto area, include that lens or explain why it is being deferred
7. **Boost** — pair complementary lenses (+0.5)
8. **Add strategy complement when needed** — if the decision is foundational and company-shaping, include the nearest strategy lens even when the wording is technical
9. **Select** — choose 2-4 lenses that cover the anchor decision first, then only the strongest secondary tradeoffs
10. **Fallback** — default trio if no strong matches

Example: for a question about "tech stack," CTO should be selected first and CEO should usually be included as the strategic counterpart. For a question about "product pricing," CRO should usually be selected first because pricing is a revenue-system decision; add CEO for strategic posture, CFO for margin/runway impact, CPO for packaging/tiering, and YC only when startup simplicity or fundraising framing is explicit.

You can always override: *"Run CTO + CISO review on this auth system"*

---

## 📋 Output: Decision Brief

Every executive review produces a structured 5-section brief:

1. **Individual Positions**: GO / MODIFY / BLOCK verdicts with concerns, endorsements, and non-negotiables.
2. **Conflict Detection**: Verdict alignment summary plus conflict counts.
3. **Conflict Mapping**: Stacked comparison across Scope, Timeline, Resource, Risk, and Success Criteria.
4. **Final Alignment**: Changes to plan, unanimous agreements, deferred decisions, assumptions, and a risk register.
5. **Summary Dashboard**: Compact executive summary with decision, tradeoffs, risks, mitigations, and confidence.

The brief is optimized for chat and narrow panes: prefer labeled sections and bullets over wide tables or ASCII borders.

Example presentation:

```markdown
VERDICT ALIGNMENT
=================
Alignment: SPLIT
CTO: MODIFY
CPO: GO
CEO: MODIFY

CONFLICT MAP
============
- Scope:
    - CTO: Narrow to API and schema changes first
    - CPO: Include the full onboarding flow now
    - CEO: Ship the smallest differentiated wedge

FINAL DECISION
--------------
Ship a pilot now, defer platform-heavy changes to phase two.
```

Conflicts are classified into 5 types: **Priority**, **Scope**, **Risk**, **Resource**, and **Fundamental**. Types 1-4 are auto-resolved; Type 5 is escalated to you.

---

## 🛠️ Lens Capabilities

Every lens can use any tool — not just think in isolation:

| Tool | Purpose |
|------|---------|
| 🌐 **Web research** | Market data, competitor analysis, industry trends |
| 📂 **Git operations** | `git log`, `git diff` — understand codebase history |
| 📄 **File access** | Read project files, configuration, documentation |
| 🔍 **Code analysis** | Trace dependencies, understand architecture |
| ⚡ **Shell commands** | Run tests, builds, linting, metrics |

Plus analytical frameworks: **SWOT**, **Porter's Five Forces**, **Jobs-to-be-Done**, **RICE**, **Kano Model**, **Cost of Delay**, **Technical Debt Quadrant**, **DORA Metrics**.

---

## 🏗️ Architecture

```
polylens/
├── skills/
│   ├── polylens-executive-review.md  # Orchestrator: full pipeline
│   ├── polylens-pre-fight.md         # Orchestrator: adversarial mode
│   ├── shared/                       # Bundled runtime docs used by installed skills
│   │   ├── prompts/
│   │   └── engines/
│   ├── lens-***/                     # Individual lenses skill
│   │   └── SKILL.md
├── engines/                          # Shared processing logic
│   ├── collision.md                  # Conflict detection & classification
│   └── synthesis.md                  # Resolution strategies & output
├── prompts/                          # Centralized data & templates
│   ├── lens-registry.md              # Lens metadata (domains, triggers, pairs)
│   ├── lens-capabilities.md          # Shared toolset & frameworks
│   ├── conflict-types.md             # 5 conflict type definitions
│   └── output-template.md            # 5-section decision brief format
├── docs/
│   ├── README.md                     # Extended documentation
│   ├── polylens/
│   │   ├── README.md                 # Artifact storage conventions
│   │   ├── memory/                   # Generic markdown memos and working notes
│   │   ├── notes/                    # Supporting notes
│   │   ├── plans/                    # Plans and proposals
│   │   ├── pre-fight/                # Saved pre-fight reports
│   │   └── reviews/                  # Saved executive review briefs
└── README.md                         # Project overview
```

The root `prompts/` and `engines/` directories remain the source docs for development. Their runtime copies live under `skills/shared/` so installed agents only need access to the symlinked `skills/` tree.

### Lens Directory Structure

Each lens lives in its own directory (`lens-<name>/SKILL.md`), enabling future extensions:

| Subdirectory | Purpose |
|--------------|---------|
| `SKILL.md` | The lens definition — philosophy, directives, metrics, strategy, review process |
| `scripts/` | Executable helpers (e.g., `calculate-dora-metrics.sh`, `check-vulnerabilities.py`) |
| `reference/` | Domain frameworks and standards (e.g., `owasp-top-10.md`, `dora-metrics.md`) |
| `checklists/` | Standalone audit checklists (e.g., `security-review-checklist.md`) |
| `templates/` | Output artifacts (e.g., `incident-report-template.md`, `post-mortem-template.md`) |

### Three-Layer Design

| Layer | Purpose | Files |
|-------|---------|-------|
| **Skills** | Individual lens prompts and orchestrators | `skills/*/SKILL.md`, `skills/polylens-*.md` |
| **Engines** | Shared collision detection and synthesis | `engines/*.md` |
| **Prompts** | Lens registry, conflict taxonomy, templates | `prompts/*.md` |

---

## ➕ Adding New Lenses

PolyLens is designed for extensibility. Adding a lens requires **two files**:

1. **Create the lens directory:** `skills/lens-<name>/SKILL.md` (follow existing lens template)
2. **Register it:** Add entry to `prompts/lens-registry.md` with domains, triggers, pairs_with

Optional subdirectories for heavier lenses:
- `scripts/` — Executable helpers that pull live data
- `reference/` — Domain frameworks and standards
- `checklists/` — Standalone audit checklists
- `templates/` — Output artifacts and report formats

That's it. No changes to orchestrators or engines. The selection algorithm picks up new lenses automatically.

---

## 🤝 Contributing

Contributions welcome:

- **New lenses** — Add perspectives we haven't covered
- **Improved frameworks** — Better analytical frameworks for lenses
- **Conflict resolution** — New strategies for resolving disagreements
- **Engine improvements** — Better collision detection or synthesis logic
- **Documentation** — Clearer examples, better explanations

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run `python3 tools/validate_markdown_contracts.py`
5. Test by invoking the skill in your AI agent
6. Submit a pull request

### Contract Validation

PolyLens includes a repo-native validator that checks the working markdown contract across the lens registry, active lens skills, orchestrators, engines, and output templates.

```bash
python3 tools/validate_markdown_contracts.py
```

The command exits non-zero when shared fields, lens inventory, or orchestration rules drift out of sync. The same check also runs automatically in GitHub Actions on pushes and pull requests.

---

## 📜 License

**GNU General Public License v3.0**

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but **WITHOUT ANY WARRANTY**; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the [GNU GPL v3.0](LICENSE) for more details.
