CREATE TABLE IF NOT EXISTS mart_top_movies
(
    batch_date Date,
    movie_id UInt32,
    title String,
    original_language String,
    release_date Nullable(Date),
    popularity Float64,
    vote_average Float64,
    vote_count UInt32,
    popularity_rank UInt32,
    rating_rank UInt32
)
ENGINE = MergeTree
ORDER BY (batch_date, popularity_rank, movie_id);