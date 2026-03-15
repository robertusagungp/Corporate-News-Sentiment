CREATE TABLE IF NOT EXISTS news_sources (
    source_id SERIAL PRIMARY KEY,
    source_name TEXT NOT NULL,
    feed_url TEXT NOT NULL UNIQUE,
    country TEXT,
    category TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS news_articles (
    article_id BIGSERIAL PRIMARY KEY,
    source_id INT NOT NULL REFERENCES news_sources(source_id),
    title TEXT NOT NULL,
    url TEXT NOT NULL UNIQUE,
    summary TEXT,
    published_at TIMESTAMP,
    author TEXT,
    language_code TEXT,
    content_hash TEXT,
    inserted_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_news_articles_published_at
    ON news_articles(published_at DESC);

CREATE INDEX IF NOT EXISTS idx_news_articles_source_id
    ON news_articles(source_id);

CREATE INDEX IF NOT EXISTS idx_news_articles_title
    ON news_articles USING GIN (to_tsvector('simple', coalesce(title, '')));

CREATE TABLE IF NOT EXISTS watchlists (
    watchlist_id BIGSERIAL PRIMARY KEY,
    company_name TEXT NOT NULL,
    keyword TEXT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_watchlists_keyword
    ON watchlists(keyword);

CREATE TABLE IF NOT EXISTS article_watchlist_hits (
    hit_id BIGSERIAL PRIMARY KEY,
    article_id BIGINT NOT NULL REFERENCES news_articles(article_id) ON DELETE CASCADE,
    watchlist_id BIGINT NOT NULL REFERENCES watchlists(watchlist_id) ON DELETE CASCADE,
    matched_keyword TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE(article_id, watchlist_id, matched_keyword)
);
