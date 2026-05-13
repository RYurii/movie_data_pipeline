# Data Dictionary

## Overview

This document describes the main tables and columns used in the Movie Data Pipeline project.

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

---

## mart_movie_potential

Analytical mart with custom movie potential scoring.

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

### Potential Segments

| Segment | Description |
|---|---|
| high_potential | High potential movie |
| medium_potential | Medium potential movie |
| low_potential | Low potential movie |

---

# Data Refresh

| Layer | Refresh Type |
|---|---|
| Raw | Daily |
| Clean | Daily refresh |
| Marts | Daily refresh |

---

# Source System

TMDB API is used as the primary data source for the project.