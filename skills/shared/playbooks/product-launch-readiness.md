# Product Launch Readiness Playbook

Use this playbook before any product, feature, or service launch — to verify readiness, identify gaps, and make a structured go/no-go decision.

## When to Use

- You are about to launch a product, feature, or major update
- You need a go/no-go checkpoint before releasing to customers
- You need to ensure all teams (product, engineering, marketing, support, sales) are aligned
- You need to identify last-minute risks before committing to a launch date

## Process

### 1. Verify Product Readiness

- Is the feature complete against the launch scope?
- Has QA sign-off been completed? What is the bug status?
- Are there any known issues or limitations to disclose?
- Is performance tested against expected load?
- Is the feature accessible and compatible across supported platforms?
- Is there a rollback plan if something goes wrong?

### 2. Verify Go-to-Market Readiness

- Is the messaging framework complete and approved?
- Are marketing assets ready (landing page, blog, email, social, ads)?
- Is the launch timeline finalized with dependencies mapped?
- Are press, analyst, or influencer briefings scheduled?
- Is the pricing and packaging finalized and communicated?

### 3. Verify Sales and Support Readiness

- Is the sales team trained on the new feature and messaging?
- Are sales enablement materials ready (deck, demo, battle cards, FAQ)?
- Is the support team trained with runbooks and troubleshooting guides?
- Are support channels staffed for expected volume spike?
- Are customer success managers briefed for proactive outreach?

### 4. Verify Technical and Operational Readiness

- Is monitoring and alerting configured for the new feature?
- Are dashboards and metrics in place to track adoption and health?
- Is the deployment plan documented with rollback procedures?
- Are dependencies (APIs, third-party services, infrastructure) confirmed ready?
- Is there an incident response plan specific to this launch?

### 5. Verify Legal and Compliance Readiness

- Are terms of service, privacy policy, and documentation updated?
- Are there regulatory or compliance implications to address?
- Are contracts or SLAs updated if the launch changes service levels?
- Is intellectual property protected (patents, trademarks if applicable)?

### 6. Make the Go/No-Go Decision

Score each area: Ready, Ready with Risks, or Not Ready.

| Area | Status | Open Items | Risk Level |
|------|--------|------------|------------|
| Product | [status] | [list] | [low/med/high] |
| GTM | [status] | [list] | [low/med/high] |
| Sales & Support | [status] | [list] | [low/med/high] |
| Technical & Ops | [status] | [list] | [low/med/high] |
| Legal & Compliance | [status] | [list] | [low/med/high] |

Decision rules:
- **GO:** All areas Ready or Ready with Risks (low risk only)
- **CONDITIONAL GO:** One area Ready with Risks (medium risk) with mitigation plan and owner
- **NO-GO:** Any area Not Ready, or multiple medium-risk items without mitigation

## Output Pattern

```text
LAUNCH READINESS SUMMARY
- Product, GTM, Sales/Support, Technical/Ops, Legal/Compliance status

OPEN ITEMS AND RISKS
- Item, owner, risk level, mitigation

GO / NO-GO DECISION
- Decision and rationale
- Conditions (if conditional go)
- Blockers (if no-go)

POST-LAUNCH MONITORING PLAN
- Key metrics, alert thresholds, escalation path, review cadence
```
