"""Build the MMAG static website into website/dist (unminified HTML).

Usage:  python3 build.py            (from website/build/)
Output: ../dist/  — drag-and-drop deployable folder (zip it for releases/)
"""
import html
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import (ADDRESS_LINES, CASES, CONTACT_INTERESTS, COUNTRY_CODES, EMAIL, FAQ_COMMON, INQUIRY_OPTIONS, LOCATION,
                     MAPS_URL, PHONE, PHONE_DISPLAY, PROCESS, SERVICES, SOCIALS, TEAM, TESTIMONIALS, WHATSAPP)
from images import (CARD_IMAGES, CASE_SERVICE, CULTURE, HOME_SERVICE_IMAGE, IMAGES, PROJECTS, RING_LOGOS, SERVICE_IMAGES,
                    SRC_ROOT, TEAM_PHOTOS, TESTIMONIAL_LOGOS, WALL)
from PIL import Image, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "src")
DIST = os.path.join(HERE, "..", "dist")
SITE = "https://mmag.in"
VERSION = os.environ.get("MMAG_VERSION", "dev")

E = html.escape
CASE_BY = {c["slug"]: c for c in CASES}

ARROW = '<svg class="arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
ARROW_UR = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17L17 7M8 7h9v9"/></svg>'
CLOSE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>'
PREV = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5M11 6l-6 6 6 6"/></svg>'
NEXT = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
WA_ICON = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.3 14.2c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .1-3.3-.8-2.8-1.1-4.5-4-4.7-4.2-.1-.2-1.1-1.5-1.1-2.8s.7-2 1-2.3c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 2c.1.2.1.4 0 .5l-.4.6-.3.4c-.1.1-.2.3-.1.5.2.3.7 1.1 1.4 1.8.9.8 1.7 1.1 2 1.2.2.1.4.1.5-.1l.7-.9c.2-.2.3-.2.5-.1l1.9.9c.3.1.4.2.5.3.1.2.1.8-.1 1.4z"/></svg>'

# image key -> (file name, width, height, alt); filled by process_images()
IMG = {}
# image key -> case slugs it must not appear on (case studies stay anonymous)
IMAGE_AVOID = {k: set(avoid) for _, _, _, keys, avoid in PROJECTS for k in keys}


def process_images():
    """Copy and resize the live site's images into dist/assets/img as WebP (logos keep transparency)."""
    out_dir = os.path.join(DIST, "assets", "img")
    os.makedirs(out_dir, exist_ok=True)
    for key, (src, width, alt, mode) in IMAGES.items():
        path = os.path.normpath(os.path.join(HERE, SRC_ROOT, src))
        if mode == "svg":
            shutil.copy(path, os.path.join(out_dir, key + ".svg"))
            IMG[key] = (key + ".svg", None, None, alt)
            continue
        im = Image.open(path)
        if mode == "og":
            im = im.convert("RGB")
            w, h = im.size
            target = 1200 / 630
            if w / h > target:
                nw = int(h * target)
                im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
            else:
                nh = int(w / target)
                im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
            im = im.resize((1200, 630), Image.LANCZOS)
            im.save(os.path.join(out_dir, "og.jpg"), quality=82, optimize=True)
            IMG[key] = ("og.jpg", 1200, 630, alt)
            continue
        if mode == "logo":
            im = im.convert("RGBA")
            flat = Image.alpha_composite(Image.new("RGBA", im.size, (255, 255, 255, 255)), im).convert("L")
            ink = flat.point(lambda v: 255 if v < 238 else 0)
            solid = im.split()[3].point(lambda v: 255 if v > 24 else 0)
            box = ImageChops.multiply(ink, solid).getbbox()
            if box:
                pad = max(2, int(max(im.size) * 0.03))
                im = im.crop((max(0, box[0] - pad), max(0, box[1] - pad), min(im.width, box[2] + pad), min(im.height, box[3] + pad)))
        else:
            im = im.convert("RGB")
        if width and im.width > width:
            im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
        name = key + ".webp"
        im.save(os.path.join(out_dir, name), "WEBP", quality=90 if mode == "logo" else 72, method=6)
        IMG[key] = (name, im.width, im.height, alt)
    logo = Image.open(os.path.normpath(os.path.join(HERE, SRC_ROOT, IMAGES["mmag-logo"][0]))).convert("RGB")
    for size, name in ((32, "favicon-32.png"), (180, "apple-touch-icon.png"), (192, "icon-192.png")):
        logo.resize((size, size), Image.LANCZOS).save(os.path.join(out_dir, name))


def img(p, key, cls="", alt=None, loading="lazy", attrs=""):
    name, w, h, default_alt = IMG[key]
    alt = default_alt if alt is None else alt
    size = f' width="{w}" height="{h}"' if w else ""
    klass = f' class="{cls}"' if cls else ""
    return f'<img{klass} src="{p.root}assets/img/{name}"{size} alt="{E(alt)}" loading="{loading}" decoding="async"{attrs}>'


def img_url(p, key):
    return f"{p.root}assets/img/{IMG[key][0]}"


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def scene(name, cls="", **opts):
    data = json.dumps(opts, separators=(",", ":")) if opts else "{}"
    return f'<div class="scene {cls}" data-scene="{name}" data-opts=\'{E(data, quote=False)}\' aria-hidden="true"></div>'


def section(theme, inner, cls="", scene_html="", attrs="", label=None):
    aria = f' aria-label="{E(label)}"' if label else ""
    return (f'<section class="s {cls} t-{theme}" data-nav-theme="{theme}"{aria}{attrs}>\n'
            f'  {scene_html}\n'
            f'  <div class="wrap">\n{inner}\n  </div>\n'
            f'</section>\n')


def split_title(text):
    return E(text)


class Page:
    """Knows its own depth, so every link is relative (works on any static host and sub-folder)."""

    def __init__(self, path):
        self.path = path  # "" for home, "work/" etc., "404.html" special
        self.is404 = path == "404.html"
        depth = 0 if self.is404 or path == "" else path.strip("/").count("/") + 1
        self.root = "/" if self.is404 else ("../" * depth if depth else "./")

    def url(self, target):
        """target like 'work/' or '' (home)."""
        if self.is404:
            return "/" + target
        if target == "":
            return self.root
        return self.root + target


# ---------------------------------------------------------------------------
# shared chrome
# ---------------------------------------------------------------------------
def head(p, title, desc, canonical_path, extra=""):
    canonical = SITE + "/" + canonical_path if canonical_path else SITE + "/"
    return f"""<!doctype html>
<html lang="en-IN" class="no-js">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{E(title)}</title>
  <meta name="description" content="{E(desc)}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="MMAG">
  <meta property="og:title" content="{E(title)}">
  <meta property="og:description" content="{E(desc)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{SITE}/assets/img/og.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#54078B">
  <meta name="generator" content="MMAG site build {E(VERSION)}">
  <link rel="icon" href="{p.root}assets/img/favicon-32.png" sizes="32x32" type="image/png">
  <link rel="icon" href="{p.root}assets/img/icon-192.png" sizes="192x192" type="image/png">
  <link rel="apple-touch-icon" href="{p.root}assets/img/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&amp;display=swap">
  <link rel="stylesheet" href="https://api.fontshare.com/v2/css?f[]=satoshi@400,500,700&amp;display=swap">
  <link rel="stylesheet" href="{p.root}assets/css/main.css">
  <script>
    /* flags read before first paint: JS on, first visit (preloader), arriving from an internal link (transition) */
    (function (d) {{
      var h = d.documentElement;
      h.classList.remove("no-js");
      h.classList.add("js");
      try {{
        if (!sessionStorage.getItem("mmag-loaded")) h.classList.add("is-first");
        if (sessionStorage.getItem("mmag-pt")) {{ h.classList.add("pt-in"); sessionStorage.removeItem("mmag-pt"); }}
      }} catch (e) {{}}
    }})(document);
  </script>
{extra}</head>
"""


def header(p, current):
    def link(target, label):
        cur = ' aria-current="page"' if current == target else ""
        return f'<a href="{p.url(target)}"{cur}>{label}</a>'
    return f"""<body>
<a class="skip" href="#main">Skip to content</a>
<div class="preloader" aria-hidden="true">
  {img(p, "mmag-logo", "preloader__logo", alt="", loading="eager")}
  <div class="preloader__count">0</div>
  <p class="preloader__word">Where brands gain momentum</p>
</div>
<div class="pt" aria-hidden="true"></div>
<canvas id="gl" aria-hidden="true"></canvas>
<div class="cursor" aria-hidden="true"><span class="cursor__dot"></span><span class="cursor__ring"></span></div>

<header class="nav" data-theme="dark">
  <a class="brand" href="{p.url('')}" aria-label="MMAG home">
    {img(p, "mmag-logo", "brand__logo", alt="MMAG", loading="eager")}
  </a>
  <nav class="nav__links" aria-label="Main">
    {link('work/', 'Work')}
    {link('services/', 'Services')}
    {link('about-us/', 'About')}
    {link('contact-us/', 'Contact')}
  </nav>
  <button class="btn btn--sm nav__cta" type="button" data-open="portfolio" data-magnetic>Download Portfolio {ARROW}</button>
  <button class="burger" type="button" aria-expanded="false" aria-controls="menu" aria-label="Open menu"><span></span><span></span></button>
</header>

<div class="menu" id="menu" aria-hidden="true">
  <a class="menu__link" href="{p.url('')}">Home</a>
  <a class="menu__link" href="{p.url('work/')}">Work</a>
  <a class="menu__link" href="{p.url('services/')}">Services</a>
  <a class="menu__link" href="{p.url('about-us/')}">About</a>
  <a class="menu__link" href="{p.url('contact-us/')}">Contact</a>
  <div class="btns"><button class="btn" type="button" data-open="call">Schedule a Call {ARROW}</button></div>
  <div class="menu__meta">
    <a href="tel:{PHONE}" data-loc="menu">{PHONE_DISPLAY}</a>
    <a href="mailto:{EMAIL}">{EMAIL}</a>
    <a href="{WHATSAPP}" target="_blank" rel="noopener" data-wa="menu">WhatsApp us</a>
    <span>{LOCATION}</span>
  </div>
</div>

"""


def footer(p):
    cases = "".join(f'<li><a href="{p.url("work/" + c["slug"] + "/")}">{E(c["short"])}</a></li>' for c in CASES[:5])
    services = "".join(f'<li><a href="{p.url("services/" + s["slug"] + "/")}">{E(s["name"])}</a></li>' for s in SERVICES)
    socials = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">MMAG on {n}</a></li>' for n, u in SOCIALS)
    inner = f"""    <div class="stack-gap">
      <p class="eyebrow">mo·men·tum · noun</p>
      <p class="footer__big" data-split>Let’s build<br>momentum</p>
      <div class="btns" data-reveal>
        <button class="btn" type="button" data-open="call" data-magnetic>Schedule a Call {ARROW}</button>
        <button class="btn btn--ghost" type="button" data-open="portfolio">Download Portfolio</button>
      </div>
    </div>
    <div class="footer__grid">
      <div>
        {img(p, "mmag-logo", "footer__logo", alt="MMAG")}
        <p class="footer__note">A Pune-born creative agency building brands and digital experiences that convert; for India and the world.</p>
        <address class="footer__note">MMAG, {'<br>'.join(E(x) for x in ADDRESS_LINES)}</address>
      </div>
      <div><h3>Work</h3><ul>{cases}<li><a href="{p.url('work/')}">All work</a></li></ul></div>
      <div><h3>Services</h3><ul>{services}</ul></div>
      <div><h3>Contact</h3><ul>
        <li><a href="tel:{PHONE}" data-loc="footer">{PHONE_DISPLAY}</a></li>
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><a href="{WHATSAPP}" target="_blank" rel="noopener" data-wa="footer">WhatsApp</a></li>
        <li><a href="{MAPS_URL}" target="_blank" rel="noopener">Find us on Google Maps</a></li>
        {socials}
      </ul></div>
    </div>
    <div class="footer__base">
      <span>© <span data-year>2026</span> MMAG. All rights reserved.</span>
      <span><a href="{p.url('privacy-policy/')}">Privacy policy</a> · <a href="#main" data-top>Back to top ↑</a></span>
    </div>"""
    return ('<footer class="s footer t-deep" data-nav-theme="deep">\n'
            f'  {scene("wave", "scene--bottom", amp=0.8)}\n'
            f'  <div class="wrap">\n{inner}\n  </div>\n</footer>\n')


def phone_field(prefix, label):
    opts = "".join(f'<option value="{E(v)}"{" selected" if v == "+91" else ""}>{E(t)}</option>' for v, t in COUNTRY_CODES)
    return f"""<div class="field">
        <label for="{prefix}-phone">{label} <span class="req">*</span></label>
        <div class="phone">
          <select class="select" name="country_code" aria-label="Country code">{opts}</select>
          <input class="input" id="{prefix}-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel-national" placeholder="Phone Number" required>
        </div>
        <span class="field__err" aria-live="polite"></span>
      </div>"""


def lead_form(p, kind):
    """Download Portfolio / Schedule a Call: same fields as the live popups."""
    name = "download-portfolio" if kind == "portfolio" else "schedule-call"
    submit = "Download Portfolio" if kind == "portfolio" else "Schedule a Call"
    pre = "pf" if kind == "portfolio" else "sc"
    inquiry = "".join(f'<option>{E(o)}</option>' for o in INQUIRY_OPTIONS)
    success = ("""<p data-portfolio-wait>Your details are in. Our team will email the portfolio to you shortly.</p>
      <a class="btn" href="#" data-portfolio-link hidden target="_blank" rel="noopener">Open the portfolio</a>"""
               if kind == "portfolio" else
               "<p>Your request is in. Our team will call you to fix a time that suits you.</p>")
    return f"""<div class="form-wrap" data-form-wrap>
    <form class="form" name="{name}" method="POST" data-netlify="true" netlify-honeypot="bot-field" data-form="{kind}" novalidate>
      <input type="hidden" name="form-name" value="{name}">
      <p class="hp"><label>Leave this empty <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
      <div class="field">
        <label for="{pre}-name">Name <span class="req">*</span></label>
        <input class="input" id="{pre}-name" name="name" type="text" autocomplete="name" placeholder="Name" required>
        <span class="field__err" aria-live="polite"></span>
      </div>
      <div class="field">
        <label for="{pre}-email">Email <span class="req">*</span></label>
        <input class="input" id="{pre}-email" name="email" type="email" autocomplete="email" placeholder="Email" required>
        <span class="field__err" aria-live="polite"></span>
      </div>
      {phone_field(pre, "Phone Number")}
      <div class="field">
        <label for="{pre}-org">Organization <span class="req">*</span></label>
        <input class="input" id="{pre}-org" name="organization" type="text" autocomplete="organization" placeholder="Organization" required>
        <span class="field__err" aria-live="polite"></span>
      </div>
      <div class="field field--full">
        <label for="{pre}-inquiry">Inquiry <span class="req">*</span></label>
        <select class="select" id="{pre}-inquiry" name="inquiry" required><option value="" disabled selected>Inquiry</option>{inquiry}</select>
        <span class="field__err" aria-live="polite"></span>
      </div>
      <div class="field field--full">
        <label for="{pre}-message">Message</label>
        <textarea class="textarea" id="{pre}-message" name="message" placeholder="Message" rows="3"></textarea>
      </div>
      <div class="form__actions">
        <p class="form__note">We use these details only to reply to you. <a href="{p.url('privacy-policy/')}">Privacy policy</a></p>
        <button class="btn" type="submit">{submit} {ARROW}</button>
      </div>
      <p class="form__status" role="status" aria-live="polite"></p>
    </form>
    <div class="form__success" tabindex="-1">
      <b>Thank you.</b>
      {success}
    </div>
  </div>"""


def contact_form(p):
    checks = "".join(f'<label class="check"><input type="checkbox" name="services" value="{E(c)}"><span>{E(c)}</span></label>' for c in CONTACT_INTERESTS)
    return f"""<div class="form-wrap" data-form-wrap>
    <form class="form form--card" name="contact" method="POST" data-netlify="true" netlify-honeypot="bot-field" data-form="contact" novalidate>
      <input type="hidden" name="form-name" value="contact">
      <p class="hp"><label>Leave this empty <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
      <div class="field">
        <label for="ct-name">Full Name <span class="req">*</span></label>
        <input class="input" id="ct-name" name="name" type="text" autocomplete="name" placeholder="David Murphy" required>
        <span class="field__err" aria-live="polite"></span>
      </div>
      <div class="field">
        <label for="ct-email">Work Email <span class="req">*</span></label>
        <input class="input" id="ct-email" name="email" type="email" autocomplete="email" placeholder="davidm@mail.com" required>
        <span class="field__err" aria-live="polite"></span>
      </div>
      {phone_field("ct", "Contact Number").replace('class="field"', 'class="field field--full"', 1)}
      <fieldset class="field field--full checks">
        <legend>What do you need?</legend>
        {checks}
      </fieldset>
      <div class="field field--full">
        <label for="ct-brief">Project Brief</label>
        <textarea class="textarea" id="ct-brief" name="message" placeholder="Tell us about your goals or a challenge you're facing..." rows="5"></textarea>
      </div>
      <div class="form__actions">
        <p class="form__note">We use these details only to reply to you. <a href="{p.url('privacy-policy/')}">Privacy policy</a></p>
        <button class="btn" type="submit">Submit {ARROW}</button>
      </div>
      <p class="form__status" role="status" aria-live="polite"></p>
    </form>
    <div class="form__success" tabindex="-1">
      <b>Thank you.</b>
      <p>Your brief is in. Our team will get back to you shortly.</p>
      <button class="btn btn--ghost" type="button" data-form-reset>Send another</button>
    </div>
  </div>"""


def modals(p):
    return f"""
<div class="modal" id="modal-portfolio" role="dialog" aria-modal="true" aria-labelledby="mt-portfolio" aria-hidden="true">
  <div class="modal__bg" data-close></div>
  <div class="modal__panel">
    <button class="modal__close" type="button" data-close aria-label="Close">{CLOSE}</button>
    <div class="modal__head">
      <h2 class="modal__title" id="mt-portfolio">Download Portfolio</h2>
      <p class="muted">Enter your details for quick access to our work</p>
    </div>
    {lead_form(p, "portfolio")}
  </div>
</div>
<div class="modal" id="modal-call" role="dialog" aria-modal="true" aria-labelledby="mt-call" aria-hidden="true">
  <div class="modal__bg" data-close></div>
  <div class="modal__panel">
    <button class="modal__close" type="button" data-close aria-label="Close">{CLOSE}</button>
    <div class="modal__head">
      <h2 class="modal__title" id="mt-call">Schedule a Call</h2>
      <p class="muted">Tell us a little about you and we’ll set up a time to talk.</p>
    </div>
    {lead_form(p, "call")}
  </div>
</div>
<div class="modal modal--video" id="modal-video" role="dialog" aria-modal="true" aria-label="MMAG showreel" aria-hidden="true">
  <div class="modal__bg" data-close></div>
  <div class="modal__panel">
    <button class="modal__close" type="button" data-close aria-label="Close">{CLOSE}</button>
    <div class="video-frame"></div>
  </div>
</div>
"""


def tail(p):
    return f"""{modals(p)}
<div class="mobile-bar">
  <a href="tel:{PHONE}" data-loc="mobile-bar">Call</a>
  <a href="{WHATSAPP}" target="_blank" rel="noopener" data-wa="mobile-bar" aria-label="WhatsApp">{WA_ICON}<span>WhatsApp</span></a>
  <button type="button" data-open="call">Schedule a Call</button>
</div>

<script src="{p.root}assets/vendor/gsap/gsap.js" defer></script>
<script src="{p.root}assets/vendor/gsap/ScrollTrigger.js" defer></script>
<script src="{p.root}assets/vendor/gsap/SplitText.js" defer></script>
<script src="{p.root}assets/vendor/lenis/lenis.js" defer></script>
<script src="{p.root}assets/js/config.js" defer></script>
<script src="{p.root}assets/js/forms.js" defer></script>
<script src="{p.root}assets/js/main.js" defer></script>
<script src="{p.root}assets/js/scenes.js" defer></script>
</body>
</html>
"""


def cta_section(p, title="Have a project in mind?", lead="Download our portfolio and let’s get in touch!"):
    inner = f"""    <p class="eyebrow">Next step</p>
    <h2 class="cta__title" data-split>{E(title)}</h2>
    <p class="lead" data-reveal>{E(lead)}</p>
    <div class="btns" data-reveal="0.1">
      <button class="btn" type="button" data-open="call" data-magnetic>Schedule a Call {ARROW}</button>
      <button class="btn btn--ghost" type="button" data-open="portfolio">Download Portfolio</button>
    </div>"""
    return section("yellow", inner, "cta", scene("knot", "scene--far", x=0.4), label="Get in touch")


def faq_section(items, title="Questions, answered"):
    rows = "".join(f"""
      <details>
        <summary>{E(q)}<i aria-hidden="true"></i></summary>
        <div class="faq__a"><p>{E(a)}</p></div>
      </details>""" for q, a in items)
    inner = f"""    <div class="split">
      <div class="split__head">
        <p class="eyebrow">FAQ</p>
        <h2 class="h2" data-split>{E(title)}</h2>
        {scene("rings", "scene--box")}
      </div>
      <div class="faq">{rows}
      </div>
    </div>"""
    return section("light", inner, "faq-sec", label="Frequently asked questions")


def steps_section(theme="dark", title="How we work"):
    steps = "".join(f"""
        <li class="step"><span class="step__n">0{i + 1}</span><span class="step__t">{E(t)}</span><span class="step__d">{E(d)}</span></li>""" for i, (t, d) in enumerate(PROCESS))
    inner = f"""    <div class="steps">
      <div>
        <p class="eyebrow">Process</p>
        <h2 class="h2" data-split>{E(title)}</h2>
        <ol class="steps__list" style="margin-top:28px">{steps}
        </ol>
      </div>
      <div class="steps__scene">{scene("helix", "", steps=4)}</div>
    </div>"""
    return section(theme, inner, "steps-sec", attrs=' data-steps', label="How we work")


def case_card(p, c, metric_override=None):
    return f"""      <a class="work-card" href="{p.url('work/' + c['slug'] + '/')}" data-tags="all {c['tags']}" data-tilt data-cursor="View">
        <div class="work-card__art"><canvas data-art="{c['slug']}" width="1200" height="750" aria-hidden="true"></canvas><span class="work-card__metric">{E(metric_override or c['metric'])}</span></div>
        <div class="work-card__body">
          <p class="work-card__kicker">{E(c['kicker'])} · {E(c['location'])}</p>
          <h3 class="work-card__title">{E(c['title'])}</h3>
          <p class="muted">{E(c['metric_label'])}</p>
        </div>
      </a>"""


def write(path, content):
    full = os.path.join(DIST, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(content)


def build_page(path, title, desc, canonical, current, body, extra_head=""):
    p = Page(path)
    out = head(p, title, desc, canonical, extra_head) + header(p, current) + '<main id="main">\n' + body(p) + '</main>\n' + footer(p) + tail(p)
    write(path if path.endswith(".html") else os.path.join(path, "index.html"), out)


# ---------------------------------------------------------------------------
# pages
# ---------------------------------------------------------------------------
def home(p):
    ring = "".join(f'<li class="ring__item" style="--i:{i}">{img(p, k)}</li>' for i, k in enumerate(RING_LOGOS))
    cards = "".join(f"""
        <article class="card card--media">
          <figure class="card__media">{img(p, HOME_SERVICE_IMAGE[s['slug']])}</figure>
          <div class="card__top"><span class="card__n">0{i + 1}</span><a class="link-arrow" href="{p.url('services/' + s['slug'] + '/')}">Explore {ARROW}</a></div>
          <div class="stack-gap">
            <h3 class="card__title">{E(s['name'])}</h3>
            <p class="muted">{E(s['line'])}</p>
          </div>
          <ul class="card__list">{''.join(f'<li>{E(x)}</li>' for x in [c[0] for c in s['cards']])}</ul>
        </article>""" for i, s in enumerate(SERVICES))
    panels = "".join(f"""
        <article class="hz__panel">
          {scene("pointsText", "", text=c['metric'])}
          <span class="hz__metric" aria-hidden="true">{E(c['metric'])}</span>
          <div class="hz__body">
            <p class="hz__kicker">{E(c['kicker'])} · {E(c['location'])}</p>
            <h3 class="hz__title">{E(c['title'])}</h3>
            <p class="muted"><b class="accent">{E(c['metric'])}</b> {E(c['metric_label'])}</p>
            <div class="hz__meta"><span class="chip">{E(c['industry'])}</span></div>
            <a class="link-arrow" href="{p.url('work/' + c['slug'] + '/')}" data-cursor="Read">Read case study {ARROW}</a>
          </div>
        </article>""" for c in CASES)
    quotes = "".join(f"""
          <blockquote class="quote{' is-active' if i == 0 else ''}">
            <p>{E(t['quote'])}</p>
            <footer>{img(p, TESTIMONIAL_LOGOS[i], "quote__logo")}<b>{E(t['name'])}</b><span>{E(', '.join(x for x in [t['role'], t['org']] if x))}</span></footer>
          </blockquote>""" for i, t in enumerate(TESTIMONIALS))
    culture_imgs = "".join(img(p, k) for k in CULTURE)

    out = []
    out.append(section("dark", f"""    <div class="hero__top">
      <p class="tagline-chip" data-reveal><b>●</b> Creative agency · Pune · India &amp; USA</p>
      <span class="scroll-cue" aria-hidden="true"><i></i>Scroll</span>
    </div>
    <h1 class="display hero__title" data-split>Where brands<br>gain momentum</h1>
    <div class="hero__bottom">
      <p class="lead" data-reveal>We craft stunning designs for businesses worldwide. Strategy, design, technology and performance under one roof.</p>
      <div class="btns" data-reveal="0.1">
        <button class="btn" type="button" data-open="call" data-magnetic>Schedule a Call {ARROW}</button>
        <button class="btn btn--ghost" type="button" data-open="video" data-cursor="Play">Watch our showreel</button>
      </div>
    </div>""", "hero", scene("momentum", "", x=2.35), label="Introduction"))

    out.append(section("light", f"""    <div class="stack-gap" style="justify-items:center;text-align:center">
      <p class="eyebrow">Trusted by industry leaders &amp; fast-growing startups</p>
      <h2 class="h2 balance" data-split>Brands that moved with us</h2>
    </div>
    <div class="ring-stage" aria-label="Clients"><ul class="ring" style="--n:{len(RING_LOGOS)}">{ring}</ul></div>""", "clients", label="Clients"))

    out.append(section("paper2", """    <div class="stack-gap">
      <p class="eyebrow">What we do</p>
      <p class="statement" data-scrub>We help businesses discover who they are, then turn it into unique strategies and higher ROI.</p>
      <div class="definition" data-reveal>
        <b>mo·men·tum</b>
        <span>/moʊˈmɛntəm/ · noun</span>
        <span>The push a brand gets when strategy, design, technology and performance move as one.</span>
      </div>
    </div>""", "manifesto", scene("ribbons", "scene--bottom", count=6, y=-0.6, opacity=0.75), label="What we do"))

    out.append(steps_section("dark"))

    out.append(section("purple", f"""    <div class="stack-head">
      <p class="eyebrow">What we build</p>
      <h2 class="h2" data-split>What we build goes beyond products</h2>
      <p class="lead" data-reveal>It’s trust, quality, and consistency.</p>
      <a class="link-arrow" href="{p.url('services/')}" data-reveal>All services {ARROW}</a>
      {scene("pillars", "scene--box")}
    </div>
    <div class="cards">{cards}
    </div>""", "stack-sec", attrs=" data-stack", label="Services"))

    # THE horizontal scroll (only one on the site)
    out.append(f"""<section class="s hz t-dark" data-nav-theme="dark" data-horizontal aria-label="Case studies">
  <div class="hz__pin">
    <div class="hz__track">
      <article class="hz__panel hz__panel--intro">
        <div class="hz__body">
          <p class="eyebrow">Case studies</p>
          <h2 class="display" style="font-size:clamp(3rem,8vw,8rem)">Work that speaks</h2>
          <p class="lead">Seven stories, each told in the number that mattered to the client.</p>
          <a class="link-arrow" href="{p.url('work/')}">All work {ARROW}</a>
          <div class="hz__thumbs" aria-label="Selected work">{img(p, "thumb-trevex")}{img(p, "thumb-tradekings")}{img(p, "thumb-bajaj")}</div>
        </div>
      </article>{panels}
      <article class="hz__panel hz__panel--intro hz__panel--photo">
        {img(p, "team-at-work", "hz__photo", alt="")}
        <div class="hz__body">
          <h3 class="h2">Your brand next?</h3>
          <div class="btns"><button class="btn" type="button" data-open="call" data-magnetic>Schedule a Call {ARROW}</button></div>
        </div>
      </article>
    </div>
    <div class="hz__progress" aria-hidden="true"><i></i></div>
  </div>
</section>
""")

    out.append(section("deep", f"""    <div class="stack-gap" style="max-width:720px">
      <p class="eyebrow">Global reach, local roots</p>
      <h2 class="h2" data-split>Pune-born. Working for India and the world.</h2>
      <p class="lead" data-reveal>Headquartered in Kothrud, Pune, with clients across India and the USA.</p>
    </div>
    <div class="numbers">
      <div class="number" data-reveal><b><span data-count="50">50</span>+</b><span>Clients across our industries</span></div>
      <div class="number number--text" data-reveal="0.08"><b><span class="flags">{img(p, "flag-india", alt="India")}{img(p, "flag-usa", alt="USA")}</span>India · USA</b><span>Global reach, local roots</span></div>
      <div class="number" data-reveal="0.16"><b><span data-count="8">8</span>+ yrs</b><span>Building brands that last</span></div>
    </div>""", "numbers-sec", scene("globe", "scene--right", x=0.6), label="Numbers"))

    out.append(section("light", f"""    <div class="stack-gap" style="max-width:820px;margin-bottom:clamp(30px,6vh,60px)">
      <p class="eyebrow">Voices of our clients</p>
      <h2 class="h2" data-split>Our clients’ experiences reflect the trust we build</h2>
    </div>
    <div class="quotes" data-quotes>
      <div class="quote-stage">{quotes}
      </div>
      <div class="stack-gap" style="justify-items:end">
        <span class="quote-count">01 / 0{len(TESTIMONIALS)}</span>
        <div class="quote-nav">
          <button class="round-btn" type="button" data-prev aria-label="Previous quote">{PREV}</button>
          <button class="round-btn" type="button" data-next aria-label="Next quote">{NEXT}</button>
        </div>
      </div>
    </div>""", "testimonials", scene("rings", "scene--far", x=0.6), label="Testimonials"))

    out.append(section("dark", f"""    <div class="teaser-grid">
      <div class="stack-gap" style="max-width:760px">
        <p class="eyebrow">People who make it happen</p>
        <h2 class="h2" data-split>A tight-knit team, obsessed with one thing</h2>
        <p class="lead" data-reveal>Strategists, designers, developers and storytellers, all working to make your brand impossible to ignore.</p>
        <a class="link-arrow" href="{p.url('about-us/')}" data-reveal>Meet the team {ARROW}</a>
      </div>
      <figure class="teaser-img" data-reveal>{img(p, "team-at-work", attrs=' data-parallax="-8"')}</figure>
    </div>
    <div class="marquee" aria-hidden="true" style="margin-top:clamp(40px,8vh,90px)">
      <div class="marquee__inner"><span>Strategists</span><span>Designers</span><span>Developers</span><span>Storytellers</span></div>
      <div class="marquee__inner"><span>Strategists</span><span>Designers</span><span>Developers</span><span>Storytellers</span></div>
    </div>
    <div class="photo-marquee" aria-label="Life at MMAG">
      <div class="photo-marquee__inner">{culture_imgs}</div>
      <div class="photo-marquee__inner" aria-hidden="true">{culture_imgs}</div>
    </div>""", "team-teaser", scene("confetti", "", count=220), label="Team"))

    out.append(cta_section(p))
    return "".join(out)


def work_hub(p):
    filters = [("all", "All"), ("service:websites", "Websites"), ("service:social", "Social"), ("service:seo", "SEO"),
               ("service:paid", "Paid"), ("service:branding", "Branding"), ("industry:real-estate", "Real estate"),
               ("industry:education", "Education"), ("industry:fmcg", "FMCG & D2C"), ("industry:b2b", "B2B"),
               ("industry:retail", "Retail"), ("loc:india", "India"), ("loc:international", "International")]
    fbtn = "".join(f'<button class="filter" type="button" data-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}">{E(v)}</button>' for k, v in filters)
    cards = "".join(case_card(p, c) for c in CASES)
    def project_row(n, t, u, keys):
        thumb = img(p, keys[0], "project__thumb", alt="")
        inner = f'{thumb}<span class="project__name">{E(n)}</span><span class="project__tags">{E(t)}</span>'
        prev = f' data-preview="{img_url(p, keys[0])}"'
        if u:
            return f'<a class="project" href="{u}" target="_blank" rel="noopener" data-cursor="Visit"{prev}>{inner}{ARROW_UR}</a>'
        return f'<div class="project"{prev}>{inner}<span></span></div>'
    projects = "".join(project_row(n, t, u, keys) for n, t, u, keys, _ in PROJECTS)
    owner = {k: n for n, _, _, keys, _ in PROJECTS for k in keys}
    wall = "".join(
        f'<div class="wall__col" data-wall="{ci}">' + "".join(
            f'<figure class="wall__item">{img(p, k)}<figcaption>{E(owner.get(k, "MMAG"))}</figcaption></figure>' for k in col) + "</div>"
        for ci, col in enumerate(WALL))
    reels = "".join(img(p, f"reel-{k}") for k in range(16))
    out = [section("dark", f"""    <nav class="crumbs" aria-label="Breadcrumb"><a href="{p.url('')}">Home</a><span>/</span><span>Work</span></nav>
    <h1 class="page-hero__title" data-split>Work that speaks</h1>
    <p class="lead" data-reveal>Case studies measured in the numbers that mattered, and a wall of brands we’ve built for.</p>""",
                   "page-hero", scene("shards", "scene--far", hero=True, x=0.4), label="Work")]
    out.append(section("light", f"""    <div class="stack-gap">
      <p class="eyebrow">Case studies</p>
      <h2 class="h2" data-split>Filter by what you need</h2>
      <div class="filters" data-filters role="group" aria-label="Filter case studies">{fbtn}</div>
      <p class="sr-only" aria-live="polite" data-filter-count></p>
    </div>
    <div class="work-grid">{cards}
    </div>""", "work-sec s--auto", scene("wave", "scene--bottom", amp=0.6), label="Case studies"))
    out.append(section("deep", f"""    <div class="stack-gap" style="max-width:820px">
      <p class="eyebrow">Portfolio</p>
      <h2 class="h2" data-split>Websites, campaigns and content, made for real brands</h2>
    </div>
    <div class="wall">{wall}</div>""", "wall-sec", scene("ribbons", "", count=5, y=-2.6, opacity=0.5), label="Portfolio wall"))
    out.append(section("dark", f"""    <div class="stack-gap" style="max-width:760px">
      <p class="eyebrow">More projects</p>
      <h2 class="h2" data-split>Brands we’ve designed, built and grown</h2>
    </div>
    <div class="projects">{projects}</div>
    <div class="reels" aria-label="Social media reels for Bajaj Housing Finance and Trade Kings Group">
      <div class="reels__inner">{reels}</div>
      <div class="reels__inner" aria-hidden="true">{reels}</div>
    </div>""", "projects-sec", scene("ribbons", "", count=5, y=1.6, opacity=0.6), label="More projects"))
    out.append(cta_section(p, "Your brand could be next", "Tell us where you want to grow. We’ll show you how we’d get there."))
    return "".join(out)


def case_page(c, i):
    def body(p):
        stats = []
        for val, fmt, pre, suf, label in c["stats"]:
            if fmt == "text":
                num = f"<b>{E(str(val))}</b>"
            else:
                shown = f"{val:,}" if fmt == "comma" else str(val)
                num = f'<b>{E(pre)}<span data-count="{val}" data-format="{fmt}">{shown}</span>{E(suf)}</b>'
            stats.append(f'<div class="stat" data-reveal>{num}<span>{E(label)}</span></div>')
        challenge = "".join(f"<li>{E(x)}</li>" for x in c["challenge"])
        approach = "".join(f'<li data-n="{k + 1}"><p>{E(x)}</p></li>' for k, x in enumerate(c["approach"]))
        results = "".join(f"<li>{E(x)}</li>" for x in c["results"])
        nxt = CASES[(i + 1) % len(CASES)]
        foot = f'<p class="approval-note">{E(c["footnote"])}</p>' if c.get("footnote") else ""
        out = [section("deep", f"""    <nav class="crumbs" aria-label="Breadcrumb"><a href="{p.url('')}">Home</a><span>/</span><a href="{p.url('work/')}">Work</a><span>/</span><span>{E(c['short'])}</span></nav>
    <p class="eyebrow">Case study · {E(c['kicker'])}</p>
    <h1 class="page-hero__title page-hero__title--case" data-split>{E(c['title'])}</h1>
    <p class="lead" data-reveal>{E(c['summary'])}</p>
    <div class="facts" data-reveal="0.1">
      <div class="fact"><span>Industry</span><b>{E(c['industry'])}</b></div>
      <div class="fact"><span>Location</span><b>{E(c['location'])}</b></div>
      <div class="fact"><span>Services</span><b>{E(c['services'])}</b></div>
    </div>""", "page-hero", scene("pointsText", "scene--far", text=c["metric"], always=True), label="Case study")]
        out.append(section("light", f"""    <div class="stack-gap" style="margin-bottom:clamp(24px,5vh,48px)">
      <p class="eyebrow">The numbers</p>
      <h2 class="h2" data-split>What changed</h2>
    </div>
    <div class="stats">{''.join(stats)}</div>
    {foot}""", "stats-sec", scene("stack", "scene--right"), label="Results in numbers"))
        out.append(section("dark", f"""    <div class="split">
      <div class="split__head">
        <p class="eyebrow">01 · Brief</p>
        <h2 class="h2" data-split>The Challenge</h2>
        {scene("shards", "scene--box", count=220, radius=1.9)}
      </div>
      <ol class="points">{challenge}</ol>
    </div>""", "challenge-sec", label="The challenge"))
        out.append(section("paper2", f"""    <div class="split">
      <div class="split__head">
        <p class="eyebrow">02 · Approach</p>
        <h2 class="h2" data-split>Our Approach</h2>
        {scene("helix", "scene--box", steps=len(c['approach']))}
      </div>
      <ol class="timeline"><span class="timeline__bar" aria-hidden="true"></span>{approach}</ol>
    </div>""", "approach-sec", label="Our approach"))
        out.append(section("purple", f"""    <div class="stack-gap" style="max-width:860px">
      <p class="eyebrow">03 · Outcome</p>
      <h2 class="h2" data-split>The Results</h2>
      <ul class="results" data-reveal>{results}</ul>
    </div>""", "results-sec", scene("rings", "scene--far", x=0.6), label="The results"))
        svc = CASE_SERVICE[c["slug"]]
        picks = [(k, cap) for k, cap in SERVICE_IMAGES[svc] if c["slug"] not in IMAGE_AVOID.get(k, set())][:3]
        svc_name = next(x["name"] for x in SERVICES if x["slug"] == svc)
        more = "".join(f'<figure class="gallery__item" data-tilt>{img(p, k)}<figcaption>{E(cap)}</figcaption></figure>' for k, cap in picks)
        out.append(section("light", f"""    <div class="stack-gap" style="max-width:820px">
      <p class="eyebrow">More {E(svc_name.lower())} from MMAG</p>
      <h2 class="h2" data-split>More work like this</h2>
      <p class="muted" data-reveal>Other projects from our portfolio. The client in this case study stays anonymous.</p>
    </div>
    <div class="gallery gallery--3">{more}</div>
    <a class="link-arrow" href="{p.url('services/' + svc + '/')}" data-reveal style="margin-top:28px">{E(svc_name)} {ARROW}</a>""", "more-sec s--auto", scene("wave", "scene--bottom", amp=0.6), label="More work like this"))
        out.append(section("yellow", f"""    <a class="next-case" href="{p.url('work/' + nxt['slug'] + '/')}" data-cursor="Next">
      <span class="eyebrow">Next case study · {E(nxt['kicker'])}</span>
      <span class="next-case__title" data-split>{E(nxt['title'])}</span>
      <span class="link-arrow">Read it {ARROW}</span>
    </a>
    <div class="btns" data-reveal style="margin-top:clamp(24px,5vh,48px)">
      <button class="btn" type="button" data-open="call" data-magnetic>Schedule a Call {ARROW}</button>
      <button class="btn btn--ghost" type="button" data-open="portfolio">Download Portfolio</button>
    </div>""", "next-sec", scene("knot", "scene--right", x=1.3), label="Next case study"))
        return "".join(out)
    return body


def services_hub(p):
    rows = "".join(f"""
      <a class="svc-row" href="{p.url('services/' + s['slug'] + '/')}" data-cursor="Open" data-preview="{img_url(p, HOME_SERVICE_IMAGE[s['slug']])}">
        <span class="svc-row__n">0{i + 1}</span>
        <span class="svc-row__name">{E(s['name'])}</span>
        <span class="svc-row__line">{E(s['line'])}</span>
        {ARROW_UR}
      </a>""" for i, s in enumerate(SERVICES))
    out = [section("dark", f"""    <nav class="crumbs" aria-label="Breadcrumb"><a href="{p.url('')}">Home</a><span>/</span><span>Services</span></nav>
    <h1 class="page-hero__title" data-split>Everything a brand needs to move</h1>
    <p class="lead" data-reveal>Strategy, design, technology and performance: five services, one team.</p>""",
                   "page-hero", scene("pillars", "scene--far", cycle=True), label="Services")]
    out.append(section("light", f"""    <div class="stack-gap" style="max-width:820px">
      <p class="eyebrow">Services</p>
      <h2 class="h2" data-split>Pick where you want momentum</h2>
    </div>
    <div class="svc-list">{rows}
    </div>""", "svc-sec", scene("ribbons", "", count=4, y=-2.2, opacity=0.5), label="All services"))
    out.append(steps_section("dark"))
    out.append(faq_section(FAQ_COMMON))
    out.append(cta_section(p))
    return "".join(out)


def service_page(s):
    def body(p):
        cards = "".join(f"""
        <article class="card card--media">
          <figure class="card__media">{img(p, CARD_IMAGES[s['slug']][k])}</figure>
          <div class="card__top"><span class="card__n">0{k + 1}</span></div>
          <div class="stack-gap">
            <h3 class="card__title">{E(t)}</h3>
            <p class="muted">{E(line)}</p>
          </div>
          <ul class="card__list">{''.join(f'<li>{E(x)}</li>' for x in chips)}</ul>
        </article>""" for k, (t, line, chips) in enumerate(s["cards"]))
        related = "".join(case_card(p, CASE_BY[slug]) for slug in s["cases"])
        gallery = "".join(f'<figure class="gallery__item" data-tilt>{img(p, k)}<figcaption>{E(cap)}</figcaption></figure>' for k, cap in SERVICE_IMAGES[s["slug"]])
        reels = ""
        if s["slug"] == "social-media-marketing":
            rr = "".join(img(p, f"reel-{k}") for k in range(16))
            reels = f'<div class="reels" aria-label="Social media reels"><div class="reels__inner">{rr}</div><div class="reels__inner" aria-hidden="true">{rr}</div></div>'

        others = "".join(f'<a class="chip" href="{p.url("services/" + o["slug"] + "/")}">{E(o["name"])}</a>' for o in SERVICES if o["slug"] != s["slug"])
        out = [section("dark", f"""    <nav class="crumbs" aria-label="Breadcrumb"><a href="{p.url('')}">Home</a><span>/</span><a href="{p.url('services/')}">Services</a><span>/</span><span>{E(s['short'])}</span></nav>
    <p class="eyebrow">{E(s['name'])}</p>
    <h1 class="page-hero__title page-hero__title--case" data-split>{E(s['hero'])}</h1>
    <p class="lead" data-reveal>{E(s['lead'])}</p>
    <div class="btns" data-reveal="0.1">
      <button class="btn" type="button" data-open="call" data-magnetic>Schedule a Call {ARROW}</button>
      <a class="btn btn--ghost" href="#related">See the work</a>
    </div>""", "page-hero", scene("pillars", "scene--far", only=s["scene"]), label=s["name"])]
        out.append(section("purple", f"""    <div class="stack-head">
      <p class="eyebrow">What you get</p>
      <h2 class="h2" data-split>Four parts, one plan</h2>
      <p class="lead" data-reveal>{E(s['line'])}</p>
      {scene("shards", "scene--box", count=200, radius=1.8)}
    </div>
    <div class="cards">{cards}
    </div>""", "stack-sec", attrs=" data-stack", label="What you get"))
        out.append(section("light", f"""    <div class="stack-gap" style="max-width:820px">
      <p class="eyebrow">Related work</p>
      <h2 class="h2" data-split>Proof, not promises</h2>
    </div>
    <div class="work-grid">{related}
    </div>
    <div class="stack-gap" style="max-width:820px;margin-top:clamp(48px,9vh,110px)">
      <p class="eyebrow">From the portfolio</p>
      <h3 class="h3" data-split>{E(s['name'])} we’ve delivered</h3>
    </div>
    <div class="gallery">{gallery}</div>
    {reels}""", "work-sec s--auto", scene("wave", "scene--bottom", amp=0.6), attrs=' id="related"', label="Related work"))
        out.append(steps_section("dark"))
        out.append(faq_section([s["faq"]] + FAQ_COMMON))
        out.append(section("deep", f"""    <div class="stack-gap">
      <p class="eyebrow">Also from MMAG</p>
      <h2 class="h2" data-split>Pair it with</h2>
      <div class="hz__meta" data-reveal>{others}</div>
    </div>""", "pair-sec s--auto", scene("ribbons", "", count=4, opacity=0.55), label="Other services"))
        out.append(cta_section(p))
        return "".join(out)
    return body


def about(p):
    team = "".join(f"""
      <div class="member" tabindex="0">
        <div class="member__face member__face--photo">
          {img(p, TEAM_PHOTOS[n], "member__photo")}
          <div class="member__label"><p class="member__name">{E(n)}</p><p class="member__role">{E(r)}</p></div>
        </div>
        <div class="member__face member__face--back">
          <span class="member__initials">{E(''.join(w[0] for w in n.split()[:2]))}</span>
          <div><p class="member__name">{E(n)}</p><p class="member__role">{E(r)}</p>{f'<a href="{u}" target="_blank" rel="noopener">LinkedIn ↗</a>' if u else ''}</div>
        </div>
      </div>""" for n, r, u in TEAM)
    values = [("Strategy first", "We don't start with Figma. We start with your business goals."),
              ("Design with purpose", "Every pixel serves a reason — clarity, trust, or conversion."),
              ("Results that show", "We measure success in traffic, leads, revenue — not likes.")]
    vals = "".join(f'<div class="value" data-reveal="{k * 0.08}"><b>{E(t)}</b><p>{E(d)}</p></div>' for k, (t, d) in enumerate(values))
    out = [section("dark", f"""    <nav class="crumbs" aria-label="Breadcrumb"><a href="{p.url('')}">Home</a><span>/</span><span>About</span></nav>
    <h1 class="page-hero__title" data-split>We're not a vendor. We're your growth partner.</h1>
    <p class="lead" data-reveal>A Pune-born creative agency building brands and digital experiences that convert; for India and the world.</p>""",
                   "page-hero", scene("shards", "scene--far", hero=True, x=0.5), label="About MMAG")]
    out.append(section("deep", f"""    <div class="stack-gap" style="max-width:640px">
      <p class="eyebrow">Where we work</p>
      <h2 class="h2" data-split>Global reach, local roots</h2>
    </div>
    <div class="numbers" style="max-width:820px">
      <div class="number" data-reveal><b><span data-count="50">50</span>+</b><span>Clients</span></div>
      <div class="number" data-reveal="0.08"><b><span data-count="8">8</span>+</b><span>Years building brands</span></div>
      <div class="number" data-reveal="0.16"><b>2</b><span>Countries: India &amp; USA</span></div>
    </div>
    <div class="locations" style="max-width:820px">
      <div class="location" data-reveal>{img(p, "flag-india", "location__flag", alt="")}<b>India</b><p class="muted">Headquartered in Kothrud, Pune. Serving brands across Real Estate, HealthCare, FMCG, Tech &amp; Manufacturing.</p><div class="hz__meta"><span class="chip">Pune HQ</span><span class="chip">Pan-India clients</span></div></div>
      <div class="location" data-reveal="0.1">{img(p, "flag-usa", "location__flag", alt="")}<b>USA</b><p class="muted">Trusted by brands in the USA — CloudSufi, The Spark, Matr Boomie. Delivering world-class output at a fraction of US agency cost.</p><div class="hz__meta"><span class="chip">USA clients</span><span class="chip">Remote first</span></div></div>
    </div>""", "where-sec", scene("globe", "scene--right", x=1.1), label="Where we work"))
    out.append(section("paper2", f"""    <div class="founder">
      <blockquote>
        <p data-split>I started MMAG because I saw great products failing due to bad branding. We exist to fix that by combining strategy, design, and tech to give brands the unfair advantage they deserve.</p>
        <footer data-reveal><b>Rushikesh Kate</b><span class="muted">Founder &amp; CEO</span></footer>
      </blockquote>
      <figure class="founder__photo" data-reveal>{img(p, "p-rushikesh", attrs=' data-parallax="-6"')}</figure>
    </div>""", "founder-sec", scene("ribbons", "", count=6, y=-1.8), label="Founder"))
    out.append(section("dark", f"""    <div class="stack-gap" style="max-width:900px">
      <p class="eyebrow">The team</p>
      <h2 class="h2" data-split>A tight-knit team of strategists, designers, developers and storytellers</h2>
      <p class="lead" data-reveal>All obsessed with one thing: making your brand impossible to ignore.</p>
    </div>
    <div class="team">{team}
    </div>""", "team-sec", scene("wave", "scene--bottom", amp=0.6), label="Team"))
    out.append(section("light", f"""    <div class="stack-gap" style="max-width:900px">
      <p class="eyebrow">What we believe</p>
      <h2 class="h2" data-split>We believe great design is invisible. Only the results show.</h2>
    </div>
    <div class="values">{vals}</div>""", "values-sec", scene("rings", "scene--right", x=1.8), label="Values"))
    out.append(section("purple", f"""    <div class="stack-gap" style="max-width:760px">
      <p class="eyebrow">Culture</p>
      <h2 class="display" style="font-size:clamp(3rem,9vw,9rem)" data-split>Work hard. Celebrate harder.</h2>
      <p class="lead" data-reveal>Capturing the moments that make our culture vibrant and unique.</p>
      <p data-reveal>Designers, developers, strategists and storytellers: if you want to join us, <a href="{p.url('contact-us/')}">tell us what you’d bring</a>.</p>
    </div>
    <div class="collage" data-reveal>{''.join(f'<figure class="collage__item" style="--k:{k}">{img(p, key)}</figure>' for k, key in enumerate(CULTURE))}</div>""", "culture-sec", scene("confetti", "", count=260), label="Culture and careers"))
    out.append(cta_section(p))
    return "".join(out)


def contact(p):
    socials = "".join(f'<a class="chip" href="{u}" target="_blank" rel="noopener">{E(n)}</a>' for n, u in SOCIALS)
    out = [section("dark", f"""    <nav class="crumbs" aria-label="Breadcrumb"><a href="{p.url('')}">Home</a><span>/</span><span>Contact</span></nav>
    <h1 class="page-hero__title" data-split>Contact us</h1>
    <p class="lead" data-reveal>Get in touch with our team to explore how we can work together.</p>
    <div class="btns" data-reveal="0.1">
      <button class="btn" type="button" data-open="call" data-magnetic>Schedule a Call {ARROW}</button>
      <a class="btn btn--ghost" href="#brief">Send a brief</a>
    </div>""", "page-hero", scene("rings", "scene--far", x=1.4), label="Contact")]
    out.append(section("light", f"""    <div class="contact-grid">
      <div class="stack-gap">
        <p class="eyebrow">Send a brief</p>
        <h2 class="h2" data-split>Tell us about your project</h2>
        {contact_form(p)}
      </div>
      <aside class="contact-side" aria-label="Contact details">
        <div class="contact-item"><span>Call</span><a href="tel:{PHONE}" data-loc="contact">{PHONE_DISPLAY}</a></div>
        <div class="contact-item"><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></div>
        <div class="contact-item"><span>WhatsApp</span><a href="{WHATSAPP}" target="_blank" rel="noopener" data-wa="contact">Chat with us ↗</a></div>
        <div class="contact-item"><span>Visit</span><a href="{MAPS_URL}" target="_blank" rel="noopener">MMAG, {'<br>'.join(E(x) for x in ADDRESS_LINES)} ↗</a></div>
        <figure class="contact-photo">{img(p, "team-at-work", alt="The MMAG studio in Kothrud, Pune")}</figure>
        <div class="contact-item"><span>Follow</span><div class="hz__meta">{socials}</div></div>
        {scene("globe", "scene--box")}
      </aside>
    </div>""", "contact-sec s--auto", attrs=' id="brief"', label="Contact form"))
    out.append(cta_section(p, "Prefer to talk it through?", "Book a call and we’ll walk you through how we’d approach it."))
    return "".join(out)


def privacy(p):
    secs = [
        ("who", "Who we are", "<p>MMAG is a creative agency at Office No. 104, Chintamani Pride, Near City Pride, Kothrud, Pune 411038, India. This policy covers the information you share through this website.</p>"),
        ("what", "What we collect", "<ul><li>Download Portfolio and Schedule a Call forms: name, email, phone number, organization, inquiry type and your message.</li><li>Contact form: full name, work email, contact number, the services you tick and your project brief.</li><li>If analytics is switched on: anonymous usage data from Google Analytics 4.</li></ul>"),
        ("why", "Why we use it", "<p>To reply to your enquiry, send you our portfolio, arrange a call, and understand which pages help visitors. We do not sell your information.</p>"),
        ("where", "Where it goes", "<p>Form submissions are delivered to our team through the form-processing service used by our web host. [To be confirmed: name of the service and storage location.]</p>"),
        ("keep", "How long we keep it", "<p>[To be confirmed with management: retention period for enquiries.]</p>"),
        ("rights", "Your choices", "<p>You can ask us to show, correct or delete the information you shared. Write to <a href=\"mailto:" + EMAIL + "\">" + EMAIL + "</a> or use the details on our <a href=\"" + p.url("contact-us/") + "\">contact page</a>.</p>"),
        ("cookies", "Cookies and storage", "<p>The site itself sets no cookies. It stores two short-lived flags in your browser session to skip the intro animation on later pages. Google Analytics, if switched on, sets its own cookies.</p>"),
    ]
    toc = "".join(f'<a href="#{k}">{E(t)}</a>' for k, t, _ in secs)
    body_secs = "".join(f'<section class="doc__sec" id="{k}" data-reveal><h2>{E(t)}</h2>{b}</section>' for k, t, b in secs)
    out = [section("dark", f"""    <nav class="crumbs" aria-label="Breadcrumb"><a href="{p.url('')}">Home</a><span>/</span><span>Privacy policy</span></nav>
    <h1 class="page-hero__title" data-split>Privacy policy</h1>
    <p class="draft-flag" data-reveal>Draft for legal review. Not yet approved.</p>""", "page-hero", scene("shards", "scene--far", hero=True, x=0.6), label="Privacy policy")]
    out.append(section("light", f"""    <div class="doc">
      <nav class="doc__toc" aria-label="On this page"><p class="eyebrow">On this page</p>{toc}</nav>
      <div class="doc__body">{body_secs}</div>
    </div>""", "doc-sec s--auto", scene("wave", "scene--bottom", amp=0.5), label="Policy"))
    return "".join(out)


def not_found(p):
    return section("dark", f"""    <p class="eyebrow">Error 404</p>
    <p class="nf__code" data-split>404</p>
    <h1 class="h2" data-split>Lost momentum?</h1>
    <p class="lead" data-reveal>This page has moved or no longer exists.</p>
    <div class="btns" data-reveal="0.1">
      <a class="btn" href="{p.url('')}">Back to home {ARROW}</a>
      <a class="btn btn--ghost" href="{p.url('work/')}">See our work</a>
      <button class="btn btn--ghost" type="button" data-open="call">Schedule a Call</button>
    </div>""", "nf", scene("tunnel", ""), label="Page not found")


# ---------------------------------------------------------------------------
# build
# ---------------------------------------------------------------------------
def org_jsonld():
    data = {
        "@context": "https://schema.org", "@type": "ProfessionalService", "name": "MMAG", "url": SITE + "/",
        "telephone": "+91-8308852044", "email": EMAIL, "areaServed": ["India", "United States"],
        "logo": SITE + "/assets/img/" + IMG["mmag-logo"][0], "image": SITE + "/assets/img/og.jpg",
        "address": {"@type": "PostalAddress", "streetAddress": "Office No. 104, Chintamani Pride, Near City Pride", "addressLocality": "Kothrud, Pune",
                    "postalCode": "411038", "addressRegion": "Maharashtra", "addressCountry": "IN"},
        "sameAs": [u for _, u in SOCIALS],
        "description": "Creative agency in Pune: branding, websites, SEO, social media and performance marketing.",
    }
    return '  <script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>\n"


def main():
    if os.path.exists(DIST):
        shutil.rmtree(DIST)
    shutil.copytree(os.path.join(SRC, "assets"), os.path.join(DIST, "assets"))
    process_images()

    build_page("", "MMAG · Creative Agency in Pune for Brands, Websites & Growth",
               "MMAG is a creative agency in Pune building brands, websites, SEO, social media and performance marketing for businesses in India and the USA.",
               "", "", home, org_jsonld())
    build_page("work/", "Work · Case Studies & Projects · MMAG",
               "Case studies and projects by MMAG: e-commerce launches, SEO, social media, branding and performance marketing, with the numbers that mattered.",
               "work/", "work/", work_hub)
    for i, c in enumerate(CASES):
        build_page(f"work/{c['slug']}/", f"{c['title']} · Case Study · MMAG", c["summary"], f"work/{c['slug']}/", "work/", case_page(c, i))
    build_page("services/", "Services · Branding, Websites, SEO, Social & Performance · MMAG",
               "MMAG services: branding and strategy, website design and development, SEO, social media marketing and performance marketing.",
               "services/", "services/", services_hub)
    for s in SERVICES:
        build_page(f"services/{s['slug']}/", f"{s['name']} · MMAG", s["meta"], f"services/{s['slug']}/", "services/", service_page(s))
    build_page("about-us/", "About MMAG · Creative Agency in Pune",
               "A Pune-born creative agency building brands and digital experiences that convert; for India and the world.",
               "about-us/", "about-us/", about)
    build_page("contact-us/", "Contact MMAG · Schedule a Call",
               "Get in touch with MMAG to explore how we can work together. Call, send a brief or schedule a call.",
               "contact-us/", "contact-us/", contact)
    build_page("privacy-policy/", "Privacy Policy · MMAG", "How MMAG handles the information you share through this website.",
               "privacy-policy/", "", privacy)
    build_page("404.html", "Page not found · MMAG", "This page has moved or no longer exists.", "", "", not_found)

    # deploy helpers
    urls = ["", "work/", "services/", "about-us/", "contact-us/", "privacy-policy/"] + [f"work/{c['slug']}/" for c in CASES] + [f"services/{s['slug']}/" for s in SERVICES]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
          "".join(f"  <url><loc>{SITE}/{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    write("_redirects", "\n".join([
        "# Old mmag.in URLs → new structure (Netlify / Cloudflare Pages format)",
        "/case-studies/zendale/            /work/      302",
        "/case-studies/yash-industries/    /work/      301",
        "/case-studies/equinext/           /work/      301",
        "/case-studies/                    /work/      301",
        "/case-studies/*                   /work/:splat 301",
        "/work/zendale/                    /work/      302",
        "/mmag-portfolio/                  /work/      301",
        "/website-portfolio/               /work/      301",
        "/under-development/               /           301",
        "/hello-world/                     /           301",
        ""]))
    write("README.txt", f"""MMAG website · build {VERSION}

Deploy: upload this folder's contents (or the zip) to any static host. index.html is at the root.
  - Netlify: drag the unzipped folder onto app.netlify.com/drop. Forms work there out of the box.
  - Other hosts: set assets/js/config.js → formEndpoint to a form service URL, or forms show a "call us" fallback.
Preview locally: run `python3 -m http.server` in this folder, then open http://localhost:8000
(opening index.html directly from disk breaks folder links and some browser features).

Settings: assets/js/config.js (form endpoint, portfolio link, GA4 ID, phone, Three.js version).
Redirects for old mmag.in URLs: _redirects (Netlify / Cloudflare Pages format).
""")
    print("built", sum(len(f) for _, _, f in os.walk(DIST)), "files into", os.path.normpath(DIST))


if __name__ == "__main__":
    main()
