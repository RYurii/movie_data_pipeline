SELECT
    'mart_top_movies should not be empty' AS check_name,
    count() = 0 AS failed
FROM mart_top_movies

UNION ALL

SELECT
    'mart_movie_potential should not be empty' AS check_name,
    count() = 0 AS failed
FROM mart_movie_potential

UNION ALL

SELECT
    'potential_score should not be negative' AS check_name,
    count() > 0 AS failed
FROM mart_movie_potential
WHERE potential_score < 0

UNION ALL

SELECT
    'potential_score should not be null' AS check_name,
    count() > 0 AS failed
FROM mart_movie_potential
WHERE potential_score IS NULL

UNION ALL

SELECT
    'potential_segment should not be empty' AS check_name,
    count() > 0 AS failed
FROM mart_movie_potential
WHERE potential_segment = ''

UNION ALL

SELECT
    'potential_segment should be valid' AS check_name,
    count() > 0 AS failed
FROM mart_movie_potential
WHERE potential_segment NOT IN
(
    'high_potential',
    'medium_potential',
    'low_potential'
)

UNION ALL

SELECT
    'mart_top_movies row count should not exceed clean layer row count' AS check_name,
    (
        SELECT count()
        FROM mart_top_movies
    ) >
    (
        SELECT count()
        FROM clean_tmdb_trending_movies
    ) AS failed

UNION ALL

SELECT
    'mart_movie_potential row count should not exceed clean layer row count' AS check_name,
    (
        SELECT count()
        FROM mart_movie_potential
    ) >
    (
        SELECT count()
        FROM clean_tmdb_trending_movies
    ) AS failed;