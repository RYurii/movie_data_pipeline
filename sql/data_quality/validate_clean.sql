SELECT
    'clean table should not be empty' AS check_name,
    count() = 0 AS failed
FROM clean_tmdb_trending_movies

UNION ALL

SELECT
    'clean layer contains duplicates' AS check_name,
    count() > 0 AS failed
FROM
(
    SELECT batch_date, movie_id, count() AS cnt
    FROM clean_tmdb_trending_movies
    GROUP BY batch_date, movie_id
    HAVING cnt > 1
)

UNION ALL

SELECT
    'vote_average out of range' AS check_name,
    count() > 0 AS failed
FROM clean_tmdb_trending_movies
WHERE vote_average < 0
   OR vote_average > 10

UNION ALL

SELECT
    'clean title should not be empty' AS check_name,
    count() > 0 AS failed
FROM clean_tmdb_trending_movies
WHERE title = ''

UNION ALL

SELECT
    'release_year should match release_date' AS check_name,
    count() > 0 AS failed
FROM clean_tmdb_trending_movies
WHERE release_date IS NOT NULL
  AND release_year != toYear(release_date)

UNION ALL

SELECT
    'popularity should not be negative' AS check_name,
    count() > 0 AS failed
FROM clean_tmdb_trending_movies
WHERE popularity < 0

UNION ALL

SELECT
    'vote_count should not be negative' AS check_name,
    count() > 0 AS failed
FROM clean_tmdb_trending_movies
WHERE vote_count < 0

UNION ALL

SELECT
    'movie_id should not be 0' AS check_name,
    count() > 0 AS failed
FROM clean_tmdb_trending_movies
WHERE movie_id = 0;