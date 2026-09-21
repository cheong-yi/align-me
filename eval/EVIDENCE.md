# Evidence and limits

This package is a new portable split of an earlier alignment skill. Its golden
cases are wholly synthetic authoring examples, not redacted or captured
transcripts. No fresh cross-harness model evaluation was run for this package.

## Accepted historical evidence

Only the accepted baseline, source archive, Gen12–Gen14 refinement, and text-first
rerun summaries informed this note. No parked delegated/control-plane material is
included. Public descriptive report IDs replace local packet identifiers; raw
source snapshots, private mappings, transcripts, and internal paths are omitted.
The summaries are not a publicly reproducible benchmark dataset.

| Report | Original result and scope |
| --- | --- |
| Baseline comparison | Six fixed scenarios, three independent paired response runners, two blind judges. Reported candidate mean 4.625; canonical mean 4.133. Mapped outcomes: candidate 9, canonical 1, ties 2. These are mapped outcome units, not twelve independent scenarios. Directional local-lab comparison only. |
| Source archive | Byte-preserving source/fixture archive; not a new evaluation. |
| Gen12–Gen14 refinement | Gen12 NEEDS_PATCH; Gen13 PASS after fixture correction; Gen14 PASS for a bounded textual regression. Gen13 had one completed review and one interrupted review explicitly recorded as incomplete, not a pass. Gen14 had one independent exact-file reviewer. |
| Text-first rerun | Three of three blind reviewers returned PASS for local source/fixture consistency: semantic alignment content remains in assistant text rather than a selection tool. No live tool-routing guarantee. |

Historical Gen14/text-first used a **0–5 ordinary-question target** (six as an
exceptional ceiling). The current source instead generally asks **two qualifying
independent questions**, with a third only when earned. **Historical PASS does not
transfer to the current two-question default or this new main/reference split.**
The baseline comparison also identified high-risk/dependent-question bundling as
a weakness; the later textual reviews are not a fresh behavioral comparison.

The machine-readable [historical summary](results/historical-summary.json) records
`current_package_evaluated: false`. This means no new model-behavior evaluation;
it does not mean local repository validation was omitted.

## Local checks

[Golden cases](golden_cases.json) specify expected and prohibited behavior for
manual semantic review. They do not contain model outputs or measured passes.
`python3 -B eval/check.py` checks this repository's restricted plain frontmatter,
file allowlist, local links, JSON structure, coverage tags, historical evidence
boundary, and broad privacy indicators. It is not a general YAML validator or a
semantic interview evaluator. `python3 -B -m unittest discover -s tests` exercises
positive and negative checker inputs without network or model calls. Tests use
and remove temporary trees inside the checkout.

Human review must still inspect all published prose/data for private details,
unsupported claims, and contract drift. Detection patterns cannot prove complete
anonymity or catch every identifier. Checker source and tests contain synthetic
privacy-pattern probes; those are not real identities or credentials.

The format was checked against the official [Agent Skills specification](https://agentskills.io/specification),
using its official GitHub source (`docs/specification.mdx`, blob
`d9a2db099d905da8b879a5c6f996728073985279`). The local checker deliberately supports
only this package's three plain frontmatter fields; it is not the official
`skills-ref` validator.

## Claim ceiling

These materials support bounded historical directional/textual observations and
current structural checks only. They do not establish cross-harness parity,
model compliance, reduced fatigue, user outcomes, statistical significance,
runtime enforcement, production readiness, or adoption readiness. Portable format
and absence of a host-specific dependency are design properties, not integration
test results. All selections remain informational and non-authorizing.
