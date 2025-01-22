from storage.istorage import IStorage
import json


class StorageJson(IStorage):
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
                return json.loads(file_obj.read())
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print(f"Error: The file {self.file_path} contains invalid JSON.")
            return []  # Return an empty list if the JSON is invalid
        except Exception as e:
            print(f"An unexpected error occurred while reading the file: {e}")
            return []


    def write_movies_data(self, data):
        """ This function write the data from movies_data
        """
        json_str = json.dumps(data, indent=4)
        with open(self.file_path, "w") as file_obj:
            return file_obj.write(json_str)


    def list_movies(self):
        """ Returns a dictionary of dictionaries that
        contains the movies information in the database.

        The function loads the information from the JSON
        file and returns the data. """
        data_movies = self.read_movies_data()
        return data_movies


    def add_movie(self, title, year, rating, poster, imdbID):
        """ Adds a movie to the database.
        Loads the information from the JSON file, add the movie,
        and saves it. The function doesn't need to validate the input.
        """
        data_movies = self.list_movies()
        data_movies.append({"movie name": title, "movie year": int(year),
                            "movie rating": float(rating), "poster": poster, "movie imdbID":imdbID})
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


    def update_movie(self, title, rating, notes):
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
                movie["movie note"] = notes
                is_update = True
                print(f"The movie {title} successfully updated")
            new_data_movies.append(movie)
        if not is_update:
            print(f"Movie {title} doesn't exist!")
        self.write_movies_data(new_data_movies)


