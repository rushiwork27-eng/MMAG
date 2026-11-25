"""Build a readable 'content record' HTML for an archived page from its extracted JSON.
Usage: python3 -I archive_record.py <page.json> <out.html>
The record shows content in DOM order (headings, text, images, stats, lists, links). It does NOT reproduce the original layout."""
import json, sys, html

d = json.load(open(sys.argv[1]))
REMOVED = {'https://mmag.in/case-studies/zendale', 'https://mmag.in/work/zendale', 'https://mmag.in/work', 'https://mmag.in/case-studies/yash-industries', 'https://mmag.in/case-studies/equinext'}
esc = lambda s: html.escape(s or '')
ALL = {'widescreen', 'desktop', 'laptop', 'tablet_extra', 'tablet', 'mobile_extra', 'mobile'}
out, imgs = [], []

def flush_imgs():
    global imgs
    if imgs:
        cls = 'grid' if len(imgs) > 1 else 'single'
        out.append(f'<div class="{cls}">' + ''.join(f'<figure><img src="{esc(u)}" alt="{esc(a)}" loading="eager"><figcaption>{esc(u.rsplit("/",1)[-1])}</figcaption></figure>' for u, a in imgs) + '</div>')
        imgs = []

for w in d['widgets']:
    if w['region'] != 'main':
        continue
    t = w['type'].split('.')[0]
    hidden = ALL <= set(w.get('hiddenOn') or [])
    tag = ' <span class="hid">hidden on all devices</span>' if hidden else ''
    if t in ('image', 'image-box') and (w.get('image') or {}).get('src'):
        im = w['image']
        imgs.append((im.get('currentSrc') or im.get('src'), im.get('alt')))
        if t == 'image-box':
            flush_imgs(); out.append(f'<h4>{esc(w.get("title"))}</h4><p>{esc(w.get("description"))}</p>')
        continue
    if t == 'video':
        flush_imgs(); s = w.get('settings') or {}
        out.append(f'<p class="meta">Video: {esc((w.get("video") or {}).get("src") or s.get("youtube_url") or s.get("hosted_url") or "")}</p>')
        continue
    flush_imgs()
    if t == 'heading':
        lvl = {'H1': 'h1', 'H2': 'h2', 'H3': 'h3'}.get(w.get('tag'), 'h4')
        out.append(f'<{lvl}>{esc(w.get("text")).replace(chr(10), "<br>")}{tag}<span class="lvl">{esc(w.get("tag"))}</span></{lvl}>')
    elif t == 'text-editor':
        out.append('<div class="text">' + ''.join(f'<p>{esc(l)}</p>' for l in (w.get('text') or '').split('\n') if l.strip()) + tag + '</div>')
    elif t == 'counter':
        out.append(f'<div class="stat"><b>{esc(w.get("prefix"))}{esc(w.get("number"))}{esc(w.get("suffix"))}</b><span>{esc(w.get("title"))}</span></div>')
    elif t in ('icon-list',):
        out.append('<ul>' + ''.join(f'<li>{esc(i["text"])}{" → " + esc(i["href"]) if i.get("href") else ""}</li>' for i in w.get('items') or []) + '</ul>')
    elif t == 'icon-box':
        out.append(f'<h4>{esc(w.get("title"))}</h4><p>{esc(w.get("description"))}</p>')
    elif t == 'button':
        out.append(f'<p class="btn">Button: “{esc(w.get("text") or "(icon)")}” → {esc(w.get("href") or "no link")}</p>')
    elif t in ('testimonial', 'blockquote'):
        out.append(f'<blockquote>{esc(w.get("text"))}</blockquote>')
    elif t in ('divider', 'spacer', 'icon', 'html', 'shortcode', 'template'):
        if t == 'shortcode' and w.get('text'):
            out.append(f'<p class="meta">{esc(w["text"])}</p>')
        continue
    elif w.get('text'):
        out.append(f'<p>{esc(w["text"])}</p>')
flush_imgs()
# links in main content that are cards (Explore more)
cards = [l for l in d['links'] if l['region'] == 'main' and l['abs'].startswith('https://mmag.in/') and l['text']]
if cards:
    out.append('<h3>Links on this page<span class="lvl">record</span></h3><ul>' + ''.join(f'<li>{esc(l["text"])} → {esc(l["abs"])}{" <span class=dead>now 404</span>" if l["abs"].rstrip("/") in REMOVED else " <span class=live>live</span>"}</li>' for l in {l["abs"]: l for l in cards}.values()) + '</ul>')

page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{esc(d['title'])} (archived)</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;700&display=swap" rel="stylesheet">
<style>
body{{margin:0;background:#FAF9F5;color:#5C5C5C;font:17px/1.6 system-ui,sans-serif}}
.banner{{background:#F3C01F;color:#1E1E1E;font-weight:600;padding:16px 32px;text-align:center}}
header{{background:#54078B;color:#fff;padding:28px 0}} header div,main{{max-width:1040px;margin:0 auto;padding:0 32px}}
header h1{{color:#fff!important;margin:0;font:700 34px/1.2 'Plus Jakarta Sans',sans-serif}} header p{{margin:6px 0 0;opacity:.85}}
main{{padding-top:24px;padding-bottom:64px}}
h1,h2,h3,h4{{font-family:'Plus Jakarta Sans',sans-serif;color:#171717;margin:28px 0 8px;line-height:1.25}} h2{{font-size:28px}} h3{{font-size:22px}} h4{{font-size:18px}}
.lvl{{font:500 11px system-ui;color:#7B7B7B;border:1px solid #E5E2EC;border-radius:6px;padding:1px 6px;margin-left:10px;vertical-align:middle}}
.hid{{font:600 11px system-ui;color:#fff;background:#3A0561;border-radius:6px;padding:1px 6px;margin-left:8px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px;margin:16px 0}} .single{{margin:16px 0}}
figure{{margin:0;background:#fff;border:1px solid #E5E2EC;border-radius:12px;padding:10px}} img{{max-width:100%;max-height:520px;display:block;margin:0 auto}}
figcaption{{font-size:12px;color:#7B7B7B;margin-top:6px;word-break:break-all}}
.stat{{display:inline-flex;flex-direction:column;background:#fff;border:1px solid #E5E2EC;border-radius:12px;padding:14px 22px;margin:8px 12px 8px 0;min-width:180px}}
.stat b{{font:700 34px 'Plus Jakarta Sans',sans-serif;color:#54078B}}
blockquote{{border-left:4px solid #F3C01F;margin:16px 0;padding:8px 18px;background:#fff}}
.live{{font-size:12px;color:#fff;background:#1F7A3D;border-radius:6px;padding:1px 6px}} .meta,.btn{{font-size:14px;color:#7B7B7B}} .dead{{font-size:12px;color:#fff;background:#B42318;border-radius:6px;padding:1px 6px}}
</style></head><body>
<div class="banner">ARCHIVED CONTENT RECORD, from the earlier scrape captured 12 Oct 2026. This page now returns 404 on mmag.in. Original layout could not be reproduced (its stylesheet was deleted); text and images below are original, in page order.</div>
<header><div><h1>{esc(d['title'])}</h1><p>{esc(d['url'])}</p></div></header>
<main>{''.join(out)}</main></body></html>"""
open(sys.argv[2], 'w').write(page)
print('record written', len(out), 'blocks')
