import streamlit as st
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="centered")
st.title('🎬 Movie Recommendation System')

# 1. GitHub repository se movie_dict.pkl load karna
@st.cache_resource
def load_movies_data():
    file_name = "movie_dict.pkl"
    if os.path.exists(file_name):
        return pickle.load(open(file_name, 'rb'))
    else:
        st.error("File 'movie_dict.pkl' not found on GitHub. Please check the file name.")
        st.stop()

# Execute data loading
movies_dict = load_movies_data()
movies = pd.DataFrame(movies_dict)

# 2. Similarity matrix ko direct website par calculate karne ka function (No Google Drive Needed)
@st.cache_resource
def compute_similarity(df):
    with st.spinner('Initializing recommendation engine... Please wait a moment.'):
        # Agar aapne tags ke alawa overview ya genres use kiya hai, toh code khud handle kar lega
        text_column = 'tags' if 'tags' in df.columns else ('overview' if 'overview' in df.columns else 'genres')
        
        # Missing values ko fill karna
        df[text_column] = df[text_column].fillna('')
        
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(df[text_column])
        return cosine_similarity(tfidf_matrix, tfidf_matrix)

similarity = compute_similarity(movies)

# Movie Recommendation Logic
def recommend(movie):
    try:
        movie_index = movies[movies['title'] == movie].index
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x)[1:6]
        
        recommended_movies = []
        for i in movies_list:
            recommended_movies.append(movies.iloc[i]['title'])
        return recommended_movies
    except Exception as e:
        return ["Error calculating recommendation or movie title mismatch."]

# Dropdown UI
selected_movie_name = st.selectbox(
    'Select a movie you like:',
    movies['title'].values
)

# Render Button
if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)
    st.subheader('Top 5 recommended movies for you:')
    for i in recommendations:
        st.write(f"🍿 {i}")
