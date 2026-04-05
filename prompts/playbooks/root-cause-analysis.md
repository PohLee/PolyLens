# Root Cause Analysis Playbook

Use this playbook when a problem, incident, or recurring failure needs explanation beyond the immediate symptom.

## When to Use

- Something broke or degraded and you need to know why
- A problem keeps recurring despite prior fixes
- You need a post-mortem or incident investigation structure
- You need to separate triggers from underlying systemic causes

## Process

### 1. Define the Problem Precisely

- What happened?
- When and where did it happen?
- Who or what was affected?
- What was the expected state?
- What was the measurable impact?

### 2. Gather Evidence

- Build a timeline of events and changes
- Collect logs, metrics, configs, witness observations, and recent change history
- Distinguish verified facts from assumptions

### 3. Apply Structured RCA

- Use 5 Whys to trace causal chains
- Use fishbone categories when causes span people, process, technology, and environment
- Keep asking past "human error" until the enabling system failure is clear

### 4. Identify Root Causes and Contributors

- Separate direct trigger, contributing factors, and root causes
- Expect multiple causes for serious failures
- Prefer evidence-backed causes over plausible stories

### 5. Convert Findings into Prevention

- Immediate corrective action
- Systemic preventive action
- Detection or monitoring improvement
- Ownership and follow-up checkpoints

## Output Pattern

```text
PROBLEM STATEMENT
- What failed and impact

CAUSAL CHAIN
- Trigger
- Contributing factors
- Root causes

PREVENTION PLAN
- Fix now
- Prevent recurrence
- Improve detection
```