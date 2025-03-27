import streamlit as st
import pickle
import pandas as pd
import requests

# Load the movie data
movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

# Ensure 'id' column exists
if 'id' not in movies.columns:
    st.error("Error: 'id' column is missing in movies dataset.")
    st.stop()

movies_list = movies['title'].values
st.header("Movie Recommendation System")
selectvalue = st.selectbox("Select from the drop-down", movies_list)

# Function to fetch poster safely
def fetch_poster(movie_id):
    try:
        api_key = "52fd9301f89c052d62416c6b80d4c0f6"
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
        response = requests.get(url)

        if response.status_code != 200:
            return "https://via.placeholder.com/150"  # Default image

        data = response.json()
        poster_path = data.get("poster_path")
        return f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "https://via.placeholder.com/150"

    except Exception as e:
        st.error(f"Error fetching poster: {e}")
        return "https://via.placeholder.com/150"

# Function to recommend movies safely
def recommend(movie_name):
    try:
        index = movies[movies['title'] == movie_name].index[0]
    except IndexError:
        st.error(f"Error: '{movie_name}' not found in dataset.")
        return [], []
    
    distances = sorted(enumerate(similarity[index]), reverse=True, key=lambda x: x[1])
    
    recommended_movies = []
    recommended_posters = []

    for i in distances[1:6]:  # Top 5 recommendations
        try:
            movie_id = movies.iloc[i[0]]['id']
            recommended_movies.append(movies.iloc[i[0]]['title'])
            recommended_posters.append(fetch_poster(movie_id))
        except Exception as e:
            st.error(f"Error fetching movie details: {e}")
    
    return recommended_movies, recommended_posters

# Initialize session state
if "recommendation_clicked" not in st.session_state:
    st.session_state.recommendation_clicked = False

# Recommend movies on button click
if st.button("Recommend"):
    st.session_state.recommendation_clicked = True

if st.session_state.recommendation_clicked:
    recommended_movies, recommended_posters = recommend(selectvalue)
    
    if recommended_movies:
        cols = st.columns(5)
        for i, col in enumerate(cols):
            with col:
                st.text(recommended_movies[i])
                st.image(recommended_posters[i])

# Reset button - Proper Fix
if st.button("Reset"):
    st.session_state.recommendation_clicked = False  # Reset only the recommendation state
    st.session_state.clear()  # Clear all session states
    st.session_state.clear()  # Ensures UI updates (Alternative: refresh manually)








  