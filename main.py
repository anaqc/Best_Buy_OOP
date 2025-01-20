import movie_app
import storage_json
import storage_csv


def main():
    """ main function.
          This function serves as the primary entry point
          for the application.
          """
    storage = storage_csv.StorageCsv('movies.csv')
    movie_app_obj = movie_app.MovieApp(storage)
    movie_app_obj.run()

if __name__ == "__main__":
    main()