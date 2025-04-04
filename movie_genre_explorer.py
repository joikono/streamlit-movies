import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("🎬 Movie Genre Explorer")

# Load the movie data
movies_df = pd.read_csv("movies.csv")

# Extract unique genres
genres_list = movies_df["genres"].str.split("|", expand=True).stack().unique()

# Genre selector
selected_genre = st.selectbox("Select a genre", genres_list, index=0)

if selected_genre:
    # Filter by selected genre and sort
    filtered_df = movies_df[movies_df["genres"].str.contains(selected_genre, na=False)].copy()
    filtered_df["genres"] = selected_genre
    filtered_df.sort_values("movieId", inplace=True)

    # Show native dataframe with scroll INSIDE only
    st.markdown(f"### Movies in {selected_genre}")
    st.dataframe(filtered_df[["movieId","title", "genres"]], use_container_width=True, height=350)

# --- Genre Distribution Plot ---
st.markdown("### 🎥 Genre Distribution")

# Explode all genres for counting
all_genres = movies_df["genres"].dropna().str.split("|")
flat_genres = all_genres.explode()
genre_counts = flat_genres.value_counts().sort_values(ascending=False)

# Plot it
fig, ax = plt.subplots(figsize=(10, 4))
genre_counts.plot(kind="bar", ax=ax)
ax.set_title("Number of Movies per Genre")
ax.set_xlabel("Genre")
ax.set_ylabel("Count")
st.pyplot(fig)
