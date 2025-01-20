import statistics
import random


class MovieApp:

    # Class variables
    MAX_RATING = 9.8
    MIN_RATING = 2


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


    def _command_input_new_movie(self):
        """ This function ask the values for a new movie, the focus is on interacting
        with the user to gather details and check for duplicates.
        """
        data_movies = self.storage.list_movies()
        movie_name = get_validate_name_movie()
        is_name_in_data_movie = False
        if len(data_movies) > 0:
            for movie in data_movies:
                if movie_name.lower() == movie["movie name"].lower():
                    is_name_in_data_movie = True

        if not is_name_in_data_movie:
            movie_year = get_validate_year()
            movie_rating = get_validate_rating()
            movie_poster = input("Enter a poster:")
            self.storage.add_movie(movie_name, movie_year, movie_rating, movie_poster)
            print(f"Movie {movie_name} successfully added")
        else:
            print(f"Movie {movie_name} already exist!")


    def _command_input_delete_movie(self):
        """ This function delete the movie by name
        """
        name_movie = input("Enter a movie name: ")
        self.storage.delete_movie(name_movie)


    def _command_input_update_movie(self):
        """ This function update the movie by name
        """
        name_movie = input("Enter movie name: ")
        new_rating = get_validate_rating()
        self.storage.update_movie(name_movie, new_rating)


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
        ...

    def run(self):
        # Print menu
        # Get use command
        # Execute command
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
                "name": "_generate_website",
                "function": self._generate_website,
                "description": "s_generate_website"
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
            movie_rating = float(input("Enter new movie rating "))
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

