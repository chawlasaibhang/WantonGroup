#!/usr/bin/env python3
"""Build the Wanton Group website into dist/.

    python3 build.py

Needs Python 3.8+ and Pillow (pip install pillow). Output in dist/ is a plain
folder of HTML/CSS/JS/images to upload to the hosting panel as-is.

Edit text in src/pages/*.html, shared header/footer in src/partials/,
styles in src/assets/css/styles.css, and site-wide facts (phone numbers,
WhatsApp messages, page titles) in the SITE and PAGES settings below.
"""
import datetime
import html
import json
import re
import shutil
from pathlib import Path
from urllib.parse import quote, quote_plus

from PIL import Image

ROOT = Path(__file__).parent
SRC = ROOT / "src"
DIST = ROOT / "dist"
BASE_URL = "https://www.wantongroup.com/"
TODAY = datetime.date.today().isoformat()

# --------------------------------------------------------------------------
# Site-wide facts. Change a number or message here and rebuild.
# --------------------------------------------------------------------------
GROUP_WA = "919867939177"   # Group, hospitality, FMCG
AJUNI_WA = "919321215812"   # Ajuni Luxe only

WHATSAPP = {
    "general":     (GROUP_WA, "Hi, I'd like to know more about Wanton Group."),
    "restaurant":  (GROUP_WA, "Hi, I'd like to reserve a table at Wanton House, Bandra.\nDate:\nTime:\nNumber of guests:"),
    "hotel":       (GROUP_WA, "Hi, I'd like to enquire about a stay at Hotel Wanton House, Vashi.\nCheck-in date:\nCheck-out date:\nNumber of guests:"),
    "franchise":   (GROUP_WA, "Hi, I'm interested in a Wanton House franchise.\nName:\nCity / location:\nF&B experience:"),
    "whs":         (GROUP_WA, "Hi, I'd like to know more about WHS Sauces."),
    "sweetgarlic": (GROUP_WA, "Hi, I'd like to know when WHS Sweet Garlic Sauce is available."),
    "horeca":      (GROUP_WA, "Hi, I'd like to enquire about WHS Sauces 2.5 KG packs for my business.\nBusiness name:\nCity:\nApprox. monthly requirement:"),
    "ajuni":       (AJUNI_WA, "Hi, I'd like to know more about Ajuni Luxe."),
    "gifting":     (AJUNI_WA, "Hi, I'd like to enquire about Ajuni Luxe corporate gifts.\nCompany:\nNumber of gifts:\nNeeded by (date):\nBudget per gift (approx.):"),
    "decor":       (AJUNI_WA, "Hi, I'm interested in Ajuni Luxe home décor."),
    "accessories": (AJUNI_WA, "Hi, I'm interested in Ajuni Luxe luxury accessories."),
    "imports":     (AJUNI_WA, "Hi, I'm interested in Ajuni Luxe import collections."),
}

MAPS = {
    "group":      "Shams Palace 98 Hill Road Bandra West Mumbai 400050",
    "restaurant": "Wanton House, Shop No 4, Shams Palace, 98 Hill Road, Bandra West, Mumbai 400050",
    "hotel":      "Hotel Wanton House, Plot 14, Sector 26A, Palm Beach Road, Vashi, Navi Mumbai 400705",
    "ajuni":      "Shop No 7, G-10, Palai Commercial Complex, Senapati Bapat Marg, Dadar West, Mumbai 400028",
}

NAV = [("about.html", "About us"), ("hospitality.html", "Hospitality"), ("fmcg.html", "FMCG"),
       ("ajuni-luxe.html", "Ajuni Luxe"), ("contact.html", "Contact")]

# Responsive image set: source file -> widths to generate (largest = original size cap)
IMAGES = {
    "ext1_web":        ("ext1_web.jpg", [450, 700]),
    "int1_web":        ("int1_web.jpg", [350, 700]),
    "int2_web":        ("int2_web.jpg", [350, 700]),
    "whs_jar_clean":   ("whs_jar_clean.jpg", [550, 1000]),
    "since_1969":      ("since_1969.png", [213, 426]),
    "wanton_shield":   ("wanton_shield.png", [56, 132, 263]),
    "wanton_wordmark": ("wanton_wordmark.png", [274, 547]),
}

RG_BADGE = """<div class="rg-badge">
        <div id="b-rcircle" data-length="29" class="b-rcircle_black rg-award-lang-en_US" onclick="if(event.target.nodeName.toLowerCase() != 'a') {window.open(this.querySelector('.b-rcircle_r-link').href);return 0;}">
          <a href="https://restaurant-guru.in/Wanton-House-Mumbai-2" class="b-rcircle_r-link" target="_blank" rel="noopener">Wanton House</a>
          <p class="b-rcircle_year">2026</p>
          <div class="b-rcircle_bottom"><p class="b-rcircle_str1">Recommended</p></div>
          <div class="b-rcircle_heading">
            <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="144px" height="144px" viewBox="0 0 144 144">
              <defs><path id="b-rcircle-arc" d="M 12 72 a 60 60 0 0 0 120 0"></path></defs>
              <text class="b-rcircle_heading__bottom" fill="#fff" text-anchor="middle">
                <textPath startOffset="50%" xlink:href="#b-rcircle-arc"><a href="https://restaurantguru.com/" target="_blank" rel="noopener" class="b-rcircle_heading__link">Restaurant Guru</a></textPath>
              </text>
            </svg>
          </div>
        </div>
      </div>"""
RG_CSS = '<link rel="stylesheet" href="https://awards.infcdn.net/2026/r_rcm.css" media="print" onload="this.media=\'all\'">'

# --------------------------------------------------------------------------
# Structured data (schema.org). Only facts confirmed by the family.
# --------------------------------------------------------------------------
ORG_ID = BASE_URL + "#organization"
ADDR_GROUP = {"@type": "PostalAddress", "streetAddress": "Shams Palace, 98 Hill Road, Bandra West",
              "addressLocality": "Mumbai", "addressRegion": "Maharashtra", "postalCode": "400050", "addressCountry": "IN"}
ORGANIZATION = {
    "@type": "Organization", "@id": ORG_ID, "name": "Wanton Group", "url": BASE_URL,
    "logo": BASE_URL + "assets/img/wanton_shield.png", "image": BASE_URL + "assets/og/index.jpg",
    "description": "Family-run Mumbai business founded in 1969 with Wanton House on Hill Road, Bandra, now spanning hospitality, FMCG (WHS Sauces) and lifestyle (Ajuni Luxe).",
    "foundingDate": "1969", "foundingLocation": "Bandra West, Mumbai",
    "founder": {"@type": "Person", "name": "Sardar Darshan Singh Chawla"},
    "address": ADDR_GROUP, "email": "info@wantongroup.com", "telephone": "+91-98679-39177",
    "contactPoint": [
        {"@type": "ContactPoint", "contactType": "customer service", "telephone": "+91-98679-39177", "email": "info@wantongroup.com", "areaServed": "IN", "availableLanguage": ["en", "hi"]},
        {"@type": "ContactPoint", "contactType": "sales", "name": "Ajuni Luxe", "telephone": "+91-93212-15812", "areaServed": "IN"},
    ],
    "brand": [{"@type": "Brand", "name": "Wanton House"}, {"@type": "Brand", "name": "WHS Sauces"}, {"@type": "Brand", "name": "Ajuni Luxe"}],
    "sameAs": ["https://www.instagram.com/wantonhouseofficial/", "https://www.instagram.com/ajuniluxe/"],
}
RESTAURANT = {
    "@type": "Restaurant", "@id": BASE_URL + "hospitality.html#wanton-house", "name": "Wanton House",
    "url": BASE_URL + "hospitality.html#restaurants", "image": BASE_URL + "assets/img/ext1_web.jpg",
    "description": "Heritage Indian-Chinese restaurant on Hill Road, Bandra West, founded in 1969 by Sardar Darshan Singh Chawla.",
    "servesCuisine": ["Indian Chinese", "Chinese"], "foundingDate": "1969",
    "address": {"@type": "PostalAddress", "streetAddress": "Shop No. 4, Shams Palace, 98 Hill Road, Bandra West",
                "addressLocality": "Mumbai", "addressRegion": "Maharashtra", "postalCode": "400050", "addressCountry": "IN"},
    "telephone": "+91-98679-39177", "email": "bandra@wantongroup.com",
    "sameAs": ["https://www.instagram.com/wantonhouseofficial/", "https://restaurant-guru.in/Wanton-House-Mumbai-2"],
    "parentOrganization": {"@id": ORG_ID},
}
HOTEL = {
    "@type": "Hotel", "@id": BASE_URL + "hospitality.html#hotel-wanton-house", "name": "Hotel Wanton House",
    "url": BASE_URL + "hospitality.html#hotels",
    "address": {"@type": "PostalAddress", "streetAddress": "Plot No. 14, Sector 26/A, Palm Beach Road, Kopri Car Bazar Zone, Vashi",
                "addressLocality": "Navi Mumbai", "addressRegion": "Maharashtra", "postalCode": "400705", "addressCountry": "IN"},
    "telephone": "+91-98679-39177", "email": "hotelwantonhouse@wantongroup.com",
    "parentOrganization": {"@id": ORG_ID},
}
AJUNI = {
    "@type": "Store", "@id": BASE_URL + "ajuni-luxe.html#store", "name": "Ajuni Luxe", "url": BASE_URL + "ajuni-luxe.html",
    "image": BASE_URL + "assets/og/ajuni-luxe.jpg",
    "description": "Corporate gifting, home décor, luxury accessories and import collections, led by Bobby Chawla.",
    "address": {"@type": "PostalAddress", "streetAddress": "Shop No. 7, G-10, Palai Commercial Complex, Senapati Bapat Marg (Tulsi Pipe Road), Dadar West",
                "addressLocality": "Mumbai", "addressRegion": "Maharashtra", "postalCode": "400028", "addressCountry": "IN"},
    "telephone": "+91-93212-15812", "sameAs": ["https://www.instagram.com/ajuniluxe/"],
    "parentOrganization": {"@id": ORG_ID},
}
WHS_PRODUCT = {
    "@type": "Product", "name": "WHS Original Schezwan Sauce", "image": BASE_URL + "assets/img/whs_jar_clean.jpg",
    "description": "Schezwan sauce developed and served at Wanton House for over five decades, crafted in small batches. 500 g retail jar; 2.5 kg packs for professional kitchens.",
    "brand": {"@type": "Brand", "name": "WHS Sauces"}, "manufacturer": {"@id": ORG_ID},
}
WEBSITE = {"@type": "WebSite", "@id": BASE_URL + "#website", "url": BASE_URL, "name": "Wanton Group", "publisher": {"@id": ORG_ID}, "inLanguage": "en-IN"}

META = {}

PAGES = {
    "index": dict(
        title="Wanton Group | Family business since 1969 · Bandra, Mumbai",
        desc="Founded in 1969 with Wanton House on Hill Road, Bandra. Three generations on, Wanton Group runs hospitality, WHS Sauces and Ajuni Luxe in Mumbai.",
        schema=[ORGANIZATION, WEBSITE], rg=True, signoff=True, lcp=("ext1_web", "(max-width: 900px) 100vw, 46vw")),
    "about": dict(
        title="About Wanton Group | Three generations since 1969",
        desc="The story of Wanton Group: founded in 1969 by Sardar Darshan Singh Chawla with Wanton House, Hill Road, Bandra, and carried forward by three generations.",
        schema=[ORGANIZATION], crumb="About us"),
    "hospitality": dict(
        title="Wanton House, Bandra & Hotel Wanton House, Vashi | Wanton Group",
        desc="Wanton House, the Indian-Chinese restaurant on Hill Road, Bandra West since 1969, and Hotel Wanton House, Vashi. Reserve, stay or enquire about a franchise.",
        schema=[RESTAURANT, HOTEL], crumb="Hospitality", rg=True, lcp=("ext1_web", "(max-width: 900px) 100vw, 44vw"),
        scripts=['<script src="https://widgets.sociablekit.com/instagram-feed/widget.js" defer></script>']),
    "fmcg": dict(
        title="WHS Sauces by Wanton House | Original Schezwan Sauce",
        desc="WHS Sauces bottles the Schezwan sauce served at Wanton House for over five decades. 500 g jars for home and 2.5 kg packs for hotels, restaurants and caterers.",
        schema=[WHS_PRODUCT], crumb="FMCG · WHS Sauces", fonts="fonts-whs.css", lcp=("whs_jar_clean", "(max-width: 900px) 100vw, 46vw")),
    "ajuni-luxe": dict(
        title="Ajuni Luxe | Corporate gifting & luxury lifestyle, Dadar, Mumbai",
        desc="Ajuni Luxe by Bobby Chawla: corporate gifts, home décor, luxury accessories and import collections. Visit us in Dadar West, Mumbai, or enquire on WhatsApp.",
        schema=[AJUNI], crumb="Ajuni Luxe", fonts="fonts-ajuni.css", float_wa="ajuni",
        float_label="Chat with Ajuni Luxe on WhatsApp",
        scripts=['<script src="https://elfsightcdn.com/platform.js" async></script>']),
    "contact": dict(
        title="Contact Wanton Group | Bandra, Vashi & Dadar, Mumbai",
        desc="Contact Wanton Group, Wanton House, Hotel Wanton House and Ajuni Luxe. Addresses in Bandra West, Vashi and Dadar West, plus WhatsApp, phone and email.",
        schema=[ORGANIZATION], crumb="Contact", scripts=['<script src="assets/js/contact.js" defer></script>']),
    "404": dict(
        title="Page not found | Wanton Group", desc="This page could not be found.", noindex=True, og="index"),
}

# --------------------------------------------------------------------------


def wa_link(key):
    number, text = WHATSAPP[key]
    return f"https://wa.me/{number}?text={quote(text, safe='')}"


def map_link(key):
    return "https://www.google.com/maps/search/?api=1&query=" + quote_plus(MAPS[key])


def minify_css(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{};:,>])\s*", r"\1", css)
    return css.replace(";}", "}").strip()


def build_images():
    out = DIST / "assets" / "img"
    out.mkdir(parents=True, exist_ok=True)
    meta = {}
    for key, (filename, widths) in IMAGES.items():
        src = Image.open(SRC / "assets" / "img" / filename)
        is_png = filename.endswith(".png")
        w0, h0 = src.size
        sizes = []
        for w in widths:
            w = min(w, w0)
            im = src if w == w0 else src.resize((w, round(h0 * w / w0)), Image.LANCZOS)
            im.save(out / f"{key}-{w}.webp", "WEBP", quality=80 if is_png else 62, method=6)
            sizes.append(w)
        # Fallback for old browsers (and the copy used by search engines / schema)
        if is_png:
            src.save(out / filename, optimize=True)
        else:
            src.convert("RGB").save(out / filename, "JPEG", quality=80, optimize=True, progressive=True)
        meta[key] = dict(file=filename, w=w0, h=h0, widths=sorted(set(sizes)))
    return meta


def picture(meta, key, alt="", sizes="100vw", cls="", eager=""):
    m = meta[key]
    srcset = ", ".join(f"assets/img/{key}-{w}.webp {w}w" for w in m["widths"])
    attrs = [f'src="assets/img/{m["file"]}"', f'width="{m["w"]}"', f'height="{m["h"]}"', f'alt="{html.escape(alt)}"']
    if cls:
        attrs.insert(0, f'class="{cls}"')
    attrs.append('fetchpriority="high"' if eager == "eager" else 'loading="lazy"')
    attrs.append('decoding="async"')
    return (f'<picture><source type="image/webp" srcset="{srcset}" sizes="{sizes}">'
            f'<img {" ".join(attrs)}></picture>')


def render(text, meta, page, cfg):
    signoff = ('    <div class="footer-signoff">\n      <p>Bandra, since 1969. <em>Still family-run.</em></p>\n'
               '      <a href="contact.html" class="btn btn-primary">Start a conversation</a>\n    </div>\n') if cfg.get("signoff") else ""
    text = text.replace("{{signoff}}", signoff)
    text = text.replace("{{rg_badge}}", RG_BADGE)
    text = text.replace("{{year}}", str(datetime.date.today().year))
    text = text.replace("{{float_label}}", cfg.get("float_label", "Chat with Wanton Group on WhatsApp"))
    text = text.replace("{{wa:float}}", wa_link(cfg.get("float_wa", "general")))
    current = ' aria-current="page"'
    navlinks = "\n".join(
        f'      <a href="{href}"{current if href == page + ".html" else ""}>{label}</a>'
        for href, label in NAV)
    text = text.replace("{{navlinks}}", navlinks)
    text = re.sub(r"\{\{wa:(\w+)\}\}", lambda m: html.escape(wa_link(m.group(1))), text)
    text = re.sub(r"\{\{map:(\w+)\}\}", lambda m: html.escape(map_link(m.group(1))), text)
    text = re.sub(r"\{\{pic:([\w-]+)\|([^|}]*)\|([^|}]*)(?:\|([^|}]*))?(?:\|([^|}]*))?\}\}",
                  lambda m: picture(meta, m.group(1), m.group(2), m.group(3), m.group(4) or "", m.group(5) or ""), text)
    assert "{{" not in text, f"Unreplaced token in {page}: " + text[text.index("{{"):text.index("{{") + 40]
    return text


def head(page, cfg):
    url = BASE_URL if page == "index" else f"{BASE_URL}{page}.html"
    og = BASE_URL + f"assets/og/{cfg.get('og', page)}.jpg"
    t, d = html.escape(cfg["title"]), html.escape(cfg["desc"])
    graph = list(cfg.get("schema", []))
    if cfg.get("crumb"):
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE_URL},
            {"@type": "ListItem", "position": 2, "name": cfg["crumb"], "item": url}]})
    lines = [
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        f"<title>{t}</title>",
        f'<meta name="description" content="{d}">',
        '<meta name="robots" content="noindex">' if cfg.get("noindex") else f'<link rel="canonical" href="{url}">',
        '<meta name="theme-color" content="#FAF5EA">',
        '<meta property="og:type" content="website">',
        '<meta property="og:site_name" content="Wanton Group">',
        '<meta property="og:locale" content="en_IN">',
        f'<meta property="og:title" content="{t}">',
        f'<meta property="og:description" content="{d}">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:image" content="{og}">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{t}">',
        f'<meta name="twitter:description" content="{d}">',
        f'<meta name="twitter:image" content="{og}">',
        '<link rel="icon" href="favicon.ico" sizes="any">',
        '<link rel="icon" type="image/png" sizes="32x32" href="assets/icons/favicon-32.png">',
        '<link rel="apple-touch-icon" href="assets/icons/apple-touch-icon.png">',
        '<link rel="manifest" href="site.webmanifest">',
        '<link rel="preload" href="assets/fonts/fraunces-normal.woff2" as="font" type="font/woff2" crossorigin>',
        '<link rel="preload" href="assets/fonts/manrope-normal.woff2" as="font" type="font/woff2" crossorigin>',
        '<link rel="stylesheet" href="assets/css/site.css">',
    ]
    if cfg.get("lcp"):
        key, sizes = cfg["lcp"]
        srcset = ", ".join(f"assets/img/{key}-{w}.webp {w}w" for w in META[key]["widths"])
        lines.append(f'<link rel="preload" as="image" type="image/webp" imagesrcset="{srcset}" imagesizes="{sizes}" fetchpriority="high">')
    if cfg.get("fonts"):
        lines.append(f'<link rel="stylesheet" href="assets/css/{cfg["fonts"]}">')
    if cfg.get("rg"):
        lines.append(RG_CSS)
    lines.append("<script>document.documentElement.classList.add('js')</script>")
    if graph:
        data = {"@context": "https://schema.org", "@graph": graph}
        lines.append('<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "</script>")
    return "\n".join(lines)


def build_icons():
    out = DIST / "assets" / "icons"
    out.mkdir(parents=True, exist_ok=True)
    shield = Image.open(SRC / "assets" / "img" / "wanton_shield.png").convert("RGBA")

    def on_square(size, pad, bg):
        canvas = Image.new("RGBA", (size, size), bg)
        inner = size - 2 * pad
        s = shield.copy()
        s.thumbnail((inner, inner), Image.LANCZOS)
        canvas.alpha_composite(s, ((size - s.width) // 2, (size - s.height) // 2))
        return canvas

    on_square(32, 1, (0, 0, 0, 0)).save(out / "favicon-32.png")
    on_square(180, 18, (250, 245, 234, 255)).convert("RGB").save(out / "apple-touch-icon.png")
    on_square(192, 24, (250, 245, 234, 255)).save(out / "icon-192.png")
    on_square(512, 64, (250, 245, 234, 255)).save(out / "icon-512.png")
    on_square(48, 1, (0, 0, 0, 0)).save(DIST / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    (DIST / "site.webmanifest").write_text(json.dumps({
        "name": "Wanton Group", "short_name": "Wanton Group", "start_url": "/", "display": "browser",
        "background_color": "#FAF5EA", "theme_color": "#FAF5EA",
        "icons": [{"src": "assets/icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "assets/icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}],
    }, indent=2))


def build_static_files():
    pages = [p for p in PAGES if not PAGES[p].get("noindex")]
    urls = "\n".join(
        f"  <url><loc>{BASE_URL if p == 'index' else BASE_URL + p + '.html'}</loc><lastmod>{TODAY}</lastmod></url>"
        for p in pages)
    (DIST / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')
    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}sitemap.xml\n")
    shutil.copy(SRC / "htaccess.txt", DIST / ".htaccess")


def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    (DIST / "assets" / "css").mkdir(parents=True)
    shutil.copytree(SRC / "assets" / "fonts", DIST / "assets" / "fonts")
    shutil.copytree(SRC / "assets" / "js", DIST / "assets" / "js")
    shutil.copytree(SRC / "assets" / "og", DIST / "assets" / "og")

    css_dir = SRC / "assets" / "css"
    site_css = (css_dir / "fonts-base.css").read_text() + (css_dir / "styles.css").read_text()
    (DIST / "assets" / "css" / "site.css").write_text(minify_css(site_css))
    for extra in ("fonts-whs.css", "fonts-ajuni.css"):
        (DIST / "assets" / "css" / extra).write_text(minify_css((css_dir / extra).read_text()))

    meta = build_images()
    META.update(meta)
    build_icons()

    header = (SRC / "partials" / "header.html").read_text()
    footer = (SRC / "partials" / "footer.html").read_text()
    for page, cfg in PAGES.items():
        body = (SRC / "pages" / f"{page}.html").read_text()
        scripts = "\n".join(['<script src="assets/js/main.js" defer></script>'] + cfg.get("scripts", []))
        doc = (f'<!DOCTYPE html>\n<html lang="en-IN">\n<head>\n{head(page, cfg)}\n</head>\n<body class="page-{page}">\n'
               f"{header}\n<main id=\"main\">\n{body}\n</main>\n\n{footer}\n{scripts}\n</body>\n</html>\n")
        (DIST / f"{page}.html").write_text(render(doc, meta, page, cfg))

    build_static_files()
    total = sum(f.stat().st_size for f in DIST.rglob("*") if f.is_file())
    print(f"Built {len(PAGES)} pages into {DIST} ({total / 1024:.0f} KB total)")


if __name__ == "__main__":
    main()
