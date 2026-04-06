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

The easiest install path is to hand your agent a single prompt and let it follow the fetchable install instructions.

### Agent Prompt

```text
Fetch and follow installation instructions from https://raw.githubusercontent.com/PohLee/PolyLens/main/INSTALL.md.
Detect my platform and target agent, install PolyLens from https://github.com/PohLee/PolyLens, use the dedicated OpenCode installer when the target is OpenCode, use the matching Claude Code, Codex, or Copilot installer when available, otherwise preserve the sibling skill layout `polylens/`, `polylens-lens-review/`, and `shared/`, and do not symlink the whole repo root. Verify the skills are discoverable when finished.
```

### What The Agent Will Do

The install instructions tell the agent to:

- use this repository as the source
- detect the target agent and skills location
- use `bash tools/install_opencode.sh` for OpenCode
- use `bash tools/install_claude_code.sh` for Claude Code when doing a personal install
- use `bash tools/install_codex.sh` for Codex when doing a personal install
- use `bash tools/install_copilot_workspace.sh /path/to/workspace` for GitHub Copilot workspace installs
- otherwise expose `skills/polylens`, `skills/polylens-lens-review`, and `skills/shared` as sibling directories in the target skills location
- verify the install

### Manual Reference

If you want to install PolyLens yourself, use the steps below.

Clone or download this repository, then expose the contents of the repo's `skills/` directory in an agent skills location.

```bash
git clone <repository-url> polylens
cd polylens
```

### Recommended Layout

For most agents, the target skills location should contain these three sibling directories:

- `polylens/`
- `polylens-lens-review/`
- `shared/`

Do **not** symlink the whole project root. The installable runtime bundle is the repo's `skills/` tree, and the public skills rely on `shared/` being a sibling directory via paths such as `../shared/...`.

OpenCode is the exception. Its runtime path handling can break sibling traversal for markdown dependencies, so use the dedicated installer instead of direct symlinks:

```bash
bash tools/install_opencode.sh
```

That command builds `dist/opencode-polylens/` and installs self-contained `polylens/` and `polylens-lens-review/` directories with nested `shared/` assets under `~/.config/opencode/skills/` by default.

For other common agents, PolyLens now provides direct installer scripts as well:

```bash
bash tools/install_claude_code.sh
bash tools/install_codex.sh
bash tools/install_copilot_workspace.sh /path/to/workspace
```

Those scripts build `dist/standard-polylens/` and install the standard sibling bundle expected by Claude Code, Codex, RooCode-style setups, and Copilot workspace skills.

### Personal Install Via Symlink

Point your agent's personal skills directory at the three directories inside this repo's `skills/` folder.

Do not use this symlink flow for OpenCode.

If you want a copied bundle rather than symlinks for Claude Code or Codex, use `bash tools/install_claude_code.sh` or `bash tools/install_codex.sh`.

macOS / Linux example:

```bash
mkdir -p ~/.claude/skills
ln -s "$(pwd)/skills/polylens" ~/.claude/skills/polylens
ln -s "$(pwd)/skills/polylens-lens-review" ~/.claude/skills/polylens-lens-review
ln -s "$(pwd)/skills/shared" ~/.claude/skills/shared
```

Windows PowerShell example:

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude\skills" | Out-Null
New-Item -ItemType Junction -Path "$env:USERPROFILE\.claude\skills\polylens" -Target "$(Get-Location)\skills\polylens" | Out-Null
New-Item -ItemType Junction -Path "$env:USERPROFILE\.claude\skills\polylens-lens-review" -Target "$(Get-Location)\skills\polylens-lens-review" | Out-Null
New-Item -ItemType Junction -Path "$env:USERPROFILE\.claude\skills\shared" -Target "$(Get-Location)\skills\shared" | Out-Null
```

If your agent uses a different personal skills directory, replace `~/.claude/skills` with that agent's equivalent skills path. The important part is that the final directory contains the three sibling directories shown above.

For OpenCode, run `bash tools/install_opencode.sh` instead of creating direct symlinks to `skills/`.

### VS Code / Copilot

GitHub Copilot in VS Code discovers project skills from `.github/skills/`, `.claude/skills/`, or `.agents/skills/` by default. For this repo, use one of these approaches:

- Run `bash tools/install_copilot_workspace.sh /path/to/workspace` to copy the bundle into `.github/skills/`
- Copy or symlink `skills/polylens`, `skills/polylens-lens-review`, and `skills/shared` into `.github/skills/` or `.claude/skills/`
- Or add `./skills` to the `chat.skillsLocations` setting so VS Code treats this repo's `skills/` folder as a skill location

> **Tip:** After installation, verify skills are detected by asking your agent: *"What skills do you have available?"*

The installable `skills/` tree is self-contained. Runtime references stay inside that tree by using sibling-relative paths such as `../shared/prompts/...`, `../shared/engines/...`, `../shared/lenses/...`, and `../shared/orchestrators/...`, so PolyLens can review another repository without extra directory permissions.

Additional navigation:

- Docs index: [docs/README.md](docs/README.md)
- Artifact storage rules: [docs/polylens/README.md](docs/polylens/README.md)

---

## 🚀 Usage

### Mode 1: Standard PolyLens Review

Full multi-lens analysis through the top-level `polylens` router. It defaults to the standard review flow unless the prompt clearly asks for adversarial or pre-fight behavior.

```
Run polylens review on our plan to migrate from PostgreSQL to MongoDB
```

**Triggers:** *"run executive review"*, *"polylens review"*, *"multi-lens review"*, *"analyze from multiple perspectives"*

### Mode 2: Focused Lens Review

Single-perspective analysis through one routed entry skill. PolyLens picks the best lens automatically unless you name one explicitly.

```
Run lens review on our new API design
Run lens review on our authentication flow and use the CISO lens
```

### Mode 3: PolyLens Pre-Fight

Adversarial critique through the same top-level `polylens` router. When the prompt asks for pre-fight, debate, adversarial review, or automatic arbitration, PolyLens routes to the internal pre-fight orchestrator.

```
Run polylens pre-fight review on our pricing strategy
Run polylens fully automatic pre-fight review on our pricing strategy
```

**Triggers:** *"pre-fight review"*, *"adversarial review"*, *"critique from all angles"*, *"stress-test this decision"*, *"debate"*, *"fully automatic pre-fight"*, *"auto-resolve disagreements"*, *"without user input"*

Standard pre-fight stays interactive and stops when a fundamental split needs a user decision. Add language like *"fully automatic"*, *"decide for me"*, or *"without user input"* to force automatic arbitration and a completed recommendation.

Pre-fight remains self-contained at runtime: the router delegates to the internal pre-fight orchestrator, which uses its embedded registry and lens briefs instead of reading other PolyLens files after activation.

### Markdown Artifact Storage

When a user asks PolyLens to generate and save a markdown file, store it under `docs/` instead of creating loose `.md` files at the repo root.

- Use `docs/polylens/reviews/` for executive review briefs
- Use `docs/polylens/pre-fight/` for pre-fight reports
- Use `docs/polylens/plans/` for plans and proposals
- Use `docs/polylens/memory/` for memory notes, working notes, and generic markdown memos when no better category is clear
- Use `docs/polylens/notes/` for other supporting notes

When storing project-specific memory, separate it into:

- `project-context` for durable facts such as mission, vision, strategic posture, constraints, and non-negotiables
- `project-preferences` for recurring defaults about how PolyLens should run reviews in that project
- `decision-history` for prior decisions and rationale that future reviews should respect

Filename convention:

- `YYMMDD_slug_rN.md`
- Example: `docs/polylens/memory/260405_selection-logic_r1.md`
- Use a clear, descriptive slug rather than a very short label; prefer names like `selection-logic-routing-fix` over `fix`
- Start at `r1`; increment the revision number when saving another version of the same dated slug

---

## 👥 The Lenses

These are internal perspectives in the routing system, not separate top-level skills. The public entrypoints route to them when needed.

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

## 🔧 Shared Playbooks

Beyond lenses, PolyLens includes reusable playbooks that any lens or orchestrator can apply when the problem needs deeper structure:

| Playbook | Purpose | When to Apply |
|-------|---------|-------------|
| 📊 **Data Analysis** | Explore datasets, compute statistics, and quantify trends | When a decision depends on actual dataset evidence |
| 💹 **Financial Statement Analysis** | Analyze profitability, liquidity, solvency, efficiency, and cash flow | When a decision depends on financial health or capacity |
| 🔍 **Root Cause Analysis** | Investigate incidents and recurring failures using causal chains | When a problem needs systemic explanation, not symptom treatment |
| ⚠️ **Risk Assessment** | Identify, score, prioritize, and mitigate cross-domain risks | When tradeoffs need explicit exposure mapping |
| 🚨 **Crisis Management** | Structure command, containment, continuity, and recovery | When an active crisis needs disciplined response |
| 📢 **PR Crisis Recovery** | Assess reputation damage and design a trust-rebuilding response | When public narrative and stakeholder trust are at risk |
| 🏁 **Competitive Analysis** | Map competitors, compare positioning, identify threats and opportunities | When strategic decisions need competitive context |
| 🚀 **Go-to-Market Planning** | Structure launches, messaging, channels, and success metrics | When launching a product, feature, or entering a new market |
| 🔮 **Scenario Planning** | Explore multiple futures, stress-test strategies, find early signals | When uncertainty is high and a single forecast is insufficient |
| 🏢 **Vendor Evaluation** | Scorecard-based vendor comparison, TCO, and lock-in risk | When choosing between tools, vendors, or build vs. buy |
| 🗣️ **Customer Interview Synthesis** | Extract patterns, map JTBD, prioritize problems from interviews | When qualitative research needs to drive product decisions |
| 💼 **Business Model Analysis** | Canvas, unit economics, pricing, revenue model stress-testing | When evaluating or designing a business model |
| 🎯 **OKR Planning** | Set, align, and cascade objectives and key results | When setting quarterly or annual goals |
| 📋 **Project Post-Mortem** | Structured review, lessons learned, action items | When a project concludes and you need to capture learnings |
| ✅ **Product Launch Readiness** | Pre-launch checklist, go/no-go, cross-functional alignment | Before any product or feature launch |
| 💰 **Cost-Benefit Analysis** | NPV, ROI, payback, sensitivity analysis across alternatives | When comparing investment options with financial rigor |
| 📊 **Board Reporting** | Board deck structure, KPI narrative, decision framing | When preparing board meeting materials |

These live under `prompts/playbooks/` in source form and under `skills/shared/playbooks/` in the installable runtime bundle.

### Usage Examples

```
Run polylens review on the outage and apply the root-cause-analysis playbook
Run CFO + CEO review on the acquisition and use the financial-statement-analysis playbook
Run polylens pre-fight review on the launch plan and include a risk assessment
```

---

## 🔌 Harness & Hooks

PolyLens includes a harness system for extended control over the analysis pipeline. Trigger it through prompts — no files needed unless you want reusable configurations.

### When Harness Activates

The harness activates when you request features like deep analysis, validation, multi-instance orchestration, or custom hooks. Standard reviews run without harness involvement.

### Hooks

Inject custom logic at any stage of the PolyLens pipeline:

| Stage | When it fires | Purpose |
|-------|---------------|---------|
| Pre-analysis | Before analysis | Inject context, load constraints |
| Lens-select | During selection | Force lenses, override scoring |
| Review | During lens reviews | Add frameworks, custom logic |
| Collision | During conflict detection | Adjust conflict weights |
| Synthesis | During brief synthesis | Override output format |
| Post-analysis | After analysis | Summarize, notify external systems |

#### User Prompt Examples

**Deep analysis with validation:**
```
Run polylens review on our pricing strategy with deep analysis and full validation
```

**Inline hooks (no files needed):**
```
Run polylens review on our hiring plan with these hooks:

PRE-ANALYSIS: This is a Series B startup. Team: 45 people. Runway: 18 months. Budget for hiring: $2M/year.
POST-ANALYSIS: Generate a one-paragraph executive summary.
```

**Force specific lenses:**
```
Run polylens review with CTO and CISO lenses only
```

### Harness Orchestration

Run multiple PolyLens analyses in sequence, parallel, or conditionally. The AI agent detects your intent and chains analyses automatically.

#### User Prompt Examples

**Sequential chaining:**
```
Run polylens review on our new API design. First do a technical review with CTO+CISO, then use that output to run a business impact review with CEO+CFO.
```

**Conditional orchestration:**
```
Run polylens review on our auth system redesign. If any HIGH security risks are found, automatically trigger a CISO deep-dive.
```

### Reasoning Control

Control analysis depth, constraints, and output format via prompt keywords.

#### User Prompt Examples

**Deep analysis:**
```
Run polylens review with deep analysis on our migration plan
```

**With constraints:**
```
Run polylens review with budget under $50K and timeline Q2 2026 constraints
```

**Concise output:**
```
Run polylens review with concise output format
```

### Validation

Automated checks appended to your decision brief: contract compliance, quality scoring, consistency verification.

#### User Prompt Examples

**Full validation:**
```
Run polylens review with full validation on our pricing strategy
```

**Validate existing brief:**
```bash
python3 tools/harness.py validate docs/polylens/reviews/260405_migration_r1.md
```

### CLI Reference

```bash
# List available hooks
python3 tools/harness.py hooks list

# Enable/disable a hook
python3 tools/harness.py hooks enable pre-analysis/inject-context
python3 tools/harness.py hooks disable pre-analysis/inject-context

# Run with harness (AI agent handles this automatically)
python3 tools/harness.py run "Your problem" --depth deep

# Validate an existing brief
python3 tools/harness.py validate docs/polylens/reviews/260405_migration_r1.md
```

### Configuration Files (Optional)

For reusable setups, create files in `harness/`:

- `harness/orchestration.md` — Multi-instance orchestration config
- `harness/reasoning.md` — Default reasoning controls
- `harness/validation.md` — Default validation settings

Create reusable hooks in `hooks/<stage>/`:
- `hooks/pre-analysis/inject-context.md`
- `hooks/post-analysis/summarize.md`
- etc.

> **Note:** Harness features require Python 3. The core PolyLens review works without it.

---

## 🧠 How It Works

```
Your Problem
    ↓
Mode Routing        ← standard review or pre-fight
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

The standard review orchestrator doesn't run all lenses. It selects the most relevant ones:

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

Shared playbooks are also available when the analysis needs more structure: **Data Analysis**, **Financial Statement Analysis**, **Root Cause Analysis**, **Risk Assessment**, **Crisis Management**, and **PR Crisis Recovery**.

---

## 🏗️ Architecture

```
polylens/
├── .github/
│   └── workflows/                    # CI validation for markdown contract drift
├── .superpowers/
│   └── brainstorm/                   # Workspace-local supporting assets
├── docs/
│   ├── README.md                     # Docs index
│   ├── project-memory-model.md       # Project memory schema
│   ├── polylens/
│   │   ├── README.md                 # Artifact storage conventions
│   │   ├── memory/                   # Generic markdown memos and working notes
│   │   ├── notes/                    # Supporting notes
│   │   ├── plans/                    # Plans and proposals
│   │   ├── pre-fight/                # Saved pre-fight reports
│   │   └── reviews/                  # Saved executive review briefs
│   └── superpowers/                  # Superpower-specific docs and plans
├── engines/                          # Shared processing logic
│   ├── collision.md                  # Conflict detection & classification
│   └── synthesis.md                  # Resolution strategies & output
├── harness/                          # Harness configuration (orchestration, reasoning, validation)
│   ├── orchestration.md
│   ├── reasoning.md
│   └── validation.md
├── hooks/                            # Hook definitions (injected at pipeline stages)
│   ├── pre-analysis/
│   ├── lens-select/
│   ├── review/
│   ├── collision/
│   ├── synthesis/
│   └── post-analysis/
├── lenses/                           # Source lens briefs
│   └── lens-*.md
├── orchestrators/                    # Internal multi-lens review modes
│   ├── polylens-executive-review.md
│   └── polylens-pre-fight.md
├── prompts/                          # Centralized data and source templates
│   ├── lens-registry.md              # Lens metadata (domains, triggers, pairs)
│   ├── lens-capabilities.md          # Shared toolset and frameworks
│   ├── shared-playbooks.md           # Reusable analysis methods index
│   ├── playbooks/                    # Detailed shared playbooks
│   ├── conflict-types.md             # 5 conflict type definitions
│   └── output-template.md            # 5-section decision brief format
├── skills/
│   ├── polylens/                     # Top-level multi-lens router
│   ├── polylens-lens-review/         # Single-entry focused lens router
│   └── shared/                       # Installable runtime bundle used by the public skills
│       ├── prompts/
│       ├── engines/
│       ├── harness/                  # Bundled harness configs
│       ├── hooks/                    # Bundled hook definitions
│       ├── lenses/
│       ├── orchestrators/
│       ├── playbooks/
│       └── tools/                    # Bundled Python tools
├── tools/
│   ├── harness.py                    # Harness engine (hook registry, orchestration, validation)
│   ├── sync_playbooks.py             # Sync source files into the runtime bundle
│   └── validate_markdown_contracts.py# Validate routers, lenses, engines, and templates stay aligned
└── README.md                         # Project overview
```

The root `prompts/`, `engines/`, `lenses/`, and `orchestrators/` directories remain the source docs for development. Their installable runtime copies live under `skills/shared/`, which is why the published install shape only needs the sibling `polylens/`, `polylens-lens-review/`, and `shared/` directories.

### Lens Library Structure

Each lens now lives as a shared brief file instead of a public skill entry:

| File | Purpose |
|------|---------|
| `lenses/lens-<name>.md` | Source lens definition — philosophy, directives, metrics, strategy, review process |
| `skills/shared/lenses/lens-<name>.md` | Bundled runtime copy used by installed skills |

### Five-Layer Design

| Layer | Purpose | Files |
|-------|---------|-------|
| **Skills** | Public entrypoints only | `skills/polylens*/SKILL.md` |
| **Orchestrators** | Internal multi-lens mode implementations | `orchestrators/*.md`, `skills/shared/orchestrators/*.md` |
| **Lens Library** | Internal perspective briefs selected by routing | `lenses/lens-*.md`, `skills/shared/lenses/lens-*.md` |
| **Engines** | Shared collision detection and synthesis | `engines/*.md` |
| **Prompts** | Lens registry, conflict taxonomy, shared playbooks, and templates | `prompts/*.md`, `prompts/playbooks/*.md` |

### Shared Playbooks vs Lenses

| Aspect | Lenses | Shared Playbooks |
|--------|--------|---------------|
| **Purpose** | Multi-perspective decision review | Reusable analytical methods inside a review |
| **Invocation** | Routed through `polylens` or `polylens-lens-review` | Applied by lenses or orchestrators when needed |
| **Output** | Position block (GO/MODIFY/BLOCK) | Supporting analysis folded into a lens position or synthesis |
| **Examples** | CEO, CTO, CPO, CFO, CRO | Data Analysis, Financial Statement Analysis, Root Cause Analysis |

---

## ➕ Adding New Lenses

PolyLens is designed for extensibility. Adding a lens requires **three updates**:

1. **Create the source lens brief:** `lenses/lens-<name>.md`
2. **Bundle the runtime copy:** `skills/shared/lenses/lens-<name>.md`
3. **Register it:** Add entry to `prompts/lens-registry.md` with domains, triggers, pairs_with

The validator checks that the source and bundled copies stay identical.

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

PolyLens includes a repo-native validator that checks the working markdown contract across the public routers, internal orchestrators, shared lens library, engines, bundled runtime copies, and output templates.

When you change files under `prompts/playbooks/` or `prompts/shared-playbooks.md`, resync the bundled runtime copy first:

```bash
python3 tools/sync_playbooks.py
```

```bash
python3 tools/validate_markdown_contracts.py
```

The command exits non-zero when shared fields, lens inventory, or orchestration rules drift out of sync. The same check also runs automatically in GitHub Actions on pushes and pull requests.

---

## 📜 License

**GNU General Public License v3.0**

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but **WITHOUT ANY WARRANTY**; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the [GNU GPL v3.0](LICENSE) for more details.
