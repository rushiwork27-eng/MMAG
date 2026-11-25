"""Site content for the MMAG website build.

Copy comes from the live mmag.in capture (site-audit/, 24 Nov 2026) unless marked NEW.
NEW copy (headlines, one-liners) makes no factual claims and still needs sign-off.
Numbers are as published on the live site and still need sign-off (findings H5/H6).
"""

PHONE = "+918308852044"
PHONE_DISPLAY = "+91 83088 52044"
MAPS_URL = "https://maps.app.goo.gl/wxVkVbBEvJV89RsL7"
LOCATION = "Kothrud, Pune"
# From MMAG's own portfolio deck on the live site (/mmag-portfolio/, "We're all ears!" slide)
EMAIL = "rushi@mmag.in"
WHATSAPP = "https://wa.me/918308852044"
ADDRESS_LINES = ["Office No. 104, Chintamani Pride", "Near City Pride, Kothrud", "Pune, Maharashtra 411038, India"]
SOCIALS = [
    ("Instagram", "https://www.instagram.com/mmag_india/"),
    ("LinkedIn", "https://www.linkedin.com/company/mmagindia"),
    ("YouTube", "https://www.youtube.com/@mmag2717"),
    ("Facebook", "https://www.facebook.com/mmag.india/"),
]

# Inquiry options: exactly as on the live Download Portfolio / Schedule A Call forms
INQUIRY_OPTIONS = [
    "Website Development", "E-Commerce Marketing", "Branding", "Social Media Marketing",
    "Search Engine Optimization", "Lead Generation", "Email Marketing", "App Development", "Others",
]
# Contact form interest checkboxes: exactly as on the live Contact page
CONTACT_INTERESTS = ["Strategy", "Design", "Technology", "Performance"]

COUNTRY_CODES = [
    ("+91", "India +91"), ("+1", "USA / Canada +1"), ("+44", "UK +44"), ("+971", "UAE +971"),
    ("+61", "Australia +61"), ("+65", "Singapore +65"), ("+49", "Germany +49"), ("+260", "Zambia +260"),
    ("+966", "Saudi Arabia +966"), ("+974", "Qatar +974"), ("+27", "South Africa +27"), ("+64", "New Zealand +64"),
    ("+31", "Netherlands +31"), ("+33", "France +33"), ("", "Other (type code in number)"),
]

# Client names shown in the 3D ring: all appear on the live site (hero logos, testimonials, portfolio links).
# Aam Aadmi Party is left out pending a management decision (site plan, decision 4).
CLIENTS = [
    "Kansai Nerolac", "Bajaj Housing Finance", "Eureka Forbes", "Trade Kings Group", "Yes Securities", "upGrad",
    "CloudSufi", "Matr Boomie", "The Spark", "Syvylyze Analytics", "ARH Design Academy", "Trevex",
    "Knorr-Bremse", "Suitefy", "Nealife", "EquiNext",
]

PROCESS = [  # live site, Home "Discover / Define / Design / Drive"
    ("Discover", "We understand client’s vision, market & audience"),
    ("Define", "We shape your brand and strategy"),
    ("Design", "We craft visual experiences"),
    ("Drive", "We launch, measure and optimize for ROI"),
]

TESTIMONIALS = [  # verbatim from the live site (typos left as written by clients)
    {"quote": "We have been working with the MMAG for the past years and have been extremely satisfied with results. The team is always responsive and professional and they have provided valuable insights and recommendations to help us continually improve our marketing efforts.",
     "name": "Rahil Sanghavi", "role": "CFO", "org": "Syvylyze Analytics"},
    {"quote": "MMAG team’s has done a great job on SEO work, approaching SEO in a very holistic way. Our Organic traffic has doubled in 6 months and our relevant key words on 1st page has quadrupled.",
     "name": "Manish Gupta", "role": "Founder of Matr Boomie", "org": "Matr Boomie - USA"},
    {"quote": "The guys are top of their game… I couldn’t recommend them any more, and I highly, highly suggest you check out their body of work.",
     "name": "Sebastian Alapatt", "role": "Founder of Spark", "org": "The Spark - USA"},
    {"quote": "Chosen for fit UX and promptness, their team included designers, project managers and developers. The project involves site mapping, Branding, UX design, Development and Launch. Workflow was efficient with daily scrum.",
     "name": "Chief Strategy Officer", "role": "", "org": "CloudSufi Tech Company - USA"},
    {"quote": "Rushikesh is extremely talented individual and the team they have build in MMAG is capable of delivering projects which will yield results. I would recommend them 10/10",
     "name": "Ajinkya Harshey", "role": "Chief Mentor", "org": "ARH Design Academy"},
]

# ---------------------------------------------------------------------------
# Case studies (live site). "stats": value, format, prefix, suffix, label.
# ---------------------------------------------------------------------------
CASES = [
    {
        "slug": "retail-florist", "short": "Retail Florist",
        "kicker": "Website + Social + Paid",
        "title": "A Seasonal E-commerce Launch in Just 20 Days",
        "summary": "How an offline florist went from no online presence to a live, revenue-generating store in time for the year’s biggest gifting season.",
        "industry": "Retail — Florist", "location": "Australia", "services": "Web, Social & Paid Ads",
        "metric": "5,859+", "metric_label": "website users in 2 months",
        "tags": "service:websites service:social service:paid industry:retail loc:international",
        "stats": [(5859, "comma", "", "+", "website users in 2 months"), (55012, "comma", "", "+", "Instagram impressions"), (22, "", "", "%", "return on ad spend")],
        "challenge": [
            "After five years running an offline dry & fresh flower business, the client wanted to move online and capture the year’s highest-demand window — New Year and Valentine’s Day.",
            "The entire store had to be designed, built and launched within a tight 20-day timeline to hit the season.",
            "As a first-time online seller, the brand needed to establish immediate trust and credibility with online shoppers.",
        ],
        "approach": [
            "Opened with a discovery session to understand the seasonal buyer, the product range and the brand’s story.",
            "Designed and developed an e-commerce store optimised for a fast launch and seasonal conversion.",
            "Built a social media presence to drive awareness and signal credibility ahead of the peak.",
            "Ran a targeted paid advertising campaign timed precisely to New Year and Valentine’s demand.",
        ],
        "results": [
            "Attracted 5,859+ users to the brand-new website within the first two months.",
            "Generated 55,012+ Instagram impressions, building rapid brand awareness.",
            "Delivered a 22% return on ad spend during the launch season.",
        ],
    },
    {
        "slug": "fmcg-d2c-food", "short": "FMCG — D2C Food",
        "kicker": "Social Media + Paid Advertising",
        "title": "From −50% Ad ROI to 200% Growth",
        "summary": "How a new-to-market snack brand reversed stalled growth by repositioning an unfamiliar product as a healthier choice.",
        "industry": "FMCG — D2C Food", "location": "India", "services": "Social & Paid Ads",
        "metric": "131%", "metric_label": "increase in sales",
        "tags": "service:social service:paid industry:fmcg loc:india",
        "stats": [(131, "", "", "%", "increase in sales"), (200, "", "", "%", "increase in ROI"), ("0.77% → 3.35%", "text", "", "", "website conversion rate")],
        "challenge": [
            "The brand produced an unfamiliar product — vacuum-fried fruit and vegetable chips (raw mango, sweet potato, okra) that were new to the market.",
            "Chips are widely seen as junk food, so buyers needed to be educated on the vacuum-frying process and its health benefits.",
            "Growth had stalled: order volumes were flat, advertising ROI sat at −50%, and website conversion over the previous three months was just 0.77%.",
        ],
        "approach": [
            "Began with a discovery session to understand the product, the buyer’s hesitations and how the category was perceived.",
            "Built an education-led content strategy to reposition the chips as a healthier snack and explain the vacuum-frying process.",
            "Rebuilt the paid advertising strategy — audience targeting, creative and funnel — to fix the negative ROI.",
            "Managed social media to build awareness, trust and community around the brand.",
        ],
        "results": [
            "Increased sales by 131%.",
            "Improved return on advertising by 200%, reversing a −50% starting point.",
            "Lifted website conversion rate from 0.77% to 3.35%.",
        ],
    },
    {
        "slug": "education", "short": "Education",
        "kicker": "Branding + Paid Advertising",
        "title": "A Category-Defining Brand That Tripled Admissions",
        "summary": "How a specialist coaching institute out-positioned larger, older competitors — and grew enough to open a new branch.",
        "industry": "Education", "location": "India", "services": "Branding & Paid Ads",
        "metric": "300%", "metric_label": "increase in admissions",
        "tags": "service:branding service:paid industry:education loc:india",
        "stats": [(300, "", "", "%", "increase in admissions"), ("New branch", "text", "", "", "opened by the client"), ("Enquiries ↑", "text", "", "", "& social engagement up")],
        "challenge": [
            "The institute coaches creative students for entry into Architecture, Design and Fashion Design, differentiated by small batch sizes, personal attention and career-focused learning.",
            "It competed against large, long-established coaching classes operating in the same area.",
            "It had no online visibility to speak of.",
            "It had less faculty experience than its bigger competitors, making differentiation harder.",
        ],
        "approach": [
            "Studied competitors’ digital strategies and found they nearly all relied on identical messaging.",
            "Used that gap to build a distinctive, category-defining brand and digital experience that showcased the institute’s real differentiators — small batches, personal attention and long-term career focus.",
            "Ran targeted paid advertising to drive enquiries and admissions.",
        ],
        "results": [
            "Increased admissions by 300%.",
            "Grew enquiries and social media engagement significantly.",
            "Performed strongly enough to enable the client to open a new branch.",
        ],
    },
    {
        "slug": "education-childrens-enrichment", "short": "Children’s Enrichment",
        "kicker": "Website Redesign (UI/UX)",
        "title": "A Website Redesign Built for Clarity and Conversion",
        "summary": "How a children’s art & wellness brand turned a cluttered website into a clean, high-converting experience across two locations.",
        "industry": "Education — Children’s Enrichment", "location": "USA", "services": "Website Redesign (UI/UX)",
        "metric": "24%", "metric_label": "increase in website orders*",
        "tags": "service:websites industry:education loc:international",
        "stats": [(24, "", "", "%", "increase in website orders*"), (2, "", "", "", "colour themes (New York & Pennsylvania)"), (16, "", "", "%", "reduction in bounce rate*")],
        "footnote": "* Measured against the six months before the redesign.",
        "challenge": [
            "The brand runs a unique programme combining art, yoga, meditation and nature for children, and was expanding to a second location — but its existing site couldn’t showcase the new services.",
            "A site audit found hygiene issues affecting text readability, flow and alignment.",
            "The homepage was cluttered, making it hard for visitors to navigate and find information.",
            "Inconsistent design across sections created a disjointed experience, and a lack of visual hierarchy let non-critical elements overshadow key content.",
        ],
        "approach": [
            "Established a design system with standardised typography, consistent spacing and compliant colour-contrast ratios to fix readability and consistency.",
            "Introduced a grid-based layout with deliberate white space, turning a cluttered homepage into an organised, scannable interface.",
            "Built a clear visual hierarchy through typography scaling, strategic colour and intentional positioning so critical information stood out.",
            "Created a unified design language with standardised components and documented guidelines for a cohesive experience across every page.",
            "Used distinct colour themes to help visitors tell the New York and Pennsylvania programmes apart.",
        ],
        "results": [
            "Increased orders placed on the website (measured against the six months before the redesign).",
            "Introduced 2 distinct colour themes to differentiate the New York and Pennsylvania classes.",
            "Reduced the site’s bounce rate (measured against the six months before the redesign).",
        ],
    },
    {
        "slug": "real-estate-luxury", "short": "Luxury Real Estate",
        "kicker": "Performance Marketing",
        "title": "Generating High-Intent Leads for Luxury Real Estate",
        "summary": "How an ultra-luxury residential project built a digital presence from scratch — and an automated sales pipeline to match.",
        "industry": "Real Estate — Luxury", "location": "India", "services": "Performance Marketing",
        "metric": "500+", "metric_label": "high-intent leads generated",
        "tags": "service:paid service:websites industry:real-estate loc:india",
        "stats": [(500, "", "", "+", "high-intent leads generated"), (4, "", "", " Lac+", "prospects reached"), (50, "", "", "+", "site visits booked")],
        "challenge": [
            "An ultra-luxurious 4 BHK development in a prime, upscale locale needed high-quality leads for exclusive 5,200 sq. ft. residences aimed at the elite of two major cities.",
            "The target audience was very niche and hard to reach.",
            "The project had no existing digital presence.",
            "There was no dedicated project sales team, so the sales process had to be automated.",
        ],
        "approach": [
            "Built a user-friendly landing-page website as the brand’s main touchpoint to raise awareness.",
            "Deployed target-specific paid campaigns aimed at high-value home buyers and investors across both key cities, highlighting the project’s USPs.",
            "Created a new social media identity to build awareness and drive purchase-intent enquiries.",
            "Automated lead nurturing over WhatsApp — sending project information and floor plans, and booking site visits — to replace a manual sales team.",
        ],
        "results": [
            "Generated a strong volume of high-intent leads for the project.",
            "Reached a large pool of qualified prospects across the two target cities.",
            "Converted interest into booked site visits through automated nurturing.",
        ],
    },
    {
        "slug": "b2b-engineering-manufacturing", "short": "B2B Engineering",
        "kicker": "Social Media",
        "title": "Building B2B Authority on LinkedIn",
        "summary": "How the Indian technology centre of a global engineering manufacturer grew an engaged LinkedIn audience from the ground up.",
        "industry": "B2B Engineering / Manufacturing", "location": "India", "services": "Social Media (LinkedIn)",
        "metric": "9K", "metric_label": "organic followers (2021–2022)",
        "tags": "service:social industry:b2b loc:india",
        "stats": [(9, "", "", "K", "organic followers (2021–2022)"), (13, "", "", " Lac+", "impressions in 10 months"), (205, "", "", "%", "increase in engagement")],
        "challenge": [
            "The Indian technology centre of a German braking-systems manufacturer — supporting mechanical and electronic products for rail and truck systems — wanted to build its LinkedIn presence for awareness, engagement and followers.",
            "Despite being a globally famous name, the page had no strategy-driven content.",
            "Engagement on existing content was low.",
            "Follower growth was slow.",
        ],
        "approach": [
            "Translated the technology centre’s deep domain knowledge and technical expertise into engaging, jargon-free social content.",
            "Implemented a content plan showcasing innovation, company culture and activities to grow awareness and engagement.",
            "Designed distinctive hiring-campaign strategies to attract top industry talent.",
        ],
        "results": [
            "Grew organic followers significantly across 2021–2022.",
            "Generated a high volume of impressions within ten months.",
            "Increased engagement on the page.",
        ],
    },
    {
        "slug": "e-commerce-fair-trade-goods-b2b", "short": "Fair-Trade B2B",
        "kicker": "Search Engine Optimisation",
        "title": "547% More First-Time Users Through B2B SEO",
        "summary": "How a fair-trade wholesale brand went from invisible to dominant for its B2B search terms.",
        "industry": "E-commerce — Fair-Trade Goods (B2B)", "location": "USA", "services": "Search Engine Optimisation",
        "metric": "547%", "metric_label": "increase in first-time users",
        "tags": "service:seo industry:b2b loc:international",
        "stats": [(547, "", "", "%", "increase in first-time users"), (252, "", "", "%", "new keywords on page 1 of SERP"), (36, "", "", "", "keywords ranking in the top 3")],
        "challenge": [
            "A US-based supplier of sustainable, fair-trade products wanted to grow B2B sales through its wholesale platform, but the wholesale site was underperforming in a competitive market.",
            "Wholesale search queries surfaced the brand’s B2C website instead of the wholesale site.",
            "The wholesale site had no visibility on search results for B2B keywords.",
            "It attracted only brand-driven keyword traffic, in a niche space dominated by prominent players.",
        ],
        "approach": [
            "Carried out in-depth keyword research to identify high-potential B2B terms (e.g. ‘plant pots wholesale’, ‘reusable shopping bags bulk’, ‘bulk terracotta pots’), each with 1,000+ monthly searches.",
            "Optimised existing pages and developed new, SEO-friendly content tailored to those keywords.",
            "Improved technical SEO — faster load times, mobile optimisation and better site architecture for crawlability and user experience.",
            "Executed a content-marketing strategy of blogs, product descriptions and educational resources aimed at B2B buyers.",
        ],
        "results": [
            "Increased first-time users by 547%.",
            "Grew the number of keywords ranking on the first page of search results.",
            "Earned multiple keywords ranking in the top three positions.",
        ],
    },
]

# Portfolio projects now live in images.py (with their images).

# ---------------------------------------------------------------------------
# Services (5). Headlines and one-liners are NEW copy; deliverables use words
# from the live site (pillars, inquiry list) and the case-study approaches.
# ---------------------------------------------------------------------------
SERVICES = [
    {
        "slug": "branding", "name": "Branding & Strategy", "short": "Branding", "scene": 0,
        "hero": "Brands people pick out of a crowd",
        "lead": "Positioning, identity and content strategy, built on what actually makes you different.",
        "line": "Positioning, identity and strategy that set you apart.",
        "meta": "Branding and brand strategy by MMAG, Pune: brand positioning, identity, marketing collaterals and content strategy.",
        "cards": [
            ("Brand Positioning", "Find the gap your competitors leave open.", ["Competitor messaging study", "Differentiators", "Category-defining brand"]),
            ("Identity & Collaterals", "A look people remember, applied everywhere.", ["Logo concept", "Typography & colour", "Marketing collaterals"]),
            ("Content Strategy", "What to say, where, and how often.", ["Content Strategy", "Discoverability", "Education-led content"]),
            ("Digital Strategy", "One plan that ties brand, site and media together.", ["Digital Strategy", "Brand Positioning", "Digital experience"]),
        ],
        "cases": ["education"],
        "faq": ("How do you build a brand that stands out?", "We study how competitors talk about themselves, find the gap in that messaging, and build a distinctive brand around your real differentiators — the approach behind our coaching-institute case study."),
    },
    {
        "slug": "website-design-development", "name": "Websites & UI/UX", "short": "Websites", "scene": 1,
        "hero": "Websites that turn visits into business",
        "lead": "UX, web design and development for brand sites, e-commerce stores and landing pages.",
        "line": "UX, design and development for sites that convert.",
        "meta": "Website design and development by MMAG, Pune: UX, UI design, e-commerce stores, landing pages and website redesigns.",
        "cards": [
            ("User Experience (UX)", "Clear paths to the action that matters.", ["Site audit", "Wireframes", "Visual hierarchy"]),
            ("Web Design", "A design system, not a pile of pages.", ["Design system", "Grid layouts", "Motion design"]),
            ("Development", "Built fast, built to be edited.", ["Front End Development", "Back End Development", "Content Management"]),
            ("E-commerce & Landing Pages", "Stores and pages ready for launch day.", ["E-commerce stores", "Landing pages", "Seasonal launches"]),
        ],
        "cases": ["retail-florist", "education-childrens-enrichment", "real-estate-luxury"],
        "faq": ("What goes into a website redesign?", "A site audit first, then a design system (typography, spacing, colour contrast), a grid-based layout, a clear visual hierarchy and documented components so every page stays consistent."),
    },
    {
        "slug": "seo", "name": "Search Engine Optimization", "short": "SEO", "scene": 2,
        "hero": "Be found by buyers already searching",
        "lead": "Keyword research, technical SEO and content built to rank for the terms that bring business.",
        "line": "Keyword research, technical SEO and content that ranks.",
        "meta": "SEO services by MMAG, Pune: keyword research, on-page optimisation, technical SEO and content marketing for B2B and e-commerce brands.",
        "cards": [
            ("Keyword Research", "Terms with real search demand behind them.", ["B2B search terms", "Search intent", "Competition gaps"]),
            ("On-page SEO", "Pages built around those terms.", ["Page optimisation", "New SEO content", "Keyword targeting"]),
            ("Technical SEO", "A site search engines can crawl and trust.", ["Load speed", "Mobile optimisation", "Site architecture"]),
            ("Content Marketing", "Answers your buyers are looking for.", ["Blogs", "Product descriptions", "Educational resources"]),
        ],
        "cases": ["e-commerce-fair-trade-goods-b2b"],
        "faq": ("What does your SEO work include?", "Keyword research, optimising existing pages and writing new SEO content, technical SEO (load speed, mobile, site architecture) and content marketing aimed at your buyers."),
    },
    {
        "slug": "social-media-marketing", "name": "Social Media Marketing", "short": "Social", "scene": 3,
        "hero": "Social that builds trust before the sale",
        "lead": "Content plans, creatives and campaigns for B2B and consumer brands.",
        "line": "Content, creatives and campaigns that build trust.",
        "meta": "Social media marketing by MMAG, Pune: content plans, creatives, campaigns and community building for B2B and consumer brands.",
        "cards": [
            ("Content Plan", "Your expertise, turned into posts people read.", ["Jargon-free content", "Innovation & culture", "Company activities"]),
            ("Creatives & Reels", "On-brand, scroll-stopping, every week.", ["Reels", "Static posts", "Campaign creatives"]),
            ("Campaigns", "Launches, seasons and hiring drives.", ["Hiring campaigns", "Seasonal pushes", "Awareness"]),
            ("Community", "Trust and conversation around the brand.", ["Engagement", "Follower growth", "Education-led content"]),
        ],
        "cases": ["b2b-engineering-manufacturing", "fmcg-d2c-food", "retail-florist"],
        "faq": ("What does social media management include?", "A content plan built from your expertise, regular creatives, campaigns (including hiring campaigns) and the day-to-day work of building a community around the brand."),
    },
    {
        "slug": "performance-marketing", "name": "Performance Marketing", "short": "Performance", "scene": 4,
        "hero": "Paid media built around leads and sales",
        "lead": "Targeted campaigns, landing pages, conversion optimisation and automated lead nurturing.",
        "line": "Paid campaigns, landing pages and lead nurturing.",
        "meta": "Performance marketing by MMAG, Pune: paid campaigns, landing pages, conversion rate optimisation, lead generation and automated lead nurturing.",
        "cards": [
            ("Paid Campaigns", "Audience, creative and funnel, rebuilt to perform.", ["Audience targeting", "Ad creative", "Funnel"]),
            ("Landing Pages", "One page, one job: the enquiry.", ["Landing-page websites", "USP messaging", "Purchase-intent enquiries"]),
            ("Lead Nurturing", "Follow-up that runs on its own.", ["WhatsApp automation", "Project info & floor plans", "Site-visit booking"]),
            ("Conversion & Growth", "More of your visits become customers.", ["Conversion Rate Optimization", "Lead Generation", "Email Marketing"]),
        ],
        "cases": ["real-estate-luxury", "fmcg-d2c-food", "education", "retail-florist"],
        "faq": ("What does performance marketing include?", "Target-specific paid campaigns, a landing page that converts, a social presence to support them, and automated lead nurturing — for example over WhatsApp — so no enquiry goes cold."),
    },
]

# Shared FAQ answers, all sourced from the live site (About page, case studies).
FAQ_COMMON = [
    ("Which industries do you work with?", "Real Estate, HealthCare, FMCG, Tech and Manufacturing — and education, retail and B2B e-commerce in our case studies."),
    ("Do you work with clients outside India?", "Yes. We work with brands in India and the USA, including CloudSufi, The Spark and Matr Boomie."),
    ("How does a project start?", "With a discovery session to understand your business, your buyers and what success looks like."),
    ("Where are you based?", "Kothrud, Pune. We work remote-first with clients in other cities and countries."),
]

TEAM = [  # live About page
    ("Rushikesh Kate", "Founder & CEO", "https://www.linkedin.com/in/rushi-kate/"),
    ("Vipul Jadhav", "Vice President", ""),
    ("Madhukar Khare", "Creative Director", ""),
    ("Saud Pardesi", "Sr. Web Developer", ""),
    ("Maithili Jadhav", "Human Resource", ""),
]
