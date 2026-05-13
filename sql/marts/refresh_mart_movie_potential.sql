TRUNCATE TABLE movie_analytics.mart_movie_potential;

INSERT INTO movie_analytics.mart_movie_potential
SELECT
    batch_date AS snapshot_date,
    movie_id,
    title,
    release_date,
    popularity,
    vote_average,
    vote_count,
    if(release_date IS NULL, NULL, dateDiff('day', release_date, today())) AS days_since_release,

    round(
        popularity * 0.6
        + vote_average * 8
        + least(vote_count, 1000) * 0.03
        + if(release_date IS NOT NULL AND release_date >= today() - 90, 15, 0),
        2
    ) AS potential_score,

    multiIf(
        round(
            popularity * 0.6
            + vote_average * 8
            + least(vote_count, 1000) * 0.03
            + if(release_date IS NOT NULL AND release_date >= today() - 90, 15, 0),
            2
        ) >= 90, 'high_potential',

        round(
            popularity * 0.6
            + vote_average * 8
            + least(vote_count, 1000) * 0.03
            + if(release_date IS NOT NULL AND release_date >= today() - 90, 15, 0),
            2
        ) >= 60, 'medium_potential',

        'low_potential'
    ) AS potential_segment

FROM movie_analytics.clean_tmdb_trending_movies;