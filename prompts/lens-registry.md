# Lens Registry

Each lens declares its metadata for context-aware selection. The orchestrator reads this file to automatically select the 2-4 most relevant lenses based on problem context.

## Format

Each lens entry contains:
- **focus:** One-line description
- **domains:** Areas of expertise (used for keyword matching)
- **triggers:** Keywords/phrases that activate the lens
- **pairs_with:** Lenses that naturally complement this one
- **default:** Part of fallback trio
- **active:** Whether this lens is ready for selection (true) or planned for future (false)
- **bias:** What this lens prioritizes
- **verdict_style:** When it says GO/MODIFY/BLOCK

## Lenses

### CEO — Business & Strategy

- **focus:** Speed, growth, market direction, and competitive advantage
- **domains:** business, strategy, market, growth, revenue, competition, pricing, go-to-market, roadmap
- **triggers:** pricing strategy, go-to-market, roadmap prioritization, resource allocation, market direction, competitive positioning, business model, monetization, growth metrics
- **pairs_with:** CTO, CPO, YC, CFO, COO
- **default:** true
- **active:** true
- **bias:** action > perfection
- **verdict_style:** GO if it moves the needle fast, MODIFY if it's too slow, BLOCK if it misses the market window

### CTO — Technical & Infrastructure

- **focus:** Scalability, risk, system integrity, and engineering excellence
- **domains:** architecture, infrastructure, scalability, tech-debt, engineering, performance, reliability
- **triggers:** tech stack, API design, database choice, deployment strategy, refactoring, system architecture, microservices, scalability, performance optimization, technical debt
- **pairs_with:** CIO, CISO, CDO
- **default:** true
- **active:** true
- **bias:** long-term stability > short-term speed
- **verdict_style:** GO if it's maintainable, MODIFY if it needs guardrails, BLOCK if it creates unmanageable debt

### CPO — Product & User Experience

- **focus:** User value, UX, retention, and product-market fit
- **domains:** product, ux, user-research, feature-design, retention, engagement, product-market-fit
- **triggers:** user experience, feature prioritization, user flow, onboarding, engagement metrics, retention, product-market fit, user research, usability
- **pairs_with:** CXO, CEO, CCO
- **default:** true
- **active:** true
- **bias:** product quality > internal efficiency
- **verdict_style:** GO if users will love it, MODIFY if UX needs work, BLOCK if it solves the wrong problem

### YC — Startup & Fundability

- **focus:** Clarity, fundability, simplicity, and traction
- **domains:** startup, fundraising, mvp, product-market-fit, metrics, investor-readiness, growth
- **triggers:** pitch deck, investor meeting, fundraising, MVP scope, growth metrics, product-market fit, traction, unit economics, burn rate
- **pairs_with:** CEO, CPO
- **default:** false
- **active:** true
- **bias:** signal > noise
- **verdict_style:** GO if it's clear and fundable, MODIFY if it needs focus, BLOCK if it's too complex

### CIO — Information & Operations

- **focus:** Operational efficiency, internal systems, and workflow automation
- **domains:** operations, internal-systems, data-flow, tooling, process, workflow, automation
- **triggers:** workflow automation, internal tools, system integration, process redesign, operational efficiency, data pipeline, tooling choice
- **pairs_with:** CTO, CDO, COO
- **default:** false
- **active:** true
- **bias:** efficiency > feature richness
- **verdict_style:** GO if it streamlines operations, MODIFY if it adds complexity, BLOCK if it breaks existing workflows

### CDO — Data & Analytics

- **focus:** Data strategy, analytics, and measurable decision-making
- **domains:** data, analytics, ml, metrics, data-quality, data-strategy, business-intelligence
- **triggers:** data pipeline, analytics dashboard, ML model, data strategy, metrics design, data quality, business intelligence, data governance
- **pairs_with:** CTO, CIO
- **default:** false
- **active:** true
- **bias:** data-driven decisions > intuition
- **verdict_style:** GO if it's measurable, MODIFY if metrics are unclear, BLOCK if it creates data debt

### CISO — Security & Compliance

- **focus:** Security posture, compliance, and risk management
- **domains:** security, compliance, risk, access-control, data-protection, privacy, audit
- **triggers:** authentication, authorization, encryption, GDPR, SOC2, vulnerability assessment, security audit, compliance requirement, data breach, access control, penetration testing
- **pairs_with:** CTO, CIO, CDO
- **default:** false
- **active:** true
- **bias:** security > convenience
- **verdict_style:** GO if it's secure by design, MODIFY if it needs security guardrails, BLOCK if it introduces unacceptable risk

### CXO — Customer Experience

- **focus:** Customer satisfaction, support, and journey optimization
- **domains:** customer-experience, support, satisfaction, feedback, customer-journey, onboarding
- **triggers:** customer journey, support flow, NPS score, customer satisfaction, feedback loop, onboarding experience, customer retention, churn reduction
- **pairs_with:** CPO, CCO
- **default:** false
- **active:** true
- **bias:** customer satisfaction > internal convenience
- **verdict_style:** GO if customers will notice and appreciate it, MODIFY if the journey has friction, BLOCK if it degrades customer experience

### CCO — Communication & Culture

- **focus:** Team alignment, documentation, and developer experience
- **domains:** communication, culture, documentation, developer-experience, team-alignment, org-structure
- **triggers:** team alignment, documentation strategy, developer experience, org structure, team onboarding, communication process, knowledge sharing, developer productivity
- **pairs_with:** CIO, CPO, CXO
- **default:** false
- **active:** true
- **bias:** clarity > speed
- **verdict_style:** GO if it improves team clarity, MODIFY if communication needs work, BLOCK if it creates confusion

### COO — Operations & Supply Chain *(future)*

- **focus:** Operational scaling, supply chain, and process optimization
- **domains:** operations, supply-chain, logistics, process-optimization, vendor-management
- **triggers:** operational efficiency, supply chain, logistics, process redesign, vendor management, operational scaling
- **pairs_with:** CIO, CEO, CFO
- **default:** false
- **active:** false
- **bias:** process efficiency > ad-hoc solutions
- **verdict_style:** GO if it streamlines operations, MODIFY if process gaps exist, BLOCK if it creates operational bottlenecks

### CFO — Finance & Budget *(future)*

- **focus:** Financial sustainability, budget allocation, and profitability
- **domains:** finance, budget, cost, revenue, profitability, unit-economics, financial-planning
- **triggers:** budget allocation, cost analysis, pricing strategy, profitability analysis, burn rate, unit economics, financial modeling, ROI, cost optimization
- **pairs_with:** CEO, COO, YC
- **default:** false
- **active:** false
- **bias:** financial sustainability > growth at all costs
- **verdict_style:** GO if it's financially sound, MODIFY if costs need control, BLOCK if it's financially unsustainable

## Selection Algorithm (for orchestrator reference)

1. **Filter active lenses:** Only consider lenses where `active: true`
2. **Keyword match:** Scan problem description against each lens's `domains` and `triggers`
3. **Score lenses:** Count matches, rank by relevance score
4. **Apply pairing rules:** If a top lens has `pairs_with` recommendations, boost those lenses' scores by 0.5 (only if they are also active)
5. **Select top 2-4:** Pick highest-scoring lenses, minimum 2, maximum 4
6. **Fallback:** If no strong matches (all scores < 2), use lenses marked `default: true`
