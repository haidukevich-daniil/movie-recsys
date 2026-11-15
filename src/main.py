import os 
import pandas as pd
import time
from dotenv import load_dotenv

from src.tmdb_client import TMDBClient
from src.database import create_tables, save_movie, get_movie_info, get_movie_genres, get_movie_credits

load_dotenv()

TMDB_TOKEN = os.getenv("TMDB_READ_ACCESS_TOKEN")
TMDB_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

def check_movie(tmdb_id, client):
    movie = get_movie_info(tmdb_id)
    if movie is not None:
        return True

    result = client.get_movie_details(tmdb_id)
    if result is None:
        return False
    details, genres = result

    credits = client.get_movie_credits(tmdb_id)
    if credits is None:
        return False
    
    save_movie(details, genres, credits)
    return True

def loading(client, links):
    tmdb_ids = links["tmdbId"].dropna().astype(int)
    failed_ids = []

    for i, tmdb_id in enumerate(tmdb_ids, start=1):
        try:
            check_movie(tmdb_id, client)

        except Exception as e:
            print(f"Unexpected error for {tmdb_id}: {e}")
            failed_ids.append(tmdb_id)

        if i % 100 == 0:
            print(f"Processed {i}/{len(tmdb_ids)} movies")

        time.sleep(0.25)

    print("Collection finished!")
    print(f"Failed movies: {len(failed_ids)}")


def main():

    # links = pd.read_csv('data/raw/ml-latest-small/links.csv')
    # loading(client, links)

    create_tables()
    client = TMDBClient(TMDB_TOKEN, BASE_URL)

    #tmdb_id = 862
    # check_movie(tmdb_id, client)

    # info = get_movie_info(tmdb_id)
    # movie_genres = get_movie_genres(tmdb_id)
    # print(info, movie_genres)

    # credits = get_movie_credits(tmdb_id)
    # for person in credits:
    #     print(person)






if __name__ == "__main__":
    main()