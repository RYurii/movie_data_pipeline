from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from src.extract.load_trending_movies import main as load_trending_movies_main
from src.utils.sql_runner import run_sql_file


def refresh_clean_table():
    run_sql_file("sql/clean/refresh_clean_tmdb_trending_movies.sql")


def refresh_mart_table():
    run_sql_file("sql/marts/refresh_mart_top_movies.sql")


def refresh_mart_movie_potential_table():
    run_sql_file("sql/marts/refresh_mart_movie_potential.sql")


with DAG(
    dag_id="movie_analytics_daily",
    start_date=datetime(2026, 3, 20),
    schedule="@daily",
    catchup=False,
    tags=["movies", "daily", "clickhouse"],
) as dag:

    load_raw = PythonOperator(
        task_id="load_trending_movies_to_raw",
        python_callable=load_trending_movies_main,
    )

    refresh_clean = PythonOperator(
        task_id="refresh_clean_table",
        python_callable=refresh_clean_table,
    )

    refresh_mart = PythonOperator(
        task_id="refresh_mart_table",
        python_callable=refresh_mart_table,
    )

    refresh_mart_movie_potential = PythonOperator(
        task_id="refresh_mart_movie_potential_table",
        python_callable=refresh_mart_movie_potential_table,
    )

    load_raw >> refresh_clean >> [refresh_mart, refresh_mart_movie_potential]