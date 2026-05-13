# Data Lineage

## Overview

This document describes the data flow in the Movie Data Pipeline project.

## Lineage

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

## Source

### TMDB API

The source system is TMDB API.  
The pipeline loads trending movies data from the daily trending endpoint.

## Raw Layer

### raw_tmdb_trending_movies

Stores raw API data with ingestion metadata and original JSON payload.

## Clean Layer

### clean_tmdb_trending_movies

Stores deduplicated and normalized movie data.

## Mart Layer

### mart_top_movies

Analytical mart for top trending movies.

### mart_movie_potential

Analytical mart with rule-based movie potential scoring.

## Dashboard Layer

### Streamlit

Streamlit reads mart tables from ClickHouse and visualizes the data.