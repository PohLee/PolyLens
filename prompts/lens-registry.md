# Lens Registry

Each lens declares its metadata for context-aware selection. The orchestrator reads this file to automatically select the 2-4 most relevant lenses based on problem context.

Selection should be deterministic. If two lenses are equally plausible, prefer the one with the stronger trigger match, then the closer user wording match, then the stronger default signal, then registry order.

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
- **pairs_with:** CTO, CPO, YC, CFO, COO, CBDO
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
- **pairs_with:** CXO, CEO
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

### CXO — Customer Experience & UI/UX Design

- **focus:** Customer satisfaction, UI/UX design quality, support, and journey optimization
- **domains:** customer-experience, ui-design, ux, accessibility, design-system, support, satisfaction, feedback, customer-journey, onboarding, visual-design, interaction-design
- **triggers:** customer journey, UI design, UX review, support flow, NPS score, customer satisfaction, feedback loop, onboarding experience, customer retention, churn reduction, visual design, accessibility, design system, wireframe, mockup
- **pairs_with:** CPO
- **default:** false
- **active:** true
- **bias:** customer satisfaction > internal convenience
- **verdict_style:** GO if customers will notice and appreciate it, MODIFY if the journey has friction, BLOCK if it degrades customer experience

### COO — Operations & Supply Chain

- **focus:** Operational scaling, supply chain resilience, process optimization, and vendor management
- **domains:** operations, supply-chain, logistics, process-optimization, vendor-management, capacity-planning, quality-assurance, business-continuity
- **triggers:** operational efficiency, supply chain, logistics, process redesign, vendor management, operational scaling, capacity planning, quality assurance, business continuity, incident response
- **pairs_with:** CIO, CEO, CFO, CAgO
- **default:** false
- **active:** true
- **bias:** process efficiency > ad-hoc solutions
- **verdict_style:** GO if it streamlines operations, MODIFY if process gaps exist, BLOCK if it creates operational bottlenecks

### CMO — Marketing, Brand & Growth Acquisition

- **focus:** Brand strategy, customer acquisition, marketing ROI, and growth marketing
- **domains:** marketing, brand, acquisition, content-strategy, growth-marketing, seo, paid-advertising, social-media, market-positioning
- **triggers:** marketing campaign, brand strategy, customer acquisition, content marketing, SEO strategy, social media, paid advertising, brand positioning, growth marketing, marketing budget, go-to-market messaging
- **pairs_with:** CEO, CXO, CBDO
- **default:** false
- **active:** true
- **bias:** measurable growth > brand awareness
- **verdict_style:** GO if it drives measurable acquisition, MODIFY if channels or messaging need refinement, BLOCK if marketing spend lacks feedback loops

### CBDO — Partnerships, Revenue Channels & Strategic Alliances

- **focus:** Strategic partnerships, channel strategy, revenue diversification, and market expansion
- **domains:** partnerships, alliances, channel-strategy, revenue-diversification, market-expansion, joint-ventures, distribution, co-marketing
- **triggers:** partnership agreement, strategic alliance, channel strategy, revenue diversification, market expansion, joint venture, distribution deal, co-marketing, reseller agreement, platform integration partnership
- **pairs_with:** CEO, CMO, CFO
- **default:** false
- **active:** true
- **bias:** strategic leverage > revenue volume
- **verdict_style:** GO if the partnership creates asymmetric value, MODIFY if terms or integration need work, BLOCK if incentives are misaligned or channel conflict is high

### CFO — Financial Sustainability & Capital Strategy

- **focus:** Financial sustainability, budget allocation, capital efficiency, and profitability
- **domains:** finance, budget, cost, revenue, profitability, unit-economics, financial-planning, capital-structure, fundraising
- **triggers:** budget allocation, cost analysis, pricing strategy, profitability analysis, burn rate, unit economics, financial modeling, ROI, cost optimization, fundraising, capital raise, financial planning
- **pairs_with:** CEO, COO, CBDO
- **default:** false
- **active:** true
- **bias:** financial sustainability > growth at all costs
- **verdict_style:** GO if it's financially sound, MODIFY if costs need control, BLOCK if it's financially unsustainable

## Selection Algorithm (for orchestrator reference)

1. **Filter active lenses:** Only consider lenses where `active: true`
2. **Score explicit wording:** Exact or near-exact matches against `triggers` score +2; domain/theme matches score +1
3. **Rank by relevance:** Sum the scores and keep a note of which user constraints each lens covers
4. **Apply pairing rules:** If a top lens has `pairs_with` recommendations, boost those lenses' scores by 0.5 (only if they are also active)
5. **Prefer coverage:** Select 2-4 lenses that cover the prompt's main business, product, technical, operational, financial, or risk themes rather than stacking near-duplicates
6. **Break ties deterministically:** Use this order: stronger trigger match, more direct user wording match, `default: true`, registry order
7. **Fallback:** If no strong matches (all scores < 2), use lenses marked `default: true`
