# MMAG brand theme (as built on mmag.in)

Sources:
- Elementor Global Kit (`backend/css/elementor-global-kit-post-6.css`), which holds the site's official colour and type tokens.
- Computed styles measured in the browser on all 15 live pages. Raw tally: `data/style-tally.json`.
- Screenshots in `screenshots/`.

Ready-to-use tokens: [`brand-tokens.css`](brand-tokens.css).

## 1. Colour

### Global palette (Elementor kit)

| Token (Elementor ID) | Hex | Where it is used on the live site |
|---|---|---|
| `d7f37db`, brand purple | `#54078B` | Hero headline, nav text, all primary buttons and links, footer bar, case-study hero background, counters |
| `accent` / `54c8b59`, brand yellow | `#F3C01F` | Logo square, decorative dots, "Get in Touch" CTA background, back-to-top button, highlights. The kit stores it twice under two IDs |
| `primary` | `#171717` | Default H1/H2 colour |
| `secondary` / `text` | `#1E1E1E` | Secondary headings |
| `fc7d875` | `#5C5C5C` | Body text (kit `body` colour) |
| `7b61cf3` | `#7B7B7B` | Muted text, service sub-items |
| `2f440a9` | `#F0F0EF` | Light grey section backgrounds (work, case-study and testimonial blocks) |
| `4bf31b2` | `#FFFFFF` | Header, cards, footer top |
| Kit body background (not a token) | `#FAF9F5` | Warm off-white page background, with a light grid pattern in the hero |

### Off-kit colours hard-coded in page CSS

These come mostly from the case-study template. Consolidate them in the redesign.

| Hex | Where | Note |
|---|---|---|
| `#3A0561` (also at 60–70% opacity) | Case-study info cards, overlays | Dark purple, a shade of the brand purple. Keep it as `purple-900` |
| `#F4B400` | Case-study eyebrow labels and the yellow box in the "What we build" timeline | Close to but **not equal to** brand yellow `#F3C01F`. Pick one |
| `#1C1230` | Case-study H2s ("The Challenge") | Purple-tinted near-black |
| `#55525C`, `#57545E` | Case-study body text | A third body-grey, alongside `#5C5C5C` and `#7B7B7B` |
| `#E5E2EC`, `#E7E4EE` | Card borders | |
| `#F4F2ED` | Section backgrounds | A third off-white, alongside `#FAF9F5` and `#F0F0EF` |
| `#E7DAF2`, `#CFC6DA`, `#EDE8F3` | Light text on purple | |
| `#696888` | "View All" text button (turns `#54078B` on hover) | |
| `#C5C5C5` | Form field borders | |
| `#000000`, `#0B0B0B` | Portfolio pages background | |

Recommendation for the redesign:
- Keep **purple `#54078B` + yellow `#F3C01F`** on a **warm off-white `#FAF9F5`** as the core palette.
- Add a purple scale (`#3A0561` dark, `#54078B` base, `#E7DAF2` tint).
- Collapse the greys to three: `#171717`, `#5C5C5C` and `#7B7B7B`.

## 2. Typography

| Role | Family | Source |
|---|---|---|
| Headings (H1–H6) | **Plus Jakarta Sans** (100–900 loaded; 300–800 seen in use) | Google Fonts |
| Body, buttons, UI | **Satoshi** (variable; 400/500/600/700 in use) | Self-hosted at `/wp-content/uploads/2026/01/Satoshi-Variable.ttf`. Satoshi is an Indian Type Foundry/Fontshare font. **Confirm the licence before reuse (unverified)** |
| Unused | Aeonik Bold (`fonnts.com-Aeonik-Bold.ttf` in the media library) | Not used on any page. It came from a third-party free-font site and Aeonik is a commercial typeface, so it was **left out of this repo**. Flag for licence check |

### Kit type scale (desktop, then ≤767 px)

| Token | Size / line-height | Weight | Mobile |
|---|---|---|---|
| `primary` (H1, H3–H6 default) | 54 / 64 | 500 | 36 / 44 |
| `secondary` (H2 default) | 40 / 48 | 500 | 32 / 48 |
| `text` (body) | 18 / 26 | 400 | 16 / 24 (1.2rem ≤1366 px; 1.1rem/1.4rem ≤1200 px) |
| `accent` (buttons) | 16 | — | 16 |
| `4a940e7` | 32 / 40 | 500 | 24 / 32 |
| `ecb9a45` | 32 / 40 | 600 | 24 / 32 |
| `512b38a` | 24 / 32 | 500 | — |
| `c8fcd12` | 24 / 32 | — | 20 / 24 |
| `f88c025` | 20 / 28 | 600 | — |
| `3c2369c` | 18 / 24 | 500 | — |
| `daefeaa` | 16 / 22 | 500 | — |
| `7fb5109` | 16 / 22 | — | — |

### Sizes measured on key headings

| Element | Measured style |
|---|---|
| Home hero H1 "WHERE BRANDS GAIN MOMENTUM" | Plus Jakarta Sans 82/95, **800**, uppercase, `#54078B` |
| Home hero sub-line (H2) | 20/30, 400, `#4D4D4D` |
| Home section H2 | 40/48, 500, `#171717`; eyebrow H2 32/40, 500, `#7B7B7B` |
| Case-study hero H2 | 50/60, 700, white on purple |
| Case-study eyebrow / labels | 16, 600, `#F4B400`; labels 14/20, 500, letter-spacing 2 px |
| Case-study big stat | 45/55, 700, `#54078B` |
| About hero H1 | 54/64, 500, white on photo |

## 3. Buttons and CTAs

Measured in the browser, including hover. Most buttons have a 0.3 s transition defined, but **only the "View All" text button visibly changes on hover**.

| Style | Example | Spec |
|---|---|---|
| Primary (kit default) | "Download Portfolio" (header, footer) | bg `#54078B`, text white, Satoshi 16, radius 8, padding 8×32 (header: 10×20, 600) |
| Primary pill | "Schedule A Call" | bg `#54078B`, white, 1 px `#54078B` border, radius 100, padding 8×32, 16/400 |
| Outline pill | "Watch Our Showreel" | bg white, text black, 1 px `#54078B` border, radius 100 |
| Yellow CTA | "Get in Touch" (end-of-page banner) | bg `#F3C01F`, text `#54078B`, 18/500, padding 14×48, radius 8 |
| Text button | "View All", "Read case study" | transparent; `#696888` → `#54078B` on hover; 24/500 or 16/700 |
| Chip (not clickable) | "Pune HQ", "Remote first" | bg `#54078B` at 20%, text `#54078B`, radius 100 |
| Back-to-top | Footer, bottom right | Yellow circle with an arrow; appears after 300 px of scroll |

## 4. Layout and spacing

- Container max-width **1280 px** (95% on smaller screens). Default widget gap 20 px.
- Elementor breakpoints:

| Breakpoint | Width |
|---|---|
| Mobile | ≤767 px |
| Mobile landscape | ≤880 px |
| Tablet | ≤1024 px |
| Tablet landscape | ≤1200 px |
| Laptop | ≤1366 px |
| Widescreen | ≥2400 px |

- Header: white, 82 px, sticky. It gains shadow `0 6px 15px rgba(0,0,0,.14)` on scroll. Logo left, 3-item nav centre, CTA right.
- Cards: white, radius ~12–16 px, soft purple-tinted shadow (case-study stat cards), 1 px `#E5E2EC` border.
- Popups: 640 px wide, white, radius 15 px, dark overlay.

## 5. Logo and brand assets

| File | Size | Use |
|---|---|---|
| `assets/media/2026/01/MMAG-logo-2.png` | 104×128 | **Live logo** in header, footer and schema. Black "MM / AG" lettering in a yellow square with a yellow outline |
| `assets/media/2026/02/MMAG-logo.png`, `MMAG-logo-1.png` | 61×75, 128×158 | Earlier variants (not used on pages) |
| `assets/media/2026/02/cropped-Group-1171275584.png` | 512×512 | Favicon source (32/180/192/270 crops generated by WordPress) |
| `assets/media/2026/01/cropped-MMAG-scaled-1.webp`, `2026/02/cropped-Frame-82.png` | 512×512 | Older site-icon candidates |

No SVG version of the MMAG logo exists in the media library. Ask the design team for the vector master.

## 6. Iconography

- Font Awesome 5 icons rendered as inline SVG by Elementor: handshake, globe, trophy, linkedin-in, arrow-right, circle, and the social icons.
- Custom uploaded SVG icons for the footer email/phone/map icons and service icons. See `assets/media/**/*.svg`.

## 7. Motion and interaction (what the redesign should keep or replace)

| Effect | Where | How it is built |
|---|---|---|
| Entrance animations `fadeInUp` / `fadeInLeft` / `fadeInRight` | Most headings and images | Elementor motion |
| Custom cursor image (371×374 `png-of-hover-1.webp`) follows the mouse | Home hero, desktop only | HTML widget + JS (`backend/custom-code/01-js.js`, `06-html-widget.html`) |
| Scroll timeline: yellow box travels down an SVG line through Strategy, Design, Technology, Performance | Home "What we build" | GSAP 3.12 ScrollTrigger + MotionPath (`02`, `05`, `07`) |
| "Process" animation (desktop only) | Loaded site-wide | `04-js.js` (`initProcessOnlyAnimation`) |
| Looping muted MP4 micro-animations (0.2–0.7 MB each) | Discover/Define/Design/Drive and the four service pillars | Elementor video widgets |
| Counters animate from 0 | Case-study cards and stats | Elementor counter |
| Testimonial carousel with arrows and autoplay (5 slides) | Home | Elementor nested carousel |
| Client-logo carousel (mobile only) and culture photo carousel | Home, About | Elementor image carousel |
| Sticky header and back-to-top reveal after 300 px | Site-wide | Elementor sticky + `03-js.js` |
| Video lightboxes (YouTube showreel; MP4 portfolio reels) | Home, portfolio pages | Elementor lightbox |

## 8. Imagery style

- **Hero:** warm off-white grid background, floating yellow dots, client logos shown in colour.
- **Case studies:** solid purple hero with large dark-purple circles, white stat cards overlapping the hero edge.
- **About:** full-bleed team photo hero, founder portrait, team portrait cards, culture photo carousel.
- **Portfolio pages:** full-width 16:9 slide images on black, plus video thumbnails that open MP4s in a lightbox.
