import streamlit as st

import pickle
import pandas as pd
import numpy as np
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

session=requests.Session()
retry=Retry(connect=3, backoff_factor=0.5)
adapter=HTTPAdapter(max_retries=retry)
session.mount('http://',adapter)
session.mount('https://',adapter)


movies_list=pickle.load(open('movies.sav','rb')) ## Import the dataset
similarity=pickle.load(open('similarity.sav','rb')) ## Load the similarity matrix

def recommend(movie):
    movie_index=movies_list[movies_list['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list_sorted=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    
    recommended_movies=[]
    path=[]
    for i in movies_list_sorted:
        movie_id=i[0]

        print(movie_id)
        ## Fetch poster via API
        

        recommended_movies.append(movies_list.loc[i[0],'title'])

        movie_id=movies_list.loc[i[0], 'id']

        url=f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=7977e4c759daaa7b1f4f036bb3677293&language=en-US'

        response = session.get(url, timeout=10)
        data=response.json()
        print(data)

        poster_path=data.get('poster_path')
        full_path="https://image.tmdb.org/t/p/w500/"+poster_path
        path.append(full_path)

    return recommended_movies, path


movies=movies_list['title'].values ## Extracting only the title column

st.title("Movies Recommender System")

option=st.selectbox(
    'Movies List',
    movies)
st.write('You selected:', option)   

if st.button('Recommend'):
    recommendations=recommend(option)
    movies, poster=recommendations

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(movies[0])
        st.image(poster[0])
    with col2:      
        st.text(movies[1])
        st.image(poster[1])
    with col3:
        st.text(movies[2])
        st.image(poster[2])
    with col4:
        st.text(movies[3])
        st.image(poster[3])
    with col5:
        st.text(movies[4])
        st.image(poster[4])
    

