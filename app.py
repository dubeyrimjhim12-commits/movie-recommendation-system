import streamlit as st
import pickle
import pandas as pd
import requests
import os

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="centered")
st.title('🎬 Movie Recommendation System')

# Movies dictionary load karna
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Google Drive se similarity.pkl download karne ka automatic function
@st.cache_resource
def load_similarity():
    url = "https://google.com"
    file_name = "similarity.pkl"
    
    if not os.path.exists(file_name):
        with st.spinner('Model files load ho rahi hain, kripya thoda intezar karein...'):
            response = requests.get(url)
            with open(file_name, "wb") as f:
                f.write(response.content)
    return pickle.load(open(file_name, 'rb'))

try:
    similarity = load_similarity()
except Exception as e:
    st.error("Model load karne mein dikkat aa rahi hai.")
    st.stop()

# Recommendation Function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x)[1:6]
    
    recommended_movies = []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i].title)
    return recommended_movies

# Dropdown Menu
selected_movie_name = st.selectbox(
    'Apni pasandida movie chunein:',
    movies['title'].values
)

# Button click karne par recommendation dikhana
if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)
    st.subheader('Aapke liye top 5 movies:')
    for i in recommendations:
        st.write(f"🍿 {i}")
