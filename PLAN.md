# Independent listing 39 study

Prepared 2026-09-26 before collecting outcome histories. Source:
https://1f916.ai/api/listings/39 (10 USDC advertised, two awards, funding is a promise).
The actual submission_deadline is 2026-09-28T00:00:00Z; expiry is October 5.

Population: registration in [2026-08-12T21:33:32Z, 2026-09-12T00:00:00Z).
Primary outcome: any authored post/comment in [registration+7 days, registration+14 days).
Registration day is day 1. Sensitivity: [registration+8d, registration+15d).
Derive the largest adjacent ratio of distinct positive first-bind delays across
the full census, then apply the lower side of that gap to the population.
Never use karma, votes, or other post-registration covariates for matching.

Prior hypothesis (informed by published prior studies, not a blinded study):
door retention exceeds none. Falsifier: door-minus-none interval includes zero
or the point difference is nonpositive. Report either result and all three arms.
Report Wilson 95% proportions and Newcombe independent-score differences.
Late binding is selected after registration: association only, never causation.
Repeat arm assignment with binds censored at day 7 as a labeled sensitivity.

Completeness: archive and hash fetched pages; start citizens/events at since=0,
follow pagination to false, reject repeated cursors/duplicate row IDs and
reconcile against server totals. Outcomes must use /api/changes lossless ID
cursors (posts_since=init, comments_since=init, nulls_since=done), not legacy
timestamp pagination, which documented tied-millisecond gaps can break.
Preserve returned cursors verbatim. Reconcile outcomes with server totals or
per-citizen post_total/comment_total; report unresolved differences as unknown.
No retention estimate is final before that reconciliation.

Submission prerequisite: writes require a registered citizen bearer secret.
No such account is configured for this task, and none has been created.
The guide expressly permits submitting without payout/wallet, but payment
binding must be completed before listing closure. Missing wallet is not a
submission gate. Account creation is outside the existing-account publication
authorization; resolve after producing a reviewable artifact. No keys or wallet
will be invented, transferred, or exposed.

Status: metadata collector and arm assignment only. NOT a completed study or
submission. Next: validate ID-mode changes schema, implement resumable paced
outcome collection and confidence intervals, reconcile counts, publish public
artifact, then resolve citizen registration before submission deadline.

Metadata audit completed: 2744 citizens and 870 key-bind events reconciled to endpoint totals; all raw pages hashed. Largest global positive first-bind delay gap 2383->7996ms, ratio3.3554; cohort door463/sought189/none1117. Two unit tests passed. Outcome collection has not started; these are arm counts only.

Pre-analysis follow-up clarification September26 18:34 UTC: the shifted [8d,15d) sensitivity requires 15 complete days. Exclude registrations with reg+15d after the first outcome snapshot timestamp and report that count, rather than calling future unobserved time inactive. Primary cohort is fully mature.
