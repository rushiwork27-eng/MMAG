# MMAG website (source)

Static site: HTML, CSS and JS, no framework. Everything is unminified. 3D is Three.js from a CDN; animation is GSAP + Lenis (vendored). Images are the live mmag.in media, resized to WebP at build time (needs Python Pillow).

| Folder | What |
|---|---|
| `build/content.py` | All page copy, case studies, services, forms' options, contact details. **Edit content here.** |
| `build/images.py` | Every image: source file (from `site-audit/assets/media/`), size, alt text, client, and where it is used. **Swap images here.** |
| `build/build.py` | Generates every page into `dist/` |
| `build/make_release.sh` | Builds and zips a versioned release into `../releases/` |
| `src/assets/css/main.css` | All styles (brand tokens at the top) |
| `src/assets/js/scenes.js` | Three.js engine + 13 code-built scenes |
| `src/assets/js/main.js` | Scroll, pins, the horizontal scroll, text reveals, modals, cursor |
| `src/assets/js/forms.js` | Form validation and submission |
| `src/assets/js/config.js` | Settings: form endpoint, portfolio link, GA4, phone, Three.js URL |
| `dist/` | Built site (what gets deployed) |

## Build a release

Run this from `website/build/`:

```bash
bash make_release.sh v1.1
```

## Preview locally

```bash
cd website/dist && python3 -m http.server 8000
```

Then open http://localhost:8000. Opening `index.html` straight from disk breaks the folder links.

## Use a page's 3D scene

Add `<div class="scene" data-scene="globe" data-opts='{"x":1}' aria-hidden="true"></div>` inside a section. Available scenes:
- `momentum`
- `ribbons`
- `helix`
- `pillars`
- `pointsText` (needs `{"text":"547%"}`)
- `globe`
- `wave`
- `shards`
- `stack`
- `knot`
- `rings`
- `confetti`
- `tunnel`

Placement classes: `scene--right`, `scene--far`, `scene--bottom`, `scene--box` (in-flow square).

The build log, version history and pending decisions are in [`../docs/PROMPT-LOG.md`](../docs/PROMPT-LOG.md).
