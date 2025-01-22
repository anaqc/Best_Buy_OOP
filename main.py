import sys
from app import movie_app
from storage import storage_csv, storage_json


def main():
    """ main function.
          This function serves as the primary entry point
          for the application.
          """
    file_name = sys.argv[1]
    if file_name.endswith(".csv"):
        storage = storage_csv.StorageCsv(f'data/{file_name}')
        movie_app_obj = movie_app.MovieApp(storage)
        movie_app_obj.run()
    elif file_name.endswith(".json"):
        storage = storage_json.StorageJson(f"data/{file_name}")
        movie_app_obj = movie_app.MovieApp(storage)
        movie_app_obj.run()
    else:
        print("Error File")


if __name__ == "__main__":
    main()