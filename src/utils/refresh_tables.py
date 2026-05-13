from src.utils.sql_runner import run_sql_file


def refresh_clean_table() -> None:
    run_sql_file("sql/clean/refresh_clean_tmdb_trending_movies.sql")


def refresh_mart_table() -> None:
    run_sql_file("sql/marts/refresh_mart_top_movies.sql")


def refresh_mart_movie_potential_table() -> None:
    run_sql_file("sql/marts/refresh_mart_movie_potential.sql")