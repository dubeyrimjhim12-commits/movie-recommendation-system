import streamlit as st
st.set_page_config(
    page_title="Popcorn Buddy | Movie Recommendation System by Rimjhim Dubey",
    page_icon="🍿"
)

import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="centered")
st.title('🎬 Movie Recommendation System')

# 1. Load movies data from GitHub repository
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

# 2. Extract column features dynamically to build similarity matrix
@st.cache_resource
def compute_similarity(df):
    # This automatically finds text/tag fields to compute algorithm matches safely
    text_features = []
    for col in ['tags', 'overview', 'genres', 'keywords']:
        if col in df.columns:
            text_features.append(col)
            
    if text_features:
        # Combine available text attributes to maintain high-quality results
        combined_text = df[text_features].astype(str).agg(' '.join, axis=1)
    else:
        # Fallback to absolute clean layout if structure differs
        combined_text = df.astype(str).agg(' '.join, axis=1)
        
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(combined_text)
    return cosine_similarity(tfidf_matrix, tfidf_matrix)

similarity = compute_similarity(movies)

# Movie Recommendation Engine Logic
def recommend(movie):
    try:
        # Matching title casing explicitly to avoid array index failures
        movie_index = movies[movies['title'].str.lower() == movie.lower()].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        
        recommended_movies = []
        for i in movies_list:
            recommended_movies.append(movies.iloc[i['index'] if 'index' in movies.columns else i[0]]['title'])
        return recommended_movies
    except Exception as e:
        return [f"No recommendations found or dataframe parsing error. Details: {e}"]

# Dropdown UI
selected_movie_name = st.selectbox(
    'Select a movie you like:',
    movies['title'].values
)

# Render Button
if st.button('Recommend'):
    with st.spinner('Generating matching recommendations...'):
        recommendations = recommend(selected_movie_name)
        st.subheader('Top 5 recommended movies for you:')
        for i in recommendations:
            st.write(f"🍿 {i}")
# =========================================================
# DEVELOPER CREDITS (Is code ko file ke sabse niche paste karein)
# =========================================================
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; padding: 10px;'>
        <p style='color: #888888; font-size: 16px; margin-bottom: 5px;'>
            🍿 <b>Popcorn Buddy</b> © 2026
        </p>
        <p style='color: #555555; font-size: 14px;'>
            Designed & Developed with ❤️ by 
            <span style='color: #FF4B4B; font-weight: bold; font-size: 16px;'>Rimjhim Dubey</span>
        </p>
    </div>
    """, 
    unsafe_allow_html=True
)
import streamlit as st
import requests

# =========================================================
# 🕵️‍♂️ COMPLETELY HIDDEN COUNTER (Normal user ko kuch nahi dikhega)
# =========================================================

# Background mein clicks track karne ka URL (Chupchaap kaam karega)
app_id = "rimjhim_dubey_popcorn_2026"
global_url = f"https://moostrap.com{app_id}/clicks"

try:
    response = requests.get(global_url).json()
    global_clicks = response.get("w_hits", "0")
except Exception:
    global_clicks = "Live"

# Streamlit ke query parameters check karna (URL check karega)
query_params = st.query_params

# 🚨 Agar URL mein '?show=rimjhim' likha hoga, tabhi counter dikhega
if query_params.get("show") == "rimjhim":
    st.markdown("---")
    st.markdown(
        f"""
        <div style='text-align: center; background-color: #262730; padding: 15px; border-radius: 12px; border: 1px solid #444; max-width: 280px; margin: 10px auto;'>
            <p style='margin: 0; font-size: 14px; color: #aaaaaa; font-weight: bold;'>🍿 Total Live App Clicks 🍿</p>
            <h1 style='margin: 10px 0 0 0; color: #FF4B4B; font-weight: bold; font-size: 36px;'>{global_clicks}</h1>
        </div>
        """, 
        unsafe_allow_html=True
    )

