SELECT
    'raw table should not be empty' AS check_name,
    count() = 0 AS failed
FROM raw_tmdb_trending_movies

UNION ALL

SELECT
    'movie_id should not be 0' AS check_name,
    count() > 0 AS failed
FROM raw_tmdb_trending_movies
WHERE movie_id = 0

UNION ALL

SELECT
    'vote_average should be between 0 and 10' AS check_name,
    count() > 0 AS failed
FROM raw_tmdb_trending_movies
WHERE vote_average < 0
   OR vote_average > 10

UNION ALL

SELECT
    'vote_count should not be negative' AS check_name,
    count() > 0 AS failed
FROM raw_tmdb_trending_movies
WHERE vote_count < 0

UNION ALL

SELECT
    'popularity should not be negative' AS check_name,
    count() > 0 AS failed
FROM raw_tmdb_trending_movies
WHERE popularity < 0

UNION ALL

SELECT
    'release_date should not be in the future' AS check_name,
    count() > 0 AS failed
FROM raw_tmdb_trending_movies
WHERE release_date > addYears(today(), 3);