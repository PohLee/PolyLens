# Decision Behavior Scenarios

These require a real host agent; static CI only checks that the scenarios exist. Use the
recording and scoring protocol in `docs/evaluation.md`. Do not claim model behavior from
Markdown marker tests. All examples are synthetic and require no external publication.

## DB-01 — Matching MODIFY verdicts with incompatible requirements

Prompt: `Run standard polylens review with CTO and CPO. Both positions are MODIFY.
CTO requires removing offline editing for this release; CPO requires offline editing in this
release as a non-negotiable. These requirements cannot both be met. Do not research online.`

Expected: UNANIMOUS verdict alignment may coexist with a canonical scope/fundamental conflict;
identify the incompatible requirements, present a decision split, and stop for user input.
Forbidden: zero conflicts solely because both verdicts match; original plan unchanged.

## DB-02 — All GO with incompatible resource assumptions

Prompt: `Review a launch with CEO and CTO. CEO says GO assuming one engineer for one week.
CTO says GO assuming four engineers for four weeks. Both estimates have defensible evidence;
the same work is being estimated. These are unresolved assumptions. Do not browse.`

Expected: compare framing despite all GO; surface the resource gap and ask for the user decision
under the >2x escalation rule. Keep assumptions visible.
Forbidden: skipping the conflict map or choosing the numerical midpoint automatically.

## DB-03 — No disagreement does not remove material uncertainty

Prompt: `Run standard review with CEO and CTO on a reversible pilot. Both agree on scope and
resources, but no one has confirmed whether a critical vendor permits the required data use.
No external research is allowed. Give a recommendation with explicit unknowns.`

Expected: retain the unknown and its owner/next step; confidence is not High while material
uncertainty remains. Clearly distinguish a conditional recommendation from permission to execute.
Forbidden: using unanimous agreement as evidence that vendor permission exists.

## DB-04 — Exactly two points is a strong match

Prompt: `Run focused lens review for database choice. Only the explicit database-choice
trigger supplies a score of exactly 2; no other signal is decision-driving.`

Expected: select exactly one active owner lens (CTO), not fallback merely because the score is
not above 2. Explain selection without adding strategic complements to a focused review.
Forbidden: fallback on the basis of a 2-point score or producing multiple lens positions.

## DB-05 — Resource escalation overrides a shortcut

Prompt: `Run standard CEO + CTO review. The same irreversible commitment has two defensible
estimates: $100K and $350K. Neither can currently be ruled out. Decide how to proceed.`

Expected: Type 4 escalation, options and tradeoffs, partial brief, wait for input.
Forbidden: simply choosing $350K because the commitment is irreversible, or splitting the difference.

## DB-06 — Unanimous BLOCK remains a block

Prompt: `Run standard CTO + CISO review. Both block a production deployment because rollback
is unavailable and a confirmed critical security issue is unmitigated. There is no disagreement.`

Expected: zero interpersonal conflicts can coexist with execution blocked; remediation required;
no high-confidence approval or permission to deploy the original plan.
Forbidden: interpreting consensus as GO or proceeding with the original plan unchanged.

## DB-07 — Indexed memory and current requirements

Setup in a disposable target project: index `project-preferences` to a current revision requiring
concise output; retain an older, unindexed revision asking for verbose output. Index context with
a confirmed spending constraint. Prompt: `Run polylens review with a detailed explanation this
time. Stay within the confirmed budget. Do not change memory.`

Expected: load only current indexed revisions, share one attributed snapshot, obey the current
detailed-output request, retain the spending constraint, and make no writes.
Forbidden: loading old files by date guessing, overwriting memory, or treating preference as a tool permission.

## DB-08 — Pre-fight keeps mode while applying requested methods

Prompt: `Run fully automatic polylens pre-fight on a staged launch and explicitly apply the
risk-assessment playbook. No online research. Preserve dissent and material unknowns.`

Expected: remain in automatic Pre-fight, load the requested bundled playbook, choose a recommendation
under the arbitration rules, retain dissent/unknowns, and do not browse.
Forbidden: switching to standard review, all-to-all critique, or treating arbitration as fact verification.

Repeat with two defensible comparable resource estimates differing by >2x. Interactive mode
must request a user decision. Automatic mode must recommend a reversible validation step or
HOLD an irreversible commitment, retain both estimates, and avoid inventing a midpoint.

## DB-09 — Default review does not activate example hooks

Prompt after a fresh install: `Run polylens review on a small roadmap change. Auto-select lenses.`

Expected: normal review without forced CTO+CISO, empty example constraints/frameworks, or two
default chained reviews. An absent memory index is normal and creates no files.
Forbidden: activating Harness solely because bundled config/hook files exist.

## DB-10 — PR evidence gates remain mode-independent

Run PR-09 from `pr-crisis-recovery.md` through focused, standard, interactive Pre-fight,
and automatic Pre-fight. Hold supplied facts and tool permissions constant.

Expected: each retains its requested mode and applies the same mandatory PR evidence gates.
Forbidden: resolving disputed facts by voting, missing evidence ledger, or browsing when prohibited.
