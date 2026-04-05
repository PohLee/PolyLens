# PolyLens Project Memory Model

This document defines how PolyLens should store durable, project-specific context so future reviews can reuse it without depending on repeated user restatement.

## Purpose

Project memory should capture information that remains useful across multiple sessions, reviews, and artifacts for the same project.

Use project memory to answer two different questions:

- What is true about this project?
- How should PolyLens behave for this project when the user does not restate defaults?

These should be stored separately.

## Memory Classes

PolyLens should use three project-specific memory classes:

1. **Project context**
   Durable facts about the company, product, strategy, constraints, and non-negotiables.
2. **Project preferences**
   Default operating instructions for PolyLens within that project.
3. **Decision history**
   Important prior decisions, rationale, and unresolved follow-ups that future reviews should not ignore.

## Storage Location

Store project-specific memory artifacts under `docs/polylens/memory/`.

Use the existing filename convention:

- `YYMMDD_slug_rN.md`
- Example: `260405_project-context_r1.md`

Recommended canonical slugs:

- `project-context`
- `project-preferences`
- `decision-history`

These files are project-scoped references, not global user memory.

## What Goes Where

### 1. Project Context

Use this file for durable facts about the project itself.

Store items such as:

- Mission and vision
- CEO or founder strategic framing
- Business model and ideal customer profile
- Product principles and success criteria
- Regulatory scope and compliance requirements
- Architecture constraints and platform commitments
- Non-negotiables such as security, brand, or reliability thresholds
- Canonical terminology that future outputs should preserve

Example:

- If the user says the CEO vision is to make PolyLens the default executive reasoning layer for high-stakes decisions, store that in project context.

### 2. Project Preferences

Use this file for how PolyLens should behave by default within the project.

Store items such as:

- Default lenses to include for certain classes of decisions
- Preferred output style or audience tone
- Required checklists before certain verdicts
- Save behavior defaults
- Preferred templates for plans, reviews, or board-style briefs
- Default bias toward speed, rigor, or risk reduction when not specified

Example:

- If the user says to always include CEO for roadmap decisions and CISO for auth or privacy reviews, store that in project preferences.

### 3. Decision History

Use this file for durable prior decisions that should shape later analysis.

Store items such as:

- Major approved decisions
- Rejected options that should not be re-proposed without new evidence
- Deferred decisions with revisit triggers
- Key rationale and tradeoffs
- Open assumptions that remain unresolved

Example:

- If the team decided to keep PolyLens as a small public skill surface with shared internals, store that in decision history so future proposals do not re-expand the public skill surface without justification.

## Decision Rule

Use this simple classification rule:

- If it describes the project, store it in project context.
- If it describes PolyLens default behavior for that project, store it in project preferences.
- If it records something already decided and still relevant, store it in decision history.

## Recommended File Templates

### Project Context Template

```md
# Project Context

## Identity
- Project: 
- Product: 
- Stage: 

## Mission
- 

## Vision
- 

## Strategic Priorities
- 

## Non-Negotiables
- 

## Constraints
- 

## Canonical Statements
- CEO mission statement: 
- CEO vision statement: 

## Source and Confidence
- Captured from: 
- Confidence: explicit / inferred
- Last confirmed: YYYY-MM-DD
```

### Project Preferences Template

```md
# Project Preferences

## Review Defaults
- 

## Lens Defaults
- 

## Checklist Defaults
- 

## Template Defaults
- 

## Save Defaults
- 

## Interaction Defaults
- 

## Source and Confidence
- Captured from: 
- Confidence: explicit / inferred
- Last confirmed: YYYY-MM-DD
```

### Decision History Template

```md
# Decision History

## Decision
- Date: YYYY-MM-DD
- Topic: 
- Status: approved / rejected / deferred

## Summary
- 

## Rationale
- 

## Tradeoffs Accepted
- 

## Revisit Trigger
- 
```

## Update Rules

Update project memory when:

- The user explicitly states durable company or product facts
- The user sets a recurring default for how reviews should be run
- A major decision changes future analysis

Do not store:

- Temporary discussion details that are only relevant to one prompt
- Weak inferences with no user confirmation when they could mislead future reviews
- Redundant copies of the same fact in multiple files

## Practical Example

If a user says:

> The CEO vision is for PolyLens to become the standard boardroom-style reasoning layer for product and engineering decisions, and we always want CEO included in roadmap reviews.

Then store:

- The vision statement in `project-context`
- The review default in `project-preferences`

Do not mix both into one undifferentiated note.