# Vendor Evaluation Playbook

Use this playbook when selecting, comparing, or replacing a vendor, tool, or service provider — to make a structured, evidence-based decision rather than a gut-feel choice.

## When to Use

- You need to choose between multiple vendors or tools
- You are evaluating whether to build vs. buy
- You are considering replacing an existing vendor
- You need to justify a vendor decision to stakeholders or finance

## Process

### 1. Define Requirements

- What problem must this vendor solve?
- What are must-have vs. nice-to-have requirements?
- What are the technical, security, and compliance constraints?
- What is the budget range and procurement timeline?
- Who are the decision makers and evaluators?

### 2. Create a Shortlist

- Identify 3-5 vendors that meet the must-have criteria
- Include the incumbent (if replacing) and a build option
- Capture basic info: pricing model, target market, maturity, references

### 3. Score Against Weighted Criteria

Define criteria and assign weights (total = 100%):

| Category | Example Criteria | Typical Weight |
|----------|-----------------|----------------|
| Functional fit | Feature coverage, workflow alignment | 25-35% |
| Technical | Integration, API, scalability, performance | 15-25% |
| Security & compliance | Certifications, data handling, audit readiness | 10-20% |
| Total cost of ownership | License, implementation, maintenance, hidden costs | 15-25% |
| Vendor viability | Financial health, customer base, roadmap, support | 10-15% |
| User experience | Ease of use, learning curve, adoption friction | 5-15% |
| Implementation | Time to value, migration effort, change management | 5-10% |

Score each vendor 1-5 per criterion. Calculate weighted scores.

### 4. Evaluate Risks and Dependencies

For each vendor:

- What happens if they go out of business or raise prices?
- How difficult is it to switch away? (lock-in risk)
- Are there single points of dependency? (specific person, custom integration)
- What is the contract flexibility? (term length, exit clauses, SLA guarantees)

### 5. Run a Proof of Concept (if warranted)

- Define success criteria for the PoC before starting
- Test with real data and real workflows, not vendor demos
- Involve the people who will actually use the tool
- Time-box the PoC (2-4 weeks maximum)

### 6. Make the Decision

- Compare weighted scores, risk profiles, and PoC results
- Consider the total cost of ownership over 3 years, not year 1
- Document the rationale for the chosen vendor and the rejected alternatives
- Define the implementation plan with milestones and success criteria

## Output Pattern

```text
REQUIREMENTS
- Must-haves, nice-to-haves, constraints, budget

VENDOR SHORTLIST
- Candidates with basic profiles

SCORECARD
- Weighted criteria and scores per vendor

RISK ASSESSMENT
- Lock-in, viability, dependency, contract risks

RECOMMENDATION
- Chosen vendor, rationale, implementation plan
- Why alternatives were not selected
```
