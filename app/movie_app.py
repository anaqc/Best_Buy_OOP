import statistics
import random
import requests
import os
from dotenv import load_dotenv


# Load Environment Variables
load_dotenv()


class MovieApp:

    # Class variables
    MAX_RATING = 8
    MIN_RATING = 2
    # Request variables
    API_KEY = os.getenv("API_KEY")
    URL = "http://www.omdbapi.com/?apikey="
    # content HTML
    HTML_TEMPLATE = "static/index_template.html"
    NEW_FILE_PATH = "static/index.html"


    def __init__(self, storage):
        self._storage = storage


    @property
    def storage(self):
        return self._storage


    @storage.setter
    def storage(self, new_storage):
        self._storage = new_storage


    def _command_list_movies(self):
        """ This function print the movies from datamovies"""
        data_movies = self.storage.list_movies()
        if len(data_movies) != 0:
            for movie in data_movies:
                print(f"{movie['movie name']} ({movie['movie year']}): {movie['movie rating']}")
        else:
            print(f"{self.storage.file_path} is clear")


    def _command_movie_stats(self):
        """ This function print statistics about the movies in the database
        """
        stats_movies = self._get_stats()
        print(f"Average ratting: {stats_movies['average_rating']}")
        print(f"Median rating: {stats_movies['median_rating']}")
        print("Best movies:")
        if len(stats_movies["best_movies"]) >= 1:
            for movie in stats_movies["best_movies"]:
                print(f"{movie['movie name']}, {movie['movie rating']}")
        else:
            print(f"Rating movies is not in grater than {stats_movies['max_rating']}")
        print("Worst movies")
        if len(stats_movies["worst_movies"]) >= 1:
            for movie in stats_movies["worst_movies"]:
                print(f"{movie['movie name']}, {movie['movie rating']}")
        else:
            print(f"Rating movies is not less than {stats_movies['min_rating']}")

    def _request_movie_API(self, movie_name):
        """ Fetch movie details from the API based on the movie name
        """
        url_search_movie_by_name = f"{MovieApp.URL}{MovieApp.API_KEY}&t={movie_name}"
        try:
            res_movie = requests.get(url_search_movie_by_name)
            res_movie.raise_for_status()
            data_movie = res_movie.json()
            if data_movie.get("Response") == "False":
                raise KeyError(f"Didn't find movie {movie_name} in the API")
            return data_movie
        except requests.exceptions.ConnectionError:
            print("Error: Unable to connect to the API. Please check your internet connection.")
        except requests.exceptions.Timeout:
            print("Error: The request timed out. Please try again later.")
        except KeyError as e:
            print(e)


    def _command_input_new_movie(self):
        """ This function ask the values for a new movie, the focus is on interacting
        with the user to gather details and check for duplicates.
        """
        data_movies = self.storage.list_movies()
        movie_name = get_validate_name_movie()
        requests_data_movie = self._request_movie_API(movie_name)
        is_name_in_data_movie = False
        if requests_data_movie != None:
            if len(data_movies) > 0:
                for movie in data_movies:
                    if movie_name.lower() == movie["movie name"].lower():
                            is_name_in_data_movie = True
            if not is_name_in_data_movie:
                movie_title = requests_data_movie.get("Title")
                movie_year = requests_data_movie.get("Year")
                movie_rating = requests_data_movie.get("imdbRating")
                movie_poster = requests_data_movie.get("Poster")
                movie_imdbID = requests_data_movie.get("imdbID")
                self.storage.add_movie(movie_title, movie_year, movie_rating, movie_poster,
                                       movie_imdbID)
                print(f"Movie {movie_name} successfully added")
            else:
                print(f"Movie {movie_name} already exist!")


    def _command_input_delete_movie(self):
        """ This function take the movie name input and delete the movie
        """
        name_movie = input("Enter a movie name: ")
        self.storage.delete_movie(name_movie)


    def _command_input_update_movie(self):
        """ This function update the movie by name
        """
        name_movie = input("Enter movie name: ")
        new_rating = get_validate_rating()
        movie_notes = input("Enter Movie note: ")
        self.storage.update_movie(name_movie, new_rating, movie_notes)


    def _get_stats(self):
        """ This function calculate statistics about the movies in the database
        """
        data_movies = self.storage.list_movies()
        list_rating = [movie["movie rating"] for movie in data_movies]
        # Average rating in the database.
        average_rating = f"{sum(list_rating) / len(list_rating):.1f}"
        # Median rating in the database
        median_rating = statistics.median(list_rating)
        # The best movie by rating
        best_movies = [movie for movie in data_movies if movie["movie rating"]
                       >= MovieApp.MAX_RATING]
        # The worst movie by rating.
        worst_movies = [movie for movie in data_movies if movie["movie rating"]
                        <= MovieApp.MIN_RATING]
        return {
            "average_rating": average_rating,
            "median_rating": median_rating,
            "best_movies": best_movies,
            "worst_movies": worst_movies,
            "max_rating": MovieApp.MAX_RATING,
            "min_rating": MovieApp.MIN_RATING
        }

    def _random_movie(self):
        """ This function show a random movie information
        """
        data_movies = self.storage.list_movies()
        choice_movie = random.choice(data_movies)
        print(f"You movie tonight: {choice_movie['movie name']} "
              f"it's rated {choice_movie['movie rating']}")


    def _search_part_movie_name(self):
        """ TAsk the user to enter a part of a movie name,
        and then search all the movies in the database
        """
        data_movies = self.storage.list_movies()
        searched_name_movie = input("Enter a movie name: ")
        is_movie_found = False
        for movie in data_movies:
            if searched_name_movie.lower() in movie["movie name"].lower():
                print(f"{movie['movie name']} ({movie['movie year']}): {movie['movie rating']}")
                is_movie_found = True
        if not is_movie_found:
            print("movie is not found")


    def _movies_sorted_by_rating(self):
        """ This function sorted the movies by rating increment or decrement
        """
        data_movies = self.storage.list_movies()
        func_rating = lambda x: x["movie rating"]
        while True:
            reverse_sorted = input("Do you want the movies by increment order? (Y/N) ")
            if reverse_sorted.lower() == "n":
                sorted_movies = sorted(data_movies, key=func_rating, reverse=True)
                for movie in sorted_movies:
                    print(f"{movie['movie name']} ({movie['movie year']}): {movie['movie rating']}")
                break
            elif reverse_sorted.lower() == "y":
                sorted_movies = sorted(data_movies, key=func_rating, reverse=False)
                for movie in sorted_movies:
                    print(f"{movie['movie name']} ({movie['movie year']}): {movie['movie rating']}")
                break
            print("Please enter 'Y' or 'N'")


    def _movies_sorted_by_year(self):
        """ This function sorted the movies by year increment or decrement
        """
        data_movies = self.storage.list_movies()
        func_year = lambda x: x["movie year"]
        while True:
            reverse_sorted = input("Do you want the movies by increment order? (Y/N) ")
            if reverse_sorted.lower() == "n":
                sorted_movies = sorted(data_movies, key=func_year, reverse=True)
                for movie in sorted_movies:
                    print(f"{movie['movie name']} ({movie['movie year']}): {movie['movie rating']}")
                break
            elif reverse_sorted.lower() == "y":
                sorted_movies = sorted(data_movies, key=func_year, reverse=False)
                for movie in sorted_movies:
                    print(f"{movie['movie name']} ({movie['movie year']}): {movie['movie rating']}")
                break
            print("Please enter 'Y' or 'N'")

    def _generate_website(self):
        """ This function generate a website from the data movie generated by user"""
        max_quantity_movies_rows = 8
        name_file_without_package = self.storage.file_path.split("/")[1]
        name_file = name_file_without_package.split(".")[0]
        data_movie = self.storage.list_movies()
        html_content = self.read_template(MovieApp.HTML_TEMPLATE)
        web_title = f"{name_file.capitalize()} Movies List"
        html_content_with_title = html_content.replace("__TEMPLATE_TITLE__", web_title)
        output = ""
        if len(data_movie) == 0:
            output += self.movie_data_not_found()
        else:
            output += "<ol class='movie-grid'>\n"
            for index, movie in enumerate(data_movie, 1):
                output += self.serialize_movie(movie)
                if index % max_quantity_movies_rows == 0:
                    output += "</ol>\n <ol class='movie-grid'>\n"

            output += "</ol>"
        new_html_content = html_content_with_title.replace("__TEMPLATE_MOVIE_GRID__", output)
        self.write_new_content(MovieApp.NEW_FILE_PATH, new_html_content)
        print(f"Website was successfully generated to the file {MovieApp.NEW_FILE_PATH}")


    def write_new_content(self, file_path, content):
        """ This function write the create website """
        with open(file_path, "w") as f:
            f.write(content)


    def serialize_movie(self, movie):
        """ This function handle a single movie serialization
        """
        title = movie.get('movie name')
        year = movie.get('movie year')
        note = movie.get('movie note')
        rating = movie.get('movie rating')
        poster = movie.get('poster')
        imdbID = movie.get('movie imdbID', "")
        # define a empty string
        output = ""
        star_output = ""
        # append information for each string
        output += "<li>\n"
        output += "<div class='movie'>\n\t"
        output += f"<a href='https://www.imdb.com/de/title/{imdbID}'>\n\t\t\t"
        output += f"<img class='movie-poster' src={poster} title=''/>\n\t\t"
        output += "</a>\n\t\t"
        output += f"<div class='movie-title'>{title}</div>\n\t\t"
        output += f"<div class='movie-year'>{year}</div>\n\t\t"
        # divide the rating to print the stars
        star_rating = rating // 2
        for star in range(1, 6):
            if star <= star_rating:
                star_output += "<span class='fa fa-star checked'></span>"
            else:
                star_output += "<span class='fa fa-star'></span>"
        output += f"<div class='movie-rating'>{star_output}  </div>\n\t"

        if note and note != "":
            output += f"<div class='movie-note'>{note}</div>\n\t\t"

        output += "</div>\n"
        output += "</li>"
        return output

    def movie_data_not_found(self):
        """ This function create a new site if the data movie is clear"""
        output = ""
        output += "<li>\n"
        output += "<div class='movie'>\n\n"
        output += "<h3> Movies not Found in data </h3>\n"
        output += "</div>"
        output += "</li>"
        return output


    def read_template(self, file_path):
        """ This. function reads an HTML template from the given file path
        """
        try:
            if file_path.lower().endswith(".html"):
                with open(file_path, "r") as handle:
                    return handle.read().strip()
            raise ValueError(f"{file_path} is not HTML file")
        except ValueError as e:
            print(e)
        except FileNotFoundError:
            print(f"File {file_path} not found")


    def run(self):
        """
        Print menu
        Get use command
        Execute command
        """

        print("**************** My Movies Database ****************")
        while True:
            self.print_menu_movie()
            user_choice = input("Enter choice (0-10): ")
            if user_choice.isdigit() and 0 <= int(user_choice) <= 10:
                self.get_menu_user()[int(user_choice)]["function"]()
            else:
                print("Invalid choice")
            print("Press ENTER to view  the menu")
            input()
            os.system('clear')


    def get_menu_user(self):
        """ This function get the menu user as list of dictionaries
        """
        menu = [
            {
                "name": "Exit",
                "function": function_exit,
                "description": "Exit from menu"
            },
            {
                "name": "List movies",
                "function": self._command_list_movies,
                "description": "Shows a list of movies"
            },
            {
                "name": "Add movie",
                "function": self._command_input_new_movie,
                "description": "Add a new movie in movies_data"
            },
            {
                "name":"Delete movie",
                "function": self._command_input_delete_movie,
                "description": "delete a movie by name"
            },
            {
                "name": "Update movie",
                "function": self._command_input_update_movie,
                "description": "update a movie by name"
            },
            {
                "name":"Stats",
                "function": self._command_movie_stats,
                "description": "Print statistics about the movies in the database"
            },
            {
                "name": "Random movie",
                "function": self._random_movie,
                "description": "show a random movie"
            },
            {
                "name": "Search movie",
                "function": self._search_part_movie_name,
                "description": "search a movie by name"
            },
            {
                "name": "Movies sorted by rating",
                "function": self._movies_sorted_by_rating,
                "description": "sorted the movies by rating"
            },
            {
                "name": "Movies sorted by year",
                "function": self._movies_sorted_by_year,
                "description": "sorted the movies by year"
            },
            {
                "name": "generate website",
                "function": self._generate_website,
                "description": "generate website"
            }
        ]
        return menu


    def print_menu_movie(self):
        """ This function print the menu movie
        """
        menus = self.get_menu_user()
        print("Menu")
        for index, menu in enumerate(menus):
            print(f"{index}. {menu['name']}")


def function_exit():
    """ This function exit from the program
    """
    print("Bye!")
    exit()


def get_validate_year():
    """ This function validate the movie year
    """
    while True:
        movie_year = input("Enter a new movie year ")
        if movie_year.isdigit() and int(movie_year) >= 0:
            return int(movie_year)
        print("Enter a valid year")


def get_validate_rating():
    """This function validate the movie rating
    """
    while True:
        try:
            movie_rating = float(input("Enter new movie rating: "))
            break
        except ValueError:
            print("Please enter a valid rating")
    return movie_rating


def get_validate_name_movie():
    """ This function validate the movie year
    """
    while True:
        movie_name = input("Enter new movie name: ")
        if len(movie_name) > 0:
            return movie_name
        print("Enter a valid name")

