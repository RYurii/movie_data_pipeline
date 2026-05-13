from pathlib import Path

from src.utils.db import get_clickhouse_client


PROJECT_ROOT = Path("/opt/airflow/project")


def split_sql_statements(sql_text: str) -> list[str]:
    parts = sql_text.split(";")
    statements = []

    for part in parts:
        statement = part.strip()
        if statement:
            statements.append(statement)

    return statements


def run_sql_file(relative_path: str) -> None:
    file_path = PROJECT_ROOT / relative_path
    sql_text = file_path.read_text(encoding="utf-8")
    statements = split_sql_statements(sql_text)

    if not statements:
        print(f"No SQL statements found in {file_path}")
        return

    client = get_clickhouse_client()

    print(f"Running {len(statements)} statement(s) from {file_path}")

    for i, statement in enumerate(statements, start=1):
        print(f"Running statement {i}/{len(statements)}")
        client.command(statement)

    print(f"Finished: {file_path}")