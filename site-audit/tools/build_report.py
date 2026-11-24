"""Build markdown docs from crawl JSON. Usage: python3 -I build_report.py <site-audit dir> <raw dir>"""
import json, os, sys, re, csv, html, base64, glob
from collections import Counter, defaultdict, OrderedDict
from urllib.parse import unquote, urlparse

OUT, RAW = sys.argv[1], sys.argv[2]
P = lambda *a: os.path.join(OUT, *a)
os.makedirs(P('content'), exist_ok=True)

pages = {}
for f in sorted(glob.glob(P('data/pages/*.json'))):
    d = json.load(open(f))
    pages[d['slug']] = d
summary = json.load(open(P('data/crawl-summary.json')))
popups = json.load(open(P('data/popups.json'))) if os.path.exists(P('data/popups.json')) else {}
wp_pages = {p['link']: p for p in json.load(open(os.path.join(RAW, 'wp_pages.json')))}
media_rows = list(csv.DictReader(open(P('data/media-library.csv'))))
media_by_url = {r['source_url']: r for r in media_rows}
linkcheck = {}
if os.path.exists(P('data/link-check.csv')):
    for r in csv.DictReader(open(P('data/link-check.csv'))):
        linkcheck[r['url']] = r

# lightbox video URLs per widget data-id, parsed from raw HTML
lightbox_by_id = {}
for f in glob.glob(P('backend/raw-html/*.html')):
    if f.endswith('.rest-content.html'): continue
    t = open(f).read()
    parts = re.split(r'(?=<div[^>]+data-id="[0-9a-f]+"[^>]+data-element_type="widget")', t)
    for part in parts:
        m = re.match(r'<div[^>]+data-id="([0-9a-f]+)"[^>]+data-widget_type="video\.default"', part)
        lb = re.search(r'data-elementor-lightbox="([^"]+)"', part)
        if m and lb:
            try: lightbox_by_id[m[1]] = json.loads(html.unescape(lb[1])).get('url')
            except Exception: pass

ORDER = ['home', 'about-us', 'case-studies', 'contact-us', 'website-portfolio', 'mmag-portfolio', 'under-development', 'hello-world']
def sort_key(s):
    return (ORDER.index(s) if s in ORDER else 50, s)
slugs = sorted(pages, key=sort_key)

ALL_BP = {'widescreen', 'desktop', 'laptop', 'tablet_extra', 'tablet', 'mobile_extra', 'mobile'}

def rgb2hex(s):
    m = re.match(r'rgba?\((\d+), (\d+), (\d+)(?:, ([\d.]+))?\)', s.strip())
    if not m: return s
    r, g, b = int(m[1]), int(m[2]), int(m[3])
    a = m[4]
    hx = '#%02X%02X%02X' % (r, g, b)
    return hx + (f' @{float(a):.2f}' if a is not None and float(a) < 1 else '')

def local_asset(url):
    if not url: return None
    u = url.split('?')[0]
    r = media_by_url.get(u) or media_by_url.get(re.sub(r'-\d+x\d+(\.\w+)$', r'\1', u)) or media_by_url.get(re.sub(r'-scaled(\.\w+)$', r'\1', u))
    if r and r['local_path']: return '../' + r['local_path']
    return None

def spacer_alias(d):
    al = {}
    for sec in d['sections']:
        if 'elementor-sticky__spacer' in (sec.get('classes') or ''):
            al[f"{sec['doc']}#{sec['index']}"] = f"{sec['doc']}#{sec['index'] - 1}"
    return al

def decode_action(href):
    if not href or 'elementor-action' not in href: return None
    h = unquote(href)
    act = re.search(r'action=([a-z:]+)', h)
    st = re.search(r'settings=([A-Za-z0-9+/=]+)', h)
    s = {}
    if st:
        try: s = json.loads(base64.b64decode(st[1] + '==='))
        except Exception: pass
    a = act[1] if act else '?'
    if a == 'popup:open': return f'opens popup #{s.get("id")}' + (f' ({popups[str(s.get("id"))]["headings"][0].split(": ",1)[-1]})' if str(s.get('id')) in popups and popups[str(s.get('id'))].get('headings') else '')
    if a == 'lightbox': return f'opens {s.get("type")} lightbox: {s.get("url","").replace(chr(92),"")}'
    return f'{a} {s}'

def hidden_note(w):
    h = set(w.get('hiddenOn') or [])
    if not h: return ''
    if ALL_BP <= h: return ' _(HIDDEN on all devices — in page code only)_'
    return f' _(hidden on: {", ".join(sorted(h))})_'

def md_esc(t):
    return (t or '').replace('|', '\\|').replace('\n', ' / ')

def link_target(href, text=''):
    if not href: return '(no link)'
    da = decode_action(href)
    if da: return da
    return href

def render_widget(w):
    t = w['type'].split('.')[0]
    hn = hidden_note(w)
    anim = f" `anim:{w['animation']}`" if w.get('animation') and w['animation'] not in ('none', '') else ''
    if t == 'heading':
        tag = w.get('tag') or ''
        txt = (w.get('text') or '').replace('\n', ' / ')
        return f"- **{tag}:** {txt}{' → ' + w['href'] if w.get('href') else ''}{hn}{anim}"
    if t == 'text-editor':
        txt = (w.get('text') or '').strip()
        return '\n'.join(['- Text:' + hn + anim] + ['  > ' + l for l in txt.split('\n') if l.strip()])
    if t == 'button':
        txt = w.get('text') or '(icon only' + (f": {w['icon']}" if w.get('icon') else '') + ')'
        return f"- **Button:** \"{txt}\" → {link_target(w.get('href'))}{hn}"
    if t in ('image', 'theme-site-logo', 'site-logo'):
        im = w.get('image') or {}
        src = im.get('currentSrc') or im.get('src')
        la = local_asset(im.get('src'))
        alt = im.get('alt') or ''
        return f"- Image: `{src}`{' (local: ' + la + ')' if la else ''} — {im.get('w')}×{im.get('h')} — alt: {('\"' + alt + '\"') if alt else '**missing**'}{' → ' + w['href'] if w.get('href') else ''}{hn}{anim}"
    if t == 'image-box':
        im = w.get('image') or {}
        return f"- Image box: **{w.get('title')}** — {w.get('description')} — img `{im.get('currentSrc') or im.get('src')}`{' → ' + w['href'] if w.get('href') else ''}{hn}"
    if t == 'icon-box':
        ic = w.get('icon') or ''
        ic = 'inline SVG' if ic.startswith('<svg') else ic
        return f"- Icon box: **{w.get('title')}** — {w.get('description')} _(icon: {ic})_{' → ' + w['href'] if w.get('href') else ''}{hn}"
    if t == 'icon-list':
        items = w.get('items') or []
        return '\n'.join([f'- Icon list:{hn}'] + [f"  - {i['text']}{' → ' + i['href'] if i.get('href') else ''}" for i in items])
    if t == 'icon':
        return f"- Icon ({w.get('icon')}){' → ' + w['href'] if w.get('href') else ''}{hn}"
    if t == 'counter':
        return f"- **Counter:** {w.get('prefix') or ''}{w.get('number')}{w.get('suffix') or ''} — {w.get('title')} (animates from {w.get('from')}){hn}"
    if t == 'video':
        v = w.get('video') or {}
        s = w.get('settings') or {}
        src = v.get('src') or s.get('youtube_url') or s.get('hosted_url') or w.get('iframe') or lightbox_by_id.get(w['id'])
        if s.get('lightbox') == 'yes' and lightbox_by_id.get(w['id']):
            mr = media_by_url.get(lightbox_by_id[w['id']])
            return f"- Video (thumbnail → opens in lightbox): `{lightbox_by_id[w['id']]}`{', ' + str(round(float(mr['filesize_kb'])/1024,1)) + ' MB' if mr and mr['filesize_kb'] else ''} — thumbnail `{s.get('image_overlay')}`{hn}"
        flags = ', '.join(k for k in ('autoplay', 'loop', 'muted', 'controls') if v.get(k))
        mr = media_by_url.get((src or '').split('?')[0])
        size = f", {round(float(mr['filesize_kb'])/1024,1)} MB" if mr and mr['filesize_kb'] else ''
        return f"- Video: `{src}` ({s.get('video_type')}; {flags}{size}){hn}"
    if t == 'image-carousel':
        sl = w.get('slides') or []
        st = w.get('settings') or {}
        lines = [f"- Image carousel — {len(sl)} slides (autoplay: {st.get('autoplay')}, speed: {st.get('speed')}, per view: {st.get('slides_to_show')}){hn}"]
        for s in sl:
            lines.append(f"  - `{s.get('currentSrc') or s.get('src') or '(lazy image, never loaded because hidden)'}` alt: {('\"' + s['alt'] + '\"') if s.get('alt') else '**missing**'}{' → ' + s['link'] if s.get('link') else ''}")
        return '\n'.join(lines)
    if t in ('nested-carousel', 'loop-carousel'):
        sl = w.get('slides') or []
        st = w.get('settings') or {}
        return f"- **Carousel ({t})** — {len(sl)} slides (autoplay: {st.get('autoplay')}){hn} — each slide's widgets follow"
    if t == 'social-icons':
        return '\n'.join([f'- Social icons:{hn}'] + [f"  - {i.get('label') or i.get('icon')} → {i['href']}" for i in w.get('items') or []])
    if t == 'nav-menu':
        return '\n'.join([f'- Nav menu:{hn}'] + [f"  - {'  ' * i['depth']}{i['text']} → {i['href']}" for i in w.get('items') or []])
    if t == 'html':
        txt = (w.get('text') or '')
        kind = 'custom CSS/JS' if re.search(r'[{};]\s*$|<script|@media|#[a-zA-Z]+\s*\{', (w.get('html') or '')[:600]) else 'custom HTML'
        snippet = re.sub(r'\s+', ' ', txt)[:160]
        return f"- HTML widget ({kind}): `{md_esc(snippet)}…`{hn} — full code in `data/pages/<slug>.json`"
    if t == 'form':
        return f"- **Form:** {w.get('formName')} — fields listed in Forms section{hn}"
    if t == 'divider':
        return f"- Divider{(': ' + w['text']) if w.get('text') else ''}" if w.get('text') else None
    if t == 'template':
        return f"- Embedded template #{', '.join(w.get('templateIds') or [])} (shared block — content follows){hn}"
    if t in ('spacer',):
        return None
    txt = (w.get('text') or '').replace('\n', ' / ')[:500]
    return f"- {w['type']}: {txt}{hn}"

def section_label(sec):
    hs = sec.get('headings') or []
    if hs: return hs[0].split(': ', 1)[-1].replace('\n', ' ')[:70]
    if sec.get('cssId'): return '#' + sec['cssId']
    return (sec.get('text') or '')[:50].replace('\n', ' ') or '(visual only)'

def meta_val(d, name):
    for m in d['meta']:
        if m['name'] == name: return m['content']
    return None

# ---------------- per-page content docs ----------------
page_index_rows = []
for slug in slugs:
    d = pages[slug]
    wp = wp_pages.get(d['url']) or {}
    L = []
    title = d['title']
    L.append(f"# {title}\n")
    desc = meta_val(d, 'description')
    h1s = [h['text'].replace('\n', ' / ') + (' _(theme page title, display:none — not visible)_' if h['region'] == 'other' else '') for h in d['headings'] if h['level'] == 'H1']
    L.append('| Field | Value |\n|---|---|')
    rows = [
        ('URL', d['url']), ('HTTP status', d['httpStatus']), ('Title tag', f"{title} ({len(title)} chars)"),
        ('Meta description', f"{desc} ({len(desc)} chars)" if desc else '**missing**'),
        ('Canonical', next((l['href'] for l in d['headLinks'] if l['rel'] == 'canonical'), 'missing')),
        ('Robots', meta_val(d, 'robots')), ('OG image', meta_val(d, 'og:image') or 'missing'),
        ('H1', ' · '.join(h1s) if h1s else '**missing**'), ('Words (visible)', len(d['bodyText'].split())),
        ('Page height (desktop)', f"{d['pageHeight']} px"),
        ('WordPress page ID / published / modified', f"{wp.get('id', '-')} / {wp.get('date', '-')[:10]} / {wp.get('modified', '-')[:10]}"),
        ('Load timing (TTFB / DOMContentLoaded / load)', f"{d['timing']['ttfb']} / {d['timing']['domContentLoaded']} / {d['timing']['load']} ms" if d.get('timing') else '-'),
        ('Requests / transfer', f"{d['network']['requests']} requests / {round(d['network']['totalKB']/1024,1)} MB"),
        ('Screenshots', f"[desktop](../screenshots/desktop/{slug}.jpg) · [desktop fold](../screenshots/desktop/{slug}-fold.png) · [mobile](../screenshots/mobile/{slug}.jpg)"),
    ]
    for k, v in rows: L.append(f'| {k} | {md_esc(str(v))} |')
    L.append('\nHeader, footer, popups and site-wide elements: see [../shared-layout.md](../shared-layout.md).\n')

    # widgets grouped by section
    wsec = d.get('widgetSection') or {}
    alias = spacer_alias(d)
    by_sec = defaultdict(list)
    for w in d['widgets']:
        if w['region'] != 'main': continue
        key = wsec.get(w['id'], 'unmapped'); key = alias.get(key, key)
        by_sec[key].append(w)
    main_secs = [s for s in d['sections'] if (s['doc'].startswith('wp-page') or s['doc'].startswith('wp-post') or s['doc'].startswith('single')) and 'elementor-sticky__spacer' not in (s.get('classes') or '')]
    L.append('## Page content (top to bottom)\n')
    L.append('Legend: `anim:` = entrance animation · _(hidden on …)_ = Elementor responsive visibility · HIDDEN on all devices = content exists in the page builder but no visitor sees it.\n')
    for n, sec in enumerate(main_secs, 1):
        key = f"{sec['doc']}#{sec['index']}"
        bgc = [rgb2hex(b['color']) for b in sec['background'] if b['color'] and b['color'] != 'rgba(0, 0, 0, 0)']
        bgi = [b['image'][:120] for b in sec['background'] if b.get('image')]
        meta = []
        if sec.get('cssId'): meta.append(f"id `#{sec['cssId']}`")
        if bgc: meta.append('bg ' + ', '.join(dict.fromkeys(bgc)))
        if bgi: meta.append('bg image ' + ', '.join(bgi))
        if sec.get('backgroundVideo'): meta.append('bg video ' + sec['backgroundVideo'])
        meta.append(f"height {sec['height']}px")
        hs = set(sec.get('hiddenOn') or [])
        hid = ' — **HIDDEN on all devices**' if ALL_BP <= hs else (f" — hidden on {', '.join(sorted(hs))}" if hs else '')
        L.append(f"### Section {n}: {section_label(sec)}{hid}\n")
        L.append(f"_{' · '.join(meta)}_\n")
        ws = by_sec.get(key, [])
        if not ws:
            L.append('- ' + (sec.get('text') or '(no widgets)').replace('\n', ' / ')[:1500])
        for w in ws:
            r = render_widget(w)
            if r: L.append(r)
            t = w['type'].split('.')[0]
            if t in ('nested-carousel', 'loop-carousel') and not any(x.get('insideWidget', '') and x['insideWidget'].startswith(t) for x in ws):
                for i, s in enumerate(w.get('slides') or [], 1):
                    L.append(f"  - Slide {i}: " + s.replace('\n', ' / ')[:600])
        L.append('')
    if by_sec.get('unmapped'):
        L.append('### Unmapped widgets\n')
        for w in by_sec['unmapped']:
            r = render_widget(w)
            if r: L.append(r)
    # forms on page
    forms = [f for f in d['forms'] if f['region'] == 'main']
    if forms:
        L.append('## Forms on this page\n')
        for f in forms:
            L.append(f"**{f['name'] or f['id'] or 'form'}** — submit: {', '.join(f['submit'])} — reCAPTCHA: {'yes' if f['hasRecaptcha'] else 'no'}\n")
            L.append('| Label | Type | Name | Placeholder | Required | Options |\n|---|---|---|---|---|---|')
            for x in f['fields']:
                if x['type'] in ('hidden', 'submit'): continue
                L.append(f"| {md_esc(x['label'] or '')} | {x['type']} | {x['name']} | {md_esc(x['placeholder'] or '')} | {'yes' if x['required'] else ''} | {md_esc(', '.join(x.get('options') or []))} |")
            L.append('')
    # interaction tests
    inter = [i for i in d.get('interactions', []) if i['action'] in ('click-trigger', 'carousel', 'click-tab', 'form-validation-check (not submitted)')]
    if inter:
        L.append('## Interaction tests (desktop)\n')
        for i in inter:
            if i['action'] == 'click-trigger':
                if i.get('error'): continue
                o = i.get('opened')
                L.append(f"- Clicked \"{i.get('label')}\" → " + (f"{o['kind']} opened ({(o.get('text') or '').split(chr(10))[0][:80]}{'; media: ' + o['media'] if o.get('media') else ''})" if o else f"no popup; scroll position {i.get('scrollY')}"))
            elif i['action'] == 'carousel':
                L.append(f"- Carousel `{i.get('widget')}`: " + (i.get('note') or (f"next arrow {'present' if i.get('hasNextArrow') else 'absent'}; slide index {i.get('indexBefore')} → {i.get('indexAfter')}" if not i.get('error') else 'error ' + i['error'][:80])))
            elif i['action'] == 'click-tab':
                if not i.get('error'): L.append(f"- Tab/accordion \"{i.get('title')}\" → shows: {(i.get('content') or '')[:200]}")
            else:
                L.append(f"- Form `{i.get('name')}` empty-state validation (not submitted): {len(i.get('invalid') or [])} required fields flagged")
        L.append('')
    mi = d.get('mobileInteractions') or []
    L.append('## Mobile (390 px)\n')
    for m in mi:
        if m.get('items'): L.append('- Hamburger menu opens with: ' + ', '.join(f"{x['text']} → {x['href']}" for x in m['items']))
        elif m.get('note'): L.append('- ' + m['note'])
    L.append(f"- Horizontal overflow: {'**yes — page is ' + str(d['mobileHorizontalOverflow']) + 'px wide**' if d.get('mobileHorizontalOverflow') else 'none'}")
    L.append(f"- Headings visible on mobile: {len(d.get('mobileHeadings') or [])}\n")
    # images list
    imgs = [i for i in d['images'] if i['region'] == 'main']
    if imgs:
        L.append('## Images on this page (main content)\n')
        L.append('| # | Image | Alt text | Natural size | Local copy |\n|---|---|---|---|---|')
        seen = set()
        for i in imgs:
            u = i.get('currentSrc') or i.get('src')
            if not u or u in seen: continue
            seen.add(u)
            la = local_asset(i.get('src')) or ''
            L.append(f"| {len(seen)} | {u} | {md_esc(i.get('alt')) if i.get('alt') else '**missing**'} | {i.get('w')}×{i.get('h')} | {la} |")
        L.append('')
    bgs = [b for b in d['backgroundImages'] if b['region'] == 'main']
    if bgs:
        L.append('**CSS background images:** ' + ', '.join(f"`{b['url']}`" for b in bgs) + '\n')
    vids = [v for v in d['videos'] if v['region'] == 'main']
    if vids:
        L.append('## Videos on this page\n')
        for v in {v['src']: v for v in vids}.values():
            mr = media_by_url.get((v['src'] or '').split('?')[0])
            L.append(f"- `{v['src']}` — {'autoplay ' if v['autoplay'] else ''}{'loop ' if v['loop'] else ''}{'muted ' if v['muted'] else ''}{'controls' if v['controls'] else 'no controls'}{(' — ' + str(round(float(mr['filesize_kb'])/1024,1)) + ' MB') if mr and mr['filesize_kb'] else ''}")
        L.append('')
    # links
    links = [l for l in d['links'] if l['region'] == 'main']
    if links:
        L.append('## Links in main content\n')
        L.append('| Text | Target | Opens in | Status |\n|---|---|---|---|')
        seen = set()
        for l in links:
            k = (l['text'], l['href'])
            if k in seen: continue
            seen.add(k)
            st = linkcheck.get(l['abs'], {}).get('status', '')
            L.append(f"| {md_esc(l['text'] or l.get('aria') or '(no text)')} | {md_esc(link_target(l['href']))} | {'new tab' if l.get('target') == '_blank' else 'same tab'} | {st} |")
        L.append('')
    # seo
    L.append('## Heading outline (main content, in DOM order)\n')
    L.append('| Level | Heading |\n|---|---|')
    for h in d['headings']:
        if h['region'] not in ('main', 'other'): continue
        note = ' _(theme title, display:none)_' if h['region'] == 'other' else hidden_note(h)
        L.append(f"| {h['level']} | {'&nbsp;&nbsp;' * (int(h['level'][1]) - 1)}{md_esc(h['text'])}{note} |")
    L.append('')
    if d.get('jsonld'):
        types = []
        for j in d['jsonld']:
            if isinstance(j, dict):
                for g in j.get('@graph', [j]): types.append(g.get('@type') if isinstance(g.get('@type'), str) else ','.join(g.get('@type') or []))
        L.append('**Schema (JSON-LD) types:** ' + ', '.join(types) + '\n')
    if d.get('consoleErrors'):
        L.append('**Console errors:** ' + '; '.join(dict.fromkeys(d['consoleErrors']))[:600] + '\n')
    open(P('content', f'{slug}.md'), 'w').write('\n'.join(L))
    page_index_rows.append((slug, d))

print('content docs:', len(slugs))

# ---------------- shared layout (header/footer/popups) ----------------
home = pages.get('home') or pages[slugs[0]]
L = ['# Shared layout — header, footer, popups, site-wide behaviour\n', f'Source page: {home["url"]} (header #47 and footer #619 are the same Elementor templates on every page).\n']
done_ids = set()
for region, title in (('header', 'Header (Elementor template #47) — sticky, white, 82px tall; logo left, menu centre, CTA right'), ('footer', 'Footer (Elementor template #619)')):
    L.append(f'## {title}\n')
    secs = [s for s in home['sections'] if s['doc'].startswith(region) and 'elementor-sticky__spacer' not in (s.get('classes') or '')]
    alias = spacer_alias(home)
    for s in secs:
        hs = set(s.get('hiddenOn') or [])
        bgc = [rgb2hex(b['color']) for b in s['background'] if b['color'] != 'rgba(0, 0, 0, 0)']
        L.append(f"### {region.title()} row {s['index']+1}{' — hidden on ' + ', '.join(sorted(hs)) if hs else ''}\n_height {s['height']}px{' · bg ' + ', '.join(dict.fromkeys(bgc)) if bgc else ''}_\n")
        key = f"{s['doc']}#{s['index']}"
        for w in home['widgets']:
            k2 = (home.get('widgetSection') or {}).get(w['id']); k2 = alias.get(k2, k2)
            if k2 == key and w['region'] == region and w['id'] not in done_ids:
                done_ids.add(w['id'])
                r = render_widget(w)
                if r: L.append(r)
        L.append('')
    L.append(f'**All {region} links:**\n')
    seen = set()
    for l in home['links']:
        if l['region'] == region and (l['text'], l['href']) not in seen:
            seen.add((l['text'], l['href']))
            L.append(f"- {l['text'] or l.get('aria') or '(icon/logo)'} → {link_target(l['href'])}{' (new tab)' if l.get('target') == '_blank' else ''}{'' if l['visible'] else ' _(not visible on desktop)_'}")
    L.append('')
L.append('## Popups (Elementor popup templates)\n')
if not popups:
    L.append('_No popup data captured._\n')
for pid, p in popups.items():
    L.append(f"### Popup #{pid} — triggered by \"{p['trigger']}\"\n")
    L.append(f"_size {p.get('size')} · bg {rgb2hex(p['bg']) if p.get('bg') else '-'} · radius {p.get('radius')}_ · [screenshot](screenshots/interactions/popup-{pid}.png)\n")
    L.append('Headings: ' + ' · '.join(p.get('headings') or []) + '\n')
    L.append('Visible text:\n')
    L.append('```\n' + p.get('text', '')[:2500] + '\n```\n')
    for f in p.get('forms') or []:
        L.append(f"**Form `{f['name']}`** — submit: {', '.join(f['submit'])} — reCAPTCHA: {'yes' if f['recaptcha'] else 'no'}\n")
        L.append('| Label | Type | Name | Placeholder | Required | Options |\n|---|---|---|---|---|---|')
        for x in f['fields']:
            L.append(f"| {md_esc(x['label'] or '')} | {x['type']} | {x['name']} | {md_esc(x['placeholder'] or '')} | {'yes' if x['required'] else ''} | {md_esc(', '.join(x.get('options') or [])[:300])} |")
        L.append('')
    if p.get('images'):
        L.append('Images: ' + ', '.join(f"`{i['src']}`" for i in p['images']) + '\n')
# triggers across site
trig = OrderedDict()
for s in slugs:
    for i in pages[s].get('interactions', []):
        if i['action'] == 'click-trigger' and not i.get('error'):
            k = (i.get('label'), i.get('href'))
            trig.setdefault(k, {'pages': [], 'i': i})['pages'].append(s)
L.append('## Every popup / lightbox trigger found\n')
L.append('| Button text | Action | Result when clicked | Pages |\n|---|---|---|---|')
for (lab, href), v in trig.items():
    o = v['i'].get('opened')
    L.append(f"| {md_esc(lab)} | {md_esc(decode_action(href) or href)} | {(o['kind'] + ' opened') if o else 'nothing opened'} | {', '.join(v['pages'])} |")
L.append('')
# scroll behaviours
sb = next((i for i in home.get('interactions', []) if i['action'] == 'scroll-behaviour'), None)
L.append('## Site-wide behaviour (tested on desktop 1440 px)\n')
if sb:
    L.append(f"- **Sticky header:** at top → position `{sb['headerAtTop'].get('position')}`, bg {rgb2hex(sb['headerAtTop'].get('bg',''))}, height {round(sb['headerAtTop'].get('height',0))}px. After scrolling 1600px → sticky active: {sb['headerAfterScroll1600'].get('stickyActive')}, shadow `{sb['headerAfterScroll1600'].get('shadow')}`. [screenshot](screenshots/interactions/home-scrolled-header.png)")
    L.append(f"- **Custom cursor image** (`#cursor-image`): {'present' if sb.get('cursorImage') else 'not found'} — follows the mouse on desktop (HTML widget with JS).")
    L.append(f"- **Scroll progress line** (`#progressLine`): {'present' if sb.get('progressLine') else 'not found'} — drives the 'What we build' timeline animation.")
    L.append("- **Back-to-top button:** icon-only button in the footer bar (href `#`); the footer HTML widget adds `body.show` after 300px of scroll to reveal it. Clicking it jumps to the top (tested).")
navh = [i for i in home.get('interactions', []) if i['action'] == 'hover-nav']
L.append(f"- **Desktop nav hover:** {len(navh)} items, dropdown sub-menus: {sum(len(i.get('sub') or []) for i in navh)} (none).")
mm = (home.get('mobileInteractions') or [{}])[0]
L.append(f"- **Mobile hamburger menu:** items {', '.join(x['text'] for x in mm.get('items') or [])}. [screenshot](screenshots/interactions/home-mobile-menu.png)")
st = home['components'].get('stickyElements')
if st: L.append(f"- Sticky element settings: `{json.dumps(st)}`")
fb = home['components'].get('floatingButtons')
L.append(f"- **Floating buttons (WhatsApp/chat):** {'found: ' + json.dumps(fb)[:300] if fb else 'none rendered on the page'}")
L.append('')
L.append('## Custom code embedded in pages (HTML widgets / inline scripts)\n')
L.append('Saved verbatim in `backend/custom-code/`. These power the GSAP scroll timeline, custom cursor, progress line and scroll-offset behaviour.\n')
open(P('shared-layout.md'), 'w').write('\n'.join(L))

# save custom code
os.makedirs(P('backend/custom-code'), exist_ok=True)
seen_code = {}
BOILER = re.compile(r'elementorFrontendConfig|ElementorProFrontendConfig|JetTabsSettings|CCFEFCustomData|PremiumSettings|wp\.i18n|uiBackCompat|lazyloadRunObserver|wp-emoji|dataLayer|"@context"|sourceURL=|_wpemojiSettings|baseUrl":"https://s.w.org')
for s in slugs:
    for i, code in enumerate(pages[s].get('inlineScripts') or []):
        c = code.strip()
        if not c or BOILER.search(c[:400]) or len(c) < 40: continue
        h = hash(c)
        if h in seen_code: seen_code[h]['pages'].append(s); continue
        seen_code[h] = {'pages': [s], 'code': c, 'kind': 'js'}
    for w in pages[s]['widgets']:
        if w['type'].startswith('html') and w.get('html'):
            c = w['html']
            h = hash(c)
            if h in seen_code: seen_code[h]['pages'].append(s); continue
            seen_code[h] = {'pages': [s], 'code': c, 'kind': 'html-widget'}
idx = ['# Custom code index\n', '| File | Type | Pages | First line |', '|---|---|---|---|']
for n, (h, v) in enumerate(seen_code.items(), 1):
    fn = f"{n:02d}-{v['kind']}.{'js' if v['kind'] == 'js' else 'html'}"
    open(P('backend/custom-code', fn), 'w').write(v['code'])
    idx.append(f"| [{fn}]({fn}) | {v['kind']} | {', '.join(sorted(set(v['pages'])))} | `{md_esc(re.sub(chr(92)+'s+', ' ', v['code'])[:90])}` |")
open(P('backend/custom-code/README.md'), 'w').write('\n'.join(idx))

# ---------------- style tally (brand) ----------------
colors, fonts, sizes = Counter(), Counter(), Counter()
for s in slugs:
    t = pages[s]['styleTally']
    for k, v in t['colors'].items():
        kind, val = k.split(' ', 1)
        if kind == 'gradient': colors[('gradient', val)] += v
        else: colors[(kind, rgb2hex(val))] += v
    fonts.update(t['fonts']); sizes.update(t['sizes'])
bt = OrderedDict()
for s in slugs:
    for i in pages[s].get('interactions', []):
        if i['action'] == 'hover-button':
            b = i['before']; a = i['after']
            k = (b['bg'], b['color'], b['radius'], b['font'], b['padding'])
            if k not in bt: bt[k] = (b, a, s)
json.dump({'colors': [[k[0], k[1], v] for k, v in colors.most_common()], 'fonts': fonts.most_common(), 'typeSizes': sizes.most_common(60),
           'buttons': [{'before': b, 'after': a, 'page': s} for b, a, s in bt.values()]}, open(P('data/style-tally.json'), 'w'), indent=1)

# ---------------- assets ----------------
img_use = defaultdict(set); vid_use = defaultdict(set); alt_of = {}
for s in slugs:
    for i in pages[s]['images']:
        u = (i.get('currentSrc') or i.get('src') or '')
        if u: img_use[u].add(s); alt_of.setdefault(u, i.get('alt'))
    for b in pages[s]['backgroundImages']:
        img_use[b['url']].add(s)
    for v in pages[s]['videos']:
        if v['src']: vid_use[v['src']].add(s)
    for w in pages[s]['widgets']:
        if w['type'].startswith('video'):
            u = (w.get('video') or {}).get('src') or (w.get('settings') or {}).get('hosted_url') or (w.get('settings') or {}).get('youtube_url') or lightbox_by_id.get(w['id'])
            if u: vid_use[u].add(s)
with open(P('data/assets-used.csv'), 'w', newline='') as fh:
    w = csv.writer(fh); w.writerow(['type', 'url', 'alt_text', 'pages', 'in_media_library', 'local_copy'])
    for u, ps in sorted(img_use.items()):
        w.writerow(['image', u, alt_of.get(u) or '', ' '.join(sorted(ps)), 'yes' if u.split('?')[0] in media_by_url else 'no', (local_asset(u) or '').replace('../', '')])
    for u, ps in sorted(vid_use.items()):
        w.writerow(['video', u, '', ' '.join(sorted(ps)), 'yes' if u.split('?')[0] in media_by_url else 'no', ''])
_n = lambda u: re.sub(r'-(\d+x\d+|scaled)(\.\w+)$', r'\2', u.split('?')[0])
used_urls = set(_n(u) for u in img_use) | set(_n(u) for u in vid_use)
for s_ in slugs:
    for w in pages[s_]['widgets']:
        im = (w.get('settings') or {}).get('image_overlay')
        if im: used_urls.add(_n(im))
json.dump({'images_used': len(img_use), 'videos_used': len(vid_use), 'media_library': len(media_rows),
           'media_unused': [r['source_url'] for r in media_rows if _n(r['source_url']) not in used_urls]}, open(P('data/assets-summary.json'), 'w'), indent=1)

# ---------------- links ----------------
all_links = defaultdict(lambda: {'pages': set(), 'texts': set(), 'regions': set(), 'target': None})
for s in slugs:
    for l in pages[s]['links']:
        k = l['abs'] if not l['href'].startswith('#') else l['href']
        e = all_links[k]; e['pages'].add(s); e['texts'].add((l['text'] or l.get('aria') or '').strip()[:60]); e['regions'].add(l['region']); e['target'] = l.get('target')
with open(P('data/links-all.csv'), 'w', newline='') as fh:
    w = csv.writer(fh); w.writerow(['url', 'kind', 'link_texts', 'regions', 'opens_new_tab', 'pages', 'status', 'final_url'])
    for u, e in sorted(all_links.items()):
        kind = 'action' if 'elementor-action' in u else 'anchor' if u.startswith('#') or '#' in u and urlparse(u).path in ('', '/') and urlparse(u).fragment else 'mailto' if u.startswith('mailto:') else 'tel' if u.startswith('tel:') else 'internal' if 'mmag.in' in urlparse(u).netloc else 'external'
        lc = linkcheck.get(u, {})
        w.writerow([u, kind, ' | '.join(sorted(t for t in e['texts'] if t)), ' '.join(sorted(e['regions'])), 'yes' if e['target'] == '_blank' else '', ' '.join(sorted(e['pages'])), lc.get('status', ''), lc.get('final', '')])
print('done')
