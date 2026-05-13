from pathlib import Path

from src.utils.db import get_clickhouse_client


PROJECT_ROOT = Path("/opt/airflow/project")


def run_data_quality_file(relative_path: str) -> None:
    file_path = PROJECT_ROOT / relative_path

    print(f"Running data quality checks from: {file_path}")

    sql_text = file_path.read_text(encoding="utf-8")

    client = get_clickhouse_client()
    result = client.query(sql_text)

    failed_checks = []

    for row in result.result_rows:
        check_name = row[0]
        failed = row[1]

        print(f"Check: {check_name} | Failed: {failed}")

        if failed:
            failed_checks.append(check_name)

    if failed_checks:
        raise ValueError(
            "Data quality checks failed: "
            + ", ".join(failed_checks)
        )

    print(f"All data quality checks passed from {file_path}")


def validate_raw_layer() -> None:
    run_data_quality_file(
        "sql/data_quality/validate_raw.sql"
    )


def validate_clean_layer() -> None:
    run_data_quality_file(
        "sql/data_quality/validate_clean.sql"
    )


def validate_mart_layer() -> None:
    run_data_quality_file(
        "sql/data_quality/validate_marts.sql"
    )