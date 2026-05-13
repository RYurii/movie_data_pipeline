from src.utils.sql_runner import run_sql_file


def create_raw_table() -> None:
    run_sql_file("sql/raw/create_raw_tmdb_trending_movies.sql")


def create_clean_table() -> None:
    run_sql_file("sql/clean/create_clean_tmdb_trending_movies.sql")


def create_mart_table() -> None:
    run_sql_file("sql/marts/create_mart_top_movies.sql")


def create_mart_movie_potential_table() -> None:
    run_sql_file("sql/marts/create_mart_movie_potential.sql")