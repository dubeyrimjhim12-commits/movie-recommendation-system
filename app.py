import streamlit as st
import pickle
import pandas as pd
import requests
import os

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="centered")
st.title('🎬 Movie Recommendation System')

# 1. Local GitHub Repository se direct movies_dict.pkl load karne ka function
@st.cache_resource
def load_movies_data():
    file_name = "movies_dict.pkl"
    if os.path.exists(file_name):
        return pickle.load(open(file_name, 'rb'))
    else:
        st.error("GitHub repository par 'movies_dict.pkl' file nahi mili. Kripya use GitHub par upload karein.")
        st.stop()

# 2. Google Drive Large File Security Warning Bypass karke download karne ka function
@st.cache_resource
def load_similarity():
    # Google Drive confirmation string ke sath large file download url
    url = "https://google.com"
    file_name = "similarity.pkl"
    
    if not os.path.exists(file_name):
        with st.spinner('Model files cloud se load ho rahi hain (1-2 min lag sakte hain)...'):
            try:
                response = requests.get(url, stream=True)
                with open(file_name, "wb") as f:
                    for chunk in response.iter_content(chunk_size=32768):
                        if chunk:
                            f.write(chunk)
            except Exception as e:
                st.error(f"Cloud se download fail ho gaya: {e}")
                st.stop()
    return pickle.load(open(file_name, 'rb'))

# Data execute aur setup karna
try:
    movies_dict = load_movies_data()
    movies = pd.DataFrame(movies_dict)
    similarity = load_similarity()
except Exception as e:
    st.error(f"Website setup hone mein samay lag raha hai. Kripya page ko refresh karein. Error: {e}")
    st.stop()

# Recommendation Engine Logic
def recommend(movie):
    try:
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        
        recommended_movies = []
        for i in movies_list:
            recommended_movies.append(movies.iloc[i[0]].title)
        return recommended_movies
    except Exception:
        return ["Kripya koi dusri movie chunein."]

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
