# PolyLens

**Multi-perspective reasoning for high-stakes decisions**

PolyLens is an agentic decision system that simulates executive-level thinking (CEO, CTO, CPO, YC, and more) to analyze problems, surface disagreements, and resolve them into clear, actionable decisions. Implemented as pure markdown skills — no code dependencies.

---

## Quick Start

```bash
git clone https://github.com/your-org/polylens.git
cd polylens
ln -s "$(pwd)/skills" ~/.config/opencode/skills/polylens
```

---

## Usage

**Executive Review** — automatic lens selection, collision detection, synthesis:

```
Run executive review on our plan to migrate from PostgreSQL to MongoDB
```

**Individual Lens** — focused single-perspective analysis:

```
Run CTO review on our new API design
```

**Pre-Fight Mode** — adversarial critique between lenses:

```
Run pre-fight review on our pricing strategy
```

---

## How It Works

```
Input Problem
    ↓
Smart Selection (2-4 lenses from registry)
    ↓
Lens Reviews (sequential, with optional tool use)
    ↓
Collision Engine (detect & classify conflicts)
    ↓
Synthesis Engine (resolve tradeoffs)
    ↓
Decision Brief (5-section structured output)
```

---

## Output Format

Every review produces a structured decision brief:

```
## Final Decision
## Key Tradeoffs
## Risks Accepted
## Mitigation Plan
## Dissenting Opinions
```

Plus detailed conflict mapping, risk register, unanimous agreements, and a confidence level (High / Medium / Low).

---

## Lenses

| Lens | Focus | Default | Triggers |
|---|---|---|---|
| CEO | Speed, growth, market direction | Yes | pricing strategy, go-to-market, roadmap |
| CTO | Scalability, risk, system integrity | Yes | tech stack, API design, scalability |
| CPO | User value, UX, retention | Yes | user experience, feature prioritization |
| YC | Clarity, fundability, simplicity | No | pitch deck, fundraising, MVP scope |
| CIO | Operational efficiency, internal systems | No | workflow automation, internal tools |
| CDO | Data strategy, analytics, metrics | No | data pipeline, analytics, ML model |
| CISO | Security posture, compliance, risk | No | authentication, GDPR, security audit |
| CXO | Customer satisfaction, journey | No | customer journey, NPS, churn reduction |
| CCO | Team alignment, documentation | No | team alignment, developer experience |

**Planned:** COO (operations & supply chain), CFO (finance & budget)

---

## Architecture

```
polylens/
├── skills/
│   ├── polylens-executive-review.md   # Orchestrator: full review
│   ├── polylens-pre-fight.md          # Orchestrator: adversarial critique
│   ├── lens-ceo.md                    # Business & Strategy
│   ├── lens-cto.md                    # Technical & Infrastructure
│   ├── lens-cpo.md                    # Product & User Experience
│   ├── lens-yc.md                     # Startup & Fundability
│   ├── lens-cio.md                    # Information & Operations
│   ├── lens-cdo.md                    # Data & Analytics
│   ├── lens-ciso.md                   # Security & Compliance
│   ├── lens-cxo.md                    # Customer Experience
│   └── lens-cco.md                    # Communication & Culture
├── engines/
│   ├── collision.md                   # Conflict detection
│   └── synthesis.md                   # Resolution & synthesis
└── prompts/
    ├── lens-registry.md               # Lens metadata
    ├── conflict-types.md              # 5 conflict types
    ├── lens-capabilities.md           # Shared toolset
    └── output-template.md             # Decision brief format
```

---

## Lens Capabilities

Every lens shares the same toolset: web research, git operations, file system access, code analysis, shell commands, and strategic frameworks (SWOT, Porter's Five Forces, RICE, Kano, and more). Lenses use tools when it would strengthen their analysis — not for the sake of research.

---

## Extensibility

Adding a new lens requires only two changes:

1. Create `skills/lens-<name>.md` with the lens prompt
2. Add an entry to `prompts/lens-registry.md` with domains, triggers, and pairing rules

No changes to orchestrators or engines are needed. The selection algorithm picks up new lenses automatically.

See `docs/README.md` for the full guide.

---

## License

MIT
