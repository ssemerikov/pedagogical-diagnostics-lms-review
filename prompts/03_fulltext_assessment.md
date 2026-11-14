<!-- Brief given to the full-text assessors. Verbatim, except that internal file paths are replaced by [bracketed descriptions] or by links to the other files in this folder; see README.md in this folder. -->

# WP02d brief: full-text eligibility assessment and data extraction (model: opus, effort: xhigh)

All paths are relative to the review's working directory. Your outputs go into Table 2 of the paper and into a public
dataset, and an independent model (Fable) re-checks every decision. **Be exact: quote, don't paraphrase,
for every extracted number.**

## The review question and criteria
Read the RQ1 text and the criteria in [prompt 01](01_title_abstract_first_pass.md) (I1–I4, E1–E7).

At full text:
- apply **all** of I1–I4 and E1–E6;
- E7 (no open-access full text) does not arise for records you are given;
- E5 is never applied;
- E1 ("insufficient data reliability demonstration") applies only when the study gives no information at
  all from which the reliability of its data or measures could be judged. Say what is missing.

The original review's commonest full-text exclusion was "does not report the indicator–outcome data the
inclusion criteria require". Use code `NOREL` for it: the study has an LMS indicator but reports no
empirical relation to learning-action success or to a personality-related construct, or it reports only
self-reported perceptions.

## Input
- A worklist file `data/ft/worklist_<NAME>.jsonl`, given in your prompt. Each line has
  `{"id", "arm", "doi", "title", "fulltext_file"}`.
- The full text is in `data/fulltext/<id>.txt` (PDF text) or `.html`. If the text is unusable (scanned,
  empty, or the wrong paper), record `decision: "unusable_fulltext"` with the reason.

## Output: one file per record, `data/ft/assess/<id>.json` (written immediately)
```
{"id", "arm", "doi", "title",
 "decision": "include|exclude|unusable_fulltext",
 "criteria_met": ["I1",...],
 "exclusion_code": "E1|E2|E3|E4|E6|NOREL|NONEMP|null",
 "reason": "<=40 words",
 "extraction": {                       // fill for includes, and for excludes where cheap
   "country": "... or nr",
   "design": "e.g. correlational | quasi-experimental | experimental/control | case study | mixed | PLS-SEM | CFA",
   "n": "integer or nr",
   "n_quote": "verbatim sentence giving n, or null",
   "population": "e.g. undergraduate engineering students, 1 university",
   "lms_indicators": "the LMS-side or activity-product indicators actually measured",
   "outcome_or_construct": "learning-action success measure, or the personality/style/strategy/SRL construct",
   "effect_sizes": [{"statistic": "r|beta|d|eta2|R2|OR|...", "value": "...", "between": "indicator ↔ outcome", "quote": "verbatim", "location": "page or section/table"}],
   "notes": "anything relevant to RQ1, e.g. 'effect reported only as p<.05'"
 },
 "assessor": "claude-opus-5-5 (WP02d)", "assessed_on": "YYYY-MM-DD"}
```
- `nr` means not recoverable from the text. **Never estimate or compute an effect size the paper does not
  report.**
- Record exactly the statistic the paper gives.

## Resume rule
On start, list `data/ft/assess/`. Any id already present and valid as JSON is done.

## Progress
After each record, append `<timestamp> <id> <decision> <code>; NEXT: <next id>` to
[the assessor's progress log].

## Re-extraction mode (worklist `reextract`)
For the 10 already-included studies (ids are bib keys), do **not** re-decide inclusion. Fill `extraction`
only, set `"decision": "include"` and `"criteria_met"` as you find them, and add
`"table2_current": {...}`, copied from the paper's Table 2 row in [the manuscript's literature-review section], so
that changed cells are visible. Pay special attention to the cells that currently say "nr" (n, country,
effect size).

## Final reply (at most 8 lines)
Counts: include, exclude by code, unusable; plus paths.
