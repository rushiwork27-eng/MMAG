# Shared layout — header, footer, popups, site-wide behaviour

Source page: https://mmag.in/ (header #47 and footer #619 are the same Elementor templates on every page).

## Header (Elementor template #47) — sticky, white, 82px tall; logo left, menu centre, CTA right

### Header row 1
_height 82px · bg #FFFFFF_

- Image: `https://mmag.in/wp-content/uploads/2026/01/MMAG-logo-2.png` (local: ../assets/media/2026/01/MMAG-logo-2.png) — 104×128 — alt: **missing** → https://mmag.in/
- Nav menu:
  - About Us → https://mmag.in/about-us/
  - Case Studies → https://mmag.in/case-studies/
  - Contact Us → https://mmag.in/contact-us/
- **Button:** "Download Portfoilo" → opens popup #3691 (Download Portfolio)

**All header links:**

- (icon/logo) → https://mmag.in
- About Us → https://mmag.in/about-us/
- Case Studies → https://mmag.in/case-studies/
- Contact Us → https://mmag.in/contact-us/
- Download Portfoilo → opens popup #3691 (Download Portfolio)

## Footer (Elementor template #619)

### Footer row 1
_height 261px · bg #FFFFFF_

- Image: `https://mmag.in/wp-content/uploads/2026/01/MMAG-logo-2.png` (local: ../assets/media/2026/01/MMAG-logo-2.png) — 104×128 — alt: **missing** → https://mmag.in/
- Social icons:
  -  → https://mmag.in/
  -  → tel:+91-8308852044
  -  → https://maps.app.goo.gl/wxVkVbBEvJV89RsL7
- Icon list:
  - About Us → https://mmag.in/about-us/
  - Case Studies → https://mmag.in/case-studies/
  - Contact Us → https://mmag.in/contact-us/
- HTML widget (custom CSS/JS): `//You can replace offset value from here var offset = 300 $(window).on('load scroll', function(){ if( $(window).scrollTop() > offset ){ $('body').addClass('show…` — full code in `data/pages/<slug>.json`
- **H2:** Follow us on
- Social icons:
  - Instagram → https://www.instagram.com/mmag_india/
  - Linkedin-in → https://www.linkedin.com/company/mmagindia
  - Youtube → https://www.youtube.com/@mmag2717
  - Facebook-f → https://www.facebook.com/mmag.india/
- **Button:** "Download Portfolio" → opens popup #3691 (Download Portfolio)

### Footer row 2
_height 52px · bg #54078B_

- Text:
  > Copyright © 2026 MMAG, All right reserved
- **Button:** "(icon only)" → #

**All footer links:**

- (icon/logo) → https://mmag.in
- (icon/logo) → (no link) (new tab)
- (icon/logo) → tel:+91-8308852044 (new tab)
- (icon/logo) → https://maps.app.goo.gl/wxVkVbBEvJV89RsL7 (new tab)
- About Us → https://mmag.in/about-us/
- Case Studies → https://mmag.in/case-studies/
- Contact Us → https://mmag.in/contact-us/
- Instagram → https://www.instagram.com/mmag_india/ (new tab)
- Linkedin-in → https://www.linkedin.com/company/mmagindia (new tab)
- Youtube → https://www.youtube.com/@mmag2717 (new tab)
- Facebook-f → https://www.facebook.com/mmag.india/ (new tab)
- Download Portfolio → opens popup #3691 (Download Portfolio)
- (icon/logo) → #

## Popups (Elementor popup templates)

### Popup #3691 — triggered by "Download Portfoilo"

_size [640, 604] · bg #FFFFFF · radius 15px_ · [screenshot](screenshots/interactions/popup-3691.png)

Headings: H2: Download Portfolio

Visible text:

```
Download Portfolio

Enter your details for quick access to our work

Name
Email
Phone Number
India +91
+91
Organization
Inquiry
Inquiry
Website Development
E-Commerce Marketing
Branding
Social Media Marketing
Search Engine Optimization
Lead Generation
Email Marketing
App Development
Others
Message
Download Portfolio
```

**Form `Download Portfolio Popup`** — submit: Download Portfolio — reCAPTCHA: yes

| Label | Type | Name | Placeholder | Required | Options |
|---|---|---|---|---|---|
| Name | text | form_fields[name] | Name | yes |  |
| Email | email | form_fields[email] | Email | yes |  |
| Phone Number | text |  | Search |  |  |
| Phone Number | tel | form_fields[field_ad8b800] | Phone Number | yes |  |
| Organization | text | form_fields[field_5db25e9] | Organization | yes |  |
| Inquiry | select-one | form_fields[field_5d34cd5] |  | yes | Inquiry, Website Development, E-Commerce Marketing, Branding, Social Media Marketing, Search Engine Optimization, Lead Generation, Email Marketing, App Development, Others |
| Message | textarea | form_fields[message] | Message |  |  |
|  | textarea | g-recaptcha-response |  |  |  |

### Popup #3962 — triggered by "Schedule A Call"

_size [640, 521] · bg #FFFFFF · radius 15px_ · [screenshot](screenshots/interactions/popup-3962.png)

Headings: H2: Schedule A Call

Visible text:

```
Schedule A Call
Name
Email
Phone Number
India +91
+91
Organization
Inquiry
Inquiry
Website Development
E-Commerce Marketing
Branding
Social Media Marketing
Search Engine Optimization
Lead Generation
Email Marketing
App Development
Others
Message
Schedule A Call
```

**Form `Schedule A Call Popup`** — submit: Schedule A Call — reCAPTCHA: yes

| Label | Type | Name | Placeholder | Required | Options |
|---|---|---|---|---|---|
| Name | text | form_fields[name] | Name | yes |  |
| Email | email | form_fields[email] | Email | yes |  |
| Phone Number | text |  | Search |  |  |
| Phone Number | tel | form_fields[field_ad8b800] | Phone Number | yes |  |
| Organization | text | form_fields[field_5db25e9] | Organization | yes |  |
| Inquiry | select-one | form_fields[field_5d34cd5] |  | yes | Inquiry, Website Development, E-Commerce Marketing, Branding, Social Media Marketing, Search Engine Optimization, Lead Generation, Email Marketing, App Development, Others |
| Message | textarea | form_fields[message] | Message |  |  |
|  | textarea | g-recaptcha-response |  |  |  |

## Every popup / lightbox trigger found

| Button text | Action | Result when clicked | Pages |
|---|---|---|---|
| Download Portfoilo | opens popup #3691 (Download Portfolio) | popup opened | home, about-us, case-studies, contact-us, hello-world, this-page-does-not-exist-404-check, case-studies__b2b-engineering-manufacturing, case-studies__e-commerce-fair-trade-goods-b2b, case-studies__education, case-studies__education-childrens-enrichment, case-studies__fmcg-d2c-food, case-studies__real-estate-luxury, case-studies__retail-florist |
| Schedule A Call | opens popup #3962 (Schedule A Call) | popup opened | home |
| Watch Our Showreel | opens video lightbox: https://www.youtube.com/embed/HVSOqY1VJ1E?feature=oembed | lightbox opened | home |
| Get in Touch | # | nothing opened | home, about-us |
| Download Portfolio | opens popup #3691 (Download Portfolio) | popup opened | home, about-us, case-studies, contact-us, hello-world, this-page-does-not-exist-404-check, case-studies__b2b-engineering-manufacturing, case-studies__e-commerce-fair-trade-goods-b2b, case-studies__education, case-studies__education-childrens-enrichment, case-studies__fmcg-d2c-food, case-studies__real-estate-luxury, case-studies__retail-florist |
|  | # | nothing opened | home, about-us, case-studies, contact-us, mmag-portfolio, mmag-portfolio, hello-world, this-page-does-not-exist-404-check, case-studies__b2b-engineering-manufacturing, case-studies__e-commerce-fair-trade-goods-b2b, case-studies__education, case-studies__education-childrens-enrichment, case-studies__fmcg-d2c-food, case-studies__real-estate-luxury, case-studies__retail-florist |
|  | opens video lightbox: https://embed-ssl.wistia.com/deliveries/ed6a7a6841e30428c3545d937faeae04b843da37/file.mp4 | lightbox opened | mmag-portfolio |

## Site-wide behaviour (tested on desktop 1440 px)

- **Sticky header:** at top → position `fixed`, bg #FFFFFF, height 82px. After scrolling 1600px → sticky active: True, shadow `rgba(0, 0, 0, 0.14) 0px 6px 15px 0px`. [screenshot](screenshots/interactions/home-scrolled-header.png)
- **Custom cursor image** (`#cursor-image`): present — follows the mouse on desktop (HTML widget with JS).
- **Scroll progress line** (`#progressLine`): present — drives the 'What we build' timeline animation.
- **Back-to-top button:** icon-only button in the footer bar (href `#`); the footer HTML widget adds `body.show` after 300px of scroll to reveal it. Clicking it jumps to the top (tested).
- **Desktop nav hover:** 3 items, dropdown sub-menus: 0 (none).
- **Mobile hamburger menu:** items About Us, Case Studies, Contact Us. [screenshot](screenshots/interactions/home-mobile-menu.png)
- Sticky element settings: `[{"dataId": "885477a", "sticky": "top", "on": ["widescreen", "desktop", "laptop", "tablet_extra", "tablet", "mobile_extra", "mobile"], "offset": 0, "effectsOffset": 0}, {"dataId": "885477a", "sticky": "top", "on": ["widescreen", "desktop", "laptop", "tablet_extra", "tablet", "mobile_extra", "mobile"], "offset": 0, "effectsOffset": 0}, {"dataId": "e98e048", "sticky": "top", "on": ["widescreen", "desktop", "laptop", "tablet_extra", "tablet", "mobile_extra", "mobile"], "offset": 90, "effectsOffset": 0}, {"dataId": "e98e048", "sticky": "top", "on": ["widescreen", "desktop", "laptop", "tablet_extra", "tablet", "mobile_extra", "mobile"], "offset": 90, "effectsOffset": 0}]`
- **Floating buttons (WhatsApp/chat):** none rendered on the page

## Custom code embedded in pages (HTML widgets / inline scripts)

Saved verbatim in `backend/custom-code/`. These power the GSAP scroll timeline, custom cursor, progress line and scroll-offset behaviour.
