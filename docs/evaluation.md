# Verification and Behavior Evaluation

## What the automated checks establish

Run from a clean checkout with Python 3.11+:

```bash
python tools/sync_playbooks.py --check
python tools/validate_markdown_contracts.py
python -B -m unittest discover -s tests -v
```

These establish resource/projection consistency, instruction contracts, configuration handling,
CLI exit status, standard brief structure, baseline structure/content drift, and isolated build/install behavior. Tests install
only into temporary directories; they do not alter personal skill directories or invoke models.
Output directories under `docs/polylens/` are created only when an artifact is saved.

`tools/runtime_bundle.py` owns the shared resource manifest. Both release layouts use it,
and each build checks declared concrete runtime references. Parameterized lens/hook paths
are covered by inventory/metadata checks rather than guessed paths.

## What they do not establish

Static instruction checks do not show that an AI follows the instructions. Format checks do
not establish factual accuracy, independent evidence, or decision quality. A valid partial brief
means the review properly stopped for input, not that the plan is approved. The legacy
`quality_gate` setting emits advisory format hints only.

## Repeatable manual behavior evaluation

Use [decision scenarios](../tests/fixtures/decision-behavior.md) and the existing
[PR crisis scenarios](../tests/fixtures/pr-crisis-recovery.md). Run only in a user-authorized
host/model session. There is no model API key requirement or model invocation in CI.

For each scenario:

1. Record repository commit, source/bundle layout, host and version, provider/model, model
   settings, exact prompt, tools permitted, and indexed project memory (or its absence).
2. Start fresh context with the installed public skill; retain the exact raw response and
   tool transcript. For multi-turn scenarios, retain every turn in order.
3. Compare against each observable expected/forbidden behavior, not exact prose.
4. Record each criterion as PASS / FAIL / INCONCLUSIVE with quotations from the response.
   A missing tool capability or ambiguous criterion is INCONCLUSIVE, not a pass.
5. If comparing revisions, hold host/model/settings/context constant. Preserve repeated runs
   and report disagreement across runs; do not select only the best response.

Save user-requested evaluation artifacts under
`docs/polylens/notes/YYMMDD_behavior-evaluation_rN.md` with raw responses linked from the report.
Do not publish user data, credentials, or private transcripts without authorization.

### Initial execution status

The scenarios are an evaluation plan, not a recorded quality result. They have **not** been
executed against an external model as part of this change. Fill in results only from actual runs.
