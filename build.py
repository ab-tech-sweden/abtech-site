#!/usr/bin/env python3
"""Generate the static AB-Tech site into this directory. Safe to re-run."""
from pathlib import Path
import json, re, html as htmlmod

ROOT = Path(__file__).resolve().parent
NEWS_JSON = ROOT / "data" / "news_posts_html.json"
NEWS_JSON_LEGACY = Path("/tmp/abtech-crawl/news_posts_html.json")

NAV = [
    ("Home", "index.html", "home"),
    ("Products", "products/", "products"),
    ("About Us", "about-us/", "about-us"),
    ("News", "news/", "news"),
    ("Contact", "contact/", "contact"),
    ("Family", "bladelius/", "bladelius"),
    ("Reviews", "reviews/", "reviews"),
]

FB = "https://www.facebook.com/Ab_tech_sweden-111388294812984"
FB_ABOUT = "https://www.facebook.com/profile.php?id=100078655786246"
IG = "https://www.instagram.com/ab_tech_sweden/"

ICON_FB = '''<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 8h3V4h-3c-2.8 0-5 2.2-5 5v2H6v4h3v8h4v-8h3l1-4h-4V9c0-.6.4-1 1-1z"/></svg>'''
ICON_IG = '''<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 3h10a4 4 0 0 1 4 4v10a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4V7a4 4 0 0 1 4-4zm10 2H7a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2zm-5 3.2A3.8 3.8 0 1 1 8.2 12 3.8 3.8 0 0 1 12 8.2zm0 1.6A2.2 2.2 0 1 0 14.2 12 2.2 2.2 0 0 0 12 9.8zM17.2 6.6a.9.9 0 1 1-.9.9.9.9 0 0 1 .9-.9z"/></svg>'''
ICON_MENU = '''<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 6h18v2H3V6zm0 5h18v2H3v-2zm0 5h18v2H3v-2z"/></svg>'''

ASSET_V = "8"
SITE = "https://ab-tech.se"


def prefix(depth: int) -> str:
    return "" if depth == 0 else "../" * depth


def href(depth: int, target: str) -> str:
    """target is 'index.html' or 'products/' etc."""
    p = prefix(depth)
    if target == "index.html":
        return p + "index.html" if p else "index.html"
    return p + target


def header(depth: int, current: str) -> str:
    p = prefix(depth)
    items = []
    for label, target, key in NAV:
        url = href(depth, target)
        cur = ' aria-current="page"' if key == current else ""
        items.append(f'          <li><a href="{url}"{cur}>{label}</a></li>')
    nav = "\n".join(items)
    return f'''  <header class="site-header">
    <div class="inner">
      <a class="logo" href="{href(depth, "index.html")}" aria-label="AB-Tech home">
        <img src="{p}images/brand/logo.png?v={ASSET_V}" width="222" height="97" alt="AB — Made in Sweden">
      </a>
      <button class="nav-toggle" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="site-nav">{ICON_MENU}</button>
      <nav class="site-nav" id="site-nav">
        <ul>
{nav}
        </ul>
      </nav>
    </div>
  </header>'''


def footer(depth: int) -> str:
    p = prefix(depth)
    return f'''  <footer class="site-footer">
    <div class="inner">
      <div>AB-Tech by Alexander Bladelius</div>
      <div class="footer-social">
        <a href="{FB}" target="_blank" rel="noopener" title="Facebook" aria-label="Facebook">{ICON_FB}</a>
        <a href="{IG}" target="_blank" rel="noopener" title="Instagram" aria-label="Instagram">{ICON_IG}</a>
      </div>
    </div>
  </footer>
  <script src="{p}js/main.js?v={ASSET_V}"></script>'''


def jsonld_tag(data) -> str:
    if not data:
        return ""
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    return f'  <script type="application/ld+json">\n{payload}\n  </script>\n'


def org_jsonld() -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "Alexander Bladelius Technologies AB",
        "brand": "AB Tech",
        "url": f"{SITE}/",
        "logo": f"{SITE}/images/brand/logo.png",
    }


def product_jsonld(name: str, description: str, image_file: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": name,
        "description": description,
        "brand": {"@type": "Brand", "name": "AB Tech"},
        "image": f"{SITE}/images/products/{image_file}",
    }


def page(depth: int, current: str, title: str, body: str, extra_head: str = "", description: str = "", json_ld=None, early_head: str = "") -> str:
    p = prefix(depth)
    desc = description or "High-end audio and tech products from Alexander Bladelius Technologies AB. Designed and made in Sweden."
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
{early_head}  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{htmlmod.escape(title)}</title>
  <meta name="description" content="{htmlmod.escape(desc)}">
  <link rel="icon" href="{p}favicon.png" type="image/png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,300;0,400;0,700;1,300;1,400&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{p}css/style.css?v={ASSET_V}">
{extra_head}{jsonld_tag(json_ld)}</head>
<body>
{header(depth, current)}
{body}
{footer(depth)}
</body>
</html>
'''


def write(rel: str, text: str):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print("wrote", rel, path.stat().st_size)


# ---------- pages ----------

def _plain(html: str, limit: int = 160) -> str:
    text = news_text_only(rewrite_news_body(html)) if html else ""
    text = re.sub(r"<[^>]+>", " ", text)
    text = htmlmod.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s+([.,;:!?])", r"\1", text)
    if len(text) > limit:
        text = text[:limit].rsplit(" ", 1)[0] + "…"
    return text


def _news_img(url: str, depth: int = 0) -> str:
    src = map_news_src(url or "")
    if depth == 0 and src.startswith("../"):
        src = src[3:]
    return src


def home():
    # Latest news from the crawl, mixed with a couple of press reviews.
    posts = load_news_posts()
    slides = []
    review_inserts = {
        1: (
            "Review",
            "images/reviews/klar-highfidelity.jpg",
            "Review of KLAR by High Fidelity",
            "https://highfidelity.pl/@main-1620&lang=en",
            "A press review of the KLAR USB isolator.",
        ),
        4: (
            "Review",
            "images/reviews/still-soundrebels.jpg",
            "Review of STILL by Soundrebels",
            "https://soundrebels.com/ab-tech-still-2/",
            "A press review of the STILL Ethernet isolator.",
        ),
    }
    news_used = 0
    total = 6
    for i in range(total):
        if i in review_inserts:
            kind, img, title, url, excerpt = review_inserts[i]
            slides.append((kind, img, title, "", url, excerpt, True))
        elif news_used < len(posts):
            post = posts[news_used]
            news_used += 1
            images = post.get("images") or []
            img = _news_img(images[0]["src"]) if images else ""
            excerpt = _plain(post.get("body_html") or "")
            if re.match(r"https?://", excerpt):
                excerpt = ""
            slides.append(("News", img, post["title"], post.get("date") or "", "news/", excerpt, False))

    slide_html = []
    for idx, (kind, img, title, date, url, excerpt, external) in enumerate(slides):
        rel = ' target="_blank" rel="noopener"' if external else ""
        img_html = f'<img src="{htmlmod.escape(img)}" alt="{htmlmod.escape(title)}">' if img else ""
        meta = f"{kind}" + (f" · {htmlmod.escape(date)}" if date else "")
        active = " is-active" if idx == 0 else ""
        excerpt_html = f"<p>{htmlmod.escape(excerpt)}</p>" if excerpt else ""
        slide_html.append(
            f'        <article class="slide{active}">\n'
            f'          <a href="{htmlmod.escape(url)}"{rel}>\n'
            f'            <div class="slide-image">{img_html}</div>\n'
            f'            <div class="slide-body">\n'
            f'              <p class="kicker">{meta}</p>\n'
            f'              <h3>{htmlmod.escape(title)}</h3>\n'
            f'              {excerpt_html}\n'
            f'            </div>\n'
            f'          </a>\n'
            f'        </article>'
        )

    extra = '  <style>.hero { background-image: url("images/hero/home.jpg"); }</style>\n'
    body = (
        '  <main>\n'
        '    <section class="hero" aria-label="AB-Tech"></section>\n'
        '\n'
        '    <section class="home-latest">\n'
        '      <div class="wrap">\n'
        '        <div class="section-head">\n'
        '          <h2>Latest</h2>\n'
        '          <a class="text-link" href="news/">All news</a>\n'
        '        </div>\n'
        '        <div class="slider" data-slider data-interval="7000" aria-label="Latest news and reviews">\n'
        '          <div class="slider-viewport">\n'
        + "\n".join(slide_html) + "\n"
        '          </div>\n'
        '          <div class="slider-controls">\n'
        '            <button type="button" class="slider-prev" aria-label="Previous"></button>\n'
        '            <div class="slider-dots" role="tablist" aria-label="Choose slide"></div>\n'
        '            <button type="button" class="slider-next" aria-label="Next"></button>\n'
        '          </div>\n'
        '        </div>\n'
        '      </div>\n'
        '    </section>\n'
        '\n'
        '    <section class="home-follow">\n'
        '      <div class="wrap">\n'
        '        <h2>Follow</h2>\n'
        '        <p>Updates from the workshop and the road, on Instagram and Facebook.</p>\n'
        '        <div class="follow-links">\n'
        f'          <a href="{IG}" target="_blank" rel="noopener">Instagram</a>\n'
        f'          <a href="{FB}" target="_blank" rel="noopener">Facebook</a>\n'
        '        </div>\n'
        '      </div>\n'
        '    </section>\n'
        '  </main>'
    )
    write("index.html", page(0, "home", "AB-Tech – Home", body, extra_head=extra,
                             description="High-end audio isolators, cables and power products from Alexander Bladelius Technologies AB. Designed and made in Sweden.",
                             json_ld=org_jsonld()))


def products():
    body = '''  <main class="page">
    <div class="wrap">
      <header class="page-header">
        <h1>Products</h1>
      </header>

      <section class="product-group">
        <h2>Digital Isolators</h2>
        <div class="product-grid">
          <a class="product-card" href="../still/">
            <div class="thumb"><img src="../images/products/still.jpg" alt="STILL Ethernet Isolator"></div>
            <div class="label">STILL — Ethernet Isolator</div>
          </a>
          <a class="product-card" href="../ren/">
            <div class="thumb"><img src="../images/products/ren-alt.jpg" alt="REN Ethernet Isolator"></div>
            <div class="label">REN — Ethernet Isolator</div>
          </a>
          <a class="product-card" href="../klar/">
            <div class="thumb"><img src="../images/products/klar.jpg" alt="KLAR USB Isolator"></div>
            <div class="label">KLAR — USB Isolator</div>
          </a>
        </div>
      </section>

      <section class="product-group">
        <h2>Power Products</h2>
        <div class="product-grid">
          <a class="product-card" href="../frid/">
            <div class="thumb"><img src="../images/products/frid.jpg" alt="FRID Power Cleaner"></div>
            <div class="label">FRID — Power Cleaner</div>
          </a>
        </div>
      </section>

      <section class="product-group">
        <h2>Digital Cables</h2>
        <div class="product-grid">
          <a class="product-card" href="../tamp/">
            <div class="thumb"><img src="../images/products/tamp.jpg" alt="TAMP Ethernet Cable"></div>
            <div class="label">TAMP — Ethernet Cable</div>
          </a>
        </div>
      </section>

      <section class="product-group sister-mini">
        <h2>The Bladelius family</h2>
        <div class="sister-mini-grid">
          <article class="sister-mini-card">
            <a class="thumb" href="https://www.bladelius.com/" target="_blank" rel="noopener">
              <img src="../images/gallery/bladelius/1.webp" alt="Bladelius amplifier">
            </a>
            <div class="sister-mini-body">
              <h3>Bladelius</h3>
              <p>High-performance audio electronics, designed in Sweden.</p>
              <a class="text-link" href="https://www.bladelius.com/" target="_blank" rel="noopener">Visit website</a>
            </div>
          </article>
          <article class="sister-mini-card">
            <a class="thumb" href="https://www.norseaudio.se/" target="_blank" rel="noopener">
              <img src="../images/pages/norse.jpg" alt="Norse Audio component">
            </a>
            <div class="sister-mini-body">
              <h3>Norse Audio</h3>
              <p>A modular audio system, powered by Bladelius.</p>
              <a class="text-link" href="https://www.norseaudio.se/" target="_blank" rel="noopener">Visit website</a>
            </div>
          </article>
        </div>
        <p class="sister-more"><a class="text-link" href="../bladelius/">More about the family</a></p>
      </section>
    </div>
  </main>'''
    write("products/index.html", page(1, "products", "AB-Tech – Products", body))


def product_page(slug, title, heading, intro_html, specs, hero, hero_alt, gallery_dir, n_gallery, current):
    specs_lis = "\n".join(f"          <li>{s}</li>" for s in specs)
    g = ""
    if n_gallery:
        items = []
        for i in range(1, n_gallery + 1):
            src = f"../images/gallery/{gallery_dir}/{i}.webp"
            items.append(
                f'        <a href="{src}" data-lightbox><img src="{src}" alt="{htmlmod.escape(heading)} — photo {i}"></a>'
            )
        g = f'''
      <div class="gallery">
{chr(10).join(items)}
      </div>'''
    body = f'''  <main class="page">
    <div class="wrap">
      <div class="split">
        <div class="prose">
          <h1>{heading}</h1>
{intro_html}
        </div>
        <div class="product-hero">
          <img src="../images/products/{hero}" alt="{htmlmod.escape(hero_alt)}">
          <div class="specs">
            <h2>Specifications</h2>
            <ul>
{specs_lis}
            </ul>
          </div>
        </div>
      </div>{g}
    </div>
  </main>'''
    desc = f"{heading}. High-end audio from AB-Tech, designed and made in Sweden."
    write(f"{slug}/index.html", page(1, current, title, body, description=desc,
                                     json_ld=product_jsonld(heading, desc, hero)))


def still():
    intro = '''          <p>STILL is our next-generation Ethernet isolator designed for precision audio streaming applications. Evolving from the experience we gained from designing the REN Ethernet Isolator with integrated cables, STILL features a more advanced isolator with connector-only architecture, enabling users to integrate their preferred high-end Ethernet cables for optimized system compatibility and performance.</p>
          <p><strong>Core Functionality</strong><br>
          STILL delivers full multi-stepped galvanic isolation for both signal and ground paths, and high-frequency filter to eliminate noise from upstream network sources. This removes jitter, electromagnetic interference (EMI), radio-frequency interference (RFI), and ground-loop artifacts, ensuring a clean data stream to downstream components such as DACs and network streamers. Onboard toggle switches provide selectable configurations for filtering profiles and ground lift options, allowing precise adjustment to match specific system requirements and environmental conditions. One switch allows the user to select the shield reference, choosing either the input or output as the reference point for the shield connection, enabling optimization of the grounding configuration to minimize noise and interference. The other switch enables selection between loose isolation or full isolation, controlling the degree of signal separation to balance system compatibility and maximum noise reduction, tailoring the isolator’s performance to the specific needs of the audio chain.</p>
          <p><strong>Construction and Materials</strong><br>
          Milled from a single block of non-magnetic, high-grade aluminum, the unibody chassis provides robust shielding against external EMI/RFI while facilitating efficient thermal management. The internal assembly is suspended in a proprietary viscoelastic damping material to suppress mechanical vibrations and microphonics, reducing resonance-induced noise in the audio chain.</p>
          <p><strong>Connectivity</strong><br>
          Input and output ports utilize high-quality custom RJ45 connectors, optimized for reliable integration with shielded Ethernet cables.</p>
          <p>STILL offers superior isolation depth resulting in measurable improvements such as significantly reduced noise floor, enhanced signal-to-noise ratio, and greater dynamic range in high-resolution audio playback. With user-configurable controls we allow the listener to get the most out of it in their particular system. Ideal for audiophiles seeking reference-level network purity without compromise.</p>'''
    specs = [
        "High level multi-stepped galvanic isolation",
        "Switch 1: Select shield reference (input or output), allowing users to define the grounding reference point to optimize noise suppression and system stability",
        "Switch 2: Select isolation level (loose or full), enabling users to adjust the degree of signal separation for tailored performance in diverse audio environments",
        "High quality RJ45 Connectors",
        "Dimensions: 149mm (W) × 42mm (H) × 93mm (D)",
    ]
    product_page("still", "AB-Tech – STILL", "STILL — Ethernet Isolator", intro, specs,
                 "still.jpg", "STILL Ethernet Isolator", "still", 3, "products")


def ren():
    intro = '''          <p>REN which in Swedish means clean or pure is our brand new accessory for high end audio streaming via ethernet.</p>
          <p>With this isolator, besides from acting as a filter, both signal and ground are completely galvanically isolated, which means all noise is removed and through comes only music.</p>
          <p>In the aluminum body milled out of two solid pieces of non magnetic high grade aluminum which is specially designed to keep out any interferance, the isolator is molded in a vibration dampening material.</p>
          <p>The connectors used are specially design for high end ethernet cables and has a die-cast robust zinz housing and high quality latch-protectors.</p>
          <p>The cable it self is a high grade cat 8 ethernet cable that is specially designed for noise cancellation most commonly used for medical and military purposes, where noise isolation is just as important as in audio. It feature an aluminum PETP foil around each balanced twisted pair of copper cable. All four pairs are then housed with a special thermoplastic material, and finally wrapped in a custom noise reducing sleeve normally used in aerospace, that also provides a luxurios finish for the listeners eyes. But as you might imagine, the real beauty comes from the sound that it provides.</p>'''
    specs = [
        "CAT 8.1 Cable &amp; Connectors",
        "Galvanic Isolation",
        "RJ45 connectors",
        "Different lenghts are available",
    ]
    product_page("ren", "AB-Tech – REN", "REN — Ethernet Isolator", intro, specs,
                 "ren.jpg", "REN Ethernet Isolator", "ren", 6, "products")


def klar():
    intro = '''          <p>KLAR which in Swedish means clear is our brand new accessory for high end audio streaming via USB.</p>
          <p>Klar is an isolating cable for high-speed USB 2.0. This isolator, besides from its filter functions, regenerates the signal and completely galvanically isolates signal, power and ground which means all noise is removed and through comes only music.</p>
          <p>In the aluminum body milled out of two solid pieces of non-magnetic high-grade aluminum, which is specially designed to keep out any interference, the isolator is molded in a vibration dampening material.</p>
          <p>We use high-quality gold-plated connectors for a good and secure connection.</p>
          <p>The cable is made with high gauge tinned copper wire, one twisted pair for signal and two separate wires for power. The shielding is done with both aluminum mylar and tinned copper braid. This is then housed with a special thermoplastic material, and finally wrapped in a custom noise reducing sleeve normally used in aerospace, that also provides a luxurious finish for the listeners eyes. But as you might imagine, the real beauty comes from the sound that it provides.</p>'''
    specs = [
        "High Speed USB 2.0 (480Mbps)",
        "Complete galvanic isolation",
        "Regenerated signal",
        "Gold plated connectors (A-B)",
        "Max load 100mA",
        "Different lenghts are available",
    ]
    product_page("klar", "AB-Tech – KLAR", "KLAR — USB Isolator", intro, specs,
                 "klar.jpg", "KLAR USB Isolator", "klar", 2, "products")


def frid():
    intro = '''          <p>FRID which in Swedish means peace and tranquility is our brand new power cleaner that removes noise on the mains in order to provide good and clean power to the system.</p>
          <p>This power cleaner is designed to draw noise from the power line and eliminating it without interfering in the amount of power available to the system.</p>
          <p>In comparison to many other power filters, this product is designed to not interfere with the amount of power available to the equipment. This means that the amount of power available will never be limited, not even to the most powerful power amplifiers. This is accomplished by not having the power flow through Frid. It is only active when there is noise that needs to be removed and it only affects the noise and not the power itself. The noise is then removed with a complex filter design resulting in a darker and wider soundstage with more details and clarity.</p>
          <p>The gold-plated connectors are of very high quality to ensure a good and stable connection and the aluminum body is milled out of two solid pieces of non-magnetic high grade aluminum.</p>
          <p>If one Frid is used it should be placed as close as possible to the rest of the system (preferably in the same power distributor). If multiple Frid are used they can also be placed near a known noise source (refrigerator etc.).</p>'''
    specs = [
        "110–250V",
        "50–60Hz",
        "Gold plated connectors",
        "Different power plugs available",
    ]
    product_page("frid", "AB-Tech – FRID", "FRID — Power cleaner", intro, specs,
                 "frid.jpg", "FRID Power Cleaner", "frid", 0, "products")


def tamp():
    intro = '''          <p>Our new Cat8 Ethernet cable is built for high-end audio streaming where signal integrity is essential.</p>
          <p>It employs a premium CAT 8.1 construction with advanced shielding: aluminum PETP foil around each twisted copper pair, reinforced by a specialized thermoplastic layer and an outer aerospace-grade noise-suppressing sleeve. This design delivers outstanding interference rejection while maintaining excellent high-frequency performance.</p>
          <p>Fitted with robust die-cast zinc RJ45 connectors and secure latch protection, the cable ensures stable, low-loss connections in every situation.</p>
          <p>This cable is the perfect match for our flagship Ethernet isolator <a href="../still/">STILL</a>, creating a complete high-end network solution when used together. Simple yet sonically refined, it serves as an excellent complement to our more advanced products.</p>'''
    specs = [
        "CAT 8.1 Cable &amp; Connectors",
        "RJ45 connectors",
        "Available in 1m and 2m lengths",
    ]
    product_page("tamp", "AB-Tech – TAMP", "TAMP — Ethernet Cable", intro, specs,
                 "tamp.jpg", "TAMP Ethernet Cable", "tamp", 0, "products")


def about():
    body = f'''  <main class="page">
    <div class="wrap">
      <div class="split">
        <div class="prose">
          <h1>About Us</h1>
          <p>We are specialized in the design and production of high end audio/tech products and accesories.</p>
          <p>Being raised in a house where there were amplifiers, transformers, pcb:s etc where ever you looked and music playing from somewhere 24/7 I didn't have much choice but to listen to a lot of music. As far as I can remember I have been comparing components, designs and big and small changes that my father made to determine which was the best and what should go in to production. When I was younger I was mosly interested in listening and also playing music myself, but as I grew older I started to help out in the factory and lab, learning a lot from my father. For the last couple of years I have also been more involved in the development of new products, making all mechanical drawings and more.</p>
          <p>From all this I have learned a lot of what makes a difference to the sound and music and with this new brand I have taken my own thoughts and designs and made products that I feel can make a difference for peoples listening experience and I am trying to complement and find solutions not many others have thought about.</p>
          <p>I hope we will contribute to your listening experience and to the audio world.</p>
          <p>Enjoy the music.<br>//Alexander Bladelius</p>

          <h2 style="margin-top:2.2em;text-transform:none;letter-spacing:-0.01em;color:#fff;font-weight:700;font-size:1.35rem;">Social Media</h2>
          <p>Follow ab_tech_sweden on <a href="{FB_ABOUT}" target="_blank" rel="noopener">Facebook</a> &amp; <a href="{IG}" target="_blank" rel="noopener">Instagram</a> to get frequent updates on what is going on at AB-Tech.</p>
        </div>
        <div>
          <img src="../images/pages/about.jpg" alt="AB-Tech product">
        </div>
      </div>
    </div>
  </main>'''
    write("about-us/index.html", page(1, "about-us", "AB-Tech – About Us", body,
          description="Alexander Bladelius Technologies AB designs and produces high-end audio and tech products in Sweden."))


def contact():
    body = '''  <main class="page">
    <div class="wrap">
      <div class="split reverse">
        <div>
          <img src="../images/pages/contact.jpg" alt="AB-Tech product">
        </div>
        <div>
          <h1>Contact form</h1>
          <p class="lede">You can contact us by filling out this form:</p>

          <form class="form" data-contact action="https://api.web3forms.com/submit" method="POST">
            <input type="hidden" name="access_key" value="e2c736a1-55c9-42b6-8eb7-ce3ac157828b">
            <input type="hidden" name="from_name" value="AB-Tech website">
            <input type="hidden" name="subject" value="Contact form — ab-tech.se">
            <div class="hp" aria-hidden="true">
              <label>Leave this empty <input type="checkbox" name="botcheck" tabindex="-1" autocomplete="off"></label>
            </div>

            <div>
              <label for="name">Name <span class="req">*</span></label>
              <input id="name" name="name" type="text" required autocomplete="name">
            </div>
            <div>
              <label for="email">E-mail <span class="req">*</span></label>
              <input id="email" name="email" type="email" required autocomplete="email">
            </div>
            <div>
              <label for="phone">Phone</label>
              <input id="phone" name="phone" type="tel" autocomplete="tel">
            </div>
            <div>
              <label for="message">Message <span class="req">*</span></label>
              <textarea id="message" name="message" required></textarea>
            </div>
            <button class="btn" type="submit">Submit</button>
            <div class="form-status" role="status" aria-live="polite"></div>
          </form>
        </div>
      </div>
    </div>
  </main>'''
    write("contact/index.html", page(1, "contact", "AB-Tech – Contact", body,
          description="Contact Alexander Bladelius Technologies AB."))


def bladelius():
    body = f"""  <main class="page">
    <div class="wrap">
      <header class="page-header">
        <h1>The Bladelius family</h1>
        <p class="lede">AB Tech, Bladelius and Norse Audio are part of the Bladelius family of Swedish audio brands.</p>
      </header>

      <div class="sister-grid">
        <article class="sister-card">
          <div class="sister-photo">
            <img src="../images/gallery/bladelius/1.webp" alt="Bladelius amplifier">
          </div>
          <div class="sister-body">
            <img class="sister-wordmark" src="../images/brand/bladelius-wordmark.png" alt="Bladelius">
            <p>Bladelius designs high-performance audio electronics, from amplifiers and preamplifiers to related components, for listeners around the world.</p>
            <a class="btn" href="https://www.bladelius.com/" target="_blank" rel="noopener">Visit website</a>
          </div>
        </article>

        <article class="sister-card">
          <div class="sister-photo">
            <img src="../images/pages/norse.jpg" alt="Norse Audio component">
          </div>
          <div class="sister-body">
            <img class="sister-wordmark norse" src="../images/brand/norse-logo.png" alt="Norse Audio">
            <p>Norse Audio, a sub-brand of Bladelius, makes a modular high-fidelity system — the X1 power amplifier, X2 pre-amplifier and X5 power supply — built for flexibility and a clean, stable sound.</p>
            <a class="btn" href="https://www.norseaudio.se/" target="_blank" rel="noopener">Visit website</a>
          </div>
        </article>
      </div>
    </div>
  </main>"""
    write("bladelius/index.html", page(1, "bladelius", "AB-Tech – The Bladelius family", body,
          description="The Bladelius family: AB Tech, Bladelius and Norse Audio."))


def reviews():
    cards = [
        ("klar-highfidelity.jpg", "Review of KLAR by High Fidelity", "https://highfidelity.pl/@main-1620&lang=en"),
        ("klar-soundrebels.jpg", "Review of KLAR by Soundrebels", "https://soundrebels.com/ab-tech-klar-2/"),
        ("still-soundrebels.jpg", "Review of STILL by Soundrebels", "https://soundrebels.com/ab-tech-still-2/"),
        ("still-highfidelity.jpg", "Review of STILL by High Fidelity", "https://highfidelity.pl/@main-1570&lang=en"),
        ("klar-analoguefellowship.webp", "Review of KLAR by Analouge Fellowship", "https://analoguefellowship.com/2025/03/15/ab-tech-klar-usb-2-0-cable-the-full-review/"),
        ("ren-soundrebels.jpg", "Review of REN by Soundrebels", "https://soundrebels.com/ab-tech-ren-english-ver/"),
        ("ren-hifiknights.jpg", "Review of REN by HIFI Knights", "https://hifiknights.com/reviews/accessories/a-b-tech-ren-ethernet-isolator/"),
    ]
    items = []
    for img, title, url in cards:
        items.append(f'''          <a class="review-card" href="{htmlmod.escape(url)}" target="_blank" rel="noopener">
            <div class="thumb"><img src="../images/reviews/{img}" alt="{htmlmod.escape(title)}"></div>
            <div class="meta">
              <h2>{htmlmod.escape(title)}</h2>
              <p>{htmlmod.escape(url)}</p>
            </div>
          </a>''')
    body = f'''  <main class="page">
    <div class="wrap">
      <header class="page-header">
        <h1>Reviews</h1>
      </header>
      <div class="review-grid">
{chr(10).join(items)}
      </div>
    </div>
  </main>'''
    write("reviews/index.html", page(1, "reviews", "AB-Tech – Reviews", body,
          description="Press reviews of AB-Tech products."))


def map_news_src(url: str) -> str:
    if not url:
        return url
    if "images/news/" in url:
        name = url.split("images/news/")[-1].split("?")[0]
        return "../images/news/" + name
    name = url.split("/files/1023973/")[-1]
    name = name.replace("medium/", "").split("?")[0]
    # jpeg was often saved as .jpg
    candidate_jpg = name[:-5] + ".jpg" if name.lower().endswith(".jpeg") else None
    news_dir = ROOT / "images" / "news"
    if candidate_jpg and (news_dir / candidate_jpg).exists() and not (news_dir / name).exists():
        name = candidate_jpg
    return "../images/news/" + name


def rewrite_news_body(body: str) -> str:
    def src_sub(m):
        return 'src="' + map_news_src(m.group(1)) + '"'
    body = re.sub(r'src="(https://site-1023973\.mozfiles\.com/[^"]+)"', src_sub, body)
    # internal site links
    body = body.replace('href="/still/"', 'href="../still/"')
    body = body.replace('href="/frid/"', 'href="../frid/"')
    body = body.replace('href="/klar/"', 'href="../klar/"')
    body = body.replace('href="/ren/"', 'href="../ren/"')
    body = body.replace('href="/tamp/"', 'href="../tamp/"')
    # unwrap leftover empty spans somewhat
    body = re.sub(r'<span>(.*?)</span>', r'\1', body)
    body = body.replace("<div>", "").replace("</div>", "")
    # make bare analoguefellowship URL a link if still plain — leave as original
    return body


def extract_thumb(body_html: str):
    m = re.search(r'<img[^>]+src="([^"]+)"', body_html)
    href_m = re.search(r'<a href="([^"]+)"[^>]*>\s*<img', body_html)
    if not m:
        return None, None
    return m.group(1), (href_m.group(1) if href_m else None)


def news_text_only(body_html: str) -> str:
    # remove images (they'll sit in the thumb column) but keep the surrounding links' text if any
    cleaned = re.sub(r'<p>\s*<a[^>]*>\s*<img[^>]*>\s*</a>\s*(?:<br\s*/?>)?\s*</p>', '', body_html)
    cleaned = re.sub(r'<p>\s*<img[^>]*>\s*(?:<br\s*/?>)?\s*</p>', '', cleaned)
    cleaned = re.sub(r'<a[^>]*>\s*<img[^>]*>\s*</a>', '', cleaned)
    cleaned = re.sub(r'<img[^>]*>', '', cleaned)
    cleaned = re.sub(r'<br\s*/?>', '', cleaned)
    cleaned = re.sub(r'<p>\s*</p>', '', cleaned)
    return cleaned.strip()


def recover_news_posts_from_html() -> list:
    """Rebuild crawl records from the last generated news page."""
    path = ROOT / "news" / "index.html"
    if not path.exists():
        return []
    html = path.read_text(encoding="utf-8")
    posts = []
    for m in re.finditer(r'<article class="news-item">(.*?)</article>', html, re.S):
        art = m.group(1)
        title_m = re.search(r'<h2>(.*?)</h2>', art, re.S)
        date_m = re.search(r'<time>(.*?)</time>', art)
        thumb_m = re.search(r'<div class="thumb">(.*?)</div>', art, re.S)
        body_m = re.search(r'<div class="body">(.*?)</div>', art, re.S)
        if not title_m or not date_m or not body_m:
            continue
        title = htmlmod.unescape(title_m.group(1))
        date = htmlmod.unescape(date_m.group(1))
        thumb = (thumb_m.group(1) if thumb_m else "").strip()
        body = body_m.group(1).strip()
        body_html = f"<p>{thumb}</p>\n{body}" if thumb else body
        images = [{"src": htmlmod.unescape(src)} for src in re.findall(r'<img[^>]+src="([^"]+)"', thumb or body_html)]
        posts.append({"title": title, "date": date, "body_html": body_html, "images": images})
    return posts


def load_news_posts() -> list:
    """Load news crawl data from the repo, a legacy /tmp path, or generated HTML."""
    for path in (NEWS_JSON, NEWS_JSON_LEGACY):
        if path.exists():
            posts = json.loads(path.read_text(encoding="utf-8"))
            if posts:
                if path != NEWS_JSON:
                    _save_news_posts(posts)
                    print(f"copied news data from {path} -> {NEWS_JSON}")
                return posts
    recovered = recover_news_posts_from_html()
    if recovered:
        _save_news_posts(recovered)
        print(f"recovered {len(recovered)} news posts from news/index.html -> {NEWS_JSON}")
        return recovered
    raise SystemExit(
        f"No news data found. Expected {NEWS_JSON} or a generated news/index.html to recover from."
    )


def _save_news_posts(posts: list) -> None:
    NEWS_JSON.parent.mkdir(parents=True, exist_ok=True)
    NEWS_JSON.write_text(json.dumps(posts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def news():
    posts = load_news_posts()
    items = []
    for post in posts:
        body = rewrite_news_body(post["body_html"])
        thumb_src, thumb_href = extract_thumb(body)
        text = news_text_only(body)
        thumb = ""
        if thumb_src:
            img = f'<img src="{thumb_src}" alt="">'
            if thumb_href:
                ext = ' target="_blank" rel="noopener"' if thumb_href.startswith("http") else ""
                img = f'<a href="{thumb_href}"{ext}>{img}</a>'
            thumb = f'        <div class="thumb">{img}</div>\n'
        else:
            thumb = '        <div class="thumb"></div>\n'
        items.append(f'''      <article class="news-item">
{thumb}        <div>
          <h2>{htmlmod.escape(post["title"])}</h2>
          <time>{htmlmod.escape(post["date"])}</time>
          <div class="body">{text}</div>
        </div>
      </article>''')

    body = f'''  <main class="page">
    <div class="wrap">
      <header class="page-header">
        <h1>News</h1>
      </header>
      <div class="social-follow">
        <p>Follow ab_tech_sweden on <a href="{FB}" target="_blank" rel="noopener">Facebook</a> and <a href="{IG}" target="_blank" rel="noopener">Instagram</a> to get frequent updates on what is going on at AB-Tech</p>
        <div class="social-icons">
          <a href="{FB}" target="_blank" rel="noopener" title="Facebook"><img src="../images/brand/facebook.svg" alt="Facebook" width="56" height="56"></a>
          <a href="{IG}" target="_blank" rel="noopener" title="Instagram"><img src="../images/brand/instagram.png" alt="Instagram" width="56" height="56"></a>
        </div>
      </div>
      <div class="news-list">
{chr(10).join(items)}
      </div>
    </div>
  </main>'''
    write("news/index.html", page(1, "news", "AB-Tech – News", body,
          description="News and show appearances from AB-Tech."))


SITEMAP_PATHS = [
    "",
    "products/",
    "still/",
    "ren/",
    "klar/",
    "frid/",
    "tamp/",
    "about-us/",
    "news/",
    "contact/",
    "bladelius/",
    "reviews/",
]


def write_sitemap():
    urls = "\n".join(
        f"  <url>\n    <loc>{SITE}/{path}</loc>\n  </url>"
        for path in SITEMAP_PATHS
    )
    write("sitemap.xml", f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>
""")


def write_robots():
    write("robots.txt", """User-agent: *
Allow: /

Sitemap: https://ab-tech.se/sitemap.xml
""")


def write_cname():
    write("CNAME", "ab-tech.se\n")


def not_found():
    early = """  <script>
  (function () {
    var preview = location.pathname.indexOf("/abtech-site/") === 0;
    document.write('<base href="' + (preview ? "/abtech-site/" : "/") + '">');
  })();
  </script>
"""
    body = """  <main class="page">
    <div class="wrap error-page">
      <h1>Page not found</h1>
      <p class="lede">The page you are looking for does not exist.</p>
      <p class="error-links">
        <a class="btn" href="index.html">Home</a>
        <a class="btn btn-ghost" href="products/">Products</a>
      </p>
    </div>
  </main>"""
    write("404.html", page(0, "", "AB-Tech – Page not found", body, early_head=early,
                           description="This page could not be found on the AB-Tech website."))


def main():
    home()
    products()
    still()
    ren()
    klar()
    frid()
    tamp()
    about()
    contact()
    bladelius()
    reviews()
    news()
    write_sitemap()
    write_robots()
    write_cname()
    not_found()
    print("done")


if __name__ == "__main__":
    main()
