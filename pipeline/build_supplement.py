#!/usr/bin/env python3
# Public-repository copy of the review's working script, derived automatically: only paths, output
# locations and the handling of private inputs differ from the working copy (see README.md).
"""Build the anonymous screening supplement (S1–S3) from the ledger. Run from the repository root AFTER pipeline/make_counts.py; writes to out/supplement/.

S1_screening_ledger.csv   every record of every arm: stage reached, verdicts, codes, full-text route, deciding agent
S2_noOA_reassessment.csv  the 31 records the original search excluded for lack of an open-access full text, re-sought (R7.3)
S3_search_strategies.md   exact queries, fields, dates and counts for every search
Scopus abstracts are never written (Scopus terms); only identifiers, titles, years and decisions.
"""
import csv, json, os, glob, datetime

R = lambda p: [json.loads(l) for l in open(p, encoding='utf-8') if l.strip()] if os.path.exists(p) else []
J = lambda p: json.load(open(p, encoding='utf-8')) if os.path.exists(p) else None
OUT = 'out/supplement'
os.makedirs(OUT, exist_ok=True)

meta = {}
for x in R('data/scopus/records.jsonl'): meta[x['eid']] = (x.get('title'), x.get('year'))
for p in ('data/ouci/openalex.jsonl', 'data/noaa/openalex.jsonl', 'data/reextract/openalex.jsonl'):
    for x in R(p): meta.setdefault(x['id'], (x.get('oa_title'), x.get('oa_year')))
lang = {x['id']: x.get('language') for p in ('data/noaa/openalex.jsonl', 'data/ouci/openalex.jsonl') for x in R(p)}

def ft(i):
    a, d = J(f'data/ft/assess/{i}.json') or {}, J(f'data/ft/adjudicate/{i}.json') or {}
    return {'ft_assessor_decision': a.get('decision', ''), 'ft_assessor_code': a.get('exclusion_code') or '',
            'adjudicator_decision': d.get('final_decision', ''), 'adjudicator_code': d.get('final_code') or '',
            'agree': '' if not d else str(d.get('agree', '')).lower(),
            'n': (a.get('extraction') or {}).get('n', '') if a.get('decision') == 'include' else ''}

ARM = {'O1': 'OUCI, original search (Jan 2026)', 'O1-chaining': 'Citation chaining (original review)',
       'N': 'Original no-OA records, re-sought (update)', 'S': 'Scopus (update)', 'O2': 'OUCI re-run (update)'}
rows = list(csv.DictReader(open('data/screening_master.csv', encoding='utf-8')))
cols = ['arm', 'arm_label', 'id', 'doi', 'title', 'year', 'stage', 'ta', 'ta_code', 'retrieval', 'route', 'final', 'reason',
        'ft_assessor_decision', 'ft_assessor_code', 'adjudicator_decision', 'adjudicator_code', 'agree', 'n', 'decided_by']
with open(f'{OUT}/S1_screening_ledger.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
    for r in rows:
        t, y = meta.get(r['id'], ('', ''))
        out = dict(r, arm_label=ARM.get(r['arm'], r['arm']), title=t or '', year=y or '')
        if r['stage'] == 'full_text' and r['arm'] not in ('O1', 'O1-chaining'): out.update(ft(r['id']))
        w.writerow({k: out.get(k, '') for k in cols})

oa = {x['id']: x for x in R('data/noaa/openalex.jsonl')}
s2cols = ['record', 'id', 'doi', 'title', 'year', 'language', 'oa_copy_listed_openalex', 'retrieval', 'route', 'final', 'reason',
          'ft_assessor_code', 'adjudicator_decision', 'adjudicator_code']
nrows = {r['id']: r for r in rows if r['arm'] == 'N'}
with open(f'{OUT}/S2_noOA_reassessment.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=s2cols); w.writeheader()
    for x in R('data/noaa/in.jsonl'):
        r = nrows.get(x['id'], {}); o = oa.get(x['id'], {})
        out = {'record': x['record'], 'id': x['id'], 'doi': x['doi'], 'title': o.get('oa_title') or '', 'year': o.get('oa_year') or '',
               'language': o.get('language') or '', 'oa_copy_listed_openalex': o.get('is_oa'), 'retrieval': r.get('retrieval', ''),
               'route': r.get('route', ''), 'final': r.get('final', ''), 'reason': r.get('reason', '')}
        out.update({k: v for k, v in ft(x['id']).items() if k in s2cols})
        w.writerow({k: out.get(k, '') for k in s2cols})

sm, om = J('data/scopus/search_meta.json') or {}, J('data/ouci/run_meta.json') or {}
ouci_q = ('(LMS | "learning  management system" | "distance learning")  (empirical | experiment | experimental  | "real-life") '
          '(sign  | signs | measurement | measure | criteria | criterion | parameter | factor ) ("learning style" | "cognitive style" | '
          '"personality type" | "sensory preference" | "modality" | "Personality Computing" | "Automatic Personality Recognition" | '
          '"Automatic Personality Perception" | systematicity | motivation | stability | mobilisation | reflection | prognosis | Self-management)')
md = f"""# S3. Search strategies

Generated {datetime.date.today().isoformat()} from the run records in the review data.

## 1. OUCI, original search (January 2026)
- Database: Open Ukrainian Scientific Content Initiative (OUCI), https://ouci.dntb.gov.ua/
- Field: the simple-search field (`title=` parameter), which covers title, abstract and DOI
- Query (vertical bar = OR, juxtaposition = AND):

```
{ouci_q}
```
- Run: early January 2026 (full-text retrieval attempts dated 4–5 January 2026); no date, language or document-type limits
- Records: 118

## 2. Scopus (update)
- Database: {sm.get('database', 'Scopus')}
- Field: {sm.get('field', '')}; limits: {sm.get('limits', '')}
- Query:

```
{sm.get('query', '')}
```
- Run: {sm.get('run_started', '')}; records: {sm.get('total_results', '')}

## 3. OUCI re-run (update)
- Same query and field as search 1
- Run: {om.get('run_started', '')} – {om.get('run_finished', '')}; records stated by OUCI: {om.get('total_results_stated', '')}; collected: {om.get('records_collected', '')}
- Field scope evidence: {om.get('title_param_scope_evidence', '')}

## 4. Other methods
- Citation chaining from included studies (original review: 1 study).
- Full texts not retrievable automatically were sought by the review team through open-access sources, library access and author request (protocol amendment to exclusion criterion E7; see S1, column `route`).
"""
open(f'{OUT}/S3_search_strategies.md', 'w', encoding='utf-8').write(md)
print('S1', len(rows), 'rows; S2', len(R('data/noaa/in.jsonl')), 'rows; S3 written')
