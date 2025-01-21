from app import movie_app
from storage import storage_csv, storage_json


def main():
    """ main function.
          This function serves as the primary entry point
          for the application.
          """
    storage = storage_csv.StorageCsv('data/movies.csv')
    storage2 = storage_json.StorageJson("data/movie.json")
    movie_app_obj = movie_app.MovieApp(storage2)
    movie_app_obj.run()

if __name__ == "__main__":
    main()