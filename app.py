import streamlit as st
import pickle
import pandas as pd
import requests
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

# 2. Download similarity matrix from Google Drive with verification bypass
@st.cache_resource
def load_similarity():
    file_id = "1Q7WFmIp8f_X_hhcrVkVTYuuOTIwpf4KN"
    file_name = "similarity.pkl"
    
    if not os.path.exists(file_name):
        with st.spinner('Loading model files from cloud, please wait (Takes 1-2 mins)...'):
            try:
                session = requests.Session()
                url = "https://google.com"
                response = session.get(url, params={'id': file_id}, stream=True)
                
                token = None
                for key, value in response.cookies.items():
                    if key.startswith('download_warning'):
                        token = value
                        break
                
                if token:
                    response = session.get(url, params={'id': file_id, 'confirm': token}, stream=True)
                
                with open(file_name, "wb") as f:
                    for chunk in response.iter_content(chunk_size=32768):
                        if chunk:
                            f.write(chunk)
                            
            except Exception as e:
                st.error(f"Cloud server response error: {e}")
                st.stop()
                
    try:
        with open(file_name, 'rb') as f:
            return pickle.load(f)
    except pickle.UnpicklingError:
        if os.path.exists(file_name):
            os.remove(file_name)
        with st.spinner('Loading via Secure Connection backup...'):
            alt_url = f"https://google.com&id={file_id}&confirm=t"
            res = requests.get(alt_url, stream=True)
            with open(file_name, "wb") as f:
                f.write(res.content)
        return pickle.load(open(file_name, 'rb'))

# Execute data loading
movies_dict = load_movies_data()
movies = pd.DataFrame(movies_dict)
similarity = load_similarity()

# Movie Recommendation Logic
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
    'Select a movie you like:',
    movies['title'].values
)

# Render Button
if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)
    st.subheader('Top 5 recommended movies for you:')
    for i in recommendations:
        st.write(f"🍿 {i}")
