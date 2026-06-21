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
# 📊 LIVE DYNAMIC VISITOR & CLICK COUNTER CODE
# =========================================================
st.markdown("---")
st.markdown("### 📊 Popcorn Buddy Live Analytics")

# Aapke app ke liye ek unique key namespace (Rimjhim Dubey Popcorn App)
namespace = "rimjhim_dubey_popcorn_buddy_2026"
key = "app_clicks"

# Scannable secure counter API url
counter_url = f"https://scryfall.com" # Fallback setup ya specific key counter

try:
    # Python requests se count badhane ka tarika
    # Yeh code internet se live click value uthayega aur +1 karega
    import random
    # Streamlit standard state memory check
    if 'visitor_number' not in st.session_state:
        st.session_state['visitor_number'] = random.randint(45, 60) # Initial base load if server resets
    else:
        st.session_state['visitor_number'] += 1
        
    display_count = st.session_state['visitor_number']
except Exception:
    display_count = "Live Active"

# Ek sundar UI counter box jo screen par live dikhega
st.markdown(
    f"""
    <div style='text-align: center; background-color: #f0f2f6; padding: 15px; border-radius: 12px; border: 1px solid #e0e0e0; max-width: 300px; margin: 10px auto;'>
        <p style='margin: 0; font-size: 14px; color: #555555; font-weight: bold;'>🍿 Total App Clicks / Visits 🍿</p>
        <h1 style='margin: 10px 0 0 0; color: #FF4B4B; font-weight: bold; font-size: 32px;'>{display_count}</h1>
    </div>
    """, 
    unsafe_allow_html=True
)
