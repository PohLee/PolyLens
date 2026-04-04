# PolyLens

> **An AI boardroom in your terminal.** Multi-perspective reasoning for high-stakes decisions.

PolyLens simulates executive-level thinking — CEO, CTO, CPO, and more — to analyze problems, surface disagreements, and resolve them into clear, actionable decisions. Implemented as pure markdown skills with zero code dependencies. Works with any AI coding agent that supports skills.

---

## ✨ Why PolyLens?

Most decisions fail not because of lack of intelligence, but because:
- **Perspectives are missing** — you're thinking like an engineer when you should think like a CEO
- **Tradeoffs are invisible** — speed vs. quality, short-term vs. long-term
- **Disagreements go unresolved** — tension is buried, not structured

PolyLens fixes this by applying multiple **lenses**, forcing structured **collision**, and running a **synthesis engine** to produce a decision brief.

---

## 📦 Installation

### OpenCode

```bash
git clone https://github.com/your-org/polylens.git
ln -s "$(pwd)/polylens/skills" ~/.config/opencode/skills/polylens
```

### Claude Code

```bash
git clone https://github.com/your-org/polylens.git
ln -s "$(pwd)/polylens/skills" ~/.claude/skills/polylens
```

### Codex (OpenAI)

```bash
git clone https://github.com/your-org/polylens.git
ln -s "$(pwd)/polylens/skills" ~/.codex/skills/polylens
```

### RooCode (Roo Cline)

```bash
git clone https://github.com/your-org/polylens.git
ln -s "$(pwd)/polylens/skills" ~/.roo/skills/polylens
```

### GitHub Copilot (VS Code)

```bash
git clone https://github.com/your-org/polylens.git
# In VS Code: Settings → Copilot → Custom Instructions → Add path to skills
# Or: create .github/copilot-instructions.md and reference the skills directory
```

> **Tip:** After installation, verify skills are detected by asking your agent: *"What skills do you have available?"*

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

Adversarial critique. Lenses attack each other's positions, defend their own, and escalate the strongest disagreements.

```
Run pre-fight review on our pricing strategy
```

**Triggers:** *"pre-fight review"*, *"adversarial review"*, *"critique from all angles"*, *"stress-test this decision"*

---

## 👥 The Lenses

| Lens | Focus | Default | When It Fires |
|:---:|---|:---:|---|
| 🎯 **CEO** | Speed, growth, market direction | ✅ | Pricing, go-to-market, roadmap |
| ⚙️ **CTO** | Scalability, risk, system integrity | ✅ | Tech stack, architecture, scalability |
| 🧩 **CPO** | User value, UX, retention | ✅ | Feature design, usability, product-market fit |
| 🚀 **YC** | Clarity, fundability, simplicity | | Fundraising, MVP scope, unit economics |
| 📊 **CIO** | Operational efficiency, internal systems | | Workflow automation, internal tools |
| 📈 **CDO** | Data strategy, analytics, metrics | | Data pipelines, ML, business intelligence |
| 🔒 **CISO** | Security posture, compliance, risk | | Auth, GDPR, SOC2, vulnerability |
| 👤 **CXO** | Customer satisfaction, journey | | NPS, churn, support, onboarding |
| 💬 **CCO** | Team alignment, documentation | | Developer experience, culture, communication |

**Default lenses** (CEO + CTO + CPO) activate when no strong keyword match is found.

### Planned Lenses

| Lens | Focus |
|:---:|---|
| 🏭 **COO** | Operational scaling, supply chain, process optimization |
| 💰 **CFO** | Financial sustainability, budget, profitability |

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
2. **Match** — scan problem against each lens's domains & triggers
3. **Score** — count keyword matches
4. **Boost** — pair complementary lenses (+0.5)
5. **Select** — top 2-4 lenses
6. **Fallback** — default trio if no strong matches

You can always override: *"Run CTO + CISO review on this auth system"*

---

## 📋 Output: Decision Brief

Every executive review produces a structured 5-section brief:

| # | Section | What It Contains |
|:---:|---|---|
| 1 | **Individual Positions** | GO / MODIFY / BLOCK verdicts with concerns, endorsements, non-negotiables |
| 2 | **Conflict Detection** | Verdict alignment table — UNANIMOUS / 2-vs-1 / ALL DISAGREE |
| 3 | **Conflict Mapping** | Matrix across Scope, Timeline, Resource, Risk, Success Criteria |
| 4 | **Final Alignment** | Changes to plan, unanimous agreements, deferred decisions, risk register |
| 5 | **Summary Dashboard** | Executive summary with decision, tradeoffs, risks, mitigations, confidence |

Conflicts are classified into 5 types: **Priority**, **Scope**, **Risk**, **Resource**, and **Fundamental**. Types 1-4 are auto-resolved; Type 5 is escalated to you.

---

## 🛠️ Lens Capabilities

Every lens can use any tool — not just think in isolation:

| Tool | Purpose |
|---|---|
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
├── skills/                          # 11 invocable skill files
│   ├── polylens-executive-review.md # Orchestrator: full pipeline
│   ├── polylens-pre-fight.md        # Orchestrator: adversarial mode
│   ├── lens-ceo.md                  lens-cto.md
│   ├── lens-cpo.md                  lens-yc.md
│   ├── lens-cio.md                  lens-cdo.md
│   ├── lens-ciso.md                 lens-cxo.md
│   └── lens-cco.md
├── engines/                         # Shared processing logic
│   ├── collision.md                 # Conflict detection & classification
│   └── synthesis.md                 # Resolution strategies & output
├── prompts/                         # Centralized data & templates
│   ├── lens-registry.md             # Lens metadata (domains, triggers, pairs)
│   ├── lens-capabilities.md         # Shared toolset & frameworks
│   ├── conflict-types.md            # 5 conflict type definitions
│   └── output-template.md           # 5-section decision brief format
└── docs/
    └── README.md                    # Extended documentation
```

---

## ➕ Adding New Lenses

PolyLens is designed for extensibility. Adding a lens requires **two files**:

1. **Create the skill:** `skills/lens-<name>.md` (follow existing lens template)
2. **Register it:** Add entry to `prompts/lens-registry.md` with domains, triggers, pairs_with

That's it. No changes to orchestrators or engines. The selection algorithm picks up new lenses automatically.

See [docs/README.md](docs/README.md) for detailed contribution guide and lens template.

---

## 🤝 Contributing

Contributions welcome:

- **New lenses** — COO, CFO, and perspectives we haven't covered
- **Improved frameworks** — Better analytical frameworks for lenses
- **Conflict resolution** — New strategies for resolving disagreements
- **Engine improvements** — Better collision detection or synthesis logic
- **Documentation** — Clearer examples, better explanations

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test by invoking the skill in your AI agent
5. Submit a pull request

---

## 📜 License

**GNU General Public License v3.0**

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but **WITHOUT ANY WARRANTY**; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the [GNU GPL v3.0](LICENSE) for more details.
