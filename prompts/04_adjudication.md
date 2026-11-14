<!-- Brief given to the adjudicator (second reading). Verbatim, except that internal file paths are replaced by [bracketed descriptions] or by links to the other files in this folder; see README.md in this folder. -->

# WP05b brief: independent adjudication of eligibility and extraction (model: fable, effort: high)

All paths are relative to the review's working directory. You replace the human confirmation gate (decision D2 in
[the revision's decision log]): the paper will report that the update's decisions were made by two language models
(first pass plus your independent adjudication) without author verification. Your verdicts set what
enters the paper's Table 2. **Be independent, be exact, and record your reasons.**

Criteria: read [prompt 01](01_title_abstract_first_pass.md) (I1–I4, E1–E7) and [prompt 03](03_fulltext_assessment.md) (full-text rules, the `NOREL`
code, the extraction schema).

## Part A: every full-text assessment (`data/ft/assess/<id>.json`)
For each assessed record:
1. **Blind first.** Open the full text `data/fulltext/<id>.txt` (or `.html`) and decide eligibility
   yourself, **before** reading the assessor's decision fields. Write down your independent decision and
   code.
2. Then read the assessor's file and compare.
   - Where you agree, `final_decision` = the shared decision.
   - Where you disagree, re-read the decisive passage and decide. Give `final_decision` with a written
     reason that quotes the decisive sentence.
3. **Check the extraction.** For every number in `extraction` (`n` and each effect size), confirm that
   the quoted sentence occurs verbatim in the full text, for example with
   `rg -F "<short distinctive substring>" data/fulltext/<id>.txt`, and that the value matches it. Correct
   wrong values, and mark them `corrected`.
   - For re-extraction records (ids are bib keys), also compare against `table2_current` and list every
     cell that should change.

Write `data/ft/adjudicate/<id>.json`:
```
{"id", "independent_decision": "include|exclude", "independent_code", "assessor_decision", "agree": true|false,
 "final_decision": "include|exclude", "final_code", "reason": "<=60 words; quote the decisive sentence when you disagree",
 "extraction_check": {"n": "ok|corrected|nr_confirmed", "n_value": ..., "effect_sizes": [{"value", "status": "ok|corrected|not_found", "quote"}],
                      "table2_changes": [{"column", "from", "to", "quote"}]},
 "adjudicator": "claude-fable-5-2 (WP05b)", "adjudicated_on": "YYYY-MM-DD"}
```

## Part B: a sample of the title/abstract exclusions
Take `data/scopus/ta_audit_sample_for_fable.jsonl` if it exists. If not, draw a 10% random sample (seed
20261112) of the non-`OFF` excludes in `data/scopus/ta_verdicts.jsonl` and the shard C batches. For each
record, say whether you uphold the exclusion. Write `data/ft/adjudicate_ta_sample.jsonl` with one line
per record: `{"id", "uphold": true|false, "reason"}`.

## Rules
- **Resume:** skip ids whose adjudication file already exists and validates.
- Append `<timestamp> <id> agree=<bool> final=<decision>; NEXT: <id>` to [the adjudicator's progress log] after each
  record.
- Do not edit any assessor file. Write only under `data/ft/adjudicate*` and [the adjudicator's notes folder].

## Final reply (at most 8 lines)
Agreements and disagreements, final includes and excludes, extraction corrections, Table 2 changes, and
the Part B uphold rate.

## Additions (orchestrator, 2026-11-12 23:10)
- **Shared decision rules.** The full-text assessors apply the decision rules in the header of
  [the main full-text assessor's progress log (its decision-rule header is prompt 03b)](03b_fulltext_decision_rules.md): include rule, E4 vs NOREL boundary, precedence order. Judge against the same
  rules. If you think a rule itself is wrong, say so in [the adjudicator's rule notes (prompt 05)](05_adjudicator_notes_on_rules.md); do not silently apply a
  different rule.
- **Incremental running.** Assessors are still writing new files (worklists manualA and manualB).
  1. Process every assess file present when you start.
  2. Re-list `data/ft/assess/` and process any new ones. Repeat until a re-list finds nothing new.
  3. Then do Part B and stop.
  The resume rule (skip ids already adjudicated) makes re-runs safe.
- **Part C: the 10 originally included studies** (re-extraction records, whose ids are bib keys). The
  assessor reports that on full text only 3 of the 10 (kolgatin2020systematicity, farameita2025integration,
  hsueh2022exploring) meet any of I1–I4 under the rules above.
  - **The original January 2026 inclusion decisions are NOT changed** (decision D8: reported as made).
  - Give an independent sensitivity judgement for each of the 10. Add this to its adjudicate file:
    `"sensitivity": {"criteria_met": [...], "meets_update_rules": true|false, "decisive_quote": "...", "note": "<=40 words"}`
  - Do these 10 FIRST. They decide what the paper says about the evidence base (R7.4), and the user will
    choose how to report them.
