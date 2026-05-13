# Movie Data Pipeline

End-to-end Data Engineering project for loading TMDB trending movies data, transforming it through raw/clean/mart layers in ClickHouse, orchestrating pipelines with Airflow, and visualizing marts with Streamlit.

---

## Tech Stack

- Database: ClickHouse
- Orchestration: Apache Airflow
- Source: TMDB API
- Visualization: Streamlit
- Containerization: Docker Compose
- Language: Python

---

## Architecture

TMDB API  
→ Airflow DAGs  
→ ClickHouse Raw Layer  
→ ClickHouse Clean Layer  
→ ClickHouse Mart Layer  
→ Streamlit Dashboard

---

## Project Structure

```text
requirements.txt        Python libraries and dependencies
.env                    Environment variables and API credentials
docker-compose.yml      Docker services configuration

dags/                   Airflow DAG files
sql/                    SQL files for raw, clean, and mart layers
src/                    Python extraction logic and utility/helper modules
streamlit_app/          Streamlit dashboard application
```

---

## Layers

### Raw Layer

```text
raw_tmdb_trending_movies
```

Stores raw data loaded directly from the TMDB API.

Includes:
- original API fields
- ingestion metadata
- raw JSON payloads
- historical loads

---

### Clean Layer

```text
clean_tmdb_trending_movies
```

Cleaned and normalized data layer.

Responsibilities:
- deduplication
- normalization
- type preparation
- business-ready base dataset

---

### Mart Layer

#### `mart_top_movies`

Top trending movies mart based on popularity and rating metrics.

#### `mart_movie_potential`

Custom analytical mart with rule-based movie potential scoring and segmentation.

---

## Local URLs

### Airflow

```text
http://localhost:8080
```

Default credentials:

```text
admin / admin
```

---

### Streamlit Dashboard

```text
http://localhost:8501
```

---

## Setup Guide

### 1. Clone repository

```bash
git clone https://github.com/RYurii/movie_data_pipeline.git
cd movie_data_pipeline
```

---

### 2. Create environment file

Create `.env` file from `.env.example`:

```bash
cp .env.example .env
```

Add your TMDB credentials:

```env
TMDB_API_KEY=your_api_key
TMDB_READ_ACCESS_TOKEN=your_access_token
```

---

### 3. Start services

```bash
docker compose up -d
```

---

### 4. Run Airflow DAGs

First run infrastructure DAG:

```text
movie_analytics_setup
```

Then run daily pipeline DAG:

```text
movie_analytics_daily
```

---

## ClickHouse Access

Open ClickHouse client:

```bash
docker compose exec clickhouse clickhouse-client
```

Useful commands:

```sql
USE movie_analytics;

SHOW TABLES;

SELECT count() FROM raw_tmdb_trending_movies;
SELECT count() FROM clean_tmdb_trending_movies;
SELECT count() FROM mart_top_movies;
SELECT count() FROM mart_movie_potential;
```

---

## Current Features

- Dockerized local data platform
- Airflow orchestration
- TMDB API ingestion
- Raw/Clean/Mart architecture
- Deduplication logic
- ClickHouse analytical storage
- Streamlit dashboard visualization
- Custom movie scoring mart

---

## Future Improvements

- Add data quality checks and governance
- Add dbt testing and transformations
- Add CI/CD pipelines
- Deploy project to AWS cloud
- Add Kubernetes orchestration after AWS migration
- Improve Streamlit dashboard UX and analytics

---

## Notes

Stop services:

```bash
docker compose down
```

Reset all local data volumes:

```bash
docker compose down -v
```

Use `down -v` carefully because it removes:
- ClickHouse data
- Airflow metadata
- local persisted volumes