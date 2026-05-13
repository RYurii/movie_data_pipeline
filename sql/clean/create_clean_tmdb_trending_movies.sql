CREATE TABLE IF NOT EXISTS clean_tmdb_trending_movies
(
    batch_date Date,
    movie_id UInt32,
    title String,
    original_title String,
    original_language String,
    overview String,
    release_date Nullable(Date),
    release_year Nullable(UInt16),
    popularity Float64,
    vote_average Float64,
    vote_count UInt32,
    adult UInt8,
    video UInt8,
    genre_ids Array(UInt32),
    ingested_at DateTime
)
ENGINE = MergeTree
ORDER BY (batch_date, movie_id);