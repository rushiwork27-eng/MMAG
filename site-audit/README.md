# mmag.in: full site capture for the redesign

Captured **24 Nov 2026** from the live site with a headless Chromium browser and public endpoints only:
- Every page loaded on desktop (1440 px) and mobile (390 px) and scrolled top to bottom.
- Every button, popup, lightbox, carousel, menu and form tested by clicking. Forms were **checked but not submitted**.
- Every link and asset URL status-checked.

No wp-admin access was used, so anything behind login is listed under *Not covered*.

**Merged with an earlier scrape (zip, 12 Oct 2026):**
- Everything it held that this capture didn't is added: 2 since-removed Zendale pages, 22 images, a custom script and a few links.
- Duplicates were dropped.
- What changed on the site between the two dates is in [`changes-oct-to-nov.md`](changes-oct-to-nov.md).

## Start here

| If you need… | Open |
|---|---|
| All copy, section by section, for any page | [`content/`](content/): one file per page, top-to-bottom, with headings, text, buttons (and where they go), images, videos, counters, carousels, hidden blocks, forms, links and the heading outline |
| Header, footer, popups and their forms, sticky/scroll behaviour | [`shared-layout.md`](shared-layout.md) |
| Colours, fonts, type scale, buttons, spacing, logo, motion | [`brand-theme.md`](brand-theme.md) + [`brand-tokens.css`](brand-tokens.css) |
| WordPress, plugins, hosting, DNS, forms backend, analytics, SEO plumbing, security, performance | [`backend-tech.md`](backend-tech.md) |
| What is broken, wrong or risky, by priority, with fixes | [`findings.md`](findings.md) |
| What changed between the 12 Oct zip scrape and this capture, and what the zip added | [`changes-oct-to-nov.md`](changes-oct-to-nov.md) |
| Pages that no longer exist (Zendale), preserved from the zip | [`content/removed__case-studies__zendale.md`](content/removed__case-studies__zendale.md), [`content/removed__work__zendale.md`](content/removed__work__zendale.md) |
| Both scrapes combined and de-duplicated (pages, links, images, scripts/stylesheets), each row flagged by source and status today | [`data/combined/`](data/combined/) |
| Images, SVGs and Lottie files from the media library (downloaded) | [`assets/media/`](assets/media/) (same folder structure as `/wp-content/uploads/`) |
| Inventory of every media item (alt text, size, URL) | [`data/media-library.csv`](data/media-library.csv) |
| Which assets each page uses | [`data/assets-used.csv`](data/assets-used.csv) |
| Every link on the site with its HTTP status | [`data/links-all.csv`](data/links-all.csv), [`data/link-check.csv`](data/link-check.csv) |
| Full-page screenshots (desktop + mobile), popups, menus, carousels | [`screenshots/`](screenshots/) |
| Custom JS/CSS from Elementor HTML widgets (cursor, GSAP timeline…) | [`backend/custom-code/`](backend/custom-code/README.md) |
| Raw data (per-page JSON, REST API dumps, raw HTML, sitemap, robots, kit CSS) | [`data/pages/`](data/pages/), [`backend/`](backend/) |

## Site at a glance

- **Platform:** WordPress 7.1.5 + Hello Elementor theme + Elementor Pro 4.2. SEO by Rank Math. GA4 `G-9WNY7XF2FT`. Hosted on Webhostbox / Unified Layer. Email on Google Workspace.
- **Navigation:** 3 flat items, no dropdowns: About Us · Case Studies · Contact Us.
  - Header CTA: "Download Portfoilo" (typo), opens a lead-capture popup.
  - Mobile: hamburger with the same 3 items.
- **Footer:**
  - Logo.
  - Icons for email (link is empty), phone `+91-8308852044` and Google Maps.
  - The same 3 links.
  - Social: Instagram `@mmag_india`, LinkedIn `/company/mmagindia`, YouTube `@mmag2717`, Facebook `/mmag.india`.
  - "Download Portfolio" button, copyright bar, back-to-top button.
- **Lead capture:** 3 Elementor forms, all with reCAPTCHA v3:
  - Download Portfolio popup.
  - Schedule A Call popup.
  - Contact page form.
- **Brand:** purple `#54078B` + yellow `#F3C01F` on warm off-white `#FAF9F5`. Plus Jakarta Sans headings, Satoshi body.
- **Content volume:** 15 live URLs (14 pages + 1 default post). There is no blog.
  - 7 case studies, plus 2 image-only portfolio pages.
  - 1 placeholder page ("Under Development").
  - 377 public media items (40 are MP4s, ≈430 MB), plus 22 images recovered from the zip.
  - **Removed since 12 Oct** (all 404 now): 2 Zendale pages (archived here), plus `/work/`, `/case-studies/yash-industries/` and `/case-studies/equinext/` (links only, never captured).

## Page inventory

| URL | Title tag | Visible H1 | Status | Words* | Meta desc | In sitemap | Pages linking in | Docs |
|---|---|---|---|---|---|---|---|---|
| [/](https://mmag.in/) | Home - Creative Agency In Pune | WHERE BRANDS GAIN MOMENTUM | 200 | 1171 | yes | yes | 15 | [content](content/home.md) · [desktop](screenshots/desktop/home.jpg) · [mobile](screenshots/mobile/home.jpg) |
| [/about-us/](https://mmag.in/about-us/) | About Us - MMAG | We're not a vendor. We're your growth partner | 200 | 273 | yes | yes | 15 | [content](content/about-us.md) · [desktop](screenshots/desktop/about-us.jpg) · [mobile](screenshots/mobile/about-us.jpg) |
| [/case-studies/](https://mmag.in/case-studies/) | Case Studies - MMAG | — none visible | 200 | 342 | yes | yes | 15 | [content](content/case-studies.md) · [desktop](screenshots/desktop/case-studies.jpg) · [mobile](screenshots/mobile/case-studies.jpg) |
| [/contact-us/](https://mmag.in/contact-us/) | Contact Us - MMAG | CONTACT US | 200 | 66 | yes | yes | 15 | [content](content/contact-us.md) · [desktop](screenshots/desktop/contact-us.jpg) · [mobile](screenshots/mobile/contact-us.jpg) |
| [/case-studies/retail-florist/](https://mmag.in/case-studies/retail-florist/) | Retail Florist - MMAG | — none visible | 200 | 280 | yes | yes | 2 | [content](content/case-studies__retail-florist.md) · [desktop](screenshots/desktop/case-studies__retail-florist.jpg) · [mobile](screenshots/mobile/case-studies__retail-florist.jpg) |
| [/case-studies/fmcg-d2c-food/](https://mmag.in/case-studies/fmcg-d2c-food/) | FMCG - D2C Food - MMAG | — none visible | 200 | 276 | yes | yes | 2 | [content](content/case-studies__fmcg-d2c-food.md) · [desktop](screenshots/desktop/case-studies__fmcg-d2c-food.jpg) · [mobile](screenshots/mobile/case-studies__fmcg-d2c-food.jpg) |
| [/case-studies/education/](https://mmag.in/case-studies/education/) | Education - MMAG | — none visible | 200 | 240 | yes | yes | 2 | [content](content/case-studies__education.md) · [desktop](screenshots/desktop/case-studies__education.jpg) · [mobile](screenshots/mobile/case-studies__education.jpg) |
| [/case-studies/education-childrens-enrichment/](https://mmag.in/case-studies/education-childrens-enrichment/) | Education - Children’s Enrichment - MMAG | — none visible | 200 | 326 | yes | yes | 2 | [content](content/case-studies__education-childrens-enrichment.md) · [desktop](screenshots/desktop/case-studies__education-childrens-enrichment.jpg) · [mobile](screenshots/mobile/case-studies__education-childrens-enrichment.jpg) |
| [/case-studies/real-estate-luxury/](https://mmag.in/case-studies/real-estate-luxury/) | Real Estate - Luxury - MMAG | — none visible | 200 | 267 | yes | yes | 2 | [content](content/case-studies__real-estate-luxury.md) · [desktop](screenshots/desktop/case-studies__real-estate-luxury.jpg) · [mobile](screenshots/mobile/case-studies__real-estate-luxury.jpg) |
| [/case-studies/b2b-engineering-manufacturing/](https://mmag.in/case-studies/b2b-engineering-manufacturing/) | B2B Engineering / Manufacturing - MMAG | — none visible | 200 | 224 | yes | yes | 2 | [content](content/case-studies__b2b-engineering-manufacturing.md) · [desktop](screenshots/desktop/case-studies__b2b-engineering-manufacturing.jpg) · [mobile](screenshots/mobile/case-studies__b2b-engineering-manufacturing.jpg) |
| [/case-studies/e-commerce-fair-trade-goods-b2b/](https://mmag.in/case-studies/e-commerce-fair-trade-goods-b2b/) | E-commerce - Fair-Trade Goods (B2B) - MMAG | — none visible | 200 | 287 | yes | yes | 2 | [content](content/case-studies__e-commerce-fair-trade-goods-b2b.md) · [desktop](screenshots/desktop/case-studies__e-commerce-fair-trade-goods-b2b.jpg) · [mobile](screenshots/mobile/case-studies__e-commerce-fair-trade-goods-b2b.jpg) |
| [/mmag-portfolio/](https://mmag.in/mmag-portfolio/) | Mmag Portfolio - MMAG | — none visible | 200 | 0 (image-only) | **no** | yes | 0 | [content](content/mmag-portfolio.md) · [desktop](screenshots/desktop/mmag-portfolio.jpg) · [mobile](screenshots/mobile/mmag-portfolio.jpg) |
| [/website-portfolio/](https://mmag.in/website-portfolio/) | Website Portfolio - MMAG | — none visible | 200 | 0 (image-only) | **no** | yes | 0 | [content](content/website-portfolio.md) · [desktop](screenshots/desktop/website-portfolio.jpg) · [mobile](screenshots/mobile/website-portfolio.jpg) |
| [/under-development/](https://mmag.in/under-development/) | Under Development - MMAG | WEBSITE UNDER DEVELOPMENT | 200 | 3 | yes | yes | 0 | [content](content/under-development.md) · [desktop](screenshots/desktop/under-development.jpg) · [mobile](screenshots/mobile/under-development.jpg) |
| [/hello-world/](https://mmag.in/hello-world/) | Hello world! - MMAG | — none visible | 200 | 124 | yes | no | 0 | [content](content/hello-world.md) · [desktop](screenshots/desktop/hello-world.jpg) · [mobile](screenshots/mobile/hello-world.jpg) |
| [/this-page-does-not-exist-404-check/](https://mmag.in/this-page-does-not-exist-404-check/) | Page Not Found - MMAG | — none visible | 404 | - | **no** | no | 0 | [content](content/this-page-does-not-exist-404-check.md) · [desktop](screenshots/desktop/this-page-does-not-exist-404-check.jpg) · [mobile](screenshots/mobile/this-page-does-not-exist-404-check.jpg) |
| [/case-studies/zendale/](https://mmag.in/case-studies/zendale/) | Zendale - MMAG | — none visible | **404 (removed; archived 12 Oct)** | 326 | yes | no | 0 (hidden Home card points to `?page_id=1924`) | [content](content/removed__case-studies__zendale.md) · [content record](screenshots/desktop/removed__case-studies__zendale.jpg) |
| [/work/zendale/](https://mmag.in/work/zendale/) | Zendale - MMAG | — none visible | **404 (removed; archived 12 Oct)** | 135 | yes | no | 0 (hidden Home card points to `?page_id=4257`) | [content](content/removed__work__zendale.md) · [content record](screenshots/desktop/removed__work__zendale.jpg) |

\*Words = all visible text on the page, including about 40 words of header and footer.

**Site structure:**

```
/                         Home
├── /about-us/
├── /case-studies/        (listing: 7 cards, shared template #5041, also embedded on Home)
│   ├── /retail-florist/                   Website + Social + Paid
│   ├── /fmcg-d2c-food/                    Social + Paid
│   ├── /education/                        Branding + Paid
│   ├── /education-childrens-enrichment/   Website redesign (UI/UX)
│   ├── /real-estate-luxury/               Performance marketing
│   ├── /b2b-engineering-manufacturing/    Social (LinkedIn)
│   └── /e-commerce-fair-trade-goods-b2b/  SEO
├── /contact-us/
├── not linked from anywhere: /mmag-portfolio/, /website-portfolio/, /under-development/, /hello-world/
└── REMOVED (404 now; live on 12 Oct): /case-studies/zendale/ (page 1924), /work/zendale/ (page 4257),
    /work/, /case-studies/yash-industries/, /case-studies/equinext/
Popups (every page): #3691 Download Portfolio · #3962 Schedule A Call (Home only)
```

Case-study pages are linked only from Home and the listing. There is no "next / related case study" navigation between them.

## Top issues (full list in [findings.md](findings.md))

1. The public contact email is a temporary Hostinger staging address. The footer email icon has an empty link.
2. "Get in Touch" (Home, About) and "View All" (Home → Work that speaks) are dead buttons.
3. Case-study numbers conflict or don't add up (6,000+ vs 5,859+; "+162%" for 0.77% → 3.35%; "22% ROAS"). Home says "100+ businesses" but About says "50+ clients". **Needs approval** before any copy is reused.
4. "Download Portfoilo" typo in the header on every page.
5. No visible H1 on `/case-studies/` or any case study. 93% of content images have no alt text.
6. Placeholder and thin pages are indexable (Under Development, Hello World, image-only portfolio pages).
7. *(from the merged zip)* The Zendale case study and Zendale work page were live on 12 Oct and now 404. Three more URLs they linked to (`/work/`, `/case-studies/yash-industries/`, `/case-studies/equinext/`) are also 404. Decide whether to restore Zendale or redirect the old URLs. Its content and images are preserved here.

## How this was captured (so it can be re-run)

1. Public endpoints: `robots.txt`, `sitemap_index.xml`, RSS, WordPress REST API (`/wp-json/wp/v2/pages|posts|media|types|…`), DNS via Google DNS-over-HTTPS.
2. Browser crawl (Playwright/Chromium). It started from the sitemap, then followed every internal link it found. On each page it:
   - Scrolled the full page so lazy content and animations loaded.
   - Extracted every Elementor widget in order, with its section, responsive visibility and animation.
   - Hovered nav items and buttons.
   - Clicked every popup/lightbox trigger, tab, carousel arrow and the mobile hamburger.
   - Ran form validation without submitting.
   - Took desktop and mobile full-page screenshots.
3. Second pass: opened each popup to read its form fields, and mapped every widget to its page section.
4. Link check: HEAD request, then a 1-byte GET as fallback, on 597 unique URLs (links, images, videos, scripts, stylesheets).
5. Generated these markdown docs from the JSON.
6. Merged the 12 Oct zip scrape:
   - Diffed its text, links, images, forms, meta, scripts and stylesheets against this capture.
   - Re-extracted its two unique pages (removed Zendale pages) with the same widget extractor. Page scripts were off and the network was limited to mmag.in assets.
   - Downloaded their still-live images and built the combined tables.

The scripts are in [`tools/`](tools/): `crawl.js`, `pass2.js`, `linkcheck.sh` and `build_report.py`, plus the merge tools `combine_scrapes.py`, `archive_extract.js`, `archive_record.py`, `shoot_record.js` and `htmltext.py`.

## Not covered (needs wp-admin or team input)

- **Form handling:** where submissions go (email, CRM, sheet); the post-submit message or redirect; auto-replies.
- **Elementor internals:** global colour and typography names (only IDs are public), template library, popup display conditions and triggers beyond button clicks, custom code snippets.
- **Server side:** plugin settings, users and roles, Wordfence configuration, backups, the `mcp` REST endpoint's permissions, and caching setup (LiteSpeed plugin on a non-LiteSpeed server).
- **Measurement:** GA4 key events and Search Console data.
- **Media and fonts:**
  - 66 media items not listed publicly by the REST API (443 reported vs 377 visible). These are attachments of unpublished pages; 22 were recovered via the zip, leaving 44 unidentified.
  - The vector logo master.
  - Licences for Satoshi and Aeonik. Font files are **not** committed here: Satoshi loads from `https://mmag.in/wp-content/uploads/2026/01/Satoshi-Variable.ttf`.
- **Videos:** the 40 MP4s were listed with URLs but not downloaded (≈430 MB). They are in `data/media-library.csv` and the page docs.
