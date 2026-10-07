# Wanton Group website: handover

The same six pages, the same design and the same approved copy, upgraded for
search, sharing, speed, accessibility and enquiries. Every existing URL is
unchanged (`index.html`, `about.html`, `hospitality.html`, `fmcg.html`,
`ajuni-luxe.html`, `contact.html`, plus the `#restaurants`, `#hotels` and
`#franchise` anchors), so nothing already shared breaks.

## Folders

| Folder | What it is |
|---|---|
| `dist/` | **Upload this.** The finished website: plain HTML, CSS, JS, images. |
| `src/` | The editable source that `dist/` is built from. |
| `build.py` | Rebuilds `dist/` from `src/`. Holds phone numbers, WhatsApp messages and page titles. |
| `_original/` | The site exactly as it was live before this upgrade, for rollback. |
| `brand-reference/` | Logo, brand sheets and the approved copy deck. |
| `tools/` | Generator for the share images (only needed if you change them). |

## Design (October 2026 redesign)

The site follows one idea: quiet heritage luxury. It's built on Wanton House's
own details: the 1969 storefront, the "Since 1969" seal, the shield, and the
carved arches inside the restaurant, which appear as the arch-shaped photo frames.

**Each vertical has its own world**, under the shared Wanton Group header and footer:

- **Hospitality (Wanton House):** "after dark". Lacquer night, lantern gold and the red of the shield; lantern light follows the cursor.
- **FMCG (WHS Sauces):** cream, deep red and antique gold from the WHS brand sheet. The page leads with the jar, and the range shows Original Schezwan plus a "packaging to follow" card for Sweet Garlic.
- **Ajuni Luxe:** green and gold from the business card, including its double gold frame. Corporate gifting has its own brief: company, number of gifts, needed by, budget.

Design render boards for Home, About and the three verticals are in `renders/`.

**Interactions.** All of them are subtle, run on a small script with no
libraries, and switch off for visitors who turn off motion on their device.

- **Header:** turns solid as you scroll, with a thin gold progress line along its bottom edge.
- **Seals:** the "Since 1969" seal on Home and About and the WHS seal turn gently as you scroll.
- **Home:**
  - The outlined "1969" behind the hero drifts slowly as you scroll.
  - A one-line statement whose words light up as you read.
  - Three arched "doors" for the ventures; they lift on hover, and on phones they become a swipeable row.
  - The heritage numbers (1969, 3rd, 3) count up when they come into view.
- **Heritage photos:** they arrive in sepia and develop into colour (Home feature and Hospitality).
- **WHS jar:** tilts slightly toward the cursor on desktop.
- **Ajuni Luxe:** a gold sheen passes across the wordmark, and the four collection icons draw themselves in.
- **Mobile menu:** full-screen, with large serif links and a WhatsApp button.
- **Page changes:** a soft cross-fade in browsers that support it.

## What changed

**Search and sharing**
- Every page has a written title and meta description, a canonical URL, and Open Graph / Twitter tags.
- Each page has its own 1200×630 share image, so links shared on WhatsApp, LinkedIn or Facebook show a proper card instead of a bare URL.
- Structured data (schema.org) tells Google the facts:
  - **Wanton Group:** Organization, founded 1969 by Sardar Darshan Singh Chawla.
  - **Wanton House:** Restaurant.
  - **Hotel Wanton House:** Hotel.
  - **Ajuni Luxe:** Store.
  - **WHS Original Schezwan Sauce:** Product.
  - **Every inner page:** breadcrumbs.
- New `sitemap.xml`, `robots.txt`, a favicon set (browser tab, iPhone home screen, Android), a web manifest, and a branded `404.html`.

**Speed**
- Images are no longer embedded inside each page. They are separate, cached files in modern WebP format, sized for phone or desktop. Hospitality went from 804 KB to about 410 KB.
- Fonts are hosted on the site itself instead of Google Fonts, so they no longer block the first paint. Each page loads only the font families it uses.
- The Restaurant Guru badge stylesheet no longer blocks the page from rendering.
- Content no longer fades in all at once on load. Sections below the fold ease in as you scroll, and the top of each page appears immediately.

**Accessibility**
- Every failing contrast pair is fixed, including the gold labels on the home page and the WHS page, the footer text and the form labels.
- Keyboard users now see a visible focus outline.
- There's a "Skip to content" link.
- The mobile menu tells screen readers whether it is open, and closes with Escape or when you tap a link.
- Headings are in proper order, and the logo is announced once instead of three times.

**Fixes**
- Hospitality photo collage layout: preserved and now responsive.
- On About, the timeline dots no longer overlap the headings, and the timeline now shows **2022** for WHS Sauces and **2026** for Ajuni Luxe.
- On the WHS page, the "For HoReCa & bulk orders" and "For every kitchen" labels were unstyled; they're fixed.
- The home page cards are aligned, and the Restaurant Guru badge sits below them.
- The phone is now a tappable **+91 98679 39177** link everywhere. The landlines are kept as text on Contact.

**Enquiries**
- WhatsApp links now pre-fill what you need to know:
  - **Franchise:** name, city, F&B experience.
  - **Trade / HoReCa:** business, city, monthly requirement.
  - **Corporate gifts:** company, number, date, budget.
  - **Table reservations and hotel stays:** date, time or check-in/out, guests.
- Ajuni Luxe always uses **93212 15812**. Everything else uses **98679 39177**.
- Hospitality now shows the restaurant and hotel addresses, "Reserve on WhatsApp", "Enquire about a stay" and "Get directions".
- The contact form now sends by **WhatsApp** (no email app needed) or by email. It checks the fields first, and routes Ajuni Luxe enquiries to Ajuni's number.

## Lighthouse, before and after (mobile)

Order: Performance / Accessibility / Best practices / SEO

| Page | Before (old live site) | After (redesign) |
|---|---|---|
| Home | 91 / 93 / 93 / 91 | 91 / 100 / 96 / 100 |
| About | 88 / 93 / 93 / 91 | 97 / 100 / 100 / 100 |
| Hospitality | 66 / 93 / 93 / 91 | 93 / 100 / 96 / 100 |
| FMCG | 87 / 93 / 93 / 91 | 94 / 100 / 100 / 100 |
| Ajuni Luxe | 96 / 93 / 93 / 91 | 93 / 100 / 96 / 100 |
| Contact | 95 / 94 / 93 / 91 | 98 / 100 / 100 / 100 |

Desktop is 100 for Performance, Accessibility and SEO on every page.

These were measured on a local test server. In that test environment the three
third-party embeds (Restaurant Guru, the SociableKit and Elfsight Instagram
feeds) were blocked, so live numbers will differ slightly.

## How to upload

1. In your hosting panel's **File Manager**, open the website folder (usually `public_html`).
2. Download a backup of what's there (or rely on `_original/` in this repository).
3. Upload **everything inside `dist/`** into that folder, overwriting the old pages. Include:
   - the `assets/` folder;
   - `favicon.ico`, `site.webmanifest`, `robots.txt`, `sitemap.xml`, `404.html`;
   - the hidden **`.htaccess`** file. Turn on "show hidden files" in the File Manager if you can't see it.
4. Open https://www.wantongroup.com on your phone and click through each page.

**About `.htaccess`.** It sets browser caching and the custom 404 page on Apache-based hosting, and every rule is wrapped so it can't break the site. Your server reports itself as nginx. Many panels run nginx in front of Apache and still read `.htaccess`.

If the 404 page doesn't appear after upload, ask your host to add the following to the site's nginx config:

```
error_page 404 /404.html;
location ~* \.(webp|jpg|png|ico|woff2)$ { expires 30d; add_header Cache-Control "public"; }
location ~* \.(css|js)$ { expires 7d; }
```

## After upload (once, about 15 minutes)

1. **Google Search Console** (search.google.com/search-console): add `https://www.wantongroup.com`, verify it, then submit `sitemap.xml` under **Sitemaps**.
2. **Rich Results Test** (search.google.com/test/rich-results): paste the home page and Hospitality URLs. They should show Organization, Restaurant and Hotel.
3. **Google Business Profiles:** make sure the restaurant, hotel and Ajuni Luxe listings link to the matching page:
   - restaurant: `/hospitality.html#restaurants`
   - hotel: `/hospitality.html#hotels`
   - Ajuni Luxe: `/ajuni-luxe.html`
4. **Share previews:** WhatsApp caches previews. Test by sending a link with something unique on the end, e.g. `https://www.wantongroup.com/?v=2`.

## How to make changes later

You need Python 3 and Pillow once: `pip install pillow`. Then:

```
python3 build.py        # rebuilds dist/ from src/
```

- **Text on a page:** edit `src/pages/<page>.html`, rebuild, upload that page from `dist/`.
- **Header or footer** (all pages at once): edit `src/partials/header.html` or `footer.html`.
- **Phone numbers, WhatsApp messages, page titles, descriptions, structured data:** edit the settings at the top of `build.py`.
- **Colours and layout:** `src/assets/css/styles.css`.
- **Replace a photo:** put the new file in `src/assets/img/` with the same name and rebuild. The build makes the phone and desktop sizes for you.
- **Add a photo:** add it to `src/assets/img/`, add one line to `IMAGES` in `build.py`, and use `{{pic:name|description for screen readers|display size}}` in a page.
- **Hotel Wanton House photos** (when ready): in `src/pages/hospitality.html`, replace the `<div class="media-placeholder">…</div>` block with a `<div class="photo-collage">` built the same way as the restaurant's.
- **Share images:** edit `tools/og-cards.html`, then run `node tools/og.mjs` (needs Node with `playwright-core` and Chromium).

For an urgent typo you can also edit the HTML in `dist/` directly in the File Manager. Make the same change in `src/` afterwards so the next rebuild keeps it.

## Still open

- **Hotel Wanton House (Vashi):** photos, and the year it opened (to show on the About timeline).
- **WHS Sweet Garlic Sauce:** packaging photo and approved copy.
- **Wanton House practical details:** opening hours and menu. Once supplied they go on Hospitality and into the Restaurant structured data, which helps Google show them.
- **Leadership portraits** for the About page (they replace the initials circles).
- **Google Business Profile links** for each location, to replace the "View on map" search links.
- **Form email:** if you'd like form submissions delivered to an inbox automatically (instead of opening WhatsApp or the visitor's email app), choose an address and a free service such as Web3Forms.
- **Instagram widgets and Restaurant Guru badge:** these only render on the live domain, so check them after upload.
