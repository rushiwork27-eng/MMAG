"""Merge the earlier zip scrape (12 Oct 2026) into this capture without duplicates.
Usage (run from site-audit/): python3 -I combine_scrapes.py <unzipped mmag-scrape dir>
Writes data/combined/{links,images,scripts-stylesheets,pages}-combined.csv"""
import sys, json, csv, glob, re, os
from collections import defaultdict
Z = sys.argv[1]
os.makedirs('data/combined', exist_ok=True)
status = {r['url']: r['status'] for r in csv.DictReader(open('data/link-check.csv'))}
pages = {}
for f in glob.glob('data/pages/*.json'):
    d = json.load(open(f)); pages[d['slug']] = d
live = {s: d for s, d in pages.items() if not d.get('archived')}
def norm(u):
    u = (u or '').strip()
    if re.fullmatch(r'https?://mmag\.in', u): u += '/'
    return u
nq = lambda u: re.sub(r'[?#].*$', '', norm(u))
path = lambda u: norm(u).replace('https://mmag.in', '') or '/'
st = lambda u: status.get(u) or status.get(nq(u)) or status.get(nq(u).rstrip('/')) or ''
def link_key(u):
    u = norm(u)
    return u if 'elementor-action' in u else u.split('#')[0]

L = defaultdict(lambda: {'texts': set(), 'nov': False, 'oct': False, 'target': ''})
for d in live.values():
    for l in d['links']:
        e = L[(norm(d['url']), link_key(l['abs']))]; e['nov'] = True
        e['texts'].add((l['text'] or l.get('aria') or '').strip()[:80]); e['target'] = e['target'] or (l.get('target') or '')
for l in json.load(open(f'{Z}/links.json')):
    if not (l['url'] or '').startswith('http'): continue
    e = L[(norm(l['page']), link_key(l['url']))]; e['oct'] = True
    e['texts'].add((l['label'] or '').strip()[:80]); e['target'] = e['target'] or (l.get('target') or '')
with open('data/combined/links-combined.csv', 'w', newline='') as fh:
    w = csv.writer(fh); w.writerow(['page', 'url', 'link_text', 'opens_new_tab', 'seen_12oct_zip', 'seen_24nov_crawl', 'status_now'])
    for (p, u), e in sorted(L.items()):
        w.writerow([path(p), u, ' | '.join(sorted(t for t in e['texts'] if t)), 'yes' if e['target'] == '_blank' else '', 'yes' if e['oct'] else '', 'yes' if e['nov'] else '', st(u)])

media = {r['source_url']: r for r in csv.DictReader(open('data/media-library.csv'))}
orig = lambda u: re.sub(r'-(\d+x\d+)(\.\w+)$', r'\2', nq(u))
I = defaultdict(lambda: {'alts': set(), 'pages': set(), 'nov': False, 'oct': False})
def add_img(u, page, alt, which):
    u = nq(u)
    if not u.startswith('http'): return
    e = I[u]; e[which] = True; e['pages'].add(path(page)); e['alts'].add(alt or '')
for d in live.values():
    for i in d['images']: add_img(i.get('currentSrc') or i.get('src'), d['url'], i.get('alt'), 'nov')
    for b in d['backgroundImages']: add_img(b['url'], d['url'], '', 'nov')
    for w in d['widgets']:
        for s in (w.get('slides') or []):
            if isinstance(s, dict) and s.get('src'): add_img(s['src'], d['url'], s.get('alt'), 'nov')
for i in json.load(open(f'{Z}/images.json')): add_img(i.get('src'), i['page'], i.get('alt'), 'oct')
with open('data/combined/images-combined.csv', 'w', newline='') as fh:
    w = csv.writer(fh); w.writerow(['url', 'alt_text', 'pages', 'seen_12oct_zip', 'seen_24nov_crawl', 'status_now', 'local_copy'])
    for u, e in sorted(I.items()):
        r = media.get(u) or media.get(orig(u)) or media.get(re.sub(r'-scaled(\.\w+)$', r'\1', orig(u)))
        w.writerow([u, ' | '.join(sorted(a for a in e['alts'] if a)) or '(none)', ' '.join(sorted(e['pages'])), 'yes' if e['oct'] else '', 'yes' if e['nov'] else '', st(u), (r or {}).get('local_path', '')])

R = defaultdict(lambda: {'pages': set(), 'nov': False, 'oct': False})
for d in live.values():
    for kind, key in (('script', 'scripts'), ('stylesheet', 'stylesheets')):
        for u in d[key]:
            e = R[(kind, nq(u))]; e['nov'] = True; e['pages'].add(path(d['url']))
for kind, f in (('script', 'scripts'), ('stylesheet', 'stylesheets')):
    for x in json.load(open(f'{Z}/{f}.json')):
        u = x.get('src') or x.get('href') or x.get('url') or ''
        if not u.startswith('http'): continue
        e = R[(kind, nq(u))]; e['oct'] = True; e['pages'].add(path(x['page']))
with open('data/combined/scripts-stylesheets-combined.csv', 'w', newline='') as fh:
    w = csv.writer(fh); w.writerow(['type', 'url', 'pages', 'seen_12oct_zip', 'seen_24nov_crawl'])
    for (k, u), e in sorted(R.items()):
        ps = sorted(e['pages']); w.writerow([k, u, ' '.join(ps) if len(ps) <= 6 else f'{len(ps)} pages', 'yes' if e['oct'] else '', 'yes' if e['nov'] else ''])

U = {}
for d in live.values(): U[norm(d['url'])] = {'title': d['title'], 'nov': True, 'oct': False, 'captured_oct': False}
for p in json.load(open(f'{Z}/pages.json')):
    e = U.setdefault(norm(p['url']), {'title': p['title'], 'nov': False, 'oct': False, 'captured_oct': False}); e['oct'] = True; e['captured_oct'] = True
for x in json.load(open(f'{Z}/url_inventory.json')):
    u = norm(x['url'].split('#')[0])
    if x['domain'].endswith('mmag.in') and '/wp-' not in u and u.startswith('http'):
        u = u if u.endswith('/') else u + '/'
        U.setdefault(u, {'title': '(linked only)', 'nov': False, 'oct': False, 'captured_oct': False})['oct'] = True
sitemap = open('backend/page-sitemap.xml').read()
with open('data/combined/pages-combined.csv', 'w', newline='') as fh:
    w = csv.writer(fh); w.writerow(['url', 'title', 'text_captured_12oct_zip', 'seen_12oct_zip', 'captured_24nov_crawl', 'in_sitemap_now', 'status_now', 'content_doc'])
    for u, e in sorted(U.items()):
        s = st(u) or ('200' if e['nov'] else '')
        slug = next((k for k, d in pages.items() if norm(d['url']) == u), '')
        w.writerow([u, e['title'], 'yes' if e['captured_oct'] else '', 'yes' if e['oct'] else '', 'yes' if e['nov'] else '', 'yes' if u in sitemap else 'no', s, f'content/{slug}.md' if slug else ''])
for f in sorted(glob.glob('data/combined/*.csv')):
    print(f, sum(1 for _ in open(f)) - 1, 'rows')
