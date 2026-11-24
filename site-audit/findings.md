# Findings to carry into the redesign (priority order)

Each finding gives the issue, the evidence (page or file), and the fix. Items marked **Needs approval** involve client claims or published data: do not change them without sign-off from the account owner or the client.

## High

| # | Issue | Evidence | Fix |
|---|---|---|---|
| H1 | The public contact email is a **temporary Hostinger staging address**: `rushi@teal-rhinoceros-988256.hostingersite.com` | `content/contact-us.md` (icon list) | Replace with the real business email. Confirm the address with Rushikesh / management |
| H2 | **Footer email icon has an empty link.** It opens the homepage in a new tab, on every page | `shared-layout.md` → footer links; `screenshots/interactions/popup-3691.png` (envelope icon) | Use `mailto:` with the confirmed email |
| H3 | The **"Get in Touch" end-of-page CTA does nothing** (`href="#"`) on Home and About. It is the main conversion button in that banner | `content/home.md`, `content/about-us.md` → interaction tests: "no popup" | Point it to `/contact-us/` or the Schedule A Call popup |
| H4 | **"View All" in "Work that speaks" has no link** | `content/home.md` section 4 | Link it to a public portfolio page |
| H5 | **Case-study numbers disagree or don't add up.** **Needs approval** before reuse | `content/case-studies*.md` | Verify each figure with the data owner, then use one approved number everywhere. Details: |
| | • Retail Florist: card says **6,000+** users; case study says **5,859+** | | |
| | • FMCG: "0.77% → 3.35% conversion rate (**+162%**)". 0.77 → 3.35 is +335% relative or +2.58 percentage points; neither is 162% | | |
| | • Retail Florist: "**22% return on ad spend**" reads as a loss (ROAS is usually a ratio such as 2.2x) | | |
| | • FMCG: "200% increase in ROI, reversing a −50% starting point". The base is unclear | | |
| H6 | **Headline claims conflict**: Home says "Trusted by startups to craft **100+ businesses**"; About says "**50+ Clients** across 4 industries" and then lists 5 industries. **Needs approval** | `content/home.md` S1; `content/about-us.md` S2, S4 | Agree one client count and industry list |
| H7 | **Typo on every page**: header button reads "Download **Portfoilo**" (the footer spells it correctly) | `shared-layout.md` → header | Fix the spelling |

## Medium

| # | Issue | Evidence | Fix |
|---|---|---|---|
| M1 | **No visible H1** on `/case-studies/` and all 7 case-study pages. Their only H1 is the theme title, which is hidden (`display:none`); the visible title is an H2 | `content/case-studies*.md` → Heading outline | One visible H1 per page in the redesign |
| M2 | **Alt text missing on 177 of 190 content images (93%)**, including client logos, team photos and the logo | "Images" table in each `content/*.md` | Write descriptive alt text; use empty alt only for decorative images |
| M3 | **Thin or placeholder pages are indexable and in the sitemap**: `/under-development/` (3 words), `/hello-world/` (default WordPress post, also in RSS), `/mmag-portfolio/` and `/website-portfolio/` (0 words, no meta description, no inbound links) | `README.md` page inventory; `backend/page-sitemap.xml` | Delete Hello World and Under Development. Noindex the portfolio pages or give them real text |
| M4 | **Hidden-but-published content** (hidden on all devices, still in the HTML): | `content/home.md` S5–S7; `content/about-us.md` S1 | Decide per block: bring it back in the redesign or drop it |
| | • Home: "WE BUILD TRUST PARTNERSHIP" section | | |
| | • Home: "Clients — They chose us" logo carousel | | |
| | • Home: Yash Group / EquiNext / Zendale work cards | | |
| | • About: a Wistia video | | |
| M5 | **Broken internal links** to `?page_id=4257` and `?page_id=1924` (404), inside the hidden Zendale/EquiNext cards | `data/links-all.csv` | Remove, or link to real pages if those cards return |
| M6 | **Schema is generic or wrong**: | `backend-tech.md` §7 | Use Organization/ProfessionalService with full NAP and social profiles; WebPage/AboutPage/ContactPage; CreativeWork for case studies; remove SearchAction |
| | • Every page is typed `Article` with author `admin` | | |
| | • Organization has no address, phone or `sameAs` | | |
| | • WebSite declares a site-search action that does not exist | | |
| M7 | **Weak meta**: | Field tables in each `content/*.md` | Rewrite titles and descriptions per page. Run the keyword step first (`keyword-fanout-map` skill) |
| | • Home title is "Home - Creative Agency In Pune" | | |
| | • Home meta description is 36 characters ("From Unique Strategies to Higher ROI") | | |
| | • OG image missing on Home and most pages | | |
| | • Portfolio pages have no meta description | | |
| M8 | **No business address (NAP) in text anywhere.** Footer has only icons; Contact has a map embed (`q=MMAG`) and the staging email. About mentions "Kothrud, Pune" in passing | `shared-layout.md`, `content/contact-us.md` | Show the full address, phone and email in footer and Contact (local SEO) |
| M9 | **Performance**: | `backend-tech.md` §9 | Remove duplicates and unused assets; compress or lazy-load videos; fix server caching |
| | • jQuery and GSAP each loaded twice on every page | | |
| | • Unused JetTabs assets load on every page | | |
| | • Home ≈6.3 MB / 169 requests | | |
| | • Uncached TTFB 1.6–3.0 s (estimate) | | |
| M10 | **About-page team LinkedIn icons**: 4 of 5 have no link (only the founder's works) | `content/about-us.md` S4 | Add profile URLs or remove the icons |
| M11 | **Case-study step numbering error**: Children's Enrichment approach runs 1, 2, 3, 4, **4** | `content/case-studies__education-childrens-enrichment.md` | Renumber to 5 |
| M12 | **Heading misuse**: labels such as "+3", "Finance", "UI/UX" and person names are H2s; eyebrows are H5/H6 | Heading outlines | Use H2/H3 only for real section and card titles |
| M13 | **Measurement gap**: GA4 only. No GTM, no Meta or LinkedIn pixel, and form conversion events are not visible from the front end | `backend-tech.md` §6 | Confirm GA4 key events with whoever owns analytics; plan GTM plus conversion tracking for the new site |
| M14 | **Case studies are near-orphans**: each one is linked only from Home and `/case-studies/`. There is no related or next case study, and no links from service mentions | README page inventory ("Pages linking in") | Add related-case-study and service links in the redesign (`internal-link-architect` skill can map them) |
| M15 | **Security hygiene** (passive checks): | `backend-tech.md` §8 | Hand to whoever manages hosting; not a redesign blocker |
| | • No security headers | | |
| | • `readme.html` exposes the WordPress version | | |
| | • "admin" username is public | | |
| | • Default login URL | | |
| | • Public `mcp` REST namespace (needs a wp-admin review) | | |
| | • SPF has no Google Workspace include (verify) | | |

## Low

| # | Issue | Evidence | Fix |
|---|---|---|---|
| L1 | **Copy typos**: | `content/home.md` S1, S9; `content/about-us.md` S3; `shared-layout.md` | Fix MMAG's own copy. Testimonial typos only with the client's OK (**Needs approval**) |
| | • "Rushikesh kate" (lowercase k) | | |
| | • "All right reserved" (should be "All rights reserved") | | |
| | • Testimonials: "teh", "be be a asset", "MMag", "MMAG team's has done" | | |
| | • "Trusted by startups to craft 100+ businesses" (awkward wording) | | |
| L2 | **Off-palette colours** (`#F4B400` vs brand `#F3C01F`; three greys; three off-whites) | `brand-theme.md` §1 | Use `brand-tokens.css` |
| L3 | **Buttons have no hover state** (bg unchanged) | `brand-theme.md` §3 | Add hover and focus states |
| L4 | **Social links' accessible names** are icon IDs ("Linkedin-in", "Facebook-f") | `shared-layout.md` | Use "MMAG on LinkedIn" and similar |
| L5 | **Default theme 404 page** ("The page can't be found.") | `content/this-page-does-not-exist-404-check.md` | Design a branded 404 with links |
| L6 | **Media library clutter**: | `data/assets-summary.json`, `data/media-library.csv` | Clean up after the redesign; check the font licence |
| | • 222 of 377 items not used on any page | | |
| | • 40 MP4s ≈430 MB | | |
| | • 10 unused Lottie files (one invalid: `trust.json`) | | |
| | • An Aeonik font from a free-font site (commercial typeface; licence unclear) | | |
| L7 | **Geography mismatch**: About says "India & USA", but case studies include Australia (florist) and Zambia (Trade Kings Group site `.co.zm`) | `content/about-us.md`, case studies | Align the geography line (**Needs approval**) |
| L8 | **External links to check**: | `data/link-check.csv` | Re-check manually in a browser; replace dead client links |
| | • `zen-dale.com` (client site linked from both portfolio pages) returned **500** | | |
| | • `suiteearth.com` and LinkedIn returned 403/999 (bot blocking; likely fine, **unverified**) | | |
| | • Three Google Drive links on `/mmag-portfolio/`: confirm they are shared publicly | | |
