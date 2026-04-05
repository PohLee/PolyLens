# Data Analysis Playbook

Use this playbook when a decision depends on understanding a dataset rather than intuition alone.

## When to Use

- You have CSV, JSON, spreadsheet, SQL, or tabular data to inspect
- You need descriptive statistics, trend analysis, or anomaly detection
- You need correlations, segment breakdowns, or data-quality validation
- You need a summary a non-technical stakeholder can understand

## Process

### 1. Frame the Question

- What decision or claim is the data supposed to inform?
- What is the source, time range, and grain of the dataset?
- What key columns, entities, or measures matter?

### 2. Profile the Data

- Count rows, columns, null rates, and duplicates
- Identify column types and invalid or mixed values
- Summarize ranges, distributions, and frequent categories
- Flag obvious anomalies or missing context

### 3. Run the Right Analysis

- Numeric: mean, median, quartiles, outliers, growth, distribution shape
- Categorical: frequency tables, segment mix, concentration, cross-tabs
- Time series: trend, seasonality, change points, moving averages
- Multi-variable: correlations, grouped comparisons, cohort slices

### 4. Test Important Claims

- Use statistical tests only when the decision depends on significance
- Distinguish statistical significance from practical significance
- State assumptions and caveats when sample quality is weak

### 5. Produce Actionable Insights

For each key finding, state:

- What happened
- Why it likely happened
- Why it matters to the decision
- What action follows
- Confidence level: high, medium, or low

## Output Pattern

Use a compact structure:

```text
DATA SUMMARY
- Source and scope
- Key quality issues

FINDINGS
- Finding 1
- Finding 2

IMPLICATIONS
- Decision impact

RECOMMENDED ACTION
- What to do next
```