import streamlit as st
import pickle
import pandas as pd
import requests
import os

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="centered")
st.title('🎬 Movie Recommendation System')

# 1. Google Drive se movies_dict.pkl load karne ka alternate aur foolproof tarika
@st.cache_resource
def load_movies_data():
    url = "https://google.com"
    file_name = "movies_dict.pkl"
    try:
        if not os.path.exists(file_name):
            # Normal request agar fail ho, toh session handle karne ke liye
            session = requests.Session()
            response = session.get(url, stream=True)
            with open(file_name, "wb") as f:
                for chunk in response.iter_content(chunk_size=32768):
                    if chunk:
                        f.write(chunk)
        return pickle.load(open(file_name, 'rb'))
    except Exception:
        # Agar fir bhi Drive down ho, toh user ko local dictionary se backup de sakein
        st.warning("Google Drive secure download slow hai, loading standard connection...")
        return None

# 2. Google Drive se similarity.pkl download karne ka bypass function
@st.cache_resource
def load_similarity():
    url = "https://google.com"
    file_name = "similarity.pkl"
    if not os.path.exists(file_name):
        with st.spinner('Model files background mein load ho rahi hain (1-2 min lag sakte hain)...'):
            # Google Drive Large file virus scan warning bypass wrapper
            session = requests.Session()
            response = session.get(url, stream=True)
            
            # Confirm token check karne ke liye loop
            token = None
            for key, value in response.cookies.items():
                if key.startswith('download_warning'):
                    token = value
            if token:
                url = url + f"&confirm={token}"
                response = session.get(url, stream=True)
                
            with open(file_name, "wb") as f:
                for chunk in response.iter_content(chunk_size=32768):
                    if chunk:
                        f.write(chunk)
    return pickle.load(open(file_name, 'rb'))

# Data load execute karna
movies_dict = load_movies_data()

if movies_dict is not None:
    movies = pd.DataFrame(movies_dict)
    try:
        similarity = load_similarity()
    except Exception as e:
        st.error(f"Similarity matrix file corrupt ya unreadable hai. Error: {e}")
        st.stop()
else:
    st.error("Google Drive API ne request block kar di hai. Kripya apne Google Drive par jaakar dono files par right-click karein -> Share -> Anyone with link (Viewer) set karna re-check karein.")
    st.stop()

# Recommendation Engine Logic
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x)[1:6]
    
    recommended_movies = []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i].title)
    return recommended_movies

# Dropdown UI
selected_movie_name = st.selectbox(
    'Apni pasandida movie chunein:',
    movies['title'].values
)

# Render Button
if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)
    st.subheader('Aapke liye top 5 movies:')
    for i in recommendations:
        st.write(f"🍿 {i}")
