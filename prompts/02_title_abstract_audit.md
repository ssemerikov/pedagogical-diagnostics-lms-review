<!-- Brief given to the title/abstract auditor. Verbatim, except that internal file paths are replaced by [bracketed descriptions] or by links to the other files in this folder; see README.md in this folder. -->

# WP02b-audit brief: second-model audit of the title/abstract screen (model: opus, effort: high)

All paths are relative to the review's working directory. Read [prompt 01](01_title_abstract_first_pass.md) first; it holds the eligibility
criteria and codes the first-pass screener (Sonnet) applied. **False exclusions are invisible later, so
your job is to protect sensitivity.**

Calibration fact: 6 known included studies were seeded blind. None was excluded, but 4 came out as
`maybe` because their abstracts do not mention LMS indicators; the original review admitted them on full
text. **Policy (binding): a `maybe` is never excluded at title/abstract stage. It goes to full text.**

## Task A: audit the excludes (`data/scopus/audit_in_excludes.jsonl`, 163 records)
This file holds every non-`OFF` exclude plus a 20% random sample of the `OFF` excludes. For each record,
decide whether the exclusion is correct under the criteria and the rule "when in doubt, do not exclude".

Write one JSON line per record:
`{"id", "audit": "uphold|overturn", "new_verdict": "exclude|maybe|pass", "code", "reason": "<=25 words", "auditor": "claude-opus-5-5 (WP02b audit)"}`

Write batch files `data/scopus/ta_audit/excl_<NNN>.jsonl`, 25 records per file. Pay special attention to:
- **NOIND:** survey-only studies. Overturn if the abstract mentions any platform or activity data, products
  or logs.
- **NONEMP:** reviews. Uphold the exclusion, but list any systematic review on LMS indicators in
  [the auditor's notes file] as a citation-chasing source.
- **E3:** check that the population really is non-HE/VET.

## Task B: prioritise the maybes (`data/scopus/audit_in_maybes.jsonl`, 146 records)
Do NOT exclude any of them. Give each a priority for full-text assessment:
- `high`: likely meets I1–I4;
- `medium`: plausible;
- `low`: probably fails at full text, e.g. a perception survey or a study unrelated to LMS indicators.

Write one line per record:
`{"id", "priority": "high|medium|low", "likely_code", "reason": "<=20 words", "auditor": "claude-opus-5-5 (WP02b audit)"}`

Write batch files `data/scopus/ta_audit/maybe_<NNN>.jsonl`, 25 records per file.

## Rules
- **Resume:** skip batch files that already exist and validate as JSON lines with the right count.
- After each batch, append `<timestamp> <task> batch NNN: uphold x / overturn y (or high/med/low counts); NEXT: ...`
  to [the auditor's progress log].
- **Stratum rule:** if you overturn more than 2 excludes within one code (for example NOIND), say so in
  the progress log and in your final reply. The orchestrator will then re-screen that whole stratum.

## Final reply (at most 8 lines)
Overturn counts by code; maybe priority counts; strata that breach the rule; and a list of review papers
useful for citation chasing.
