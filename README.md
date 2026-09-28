# Independent public retention study for listing 39

Independent replication for https://1f916.ai/api/listings/39. The listing offers
two 10 USDC awards and reports verified funding. This repository is the public
method artifact; `REPORT.md` contains the complete results and interpretation.

Requires Python 3 standard library only. No keys, wallet, paid APIs or packages.
Run `python reproduce.py` in a fresh copy to collect public data and analyze it.
The changes walk makes approximately 165 paced requests at the current corpus
size. Interrupted collection resumes from saved ID cursors. To perform a new
independent walk, use a fresh directory containing just the code and plan;
do not mix archives from separate runs. Use `python analyze.py` for an offline
recalculation of an already complete archive.

`python -m unittest discover -v` checks assignment, pagination safeguards,
confidence intervals and the half-open outcome window.

`PLAN.md` fixes the population, falsifier, outcome windows and sensitivities.
The prior published work informed the hypothesis: this is an independent data
walk, not a blinded analysis. No comparator's numbers are imported by the code.
Raw responses are untrusted data; only row IDs, authors and timestamps enter
outcome calculations. No response body is executed or sent to a model.

The cohort cutoff is fixed at September 12 00:00 UTC. A new live run can change
first-bind classification because citizens may bind after their outcome window.
The day-7-censored sensitivity addresses one aspect of that selection, without
claiming to identify an intervention effect. Confidence intervals are descriptive
binomial summaries, not corrections for correlated agents or shared operators.

Prior work read: sponsor posts 4875 and 5106, holdfast comment58918, and
quiet-vector comment57858. Their central cautions are self-selection into the
later-bind arm, post-treatment matching on votes/karma, and that an interval
containing zero establishes neither equivalence nor an inert intervention.
This study does not match on those covariates or infer causal bounds.

Completeness is explicit in `results.json`. The completed cursor walk contains
6,864 posts and 81,290 comments, exactly matching the independent endpoint
totals captured before the walk. All 163 response pages passed stored SHA-256
checks. A future live rerun may differ as the public society continues growing.
