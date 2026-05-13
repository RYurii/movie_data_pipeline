CREATE TABLE IF NOT EXISTS movie_analytics.mart_movie_potential
(
    snapshot_date Date,
    movie_id UInt32,
    title String,
    release_date Nullable(Date),
    popularity Float64,
    vote_average Float64,
    vote_count UInt32,
    days_since_release Nullable(Int32),
    potential_score Float64,
    potential_segment String
)
ENGINE = MergeTree
ORDER BY (snapshot_date, potential_score, movie_id);