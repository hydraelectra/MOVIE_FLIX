import streamlit as st
import pandas as pd
import requests
import pickle

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=2eadc8b6a65a69c13138f0eee094101b&language=en-US"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        poster_path = data['poster_path']
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster for movie ID {movie_id}: {e}")
        return "https://via.placeholder.com/150?text=No+Image"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Updated path for similarity.pkl
similarity = pickle.load(open('movieflix/data/similarity.pkl', 'rb'))

st.title('Movieflix')

selected_movie_name = st.selectbox(
    'How Would you like to recommend?',
    movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])