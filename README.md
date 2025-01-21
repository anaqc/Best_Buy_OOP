#  My Movie Project

A Python-based command-line application that allows users to search, store, and manage movie information using the OMDB API. The application supports both CSV and JSON storage formats for maintaining your personal movie database.

## Features

* Search movies using the OMDB API.
* Store movie information locally in CSV or JSON format.
* List all saved movies.
* Add new movies to the database.
* Delete movies from the database.
* Update existing movie information.
* View movie statistics.
* Get a random movie suggestion.
* Search through saved movies.
* Sort movies by rating.
* Sort movies by year.
* Generate a static website to display your movie collection.

## Prerequisites

* OMDB API key (Get it from OMDB API).

## Installation

1. Clone the repository: `git clone <repository-url>`.
2. Install required dependencies: `pip install -r requirements.txt`.
3. Create a .env file in the root directory and add your OMDB API key: `API_KEY=your_api_key_here`.

## Usage

1. To use this project, run the following command - `python main.py`.
2. You can show the generate website in `index.html`.
3. Use the menu options to:

    + List all movies in your database
    + Add new movies by searching the OMDB API
    + Delete unwanted movies
    + Update movie information
    + View statistics about your collection
    + Get random movie suggestions
    + Search through your saved movies
    + Sort movies by rating or year
    + Generate a website to showcase your collection

## Storage Options

The application supports two storage formats:
+ CSV: Stores movie data in a comma-separated values file
+ JSON: Stores movie data in a JSON format

## Web Interface

The application generates a clean and modern static website to showcase your movie collection. The web interface features:

+ Movie posters displayed in a responsive grid layout.
+ For each movie:

    + Movie poster image.
    + Movie title in clear typography.
    + Release year displayed below the title.

The website is automatically generated when you select the "generate website" option from the main menu.

## Contact

For questions, contact open an issue on the repository.py