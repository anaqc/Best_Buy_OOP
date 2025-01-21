from storage.istorage import IStorage



class StorageCsv(IStorage):
    def __init__(self, file_path):
        self._file_path = file_path


    @property
    def file_path(self):
        return self._file_path


    @file_path.setter
    def file_path(self, new_file_path):
        self._file_path = new_file_path


    def read_movies_data(self):
        """
        This function reads all the data from _file_path and returns it.
        """
        try:
            with open(self.file_path, "r") as file_obj:
                return file_obj.readlines()
        except FileNotFoundError:
            return []


    def write_movies_data(self, data):
        """ This function write the data from movies_data
        """
        with open(self.file_path, "w") as file_obj:
            if len(data) == 0:
                file_obj.write(data)
            else:
                title, year, rating, poster = data[0].keys()
                file_obj.write(f"{title},{year},{rating},{poster}\n")
                for movie in data:
                    title_movie, year_movie, rating_movie, poster_movie = movie.values()
                    file_obj.write(f"{title_movie},{year_movie},{rating_movie},"
                                        f"{poster_movie}\n")


    def list_movies(self):
        """ Returns a dictionary of dictionaries that
        contains the movies information in the database.

        The function loads the information from the JSON
        file and returns the data. """

        data_movies = self.read_movies_data()
        list_data_movies = []
        if len(data_movies) == 0:
            return list_data_movies
        # First line for the dictionary keys
        dict_keys = data_movies[0]
        title, year, rating, poster = dict_keys.split(",")
        dict_values = data_movies[1:]
        for movie_value in dict_values:
            if movie_value.find(",") > 0:
                title_movie, year_movie, rating_movie, poster_movie = movie_value.strip().split(",")
                list_data_movies.append({title: title_movie, year: int(year_movie),
                                rating: float(rating_movie), poster.strip(): poster_movie.strip()})
        return list_data_movies


    def add_movie(self, title, year, rating, poster):
        """ Adds a movie to the movies database.
        Loads the information from the JSON file, add the movie,
        and saves it. The function doesn't need to validate the input.
        """
        data_movies = self.list_movies()
        data_movies.append({"movie name": title, "movie year": year,
                            "movie rating": float(rating), "poster": poster})
        self.write_movies_data(data_movies)



    def delete_movie(self,title):
        """
        Deletes a movie from the movies database.
        Loads the information from the JSON file, deletes the movie,
        and saves it. The function doesn't need to validate the input.
        """
        data_movies = self.list_movies()
        is_movie_name_found = False
        for movie in data_movies:
            if title.lower() == movie["movie name"].lower():
                is_movie_name_found = True
                data_movies.remove(movie)
                print(f"Movie {title} successfully deleted")
                break
        if not is_movie_name_found:
            print(f"Movie {title} doesn't exist!")
        self.write_movies_data(data_movies)


    def update_movie(self, title, rating):
        """
        Updates a movie from the movies database.
        Loads the information from the JSON file, updates the movie,
        and saves it. The function doesn't need to validate the input.
        """
        data_movies = self.list_movies()
        new_data_movies = []
        is_update = False
        for movie in data_movies:
            if title.lower() == movie["movie name"].lower():
                movie["movie rating"] = rating
                is_update = True
                print(f"The movie {title} successfully updated")
            new_data_movies.append(movie)
        if not is_update:
            print(f"Movie {title} doesn't exist!")
        self.write_movies_data(new_data_movies)