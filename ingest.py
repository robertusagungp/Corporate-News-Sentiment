import os
import re
import hashlib
from datetime import datetime, timezone

import feedparser

from db import get_conn

FEEDS = [
    {
        "source_name": "BBC World",
        "feed_url": "http://feeds.bbci.co.uk/news/world/rss.xml",
        "country": "International",
        "category": "General",
    },
    {
        "source_name": "Reuters World News",
        "feed_url": "https://feeds.reuters.com/Reuters/worldNews",
        "country": "International",
        "category": "General",
    },
    {
        "source_name": "CNBC World",
        "feed_url": "https://www.cnbc.com/id/100727362/device/rss/rss.html",
        "country": "International",
        "category": "Business",
    },
    {
        "source_name": "Kompas Nasional",
        "feed_url": "https://rss.kompas.com/rss/news",
        "country": "Indonesia",
        "category": "General",
    },
]

def clean_text(text: str | None) -> str:
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def ensure_source(cur, source):
    cur.execute(
        """
        INSERT INTO news_sources (source_name, feed_url, country, category, is_active)
        VALUES (%s, %s, %s, %s, TRUE)
        ON CONFLICT (feed_url)
        DO UPDATE SET
            source_name = EXCLUDED.source_name,
            country = EXCLUDED.country,
            category = EXCLUDED.category,
            is_active = TRUE
        RETURNING source_id
        """,
        (
            source["source_name"],
            source["feed_url"],
            source["country"],
            source["category"],
        ),
    )
    row = cur.fetchone()
    return row[0]

def parse_published(entry):
    if getattr(entry, "published_parsed", None):
        return datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
    if getattr(entry, "updated_parsed", None):
        return datetime(*entry.updated_parsed[:6], tzinfo=timezone.utc)
    return None

def insert_article(cur, source_id, entry):
    title = clean_text(getattr(entry, "title", ""))
    url = getattr(entry, "link", "").strip()
    summary = clean_text(getattr(entry, "summary", ""))
    author = clean_text(getattr(entry, "author", ""))
    published_at = parse_published(entry)
    language_code = None

    if not title or not url:
        return None

    content_hash = hash_text(f"{title}|{summary}")

    cur.execute(
        """
        INSERT INTO news_articles (
            source_id, title, url, summary, published_at,
            author, language_code, content_hash
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (url) DO NOTHING
        RETURNING article_id
        """,
        (
            source_id,
            title,
            url,
            summary,
            published_at,
            author,
            language_code,
            content_hash,
        ),
    )
    row = cur.fetchone()
    return row[0] if row else None

def match_watchlists(cur, article_id, title, summary):
    haystack = f"{title} {summary}".lower()

    cur.execute(
        """
        SELECT watchlist_id, company_name, keyword
        FROM watchlists
        WHERE is_active = TRUE
        """
    )
    rows = cur.fetchall()

    for watchlist_id, company_name, keyword in rows:
        kw = (keyword or "").strip().lower()
        if kw and kw in haystack:
            cur.execute(
                """
                INSERT INTO article_watchlist_hits (
                    article_id, watchlist_id, matched_keyword
                )
                VALUES (%s, %s, %s)
                ON CONFLICT (article_id, watchlist_id, matched_keyword) DO NOTHING
                """,
                (article_id, watchlist_id, keyword),
            )

def main():
    inserted = 0

    with get_conn() as conn:
        with conn.cursor() as cur:
            for source in FEEDS:
                source_id = ensure_source(cur, source)
                feed = feedparser.parse(source["feed_url"])

                for entry in feed.entries[:50]:
                    article_id = insert_article(cur, source_id, entry)
                    if article_id:
                        title = clean_text(getattr(entry, "title", ""))
                        summary = clean_text(getattr(entry, "summary", ""))
                        match_watchlists(cur, article_id, title, summary)
                        inserted += 1

    print(f"Inserted new articles: {inserted}")

if __name__ == "__main__":
    main()
