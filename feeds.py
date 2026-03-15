# feeds.py

"""
Indonesia-first feeds for corporate media monitoring MVP.

Notes:
- ANTARA feeds are from official RSS pages.
- CNA Indonesia is intentionally kept in OPTIONAL_FEEDS because its RSS page
  states personal/non-commercial usage.
- Start with CORE_FEEDS first. Add REGIONAL_FEEDS gradually after stable.
"""

CORE_FEEDS = [
    # ===== ANTARA NATIONAL =====
    {
        "source_name": "ANTARA Terkini",
        "feed_url": "https://www.antaranews.com/rss/terkini.xml",
        "country": "Indonesia",
        "category": "General",
        "priority": 1,
        "is_active": True,
    },
    {
        "source_name": "ANTARA Top News",
        "feed_url": "https://www.antaranews.com/rss/top-news.xml",
        "country": "Indonesia",
        "category": "General",
        "priority": 1,
        "is_active": True,
    },
    {
        "source_name": "ANTARA Politik",
        "feed_url": "https://www.antaranews.com/rss/politik.xml",
        "country": "Indonesia",
        "category": "Politics",
        "priority": 1,
        "is_active": True,
    },
    {
        "source_name": "ANTARA Hukum",
        "feed_url": "https://www.antaranews.com/rss/hukum.xml",
        "country": "Indonesia",
        "category": "Legal",
        "priority": 1,
        "is_active": True,
    },
    {
        "source_name": "ANTARA Ekonomi",
        "feed_url": "https://www.antaranews.com/rss/ekonomi.xml",
        "country": "Indonesia",
        "category": "Business",
        "priority": 1,
        "is_active": True,
    },
    {
        "source_name": "ANTARA Finansial",
        "feed_url": "https://www.antaranews.com/rss/ekonomi-finansial.xml",
        "country": "Indonesia",
        "category": "Finance",
        "priority": 1,
        "is_active": True,
    },
    {
        "source_name": "ANTARA Bisnis",
        "feed_url": "https://www.antaranews.com/rss/ekonomi-bisnis.xml",
        "country": "Indonesia",
        "category": "Business",
        "priority": 1,
        "is_active": True,
    },
    {
        "source_name": "ANTARA Bursa",
        "feed_url": "https://www.antaranews.com/rss/ekonomi-bursa.xml",
        "country": "Indonesia",
        "category": "Markets",
        "priority": 1,
        "is_active": True,
    },
    {
        "source_name": "ANTARA Metro",
        "feed_url": "https://www.antaranews.com/rss/metro.xml",
        "country": "Indonesia",
        "category": "Metro",
        "priority": 2,
        "is_active": True,
    },
    {
        "source_name": "ANTARA Humaniora",
        "feed_url": "https://www.antaranews.com/rss/humaniora.xml",
        "country": "Indonesia",
        "category": "Society",
        "priority": 2,
        "is_active": True,
    },
    {
        "source_name": "ANTARA Dunia",
        "feed_url": "https://www.antaranews.com/rss/dunia.xml",
        "country": "International",
        "category": "World",
        "priority": 2,
        "is_active": True,
    },
    {
        "source_name": "ANTARA Dunia ASEAN",
        "feed_url": "https://www.antaranews.com/rss/dunia-asean.xml",
        "country": "ASEAN",
        "category": "World",
        "priority": 2,
        "is_active": True,
    },
    {
        "source_name": "ANTARA Tekno",
        "feed_url": "https://www.antaranews.com/rss/tekno.xml",
        "country": "Indonesia",
        "category": "Technology",
        "priority": 2,
        "is_active": True,
    },
    {
        "source_name": "ANTARA Otomotif",
        "feed_url": "https://www.antaranews.com/rss/otomotif.xml",
        "country": "Indonesia",
        "category": "Automotive",
        "priority": 3,
        "is_active": True,
    },
    {
        "source_name": "ANTARA Warta Bumi",
        "feed_url": "https://www.antaranews.com/rss/warta-bumi.xml",
        "country": "Indonesia",
        "category": "Environment",
        "priority": 3,
        "is_active": True,
    },
    {
        "source_name": "ANTARA Rilis Pers",
        "feed_url": "https://www.antaranews.com/rss/rilis-pers.xml",
        "country": "Indonesia",
        "category": "Press Release",
        "priority": 4,
        "is_active": False,  # OFF by default to reduce PR/noise bias
    },
]

REGIONAL_FEEDS = [
    # ===== ANTARA REGIONAL - KALTENG =====
    {
        "source_name": "ANTARA Kalteng Terkini",
        "feed_url": "https://kalteng.antaranews.com/rss/terkini.xml",
        "country": "Indonesia",
        "category": "Regional",
        "priority": 3,
        "is_active": True,
    },
    {
        "source_name": "ANTARA Kalteng Top News",
        "feed_url": "https://kalteng.antaranews.com/rss/top-news.xml",
        "country": "Indonesia",
        "category": "Regional",
        "priority": 3,
        "is_active": True,
    },
    {
        "source_name": "ANTARA Kalteng Kabar Daerah",
        "feed_url": "https://kalteng.antaranews.com/rss/kabar-daerah.xml",
        "country": "Indonesia",
        "category": "Regional",
        "priority": 3,
        "is_active": True,
    },
    {
        "source_name": "ANTARA Kalteng Bisnis",
        "feed_url": "https://kalteng.antaranews.com/rss/bisnis.xml",
        "country": "Indonesia",
        "category": "Regional Business",
        "priority": 3,
        "is_active": True,
    },
    {
        "source_name": "ANTARA Kalteng Bisnis Umum",
        "feed_url": "https://kalteng.antaranews.com/rss/bisnis-umum.xml",
        "country": "Indonesia",
        "category": "Regional Business",
        "priority": 3,
        "is_active": True,
    },
    {
        "source_name": "ANTARA Kalteng Perkebunan",
        "feed_url": "https://kalteng.antaranews.com/rss/bisnis-perkebunan.xml",
        "country": "Indonesia",
        "category": "Plantation",
        "priority": 4,
        "is_active": True,
    },
    {
        "source_name": "ANTARA Kalteng Pertambangan",
        "feed_url": "https://kalteng.antaranews.com/rss/bisnis-pertambangan.xml",
        "country": "Indonesia",
        "category": "Mining",
        "priority": 4,
        "is_active": True,
    },
    {
        "source_name": "ANTARA Kalteng Internasional",
        "feed_url": "https://kalteng.antaranews.com/rss/internasional.xml",
        "country": "International",
        "category": "World",
        "priority": 4,
        "is_active": False,
    },
]

OPTIONAL_FEEDS = [
    # ===== CNA INDONESIA =====
    # Keep optional until legal/terms are cleared for commercial use.
    {
        "source_name": "CNA Indonesia Latest",
        "feed_url": "https://www.cna.id/api/v1/rss-outbound-feed?_format=xml",
        "country": "Indonesia",
        "category": "General",
        "priority": 5,
        "is_active": False,
    },
    {
        "source_name": "CNA Indonesia Bisnis",
        "feed_url": "https://www.cna.id/api/v1/rss-outbound-feed?_format=xml&category=3321",
        "country": "Indonesia",
        "category": "Business",
        "priority": 5,
        "is_active": False,
    },
    {
        "source_name": "CNA Indonesia Asia",
        "feed_url": "https://www.cna.id/api/v1/rss-outbound-feed?_format=xml&category=3346",
        "country": "Asia",
        "category": "Asia",
        "priority": 5,
        "is_active": False,
    },
    {
        "source_name": "CNA Indonesia Dunia",
        "feed_url": "https://www.cna.id/api/v1/rss-outbound-feed?_format=xml&category=3136",
        "country": "International",
        "category": "World",
        "priority": 5,
        "is_active": False,
    },
]

FEEDS = CORE_FEEDS + REGIONAL_FEEDS
