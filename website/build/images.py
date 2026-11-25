"""Image registry for the MMAG website (v2.0+).

Every image comes from the live mmag.in media library, captured in site-audit/assets/media/.
Client attribution follows the live /mmag-portfolio/ page, where each slide sits next to its
client's link. Each entry: key -> (source path, output width, alt text, mode).
mode: "photo" (lossy WebP), "logo" (trimmed, alpha kept), "square" (centre-cropped square).

Excluded on purpose (pending decisions in docs/PROMPT-LOG.md):
  Aam Aadmi Party (slides 27/28, logo 13-4.png) and Zendale (slides 24-26).
"""

SRC_ROOT = "../../site-audit/assets/media"

IMAGES = {
    # ---- brand --------------------------------------------------------------
    "mmag-logo": ("2026/02/cropped-Group-1171275584.png", 192, "MMAG logo", "logo"),
    "og": ("2026/06/1-scaled-1.webp", 1200, "MMAG agency profile", "og"),

    # ---- client logos (live site: hero strip, hidden clients carousel, testimonials) ----
    "logo-nerolac": ("2026/06/7-1.png", 320, "Kansai Nerolac", "logo"),
    "logo-bajaj": ("2026/06/8.png", 320, "Bajaj Housing Finance", "logo"),
    "logo-eureka": ("2026/06/9.png", 320, "Eureka Forbes", "logo"),
    "logo-tradekings": ("2026/06/10.png", 360, "Trade Kings Group", "logo"),
    "logo-yes": ("2026/06/11-1.png", 360, "Yes Securities", "logo"),
    "logo-upgrad": ("2026/06/12-1.png", 320, "upGrad", "logo"),
    "logo-cloudsufi": ("2026/02/Frame-59.webp", 260, "CloudSufi", "logo"),
    "logo-matrboomie": ("2026/02/logo_png_Asset_1_2x_400e53c3-6e4a-4237-a14c-c214cf2aab92.png", 360, "Matr Boomie", "logo"),
    "logo-syvylyze": ("2026/02/8ee374_023c7eb18711467482c296805dd29654mv2.webp", 360, "Syvylyze Analytics", "logo"),
    "logo-arh": ("2026/02/images.png", 220, "ARH Design Academy", "logo"),
    "logo-trevex": ("2026/02/Main-Logo-1.webp", 360, "Trevex", "logo"),
    "logo-yash": ("2026/02/logo-1.png", 260, "Yash Group of Industries", "logo"),
    "logo-the-spark": ("2026/02/logo.svg", 0, "The Spark", "svg"),

    # ---- people (live About page; names verified from the page markup) ----
    "p-rushikesh": ("2026/02/Rushi-1.webp", 700, "Rushikesh Kate, Founder & CEO of MMAG", "photo"),
    "p-vipul": ("2026/02/Frame-1.webp", 560, "Vipul Jadhav, Vice President", "photo"),
    "p-madhukar": ("2026/02/Frame-12.webp", 560, "Madhukar Khare, Creative Director", "photo"),
    "p-saud": ("2026/06/default-Saud.webp", 560, "Saud Pardesi, Sr. Web Developer", "photo"),
    "p-maithili": ("2026/06/default-Maithili.webp", 560, "Maithili Jadhav, Human Resource", "photo"),
    "team-at-work": ("2026/06/team-scaled.webp", 1600, "The MMAG team at work in the Pune studio", "photo"),
    "culture-1": ("2026/06/IMG_6783-1-1.webp", 1124, "MMAG team celebration in the studio", "photo"),
    "culture-2": ("2026/06/IMG_6783-5.webp", 1124, "MMAG team selfie", "photo"),
    "culture-3": ("2026/06/IMG_6783-2-1.webp", 1124, "MMAG team group photo", "photo"),
    "culture-4": ("2026/06/IMG_6783-3.webp", 1124, "MMAG team at a festive celebration", "photo"),
    "culture-5": ("2026/06/IMG_6783-7.webp", 1124, "MMAG team outing", "photo"),
    "flag-india": ("2026/06/world.webp", 160, "India", "logo"),
    "flag-usa": ("2026/06/flag.webp", 160, "USA", "logo"),

    # ---- work thumbnails (live Home "Work that speaks") ----
    "thumb-trevex": ("2026/03/trevex-tumbnail.webp", 900, "Trevex website shown on desktop, tablet and phone", "photo"),
    "thumb-tradekings": ("2026/03/tkg-thumbnail.webp", 900, "Trade Kings Group social media creatives", "photo"),
    "thumb-bajaj": ("2026/03/BHFL-thumbnail.webp", 900, "Bajaj Housing Finance social media posts", "photo"),

    # ---- portfolio slides (live /mmag-portfolio/, client from the adjacent link) ----
    "w-bajaj-social": ("2026/06/8-scaled-1.webp", 1400, "Bajaj Housing Finance social media campaign posts", "photo"),
    "w-eureka-web": ("2026/06/13-4-scaled-1.webp", 1400, "Eureka Forbes website on laptop and phone", "photo"),
    "w-eureka-creatives": ("2026/06/13-2-scaled-1.webp", 1400, "Eureka Forbes e-commerce creatives", "photo"),
    "w-eureka-creatives-2": ("2026/06/13-3-scaled-1.webp", 1400, "Eureka Forbes campaign creatives", "photo"),
    "w-tradekings-creatives": ("2026/06/12-scaled-1.webp", 1400, "Trade Kings Group product creatives", "photo"),
    "w-tradekings-social": ("2026/06/13-scaled-1.webp", 1400, "Trade Kings Group social media posts", "photo"),
    "w-tradekings-reels": ("2026/06/14-scaled-1.webp", 1400, "Trade Kings Group product reels", "photo"),
    "w-trevex-web": ("2026/06/20-scaled-1.webp", 1400, "Trevex website for debt recovery", "photo"),
    "w-trevex-web-2": ("2026/06/21-scaled-1.webp", 1400, "Trevex credit report web pages", "photo"),
    "w-trevex-social": ("2026/06/22-scaled-1.webp", 1400, "Trevex social media creatives", "photo"),
    "w-cloudsufi-web": ("2026/06/8-scaled-2.webp", 1400, "CloudSufi website on multiple devices", "photo"),
    "w-cloudsufi-social": ("2026/06/9-1-scaled-2.webp", 1400, "CloudSufi social media creatives", "photo"),
    "w-matrboomie-web": ("2026/06/14-2-scaled-1.webp", 1400, "Matr Boomie e-commerce website", "photo"),
    "w-suiteearth-web": ("2026/06/16-scaled-1.webp", 1400, "Suiteearth website on multiple devices", "photo"),
    "w-suiteearth-print": ("2026/06/17-scaled-1.webp", 1400, "Suiteearth printed collateral", "photo"),
    "w-suitefy-web": ("2026/06/19-3-2-scaled-1.webp", 1400, "Suitefy website on multiple devices", "photo"),
    "w-equinext-web": ("2026/06/19-3-1-scaled-1.webp", 1400, "EquiNext website on multiple devices", "photo"),
    "w-equinext-brochure": ("2026/06/19-3-7-scaled-1.webp", 1400, "EquiNext brochure", "photo"),
    "w-equinext-social": ("2026/06/19-3-8-scaled-1.webp", 1400, "EquiNext social media posts", "photo"),
    "w-equinext-standees": ("2026/06/19-3-9-scaled-1.webp", 1400, "EquiNext event standees", "photo"),
    "w-knorr-social": ("2026/06/19-1-1-scaled-1.webp", 1400, "Knorr-Bremse LinkedIn creatives", "photo"),
    "w-knorr-social-2": ("2026/06/19-1-1-1-scaled-1.webp", 1400, "Knorr-Bremse LinkedIn posts", "photo"),
    "w-yash-web": ("2026/06/19-3-scaled-1.webp", 1400, "Yash Group of Industries website", "photo"),
    "w-copilot-web": ("2026/06/21-scaled-2.webp", 1400, "CopilotForce website on multiple devices", "photo"),
    "w-copilot-bot": ("2026/06/22-scaled-2.webp", 1400, "CopilotForce chatbot assistant ‘Mark’", "photo"),
    "w-copilot-social": ("2026/06/23-scaled-2.webp", 1400, "CopilotForce social media creatives", "photo"),
    "w-mantri-web": ("2026/06/30-scaled-2.webp", 1400, "Mantri Constructions Casa Jewel website", "photo"),
    "w-mantri-social": ("2026/06/31-scaled-1.webp", 1400, "Mantri Constructions Casa Jewel social media and ads", "photo"),
    "w-nealife-web": ("2026/06/33-1-scaled-1.webp", 1400, "NEA Life website on multiple devices", "photo"),
    "w-print-catalogue": ("2026/06/43-scaled-1.webp", 1400, "Printed product catalogue", "photo"),
    "w-print-billboard": ("2026/06/44-scaled-1.webp", 1400, "Outdoor billboard design", "photo"),
}

# Social reel covers (live portfolio pages: video thumbnails)
REELS = [
    ("2026/06/3-21.png", "Bajaj Housing Finance reel"), ("2026/06/Group-1171275619.webp", "Trade Kings Group reel"),
    ("2026/06/3-22.png", "Bajaj Housing Finance reel"), ("2026/06/Group-1171275558.webp", "Trade Kings Group reel"),
    ("2026/06/3-24.png", "Bajaj Housing Finance reel"), ("2026/06/Group-1171275559.webp", "Trade Kings Group reel"),
    ("2026/06/3-25.png", "Bajaj Housing Finance reel"), ("2026/06/Group-1171275560.webp", "Trade Kings Group reel"),
    ("2026/06/3-26.png", "Bajaj Housing Finance reel"), ("2026/06/Group-1171275562.webp", "Trade Kings Group reel"),
    ("2026/06/3-27@2x.png", "Bajaj Housing Finance reel"), ("2026/06/Group-1171275563.webp", "Trade Kings Group reel"),
    ("2026/06/3-28.png", "Bajaj Housing Finance reel"), ("2026/06/Group-1171275564.webp", "Trade Kings Group reel"),
    ("2026/06/Group-1171275565.webp", "Trade Kings Group reel"), ("2026/06/Group-1171275566.webp", "Trade Kings Group reel"),
]
for _i, (_src, _alt) in enumerate(REELS):
    IMAGES[f"reel-{_i}"] = (_src, 420, _alt, "photo")

# Clients ring (13 logos; AAP excluded pending decision)
RING_LOGOS = ["logo-nerolac", "logo-bajaj", "logo-eureka", "logo-tradekings", "logo-yes", "logo-upgrad", "logo-cloudsufi",
              "logo-matrboomie", "logo-syvylyze", "logo-arh", "logo-trevex", "logo-yash", "logo-the-spark"]

# Testimonial logos (same order as content.TESTIMONIALS)
TESTIMONIAL_LOGOS = ["logo-syvylyze", "logo-matrboomie", "logo-the-spark", "logo-cloudsufi", "logo-arh"]

# Projects: name, tags, live link, images (first = preview), avoid-on (case slugs that are probably this client, kept anonymous)
PROJECTS = [
    ("Bajaj Housing Finance", "Social media · Housing finance", "https://www.bajajhousingfinance.in/", ["w-bajaj-social", "thumb-bajaj"], []),
    ("Trade Kings Group", "Social media · FMCG", "https://www.tradekings.co.zm/", ["w-tradekings-creatives", "w-tradekings-social", "w-tradekings-reels", "thumb-tradekings"], []),
    ("Eureka Forbes", "Website · Social · Consumer durables", "https://www.eurekaforbes.com/", ["w-eureka-web", "w-eureka-creatives", "w-eureka-creatives-2"], []),
    ("Trevex", "UI/UX · Website · Social · Finance", "", ["w-trevex-web", "w-trevex-web-2", "w-trevex-social", "thumb-trevex"], []),
    ("CloudSufi", "Website · Branding · UX · Technology", "https://www.cloudsufi.com/", ["w-cloudsufi-web", "w-cloudsufi-social"], []),
    ("Mantri Constructions · Casa Jewel", "Website · Social · Real estate", "", ["w-mantri-web", "w-mantri-social"], ["real-estate-luxury"]),
    ("Matr Boomie", "Website · SEO · E-commerce", "https://matrboomie.com/", ["w-matrboomie-web"], ["e-commerce-fair-trade-goods-b2b"]),
    ("Knorr-Bremse", "LinkedIn · Automobile", "https://www.knorr-bremse.com/en/", ["w-knorr-social", "w-knorr-social-2"], ["b2b-engineering-manufacturing"]),
    ("CopilotForce", "Website · Chatbot · Technology", "", ["w-copilot-web", "w-copilot-bot", "w-copilot-social"], []),
    ("EquiNext", "Website · Brochure · Social · Turnkey solutions", "https://equinextsolution.com/", ["w-equinext-web", "w-equinext-brochure", "w-equinext-social", "w-equinext-standees"], []),
    ("Suiteearth", "Website · Print · SaaS", "https://suiteearth.com/", ["w-suiteearth-web", "w-suiteearth-print"], []),
    ("Suitefy", "Website · SaaS", "https://suitefy.com/", ["w-suitefy-web"], []),
    ("NEA Life", "Website · Education", "https://nealife.in/", ["w-nealife-web"], []),
    ("Yash Group of Industries", "Website · Manufacturing", "", ["w-yash-web"], []),
]

# Image for each Home service card, and the gallery strip on each service page (key, caption)
SERVICE_IMAGES = {
    "branding": [("w-equinext-standees", "EquiNext · event standees"), ("w-equinext-brochure", "EquiNext · brochure"),
                 ("w-suiteearth-print", "Suiteearth · print collateral"), ("w-print-catalogue", "Print · product catalogue"),
                 ("w-print-billboard", "Outdoor · billboard")],
    "website-design-development": [("w-eureka-web", "Eureka Forbes · website"), ("w-trevex-web", "Trevex · website"),
                                   ("w-cloudsufi-web", "CloudSufi · website"), ("w-copilot-web", "CopilotForce · website"),
                                   ("w-suiteearth-web", "Suiteearth · website"), ("w-equinext-web", "EquiNext · website"),
                                   ("w-nealife-web", "NEA Life · website"), ("w-yash-web", "Yash Group · website")],
    "seo": [("w-matrboomie-web", "Matr Boomie · website & SEO"), ("w-mantri-web", "Mantri Constructions · website & SEO"),
            ("w-suitefy-web", "Suitefy · website")],
    "social-media-marketing": [("w-bajaj-social", "Bajaj Housing Finance · social"), ("w-tradekings-creatives", "Trade Kings Group · creatives"),
                               ("w-knorr-social", "Knorr-Bremse · LinkedIn"), ("w-trevex-social", "Trevex · social"),
                               ("w-cloudsufi-social", "CloudSufi · social"), ("w-equinext-social", "EquiNext · social"),
                               ("w-copilot-social", "CopilotForce · social"), ("w-tradekings-social", "Trade Kings Group · social")],
    "performance-marketing": [("w-mantri-social", "Mantri Constructions · social & ads"), ("w-eureka-creatives-2", "Eureka Forbes · campaign creatives"),
                              ("w-trevex-social", "Trevex · campaign creatives"), ("w-tradekings-reels", "Trade Kings Group · reels")],
}

# Image for each deliverable card on service pages (4 per service)
CARD_IMAGES = {
    "branding": ["w-equinext-brochure", "w-suiteearth-print", "w-equinext-social", "w-equinext-standees"],
    "website-design-development": ["w-trevex-web-2", "w-eureka-web", "w-copilot-web", "w-mantri-web"],
    "seo": ["w-matrboomie-web", "w-suitefy-web", "w-nealife-web", "w-cloudsufi-web"],
    "social-media-marketing": ["w-knorr-social", "w-bajaj-social", "w-equinext-social", "w-tradekings-social"],
    "performance-marketing": ["w-mantri-social", "w-copilot-web", "w-copilot-bot", "w-eureka-creatives"],
}
HOME_SERVICE_IMAGE = {"branding": "w-equinext-standees", "website-design-development": "w-eureka-web", "seo": "w-matrboomie-web",
                      "social-media-marketing": "w-bajaj-social", "performance-marketing": "w-mantri-social"}

# Which services each case study belongs to (for its "More work like this" row)
CASE_SERVICE = {
    "retail-florist": "website-design-development", "fmcg-d2c-food": "social-media-marketing", "education": "branding",
    "education-childrens-enrichment": "website-design-development", "real-estate-luxury": "performance-marketing",
    "b2b-engineering-manufacturing": "social-media-marketing", "e-commerce-fair-trade-goods-b2b": "seo",
}

TEAM_PHOTOS = {"Rushikesh Kate": "p-rushikesh", "Vipul Jadhav": "p-vipul", "Madhukar Khare": "p-madhukar",
               "Saud Pardesi": "p-saud", "Maithili Jadhav": "p-maithili"}

CULTURE = ["culture-1", "culture-2", "culture-3", "culture-4", "culture-5"]

# Portfolio wall on /work/ (3 parallax columns)
WALL = [
    ["w-eureka-web", "w-bajaj-social", "w-copilot-bot", "w-suiteearth-web", "w-equinext-brochure"],
    ["w-tradekings-creatives", "w-trevex-web", "w-mantri-social", "w-knorr-social", "w-nealife-web"],
    ["w-cloudsufi-web", "w-equinext-standees", "w-trevex-social", "w-yash-web", "w-print-billboard"],
]
