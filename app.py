import os
import pandas as pd
import streamlit as st
import psycopg

st.set_page_config(page_title="B2B Media Monitoring", layout="wide")

DATABASE_URL = st.secrets["DATABASE_URL"] if "DATABASE_URL" in st.secrets else os.getenv("DATABASE_URL")

@st.cache_resource
def get_conn():
    return psycopg.connect(DATABASE_URL)

def load_latest_articles(limit=100):
    conn = get_conn()
    query = """
        SELECT
            a.article_id,
            s.source_name,
            a.title,
            a.url,
            a.summary,
            a.published_at,
            a.inserted_at
        FROM news_articles a
        JOIN news_sources s
          ON a.source_id = s.source_id
        ORDER BY COALESCE(a.published_at, a.inserted_at) DESC
        LIMIT %s
    """
    return pd.read_sql(query, conn, params=(limit,))

def load_hits():
    conn = get_conn()
    query = """
        SELECT
            w.company_name,
            w.keyword,
            a.title,
            a.url,
            a.published_at,
            s.source_name
        FROM article_watchlist_hits h
        JOIN watchlists w
          ON h.watchlist_id = w.watchlist_id
        JOIN news_articles a
          ON h.article_id = a.article_id
        JOIN news_sources s
          ON a.source_id = s.source_id
        ORDER BY COALESCE(a.published_at, a.inserted_at) DESC
        LIMIT 200
    """
    return pd.read_sql(query, conn)

def add_watchlist(company_name, keyword):
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO watchlists (company_name, keyword, is_active)
            VALUES (%s, %s, TRUE)
            """,
            (company_name, keyword),
        )
        conn.commit()

st.title("B2B Media Monitoring SaaS MVP")

tab1, tab2, tab3 = st.tabs(["Latest News", "Watchlist Hits", "Add Watchlist"])

with tab1:
    st.subheader("Latest News")
    df = load_latest_articles()
    search = st.text_input("Search title")
    if search:
        df = df[df["title"].str.contains(search, case=False, na=False)]
    st.dataframe(df, use_container_width=True)

with tab2:
    st.subheader("Watchlist Hits")
    hits = load_hits()
    st.dataframe(hits, use_container_width=True)

with tab3:
    st.subheader("Add Watchlist")
    with st.form("watchlist_form"):
        company_name = st.text_input("Company Name")
        keyword = st.text_input("Keyword")
        submitted = st.form_submit_button("Save")
        if submitted:
            if company_name.strip() and keyword.strip():
                add_watchlist(company_name.strip(), keyword.strip())
                st.success("Watchlist saved")
            else:
                st.error("Company Name and Keyword are required")
