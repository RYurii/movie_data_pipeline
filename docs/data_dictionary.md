# Data Dictionary

## Overview

This document describes the main tables, columns, and analytical logic used in the Movie Data Pipeline project.

---

# Raw Layer

## raw_tmdb_trending_movies

Stores raw movie data loaded directly from the TMDB API.

### Columns

| Column | Type | Description |
|---|---|---|
| ingested_at | DateTime | Timestamp when the record was ingested |
| batch_date | Date | Pipeline batch date |
| source | String | Source system name |
| page | UInt16 | TMDB API page number |
| movie_id | UInt32 | TMDB movie identifier |
| title | String | Movie title |
| original_title | String | Original movie title |
| original_language | String | Original movie language |
| overview | String | Movie overview |
| release_date | Nullable(Date) | Movie release date |
| popularity | Float64 | TMDB popularity metric |
| vote_average | Float64 | Average movie vote |
| vote_count | UInt32 | Number of votes |
| adult | UInt8 | Adult content flag |
| video | UInt8 | Video flag |
| genre_ids | Array(UInt32) | List of TMDB genre identifiers |
| backdrop_path | Nullable(String) | Movie backdrop image path |
| poster_path | Nullable(String) | Movie poster image path |
| raw_json | String | Original raw JSON payload |

### Raw Layer Responsibilities

- Store original API response data
- Preserve ingestion history
- Preserve original raw payloads
- Provide source data for clean transformations

---

# Clean Layer

## clean_tmdb_trending_movies

Stores cleaned and deduplicated movie data.

### Columns

| Column | Type | Description |
|---|---|---|
| batch_date | Date | Pipeline batch date |
| movie_id | UInt32 | TMDB movie identifier |
| title | String | Movie title |
| original_title | String | Original movie title |
| original_language | String | Original movie language |
| overview | String | Movie overview |
| release_date | Nullable(Date) | Movie release date |
| release_year | Nullable(UInt16) | Release year extracted from release_date |
| popularity | Float64 | TMDB popularity metric |
| vote_average | Float64 | Average movie vote |
| vote_count | UInt32 | Number of votes |
| adult | UInt8 | Adult content flag |
| video | UInt8 | Video flag |
| genre_ids | Array(UInt32) | List of TMDB genre identifiers |
| ingested_at | DateTime | Timestamp of selected latest raw record |

### Clean Layer Responsibilities

- Deduplication
- Data normalization
- Type standardization
- Preparation for marts
- Business-ready analytical base layer

---

# Mart Layer

## mart_top_movies

Analytical mart for top trending movies.

### Main Metrics

| Column | Description |
|---|---|
| movie_id | TMDB movie identifier |
| title | Movie title |
| release_date | Movie release date |
| original_language | Original movie language |
| popularity | TMDB popularity metric |
| vote_average | Average movie vote |
| vote_count | Number of votes |
| popularity_rank | Rank based on popularity |
| rating_rank | Rank based on rating |

### Mart Purpose

Provides ranked analytical view of trending movies based on popularity and rating metrics.

---

## mart_movie_potential

Analytical mart with custom rule-based movie potential scoring.

### Main Metrics

| Column | Description |
|---|---|
| movie_id | TMDB movie identifier |
| title | Movie title |
| release_date | Movie release date |
| popularity | TMDB popularity metric |
| vote_average | Average movie vote |
| vote_count | Number of votes |
| days_since_release | Number of days since release |
| potential_score | Custom weighted movie potential score |
| potential_segment | Rule-based movie potential segment |

---

### Potential Score Logic

`potential_score` is a custom rule-based metric used to estimate movie potential.

Formula:

```text
potential_score =
    popularity * 0.6
  + vote_average * 8
  + least(vote_count, 1000) * 0.03
  + freshness_bonus
```

### Formula Components

| Component | Description |
|---|---|
| popularity * 0.6 | Weight for TMDB popularity |
| vote_average * 8 | Weight for movie rating |
| least(vote_count, 1000) * 0.03 | Vote count contribution capped at 1000 votes |
| freshness_bonus | Additional score for recent releases |

### Freshness Bonus Logic

```text
If release_date >= today() - 90 days:
    freshness_bonus = 15
Else:
    freshness_bonus = 0
```

### Potential Segments

| Segment | Rule |
|---|---|
| high_potential | potential_score >= 90 |
| medium_potential | potential_score >= 60 and < 90 |
| low_potential | potential_score < 60 |

### Important Note

This mart uses a custom rule-based scoring model and does not represent a machine learning prediction system.

---

# Data Refresh

| Layer | Refresh Type |
|---|---|
| Raw | Daily ingestion |
| Clean | Daily refresh |
| Marts | Daily refresh |

---

# Source System

TMDB API is used as the primary data source for the project.

### Source Endpoint

```text
TMDB Trending Movies API
```

---

# Pipeline Architecture

```text
TMDB API
↓
raw_tmdb_trending_movies
↓
clean_tmdb_trending_movies
↓
mart_top_movies
mart_movie_potential
↓
Streamlit Dashboard
```