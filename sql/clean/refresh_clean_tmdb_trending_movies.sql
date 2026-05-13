TRUNCATE TABLE movie_analytics.clean_tmdb_trending_movies;

INSERT INTO movie_analytics.clean_tmdb_trending_movies
SELECT
    batch_date,
    movie_id,
    title,
    original_title,
    original_language,
    overview,
    release_date,
    release_year,
    popularity,
    vote_average,
    vote_count,
    adult,
    video,
    genre_ids,
    ingested_at
FROM
(
    SELECT
        batch_date,
        movie_id,
        title,
        original_title,
        original_language,
        overview,
        release_date,
        toYear(release_date) AS release_year,
        popularity,
        vote_average,
        vote_count,
        adult,
        video,
        genre_ids,
        ingested_at,
        row_number() OVER (
            PARTITION BY batch_date, movie_id
            ORDER BY ingested_at DESC
        ) AS rn
    FROM movie_analytics.raw_tmdb_trending_movies
)
WHERE rn = 1;