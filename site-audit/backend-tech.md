# Backend and tech stack: mmag.in

All findings come from public sources only:
- HTTP headers, page source and the public WordPress REST API
- `robots.txt`, sitemaps and the RSS feed
- Public DNS (Google DNS-over-HTTPS)

No login was attempted and no forms were submitted. Anything that needs wp-admin access is marked **needs wp-admin**. Raw data is in `backend/`.

## 1. Platform

| Layer | Finding | Evidence |
|---|---|---|
| CMS | WordPress **7.1.5** (it was 7.1.3 on 12 Oct 2026, per the zip scrape) | `<meta name="generator">`, RSS feed generator |
| Theme | Hello Elementor 3.5.1 | Its `reset.css`, `theme.css`, `header-footer.css` and `hello-frontend.js` loaded on 12 Oct. They no longer load (24 Nov), and the theme's "Skip to content" link went with them |
| Page builder | Elementor **4.2.4** + Elementor Pro **4.2.2** | Generator meta, asset versions |
| Elementor features | Inline SVG icons, additional custom breakpoints, external CSS print method, Google Fonts with `font-display: swap` | Generator meta |
| Templates | Header #47, Footer #619, case-study cards container #5041, portfolio containers #3850 and #3858, popups #3691 (Download Portfolio) and #3962 (Schedule A Call) | `data-elementor-id` attributes |
| Unpublished pages | 1924 = `/case-studies/zendale/`, 4257 = `/work/zendale/` (live on 12 Oct, 404 now; their `post-<id>.css` files are deleted) | Zip scrape + `?page_id=` links on Home. See `changes-oct-to-nov.md` |

## 2. Plugins detected

| Plugin | How detected | Used on front end? |
|---|---|---|
| Elementor / Elementor Pro | Assets, REST `elementor/v1`, `elementor-pro/v1` | Yes: all pages, forms, popups, sticky header, carousels |
| Rank Math SEO (with AI-visibility and Content AI modules) | Sitemap comment, REST `rankmath/v1/*`, schema | Yes: sitemap, schema, meta |
| JetTabs 2.2.3 | Assets on every page, REST `jet-tabs-api/v1` | **No tabs found on any page**, so its CSS/JS loads for nothing |
| Premium Addons for Elementor | `elements-handler.min.js` | Unclear (handler loaded on every page) |
| Country Code Field for Elementor Form 1.7.4 | Assets | Yes: phone field with country picker (default India +91) |
| LiteSpeed Cache | REST `litespeed/v1`, `litespeed/v3` | Unclear. The server is not LiteSpeed (see hosting) |
| Wordfence + Wordfence Login Security | REST `wordfence/v1`, `wordfence-login-security/v1` | Security plugin (back end) |
| All-in-One WP Migration | REST `ai1wm/v1` | Back end. Suggests the site was migrated from another host |
| Elementor AI / "Elementor One" | REST `elementor-ai/v1`, `elementor-one/v1` | Back end |
| WordPress MCP / Abilities API | REST `mcp`, `wp-abilities/v1` | Back end. An MCP endpoint is exposed on the public REST index. **needs wp-admin** to confirm what it allows |

The full namespace list is in `backend/wp-rest/site-root-namespaces.json`.

## 3. Hosting, DNS and email (inferred from public DNS)

| Item | Value | Inference |
|---|---|---|
| A record | `162.241.27.65` (PTR `162-241-27-65.unifiedlayer.com`) | Unified Layer / Newfold Digital infrastructure |
| Nameservers | `cns3999.webhostbox.net`, `cns4000.webhostbox.net` | Webhostbox reseller hosting |
| Server header | Alternated between `Apache` and `nginx/1.31.8` with `X-Proxy-Cache: HIT`, `X-Server-Cache: true` | nginx cache proxy in front of Apache |
| MX | `aspmx.l.google.com` + alternates | Email on **Google Workspace** |
| SPF | `v=spf1 ip4:69.49.232.70 a mx include:websitewelcome.com ~all` | Authorises the host's mail servers. It does **not** include `_spf.google.com`, so Gmail-sent mail may fail SPF. **Verify with the email admin** |
| Other TXT | `google-site-verification=…` | Google Search Console is verified |
| Redirects | `http://` → `https://` (301); `www` → apex (301) | Correct |
| Contact email shown on site | `rushi@teal-rhinoceros-988256.hostingersite.com` | A **Hostinger temporary/staging domain**. Together with the migration plugin, this suggests the site was built on Hostinger and moved. The email is almost certainly not the intended public address |

TLS certificate details were not captured, because the cloud proxy used for this audit re-signs HTTPS traffic.

## 4. Content model (REST API)

| Type | Count | Notes |
|---|---|---|
| Pages | 14 published | 7 case studies are child **pages** of `/case-studies/` (ID 3167), not a custom post type |
| Posts | 1 | Default "Hello world!" (2026-01-05) is still published, indexable and in the RSS feed |
| Categories / tags | 1 (Uncategorized) / 0 | There is no blog |
| Media | 377 listed publicly (header reports 443 total). The gap is attachments of unpublished pages, which WordPress hides from the public API. 22 of these (the Zendale pages) were recovered via the zip scrape and are still served from `/wp-content/uploads/` | 199 WebP, 76 SVG, 49 PNG, 2 JPG, **40 MP4 (≈430 MB)**, 10 JSON (Lottie, none used on pages, one invalid), 1 TTF. 222 of the 377 are not referenced on any live page (approximate; see `data/assets-summary.json`) |
| Floating buttons (`e-floating-buttons`) | 0 | Type exists, nothing published |
| Elementor library / snippets | Private (401) | **needs wp-admin** |

Page IDs, dates and parent relationships: `backend/wp-rest/pages.json`. Builder HTML of each page: `backend/raw-html/*.rest-content.html`.

## 5. Forms and lead capture

| Form | Location | Fields (required*) | Submit |
|---|---|---|---|
| Download Portfolio Popup (#3691) | Header and footer "Download Portfolio" buttons on every page | Name*, Email*, Phone* (country picker), Organization*, Inquiry* (dropdown), Message | "Download Portfolio" |
| Schedule A Call Popup (#3962) | Home hero "Schedule A Call" | Same fields as above | "Schedule A Call" |
| Contact form ("New Form") | /contact-us/ | Full Name*, Work Email*, Contact Number*, interest checkboxes (Strategy / Design / Technology / Performance), Project Brief | "Submit" |

The Inquiry dropdown options are: Website Development, E-Commerce Marketing, Branding, Social Media Marketing, Search Engine Optimization, Lead Generation, Email Marketing, App Development, Others.

- All three forms are Elementor Pro forms posting to `wp-admin/admin-ajax.php`, protected by **reCAPTCHA v3** (invisible, inline badge).
- **Not visible from the front end:** where submissions go (email, CRM, webhook, Google Sheet), what the "Download Portfolio" form returns after submit, and whether an auto-reply is sent. **needs wp-admin** (Elementor → Submissions, and each form's Actions After Submit).
- The two portfolio pages (`/mmag-portfolio/`, `/website-portfolio/`) have no inbound links. They are probably the post-submit destination of the portfolio form. **Unverified**: the form was not submitted, to avoid sending a fake lead.

## 6. Analytics and tracking

| Tool | Status |
|---|---|
| Google Analytics 4 | `G-9WNY7XF2FT`, loaded with gtag.js on every page |
| Google Tag Manager | Not present (only `gtag/js`) |
| Meta Pixel, LinkedIn Insight, Hotjar, Clarity | **Not detected** |
| Conversion events on form submit | Not detectable from the front end. **needs GA4 access** |
| DoubleClick calls | Come from the YouTube embed only |

## 7. SEO plumbing (Rank Math)

- **Sitemap:** `/sitemap_index.xml` → `page-sitemap.xml` (14 URLs). It includes `/under-development/` and both portfolio pages. `/sitemap.xml` and `/wp-sitemap.xml` 301 to it.
- **robots.txt:** standard WordPress rules plus the sitemap line.
- **Meta tags:** title tags follow `%page% - MMAG`; the home title is "Home - Creative Agency In Pune". Canonical tags are present.
- **OG images:** missing on Home and on most pages.
- **Schema graph on every page:** Organization (logo only; no address, phone or social `sameAs`), WebSite with SearchAction (site search is not used), WebPage, Person "admin", and **Article**. Article is the wrong type for service and company pages.
- **Exposed username:** the author "admin" appears in schema, in `twitter:data1` ("Written by admin") and in the RSS feed.
- **Visible H1:** the theme's own H1 page title is output but hidden (`display:none`). Case-study pages and `/case-studies/` therefore have **no visible H1**.

## 8. Security posture (passive checks only)

| Check | Result |
|---|---|
| `/wp-json/wp/v2/users` | 401 (user listing blocked) ✔ |
| `/wp-admin/` | 302 to the default `/wp-login.php` (reachable at the default URL) |
| `/xmlrpc.php` | 405 on GET (XML-RPC state for POST not tested) |
| `/readme.html`, `/license.txt` | 200 (reveal the WordPress version) |
| Security headers on HTML | **None set**: no HSTS, CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy or Permissions-Policy |
| Username "admin" | Public via schema, meta and feed |

## 9. Front-end performance (measured from this cloud container; treat as estimates)

| Page | Requests | Transfer | TTFB | Load |
|---|---|---|---|---|
| Home | 169 | ≈6.3 MB | 0.3 s (cache hit) | 4.1 s |
| About | 157 | ≈1.4 MB | 1.6 s | 3.3 s |
| Contact | 128 | ≈0.7 MB | 3.0 s | 4.9 s |
| Case studies (each) | ≈86 | ≈0.07 MB after cache | 1.6–2.4 s | 2.1–3.0 s |
| MMAG Portfolio | 152 | ≈6.0 MB | 1.6 s | 2.3 s (55,500 px tall) |

Causes worth fixing in the rebuild:
- **jQuery loaded twice**: WordPress core plus `code.jquery.com/jquery-3.6.0` from a footer HTML widget on every page.
- **GSAP loaded twice** (3.12.2 and 3.12.5) on every page, though the timeline only runs on Home.
- JetTabs, Premium Addons and Font Awesome 4 shims load on every page.
- `wp-emoji` script loads on every page.
- Uncached TTFB of 1.6–3.0 s.

## 10. Custom code inventory

Nine custom snippets live inside Elementor HTML widgets and inline scripts: cursor follower, scroll progress line, GSAP timeline, process animation, back-to-top reveal, Wistia player, and a duplicate jQuery include. They are saved verbatim with an index in [`backend/custom-code/`](backend/custom-code/README.md).
