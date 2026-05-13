from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from src.utils.create_tables import (
    create_clean_table,
    create_mart_movie_potential_table,
    create_mart_table,
    create_raw_table,
)


with DAG(
    dag_id="movie_analytics_setup",
    start_date=datetime(2026, 3, 20),
    schedule=None,
    catchup=False,
    tags=["movies", "setup", "clickhouse"],
) as dag:

    create_raw = PythonOperator(
        task_id="create_raw_table",
        python_callable=create_raw_table,
    )

    create_clean = PythonOperator(
        task_id="create_clean_table",
        python_callable=create_clean_table,
    )

    create_mart = PythonOperator(
        task_id="create_mart_table",
        python_callable=create_mart_table,
    )

    create_mart_movie_potential = PythonOperator(
        task_id="create_mart_movie_potential_table",
        python_callable=create_mart_movie_potential_table,
    )

    create_raw >> create_clean >> [create_mart, create_mart_movie_potential]