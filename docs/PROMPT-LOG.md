# MMAG redesign: prompt log

Every prompt, the approach taken, what went wrong, and what was delivered. Newest first.

**Versioning:** each prompt that changes the website ships a new zip in [`releases/`](../releases/). Large changes bump the major number (v1.0 → v2.0); small fixes bump the minor number (v1.0 → v1.1).

| Version | Date | Prompt in one line | Zip |
|---|---|---|---|
| — | 25 Nov 2026 | Run the website on localhost | — (no site change) |
| v1.0 | 25 Nov 2026 | Build the website: 3D in every section, one horizontal scroll, the live site's forms | [`mmag-website-v1.0.zip`](../releases/mmag-website-v1.0.zip) |
| — | 25 Nov 2026 | Decide flow and pages (site plan) | — |
| — | 25 Nov 2026 | Merge the older zip scrape | — |
| — | 24 Nov 2026 | Scrape and evaluate mmag.in | — |

---

## (no version) · 25 Nov 2026 · Run the website on localhost

**Prompt**

> Run this website in local host as well for me to look

**Approach:** the site runs in a cloud container, whose localhost the user's browser can't reach. Checked for a connected computer (Remote Control): none attached.

**Challenge:** no way to start a server on the user's machine from this session.

**Output:** step-by-step local run instructions:
- unzip, then `python3 -m http.server 8000` or `npx serve .`
- open http://localhost:8000
- noted that forms can't send locally and that double-clicking `index.html` won't work

Alternatives offered: connect the computer via Remote Control, or Netlify Drop for a shareable link. No site change, so no new zip.

---

## v1.0 · 25 Nov 2026 · First build of the new website

**Prompt**

> Keep documenting every prompt, its approach, challenges, and your output in the background from now. I need a zip file I can drag, drop, and deploy. Keep versioning the zip file in every prompt. Small changes can be sub-versioned. Like v2.2. Reference: https://copula.agency/
> 1. All sections should have some 3D element or amazing new layouts like the reference website. I don't want even a single plain, normal section. Give each section the importance of a hero section. You can get those from: gsap.com (read docs and install if possible), awwwards.com, Three.js loaded from a CDN. All built with code, no image files.
> 2. All index files should be unminified. 3. One Horizontal scroll. 4. Navbar CTA: "Download Portfolio". 5. "Schedule a Call" (CTA) on the rest of the pages. 6. Check the form details on the website and use those in the form.

**Approach**

1. **Reference.** copula.agency crashed in headless Chrome (a JS chunk failed through the proxy). I fed the chunks in manually, so the page loaded and its text and structure came through, but its scroll animations never fired and the screenshots were blank. Patterns used from its structure:
   - oversized kinetic type
   - a manifesto with letter-by-letter scroll reveal
   - a dictionary-style definition ("mo·men·tum · noun")
   - a big repeated CTA
2. **Stack** (static site, no build step needed to deploy):
   - **GSAP 3.15.1** (ScrollTrigger, SplitText), installed from npm and vendored. The package states it is free including commercial use.
   - **Lenis 1.3.27** (MIT) for smooth scroll, installed from npm.
   - **Three.js 0.187.0** from the jsDelivr CDN.
   - All vendored files are the libraries' readable (unminified) builds.
3. **3D engine.** One shared WebGL renderer draws every 3D element into its section's rectangle (scissor rendering). This avoids the browser's WebGL-context limit. 13 scenes, all generated in code with no textures or image files:
   - momentum blob
   - ribbons
   - DNA helix
   - service objects that morph per service
   - particle numbers that assemble on scroll
   - dotted globe with Pune → USA arcs
   - particle wave
   - assembling shards
   - growth bars
   - torus knot
   - gyroscope rings
   - confetti
   - 404 tunnel
4. **Layouts.**
   - **The one horizontal scroll:** Home case studies, with particle numbers per panel.
   - Pinned process steps driving the helix.
   - Stacking service cards that switch the 3D object.
   - A CSS-3D ring of client names.
   - A scroll-scrubbed statement.
   - Tilt cards with code-generated art, flip cards for the team, and a quote carousel.
   - Also: marquee, magnetic buttons, custom cursor, preloader and page-wipe transitions.
5. **Pages (18).**
   - Home and Work.
   - 7 case studies at `/work/<slug>/`.
   - Services hub and 5 service pages.
   - About, Contact, a draft privacy policy, and a 404.
   - Sitemap from the 25 Nov site plan.
6. **CTAs.** Navbar: "Download Portfolio" on every page, desktop and mobile. Hero, end-of-page, mobile bar and footer: "Schedule a Call".
7. **Forms.** Fields copied from the live site:
   - **Download Portfolio** and **Schedule a Call** (same as the live popups): Name*, Email*, Phone Number* with country code (India +91 default), Organization*, Inquiry* (the same 9 options), Message.
   - **Contact** (same as the live page): Full Name*, Work Email*, Contact Number*, Strategy / Design / Technology / Performance, Project Brief, with the same placeholders.
   - Submission goes through Netlify Forms by default, with a honeypot for spam. On other hosts, set a form endpoint in `config.js`.
8. **Generator.** All content lives in `website/build/content.py`. `build.py` writes the unminified HTML; `make_release.sh` builds and zips.
9. **QA.**
   - Every page was run in headless Chrome with software WebGL, scrolled top to bottom and screenshotted at desktop (1440) and mobile (390).
   - Checked: console errors, horizontal overflow, modal open/close and focus, validation, submit fallback, mobile menu, 404.
   - The final zip was unzipped into an empty folder, served, and checked again.

**Challenges and fixes**

| Problem | Cause | Fix |
|---|---|---|
| Reference site crashed in the headless browser | A JS chunk failed through the proxy | Fed the chunks in through curl; the text came through but the animations never fired, so worked from its structure |
| GSAP ScrollSmoother would hide text under the 3D canvas | It transforms the page wrapper, which changes stacking | Used Lenis (no transform) with ScrollTrigger instead |
| 3D objects leaked into other sections; blank screens after the horizontal scroll | Pinned ScrollTriggers created out of page order | Create all pins top-to-bottom |
| Counters looked empty | CSS `.number span` also hit the digits | Scoped to direct children |
| Quotes overlapped the next content | Absolute positioning reserved no height | Grid stacking |
| 3D objects behind big headlines hurt legibility | Placement | Moved scenes further right; added a soft text shadow |
| Zendale page styling (previous prompt) could not be rebuilt | Its stylesheet was deleted | Not used in v1.0 (Zendale pending decision) |

**Output**

| Item | Value |
|---|---|
| Zip | `releases/mmag-website-v1.0.zip` (≈228 KB, 33 files, 0 image files) |
| Pages | 18 (Home, Work, 7 case studies, Services, 5 services, About, Contact, Privacy, 404) |
| Sections with a 3D element | All. The Home clients section uses a CSS-3D ring; every other section has a WebGL scene |
| Horizontal scrolls | 1 (Home → case studies) |
| Source | `website/src` (CSS/JS), `website/build` (content + generator), `website/dist` (built site) |
| Deploy helpers | `_redirects` (old mmag.in URLs → new), `robots.txt`, `sitemap.xml`, `README.txt` |

**Assumptions taken (flag if wrong)**

- **"No image files" applies to the whole site, not only the 3D.** Client logos, work images and team photos are replaced by names, code-generated art and initials. Real images can return in a v1.x once permissions are cleared (site plan, decision 3).
- **The navbar CTA is "Download Portfolio"**, as you specified. This overrides the plan's "Book a call" proposal (decision 6 closed).
- **Numbers and claims are as published on the live site** (still pending approval, findings H5/H6), with three exceptions:
  - The FMCG "+162%" was dropped because it doesn't match 0.77% → 3.35%.
  - Home's "100+ businesses" is not used; About's "50+ clients" is.
  - The Retail Florist figure uses the case page's 5,859+, not the card's 6,000+.
- **Testimonials are verbatim**, client typos included.
- **Left out pending decisions:** Aam Aadmi Party, Zendale, and a WhatsApp number.
- **Contact email is omitted.** The live site shows a staging address (findings H1).
- **New copy needs sign-off:** service headlines, one-liners and the "mo·men·tum" definition. They make no factual claims.

**Needs action before going live**

1. Confirm the public email and add it to `assets/js/config.js` and the contact page.
2. A portfolio PDF link for `config.js → portfolioUrl`. Until then the form says the team will email it.
3. Choose the host:
   - **Netlify:** forms work as is.
   - **Elsewhere:** set `formEndpoint`.
4. GA4: set `ga4Id` only on the production deploy.
5. Approvals:
   - all numbers
   - new copy
   - privacy policy text (legal)
   - client names shown in the ring and the project list
6. Domain cut-over: apply `_redirects`, then submit `sitemap.xml` in Search Console.

---

## Before logging started (summary)

| Date | Prompt | Output |
|---|---|---|
| 24 Nov 2026 | Scrape and evaluate mmag.in (front end and back end) | `site-audit/`: content per page, brand theme, tech stack, findings, assets, screenshots |
| 25 Nov 2026 | Merge an older zip scrape, remove duplicates | Two removed Zendale pages archived, 22 images, `data/combined/`, `changes-oct-to-nov.md` |
| 25 Nov 2026 | Decide the website flow and pages | `redesign/site-structure-plan.html` (sitemap, journeys, blueprints, 11 decisions) |
