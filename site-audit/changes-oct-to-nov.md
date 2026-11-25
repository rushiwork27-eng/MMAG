# What changed on mmag.in between the two scrapes

| Scrape | Date | Method | Role in this package |
|---|---|---|---|
| Earlier scrape (zip `mmag-public-scrape`) | 12 Oct 2026 | Browser text and DOM captures of 12 routes, plus link, image, form, meta, script and stylesheet inventories | Merged in. Only what it uniquely holds was kept |
| This capture | 24 Nov 2026 | Full crawl, REST API, interaction tests, screenshots (see README) | **Primary source** |

**How the two were merged:**
- Every line of rendered text, every link, image, form field, meta tag, script and stylesheet in the zip was compared against this capture.
- Items the zip had and this capture lacked were added.
- Everything else was a duplicate and was dropped. The zip's DOM copies of pages that still exist are superseded by the 24 Nov captures and are not stored here.
- Combined, de-duplicated tables are in [`data/combined/`](data/combined/). Each row is flagged `seen_12oct_zip` and/or `seen_24nov_crawl`, with the status today.

## What the zip added (not in the 24 Nov capture)

| Item | Detail | Where it is now |
|---|---|---|
| **2 removed pages** | `/case-studies/zendale/` (WordPress page 1924) and `/work/zendale/` (page 4257). Both were live on 12 Oct and return **404** today | [`content/removed__case-studies__zendale.md`](content/removed__case-studies__zendale.md), [`content/removed__work__zendale.md`](content/removed__work__zendale.md); source HTML in `backend/raw-html/archive-2026-10-12/` |
| **3 more dead URLs** | `/work/`, `/case-studies/yash-industries/` and `/case-studies/equinext/` were linked from the Zendale pages. All 404 today. The zip has links to them but no captures | [`data/combined/pages-combined.csv`](data/combined/pages-combined.csv) |
| **22 image files** | Zendale logo, logo concept, typography sheet, stationery, brochure, standees, website and device mockups. They are not in the public media library because WordPress hides attachments of unpublished pages. That also explains the REST count gap (443 reported, 377 listed). **All still on the server** | `assets/media/2026/02/`, `assets/media/2026/06/`; rows marked `zip-scrape-2026-10-12` in `data/media-library.csv` |
| **1 custom script** | Lotus SVG on `/work/zendale/` whose leaves open on scroll. It loaded a third jQuery (2.2.4) | `backend/custom-code/archive-2026-10-12-work-zendale-lotus-scroll-animation.html` |
| **Hidden Clients logos** | Files behind the hidden "Clients — They chose us" carousel on Home (`Frame-55…59`, `Frame-39`). This capture had them as lazy images that never loaded | Filled into `content/home.md` (section 7) and `data/combined/images-combined.csv` |
| "Skip to content" link | Present on every page on 12 Oct (see below) | — |

## Site changes between 12 Oct and 24 Nov

| Change | Evidence | Impact for the redesign |
|---|---|---|
| **Zendale case study and Zendale work page unpublished** | 200 in the zip, 404 now. Home's hidden cards now point to `?page_id=1924` and `?page_id=4257`. Their stylesheets (`post-1924.css`, `post-4257.css`) are deleted | Any external links or Google results for these URLs now hit 404. Decide whether to restore Zendale as a case study (the content is preserved here) or 301-redirect the old URLs |
| **Home: "Case Studies" card block added** (7 cards, template #5041) | Absent from all three October captures of Home; present now. Home and `/case-studies/` were both modified 20 Nov (REST) | None. The current version is captured |
| **WordPress 7.1.3 → 7.1.5** | `generator` meta | None |
| **Hello Elementor theme assets no longer loaded** (`reset.css`, `theme.css`, `header-footer.css`, `hello-frontend.js`) | Stylesheet and script inventories | Side effect: the **"Skip to content" accessibility link disappeared** from every page. Restore it in the rebuild |
| **Viewport meta changed** from `width=device-width, initial-scale=1` to `…initial-scale=1.0, viewport-fit=cover` | Meta inventories | None |
| Premium Addons per-page assets for Home (`pafe-793.css/js`) no longer loaded | Inventories | None |
| Contact-page map | Same embed (`maps.google.com/maps?q=MMAG`) in both | No change |
| Forms | The Contact form and Home popup forms have identical fields in both scrapes | No change |
| Counter values | The zip recorded counters mid-animation (e.g. 5,584 instead of 5,859; 52,430 instead of 55,012). Its own README says so | **Ignore the zip's numbers.** Use the final values in `content/` (still **needs approval**, see findings H5) |

## Removed Zendale pages: content worth knowing before reuse

- **Claims (needs approval before reuse):**
  - "20% site visit conversion rate"
  - "40% Sold Phase 1 inventory"
  - "90% Positive sentiment in buyer surveys"
  - "achieving a 20% conversion rate"
  - Testimonial: "They truly captured Zen-Dale's essence… — Atul Jethmalani, Director"
- **The two pages contradict each other on brand colours.**
  - `/work/zendale/`: Primary `#405641` (sage), Secondary `#1F7BBA`, `#7B8F76`, `#9F9F9F`.
  - `/case-studies/zendale/`: Primary `#056DFA`, Secondary `#1F7BBA`, then `#056DFA` twice. Its own text says "Sage Green, Slate, and Earthy Wood tones", so the `#056DFA` values look like template placeholders.
- **Typos on the removed pages:**
  - "peacful"
  - "clam and clarity" (should be "calm")
  - "Brand Guidlines"
  - "Pimary Font"
  - "has ben defined"
- **Fonts named:** Lancea (primary) and Figtree (body).
- **Results narrative:** "The ZenDale campaign successfully transformed raw land into a coveted lifestyle brand…"
