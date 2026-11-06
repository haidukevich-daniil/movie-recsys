import os 
from dotenv import load_dotenv

from src.tmdb_client import TMDBClient 
from src.database import create_tables, save_movie, get_movie_info, get_movie_genres

load_dotenv()

TMDB_TOKEN = os.getenv("TMDB_READ_ACCESS_TOKEN")
TMDB_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

def main():
    create_tables()

    client = TMDBClient(TMDB_TOKEN, BASE_URL)
    details, genres = client.get_movie_details(550)

    save_movie(details, genres)

    info = get_movie_info(550)
    movie_genres = get_movie_genres(550)
    print(info, movie_genres)




if __name__ == "__main__":
    main()