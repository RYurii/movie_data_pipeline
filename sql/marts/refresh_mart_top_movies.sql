TRUNCATE TABLE mart_top_movies;

INSERT INTO mart_top_movies
SELECT
    batch_date,
    movie_id,
    title,
    original_language,
    release_date,
    popularity,
    vote_average,
    vote_count,
    row_number() OVER (PARTITION BY batch_date ORDER BY popularity DESC) AS popularity_rank,
    row_number() OVER (PARTITION BY batch_date ORDER BY vote_average DESC, vote_count DESC) AS rating_rank
FROM clean_tmdb_trending_movies;