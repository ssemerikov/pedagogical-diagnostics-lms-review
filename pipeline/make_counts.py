#!/usr/bin/env python3
# Public-repository copy of the review's working script, derived automatically: only paths, output
# locations and the handling of private inputs differ from the working copy (see README.md).
"""Build the master screening ledger and the PRISMA 2020 (updated review) counts.

Reads every arm's on-disk records (run from the repository root):
  O1 original OUCI search (Jan 2026): data/original/supplementary_screening.csv (+1 study by citation chaining)
  N  re-sought originally-unretrieved records (31): data/noaa/*
  S  Scopus (searched 2026-11-12): data/scopus/*
  O2 OUCI re-run (2026-11-12): data/ouci/*
  ft assessment: data/ft/assess/<id>.json ; adjudication (Fable): data/ft/adjudicate/<id>.json
Writes:
  data/screening_master.csv   one row per record per arm, with every stage and the deciding model
  data/prisma_counts.json     all counts used in the paper
  data/counts.tex  LaTeX macros (names are fixed; see the file header)
Final decision rule for update records: included only if the full-text assessor and the independent
adjudicator agree on inclusion, or the adjudicator's written re-read includes it (adjudicate.final_decision).
Records not yet adjudicated count as 'pending' and are NOT counted as included.
"""
import csv, glob, json, os, datetime
from collections import Counter

R = lambda p: [json.loads(l) for l in open(p) if l.strip()] if os.path.exists(p) else []
J = lambda p: json.load(open(p)) if os.path.exists(p) else None

def assess(i): return J(f'data/ft/assess/{i}.json')
def adjud(i): return J(f'data/ft/adjudicate/{i}.json')

def final_ft(i):
    a, d = assess(i), adjud(i)
    if not a: return 'pending_assessment', None
    if a.get('decision') == 'unusable_fulltext': return 'not_retrieved_usable', 'unusable full text'
    if not d: return 'pending_adjudication', a.get('exclusion_code')
    if d.get('final_decision') == 'unusable_fulltext': return 'not_retrieved_usable', 'unusable full text'
    dec = d.get('final_decision') or a.get('decision')
    return ('included' if dec == 'include' else 'excluded'), (d.get('final_code') or a.get('exclusion_code'))

# How each full text was obtained (decision D8): last line per id wins; 'invalid' = wrong or unusable file.
ROUTE = {}
for x in R('data/fulltext_routes.jsonl'): ROUTE[x['id']] = x['route']
def has_text(i): return ROUTE.get(i) in ('oa_auto', 'manual_user', 'author')
E7_UPD = 'E7 (full text not obtainable by the review team; amended criterion, D8)'

rows = []
# ---- O1 original
orig = list(csv.DictReader(open('data/original/supplementary_screening.csv')))
for r in orig:
    rows.append({'arm': 'O1', 'id': f"OUCI-{int(r['Record']):03d}", 'doi': r['DOI'].strip().lower(), 'stage': 'full_text', 'ta': '', 'ta_code': '',
                 'retrieval': 'not_retrieved' if 'open access' in r['Reason'].lower() else 'retrieved',
                 'final': r['Decision'].lower(), 'reason': r['Reason'], 'decided_by': 'first author (Jan 2026; Gemini 3.0 first pass)'})
rows.append({'arm': 'O1-chaining', 'id': 'ferdiansyah2025assessing', 'doi': '10.1016/j.ssaho.2025.101696', 'stage': 'full_text', 'ta': '', 'ta_code': '',
             'retrieval': 'retrieved', 'final': 'included', 'reason': 'citation chaining', 'decided_by': 'first author (Jan 2026)'})
# ---- N: originally-unretrieved 31, re-sought
nlog = {x['id']: x for x in R('data/noaa/retrieval_log.jsonl')}
for x in R('data/noaa/in.jsonl'):
    rl = nlog.get(x['id'], {})
    if rl.get('result') == 'retrieved' or has_text(x['id']):
        rl = dict(rl, result='retrieved')
        f, code = final_ft(x['id'])
    else:
        f, code = ('not_retrieved' if rl else 'pending_retrieval'), (E7_UPD if rl else None)
    rows.append({'arm': 'N', 'id': x['id'], 'doi': x['doi'], 'stage': 'retrieval', 'ta': '', 'ta_code': '', 'retrieval': rl.get('result', 'pending'),
                 'final': f, 'reason': code or '', 'decided_by': 'update pipeline (two language models, no author verification)'})
# ---- S and O2 (title/abstract pipeline)
ta = {}
for f in sorted(glob.glob('data/scopus/ta_batches/*.jsonl')):
    for x in R(f): ta[x['id']] = x
aud = {}
for f in sorted(glob.glob('data/scopus/ta_audit/*.jsonl')):
    for x in R(f): aud[x['id']] = x
rlog = {}
for p in ('data/scopus/retrieval_log.jsonl', 'data/ouci/retrieval_log.jsonl'):
    for x in R(p): rlog[x['id']] = x
setup_s = J('data/scopus/screening_setup.json') or {}
overlap = {o['id'] for o in setup_s.get('overlap_with_ouci118', [])}
# Scopus copies of already-included studies not matched by DOI to the 118: Ferdiansyah (citation chaining) and Bykova (no DOI in Scopus; title match)
overlap |= {'2-s2.0-105009000141', '2-s2.0-85108022090'}
setup_o = J('data/ouci/screening_setup.json') or {}

def ta_final(i):
    v = ta.get(i); a = aud.get(i)
    if not v: return 'pending', ''
    if a and a.get('audit') == 'overturn': return a.get('new_verdict', 'maybe'), a.get('code', '')
    return v['verdict'], v.get('code', '')

def pipeline_row(arm, i, doi):
    tv, code = ta_final(i)
    row = {'arm': arm, 'id': i, 'doi': doi, 'ta': tv, 'ta_code': code, 'decided_by': 'update pipeline (two language models, no author verification)'}
    if tv == 'pending':
        row.update(stage='ta', retrieval='', final='pending_screening', reason='')
    elif tv == 'exclude':
        row.update(stage='ta', retrieval='', final='excluded_ta', reason=code)
    else:
        rl = rlog.get(i)
        if has_text(i) or (rl and rl['result'] == 'retrieved'):
            f, c = final_ft(i); row.update(stage='full_text', retrieval='retrieved', final=f, reason=c or '')
        elif not rl: row.update(stage='retrieval', retrieval='pending', final='pending_retrieval', reason='')
        elif rl['result'] != 'retrieved': row.update(stage='retrieval', retrieval='not_retrieved', final='not_retrieved', reason=E7_UPD)
        else:
            f, c = final_ft(i); row.update(stage='full_text', retrieval='retrieved', final=f, reason=c or '')
    return row

for x in R('data/scopus/records.jsonl'):
    if x['eid'] in overlap:
        how = 'title match (copy of an included study)' if not x.get('doi') else 'DOI match'
        rows.append({'arm': 'S', 'id': x['eid'], 'doi': x['doi'], 'stage': 'dedup', 'ta': '', 'ta_code': '', 'retrieval': '', 'final': 'duplicate_of_O1', 'reason': '', 'decided_by': how})
    else:
        rows.append(pipeline_row('S', x['eid'], x['doi']))
dup_o = {d['id'] for d in setup_o.get('duplicates_of_orig118', [])}
carried = {c['id'] for c in setup_o.get('also_in_scopus_carried_over', [])}
orig_dois = {r['DOI'].strip().lower() for r in orig if r['DOI'].strip()}
for x in R('data/ouci/ouci_rerun.jsonl'):
    i = 'OUCI2-' + x['ouci_work']
    if x['doi'] in orig_dois or i in dup_o:
        rows.append({'arm': 'O2', 'id': i, 'doi': x['doi'], 'stage': 'dedup', 'ta': '', 'ta_code': '', 'retrieval': '', 'final': 'duplicate_of_O1', 'reason': '', 'decided_by': 'DOI/title match'})
    elif i in carried or i == 'OUCI2-4VPazBzY':   # 4VPazBzY = Scopus 2-s2.0-105019320162 (same CEUR paper; identical PDF)
        rows.append({'arm': 'O2', 'id': i, 'doi': x['doi'], 'stage': 'dedup', 'ta': '', 'ta_code': '', 'retrieval': '', 'final': 'duplicate_of_S', 'reason': '', 'decided_by': 'DOI match'})
    else:
        rows.append(pipeline_row('O2', i, x['doi']))

os.makedirs('data', exist_ok=True)
for r in rows:
    r['route'] = ROUTE.get(r['id'], '') if r.get('retrieval') == 'retrieved' and r['arm'] not in ('O1', 'O1-chaining') else ''
cols = ['arm', 'id', 'doi', 'stage', 'ta', 'ta_code', 'retrieval', 'route', 'final', 'reason', 'decided_by']
with open('data/screening_master.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); [w.writerow({k: r.get(k, '') for k in cols}) for r in rows]

def n(arm, pred): return sum(1 for r in rows if r['arm'] in arm and pred(r))
upd = ('S', 'O2')
c = {
 'nOuciRecords': n(('O1',), lambda r: True), 'nChaining': 1, 'nSought': n(('O1',), lambda r: True) + 1,
 'nNotRetrieved': n(('O1',), lambda r: r['retrieval'] == 'not_retrieved'),
 'nIncluded': n(('O1', 'O1-chaining'), lambda r: r['final'] == 'included'),
 'nScopusRecords': n(('S',), lambda r: True), 'nScopusOverlapOuci': n(('S',), lambda r: r['final'] == 'duplicate_of_O1'),
 'nOuciRerunRecords': n(('O2',), lambda r: True), 'nOuciRerunDupOrig': n(('O2',), lambda r: r['final'] == 'duplicate_of_O1'),
 'nOuciRerunDupScopus': n(('O2',), lambda r: r['final'] == 'duplicate_of_S'),
 'nUpdateScreened': n(upd, lambda r: r['stage'] not in ('dedup',) and r['final'] != 'pending_screening'),
 'nUpdateTAExcluded': n(upd, lambda r: r['final'] == 'excluded_ta'),
 'nUpdateSought': n(upd, lambda r: r['ta'] in ('pass', 'maybe')),
 'nUpdateNotRetrieved': n(upd, lambda r: r['final'] in ('not_retrieved', 'not_retrieved_usable')),
 'nUpdateAssessed': n(upd, lambda r: r['stage'] == 'full_text' and r['final'] not in ('not_retrieved_usable',)),
 'nUpdateFTExcluded': n(upd, lambda r: r['stage'] == 'full_text' and r['final'] == 'excluded'),
 'nUpdateIncludedDB': n(upd, lambda r: r['final'] == 'included'),
 'nUpdatePending': n(upd + ('N',), lambda r: r['final'].startswith('pending')),
 'nNoOAReSought': n(('N',), lambda r: True), 'nNoOARetrieved': n(('N',), lambda r: r['retrieval'] == 'retrieved'),
 'nNoOAIncluded': n(('N',), lambda r: r['final'] == 'included'),
 'nFTAuto': n(upd + ('N',), lambda r: r['route'] == 'oa_auto' and r['final'] in ('included', 'excluded', 'pending_adjudication')),
 'nFTManual': n(upd + ('N',), lambda r: r['route'] in ('manual_user', 'author') and r['final'] in ('included', 'excluded', 'pending_adjudication')),
}
c['nUpdateIncluded'] = c['nUpdateIncludedDB'] + c['nNoOAIncluded']
# Reporting quality over the final included set (R7.4): original included studies (re-extraction files, bib keys) + update includes.
ORIG_INCL = [x['id'] for x in R('data/reextract/in.jsonl')]
def reports(i):
    a, d = assess(i) or {}, adjud(i) or {}
    ex, chk = a.get('extraction') or {}, d.get('extraction_check') or {}
    n_ok = isinstance(ex.get('n'), int) or str(ex.get('n', '')).isdigit()
    if chk.get('n') == 'nr_confirmed': n_ok = False
    if chk.get('n') == 'corrected' and chk.get('n_value') not in (None, '', 'nr'): n_ok = True
    es = [e for e in (ex.get('effect_sizes') or [])]
    bad = sum(1 for e in (chk.get('effect_sizes') or []) if e.get('status') == 'not_found')
    return n_ok, len(es) - bad > 0
final_incl = ORIG_INCL + [r['id'] for r in rows if r['arm'] in upd + ('N',) and r['final'] == 'included']
rep = [reports(i) for i in final_incl]
# Effect sizes (R7.4): data/ft/effect_size_classification.jsonl records, per included study, whether an extracted statistic is an
# indicator-outcome effect size (a correlation, regression or path coefficient, odds ratio or variance explained). Test statistics or
# p values alone (t, F), classification accuracy and contrasts between intervention groups do not count. Last line per id wins.
ESC = {x['id']: x['counts_as_indicator_outcome_effect_size'] for x in R('data/ft/effect_size_classification.jsonl')}
c['nReportN'] = sum(1 for a, b in rep if a)
c['nReportStatistic'] = sum(1 for a, b in rep if b)   # any indicator-outcome statistic extracted and found by the adjudicator
c['nReportEffectSize'] = sum(1 for i, (a, b) in zip(final_incl, rep) if ESC.get(i, b))
c['nReportCoefficient'] = c['nReportEffectSize']       # alias used by WP07a
c['nReportBase'] = len(final_incl)
assert all(i in ESC for i in final_incl), 'included study missing from effect_size_classification.jsonl: ' + str([i for i in final_incl if i not in ESC])
sens = [(adjud(i) or {}).get('sensitivity') for i in ORIG_INCL]
c['nOrigSensitivityJudged'] = sum(1 for x in sens if x)
c['nOrigMeetUpdateRules'] = sum(1 for x in sens if x and x.get('meets_update_rules'))
# D12: included only under the shared E3 reading ("only clearly non-HE/VET samples"); a strict reading of E3 would exclude them.
E3_BORDERLINE = {'2-s2.0-84993953291', '2-s2.0-85064678466', 'farameita2025integration'}
c['nOrigMeetUpdateRulesStrict'] = sum(1 for i, x in zip(ORIG_INCL, sens) if x and x.get('meets_update_rules') and i not in E3_BORDERLINE)
c['nIncludedTotal'] = c['nIncluded'] + c['nUpdateIncluded']
c['nUpdateIncludedStrict'] = c['nUpdateIncluded'] - sum(1 for r in rows if r['arm'] in upd + ('N',) and r['final'] == 'included' and r['id'] in E3_BORDERLINE)
# per-code macros (LaTeX names cannot contain digits: E3 -> EThree)
CODE = {'OFF': 'OFF', 'NOIND': 'NOIND', 'NONEMP': 'NONEMP', 'NOREL': 'NOREL', 'E1': 'EOne', 'E2': 'ETwo', 'E3': 'EThree', 'E4': 'EFour', 'E6': 'ESix'}
ta_codes = Counter(r['reason'] for r in rows if r['arm'] in upd and r['final'] == 'excluded_ta')
ft_codes = Counter(r['reason'] for r in rows if r['arm'] in upd + ('N',) and r['final'] == 'excluded')
n_codes = Counter(r['reason'] for r in rows if r['arm'] == 'N' and r['final'] == 'excluded')
for k, nm in CODE.items():
    c['nTAExcl' + nm] = ta_codes.get(k, 0); c['nFTExcl' + nm] = ft_codes.get(k, 0); c['nNoOAExcl' + nm] = n_codes.get(k, 0)
assert sum(ta_codes.values()) == sum(c['nTAExcl' + nm] for nm in CODE.values()), 'unmapped title/abstract code: ' + str(ta_codes)
assert sum(ft_codes.values()) == sum(c['nFTExcl' + nm] for nm in CODE.values()), 'unmapped full-text code: ' + str(ft_codes)
c['nNoOARouteAuto'] = n(('N',), lambda r: r['final'] in ('included', 'excluded') and r['route'] == 'oa_auto')
c['nNoOARouteManual'] = n(('N',), lambda r: r['final'] in ('included', 'excluded') and r['route'] in ('manual_user', 'author'))
tri = Counter(x.get('classification') for x in R('data/ft/noaa_abstract_triage.jsonl'))
c['nNoOATriageEligible'], c['nNoOATriageUnclear'], c['nNoOATriageIneligible'] = tri.get('likely_eligible', 0), tri.get('unclear', 0), tri.get('likely_ineligible', 0)
# original arm (O1), full-text exclusion reasons as recorded in January 2026
OREASON = {'Does not report the indicator--outcome data the inclusion criteria require': 'NoRel', 'Full text not available in open access': 'NoOA',
           'Not a primary empirical study (review or conceptual paper)': 'NonEmp', 'Publication language other than English or Ukrainian': 'Lang',
           'Evaluates learning achievement rather than effectiveness of learning actions': 'Achiev', 'Duplicate of another record (preprint or repository copy)': 'Dup'}
o_codes = Counter(r['reason'] for r in rows if r['arm'] == 'O1' and r['final'] == 'excluded')
assert set(o_codes) <= set(OREASON), 'unmapped original reason: ' + str(set(o_codes) - set(OREASON))
for k, nm in OREASON.items(): c['nOrigExcl' + nm] = o_codes.get(k, 0)
c['taExcludedByCode'] = dict(Counter(r['reason'] for r in rows if r['arm'] in upd and r['final'] == 'excluded_ta'))
c['ftExcludedByCode'] = dict(Counter(r['reason'] for r in rows if r['arm'] in upd + ('N',) and r['final'] == 'excluded'))
def _newest_input_date():
    # Deterministic stand-in for the wall clock (public repository): the newest date recorded in the input data,
    # so that re-running on the same data reproduces this file byte for byte.
    import re
    found = []
    for p in sorted(glob.glob('data/**/*.json', recursive=True) + glob.glob('data/**/*.jsonl', recursive=True)):
        if os.path.basename(p) == 'prisma_counts.json': continue
        found += re.findall(r'"(?:logged_on|assessed_on|adjudicated_on|date|run_started|run_finished)"\s*:\s*"(\d{4}-\d{2}-\d{2})',
                            open(p, encoding='utf-8').read())
    return max(found) if found else 'unknown'
c['generated'] = _newest_input_date()
json.dump(c, open('data/prisma_counts.json', 'w'), indent=1)

meta_s = J('data/scopus/search_meta.json') or {}; meta_o = J('data/ouci/run_meta.json') or {}
def ta_audit():
    """Title/abstract audit of exclusions (WP02b): last line per id wins."""
    import glob as _g
    a = {}
    for f in sorted(_g.glob('data/scopus/ta_audit/excl*.jsonl')):
        for l in open(f, encoding='utf-8'):
            if l.strip():
                r = json.loads(l); a[r['id']] = r['audit']
    return len(a), sum(1 for v in a.values() if v == 'overturn')
TA_AUDITED, TA_OVERTURNED = ta_audit()

def d(iso):
    if not iso: return 'TBD'
    dt = datetime.datetime.fromisoformat(iso); return f"{dt.day}~{dt.strftime('%B')} {dt.year}"
tex = ['%% GENERATED by pipeline/make_counts.py from data/screening_master.csv -- do not edit by hand.',
       f"%% generated {c['generated']}; pending records (not counted as included): {c['nUpdatePending']}"]
for k, v in c.items():
    if isinstance(v, int): tex.append(f'\\newcommand{{\\{k}}}{{{v}}}')
# legacy macro names used by the writers
alias = {'nAssessedFT': c['nSought'] - c['nNotRetrieved'], 'nExcludedFT': c['nSought'] - c['nNotRetrieved'] - c['nIncluded'],
         'nExcludedAll': c['nSought'] - c['nIncluded'], 'nScopusScreened': n(('S',), lambda r: r['stage'] != 'dedup'),
         'nScopusTAExcluded': n(('S',), lambda r: r['final'] == 'excluded_ta'), 'nScopusSought': n(('S',), lambda r: r['ta'] in ('pass', 'maybe')),
         'nScopusNotRetrieved': n(('S',), lambda r: r['final'] in ('not_retrieved', 'not_retrieved_usable')),
         'nScopusAssessed': n(('S',), lambda r: r['stage'] == 'full_text' and r['final'] != 'not_retrieved_usable'),
         'nScopusFTExcluded': n(('S',), lambda r: r['final'] == 'excluded'),
         'nScopusIncluded': n(('S',), lambda r: r['final'] == 'included'), 'nOuciRerunNew': n(('O2',), lambda r: r['stage'] != 'dedup'),
         'nOuciRerunIncluded': n(('O2',), lambda r: r['final'] == 'included'), 'nOtherIncluded': 0, 'nNoOAOAFound': 15,
         # per-arm boxes for the updated-review PRISMA figure (2026-11-13): every arm sums on its own
         'nOuciRerunTAExcluded': n(('O2',), lambda r: r['final'] == 'excluded_ta'),
         'nTAAudited': TA_AUDITED, 'nTAAuditOverturned': TA_OVERTURNED,  # WP11 F025
         'nOuciRerunSought': n(('O2',), lambda r: r['ta'] in ('pass', 'maybe')),
         'nOuciRerunNotRetrieved': n(('O2',), lambda r: r['final'] in ('not_retrieved', 'not_retrieved_usable')),
         'nOuciRerunAssessed': n(('O2',), lambda r: r['stage'] == 'full_text' and r['final'] != 'not_retrieved_usable'),
         'nOuciRerunFTExcluded': n(('O2',), lambda r: r['final'] == 'excluded'),
         'nNoOANotRetrieved': n(('N',), lambda r: r['final'] in ('not_retrieved', 'not_retrieved_usable')),
         'nNoOAAssessed': n(('N',), lambda r: r['final'] in ('included', 'excluded')),
         'nNoOAFTExcluded': n(('N',), lambda r: r['final'] == 'excluded'),
         # every record of the update (S, O2, N) whose full text the team could not obtain (residual availability limitation)
         'nResidualNotRetrieved': n(upd + ('N',), lambda r: r['final'] in ('not_retrieved', 'not_retrieved_usable'))}
for k, v in alias.items(): tex.append(f'\\newcommand{{\\{k}}}{{{v}}}')
tex.append(f"\\newcommand{{\\dateScopus}}{{{d(meta_s.get('run_started'))}}}")
tex.append(f"\\newcommand{{\\dateOuciRerun}}{{{d(meta_o.get('run_started'))}}}")
open('data/counts.tex', 'w').write('\n'.join(tex) + '\n')
print(json.dumps({k: v for k, v in c.items() if k != 'generated'}, indent=0))
