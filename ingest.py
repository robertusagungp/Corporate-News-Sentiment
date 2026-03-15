# ingest.py

import hashlib
import logging
import os
import re
import socket
from datetime import datetime, timezone
from typing import Optional

import feedparser

from db import get_conn
from feeds import FEEDS

# Avoid hanging too long on slow feeds
socket.setdefaulttimeout(20)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)


def clean_text(text: Optional[str]) -> str:
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def normalize_url(url: str) -> str:
    url = (url or "").strip()
    # remove common tracking params if needed later
    return url


def hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def parse_published(entry) -> Optional[datetime]:
    if getattr(entry, "published_parsed", None):
        return datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
    if getattr(entry, "updated_parsed", None):
        return datetime(*entry.updated_parsed[:6], tzinfo=timezone.utc)
    return None


def ensure_source(cur, source: dict) -> int:
    cur.execute(
        """
        INSERT INTO news_sources (source_name, feed_url, country, category, is_active)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (feed_url)
        DO UPDATE SET
            source_name = EXCLUDED.source_name,
            country = EXCLUDED.country,
            category = EXCLUDED.category,
            is_active = EXCLUDED.is_active
        RETURNING source_id
        """,
        (
            source["source_name"],
            source["feed_url"],
            source["country"],
            source["category"],
            source.get("is_active", True),
        ),
    )
    row = cur.fetchone()
    return row[0]


def article_already_exists_by_hash(cur, content_hash: str) -> bool:
    cur.execute(
        """
        SELECT 1
        FROM news_articles
        WHERE content_hash = %s
        LIMIT 1
        """,
        (content_hash,),
    )
    return cur.fetchone() is not None


def insert_article(cur, source_id: int, entry) -> Optional[int]:
    title = clean_text(getattr(entry, "title", ""))
    url = normalize_url(getattr(entry, "link", ""))
    summary = clean_text(getattr(entry, "summary", ""))
    author = clean_text(getattr(entry, "author", ""))
    published_at = parse_published(entry)
    language_code = None

    if not title or not url:
        return None

    content_hash = hash_text(f"{title}|{summary}")

    # soft dedup by hash before insert
    if article_already_exists_by_hash(cur, content_hash):
        return None

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


def match_watchlists(cur, article_id: int, title: str, summary: str) -> int:
    haystack = f"{title} {summary}".lower()
    total_hits = 0

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
        if not kw:
            continue

        # simple contains for MVP
        if kw in haystack:
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
            total_hits += 1

    return total_hits


def ingest_one_feed(cur, source: dict) -> dict:
    source_name = source["source_name"]
    feed_url = source["feed_url"]

    result = {
        "source_name": source_name,
        "feed_url": feed_url,
        "entries_seen": 0,
        "articles_inserted": 0,
        "watchlist_hits": 0,
        "status": "ok",
        "error": None,
    }

    try:
        source_id = ensure_source(cur, source)
        parsed = feedparser.parse(feed_url)

        if getattr(parsed, "bozo", 0):
            # bozo means feedparser detected malformed feed, but some entries may still be usable
            logger.warning("Feed issue detected: %s | bozo_exception=%s", source_name, getattr(parsed, "bozo_exception", None))

        entries = getattr(parsed, "entries", []) or []
        result["entries_seen"] = len(entries)

        for entry in entries[:50]:
            article_id = insert_article(cur, source_id, entry)
            if article_id:
                title = clean_text(getattr(entry, "title", ""))
                summary = clean_text(getattr(entry, "summary", ""))
                hits = match_watchlists(cur, article_id, title, summary)

                result["articles_inserted"] += 1
                result["watchlist_hits"] += hits

        logger.info(
            "DONE | %s | seen=%s inserted=%s hits=%s",
            source_name,
            result["entries_seen"],
            result["articles_inserted"],
            result["watchlist_hits"],
        )
        return result

    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
        logger.exception("FAILED | %s | %s", source_name, e)
        return result


def main():
    logger.info("Starting ingestion for %s feeds", len(FEEDS))

    all_results = []
    total_inserted = 0
    total_hits = 0

    with get_conn() as conn:
        with conn.cursor() as cur:
            for source in FEEDS:
                if not source.get("is_active", True):
                    logger.info("SKIP | inactive feed | %s", source["source_name"])
                    continue

                result = ingest_one_feed(cur, source)
                all_results.append(result)
                total_inserted += result["articles_inserted"]
                total_hits += result["watchlist_hits"]

    success_count = sum(1 for r in all_results if r["status"] == "ok")
    error_count = sum(1 for r in all_results if r["status"] == "error")

    logger.info("SUMMARY | feeds_ok=%s feeds_error=%s inserted=%s hits=%s",
                success_count, error_count, total_inserted, total_hits)

    # Fail the workflow only if every feed failed
    if all_results and success_count == 0:
        raise RuntimeError("All feeds failed. Check source availability or connection.")

    print(f"Inserted new articles: {total_inserted}")
    print(f"Watchlist hits: {total_hits}")
    print(f"Feeds OK: {success_count}, Feeds Error: {error_count}")


if __name__ == "__main__":
    main()
