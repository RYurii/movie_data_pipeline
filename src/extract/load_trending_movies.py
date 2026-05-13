import json
import os
from datetime import datetime

import requests
from dotenv import load_dotenv

from src.utils.db import get_clickhouse_client


load_dotenv()

TMDB_API_READ_ACCESS_TOKEN = os.getenv("TMDB_API_READ_ACCESS_TOKEN")


def fetch_trending_movies(page=1):
    if not TMDB_API_READ_ACCESS_TOKEN:
        raise ValueError("TMDB_API_READ_ACCESS_TOKEN is missing in .env")

    url = "https://api.themoviedb.org/3/trending/movie/day"
    headers = {
        "Authorization": f"Bearer {TMDB_API_READ_ACCESS_TOKEN}",
        "Accept": "application/json",
    }
    params = {
        "language": "en-US",
        "page": page,
    }

    response = requests.get(url, headers=headers, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def parse_release_date(value):
    if not value:
        return None

    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def prepare_rows(payload, source, page):
    ingested_at = datetime.now()
    batch_date = ingested_at.date()
    rows = []

    movies = payload.get("results", [])

    for movie in movies:
        rows.append([
            ingested_at,
            batch_date,
            source,
            page,
            movie.get("id"),
            movie.get("title", ""),
            movie.get("original_title", ""),
            movie.get("original_language", ""),
            movie.get("overview", ""),
            parse_release_date(movie.get("release_date")),
            float(movie.get("popularity", 0.0)),
            float(movie.get("vote_average", 0.0)),
            int(movie.get("vote_count", 0)),
            1 if movie.get("adult", False) else 0,
            1 if movie.get("video", False) else 0,
            movie.get("genre_ids", []),
            movie.get("backdrop_path"),
            movie.get("poster_path"),
            json.dumps(movie, ensure_ascii=False),
        ])

    return rows


def insert_rows(rows):
    if not rows:
        print("No rows to insert")
        return

    client = get_clickhouse_client()

    client.insert(
        "movie_analytics.raw_tmdb_trending_movies",
        rows,
        column_names=[
            "ingested_at",
            "batch_date",
            "source",
            "page",
            "movie_id",
            "title",
            "original_title",
            "original_language",
            "overview",
            "release_date",
            "popularity",
            "vote_average",
            "vote_count",
            "adult",
            "video",
            "genre_ids",
            "backdrop_path",
            "poster_path",
            "raw_json",
        ],
    )

    print(f"Inserted {len(rows)} rows into raw_tmdb_trending_movies")


def main():
    source = "trending/movie/day"
    page = 1

    print("Fetching trending movies from TMDB...")
    payload = fetch_trending_movies(page)

    rows = prepare_rows(payload, source, page)

    print(f"Fetched {len(rows)} movies")

    if rows:
        print("First movie preview:")
        print(rows[0])

    insert_rows(rows)


if __name__ == "__main__":
    main()