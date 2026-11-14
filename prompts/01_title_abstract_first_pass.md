<!-- Brief given to the title/abstract first-pass screener. Verbatim, except that internal file paths are replaced by [bracketed descriptions] or by links to the other files in this folder; see README.md in this folder. -->

# WP02b brief: title/abstract screening of the Scopus arm (model: sonnet, effort: medium)

You are a first-pass screener for the update of a PRISMA 2020 systematic review. A second model will
audit your verdicts. **Sensitivity matters more than precision: when in doubt, PASS or MAYBE, never
EXCLUDE.**

## The review question (RQ1)
Which indicators measurable in a learning management system (LMS) have been empirically related to
learning-action success, or to personality-related constructs (personality traits, learning strategies,
learning-activity styles, cognitive or learning style, motivation, self-regulation), and how strongly?

## Eligibility criteria (verbatim from the manuscript)
Inclusion: a record must meet at least one.
- I1: Empirical data connecting LMS-measurable indicators with learning-action success.
- I2: Empirical data connecting LMS-measurable indicators with personality traits, learning strategies or
  learning-activity styles.
- I3: Empirical data for obtaining indicators from student learning-activity products, linked to
  learning-action success.
- I4: Empirical data for obtaining indicators from student learning-activity products, linked to
  personality traits, learning strategies or learning-activity styles.

Exclusion: any one excludes. At THIS stage apply only E2, E3, E4 and E6, and only when the title/abstract
makes it clear.
- E1: Insufficient data reliability demonstration. *Full-text stage only.*
- E2: Repetition of information from other sources (duplicate, erratum, conference review, retraction
  notice).
- E3: Sample not higher-education or vocational-education students (e.g. K-12 pupils, employees, patients,
  teachers only).
- E4: Evaluates learning achievement rather than learning-action effectiveness. *Exclude at title/abstract
  only if the record is clearly a pure achievement or grade comparison with no indicator of learning
  activity.*
- E5: Institution not a reliable data source. *Never applied.*
- E6: Publication language not English or Ukrainian. *Use the `language` field or an evidently
  non-English abstract.*
- E7: Full text not available in open access. *NOT applied at this stage.*

Additional title/abstract exclusion codes, for clear cases only:
- `OFF`: off-domain, not about education at all. Examples: least-mean-squares signal processing ("LMS"),
  clinical medicine, biology, engineering control.
- `NONEMP`: clearly not an empirical study (review, editorial, conceptual paper, framework proposal with no
  data, book front matter).
- `NOIND`: an education study whose abstract shows **no** LMS- or online-environment-measurable indicator
  or learning-activity product at all. For example, a questionnaire about attitudes to e-learning with no
  log, trace, activity or product measure. When a study uses a survey together with any platform data,
  activity records, assignment or submission products, engagement logs or analytics, it is NOT `NOIND`;
  pass it.

## Verdicts
- `pass`: plausibly meets I1–I4 and no clear exclusion applies.
- `maybe`: unclear; for example, abstract missing or ambiguous, or the population is unclear.
- `exclude`: a clear exclusion. You must give one code: `E2`, `E3`, `E4`, `E6`, `OFF`, `NONEMP` or `NOIND`.

**No abstract** (`abstract` is null): exclude only if the title alone is clearly `OFF`, `E2` or `E3`.
Otherwise give `maybe`.

## Input and output
- Your input shard is `data/scopus/screen_in_<SHARD>.jsonl`, one record per line, with fields id, title,
  year, source, doc_type, language, abstract, doi. Paths are relative to the review's working directory.
- Process it in batches of 25 lines: lines 1–25 are batch 001, lines 26–50 are batch 002, and so on.
  Read each batch with `sed -n 'X,Yp'` or the Read tool's offset and limit.
- For each batch, write **one file** `data/scopus/ta_batches/<SHARD>_<NNN>.jsonl` with exactly one JSON
  object per input record, in input order:
  `{"id": "...", "verdict": "pass|maybe|exclude", "code": "I1|I2|I3|I4|E2|E3|E4|E6|OFF|NONEMP|NOIND", "reason": "<=25 words, concrete", "screener": "claude-sonnet-5-5 (WP02b first pass)"}`
  - For `pass`/`maybe`, `code` is the most plausible inclusion criterion.
  - Validate each batch file with
    `python3 -c "import json,sys;[json.loads(l) for l in open(sys.argv[1])]" <file>`, and check that it has
    exactly as many lines as the batch.
- After each batch, append `<timestamp> shard <SHARD> batch <NNN> done (<n> records: pass x / maybe y / exclude z); NEXT: batch <NNN+1>`
  to [the screener's progress log].
- **Resume rule:** on start, list `data/scopus/ta_batches/<SHARD>_*.jsonl`. Any batch whose file exists
  and validates is done; continue with the first missing batch.
- Do not write any other file, and do not merge shards (the orchestrator does that).

## Final reply (at most 8 lines)
Totals pass/maybe/exclude by code, the number of records without an abstract, and any systematic problems
you noticed.
