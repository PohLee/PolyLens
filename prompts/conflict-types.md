# Conflict Types

The collision engine classifies disagreements between lenses into five types. Each type has a specific resolution strategy.

## Type 1: Priority Conflicts

**Definition:** Lenses disagree on what to tackle first or the order of execution.

**Example:** CEO wants to ship fast to capture market window; CTO wants to invest in infrastructure first.

**Resolution Strategy:** Time-horizon split — phase the work. Ship an MVP now (CEO's concern), but architect for the next phase (CTO's concern). Define clear milestones for when to address deferred work.

**Detection Pattern:** One lens says "do X first," another says "do Y first."

## Type 2: Scope Conflicts

**Definition:** Lenses disagree on what should be included or excluded from the solution.

**Example:** CPO wants comprehensive user onboarding; CEO wants minimal friction to reduce drop-off.

**Resolution Strategy:** Constraint resolution — identify non-negotiables from each lens, then find the smallest scope that satisfies all non-negotiables. Everything else becomes a deferred decision.

**Detection Pattern:** One lens says "must include X," another says "X is out of scope."

## Type 3: Risk Conflicts

**Definition:** Lenses disagree on the severity or likelihood of risks.

**Example:** CISO flags a security risk as critical; CEO considers it acceptable for speed.

**Resolution Strategy:** Weighted tradeoff matrix — score the risk across dimensions (impact, likelihood, reversibility, cost). If the risk is irreversible and high-impact, it's non-negotiable. If reversible, accept with mitigation.

**Detection Pattern:** One lens rates risk as HIGH, another rates it as LOW or MEDIUM.

## Type 4: Resource Conflicts

**Definition:** Lenses disagree on time, budget, or effort allocation.

**Example:** CTO wants 3 sprints for refactoring; CEO wants 1 sprint to ship.

**Resolution Strategy:** Reversible vs irreversible decision framework. If the resource allocation is reversible (can reassign later), go with the faster option. If irreversible (hiring, long-term contracts), go with the more conservative estimate.

**Detection Pattern:** One lens proposes X resources, another proposes Y resources where Y >> X or X >> Y.

## Type 5: Fundamental Conflicts

**Definition:** Lenses disagree on the core approach or direction — not just details, but the fundamental strategy.

**Example:** CEO wants to build in-house; CTO wants to buy/adopt existing solution.

**Resolution Strategy:** Escalate to user with split recommendations. Present both positions with their reasoning, tradeoffs, and consequences. The user must decide — this cannot be auto-resolved.

**Detection Pattern:** Lenses have opposing GO/BLOCK verdicts with irreconcilable reasoning.

## Conflict Classification Table

| Type | Name | Auto-Resolvable? | Escalation Threshold |
|---|---|---|---|
| 1 | Priority | Yes | If phases can't be defined |
| 2 | Scope | Yes | If non-negotiables are mutually exclusive |
| 3 | Risk | Yes | If risk is irreversible AND high-impact AND disputed |
| 4 | Resource | Yes | If resource gap > 2x and both positions are defensible |
| 5 | Fundamental | No | Always escalate to user |
