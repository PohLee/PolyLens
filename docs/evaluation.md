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

Rule ownership:

- `tools/brief_contract.py` interprets standard Decision Briefs for contract, consistency,
  and regression checks. Lens Position content cannot supply report sections; completion
  sections belong to the completion summary and options belong to the pending split.
  Both plain and Markdown headings work. Duplicate sections/position fields are ambiguous.
- The Harness Hook loader owns JSON/legacy-flat metadata and defaults, shared with the
  repository checker. Omitted `order`, `enabled`, and `type` mean `99`, `false`, and `markdown`.
- `tools/lens_contract.py` owns Registry field validity and paired projection regions.
  Synchronization rejects missing/duplicate/reversed markers and preserves text outside them.
- `tools/runtime_bundle.py` owns the shared resource manifest. A direct build first rejects
  stale projections, then captures one release for layout rendering, content verification,
  and installation's post-move verification. It never silently edits source projections.
  `verify_bundle` compares an existing artifact with current source; a snapshot returned by
  `build_bundle` verifies its captured release without rereading live source.

Each build also checks declared concrete runtime references. Parameterized Lens/Hook paths
are covered by inventory/metadata checks rather than guessed paths. Projection freshness
is checked against captured inputs, not a separate read of the live source tree.

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
