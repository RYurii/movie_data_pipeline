import streamlit as st
import pandas as pd
import clickhouse_connect


st.set_page_config(
    page_title="Movie Analytics Dashboard",
    layout="wide",
)


def get_client():
    return clickhouse_connect.get_client(
        host="clickhouse",
        port=8123,
        username="admin",
        password="admin123",
        database="movie_analytics",
    )


@st.cache_data(ttl=300)
def load_query(query: str) -> pd.DataFrame:
    client = get_client()
    result = client.query(query)
    return pd.DataFrame(result.result_rows, columns=result.column_names)


st.title("Movie Analytics Dashboard")
st.caption("Analytics dashboard based on TMDB trending movies data")

top_movies = load_query("""
SELECT *
FROM mart_top_movies
ORDER BY popularity_rank ASC
""")

potential_movies = load_query("""
SELECT *
FROM mart_movie_potential
ORDER BY potential_score DESC
""")


total_movies = len(top_movies)
avg_popularity = round(top_movies["popularity"].mean(), 2)
avg_rating = round(top_movies["vote_average"].mean(), 2)
high_potential_count = len(
    potential_movies[potential_movies["potential_segment"] == "high_potential"]
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Movies", total_movies)
col2.metric("Avg popularity", avg_popularity)
col3.metric("Avg rating", avg_rating)
col4.metric("High potential", high_potential_count)


tab1, tab2 = st.tabs(["Top Movies", "Movie Potential"])


with tab1:
    st.subheader("Top Movies Mart")
    st.caption("Movies ranked by popularity and rating from the clean TMDB layer.")

    col1, col2 = st.columns([1, 1])

    with col1:
        language = st.selectbox(
            "Language",
            options=["All"] + sorted(top_movies["original_language"].unique().tolist()),
        )

    with col2:
        min_votes = st.slider(
            "Minimum vote count",
            min_value=0,
            max_value=int(top_movies["vote_count"].max()),
            value=0,
        )

    filtered_top = top_movies.copy()

    if language != "All":
        filtered_top = filtered_top[filtered_top["original_language"] == language]

    filtered_top = filtered_top[filtered_top["vote_count"] >= min_votes]

    st.bar_chart(
        filtered_top.set_index("title")["popularity"].head(10)
    )

    st.dataframe(
        filtered_top[
            [
                "title",
                "release_date",
                "original_language",
                "popularity",
                "vote_average",
                "vote_count",
                "popularity_rank",
                "rating_rank",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )


with tab2:
    st.subheader("Movie Potential Mart")
    st.caption("Rule-based scoring model for estimating movie potential.")

    segment = st.selectbox(
        "Potential segment",
        options=["All"] + sorted(potential_movies["potential_segment"].unique().tolist()),
    )

    filtered_potential = potential_movies.copy()

    if segment != "All":
        filtered_potential = filtered_potential[
            filtered_potential["potential_segment"] == segment
        ]

    st.bar_chart(
        filtered_potential.set_index("title")["potential_score"].head(10)
    )

    st.dataframe(
        filtered_potential[
            [
                "title",
                "release_date",
                "popularity",
                "vote_average",
                "vote_count",
                "days_since_release",
                "potential_score",
                "potential_segment",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )