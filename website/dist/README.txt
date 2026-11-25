MMAG website · build v1.0

Deploy: upload this folder's contents (or the zip) to any static host. index.html is at the root.
  - Netlify: drag the unzipped folder onto app.netlify.com/drop. Forms work there out of the box.
  - Other hosts: set assets/js/config.js → formEndpoint to a form service URL, or forms show a "call us" fallback.
Preview locally: run `python3 -m http.server` in this folder, then open http://localhost:8000
(opening index.html directly from disk breaks folder links and some browser features).

Settings: assets/js/config.js (form endpoint, portfolio link, GA4 ID, phone, Three.js version).
Redirects for old mmag.in URLs: _redirects (Netlify / Cloudflare Pages format).
