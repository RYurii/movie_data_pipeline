# Data Quality Checks

## Overview

This document describes data quality checks used in the Movie Data Pipeline project.

Data quality validation is executed as part of the Airflow daily pipeline.

If a validation check fails, the related Airflow task fails and the pipeline stops before continuing to downstream tasks.

---

## Raw Layer Checks

Validation file:

```text
sql/data_quality/validate_raw.sql
```

Target table:

```text
raw_tmdb_trending_movies
```

Checks:

- raw table should not be empty
- movie_id should not be 0
- vote_average should be between 0 and 10
- vote_count should not be negative
- popularity should not be negative
- release_date should not be more than 3 years in the future

---

## Clean Layer Checks

Validation file:

```text
sql/data_quality/validate_clean.sql
```

Target table:

```text
clean_tmdb_trending_movies
```

Checks:

- clean table should not be empty
- clean layer should not contain duplicates by batch_date and movie_id
- vote_average should be between 0 and 10
- title should not be empty
- release_year should match release_date
- popularity should not be negative
- vote_count should not be negative
- movie_id should not be 0

---

## Mart Layer Checks

Validation file:

```text
sql/data_quality/validate_marts.sql
```

Target tables:

```text
mart_top_movies
mart_movie_potential
```

Checks:

- mart_top_movies should not be empty
- mart_movie_potential should not be empty
- potential_score should not be negative
- potential_score should not be null
- potential_segment should not be empty
- potential_segment should be valid
- mart_top_movies row count should not exceed clean layer row count
- mart_movie_potential row count should not exceed clean layer row count

---

## Airflow Integration

Data quality checks are integrated into the Airflow DAG:

```text
load_raw
→ validate_raw
→ refresh_clean
→ validate_clean
→ refresh_marts
→ validate_marts
```

Validation failures stop the pipeline execution before downstream tasks continue.

---

## Validation Strategy

The project uses SQL-based validation checks.

Each validation query returns:

- check_name
- failed flag

Example:

```text
movie_id should not be 0 | 0
```

Where:

- `0` = check passed
- `1` = check failed

The Python validation runner reads the SQL results and raises an exception if any check fails.

---

## Future Improvements

Planned future improvements:

- dbt tests
- freshness checks
- anomaly detection
- schema validation
- automated alerting
- governance expansion