
"""
import requests
try:
    API_KEY = "1b95df6b"
    MOVIE_NAME = "hhhhhhhh"
    URL = f"http://www.omdbapi.com/?apikey={API_KEY}&t={MOVIE_NAME}"
    res_countries = requests.get(URL)
    data_movie = res_countries.json()
    if data_movie.get("Response") == "False":
        raise KeyError(data_movie.get('Error', 'Unknown error'))

    print(data_movie)
    print(data_movie["Title"])
    print(data_movie["Year"])
    print(data_movie["imdbRating"])
    print(data_movie["Poster"])
except KeyError as e:
    print(e)
"""



