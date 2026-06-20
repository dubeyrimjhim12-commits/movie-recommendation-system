import streamlit as st
import pickle
import pandas as pd
import requests
import os

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="centered")
st.title('🎬 Movie Recommendation System')

# 1. Local GitHub repository se movies_dict.pkl load karna
@st.cache_resource
def load_movies_data():
    file_name = "movies_dict.pkl"
    if os.path.exists(file_name):
        return pickle.load(open(file_name, 'rb'))
    else:
        st.error("GitHub par 'movies_dict.pkl' file nahi mili. Kripya use upload karein.")
        st.stop()

# 2. Google Drive Badi files virus scan verification bypass karke download karne ka function
@st.cache_resource
def load_similarity():
    file_id = "1Q7WFmIp8f_X_hhcrVkVTYuuOTIwpf4KN"
    file_name = "similarity.pkl"
    
    if not os.path.exists(file_name):
        with st.spinner('Model files cloud se load ho rahi hain (1-2 min lag sakte hain)...'):
            try:
                # Step A: Google Drive standard url framework call karna
                session = requests.Session()
                url = "https://docs.google.com/uc?export=download"
                response = session.get(url, params={'id': file_id}, stream=True)
                
                # Step B: Large file warning cookie confirm token check karna
                token = None
                for key, value in response.cookies.items():
                    if key.startswith('download_warning'):
                        token = value
                        break
                
                # Step C: Agar warning token mile toh use automatic confirm response ke sath download karna
                if token:
                    response = session.get(url, params={'id': file_id, 'confirm': token}, stream=True)
                
                # Step D: File ko locally write block mein binary chunk wise save karna
                with open(file_name, "wb") as f:
                    for chunk in response.iter_content(chunk_size=32768):
                        if chunk:
                            f.write(chunk)
                            
            except Exception as e:
                st.error(f"Cloud server response error: {e}")
                st.stop()
                
    # Verifying file content standard layout format
    try:
        with open(file_name, 'rb') as f:
            return pickle.load(f)
    except pickle.UnpicklingError:
        # Agar token fail ho toh alternative direct secure link backup execute karna
        if os.path.exists(file_name):
            os.remove(file_name) # Purani corrupted file clear karna
        with st.spinner('Bypass Secure Connection load ho raha hai...'):
            alt_url = f"https://docs.google.com/uc?export=download&id={file_id}&confirm=t"
            res = requests.get(alt_url, stream=True)
            with open(file_name, "wb") as f:
                f.write(res.content)
        return pickle.load(open(file_name, 'rb'))

# Data execute aur run karna
movies_dict = load_movies_data()
movies = pd.DataFrame(movies_dict)
similarity = load_similarity()

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
