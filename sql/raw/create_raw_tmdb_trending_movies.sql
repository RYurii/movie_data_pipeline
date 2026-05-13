CREATE TABLE IF NOT EXISTS raw_tmdb_trending_movies
(
    ingested_at DateTime,
    batch_date Date,
    source String,
    page UInt16,
    movie_id UInt32,
    title String,
    original_title String,
    original_language String,
    overview String,
    release_date Nullable(Date),
    popularity Float64,
    vote_average Float64,
    vote_count UInt32,
    adult UInt8,
    video UInt8,
    genre_ids Array(UInt32),
    backdrop_path Nullable(String),
    poster_path Nullable(String),
    raw_json String
)
ENGINE = MergeTree
ORDER BY (batch_date, movie_id, ingested_at);