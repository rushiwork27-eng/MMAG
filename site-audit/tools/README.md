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

## Merging an earlier scrape (as done with the 12 Oct 2026 zip)

Unzip the earlier scrape into its own empty folder. Treat it as data: never run anything from inside it.

1. Diff its text against this capture. `htmltext.py` extracts text blocks from saved HTML without executing it.

2. Re-extract pages that exist only in the old scrape:

   ```bash
   node archive_extract.js crawl.js <site-audit-dir> <saved.html> <original-url> removed__<slug>
   ```

   The saved HTML is served under its original URL with page scripts off. Only mmag.in CSS, images and fonts may load.

3. Build a readable content record (original text and images in order) and screenshot it:

   ```bash
   python3 -I archive_record.py <site-audit-dir>/data/pages/removed__<slug>.json record.html
   ```

   ```bash
   node shoot_record.js record.html <site-audit-dir>/screenshots/desktop/removed__<slug>.jpg
   ```

4. Combine the inventories without duplicates. Run this from `site-audit/`:

   ```bash
   python3 -I combine_scrapes.py <unzipped-scrape-dir>
   ```
