# Cost-Benefit Analysis Playbook

Use this playbook when comparing alternatives with different cost and benefit profiles — to make a financially rigorous decision that accounts for time value of money, risk, and opportunity cost.

## When to Use

- You need to choose between two or more investment options
- You need to justify a spend with financial rigor
- You are evaluating build vs. buy, in-house vs. outsourced, or tool alternatives
- You need to compare options with different timelines and cash flow patterns

## Process

### 1. Define the Alternatives

- What options are being compared? (including the "do nothing" baseline)
- What is the analysis period? (typically 3-5 years)
- What is the discount rate? (cost of capital or hurdle rate)
- What assumptions underpin each alternative?

### 2. Identify All Costs

For each alternative, enumerate:

- **Upfront costs:** purchase, implementation, training, migration
- **Recurring costs:** license, maintenance, support, hosting, personnel
- **Hidden costs:** integration effort, productivity loss during transition, opportunity cost of team time
- **End-of-life costs:** decommissioning, data migration, contract termination fees

Express all costs in present value terms using the discount rate.

### 3. Identify All Benefits

For each alternative, enumerate:

- **Revenue impact:** incremental revenue, price increases enabled, new market access
- **Cost savings:** labor reduction, efficiency gains, license consolidation, error reduction
- **Risk reduction:** avoided fines, reduced downtime, lower security exposure
- **Strategic value:** capability enablement, competitive positioning (qualitative — note separately)

Express all benefits in present value terms. Be conservative — overestimated benefits are the most common CBA error.

### 4. Calculate Financial Metrics

For each alternative:

- **Net Present Value (NPV):** Sum of discounted benefits minus discounted costs
  - NPV > 0: creates value
  - NPV < 0: destroys value
  - Compare NPVs across alternatives — highest wins

- **Return on Investment (ROI):** (Total Benefits - Total Costs) / Total Costs × 100%
  - Useful for quick comparison but ignores time value

- **Payback Period:** Time until cumulative benefits exceed cumulative costs
  - Shorter is better, but payback ignores benefits after the payback point

- **Benefit-Cost Ratio (BCR):** Total Benefits / Total Costs
  - BCR > 1: benefits exceed costs
  - Higher is better

### 5. Run Sensitivity Analysis

Test how the decision changes under different assumptions:

- What if costs are 20% higher than estimated?
- What if benefits are 20% lower than estimated?
- What if the timeline slips by 6 months?
- What if the discount rate changes?
- Which variable has the biggest impact on the outcome? (the decision driver)

### 6. Make the Recommendation

- Which alternative has the highest NPV?
- Is the result robust under sensitivity analysis?
- What are the non-financial factors? (strategic fit, risk, reversibility)
- What is the recommendation and the key assumption it depends on?

## Output Pattern

```text
ALTERNATIVES
- Options compared, analysis period, discount rate, key assumptions

COST BREAKDOWN
- Upfront, recurring, hidden, end-of-life costs per alternative (PV)

BENEFIT BREAKDOWN
- Revenue, savings, risk reduction per alternative (PV)

FINANCIAL METRICS
- NPV, ROI, payback period, BCR per alternative

SENSITIVITY ANALYSIS
- Key variables and their impact on the decision

RECOMMENDATION
- Chosen alternative, rationale, key assumption, non-financial factors
```
