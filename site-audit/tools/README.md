# Re-running the capture

Requires Node 18+ with Playwright (Chromium) and Python 3.

The scripts are run from outside this folder. Keep raw downloads in a separate working directory.

1. Build a seed list. Use the sitemap URLs plus any extra URLs (e.g. `/hello-world/` and a fake URL for the 404 page), one per line, in `seeds.txt`.

2. Crawl. This takes about 60 s per page:

   ```bash
   node crawl.js <site-audit-dir> seeds.txt
   ```

3. Map widgets to sections and read the popup forms:

   ```bash
   node pass2.js <site-audit-dir>
   ```

4. Link check. Put one URL per line in `urls.txt`:

   ```bash
   bash linkcheck.sh urls.txt <site-audit-dir>/data/link-check.csv
   ```

5. Generate the docs. `<raw-dir>` must contain `wp_pages.json`, which is the output of `https://mmag.in/wp-json/wp/v2/pages?per_page=100`:

   ```bash
   python3 -I build_report.py <site-audit-dir> <raw-dir>
   ```

What the scripts do and don't do:
- Forms are never submitted. `crawl.js` only calls `checkValidity()`.
- Popups are opened by clicking their trigger buttons.
- Nothing logs in.
