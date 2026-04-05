# Customer Interview Synthesis Playbook

Use this playbook when you have raw customer interview data and need to extract patterns, prioritize needs, and translate qualitative research into actionable product and strategy insights.

## When to Use

- You have conducted customer interviews, discovery calls, or usability sessions
- You need to synthesize findings from multiple interviews into patterns
- You need to identify Jobs-to-be-Done, pain points, and willingness to pay
- You need to prioritize which problems to solve first

## Process

### 1. Gather and Organize Raw Data

- Collect all interview notes, recordings, transcripts, and observations
- Note the interviewee profile for each: role, company size, segment, usage level
- Record the interview date and context (discovery, usability, churn, win/loss)
- Aim for at least 5-8 interviews per segment before synthesizing

### 2. Extract Observations

From each interview, pull out discrete observations:

- Direct quotes that capture sentiment or pain
- Behaviors observed (what they did, not just what they said)
- Workarounds and hacks they use today
- Emotional reactions (frustration, delight, confusion)
- Willingness to pay signals (what they currently spend, what they would pay)
- Decision-making process (who decides, what criteria matter)

One observation per note. Do not interpret yet — just capture.

### 3. Affinity Cluster

Group observations into themes:

- Look for patterns that appear across multiple interviewees
- Cluster related observations under theme labels
- Note how many interviewees mentioned each theme
- Separate signal (recurring across multiple people) from noise (one-off mentions)

### 4. Map to Jobs-to-be-Done

For each major theme, articulate the underlying job:

- Functional job: what are they trying to accomplish?
- Emotional job: how do they want to feel?
- Social job: how do they want to be perceived?

Format: "When [situation], I want to [motivation], so I can [outcome]."

### 5. Prioritize Problems to Solve

Score each identified problem on:

- Frequency: how many customers experience this? (1-5)
- Intensity: how painful is it when it occurs? (1-5)
- Willingness to pay: would they pay to solve it? (1-5)
- Current alternatives: how well is it solved today? (1-5, inverted — higher = worse alternatives)

Priority score = Frequency × Intensity × Willingness to Pay × Current Alternatives

### 6. Translate into Action

For each high-priority problem:

- What would a good solution look like?
- What is the smallest thing we could build to test this?
- What evidence would confirm or invalidate this as a real problem?
- Who should own the follow-up?

## Output Pattern

```text
INTERVIEW SUMMARY
- Number of interviews, segments covered, profiles

KEY THEMES
- Theme 1: [description] — mentioned by [N] of [total] interviewees
- Theme 2: [description] — mentioned by [N] of [total] interviewees

JOBS-TO-BE-DONE
- JTBD 1, JTBD 2, JTBD 3

PROBLEM PRIORITIZATION
- Problem, frequency, intensity, WTP, priority score

RECOMMENDED ACTIONS
- What to build, test, or investigate next
- What to stop doing or deprioritize
```
