<!-- Notes written by the adjudicator on how it applied the rules (its own output). Verbatim, except that internal file paths are replaced by [bracketed descriptions] or by links to the other files in this folder; see README.md in this folder. -->

# WP05b rule notes (adjudicator: claude-fable-5-2)

## 1. Blinding: what was and was not blind
- **Not strictly blind (main worklist).** While reading the shared decision rules I printed the first 60
  lines of [the main full-text assessor's progress log (its decision-rule header is prompt 03b)](03b_fulltext_decision_rules.md), which list the assessor's decision and code for about 50
  main-worklist ids. I did not open that file again. For those ids my decision is still taken from the
  full text first and written down before the assess file is opened, but I had seen the assessor's code.
- **Not blind (Part C, three ids).** The brief names the three studies the assessor found to meet the
  rules (kolgatin2020systematicity, farameita2025integration, hsueh2022exploring).
- Everything else (manualA, manualB, OUCI ids) was decided before the assess file was opened.

## 2. Part C convention (the 10 originally included studies)
- `final_decision` is `include` for all ten: decision D8 keeps the January 2026 decisions as made.
- `independent_decision` / `independent_code` hold my **sensitivity** verdict under the update rules
  (include = meets the rules; otherwise the exclusion code that would apply).
- `agree` compares my sensitivity verdict with the assessor's `criteria_met` (empty = fails).
- These ten carry `"part": "C"` and are **not** counted in the Part A agreement figures or in the list of
  final includes of the update.

## 3. Part C result
3 of 10 meet the update rules: kolgatin2020systematicity (I1), hsueh2022exploring (I1, I3),
farameita2025integration (I1, with an E3 caveat). The other seven fail:
bykonia2019teaching (NOREL), bykova2021blended (NOREL), herrera2024metaphorical (NOREL),
udin2022self (NOREL), ferdiansyah2025assessing (E4), savchuk2019interactivity (E4),
suwardika2024flipped (E4). My verdict matches the assessor's on all ten; on savchuk the hypothetical code
differs (E4 vs the assessor's NOREL), which has no effect because the decision is not changed.

## 4. Is the update rule stricter than the January criteria?
Yes, in practice. I1-I4 as worded ask for "empirical data connecting LMS-measurable indicators with"
success or a construct. The update's include rule operationalises this as a per-student,
platform-recorded measure (or scored activity product) entering an analysis, and says group membership
is not an indicator. The seven failing studies appear to have been admitted in January on a looser reading:
an intervention delivered through a digital environment, with achievement or self-report outcomes. I think
the update rule is the correct reading of I1-I4 and I applied it unchanged. The consequence for the paper
is that the two arms of the review were not screened to the same operational standard, which should be
stated.

## 5. E3 and trainees (farameita2025integration)
The sample is "200 participants from various Indonesian government institutions" in a one-month
professional training programme. [prompt 01](01_title_abstract_first_pass.md) lists "employees" under E3; the shared rule in
[prompt 03b](03b_fulltext_decision_rules.md) says trainees are decided on other criteria. I followed the shared rule and counted
the study as meeting I1, with the caveat recorded. A strict reading of E3 would leave only 2 of 10.

## 6. Table 2 errors found in Part C (not just empty cells)
- ferdiansyah2025assessing: n is 35, not 60; design is single-group pre/post, not correlational; no
  activity records are analysed.
- udin2022self: no log analysis exists; the listed indicators are questionnaire items.
- farameita2025integration: "object-interaction frequency" does not occur in the text; design is not CFA.
- hsueh2022exploring: no clustering is performed.
- bykonia2019teaching: no control group.

## 7. Part A notes (added while adjudicating)
- **Two update records are originally included studies.** `2-s2.0-85073395065` = savchuk2019interactivity
  and `2-s2.0-85073683089` = bykonia2019teaching (same DOIs). The assessor excluded both at full text. They
  should leave the update flow as duplicates of already-included reports; otherwise the paper would list the
  same publication as included (original review) and excluded (update). Flagged in their adjudicate files
  (`duplicate_of_original_include`).
- **Same study, two reports.** `2-s2.0-84993953291` (IJDET 2017) and `2-s2.0-84994219912` (TOJDE 2016) report
  the same samples and tables. The assessor included the first and excluded the second as E3, which cannot
  both be right. Final: the first is included (I4), the second is E2.
- **E3 with no human sample.** The assessor used E3 for studies with no student sample. I kept E3 where the
  only human sample is non-students (`2-s2.0-105019297225`, experts) and used NOREL where there is no human
  sample at all (`2-s2.0-105038603936`, software agents). Code-only change.
- **Extraction checks on excluded records.** Every number the assessor extracted was checked mechanically
  (quote found in the full text after whitespace normalisation, value present in the quote) and by hand where
  the mechanical check failed. Where the assessor gave `nr` for an excluded record I did not search for n;
  those are marked `nr_unverified`. They do not enter Table 2.
- **Wrong full text (superseded, see section 10).** `2-s2.0-84865086835`: the first saved file was another paper by the same author. Status
  `unusable_fulltext` is kept; my blind exclude was made before I noticed the mismatch.
- **E4 versus NOREL.** The boundary is the least stable part of the shared rules. I applied the written
  clarification literally: an intervention or group-comparison design with an achievement outcome and no
  per-student activity measure in any analysis is E4, even when self-report scales are also analysed. This
  moved a few records from the assessor's NOREL to E4 (`code_agree: false`). None of these changes affects
  an inclusion decision. If the paper reports exclusion reasons, E4 and NOREL could be reported together as
  "no indicator-outcome data" without loss.
- **E3 and trainees, again.** `2-s2.0-85204875563` (working chemists) is excluded on other grounds; like
  farameita2025integration it shows that the shared E3 rule lets employee trainees through.

## 8. Part B (title/abstract exclusion sample)
- `data/scopus/ta_audit_sample_for_fable.jsonl` did not exist, so I drew the sample myself.
- Population: first-pass `exclude` verdicts with a code other than `OFF`, from `ta_verdicts.jsonl` (562
  records) plus the three shard C batch files (58 further records), deduplicated by id: 139 records.
- Sample: ids sorted, `random.seed(20261112)`, `random.sample(pop, 14)` (10%).
- Judged on title and abstract only, under the 2b rule that doubt means pass. All 14 upheld. All 14 had
  also been upheld by the earlier Opus audit, so this is a third reading of those records, not a second.
- One record (OUCI2-7A5oAOn1) is excluded on language alone; its abstract describes a Moodle
  quasi-experiment.

## 9. Part D (abstract triage of the 11 originally no-open-access records still without full text)
Ids: every id in `data/noaa/in.jsonl` with no `data/fulltext/<id>.txt` (none had a last route of `invalid`).
Judged on the OpenAlex title and abstract only. Result: likely_eligible 2 (OUCI-034, OUCI-107), unclear 2
(OUCI-041, OUCI-096), likely_ineligible 7 (NOIND 5, E2 1, E3 1). OUCI-008 is a book-chapter reprint of
OUCI-007 (identical abstract). All 11 abstracts are in English; the full-text language of OUCI-041 was not
verified. File: `data/ft/noaa_abstract_triage.jsonl`.

## 10. Part A final state (2026-11-13, after shard B reported DONE)
- 179 records adjudicated (worklists main 53, manualA 62, manualB 66; two ids occur twice because they were
  re-saved and re-assessed). The ten Part C records are separate.
- Decisions: my blind decision equalled the assessor's on all 179 as they now stand. One record
  (`2-s2.0-84865086835`) was first adjudicated on a wrong file, where I missed the mismatch the assessor
  caught; it was re-adjudicated on the correct text (exclude, NOREL).
- Final: include 12; exclude 166 (NOREL 73, E4 49, E6 20, NONEMP 12, E3 9, E2 2, E1 1);
  unusable full text 1 (`2-s2.0-84947649275`, publisher preview only).
- Final code differs from the assessor's on 10 excludes (6 NOREL to E4, 2 E3 to NOREL, 1 E3 to E2,
  1 NONEMP to E4). My blind code differed from the assessor's on 21 records; on 11 of them I adopted the
  assessor's code after re-reading (mostly E3 precedence for non-HE samples I had not checked, and
  NONEMP for abstracts with no results).
- Two of the 166 excludes are originally included studies met again in the Scopus arm (section 7); they
  should be moved to "duplicates" in the flow, leaving 164 eligibility exclusions.
- Includes (criteria): 2-s2.0-77955466176 (I2, I1), 2-s2.0-84993953291 (I4), 2-s2.0-85041501774 (I1),
  2-s2.0-85047255869 (I1), 2-s2.0-85063288496 (I1, I2), 2-s2.0-85064678466 (I1), 2-s2.0-85173737803 (I2),
  2-s2.0-85206140870 (I1), 2-s2.0-85218629537 (I1), 2-s2.0-105030276337 (I1), 2-s2.0-105046336713 (I1),
  OUCI2-4kEb33no (I1, I3).
- Borderline includes to report with caveats: 2-s2.0-84993953291 and 2-s2.0-85064678466 (mixed samples,
  E3 arguable); 2-s2.0-85218629537 (analysed n not reported, signs of rho flip between cohorts);
  2-s2.0-85047255869 (n = 37, dichotomised indicator).
- Extraction corrections on includes: 2-s2.0-84993953291 (assessor said no r is printed; Table 1 gives
  r = -0.287, -0.210, 0.182 on n = 120, plus R2 = 0.12 and 0.14); 2-s2.0-105046336713 (n 589 to 595);
  2-s2.0-85218629537 and OUCI2-4kEb33no (analysed n clarified, values unchanged). On excludes: OUCI-054
  (n nr to 232, and the code).
- In Part C, `n: corrected` means corrected relative to the paper's current Table 2 cell; the assessor's
  re-extraction had reached the same values, except herrera2024metaphorical, where the assessor left n as nr.
- After all adjudications were written I tailed [the full-text assessor's progress log, worklist manualB] once to confirm shard B had
  finished. This had no effect on blinding.

## 11. Rule I (E4 versus NOREL), upheld and applied to all three shards (2026-11-13)
Shard B's tie-break is the same rule as the clarification in the header of [prompt 03b](03b_fulltext_decision_rules.md), and I uphold
it. As applied in `final_code`:
- **E4** when (a) the design compares groups, cohorts, conditions or time points, (b) an achievement or
  performance measure is among the compared outcomes, and (c) no per-student platform-recorded measure enters
  any analysis.
- **NOREL** when a platform-recorded measure is collected or analysed but never related to success or a
  construct (including when it is itself only compared between groups), when every outcome is self-report,
  or when a cross-sectional survey correlates self-report scales with grades.
- Sweep: I re-read the design and outcome fields of every record whose final code was NOREL (71 at the time).
  Two more were recoded to E4: `2-s2.0-105042502652` and `2-s2.0-85061305268` (both from the first two
  shards, both coded NOREL by the assessor and by me). Records kept as NOREL although they compare groups on
  a test, because a platform measure enters an analysis: `2-s2.0-105022660484`, `2-s2.0-105043924681`,
  `2-s2.0-85017608602`, `2-s2.0-85192716149`, `2-s2.0-84969916962`.
- The assessor's five late recodes in shard B (NOREL to E4) match my final codes. I adopted two of them on
  re-comparison (`2-s2.0-85117921314`, `2-s2.0-85149961388`); the other three I had already coded E4.
- Even after the sweep the E4/NOREL split depends on fine readings. Reporting the two together as "no
  indicator-outcome data" would be the more defensible presentation; if they are reported separately, use
  the `final_code` values.

## 12. Other points raised by the orchestrator
- `OUCI2-4NkxOZDV` and `OUCI2-lmbPyXBP`: I agree they report the same cohort (same authors, n = 420 split
  210/210, same six scales). Both are excluded as NOREL; for the record the second is a companion report.
- `2-s2.0-84947649275` is adjudicated `unusable_fulltext` (two-page publisher preview).
- Shard B includes (`2-s2.0-105030276337`, `2-s2.0-85063288496`, `2-s2.0-85206140870`): every extracted number
  was checked against the text; in `2-s2.0-85063288496` the signs were read from the U+0002 characters.
- Assessor files revised after my first pass were re-compared (eight files had a newer modification time);
  see the `recompared` field. `2-s2.0-77955466176` now carries I2 only.
- Section 10 figures are superseded by the final tally in [the adjudicator's progress log].
