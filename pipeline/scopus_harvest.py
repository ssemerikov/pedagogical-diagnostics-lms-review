#!/usr/bin/env python3
# Public-repository copy of the review's working script, derived automatically: only paths, output
# locations and the handling of private inputs differ from the working copy (see README.md).
"""Harvest the Scopus arm of the review update (WP02a).

Runs the review's four-cluster query against the Scopus Search API (STANDARD view;
this key has no entitlement for COMPLETE view or abstracts). Writes one JSON line per record
to out/scopus/records.jsonl (git-ignored: Scopus records are not redistributed), page by page,
and logs each page to standard error.
Resumable: pages already recorded in out/scopus/pages_done.txt are skipped.

The API key is read from the environment variable SCOPUS_API_KEY; without it the script says so and
exits. The key is never printed or written.
Usage:  SCOPUS_API_KEY=... python3 pipeline/scopus_harvest.py   (run from the repository root)
"""
import datetime
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

QUERY = ('TITLE-ABS-KEY ( ( LMS OR "learning management system" OR "distance learning" ) AND '
         '( empirical OR experiment OR experimental OR "real-life" ) AND '
         '( sign OR signs OR measurement OR measure OR criteria OR criterion OR parameter OR factor ) AND '
         '( "learning style" OR "cognitive style" OR "personality type" OR "sensory preference" OR "modality" OR '
         '"Personality Computing" OR "Automatic Personality Recognition" OR "Automatic Personality Perception" OR '
         'systematicity OR motivation OR stability OR mobilisation OR reflection OR prognosis OR Self-management ) )')
PAGE = 25
OUT_DIR = 'out/scopus'
RECORDS = os.path.join(OUT_DIR, 'records.jsonl')
PAGES_DONE = os.path.join(OUT_DIR, 'pages_done.txt')
META = os.path.join(OUT_DIR, 'search_meta.json')


def api_key():
    key = os.environ.get('SCOPUS_API_KEY', '').strip()
    if not key:
        print('scopus_harvest: SCOPUS_API_KEY is not set. The Scopus Search API needs a personal key '
              '(https://dev.elsevier.com/); nothing was harvested.', file=sys.stderr)
        sys.exit(0)
    return key


def log(msg):
    print(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} {msg}", file=sys.stderr)


def fetch(key, start):
    url = 'https://api.elsevier.com/content/search/scopus?' + urllib.parse.urlencode(
        {'query': QUERY, 'count': PAGE, 'start': start, 'view': 'STANDARD'})
    req = urllib.request.Request(url, headers={'X-ELS-APIKey': key, 'Accept': 'application/json'})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504):
                time.sleep(5 * (attempt + 1))
                continue
            raise
        except urllib.error.URLError:
            time.sleep(5 * (attempt + 1))
    raise RuntimeError(f'page start={start} failed after retries')


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    key = api_key()
    done = set()
    if os.path.exists(PAGES_DONE):
        done = {int(x) for x in open(PAGES_DONE).read().split()}
    first = fetch(key, 0)
    total = int(first['search-results']['opensearch:totalResults'])
    if not os.path.exists(META):
        json.dump({'database': 'Scopus (Elsevier Scopus Search API, STANDARD view)',
                   'query': QUERY, 'field': 'TITLE-ABS-KEY', 'limits': 'none (no date, language or document-type limits)',
                   'run_started': datetime.datetime.now().astimezone().isoformat(timespec='seconds'),
                   'total_results': total}, open(META, 'w'), indent=2)
    log(f'WP02a harvest: total={total}, pages already done={len(done)}')
    for start in range(0, total, PAGE):
        if start in done:
            continue
        d = first if start == 0 else fetch(key, start)
        entries = d['search-results'].get('entry', [])
        with open(RECORDS, 'a') as f:
            for i, e in enumerate(entries):
                rec = {
                    'eid': e.get('eid'), 'doi': (e.get('prism:doi') or '').lower() or None,
                    'title': e.get('dc:title'), 'first_author': e.get('dc:creator'),
                    'year': (e.get('prism:coverDate') or '')[:4] or None, 'cover_date': e.get('prism:coverDate'),
                    'source': e.get('prism:publicationName'), 'doc_type': e.get('subtypeDescription'),
                    'aggregation': e.get('prism:aggregationType'), 'open_access_flag': e.get('openaccessFlag'),
                    'affiliation_countries': sorted({a.get('affiliation-country') for a in (e.get('affiliation') or []) if a.get('affiliation-country')}),
                    'scopus_rank': start + i + 1, 'harvested': datetime.date.today().isoformat(),
                }
                f.write(json.dumps(rec, ensure_ascii=False) + '\n')
        with open(PAGES_DONE, 'a') as f:
            f.write(f'{start}\n')
        log(f'page start={start}: {len(entries)} records appended; NEXT: start={start + PAGE}')
        time.sleep(0.3)
    meta = json.load(open(META))
    meta['run_finished'] = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
    json.dump(meta, open(META, 'w'), indent=2)
    log('WP02a harvest complete')


if __name__ == '__main__':
    main()
